import time
from random import randint
import discord
import requests
from random_username.generate import generate_username
import youtube_dl
from discord.ext import commands
import os
import webbrowser

players = {}

help = """```
~help = List of commands
~roll = Play the Roll Number Game
~username = Returns a random username
~emoji = Returns a random server emoji, jumping around
~hangman = Play the Hangman Game
```"""

randomWordAPI = "https://random-word-api.herokuapp.com/word?number=1"
token = "YOUR_TOKEN_HERE"
bot = commands.Bot(command_prefix="~")

@bot.event
async def on_ready():
    presence = discord.Game("Yay, Voice Commands work now")
    print("READY")
    await bot.change_presence(status=discord.Status.idle, activity=presence)

################################################ HELP ################################################
@bot.command(pass_context=True)
async def help1(ctx):
    embed = discord.Embed(colour=discord.Color.teal())
    embed.add_field(name="Command Help List", value=help)
    await ctx.message.channel.send(content=None, embed=embed)

@bot.command(pass_context=True)
async def roll(ctx):
    sender = ctx.message.author
    against = ctx.message.content.split(" ")[1]
    againstId = against.split("!")[1][:-1]
    temp = await bot.fetch_user(againstId)
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

    await ctx.message.channel.send(content=None, embed=embed)

################################################ RANDOM USERNAME ################################################
@bot.command(pass_context=True)
async def username(ctx):
    await ctx.message.channel.send(generate_username(1)[0])

################################################ HANGMAN ################################################
@bot.command(pass_context=True)
async def hangman(ctx):
    user = ctx.message.author
    await ctx.message.channel.send("Let's play a game!")
    time.sleep(1)
    await ctx.message.channel.send("Start guessing...")
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
            await ctx.message.channel.send(temp + "`")
            await ctx.message.channel.send("You won")
            break

        await ctx.message.channel.send(temp + "`")

        guess = await bot.wait_for("message")

        if guess.content == "~stop" and guess.author == user:
            await ctx.message.channel.send("Game stopped...")
            break
        elif len(guess.content) != 1:
            await ctx.message.channel.send("Please input exactly one character!")
        else:
            if guess.content not in guesses:
                guesses += guess.content

                if guess.content not in word:
                    turns -= 1
                    await ctx.message.channel.send("Wrong")
                else:
                    await ctx.message.channel.send("Correct")
                await ctx.message.channel.send("You have " + str(turns) + " more guesses")

                if turns == 0:
                    await ctx.message.channel.send('You lose, the word was "' +  word + '"')
            else:
                await ctx.message.channel.send("Character '" + guess.content + "' already guessed!")

################################################ YOUTUBE - JOIN CHANNEL ################################################
@bot.command(pass_context=True)
async def join(ctx):
    voiceChannel = ctx.message.author.voice.channel.id
    vc = bot.get_channel(voiceChannel)
    a = await vc.connect()
    #print(voice)
    #await client.join_voice_channel(channel)

################################################ YOUTUBE - PLAY MUSIC ################################################
@bot.command(pass_context=True)
async def play(ctx, url):
    dirCount = len(os.listdir("./Queue"))
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
        title = ytdl.extract_info(url)["title"]

    if dirCount == 0:
        server = ctx.message.author.voice.channel.id
        vc = bot.get_channel(server)
        connected = await vc.connect()
        path = "C:/Users/Nabernik/PycharmProjects/discordBot/Queue/song" + str(int(os.listdir("./Queue/")[-1].split(".")[0].split("g")[1])) + ".mp3"
        #await ctx.message.channel.send("Now playing song: {}".format(title))
        connected.play(discord.FFmpegPCMAudio(path), after=lambda e: cleanQueue(path))

################################################ YOUTUBE - LEAVE THE CHANNEL AND RESET QUEUE ################################################
@bot.command(pass_context=True)
async def leave(ctx):
    await bot.voice_clients[0].disconnect()
    time.sleep(1)
    files = os.listdir("./Queue/")
    for file in files:
        os.remove("C:/Users/Nabernik/PycharmProjects/discordBot/Queue/" + file)

################################################ OPEN URL IN BROWSER ################################################
@bot.command(pass_context=True)
async def open(ctx):
    webbrowser.open("https://docs.python.org/3/library/webbrowser.html")

################################################ TESTING GROUNDS ################################################
@bot.command(pass_context=True)
async def test(ctx):
    print("A")

bot.run(token)