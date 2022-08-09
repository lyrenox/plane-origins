import os
import asyncio

import discord
from discord.ext import commands
from dotenv import load_dotenv


load_dotenv()
TOKEN = os.getenv('ALPHA_TOKEN')

intents = discord.Intents.default()
intents.members = True
intents.message_content = True

bot = commands.Bot(command_prefix=">", case_insensitive=True, help_command=None, intents=intents)

@bot.event
async def on_ready():
    print(f"{bot.user} is up, nyoom!")


for cog in ['cogs.fun', 'cogs.images', 'cogs.utility']:
    try:
        bot.load_extension(cog)
        print(f"Loaded {cog}")
    except Exception as e:
        print(f"Failed to load {cog}: {e}")


bot.run(TOKEN)
