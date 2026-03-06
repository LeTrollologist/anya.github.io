import os
import random
import requests
from flask import Flask, request, jsonify, send_from_directory

app = Flask(__name__)

# --- CONFIGURATION ---
ANYA_MESSAGES = [
    "I love you mostest times infinity times perpetuity 💖",
    "I love you more than chocos 🍫❤️",
    "Forever and always, my heart is yours 💞",
    "You are my sun, moon, and stars 🌞🌙✨",
    "My world is better with you in it 🌸"
]

@app.route("/")
def index():
    return send_from_directory('.', 'checkin.html')

@app.route("/api/checkin", methods=["POST"])
def api_checkin():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "No data received"}), 400
            
        target = data.get("type")
        
        # Determine Webhook URL from Render Env Vars
        if target == "anya":
            msg = random.choice(ANYA_MESSAGES)
            url = os.environ.get("WEBHOOK_ANYA")
        elif target == "micheal":
            msg = "💙 Micheal has checked in with love!"
            url = os.environ.get("WEBHOOK_MICHEAL")
        else:
            msg = "🌟 Someone has paid their respects!"
            url = os.environ.get("WEBHOOK_RANDOM")

        # LOGGING FOR DEBUGGING
        if not url:
            print(f"!!! CONFIG ERROR: WEBHOOK_{target.upper()} is not set in Render Environment Variables.")
            return jsonify({"error": f"Webhook for {target} not configured"}), 500

        print(f"Sending message for {target} to Discord...")

        # The actual POST to Discord
        # We use a 10-second timeout to prevent hanging
        resp = requests.post(url, json={"content": msg}, timeout=10)
        
        if resp.status_code in [200, 204]:
            print("Message sent successfully!")
            return jsonify({"message": msg}), 200
        else:
            print(f"Discord Error ({resp.status_code}): {resp.text}")
            return jsonify({"error": "Discord rejected the message"}), 502

    except Exception as e:
        print(f"CRITICAL SERVER ERROR: {str(e)}")
        return jsonify({"error": "Internal Server Error", "details": str(e)}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
