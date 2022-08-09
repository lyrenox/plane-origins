import os
import json
from random import choice

import discord
from discord.ext import commands


def image(category):
    f = open(os.getcwd()+'/lib/images.json') # The directory only works if this project is forever sitting in my computer
    data = json.load(f)
    results = []
    for i in data["images"]:
        if ("category", category) in i.items():
            results.append(i)
    final = choice(results)
    image.url = final.get("url")
    image.artist = final.get("artist")


class Images(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="lati", aliases=["eonduo", "lati@s"], brief="Gives you a picture of of planes",
    description = "Get a random image of Latios, Latias, sometimes both.")
    async def lati(self, ctx):
        try:
            image("lati")
            embed = discord.Embed(color=0x66e0ff)
            embed.set_author(name="lati", icon_url=ctx.author.avatar.url)
            embed.set_image(url=image.url)
            embed.set_footer(text=f'Source: {image.artist}')
            await ctx.send(embed=embed)
        except IndexError:
            await ctx.send("No images in category `lati`...")


    @commands.command(name="zeraora", aliases=["zera", "zapcat"], brief="Gives you a picture of electric kitty",
    description = "Get a random image of Zeraora.")
    async def zeraora(self, ctx):
        try:
            image("zeraora")
            embed = discord.Embed(color=0xffdd00)
            embed.set_author(name="zeraora", icon_url=ctx.author.avatar.url)
            embed.set_image(url=image.url)
            embed.set_footer(text=f'Source: {image.artist}')
            await ctx.send(embed=embed)
        except IndexError:
            await ctx.send("No images in category `zeraora`...")


def setup(bot):
    bot.add_cog(Images(bot))
