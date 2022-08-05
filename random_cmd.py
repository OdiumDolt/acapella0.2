import random


async def random_option(message):
    message.content = message.content[len("random") + 1:]
    message.content = message.content.split(" ")
    try:
        await message.channel.send(message.content[random.randint(0, len(message.content) - 1)])
    except ValueError:
        await message.channel.send("Please enter options to pick from")
