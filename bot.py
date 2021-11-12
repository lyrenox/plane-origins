import os
import asyncio

import nextcord
from nextcord.ext import commands
from dotenv import load_dotenv


load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

intents = nextcord.Intents.default()
intents.members = True

bot = commands.Bot(command_prefix=">", case_insensitive=True, help_command=None, intents=intents)

@bot.event
async def on_ready():
    print(f"{bot.user} is up, nyoom!")


bot.load_extension("cogs.fun")
bot.load_extension("cogs.images")
bot.load_extension("cogs.utility")

bot.run(TOKEN)
