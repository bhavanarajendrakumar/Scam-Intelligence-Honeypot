from flask import Flask, jsonify, request

app = Flask(__name__)

API_KEY = "hello"

@app.route("/analyze", methods=["POST"])
def analyze():
    try:
        api_key = request.headers.get("x-api-key")
        if api_key != API_KEY:
            return jsonify({"error": "Unauthorized"}), 401

        data = request.get_json(force=True)

        # ---- FIX FOR HACKATHON TESTER FORMAT ----
        # They send: { sessionId, message: { text: "..."} }
        if "message" in data and isinstance(data["message"], dict):
            message = data["message"].get("text", "").lower()
        else:
            message = data.get("message", "").lower()
        # ----------------------------------------

        if not message:
            return jsonify({"error": "Invalid request format"}), 400

        # Decide reply (honeypot logic)
        if "block" in message or "suspend" in message:
            reply_text = "Why is my account being suspended?"
        elif "otp" in message:
            reply_text = "Why do you need my OTP?"
        else:
            reply_text = "Can you explain more?"

        # ---- EXACT EXPECTED OUTPUT ----
        return jsonify({
            "status": "success",
            "reply": reply_text
        }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
