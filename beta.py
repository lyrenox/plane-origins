# bot.py
import os
import random
import discord

from discord.ext import commands
from dotenv import load_dotenv
from random import randint

print(os.listdir('.'))

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

bot = commands.Bot(command_prefix='>', help_command=None)

@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')

async def on_disconnect():
    print(f'Oh noes! {bot.user} has disconnected!')

@bot.command(name='help', help='Shows this menu.')
async def help(ctx, command:str=None):
    if command is None:
        embed = discord.Embed(title="Help Menu", description="To view info about a certain command, use the commands below!", color=0x007bff)
        embed.add_field(name=":game_die: Fun", value="`>help fun`", inline=True)
        embed.add_field(name=":camera: Images", value="`>help images`", inline=True)
        embed.add_field(name=":information_source: Info", value="`>help info`", inline=True)
        await ctx.send(embed=embed)
    else:
        await ctx.send('Menu for commands under development. Check back sooner!')

@bot.command(name='status', help='Shows the bot\'s status')
async def status(ctx):
    embed=discord.Embed()
    embed.set_author(name="Bot status")
    embed.add_field(name="Version", value="`0.22`", inline=True)
    embed.add_field(name="Latency", value=f"{round(bot.latency * 1000)} ms", inline=True)
    await ctx.send(embed=embed)

@bot.command(name='changelog', help='Shows previous updates and changes to the bot.', aliases=['update', 'log'])
async def log(ctx):
    log='''```
    lyrebot Change Log
    version 0.22 I can't remember
    - Added echo command
    ```'''
    await ctx.send(log)

@bot.event
async def on_message(message):

    if 'latios simp' in message.content.lower():
        await message.channel.send('no')

    if 'remove yourself from reddit' in message.content.lower():
        await message.channel.send('You are fuck')

    # Dad joke (caps still don't work)
#    keyword = ["im ", "i'm ", "am "]
#    for term in keyword:
#        if term in message.content.lower():
#            if message.author == bot.user:
#                return
#            name = message.content.partition(term)[-1]
#            await message.channel.send(f'Hi {name}, I\'m Dad.')
#            return
#        else: pass

    await bot.process_commands(message)

@bot.command(name='echo', help='Literally repeats everything you say')
async def echo(ctx, *, message):
        await ctx.send(message)

@bot.command(name='quote', help='Displays some random quote.')
async def quote(ctx):
    f = open('quote.txt', 'r')
    quote = f.read().splitlines()
    response = random.choice(quote)
    await ctx.send(response)

@bot.command(name='roll', help='Rolls up to **30 dice** with up to **120 sides**.')
async def roll(ctx, number_of_dice: int, number_of_sides: int):
    dice = [
        str(random.choice(range(1, number_of_sides + 1)))
        for _ in range(number_of_dice)
    ]
    if number_of_dice > 30:
        await ctx.send('listen mate i don\'t have time for that much dice')
    elif number_of_sides > 120:
        await ctx.send('Hmm do dice really exist with that many sides??')
    else:
        await ctx.send('You rolled out **{}**'.format(', '.join(dice)))

@bot.command(name='alert', help='Sends an alert to a specific person. (or to yourself if you have no friends)')
async def alert(ctx, member: discord.Member, *, message: str):
    await member.send(f'**{ctx.author} from {ctx.guild.name}**: {message}')
    await ctx.send(f'Message successfully sent to **{member}**!')

# Image commands
@bot.command(name='zeraora', help='Displays a random Zeraora image.', aliases=['zera', 'zapcat'])
async def zeraora(ctx):
    fa = open('img.txt', 'r')
    img = fa.read().splitlines()
    fb = open('credit.txt', 'r')
    credit = fb.read().splitlines()
    response = randint(1,8)
    embed = discord.Embed(color=0xffdd00)
    embed.add_field(name='Requested by', value=ctx.author)
    embed.set_image(url=img[response])
    embed.set_footer(text=f'Artist: {credit[response]}')
    await ctx.send(embed=embed)

@bot.command(name='lati', help='Displays a random image with Latios or Latias. (maybe both)', aliases=['eonduo', 'lati@s'])
async def eonduo(ctx):
    fa = open('img.txt', 'r')
    img = fa.read().splitlines()
    fb = open('credit.txt', 'r')
    credit = fb.read().splitlines()
    response = randint(11,20)
    embed = discord.Embed(color=0x66e0ff)
    embed.add_field(name='Requested by', value=ctx.author)
    embed.set_image(url=img[response])
    embed.set_footer(text=f'Artist: {credit[response]}')
    await ctx.send(embed=embed)

bot.run(TOKEN)
