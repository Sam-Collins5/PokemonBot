import discord
from discord.ext import commands
import os
from dotenv import load_dotenv

import api_client

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



async def _get_db_user_id(discord_id: int):
    """
    Always ensure this Discord user exists in the DB,
    and return their database user_id.
    """
    user = await api_client.get_or_create_user(discord_id)
    return int(user["user_id"])


@bot.command()
async def register(ctx):
    """
    Ensure this Discord user exists in the database.
    Usage: $register
    """
    discord_id = ctx.author.id

    try:
        user = await api_client.get_or_create_user(discord_id)
    except api_client.ApiError as e:
        await ctx.send(f"❌ Failed to register you in the database:\n`{e}`")
        return

    await ctx.send(
        f"✅ You are registered!\n"
        f"- DB user_id: `{user['user_id']}`\n"
        f"- DiscordId stored as: `{user['discord_id']}`"
    )


@bot.command()
async def myteams(ctx):
    """
    List all teams associated with this Discord user.
    Usage: $myteams
    """
    discord_id = ctx.author.id
    db_user_id = await _get_db_user_id(discord_id)

    if db_user_id is None:
        await ctx.send(
            "You are not registered yet. Use `$register` first so I can link you in the database."
        )
        return

    try:
        teams = await api_client.list_teams_for_user(db_user_id)
    except api_client.ApiError as e:
        await ctx.send(f"❌ Failed to fetch your teams:\n`{e}`")
        return

    if not teams:
        await ctx.send("You don't have any teams yet. Use `$createteam` to make one!")
        return

    lines = []
    for team in teams:
        team_id = team["team_id"]
        name = team["team_name"]
        mons = [
            team["pokemon_id1"],
            team["pokemon_id2"],
            team["pokemon_id3"],
            team["pokemon_id4"],
            team["pokemon_id5"],
            team["pokemon_id6"],
        ]
        lines.append(f"- **{name}** (ID `{team_id}`) – Pokémon IDs: {mons}")

    await ctx.send("📋 **Your Teams:**\n" + "\n".join(lines))

@bot.command()
async def createteam(ctx, name: str, *pokemon_ids: int):
    """
    Create a new team for this user.
    Usage: $createteam "Team Name" 1 6 25 39 131 150
    (exactly 6 Pokémon IDs)
    """
    discord_id = ctx.author.id
    db_user_id = await _get_db_user_id(discord_id)

    if db_user_id is None:
        await ctx.send(
            "You are not registered yet. Use `$register` first so I can link you in the database."
        )
        return

    if len(pokemon_ids) != 6:
        await ctx.send(
            "Please provide exactly 6 Pokémon IDs.\n"
            'Example: `$createteam "Kanto Faves" 1 6 25 39 131 150`'
        )
        return

    try:
        team = await api_client.create_team_for_user(
            db_user_id,
            name,
            list(pokemon_ids),
        )
    except (api_client.ApiError, ValueError) as e:
        await ctx.send(f"❌ Failed to create your team:\n`{e}`")
        return

    await ctx.send(
        f"✅ Created team **{team['team_name']}** with ID `{team['team_id']}` "
        f"for <@{discord_id}>."
    )

bot.run(os.getenv("DISCORD_TOKEN"))

