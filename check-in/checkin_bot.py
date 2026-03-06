import os
import random
import requests
from flask import Flask, request, jsonify, send_from_directory

app = Flask(__name__)

# --- THE MESSAGE POOL ---
ANYA_MESSAGES = [
    "I love you mostest times infinity! 💖",
    "I love you mostest times infinity times perpetuity! 💖",
    "You are my sunshine every day ☀️💕",
    "Forever and always, my heart is yours 💞",
    "You're my favorite human in the universe 🌌💖",
    "I love you more than chocos! 🍫❤️"
]

@app.route("/")
def index():
    # Serves the checkin.html file
    return send_from_directory('.', 'checkin.html')

@app.route("/api/checkin", methods=["POST"])
def api_checkin():
    try:
        data = request.get_json()
        target = data.get("type")
        
        # 1. Get the Webhook URL from Render Environment Variables
        # IMPORTANT: These must be the FULL URLs from Discord
        if target == "anya":
            url = os.environ.get("WEBHOOK_ANYA")
            msg = random.choice(ANYA_MESSAGES)
        elif target == "micheal":
            url = os.environ.get("WEBHOOK_MICHEAL")
            msg = "💙 Micheal has checked in with love!"
        else:
            url = os.environ.get("WEBHOOK_RANDOM")
            msg = "🌟 Someone has paid their respects!"

        # 2. Check if the URL exists
        if not url or not url.startswith("http"):
            print(f"!!! CONFIG ERROR: WEBHOOK_{target.upper()} is missing or invalid!")
            return jsonify({"error": f"Webhook for {target} not configured properly"}), 400

        # 3. Send to Discord
        print(f"Sending to Discord for {target}...")
        resp = requests.post(url, json={"content": msg}, timeout=10)
        
        if resp.status_code in [200, 204]:
            return jsonify({"message": msg}), 200
        else:
            print(f"Discord Rejected Request: {resp.status_code} - {resp.text}")
            return jsonify({"error": f"Discord Error {resp.status_code}"}), 502

    except Exception as e:
        print(f"CRITICAL ERROR: {str(e)}")
        return jsonify({"error": "Internal Server Error"}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
