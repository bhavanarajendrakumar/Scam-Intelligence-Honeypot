conversations = {}
API_KEY = "hello"

@app.route("/analyze", methods=["POST"])
def analyze():
    api_key = request.headers.get("x-api-key")

    if api_key != API_KEY:
        return jsonify({"error": "Unauthorized"}), 401

    data = request.get_json()

    if not data or "message" not in data:
        return jsonify({"error": "Invalid request format"}), 400

    message = str(data["message"]).lower()
    convo_id = data.get("conversation_id", "default")

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
    convo["history"].append(message)
    convo["turn_count"] += 1

    extract_intel(message, convo)
    convo["extracted"]["urls"] = list(set(convo["extracted"]["urls"]))

    is_scam = detect_scam_intent(message)
    convo["scam_detected"] = is_scam

    scam_type = "Potential phishing" if is_scam else "Benign message"

    response = {
        "is_scam": is_scam,
        "confidence_score": 0.85 if is_scam else 0.15,
        "scam_type": scam_type,
        "extracted_entities": {
            "phone_numbers": [],
            "urls": convo["extracted"]["urls"],
            "bank_names": []
        }
    }

    return jsonify(response), 200
