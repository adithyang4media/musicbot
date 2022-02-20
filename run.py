import discord
from discord.ext import commands
import youtube_dl
import os
from pytube import YouTube
import urllib.request
import re
client = commands.Bot(command_prefix='!')

@client.event
async def on_ready():
    print("Bot is now up")
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="Youtube"))

@client.command()
async def play(ctx, url_1: str, url_2: str, url_3: str, url_4: str, url_5: str, url_6: str, url_7: str, url_8: str, url_9: str, url_10: str, url_11: str):
    url_=url_1+" "+url_2+" "+url_3+" "+url_4+" "+url_4+" "+url_5+" "+url_6+" "+url_7+" "+url_8+" "+url_9+" "+url_10+" "+url_11
    song_there = os.path.isfile("song.mp3")
    try:
        if song_there:
            os.remove("song.mp3")
    except PermissionError:
        await ctx.send("Wait for the audio to stop or use !stop command")
        return
   
    voiceChannel = discord.utils.get(ctx.guild.voice_channels, name='Music')
    filen = str(voiceChannel.id)
    filename = filen + ".mp3"
    fln = filen + ".mp3"
    if "https://youtu" in url_:
        print("Url Detected")
    else:
        print("Not Found")
        await ctx.send("Searching For " + url_)
        url_ = url_.replace(" ", "+")
        html = urllib.request.urlopen("https://www.youtube.com/results?search_query=" + url_)
        video_ids = re.findall(r"watch\?v=(\S{11})", html.read().decode())
        print("https://www.youtube.com/watch?v=" + video_ids[0])
        url_ = "https://www.youtube.com/watch?v=" + video_ids[0]
    
    
    
    await ctx.send("Searching...")
    yt = YouTube(url_)
    t = yt.streams.filter(only_audio=True)
    t[0].download('./')
    print("Processing")
        
    await ctx.send("Music is about to play")
    for file in os.listdir("./"):
        if file.endswith(".mp4"):
            os.rename(file, fln)
            exe="yes | ffmpeg -i " + fln + " -vn \
            -acodec libmp3lame -ac 2 -qscale:a 4 -ar 48000 \
            " + filename
            os.system(exe)
            await ctx.send("Music Loading............")
            
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    if voice == None: # None being the default value if the bot isnt in a channel (which is why the is_connected() is returning errors)
        await voiceChannel.connect()
        await ctx.send(f"Joined **{voiceChannel}**")
        voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    else:
        await ctx.send("I'm already connected!")
    
    await ctx.send("Playing.......")
    
    voice.play(discord.FFmpegPCMAudio(filename))
    user_id = "913780712715485254"
    await ctx.send(f"This bot was made by <@{user_id}> \n Thanks for using this Bot \n Have a Nice Day")
    
   
@client.command()
async def leave(ctx):
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)

    if voice.is_connected():

        
        await voice.disconnect()
        await ctx.send("Disconnected Use !play command to reconnect")

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
    
@client.command()
async def replay(ctx):
    voiceChannel = discord.utils.get(ctx.guild.voice_channels, name='Music')
    filen = str(voiceChannel.id)
    filename = filen + ".mp3"
    fln = filen + ".mp3"
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    await ctx.send("Playing.....")
    voice.play(discord.FFmpegPCMAudio(filename))
    
@client.command()
async def commands(ctx):
   await ctx.send("This Bot Was made by @adithyanspillai#1404 \n Bot Commands \n !play <youtube url> : Play a song \n !pause : Pause song \n !resume : Resume a paused song  \n !stop : Stop the current playing song \n !leave : Disconnect Bot From Voice Channel")
    
@client.command()
async def stats(ctx):
   count = f"{len(client.guilds)} servers!"
   await ctx.send(count)
   
client.run(os.environ['token'])
