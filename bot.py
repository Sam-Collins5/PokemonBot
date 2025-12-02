import discord
import os
from dotenv import load_dotenv

load_dotenv()
intents = discord.Intents.default()
intents.message_content=True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f"{client.user} has logged in!")


client.run(os.getenv("DISCORD_TOKEN"))