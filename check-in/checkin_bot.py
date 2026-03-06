import os
import random
import requests
from flask import Flask, request, jsonify, send_from_directory

app = Flask(__name__)

# --- CONFIGURATION ---
# These must match the keys in Render exactly!
ANYA_MESSAGES = [
    "I love you mostest times infinity times perpetuity 💖",
    "I love you more than chocos 🍫❤️",
    "You are my sunshine every day ☀️💕",
    "Forever and always, my heart is yours 💞",
    "You're my favorite human in the universe 🌌💖"
]

@app.route("/")
def index():
    return send_from_directory('.', 'checkin.html')

@app.route("/api/checkin", methods=["POST"])
def api_checkin():
    try:
        data = request.json
        check_type = data.get("type")
        
        # Determine which webhook to use
        if check_type == "anya":
            msg = random.choice(ANYA_MESSAGES)
            url = os.getenv("WEBHOOK_ANYA")
        elif check_type == "micheal":
            msg = "💙 Michael has checked in with love!"
            url = os.getenv("WEBHOOK_MICHAEL")
        else:
            msg = "🌟 A visitor has paid their respects!"
            url = os.getenv("WEBHOOK_RANDOM")

        # DEBUG LOGGING (Check your Render logs for these!)
        if not url:
            print(f"ERROR: Webhook URL for '{check_type}' is MISSING in Render Env Vars!")
            return jsonify({"status": "error", "message": "Server configuration missing"}), 500

        print(f"Attempting to send message to Discord for: {check_type}")

        # Send to Discord
        response = requests.post(url, json={"content": msg}, timeout=5)
        
        if response.status_code in [200, 204]:
            print("Successfully sent to Discord!")
            return jsonify({"status": "success", "message": msg}), 200
        else:
            print(f"Discord returned error: {response.status_code} - {response.text}")
            return jsonify({"status": "error", "message": "Discord rejected message"}), 500

    except Exception as e:
        print(f"CRITICAL ERROR: {str(e)}")
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
