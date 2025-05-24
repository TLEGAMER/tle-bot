import discord
from discord.ext import tasks, commands
import asyncio
import os
from flask import Flask
from threading import Thread

# == ✅ START: Keep-alive server ==
app = Flask('')

@app.route('/')
def home():
    return "✅ Bot is alive!"

def run():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()
# == ✅ END: Keep-alive server ==


# == 🔐 ใช้ Environment Variable ==
TOKEN = os.getenv("DISCORD_BOT_TOKEN")
VOICE_CHANNEL_ID = 1375227595741855825
TEXT_CHANNEL_ID = 1375767832234823740

intents = discord.Intents.default()
intents.message_content = True
intents.voice_states = True
intents.guilds = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

voice_client = None
text_channel = None


@bot.event
async def on_ready():
    global text_channel
    print(f"✅ Logged in as {bot.user}")
    await connect_to_voice()

    for guild in bot.guilds:
        text_channel = guild.get_channel(TEXT_CHANNEL_ID)
        if text_channel:
            break

    if text_channel:
        send_status.start()
    else:
        print("❌ ไม่พบ text channel ที่กำหนด")


async def connect_to_voice():
    global voice_client
    for guild in bot.guilds:
        channel = guild.get_channel(VOICE_CHANNEL_ID)
        if channel and isinstance(channel, discord.VoiceChannel):
            try:
                if bot.voice_clients:
                    return  # already connected
                voice_client = await channel.connect()
                print(f"🎧 Connected to voice channel: {channel.name}")
            except discord.ClientException:
                print("⚠️ Already connected.")
            except Exception as e:
                print(f"❌ Failed to connect: {e}")


@tasks.loop(minutes=30)
async def send_status():
    if text_channel:
        await text_channel.send("I'm online Kub 👋")


@bot.event
async def on_voice_state_update(member, before, after):
    if member.id == bot.user.id:
        if after.channel is None:
            print("❌ Bot disconnected, reconnecting...")
            await asyncio.sleep(5)
            await connect_to_voice()


# ✅ เรียก keep_alive ก่อน run bot
keep_alive()
bot.run(TOKEN)
