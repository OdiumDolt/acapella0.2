import discord
from common import queue
from common import connected_channels
from play_cmd import play
from leave_cmd import leave
from remove_queue_cmd import remove
from random_cmd import random, random_option
from market.market_cmd import eco


client = discord.Client()

TOKEN = ""

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    # if the user is the bot, dont handle it as a request
    if message.author == client.user:
        return
    # parse messages for commands
    if message.content.startswith('!'):

        # erase the ! in the command for further parsing
        message.content = message.content[1:]
        if len(message.content) == 0:
            return False
#       ---ADD NEW COMMANDS HERE---

        if message.content[0].lower() == "p" and message.content[1] == " ":
            await play(message, client)

        elif message.content[0].lower() == "l" and len(message.content) == 1:
            await leave(message)
        
        elif message.content[0].lower() == "s" and len(message.content) == 1:
            try:
                await message.channel.send("Skipped... Now playing: " + queue[message.guild.name][1]["title"])
            except:
                await message.channel.send("Skipped")
            connected_channels[message.guild.name].stop()
        
        elif message.content[0].lower() == "q" and len(message.content) == 1:
            response = ""
            try:
                for i in queue[message.guild.name]:
                    response += "\n" + i["title"]
                if len(response) == 0:
                    await message.channel.send("There is no queue!")
                else:
                    await message.channel.send(response)
            except KeyError:
                await message.channel.send("The is no queue!")

        elif message.content[0:len("remove")].lower() == "remove":
            await remove(message)

        elif message.content[0:len("random")].lower() == "random":
            await random_option(message)

        elif message.content[0:len("eco")].lower() == "eco":
            await eco(message)

client.run(TOKEN)
