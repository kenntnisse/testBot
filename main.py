import discord
from discord.ext import commands
import logging
from dotenv import load_dotenv
import os
import webserver 
from datetime import datetime

load_dotenv()

token = os.getenv('DISCORD_TOKEN')
bday = os.getenv('BDAY')
secret = os.getenv('SECRET')

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
    
    if datetime.today().strftime('%m-%d') == bday:
        await message.channel.send(f"Thanks! {message.author}")

    if secret in message.content.lower():
        await message.delete()
        await message.channel.send(f"{message.author.mention} counted!")


    await bot.process_commands(message)

@bot.command()
async def hello(ctx):
    await ctx.send(f"Hello {ctx.author.mention}!")


webserver.keep_alive()
bot.run(token, log_handler=handler, log_level=logging.DEBUG)