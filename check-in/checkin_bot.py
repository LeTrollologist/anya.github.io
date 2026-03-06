import os
import random
import requests
from flask import Flask, request, jsonify, send_from_directory

app = Flask(__name__)

# --- CONFIGURATION ---
# These must be set in Render Environment Variables
WEBHOOK_ANYA = os.getenv("WEBHOOK_ANYA")
WEBHOOK_MICHEAL = os.getenv("WEBHOOK_MICHEAL")
WEBHOOK_RANDOM = os.getenv("WEBHOOK_RANDOM")

ANYA_MESSAGES = [
    "I love you mostest times infinity times perpetuity 💖",
    "I love you more than chocos 🍫❤️",
    "Forever and always, my heart is yours 💞",
    "You are my sun, moon, and stars 🌞🌙✨",
    "My world is better with you in it 🌸",
    "I adore you endlessly ❤️"
]

@app.route("/")
def index():
    # Serves the beauty UI
    return send_from_directory('.', 'checkin.html')

@app.route("/api/checkin", methods=["POST"])
def api_checkin():
    try:
        data = request.json
        target = data.get("type")
        
        # Select target details
        if target == "anya":
            msg = random.choice(ANYA_MESSAGES)
            url = WEBHOOK_ANYA
        elif target == "micheal":
            msg = "💙 Micheal has checked in with love!"
            url = WEBHOOK_MICHEAL
        else:
            msg = "🌟 Someone has paid their respects!"
            url = WEBHOOK_RANDOM

        if not url:
            return jsonify({"status": "error", "message": "Config Missing"}), 500

        # Send to Discord via Webhook
        res = requests.post(url, json={"content": msg}, timeout=10)
        
        if res.status_code in [200, 204]:
            return jsonify({"status": "success", "message": "Message Sent!"}), 200
        else:
            return jsonify({"status": "error", "message": "Discord Busy"}), 500

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == "__main__":
    # Standard Flask runner
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
