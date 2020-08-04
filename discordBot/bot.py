import discord
from random import randint
from random_username.generate import generate_username
import string
import time
import requests

randomWordAPI = "https://random-word-api.herokuapp.com/word?number=1"
token = "YOUR_TOKEN_HERE"
client = discord.Client()

def emptyString():
    temp = randint(0, 200)
    string = ""
    while temp > 0:
        temp -= 1
        string = string + " "

    return string


@client.event
async def on_message(message):
    ################################################ ROLL NUMBER GAME ################################################
    if message.content.startswith("!play"):
        sender = message.author
        against = message.content.split(" ")[1]
        againstId = against.split("!")[1][:-1]
        temp = await client.fetch_user(againstId)
        againstUser = temp
        user1 = randint(0,100)
        user2 = randint(0,100)

        winner = sender
        if user1 < user2:
            winner = againstUser

        embed = discord.Embed(title="Result", description="The winner is {}!".format(winner.mention), colour=discord.Color.teal())
        embed.set_thumbnail(url=winner.avatar_url_as(size=64))
        embed.add_field(name=sender.display_name, value=user1)
        embed.add_field(name=againstUser.display_name, value=user2)

        await message.channel.send(content=None, embed=embed)

    ################################################ RANDOM USERNAME ################################################
    elif message.content.startswith("!username"):
        await message.channel.send(generate_username(1)[0])

    ################################################ RANDOM EMOJI IN CHAT ################################################
    elif message.content.startswith("!q"):
        string = emptyString()
        emoji = str(message.guild.emojis[randint(0, len(message.guild.emojis) - 1)])
        #a = await message.channel.send("```{}{{}}{}```".format(string, emoji, string))
        a = await message.channel.send(f"|{string}{emoji}{string}|")

        i = 0
        while i < 6:
            i+=1
            string = emptyString()
            emoji = str(message.guild.emojis[randint(0, len(message.guild.emojis) - 1)])
            time.sleep(2)
            #await a.edit(content="```{}{{}}{}```".format(string, emoji, string))
            await a.edit(content=f"|{string}{emoji}{string}|")

    ################################################ HANGMAN ################################################
    elif message.content.startswith("!hangman"):
        await message.channel.send("Let's play a game!")
        time.sleep(1)
        await message.channel.send("Start guessing...")
        time.sleep(0.5)

        r = requests.get(randomWordAPI)
        word = r.json()[0]
        guesses = ""
        turns = 10

        while turns > 0:
            failed = 0
            temp = "`"
            for char in word:
                if char in guesses:
                    temp = temp + char
                else:
                    temp = temp + " _ "
                    failed += 1

            if failed == 0:
                await message.channel.send(temp + "`")
                await message.channel.send("You won")
                break

            await message.channel.send(temp + "`")

            guess = await client.wait_for("message")

            if guess.content == "!stop":
                await message.channel.send("Game stopped...")
                break
            elif len(guess.content) != 1:
                await message.channel.send("Please input exactly one character!")
            else:
                if guess.content not in guesses:
                    guesses += guess.content

                    if guess.content not in word:
                        turns -= 1
                        await message.channel.send("Wrong")
                    else:
                        await message.channel.send("Correct")
                    await message.channel.send("You have " + str(turns) + " more guesses")

                    if turns == 0:
                        await message.channel.send('You lose, the word was "' +  word + '"')
                else:
                    await message.channel.send("Character '" + guess.content + "' already guessed!")

    elif message.content.startswith("!test"):
        a = "a"
        string = "sd"
        if a in string:
            print("A")
        else:
            print("B")

client.run(token)
