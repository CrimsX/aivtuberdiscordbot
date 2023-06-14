import discord

def run_bot():
    TOKEN = ''
    client = discord.Client()

    @client.event
    async def on_ready():
        print(f'{client.user} is running!')
        

        client.run(TOKEN)
