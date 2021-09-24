# bot.py
import os
import discord

from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

client = discord.Client()

@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')
    channel = input("Enter a channel ID (One time): ")
    channel = client.get_channel(int(channel))
    while True:
        message = input(f"Send to {channel}: ")
        await channel.send(message)

client.run(TOKEN)
