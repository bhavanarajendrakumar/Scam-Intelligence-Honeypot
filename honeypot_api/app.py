@app.route("/analyze", methods=["POST"])
def analyze():
    api_key = request.headers.get("x-api-key")

    if api_key != API_KEY:
        return jsonify({"error": "Unauthorized"}), 401

    data = request.get_json()

    if not data or "message" not in data:
        return jsonify({"error": "Invalid request format"}), 400

    message = str(data["message"]["text"]).lower()
    convo_id = data.get("sessionId", "default")

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

   
    response = {
        "status": "success",
        "reply": "Why is my account being suspended?"
    }

    return jsonify(response), 200
