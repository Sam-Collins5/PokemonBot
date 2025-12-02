from fastapi import FastAPI, Request
from database_operations import *
from database_models import *

app = FastAPI()

@app.get("/")
async def root():
    return { "message": "this is the Pokemon discord bot database API" }


# User

@app.get("/users/")
async def read_users():
    users = get_users()
    if not users:
        return
    user_list = list()
    for user in users:
        user_list.append(user.json())
    return user_list


@app.get("/users/userId/{userId}")
async def read_user(userId: str = ""):
    if not userId:
        return
    user = get_user(int(userId))
    if not user:
        return
    return user.json()


@app.get("/users/discordId/{discordId}")
async def read_user_by_discord_id(discordId: str = ""):
    if not discordId:
        return
    user = get_user_by_discord_id(int(discordId))
    if not user:
        return
    return user.json()


@app.put("/users/{userId}", response_model=dict)
async def update_user(userId: str, updated_user: dict):
    if not userId or not updated_user:
        return
    user = user_update(int(userId), updated_user)
    return user.json()


@app.post("/users/", response_model=dict)
async def create_user(new_user: dict):
    if not new_user:
        return
    try:
        print(new_user)
        user = user_create(new_user)
        return user.json()
    except Exception as e:
        print(f"create_user failed: {e}")
        return


@app.delete("/users/{userId}")
async def delete_user(userId: str):
    if not userId:
        return
    user_delete(int(userId))


# Teams

@app.get("/teams/all")
async def read_teams():
    teams = get_teams()
    if not teams:
        return
    team_list = list()
    for team in teams:
        team_list.append(team.json())
    return team_list


@app.get("/teams/")
async def read_team(userId: str = "", teamId: str = ""):
    if not userId or not teamId:
        return
    team = get_user_team(int(userId), int(teamId))
    if not team:
        return
    return team.json()


@app.get("/teams/userId/{userId}")
async def read_user_teams(userId: str = ""):
    if not userId:
        return
    teams = get_user_team(int(userId))
    if not teams:
        return
    team_list = list()
    for team in teams:
        team_list.append(team.json())
    return team_list


@app.put("/teams/{teamId}", response_model=dict)
async def update_team(teamId: str, updated_team: dict):
    if not teamId or not updated_team:
        return
    team = team_update(int(teamId), updated_team)
    return team.json()


@app.post("/teams/", response_model=dict)
async def create_team(new_team: dict):
    if not new_team:
        return
    try:
        team = team_create(new_team)
        return team.json()
    except Exception as e:
        print(f"create_team failed: {e}")
        return


@app.delete("/teams/{teamId}")
async def delete_user(userId: str):
    if not userId:
        return
    user_delete(int(userId))


# Pokemon

@app.get("/pokemon/all")
async def read_all_pokemon():
    pokemon = get_all_pokemon()
    if not pokemon:
        return
    pokemon_list = list()
    for mon in pokemon:
        pokemon_list.append(mon.json())
    return pokemon_list


@app.get("/pokemon/{pokemonId}")
async def read_pokemon(pokemonId: str = ""):
    if not pokemonId:
        return
    pokemon = get_pokemon(int(pokemonId))
    if not pokemon:
        return
    return pokemon.json()


@app.get("/pokemon/get/")
async def read_pokemon_by_team(userId: str = "", teamId: str = ""):
    if not userId or not teamId:
        return
    pokemon = get_pokemon_by_team(int(userId), int(teamId))
    if not pokemon:
        return
    pokemon_list = list()
    for mon in pokemon:
        pokemon_list.append(mon.json())
    return pokemon_list


@app.put("/pokemon/{pokemonId}", response_model=dict)
async def update_pokemon(pokemonId: str, updated_pokemon: dict):
    if not pokemonId or not update_pokemon:
        return
    pokemon = pokemon_update(int(pokemonId), updated_pokemon)
    return pokemon.json()


@app.post("/pokemon/", response_model=dict)
async def create_pokemon(new_pokemon: dict):
    if not new_pokemon:
        return
    try:
        pokemon = pokemon_create(new_pokemon)
        return pokemon.json()
    except Exception as e:
        print(f"create_pokemon failed: {e}")
        return


@app.delete("/pokemon/{pokemonId}")
async def delete_pokemon(pokemonId: str):
    if not pokemonId:
        return
    pokemon_delete(int(pokemonId))


def main():
    database_init()


main()
