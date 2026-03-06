import discord
from discord.ext import commands
import os
import random
from keep_alive import keep_alive

# Load environment variable
TOKEN = os.environ['DISCORD_TOKEN']

# Intents for bot
intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)

# Anya messages
anya_messages = [
    "I love you mostest times infinity times perpetuity ❤️",
    "I love you more than chocos 🍫💖",
    "You make my heart dance every day 💃💖",
    "Forever and always, my love 💞",
    "You're my favorite human in the multiverse 🌌❤️"
]

# Micheal messages
micheal_messages = [
    "Micheal says: I miss you 💖",
    "Micheal says: You're amazing ❤️",
    "Micheal says: Sending you love 💌",
    "Micheal says: Can't wait to see you 🌟"
]

# Guest messages
guest_messages = [
    "Someone paid their respects ❤️",
    "A kind soul checked in 💖",
    "Love and light to this page 🌸",
    "A guest sends a warm hug 🤗"
]

# Commands to send messages to specific channels
@bot.command()
async def checkin(ctx, person):
    if person.lower() == "anya":
        channel_id = int(os.environ['ANYA_CHANNEL'])
        msg = random.choice(anya_messages)
    elif person.lower() == "micheal":
        channel_id = int(os.environ['MICHEAL_CHANNEL'])
        msg = random.choice(micheal_messages)
    else:
        channel_id = int(os.environ['GUEST_CHANNEL'])
        msg = random.choice(guest_messages)

    channel = bot.get_channel(channel_id)
    if channel:
        await channel.send(msg)
        await ctx.send(f"Check-in sent! 💖 ({msg})")
    else:
        await ctx.send("Channel not found 😢")

# Keep bot alive for Render.com
keep_alive()

# Run bot
bot.run(TOKEN)
