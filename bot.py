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
    
    
    
    ydl_opts = {
        'format': 'bestaudio[ext=mp3]/bestaudio[ext=ogg]/best[ext=mp4]/best[ext=m4a]/best[ext=mkv]/best' ,
        'postprosessors': [{
            'key' : 'FFmpegExtractAudio' ,
            'preferredcodec': 'mp3' ,
            'preferredquality': '192' ,
        }],
    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        await ctx.send("Preparing to play")
        ydl.download([url_])
        
        await ctx.send("Music is about to play")
    for file in os.listdir("./"):
        if file.endswith(".mp4"):
            os.rename(file, "vid.mp4")
            exe="yes | ffmpeg -i vid.mp4 -vn \
            -acodec libmp3lame -ac 2 -qscale:a 4 -ar 48000 \
            audio.mp3"
            os.system(exe)
            await ctx.send("Music Loading............")
            
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    if voice == None: # None being the default value if the bot isnt in a channel (which is why the is_connected() is returning errors)
        await voiceChannel.connect()
        await ctx.send(f"Joined **{voiceChannel}**")
        voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    else:
        await ctx.send("I'm already connected!")
    await ctx.send("Playing......")
    
    voice.play(discord.FFmpegPCMAudio("audio.mp3"))
@client.command()
async def leave(ctx):
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)

    if voice.is_connected():

        
        await voice.disconnect()
        await ctx.send("Disconnected")

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
