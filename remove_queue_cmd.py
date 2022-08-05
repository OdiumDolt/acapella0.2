from common import queue
from common import connected_channels


async def remove(message):

    message.content = message.content[len("remove") + 1:]

    try:
        if len(queue[message.guild.name]) == 0:
            await message.channel.send("No song to remove from queue beep")
            return False
    except KeyError:
        await message.channel.send("No song to remove from queue")
        return False

    if message.content == "":
        await message.channel.send("Please enter a song to remove from queue")
        return False
    
    index = int(message.content) - 1

    if index > len(queue[message.guild.name]) - 1:
        await message.channel.send("That song does not exist")
        return False
    elif index < 0:
        await message.channel.send("please pick a big boy number. not a little boy negitive number")
        return False

    try:
        if index == 0:
            connected_channels[message.guild.name].stop()
        else:
            del queue[message.guild.name][index]
    except:
        await message.channel.send("no clue what happened tbh")
