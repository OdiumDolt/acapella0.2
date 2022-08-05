import json

async def eco(message):
    
    with open("player_data.json", "r") as read_file:
        players = json.load(read_file)

    message.content = message.content[len("eco") + 1:]
    message.content = message.content.split(" ")


    if message.content[0].lower() == "gift":
        if message.content[1].lower() == "invite":
            if players[message.author.name]["balance"] > int(message.content[3]):
                
                players[message.content[2]]["trade_requests"] = {
                    "from":message.author.name, 
                    "amount":int(message.content[3]), 
                    "to": message.content[1]}

                with open("player_data.json", "w") as write_file:
                    json.dump(players, write_file, indent=4)
                
                await message.channel.send("Invited " + message.content[2] + ". They can accept with !eco gift accept")
            else:
                await message.channel.send("Maybe get your own bread up before trying to give it to others. " + message.content[3])

        elif message.content[1].lower() == "accept":
            try:
                
                await message.channel.send(message.author.name + " has accepted " + str(players[message.author.name]["trade_requests"]["amount"]) + " from " + players[message.author.name]["trade_requests"]["from"])
                
                players[message.author.name]["balance"] += players[message.author.name]["trade_requests"]["amount"]
                players[players[message.author.name]["trade_requests"]["from"]]["balance"] -= players[message.author.name]["trade_requests"]["amount"]
                players[message.author.name]["trade_requests"] = {}
                with open("player_data.json", "w") as write_file:
                    json.dump(players, write_file, indent=4)

            except KeyError:
                await message.channel.send("No gift to accept!")

    elif message.content[0].lower() == "create":
        
        players[message.author.name] = {
        "balance":1000,
        "trade_requests":{},
    }
        with open("player_data.json", "w") as write_file:
            json.dump(players, write_file, indent=4)

    elif message.content[0].lower == "b" or message.content[0].lower == "balance":
        try:
            await message.channel.send(players[message.author.name]["balance"])
        except KeyError:
            await message.channel.send("You dont have a wallet!")

    
