import discord
from discord.ext import commands
import os
from dotenv import load_dotenv

load_dotenv()
intents = discord.Intents.default()
intents.message_content=True

bot = commands.Bot(command_prefix='$', intents=intents)
@bot.event
async def on_ready():
    print(f"{bot.user} has logged in!")

@bot.command()
async def greet(ctx):
    await ctx.send("Hello little buddy")


bot.run(os.getenv("DISCORD_TOKEN"))


