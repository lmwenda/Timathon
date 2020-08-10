import time
from random import randint
import discord
import requests
from random_username.generate import generate_username
import youtube_dl
import os
from youtube_search import YoutubeSearch

help = """```
~help = List of commands
~roll = Play the Roll Number Game
~username = Returns a random username
~emoji = Returns a random server emoji, jumping around
~hangman = Play the Hangman Game
~play = Play song in current voice channel
~leave = Leave the current voice channel and clean Queue
```"""

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
    ################################################ HELP ################################################
    if message.content.startswith("~help"):
        embed = discord.Embed(colour=discord.Color.teal())
        embed.add_field(name="Command Help List", value=help)
        await message.channel.send(content=None, embed=embed)
    ################################################ ROLL NUMBER GAME ################################################
    elif message.content.startswith("~roll"):
        sender = message.author
        against = message.content.split(" ")[1]
        againstId = against.split("~")[1][:-1]
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
    elif message.content.startswith("~username"):
        await message.channel.send(generate_username(1)[0])

    ################################################ RANDOM EMOJI IN CHAT ################################################
    elif message.content.startswith("~emoji"):
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
    elif message.content.startswith("~hangman"):
        user = message.author
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

            if guess.content == "~stop" and guess.author == user:
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

    ################################################ YOUTUBE - PLAY SONG ################################################
    elif message.content.startswith("~play"):
        dirCount = len(os.listdir("./Queue"))
        video = message.content.split(" ", 1)[1]
        await message.channel.send("Searching for: `{}`".format(video))
        urlSuffix = YoutubeSearch(video).to_dict()[0]["url_suffix"]
        url = "https://www.youtube.com" + urlSuffix

        def cleanQueue(path):
            os.remove(path)

            songCounter = len(os.listdir("./Queue"))

            if songCounter == 0:
                print("STOP PLAYING")
            else:
                nextSong = "C:/Users/Nabernik/PycharmProjects/discordBot/Queue/" + os.listdir("./Queue/")[0]
                connected.play(discord.FFmpegPCMAudio(nextSong), after=lambda e: cleanQueue(nextSong))

        if dirCount == 0:
            songNumber = 0
        else:
            songNumber = int(os.listdir("./Queue/")[-1].split(".")[0].split("g")[1]) + 1

        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': 'C:/Users/Nabernik/PycharmProjects/discordBot/Queue/song' + str(songNumber) + '.mp3',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
        }

        with youtube_dl.YoutubeDL(ydl_opts) as ytdl:
            extract = ytdl.extract_info(url)
            print(extract)

        if dirCount == 0:
            server = message.author.voice.channel.id
            vc = client.get_channel(server)
            connected = await vc.connect()
            path = "C:/Users/Nabernik/PycharmProjects/discordBot/Queue/song" + str(int(os.listdir("./Queue/")[-1].split(".")[0].split("g")[1])) + ".mp3"
            # await ctx.message.channel.send("Now playing song: {}".format(title))
            connected.play(discord.FFmpegPCMAudio(path), after=lambda e: cleanQueue(path))

    ################################################ YOUTUBE - LEAVE CHANNEL ################################################
    elif message.content.startswith("~leave"):
        await client.voice_clients[0].disconnect()
        time.sleep(1)
        files = os.listdir("./Queue/")
        for file in files:
            os.remove("C:/Users/Nabernik/PycharmProjects/discordBot/Queue/" + file)

    ################################################ TESTING GROUNDS ################################################
    elif message.content.startswith("~test"):
        a = message.content.split(" ", 1)
        print(a)

client.run(token)