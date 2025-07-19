import discord
from discord.ext import commands
import logging
from dotenv import load_dotenv
import os
import webserver 
from datetime import datetime
import ast
load_dotenv()

token = os.getenv('DISCORD_TOKEN')
bday = os.getenv('BDAY')
secret = os.getenv('SECRET')
directory = ast.literal_eval(os.getenv('DIRECTORY'))
available = os.getenv('AVAILABLE') == True

handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')

intents = discord.Intents.default()

intents.message_content = True

intents.members = True

bot = commands.Bot(command_prefix='/', intents = intents)



@bot.event
async def on_ready():
    print(f"on_ready called {bot.user.name}")


@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    
    if datetime.now().strftime('%m-%d') == bday:
        await message.channel.send(f"Thanks! {directory[message.author.id]}")

    if secret in message.content.lower():
        await message.delete()
        await message.channel.send(f"{message.author.mention} counted!")

    if "@kitherain_29768" in message.content.lower():
        await message.channel.send(f"pinged{message.author}")


    await bot.process_commands(message)

@bot.command()
async def hello(ctx):
    await ctx.send(f"Hello {ctx.author.mention}!")


webserver.keep_alive()
bot.run(token, log_handler=handler, log_level=logging.DEBUG)