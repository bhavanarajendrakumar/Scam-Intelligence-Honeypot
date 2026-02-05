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

        if not data or "message" not in data:
            return jsonify({"error": "Invalid request format"}), 400

        message = data["message"].lower()

        # Simple logic to decide reply (you can improve later)
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

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
