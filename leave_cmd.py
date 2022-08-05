from common import connected_channels
from common import queue


async def leave(message):
    try:
        try:
            connected_channels[message.guild.name].stop()
        except:
            pass
        await connected_channels[message.guild.name].disconnect()
        queue[message.guild.name] = []
    except KeyError:
        await message.channel.send("Bot was never conneceted to chat")