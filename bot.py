# bot.py


import os
import random
import logging
import discord
import requests
import json
from dotenv import load_dotenv
from discord.ext import commands

# ###
# Load Items
# ###
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')
runDirectory = os.path.dirname(os.path.realpath(__file__))+"/"

logging.basicConfig(level=logging.INFO)


# ###
# Discord Commands
# ###

bot = commands.Bot(command_prefix='!')

@bot.event
async def on_ready():
	guild = discord.utils.get(bot.guilds, name=GUILD)
	print(
		f'{bot.user.name} has connected to the following guild:\n'
		f'{guild.name}(id: {guild.id})'
	)

@bot.event
async def on_member_join(member):
	await member.create_dm()
	await member.dm_channel.send(
		f'Hi {member.name}, welcome to Paper Handgrenades!'
		)

#@bot.command(name='donations', cls=participantID, help='Looks up most recent donation')
#async def donations(ctx):
#	url = "https://www.extra-life.org/api/participants/%s/donations" % participantID
#	payload = {}
#	headers = {}
#	response = requests.request("GET", url, headers=headers, data = payload)

#	await ctx.send(response)

@bot.command(name='99', help='Responds with a a random quote from Brooklyn 99')
async def nine_nine(ctx):
    try:
        with open(runDirectory+'B99.json') as f:
            b99Options = json.load(f)
        response = (random.choice(b99Options['responses']))['text']
    except Exception as e:
        print(e)
        response = "Error Finding response from Brooklyn 99"
    await ctx.send(response)
    
@bot.command(name='8Ball', help='Responds with a a random selection from the Magic 8 Ball')
async def eight_ball(ctx,question='8BALL'):
    try:
        with open(runDirectory+'8Ball.json') as f:
            eightBallOptions = json.load(f)
        if(question=='8BALL' or question[-1] != '?'):
            response = eightBallOptions['msgError']
        else: 
            response = (random.choice(eightBallOptions['responses']))['text']
    except Exception as e:
        print(e)
    await ctx.send(response)    
    
     
# ###
# Error Handling and Execution
# ###

@bot.event
async def on_command_error(ctx, error):
	if isinstance(error, commands.errors.CommandNotFound):
		await ctx.send('The command you entered does not exist')
	else:
		with open('err.log', 'a') as f:
			f.write(f'Unhandled message: {error}\n')

bot.run(TOKEN)
