import discord
from discord.ext import commands
import logging
from dotenv import load_dotenv
import os
import webserver 
import datetime
import ast
from pytz import timezone, utc
import random


load_dotenv()

token = os.getenv('DISCORD_TOKEN')
bday = os.getenv('BDAY')
secret = os.getenv('SECRET')
directory = ast.literal_eval(os.getenv('DIRECTORY'))
available = os.getenv('AVAILABLE') == True
owner = ast.literal_eval(os.getenv('OWNER'))


handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')

intents = discord.Intents.default()

intents.message_content = True

intents.members = True

bot = commands.Bot(command_prefix='/', intents = intents)

pings = []


@bot.event
async def on_ready():
    print(f"on_ready called {bot.user.name}")


@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    
    reply = ""
    for m in message.mentions:
        if m.id == owner:
            pings.append(message.created_at)
            if not available:
                reply += "I don't think he's available right now."
            break


    date = datetime.datetime.now(tz=utc)
    date = date.astimezone(timezone('US/Pacific'))
    if date.strftime('%m-%d') == bday:
        if "happy birthday" in message.content.lower() or "hbd" in message.content.lower:
            await message.add_reaction(str('❤️'))
            if reply == "":
                choice = random.randint(0,1)
                if choice == 0:
                    reply += "Thanks " + directory[message.author.id] + "!" 
                elif choice == 1:
                    reply += "tysm " + directory[message.author.id] + "!"
            else:
                choice = random.randint(0,1)
                if choice == 0:
                    reply += "I'm sure he's grateful though."
                elif choice == 1:
                    reply += "I'll pass it on. Thanks!"
    
    if secret in message.content.lower():
        await message.delete()
        await message.channel.send(f"{message.author.mention} counted!")


    await message.channel.send(reply)
    await bot.process_commands(message)

@bot.command()
async def hello(ctx):
    await ctx.send(f"Hello {ctx.author.mention}!")


webserver.keep_alive()
bot.run(token, log_handler=handler, log_level=logging.DEBUG)