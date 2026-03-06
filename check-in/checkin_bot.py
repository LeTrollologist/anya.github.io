import os
import random
from flask import Flask, request, jsonify, send_from_directory
import requests

app = Flask(__name__)

# --- CONFIGURATION (Set these in Render Environment Variables) ---
# Instead of a Token, we use Webhook URLs
WEBHOOK_ANYA = os.getenv("WEBHOOK_ANYA")
WEBHOOK_MICHAEL = os.getenv("WEBHOOK_MICHAEL")
WEBHOOK_RANDOM = os.getenv("WEBHOOK_RANDOM")

ANYA_MESSAGES = [
    "I love you mostest times infinity times perpetuity 💖",
    "I love you more than chocos 🍫❤️",
    "You are my sunshine every day ☀️💕",
    "Forever and always, my heart is yours 💞",
    "You're my favorite human in the universe 🌌💖",
    "Every heartbeat is just for you 💓",
    "My world is better with you in it 🌸"
]

@app.route("/")
def index():
    # Serves your checkin.html
    return send_from_directory('.', 'checkin.html')

@app.route("/api/checkin", methods=["POST"])
def api_checkin():
    data = request.json
    check_type = data.get("type")
    
    msg = "A loving check-in has arrived! ✨"
    webhook_url = WEBHOOK_RANDOM

    if check_type == "anya":
        msg = random.choice(ANYA_MESSAGES)
        webhook_url = WEBHOOK_ANYA
    elif check_type == "micheal":
        msg = "💙 Michael has checked in with love!"
        webhook_url = WEBHOOK_MICHAEL

    # Send via Webhook instead of Bot
    if webhook_url:
        payload = {"content": msg}
        response = requests.post(webhook_url, json=payload)
        if response.status_code == 204 or response.status_code == 200:
            return jsonify({"status": "success", "message": msg}), 200
        else:
            return jsonify({"status": "error", "detail": "Discord rejected the webhook"}), 500
    
    return jsonify({"status": "error", "detail": "Webhook URL not configured"}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
