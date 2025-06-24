import os
import discord
import asyncio

VOICE_CHANNEL_ID = 1375227595741855825
TEXT_CHANNEL_ID = 1375767832234823740

# ดึง Tokens จาก environment variable (ใช้ , คั่น)
TOKENS = os.getenv("TOKENS", "").split(",")

clients = []

# ฟังก์ชันสร้างและรัน client
async def start_bot(token):
    class MyClient(discord.Client):
        async def on_ready(self):
            print(f'✅ Logged in as {self.user} ({self.user.id})')

            # เข้าห้องเสียง
            voice_channel = self.get_channel(VOICE_CHANNEL_ID)
            if voice_channel and isinstance(voice_channel, discord.VoiceChannel):
                try:
                    await voice_channel.connect()
                    print(f'{self.user} joined voice channel.')
                except discord.ClientException:
                    print(f'{self.user} already connected or error.')

            # เริ่ม loop สำหรับ ping ทุก 1 ชั่วโมง
            asyncio.create_task(self.ping_loop())

        async def ping_loop(self):
            await self.wait_until_ready()
            channel = self.get_channel(TEXT_CHANNEL_ID)
            while not self.is_closed():
                try:
                    await channel.send(f'{self.user.mention} is alive ✅')
                except Exception as e:
                    print(f'Error sending message: {e}')
                await asyncio.sleep(3600)

    intents = discord.Intents.default()
    intents.message_content = True
    client = MyClient(intents=intents)
    clients.append(client)
    await client.start(token.strip())

# เรียกใช้บอททุกตัวพร้อมกัน
async def main():
    await asyncio.gather(*(start_bot(token) for token in TOKENS if token.strip()))

asyncio.run(main())
