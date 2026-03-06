# checkin_bot.py
import discord
from discord.ext import commands
from flask import Flask, request, jsonify
import threading
import os

TOKEN = "YOUR_DISCORD_BOT_TOKEN" # Removed for security purposes

# Channel IDs
ANYA_CHANNEL = 123456789012345678  # Placeholder
MICHEAL_CHANNEL = 234567890123456789  # Placeholder
GUEST_CHANNEL = 345678901234567890  # Placeholder

# ===== Discord Bot =====
intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")

async def send_checkin(channel_id, message):
    channel = bot.get_channel(channel_id)
    if channel:
        await channel.send(message)

# ===== Flask Webserver =====
app = Flask("CheckInServer")

@app.route("/checkin", methods=["POST"])
def checkin():
    data = request.json
    checkin_type = data.get("type")
    message = data.get("message")
    
    if not checkin_type or not message:
        return jsonify({"error":"Invalid payload"}), 400
    
    if checkin_type == "anya":
        bot.loop.create_task(send_checkin(ANYA_CHANNEL, message))
    elif checkin_type == "micheal":
        bot.loop.create_task(send_checkin(MICHEAL_CHANNEL, message))
    else:
        bot.loop.create_task(send_checkin(GUEST_CHANNEL, message))
    
    return jsonify({"status":"ok"}), 200

# ===== Run Flask in Thread =====
def run_flask():
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)

threading.Thread(target=run_flask).start()
bot.run(TOKEN)
