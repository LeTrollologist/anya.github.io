# checkin_bot.py
import os
import discord
from discord.ext import commands
from dotenv import load_dotenv
import random

load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")

# Channel IDs from Discord (replace with your actual channel IDs)
ANYA_CHANNEL = int(os.getenv("ANYA_CHANNEL_ID"))
MICHAEL_CHANNEL = int(os.getenv("MICHAEL_CHANNEL_ID"))
RANDOM_CHANNEL = int(os.getenv("RANDOM_CHANNEL_ID"))

intents = discord.Intents.default()
intents.messages = True

bot = commands.Bot(command_prefix="!", intents=intents)

# Loving messages for Anya
ANYA_MESSAGES = [
    "I love you mostest times infinity times perpetuity 💖",
    "I love you more than chocos 🍫💗",
    "Forever and always, my Anya 🌸",
    "You are my universe 🌌❤️",
    "Every heartbeat is yours 💓",
    "I love you more than all the stars ✨💖",
    "My heart belongs to you forever 💘",
    "You are my sunshine and moonlight 🌞🌙",
    "I adore you endlessly 💞",
]

# Responses when someone checks in
MICHAEL_MESSAGES = [
    "Micheal checked in with love 💖",
    "Micheal says hi! 💗",
    "Another loving thought from Micheal 🌸",
]

RANDOM_MESSAGES = [
    "Someone just paid their respects 💌",
    "A visitor sends love ❤️",
    "A random heart joins the celebration 💖",
]

@bot.event
async def on_ready():
    print(f"{bot.user} is online!")

@bot.event
async def on_message(message):
    # Ignore bot messages
    if message.author == bot.user:
        return

    # We listen for POST requests via a command-like interface (we will send from JS)
    await bot.process_commands(message)

# Commands triggered via JS fetch
@bot.command()
async def anya(ctx):
    channel = bot.get_channel(ANYA_CHANNEL)
    if channel:
        msg = random.choice(ANYA_MESSAGES)
        await channel.send(msg)
        await ctx.send("Anya check-in sent!")

@bot.command()
async def michael(ctx):
    channel = bot.get_channel(MICHAEL_CHANNEL)
    if channel:
        msg = random.choice(MICHAEL_MESSAGES)
        await channel.send(msg)
        await ctx.send("Micheal check-in sent!")

@bot.command()
async def random_user(ctx):
    channel = bot.get_channel(RANDOM_CHANNEL)
    if channel:
        msg = random.choice(RANDOM_MESSAGES)
        await channel.send(msg)
        await ctx.send("Random check-in sent!")

# For ping from server (optional)
@bot.command()
async def ping(ctx):
    await ctx.send("Pong! 💖")

# Run the bot
bot.run(TOKEN)
