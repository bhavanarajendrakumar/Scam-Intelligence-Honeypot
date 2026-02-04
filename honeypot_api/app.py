import re
from flask import Flask, jsonify, request

app = Flask(__name__)
@app.route("/")
def home():
    return "Scam Intelligence Honeypot is Live! 🚀"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)

API_KEY = "hello"

conversations = {}

# Scam Intent Detection
def detect_scam_intent(message):
    scam_patterns = [
        r'otp',
        r'account.*block',
        r'urgent.*action',
        r'click.*link',
        r'prize|lottery|winner',
        r'kyc.*update',
        r'upi.*send',
        r'verify.*bank',
        r'limited.*offer',
        r'password.*reset'
    ]

    for pattern in scam_patterns:
        if re.search(pattern, message):
            return True
    return False

# Intelligence Extraction
def extract_intel(message, convo):
    urls = re.findall(r'https?://\S+|www\.\S+', message)
    upi_ids = re.findall(r'\b[\w.-]+@[\w.-]+\b', message)
    bank_accounts = re.findall(r'\b\d{9,18}\b', message)

    convo["extracted"]["urls"].extend(urls)
    convo["extracted"]["upi_ids"].extend(upi_ids)
    convo["extracted"]["bank_accounts"].extend(bank_accounts)

    # Remove duplicates
    convo["extracted"]["urls"] = list(set(convo["extracted"]["urls"]))
    convo["extracted"]["upi_ids"] = list(set(convo["extracted"]["upi_ids"]))
    convo["extracted"]["bank_accounts"] = list(set(convo["extracted"]["bank_accounts"]))

# Honey-Pot Agent Persona
def honey_pot_agent_reply(history):
    prompts = [
        "Oh okay… I am not very good with these things. Can you help me step by step?",
        "I don't understand where to click. Can you send the full link?",
        "Is this my bank account or your company account?",
        "My son usually handles this… what details do you need exactly?",
        "It is asking for account number… should I enter mine or yours?",
        "The payment page opened. It shows a UPI ID… is that correct?",
        "I got a message saying transaction failed. Can you send the details again?",
        "I am a bit confused. Which bank account should I transfer to?",
    ]

    return prompts[len(history) % len(prompts)]


@app.route("/analyze", methods=["POST"])
def analyze():
    api_key = request.headers.get("x-api-key")

    if api_key != API_KEY:
        return jsonify({"error": "Unauthorized"}), 401

    data = request.get_json()

    if not data or "message" not in data:
        return jsonify({"error": "Invalid request format"}), 400

    message = data["message"].lower()
    convo_id = data.get("conversation_id", "default")

    # Create new conversation if not exists
    if convo_id not in conversations:
        conversations[convo_id] = {
            "history": [],
            "scam_detected": False,
            "agent_active": False,
            "extracted": {
                "urls": [],
                "upi_ids": [],
                "bank_accounts": []
            },
            "turn_count": 0
        }

    convo = conversations[convo_id]

    # Update conversation
    convo["history"].append(message)
    convo["turn_count"] += 1

    # Extract intelligence from incoming message
    extract_intel(message, convo)

    # Detect scam and activate agent if needed
    if not convo["scam_detected"] and detect_scam_intent(message):
        convo["scam_detected"] = True
        convo["agent_active"] = True

    # Generate response
    if convo["agent_active"]:
        reply = honey_pot_agent_reply(convo["history"])
        result = "SCAM !"
    else:
        reply = "Okay, can you explain more?"
        result = "SAFE MESSAGE"

    return jsonify({
        "received_message": message,
        "result": result,
        "scam_detected": convo["scam_detected"],
        "agent_active": convo["agent_active"],
        "response_message": reply,
        "engagement_metrics": {
            "turn_count": convo["turn_count"]
        },
        "extracted_intelligence": convo["extracted"]
    })


# 🚀 Required for deployment
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)


