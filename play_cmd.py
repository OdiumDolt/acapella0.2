import discord
from youtube_dl import YoutubeDL
import asyncio
from helper import add_to_queue
from common import queue
from common import connected_channels


def play_next(message):
    try:
        del queue[message.guild.name][0]
        asyncio.run(play_song(message))
    except IndexError:
        pass

async def play_song(message):
    if len(queue[message.guild.name]) == 0:
        return False


    current_song = queue[message.guild.name][0]["url"]
    voice = connected_channels[message.guild.name]
    FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 1'}
    YDL_OPTIONS = {'format': 'bestaudio/best', 'noplaylist':'False', "cookiefile":"cookies.txt"}
    try:
        with YoutubeDL(YDL_OPTIONS) as ydl:
            info = ydl.extract_info(current_song, download=False)
            I_URL = info['formats'][0]['url']
            source = await discord.FFmpegOpusAudio.from_probe(I_URL, **FFMPEG_OPTIONS)
            voice.play(source, after=lambda e: play_next(message))
    except:
        print("a error accured")



async def play(message, client):
    try:

        message.content = message.content[2:]
        try:
            if connected_channels[message.guild.name].is_connected():
                await add_to_queue(message)
                if connected_channels[message.guild.name].is_playing() == False:
                    await play_song(message)
            else:
                try:
                    await connected_channels[message.guild.name].disconnect()
                except:
                    pass
                try:
                    await message.author.voice.channel.connect()
                    connected_channels[message.guild.name] = client.voice_clients[-1]
                    
                    queue[message.guild.name] = []
                    await add_to_queue(message)
                    await play_song(message)
                except AttributeError:
                    await message.channel.send("Please join a channel")

        except KeyError:
            try:
                try:
                    await connected_channels[message.guild.name].disconnect()
                except:
                    pass

                try:
                    await message.author.voice.channel.connect()
                    connected_channels[message.guild.name] = client.voice_clients[-1]
                    
                    queue[message.guild.name] = []
                    await add_to_queue(message)
                    await play_song(message)
                except AttributeError:
                    await message.channel.send("Please join a channel")
            
            except discord.errors.ClientException:
                await message.channel.send("To move acapella bot, please use !m")


    except IndexError:
        await message.channel.send("Please enter a URL or search term")