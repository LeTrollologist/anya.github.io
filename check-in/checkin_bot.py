# checkin_bot.py
import os
import discord
from discord.ext import commands
from flask import Flask, request, jsonify
from threading import Thread

# ---------------- CONFIG ----------------
DISCORD_TOKEN = os.environ.get("DISCORD_TOKEN")  # Bot token in Render secrets
ANYA_CHANNEL_ID = int(os.environ.get("ANYA_CHANNEL_ID"))  # channel for Anya
MICHEAL_CHANNEL_ID = int(os.environ.get("MICHEAL_CHANNEL_ID"))  # channel for you
RANDOM_CHANNEL_ID = int(os.environ.get("RANDOM_CHANNEL_ID"))  # random users

# ---------------- DISCORD BOT ----------------
intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)

# ---------------- FLASK APP ----------------
app = Flask(__name__)

@app.route("/send", methods=["POST"])
def send_message():
    data = request.get_json()
    user = data.get("user")
    message = data.get("message")
    
    if user == "anya":
        channel_id = ANYA_CHANNEL_ID
    elif user == "micheal":
        channel_id = MICHEAL_CHANNEL_ID
    else:
        channel_id = RANDOM_CHANNEL_ID
    
    channel = bot.get_channel(channel_id)
    if channel:
        bot.loop.create_task(channel.send(message))
        return jsonify({"status":"sent"}), 200
    else:
        return jsonify({"status":"channel not found"}), 404

# ---------------- RUN FLASK IN THREAD ----------------
def run_flask():
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))

Thread(target=run_flask).start()

# ---------------- RUN DISCORD BOT ----------------
bot.run(DISCORD_TOKEN)
