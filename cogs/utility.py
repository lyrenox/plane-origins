import discord
from discord.ext import commands
from discord.ui import View, Button

from time import time
from psutil import Process
from math import *


class Invite(View):
    def __init__(self):
        super().__init__()
        self.add_item(
            Button(
                label="Invite LatiOS",
                url="https://discord.com/api/oauth2/authorize?client_id=781705025582792704&permissions=274878285888&scope=bot"))


class Dropdown(discord.ui.Select):
    def __init__(self, bot):
        options = []
        self.bot = bot
        for NameOfCog,TheClassOfCog in self.bot.cogs.items():
            options.append(discord.SelectOption(label=NameOfCog))
        options.append(discord.SelectOption(label="All"))
        super().__init__(placeholder='Select a category', min_values=1, max_values=1, options=options)

    async def callback(self, interaction: discord.Interaction):
        command_list = ""
        if self.values[0] == "All":
            commands = self.bot.commands
        else:
            cog = self.bot.get_cog(self.values[0])
            commands = cog.get_commands()
        for c in commands:
            command_list += f"\> [{c.name}](https://youtu.be/hy_lL_On9EY)\n{c.brief}\n\n"
        embed = discord.Embed(description=command_list, color=0x4287f5)
        embed.set_footer(text=f"Category: {self.values[0]}")
        await interaction.response.edit_message(embed=embed)


class DropdownView(View):
    def __init__(self, ctx, bot):
        super().__init__(timeout=20.0)
        self.ctx = ctx
        self.bot = bot
        self.add_item(Dropdown(self.bot))

    async def interaction_check(self, interaction: discord.Interaction):
        if interaction.user != self.ctx.author:
            await interaction.response.send_message(content=f"Hey! This menu can only be controlled by **{self.ctx.author.name}**.", ephemeral=True)
            return False
        else:
            return True

    async def on_timeout(self):
        for item in self.children:
            item.disabled = True
        await self.message.edit("You can no longer interact with this menu.", view=self)



class Utility(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    def display_time(self, seconds):
        intervals = (
            ('d', 86400),    # 60 * 60 * 24
            ('h', 3600),     # 60 * 60
            ('m', 60),
            ('s', 1),
        )
        result = []
        for name, count in intervals:
            value = seconds // count
            if value:
                seconds -= value * count
                result.append("{}{}".format(value, name))
        return ' '.join(result)


    @commands.command(name="help", brief="Nyooooooooom")
    async def help(self, ctx, command=None):
        view = DropdownView(ctx, self.bot)
        embed = discord.Embed(description="**Select a category below to view its list of commands!**", color=0x4287f5)
        if command is None:
            view.message = await ctx.send(embed=embed, view=view)
        else:
            try:
                selected_command = self.bot.get_command(command.lower())
                embed = discord.Embed(title=f"{self.bot.command_prefix}{selected_command} info", description=selected_command.description, color=0x4287f5)
                embed.add_field(name="Usage", value=f"```{self.bot.command_prefix}{selected_command} {selected_command.signature}```", inline=False)
                embed.add_field(name="Aliases", value=', '.join(selected_command.aliases) if len(selected_command.aliases) != 0 else None, inline=False)
                await ctx.send(embed=embed)
            except AttributeError:
                view.message = await ctx.send(embed=embed, view=view)


    @commands.command(name="info", aliases=["bot", "botinfo", "statistics"], brief="Get info about me, LatiOS!")
    async def info(self, ctx):
        proc = Process()
        uptime = self.display_time(round(time()-proc.create_time()))
        embed = discord.Embed(title="LatiOS Statistics", color=0x4287f5)
        embed.add_field(name="Servers", value=len(self.bot.guilds), inline=True)
        embed.add_field(name="Uptime", value=uptime, inline=True)
        embed.set_thumbnail(url=self.bot.user.avatar.url)
        embed.set_footer(text="Created by Lyreon | Icon by 5 dollar plushie")
        await ctx.send("Nyoom!", embed=embed)


    @commands.command(name="ping", aliases=["latency"], brief="Pong!")
    async def ping(self, ctx):
        start = time()
        response = await ctx.send(f":ping_pong: Pong! **{round(self.bot.latency*1000)}ms**")
        end = time()
        await response.edit(content=f":ping_pong: Pong! **{round(self.bot.latency*1000)}ms**\nResponse time: **{round((end-start)*1000)}ms**")


    @commands.command(name="user", aliases=["userinfo"], brief="Fetch some info of a user")
    async def user(self, ctx, *, user: discord.Member=None):
        if user is None:
            user = ctx.author
        embed = discord.Embed(title=f"Info for {user}",
                               description=f"Server Nickname: **{user.nick}**\nUser ID: `{user.id}`\nCreated at {user.created_at.strftime('%d %B %Y %H:%M:%S')} (UTC)\nJoined at {user.joined_at.strftime('%d %B %Y %H:%M:%S')} (UTC)",
                               color=user.color)
        if user.avatar is not None:
            embed.set_thumbnail(url=user.avatar.url)
        await ctx.send(embed=embed)

    @user.error
    async def user_err(self, ctx, error):
        if isinstance(error, commands.UserInputError):
            await ctx.send(f"I could not find that user...")


    @commands.command(name="server", aliases=["serverinfo"], brief="Fetch info about your current server")
    async def server(self, ctx):
        def filterOnlyBots(member):
            return member.bot
        bots = list(filter(filterOnlyBots, ctx.guild.members))
        embed = discord.Embed(title=f"Info for {ctx.guild.name}", description=f"Server ID: `{ctx.guild.id}`", color=0x4287f5)
        embed.add_field(name=f"Members", value=f"Total: {ctx.guild.member_count}\nHumans: {ctx.guild.member_count - len(bots)}\nBots: {len(bots)}", inline=True)
        embed.add_field(name="Channels", value=f"Text: {len(ctx.guild.text_channels)}\nVoice: {len(ctx.guild.voice_channels)}", inline=True)
        embed.add_field(name="Other Info", value=f"Created at {ctx.guild.created_at.strftime('%d %B %Y %H:%M:%S')} (UTC)\nOwned by: {ctx.guild.owner.mention}", inline=True)
        if ctx.guild.icon is not None:
            embed.set_thumbnail(url=ctx.guild.icon.url)
        await ctx.send(embed=embed)


    @commands.command(name="invite", brief="Invite me to your server")
    async def invite(self, ctx):
        await ctx.send('Invite me to your server!', view=Invite())


    @commands.command(aliases=['calc', 'calculator', 'eval', 'evaluate', 'math'], brief="Calculate an equation")
    async def calculate(self, ctx, *, equation):
        try:
            power = equation.replace('^', '**')
            i = power.replace('π', 'pi')
            output = float(eval(i))
            footer = 'Biggus brainium'
        except (SyntaxError, NameError, TypeError, ZeroDivisionError):
            output = 'undefined'
            footer = 'Uh oh...'
        embed = discord.Embed(color=0x4287f5)
        embed.set_author(name=f"{ctx.author.name}'s equation", icon_url=ctx.author.avatar.url)
        embed.add_field(name="Input", value=f"```{equation}```", inline=False)
        embed.add_field(name="Result", value=f"```{output}```", inline=False)
        embed.set_footer(text=footer)
        await ctx.send(embed=embed)

    @calculate.error
    async def calc_err(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.reply(f"You need to type in an equation.\n`{self.bot.command_prefix}calculate <equation>` is how you use this")
            return


def setup(bot):
    bot.add_cog(Utility(bot))
