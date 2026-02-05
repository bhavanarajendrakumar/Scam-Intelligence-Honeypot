from flask import Flask, jsonify, request

app = Flask(__name__)

API_KEY = "hello"

@app.route("/analyze", methods=["POST"])
def analyze():
    api_key = request.headers.get("x-api-key")
    if api_key != API_KEY:
        return jsonify({"error": "Unauthorized"}), 401

    data = request.get_json(force=True)

    if "message" in data and isinstance(data["message"], dict):
        message = data["message"].get("text", "").lower()
    else:
        message = data.get("message", "").lower()

    if not message:
        return jsonify({"error": "Invalid request"}), 400

    if "block" in message or "suspend" in message:
        reply_text = "Why is my account being suspended?"
    elif "otp" in message:
        reply_text = "Why do you need my OTP?"
    else:
        reply_text = "Can you explain more?"

    return jsonify({
        "status": "success",
        "reply": reply_text
    }), 200
