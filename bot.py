# bot.py

import os
import random
import logging
import discord
import requests
import json
from dotenv import load_dotenv
from discord.ext import commands
import asyncio

# ###
# Load Items
# ###
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')
ERRORCHANNEL = os.getenv('DISCORD_ERROR_CHANNEL')
runDirectory = os.path.dirname(os.path.realpath(__file__))+"/"
logging.basicConfig(level=logging.INFO)


# ###
# Functions
# ###

def get_error_channel():
    guild = discord.utils.get(bot.guilds, name=GUILD)
    for channel in guild.channels:
        if(channel.name == ERRORCHANNEL):
            tmpChannel = bot.get_channel(channel.id)          
    return tmpChannel


# ###
# Discord Commands
# ###

bot = commands.Bot(command_prefix='!')

async def status_task(passedChoices):
    await bot.change_presence(activity=discord.Game(name="the loading music..."))
    await asyncio.sleep(10)
    while True:
        i = random.randint(1,4)
        if i==1 | i==2:
            await bot.change_presence(activity=discord.Game(name=(random.choice(passedChoices['games']))['text']))
        elif i==3:
            await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name=(random.choice(passedChoices['listens']))['text']))   
        elif i==4:
            await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=(random.choice(passedChoices['watches']))['text']))
        # Setting `Streaming ` status
            # await bot.change_presence(activity=discord.Streaming(name="My Stream", url=my_twitch_url))   
        await asyncio.sleep(900)

@bot.event
async def on_ready():
    guild = discord.utils.get(bot.guilds, name=GUILD)
    print(
        f'{bot.user.name} has connected to the following guild:\n'
        f'{guild.name}(id: {guild.id})'
    )    
    ErrChannel = get_error_channel()
    await ErrChannel.send("QuoteBot has Connected")
    try:
        with open(runDirectory+'status.json') as f:
            statusChoices = json.load(f)
        bot.loop.create_task(status_task(statusChoices))    
    except Exception as e:
        print(e)
        await ErrChannel.send("Error Finding response from Status File")

@bot.event
async def on_member_join(member):
	await member.create_dm()
	await member.dm_channel.send(
		f'Hi {member.name}, welcome to Paper Handgrenades!'
		)

@bot.command(name='99', help='Responds with a a random quote from Brooklyn 99')
async def nine_nine(ctx):
    ErrChannel = get_error_channel()
    try:
        with open(runDirectory+'B99.json') as f:
            b99Options = json.load(f)
        await ctx.send((random.choice(b99Options['responses']))['text'])
    except Exception as e:
        print(e)
        await ErrChannel.send("Error Finding response from Brooklyn 99")
    
    
@bot.command(name='8Ball', help='Responds with a a random selection from the Magic 8 Ball')
async def eight_ball(ctx,question='8BALL'):
    ErrChannel = get_error_channel()
    try:
        with open(runDirectory+'8Ball.json') as f:
            eightBallOptions = json.load(f)
        if(question=='8BALL' or question[-1] != '?'):
            await ctx.author.send(eightBallOptions['msgError'])
        else: 
            await ctx.send((random.choice(eightBallOptions['responses']))['text']) 
    except Exception as e:
        print(e)
        await ErrChannel.send("Error Finding response from Magic 8 Ball")

    
# ###
# Error Handling and Execution
# ###

bot.run(TOKEN)
