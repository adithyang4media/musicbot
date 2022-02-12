import discord

from discord.ext import commands

import youtube_dl

import os




client = commands.Bot(command_prefix='!')


@client.command()

async def play(ctx, url_: str):
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    await client.join_voice_channel(voice)
    server = ctx.message.server
    voice_client = client.voice_client_in(server)
    player = await voice_client.create_ytdl_player(url)
    players[server.id] = player
    player.start()


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
