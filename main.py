import discord
from discord.ext import commands

client = commands.Bot(command_prefix = '!', intents = discord.Intents.all())

@client.event 
async def on_ready():
    print("successfully logged on as: bot")

@client.command() # !hello command says hello
async def hello(ctx):
    await ctx.send("hello")

@client.command(pass_context = True) # pass_context = true needed for vcs i guess??
async def join(ctx): # !join joins users vc
    if (ctx.author.voice): 
        channel = ctx.message.author.voice.channel
        await channel.connect()
    else:
        await ctx.send("You are not in a voice channel, you must join a voice channel to summon me.")

@client.command(pass_context = True)
async def disconnect(ctx): # !disconnect disconnects if in a vc
    if (ctx.voice_client):
        await ctx.guild.voice_client.disconnect()
        await ctx.send("Left voice channel")
    else:
        await ctx.send("I'm not in a voice channel right now.")

client.run('INSERT TOKEN HERE') # PUT TOKEN IN HERE~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
