import discord
import asyncio
import os
import whisper
from discord.ext import commands
from discord import FFmpegPCMAudio
#dependencies:
#   py-cord
#   py-cord[voice]
#   openai-whisper

model = whisper.load_model("tiny")
def run_bot():
    TOKEN = ''
    intents = discord.Intents.all()
    bot = commands.Bot(command_prefix= '$',intents = discord.Intents.all())

    @bot.event
    async def on_ready():
        print(f'{bot.user} is running!')

    @bot.command(pass_context = True) # pass_context = true needed for vcs i guess??
    async def join(ctx): # !join joins users vc
        await join_vc(ctx)

    @bot.command(pass_context = True)
    async def leave(ctx): # !disconnect disconnects if in a vc
        await leave_vc(ctx)

    #records audio
    @bot.command()
    async def listen(ctx):
        if ctx.voice_client:
            ctx.voice_client.start_recording(discord.sinks.WaveSink(), callback, ctx)
            await ctx.send("listening...")
        else:
            await ctx.send("not in a voice channel!")

    #stops recording
    @bot.command()
    async def stop(ctx):
        ctx.voice_client.stop_recording()

    bot.run(TOKEN)

async def join_vc(ctx):
    if (ctx.author.voice): 
        channel = ctx.message.author.voice.channel
        return await channel.connect()
    else:
        await ctx.send("You are not in a voice channel, you must join a voice channel to summon me.")

async def leave_vc(ctx):
    if (ctx.voice_client):
        await ctx.voice_client.disconnect()
    else:
        await ctx.send("I'm not in a voice channel right now.")

async def callback(sink: discord.sinks, ctx):
        for user_id, audio in sink.audio_data.items():
            if user_id == ctx.author.id:
                audio: discord.sinks.core.AudioData = audio
                print(user_id)
                filename = "audio.wav"
                with open(filename, "wb") as f:
                    f.write(audio.file.getvalue())
                text = model.transcribe(filename)["text"]
                os.remove(filename)
                print(f"Received from {ctx.author.name}: {text}")

