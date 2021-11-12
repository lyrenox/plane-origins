import nextcord
from nextcord.ext import commands
from bot import bot

class Invite(nextcord.ui.View):
    def __init__(self):
        super().__init__()
        self.add_item(
            nextcord.ui.Button(
                label="Invite LatiOS",
                url="https://discord.com/api/oauth2/authorize?client_id=781705025582792704&permissions=274878285888&scope=bot"))


class Dropdown(nextcord.ui.Select):
    def __init__(self):
        options = []
        for NameOfCog,TheClassOfCog in bot.cogs.items():
            options.append(nextcord.SelectOption(label=NameOfCog))
        options.append(nextcord.SelectOption(label="All"))
        super().__init__(placeholder='Select a category', min_values=1, max_values=1, options=options)

    async def callback(self, interaction: nextcord.Interaction):
        command_list = ""
        if self.values[0] == "All":
            commands = bot.commands
        else:
            cog = bot.get_cog(self.values[0])
            commands = cog.get_commands()
        for c in commands:
            command_list += f"‣ [{c.name}](https://youtu.be/hy_lL_On9EY)\n{c.brief}\n"
        embed = nextcord.Embed(description=command_list, color=0x4287f5)
        embed.set_footer(text=f"Category: {self.values[0]}")
        await interaction.response.edit_message(embed=embed)

class DropdownView(nextcord.ui.View):
    def __init__(self, author):
        super().__init__(timeout=20.0)
        self.author = author
        self.add_item(Dropdown())

    async def interaction_check(self, interaction: nextcord.Interaction):
        if interaction.user != self.author:
            await interaction.response.send_message(content=f"This menu can only be controlled by **{self.author.name}**, sorry!", ephemeral=True)
            return False
        else:
            return True

    async def on_timeout(self):
        await self.message.edit(content="This menu is disabled. (20 seconds of inactivity)", view=None)


class Utility(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="help", brief="Nyooooooooom")
    async def help(self, ctx, command=None):
        view = DropdownView(ctx.author)
        embed = nextcord.Embed(description="**Select a category below to view its list of commands!**", color=0x4287f5)
        if command is None:
            view.message = await ctx.send("This command is still a work in progress.", embed=embed, view=view)
        else:
            try:
                selected_command = bot.get_command(command.lower())
                embed = nextcord.Embed(title=f"{bot.command_prefix}{selected_command} info", description=selected_command.description, color=0x4287f5)
                embed.add_field(name="Usage", value=f"```{bot.command_prefix}{selected_command} {selected_command.signature}```", inline=False)
                embed.add_field(name="Aliases", value=', '.join(selected_command.aliases), inline=False)
                await ctx.send("This command is still a work in progress.", embed=embed)
            except AttributeError:
                view.message = await ctx.send("This command is still a work in progress.", embed=embed, view=view)


    @commands.command(name="info", aliases=["bot", "botinfo", "statistics", "ping"], brief="Get info about me, LatiOS!")
    async def info(self, ctx):
        embed = nextcord.Embed(title="LatiOS Statistics", color=0x4287f5)
        embed.add_field(name="Latency", value=f"{round(bot.latency*1000)}ms", inline=True)
        embed.add_field(name="Servers", value=len(bot.guilds), inline=True)
        embed.set_thumbnail(url="https://cdn.discordapp.com/avatars/781705025582792704/32016605cc5e4d886aee22870c097dfe.webp?size=160")
        embed.set_footer(text="Created by Lyreon | Icon by 5 dollar plushie")
        await ctx.send("Nyoom!", embed=embed)


    @commands.command(name="user", aliases=["userinfo"], brief="Fetch some info of a user")
    async def user(self, ctx, *, user: nextcord.Member=None):
        if user is None:
            user = ctx.author
        embed = nextcord.Embed(title=f"Info for {user}",
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
        embed = nextcord.Embed(title=f"Info for {ctx.guild.name}", description=f"Server ID: `{ctx.guild.id}`", color=0x4287f5)
        embed.add_field(name=f"Members", value=f"Total: {ctx.guild.member_count}\nHumans: {ctx.guild.member_count - len(bots)}\nBots: {len(bots)}", inline=True)
        embed.add_field(name="Channels", value=f"Text: {len(ctx.guild.text_channels)}\nVoice: {len(ctx.guild.voice_channels)}", inline=True)
        embed.add_field(name="Other Info", value=f"Created at {ctx.guild.created_at.strftime('%d %B %Y %H:%M:%S')} (UTC)\nOwned by: {ctx.guild.owner.mention}", inline=True)
        if ctx.guild.icon is not None:
            embed.set_thumbnail(url=ctx.guild.icon.url)
        await ctx.send(embed=embed)


    @commands.command(name="invite", brief="Invite me to your server")
    async def invite(self, ctx):
        await ctx.send('Invite me to your server!', view=Invite())


def setup(bot):
    bot.add_cog(Utility(bot))
