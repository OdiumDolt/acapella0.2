from common import queue
import pafy.pafy
import urllib
import re

async def add_to_queue(message):
    new_queue_item = {
        "got_from":"",
        "url":"",
        "title":"",
        "print_playing":True
    }

    if message.content[0:23] == "https://www.youtube.com":
        url = message.content
        new_queue_item["got_from"] = "url"

    else:
        url_or_term = message.content.replace(" ", "+")
        html = urllib.request.urlopen("https://www.youtube.com/results?search_query=" + url_or_term)
        video_ids = re.findall(r"watch\?v=(\S{11})", html.read().decode())
        url = "https://www.youtube.com/watch?v=" + video_ids[0]
        new_queue_item["got_from"] = "search"
    
    video = pafy.new(url)
    new_queue_item["title"] = video.title
    new_queue_item["url"] = url
    if new_queue_item["got_from"] == "search":
        await message.channel.send("Added " + video.title + "\n" + url)
    else:
        await message.channel.send("Added " + video.title)

    queue[message.guild.name].append(new_queue_item)