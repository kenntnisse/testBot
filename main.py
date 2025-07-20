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
trigger = os.getenv('TRIGGER')


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
    


    reply = ""

    pings = []
    fin = open("pings.txt", "r+")
    for line in fin.readlines():
        message.channel.send(line)
        pings.append(datetime.datetime.fromisoformat(line))
    fin.close()

    message.channel.send(str(pings))
    for m in message.mentions:
        if m.id == owner:
            if not available:
                unavailable = "I don't think he's available right now. "
                if (random.randint(0, 2) == 1):
                    unavailable += "Try texting him. I'd give it a 50/50 of working, but then I heard you gacha players like that. "
                else:
                    unavailable = "Shunzo's not here right now. "
                await message.channel.send("not available")
                if len(pings) == 0:
                    reply += unavailable
                    await message.channel.send("pings 0")
                elif message.created_at - pings[-1] > datetime.timedelta(minutes=5):
                    reply += unavailable
                    await message.channel.send("last ping more than 5 minutes ago")
            await message.channel.send("???????"+str(pings))
            pings.append(message.created_at)
            await message.channel.send("ping added"+str(pings))
            i = 0
            while i < len(pings) and message.created_at - pings[i] > datetime.timedelta(minutes=5):
                i += 1
            pings = pings[i:]
            message.channel.send(str(pings))
            if len(pings) == 3:
                await message.channel.send("Spam identifier activated...")
            elif len(pings) == 6:
                await message.channel.send("Hey, that's spam, right? Stop that.")
            elif len(pings) == 10:
                await message.channel.send("Quit it.")
            elif len(pings) == 50:
                await message.channel.send("Ok, that's impressive.")
            break
    
    fout = open("pings.txt", "w+")
    toWrite = ""
    for d in pings:
        toWrite += d.isoformat() +  "\n"
    toWrite.strip()
    fout.write(toWrite)
    fout.close()

    date = datetime.datetime.now(tz=utc)
    date = date.astimezone(timezone('US/Pacific'))
    if date.strftime('%m-%d') == bday:
        if "happy birthday" in message.content.lower() or "hbd" in message.content.lower():
            await message.add_reaction('❤️')
            if reply == "":
                choice = random.randint(0,1)
                if choice == 0:
                    reply += "Thanks " + directory[message.author.id] + "!" 
                elif choice == 1:
                    reply += "tysm " + directory[message.author.id] + "!"
            else:
                choice = random.randint(0,1)
                if choice == 0:
                    reply += "But, I'm sure he's grateful though."
                elif choice == 1:
                    reply += "I'll pass it on anyway. Thanks!"
    
    if trigger.lower() in message.content.lower():
        choice = random.randint(0,99)
        if choice == 99:
            await message.channel.send(f"I'll be seeing you soon... {directory[message.author.id]}")
        elif choice < 50:
            await message.channel.send(f"awww I missed you too, {directory[message.author.id]}")
        else:
            await message.channel.send("<3")


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