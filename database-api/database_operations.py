import sqlalchemy
from sqlalchemy import Column, String, Integer, create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from database_models import *

# User

def get_users():
    try:
        global session
        return session.query(User).all()
    except Exception as e:
        print(f"get_users failed: {e}")


def get_user(user_id: int):
    try:
        global session
        return session.query(User).where(User.UserId == user_id).first()
    except Exception as e:
        print(f"get_user failed: {e}")


def get_user_by_discord_id(discord_id: int):
    try:
        global session
        return session.query(User).where(User.DiscordId == discord_id).first()
    except Exception as e:
        print(f"get_user_by_discord_id failed: {e}")


def user_update(user_id: int, updated_user: dict):
    try:
        global session
        user = session.query(User).where(User.UserId == user_id).first()
        user.UserId = int(updated_user["user_id"])
        user.DiscordId = int(updated_user["discord_id"])
        session.commit()
        return user
    except Exception as e:
        print(f"user_update failed: {e}")


def user_create(new_user: dict):
    try:
        global session
        user = User()
        # Changed to let the database pick UserId instead of it being explicit
        user.DiscordId = int(new_user["discord_id"])
        session.add(user)
        session.commit()
        return user
    except Exception as e:
        print(f"user_create failed: {e}")


def user_delete(user_id: int):
    try:
        global session
        user = session.query(User).where(User.UserId == user_id).first()
        session.delete(user)
        session.commit()
    except Exception as e:
        print(f"user_delete failed: {e}")


# Team

def get_teams():
    try:
        global session
        return session.query(Team).all()
    except Exception as e:
        print(f"get_teams failed: {e}")


def get_user_teams(user_id: int):
    try:
        global session
        return session.query(Team).where(Team.UserId == user_id).all()
    except Exception as e:
        print(f"get_user_teams failed: {e}")



def get_user_team(user_id: int, team_id: int):
    try:
        global session
        return (
            session.query(Team)
            .where(Team.UserId == user_id)
            .where(Team.TeamId == team_id)
            .first()
        )
    except Exception as e:
        print(f"get_user_team failed: {e}")


def team_update(team_id: int, updated_team: dict):
    try:
        global session
        team = session.query(Team).where(Team.TeamId == team_id).first()
        team.TeamId = int(updated_team["team_id"])
        team.TeamName = updated_team["team_name"]
        team.UserId = int(updated_team["user_id"])

        team.PokemonId1 = int(updated_team["pokemon_id1"])
        team.PokemonId2 = int(updated_team["pokemon_id2"])
        team.PokemonId3 = int(updated_team["pokemon_id3"])
        team.PokemonId4 = int(updated_team["pokemon_id4"])
        team.PokemonId5 = int(updated_team["pokemon_id5"])
        team.PokemonId6 = int(updated_team["pokemon_id6"])

        session.commit()
        return team
    except Exception as e:
        print(f"team_update failed: {e}")


def team_create(new_team: dict):
    try:
        global session
        team = Team()
        # Let DB choose TeamId
        team.TeamName = new_team["team_name"]
        team.UserId = int(new_team["user_id"])

        team.PokemonId1 = int(new_team["pokemon_id1"])
        team.PokemonId2 = int(new_team["pokemon_id2"])
        team.PokemonId3 = int(new_team["pokemon_id3"])
        team.PokemonId4 = int(new_team["pokemon_id4"])
        team.PokemonId5 = int(new_team["pokemon_id5"])
        team.PokemonId6 = int(new_team["pokemon_id6"])

        session.add(team)
        session.commit()
        return team
    except Exception as e:
        print(f"team_create failed: {e}")



def team_delete(team_id: int):
    try:
        global session
        team = session.query(Team).where(Team.TeamId == team_id).first()  # Fixed typo
        session.delete(team)
        session.commit()
    except Exception as e:
        print(f"team_delete failed: {e}")


# Pokemon

def get_all_pokemon():
    try:
        global session
        return session.query(Pokemon).all()
    except Exception as e:
        print(f"get_all_pokemon failed: {e}")


def get_pokemon(pokemon_id: int):
    try:
        global session
        return session.query(Pokemon).where(Pokemon.PokemonId == pokemon_id).first()
    except Exception as e:
        print(f"get_pokemon failed: {e}")


def get_pokemon_by_team(user_id: int, team_id: int):
    try:
        global session
        return session.query(Pokemon).where(Pokemon.UserId == user_id).where(Pokemon.TeamId == team_id)
    except Exception as e:
        print(f"get_pokemon_by_team failed: {e}")


def pokemon_update(pokemon_id: int, updated_pokemon: dict):
    try:
        global session
        pokemon = session.query(Pokemon).where(Pokemon.PokemonId == pokemon_id).first()

        pokemon.PokemonId = int(updated_pokemon["pokemon_id"])
        pokemon.Species = updated_pokemon["species"]

        pokemon.Ability = updated_pokemon["ability"]

        pokemon.Move1 = updated_pokemon["move1"]
        pokemon.Move2 = updated_pokemon["move2"]
        pokemon.Move3 = updated_pokemon["move3"]
        pokemon.Move4 = updated_pokemon["move4"]

        pokemon.TeamId = int(updated_pokemon["team_id"])
        pokemon.UserId = int(updated_pokemon["user_id"])

        session.commit()
        return pokemon
    except Exception as e:
        print(f"pokemon_update failed: {e}")


def pokemon_create(new_pokemon: dict):
    try:
        global session
        pokemon = Pokemon()

        pokemon.Species = new_pokemon["species"]

        pokemon.Ability = new_pokemon["ability"]

        pokemon.Move1 = new_pokemon["move1"]
        pokemon.Move2 = new_pokemon["move2"]
        pokemon.Move3 = new_pokemon["move3"]


        #pokemon.TeamId = int(new_pokemon["team_id"])
        #pokemon.UserId = int(new_pokemon["user_id"])
        
        session.add(pokemon)
        session.commit()
        return pokemon
    except Exception as e:
        print(f"pokemon_create failed: {e}")


def pokemon_delete(pokemon_id: int):
    try:
        global session
        pokemon = session.query(Pokemon).where(Pokemon.PokemonId == pokemon_id).first()
        session.delete(pokemon)
        session.commit()
    except Exception as e:
        print(f"pokemon_delete failed: {e}")


def database_init():
    DATABASE_URL = "sqlite:///../database/pokemon-bot.db"

    engine = create_engine(
        DATABASE_URL,
        pool_size=5,
        pool_recycle=1800,
        pool_pre_ping=True,
    )
    Base.metadata.create_all(engine)

    session_factory = sessionmaker(autoflush=False, bind=engine)

    global session
    session = session_factory()
