from flask import Flask, jsonify, request
import re

app = Flask(__name__)

API_KEY = "hello"
conversations = {}

def detect_scam_type(message):
    if re.search(r'otp|upi', message):
        return "otp_scam"
    elif re.search(r'account.*(block|suspend)', message):
        return "account_block_scam"
    elif re.search(r'click.*link|verify', message):
        return "phishing_scam"
    else:
        return "unknown"

def generate_honeypot_reply(scam_type):
    replies = {
        "otp_scam": "Why do you need my OTP?",
        "account_block_scam": "Why is my account being suspended?",
        "phishing_scam": "Where exactly should I click?",
        "unknown": "Can you explain this more clearly?"
    }
    return replies.get(scam_type, "I don’t understand your message.")

@app.route("/analyze", methods=["POST"])
def analyze():
    api_key = request.headers.get("x-api-key")
    if api_key != API_KEY:
        return jsonify({"error": "Unauthorized"}), 401

    data = request.get_json()
    if not data or "message" not in data:
        return jsonify({"error": "Invalid request format"}), 400

    message = data["message"].lower()
    convo_id = data.get("sessionId", "default")

    if convo_id not in conversations:
        conversations[convo_id] = {"history": []}

    conversations[convo_id]["history"].append(message)

    scam_type = detect_scam_type(message)

    reply = generate_honeypot_reply(scam_type)

    return jsonify({
        "status": "success",
        "reply": reply
    }), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
