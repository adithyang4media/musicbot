import discord

from discord.ext import commands

import youtube_dl

import os




client = commands.Bot(command_prefix='!')


@client.command()

async def play(ctx, url_: str):

    song_there = os.path.isfile("song.mp3")

    try:

        if song_there:

            os.remove("song.mp3")

    except PermissionError:

        await ctx.send("Wait for the audio to stop or use !stop command")

        return

   
    voiceChannel = discord.utils.get(ctx.guild.voice_channels, name='General')

    

    
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    if voice == None: # None being the default value if the bot isnt in a channel (which is why the is_connected() is returning errors)
        await voiceChannel.connect()
        await ctx.send(f"Joined **{voiceChannel}**")
        voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    else:
        await ctx.send("I'm already connected!")





    ydl_opts = {

        'format': 'bestaudio[ext=mp3]/best' ,

        'postprosessors': [{

            'key' : 'FFmpegExtractAudio' ,

            'preferredcodec': 'mp3' ,

            'preferredquality': '192' ,

        }],

    }

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:

        ydl.download([url_])

    for file in os.listdir("./"):

        if file.endswith(".webm"):

            os.rename(file, "song.mp3")

    voice.play(discord.FFmpegPCMAudio("song.mp3"))



@client.command()

async def leave(ctx):

    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)

    if voice.is_connected():

        await voice.didconnect()

    else:

        await ctx.send("The bot is not connected to any voice channel")



@client.command()

async def pause(ctx):

    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)

    if voice.is_playing():

        await voice.pause()

    else:

        await ctx.send("No Audio is playing")



@client.command()

async def resume(ctx):

    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)

    if voice.is_paused():

        await voice.resume()

    else:

        await ctx.send("Audio not paused")



@client.command()
async def stop(ctx):

    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)

    voice.stop()





client.run(os.environ['token'])
