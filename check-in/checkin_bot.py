import os
import random
import threading
import asyncio
from flask import Flask, request, jsonify, send_from_directory
import discord
from discord.ext import commands

# --- CONFIGURATION ---
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
ANYA_CH_ID = int(os.getenv("ANYA_CHANNEL_ID", 0))
MICHEAL_CH_ID = int(os.getenv("MICHEAL_CHANNEL_ID", 0))
RANDOM_CH_ID = int(os.getenv("RANDOM_CHANNEL_ID", 0))

# --- MESSAGE POOLS ---
ANYA_MESSAGES = [
    "I love you mostest times infinity! 💖",
    "You are my favorite human 🌸",
    "Thinking of you always, Anya ❤️",
    "You make my heart dance! 💃"
]

# --- BOT SETUP ---
intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)

# --- FLASK WEB SERVER ---
app = Flask(__name__)

@app.route("/")
def index():
    # This serves the checkin.html file when someone visits the root URL
    return send_from_directory('.', 'checkin.html')

@app.route("/api/checkin", methods=["POST"])
def api_checkin():
    data = request.json
    check_type = data.get("type")
    
    msg = "A loving check-in has arrived! ✨"
    channel_id = RANDOM_CH_ID

    if check_type == "anya":
        msg = random.choice(ANYA_MESSAGES)
        channel_id = ANYA_CH_ID
    elif check_type == "micheal":
        msg = "💙 Michael has checked in with love!"
        channel_id = MICHEAL_CH_ID
    
    # Bridge Flask to Discord Bot
    if bot.is_ready():
        channel = bot.get_channel(channel_id)
        if channel:
            bot.loop.create_task(channel.send(msg))
            return jsonify({"status": "success"}), 200
    
    return jsonify({"status": "bot_not_ready"}), 503

# --- RUNNING THE SERVICES ---
def run_discord():
    # Discord.py bot.run is blocking, so it must be in its own thread
    bot.run(DISCORD_TOKEN)

if __name__ == "__main__":
    # 1. Start Discord in a background thread
    t = threading.Thread(target=run_discord)
    t.daemon = True
    t.start()

    # 2. Start Flask in the main thread (Render listens to this)
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
