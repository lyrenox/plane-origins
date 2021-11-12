import nextcord
from nextcord.ext import commands
from bot import bot

import asyncio
from random import randint, choice


class Fun(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    # Guess the number
    @commands.command(name="guessthenumber", aliases=["gtn", "guess"], brief="Start a guessing game")
    async def guessthenumber(self, ctx, *, difficulty=None):
        levels = {
            "easy": 20,
            "medium": 50,
            "hard": 100,
            "harder": 500,
            "expert": 1000,
            "insane": 5000,
            "extreme": 10000
        }
        call = ["massive brain", "genius"]

        if difficulty is not None:
            difficulty = difficulty.lower()

        if difficulty in levels.keys():
            range = levels.get(difficulty)
            my_number = randint(1, range)
            attempts = 0
            embed = nextcord.Embed(title="Guess the Number",
                                   description=f"Your number is somewhere between **1** and **{range}**.\nType your guess in chat!")
            embed.set_footer(text="You have 20 seconds to respond!")
            await ctx.reply(embed=embed)

            guesses = []
            while True:
                def check(m):
                    return m.author == ctx.author and m.channel == ctx.message.channel and m.content.isnumeric()
                try:
                    response = await bot.wait_for('message', timeout=20.0, check=check)
                except asyncio.TimeoutError:
                    embed = nextcord.Embed(title="Guess the Number",
                                           description=f"You took too long to respond! I was thinking of **{my_number}**.",
                                           color=0xeb4034)
                    await ctx.reply(embed=embed)
                    break
                guess = int(response.content)
                if guess < 1 or guess > range:
                    await ctx.reply(f"Smh your number should be between **1** and **{range}**!")
                elif guess in guesses:
                    await ctx.reply(f"You already picked that number. Maybe try something else?")
                else:
                    attempts += 1
                    if guess == my_number:
                        embed = nextcord.Embed(title="Guess the Number",
                                               description=f"Nice, you guessed it in **{attempts} attempts** {choice(call)}. I was thinking of **{my_number}**.",
                                               color=0x11d445)
                        await ctx.reply(embed=embed)
                        break
                    else:
                        if guess > my_number: hint = ["high", "lower"]
                        else: hint = ["low", "higher"]
                        embed = nextcord.Embed(title="Guess the Number",
                                               description=f"Your number was too **{hint[0]}**! Try going **{hint[1]}**.\nYou have **{attempts} attempts** so far.")
                        embed.set_footer(text="You have 20 seconds to respond!")
                        await ctx.reply(embed=embed)
                        guesses.append(guess)

        else:
            embed = nextcord.Embed(title="Guess the Number",
                                   description=f"Start a game with `{bot.command_prefix}guessthenumber [difficulty]`!\nThe available difficulties are `{'`, `'.join(list(levels.keys())[:-1])}` and `{list(levels.keys())[-1]}`",
                                   color=0x4287f5)
            await ctx.reply(embed=embed)




    # Roll dice
    @commands.command(name="roll", aliases=["rolldice", "dice"], brief="Roll some dice")
    async def roll(self, ctx, number: int, sides: int):
        if number > 10:
            await ctx.reply("You can only roll up to 10")
        elif number < 1:
            await ctx.reply("I can't roll nothing man")
        elif sides > 100:
            await ctx.reply("hey i only have the ones up to 100 sides")
        elif sides < 4:
            await ctx.reply("dice have at least 4 sides man")
        else:
            sum = 0
            dice = [
                str(choice(range(1, sides + 1)))
                for _ in range(number)
            ]
            for roll in dice:
                sum += int(roll)
            embed = nextcord.Embed(title=f"{ctx.author.name} rolls out a total of {sum}!",
                                   description=f"Rolled: [**{'**] [**'.join(dice)}**]",
                                   color=0x4287f5)
            await ctx.reply(embed=embed)

    @roll.error
    async def roll_err(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.reply(f"Try again, `{bot.command_prefix}roll <number> <sides>` is how you use this")
            return




    # Choose
    @commands.command(name="choose", aliases=["select"], brief="LatiOS will choose something for you")
    async def choose(self, ctx, *, choices: str):
        if "|" in choices:
            choices = choices.split("|")
        elif "," in choices:
            choices = choices.split(",")
        else:
            choices = choices.split(" ")
        if len(choices) < 2:
            await ctx.reply(f"Bruh, you only gave one choice, so I only have one option, `{choices[0]}` <:bruh:907585845798772766>")
        else:
            final = choice(choices)
            await ctx.reply(f"**{ctx.author.name}**, I choose `{final}`!")

    @choose.error
    async def choose_err(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.reply(f"**{ctx.author.name}**, I choose `for you to run this command correctly`\n`{bot.command_prefix}choose <choice 1,choice 2,...>` is how you use this")


def setup(bot):
    bot.add_cog(Fun(bot))
