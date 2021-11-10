import nextcord
from nextcord.ext import commands

import json
from random import randint, choice


def image(category):
    f = open("lib\images\images.json",)
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

    @commands.command(name="lati", aliases=["eonduo", "lati@s"], brief="Gives you a random image of a plane")
    async def lati(self, ctx):
        try:
            image("lati")
            embed = nextcord.Embed(color=0x66e0ff)
            embed.set_author(name="lati", icon_url=ctx.author.avatar.url)
            embed.set_image(url=image.url)
            embed.set_footer(text=f'Artist: {image.artist}')
            await ctx.send("(This command is still a work in progress)", embed=embed)
        except IndexError:
            await ctx.send("No images in category `lati`...")


    @commands.command(name="zeraora", aliases=["zera", "zapcat"], brief="Gives you a random image of electric kitty")
    async def zeraora(self, ctx):
        try:
            image("zeraora")
            embed = nextcord.Embed(color=0xffdd00)
            embed.set_author(name="zeraora", icon_url=ctx.author.avatar.url)
            embed.set_image(url=image.url)
            embed.set_footer(text=f'Artist: {image.artist}')
            await ctx.send("(This command is still a work in progress)", embed=embed)
        except IndexError:
            await ctx.send("No images in category `zeraora`...")


def setup(bot):
    bot.add_cog(Images(bot))
