from flask import Flask, render_template_string, request, jsonify, redirect
import requests
import random
import os

app = Flask(__name__)

# --- WEBHOOKS ---
WEBHOOK_Anya = os.getenv("WEBHOOK_Anya")  # Anya channel
WEBHOOK_Michael = os.getenv("WEBHOOK_Michael")  # Michael channel
WEBHOOK_Random = os.getenv("WEBHOOK_Random")  # Random users

# --- LOVING MESSAGES FOR ANYA ---
anya_messages = [
    "I love you mostest times infinity times perpetuity 💖",
    "I love you more than chocos 🍫💘",
    "You are my sunshine and my moonlight 🌞🌙",
    "Forever and always, my heart is yours ❤️",
    "I love you to the stars and back ✨🌌",
    "You are the best part of my day 💞",
    "Every heartbeat whispers your name 💓",
    "You're my forever favorite 💘",
]

# --- ROUTES ---

@app.route("/")
def home():
    # Redirect to the checkin page
    return redirect("/checkin")

@app.route("/checkin")
def checkin_page():
    # Full HTML page with buttons and JS
    return render_template_string("""
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Check-In 💖</title>
<style>
  @import url('https://fonts.googleapis.com/css2?family=Great+Vibes&family=Playfair+Display:wght@400;600&display=swap');
  body {
    margin: 0; padding: 0; font-family: 'Playfair Display', serif;
    background: linear-gradient(135deg, #2c3e50, #8e44ad);
    color: #fff; display: flex; flex-direction: column; align-items: center; justify-content: center;
    min-height: 100vh;
  }
  h1 { font-family: 'Great Vibes', cursive; font-size: 4rem; text-align:center; margin-bottom: 20px; text-shadow: 2px 2px 5px #000; }
  p { font-size: 1.2rem; text-align:center; margin-bottom: 30px; }
  .buttons { display: flex; flex-wrap: wrap; gap: 15px; justify-content:center; }
  button {
    padding: 15px 25px; font-size:1rem; border:none; border-radius:12px;
    cursor:pointer; transition: all 0.3s ease;
    font-family: 'Playfair Display', serif;
    box-shadow: 0 4px 8px rgba(0,0,0,0.3);
  }
  button:hover { transform: translateY(-3px) scale(1.05); box-shadow: 0 6px 12px rgba(0,0,0,0.5); }
  .anya { background: #e84393; color: #fff; }
  .michael { background: #00cec9; color: #fff; }
  .random { background: #fdcb6e; color: #000; }
  .home { background: #6c5ce7; color: #fff; }
  #status { margin-top: 25px; font-size: 1.2rem; min-height: 30px; text-align:center; }
  a { color: #ffeaa7; text-decoration:none; margin-top:30px; font-size:1rem; }
  a:hover { text-decoration: underline; }
</style>
</head>
<body>
<h1>💖 Check In 💖</h1>
<p>Send your love and respect with a click!</p>
<div class="buttons">
  <button class="anya" onclick="checkin('anya')">Anya Check-In</button>
  <button class="michael" onclick="checkin('michael')">Michael Check-In</button>
  <button class="random" onclick="checkin('random')">Random Check-In</button>
  <button class="home" onclick="window.location.href='/'">Return Home</button>
</div>
<div id="status"></div>
<a href="/">Back to Main Site</a>

<script>
async function checkin(type) {
  const status = document.getElementById('status');
  status.textContent = "Sending love... 💌";
  try {
    const res = await fetch('/api/checkin', {
      method: 'POST',
      headers: {'Content-Type':'application/json'},
      body: JSON.stringify({type})
    });
    const data = await res.json();
    status.textContent = data.message;
  } catch(err) {
    status.textContent = "Oops! Something went wrong 💔";
  }
}
</script>
</body>
</html>
""")

@app.route("/api/checkin", methods=["POST"])
def api_checkin():
    data = request.get_json()
    check_type = data.get("type")

    if check_type == "anya":
        message = random.choice(anya_messages)
        webhook_url = WEBHOOK_Anya
    elif check_type == "michael":
        message = "Michael has checked in 💙"
        webhook_url = WEBHOOK_Michael
    elif check_type == "random":
        message = "A friend has paid their respects 🌸"
        webhook_url = WEBHOOK_Random
    else:
        return jsonify({"message":"Invalid type"}), 400

    # Send message via webhook
    if webhook_url:
        requests.post(webhook_url, json={"content": message})
        return jsonify({"message": f"Sent! 💌 {message}"})
    else:
        return jsonify({"message":"Webhook not configured"}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
