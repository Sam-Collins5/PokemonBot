import sqlalchemy
from sqlalchemy import Column, ForeignKey, String, Integer, Boolean, create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from pydantic import BaseModel

Base = declarative_base()

class User(Base):
    __tablename__ = "Users"

    UserId = Column(Integer, primary_key=True, autoincrement=True)
    DiscordId = Column(Integer)

    def json(self):
        json = dict()
        json["user_id"] = self.UserId
        json["discord_id"] = self.DiscordId
        return json  # Made it return json

class Team(Base):
    __tablename__ = "Team"

    TeamId = Column(Integer, primary_key=True, autoincrement=True)
    TeamName = Column(String)
    UserId = Column(Integer, ForeignKey(User.UserId))

    PokemonId1 = Column(Integer, ForeignKey("Pokemon.PokemonId"))
    PokemonId2 = Column(Integer, ForeignKey("Pokemon.PokemonId"))
    PokemonId3 = Column(Integer, ForeignKey("Pokemon.PokemonId"))
    PokemonId4 = Column(Integer, ForeignKey("Pokemon.PokemonId"))
    PokemonId5 = Column(Integer, ForeignKey("Pokemon.PokemonId"))
    PokemonId6 = Column(Integer, ForeignKey("Pokemon.PokemonId"))

    def json(self):
        json = dict()
        json["team_id"] = self.TeamId
        json["team_name"] = self.TeamName
        json["user_id"] = self.UserId
        json["pokemon_id1"] = self.PokemonId1
        json["pokemon_id2"] = self.PokemonId2
        json["pokemon_id3"] = self.PokemonId3
        json["pokemon_id4"] = self.PokemonId4
        json["pokemon_id5"] = self.PokemonId5
        json["pokemon_id6"] = self.PokemonId6
        return json  # Made it return json


class Pokemon(Base):
    __tablename__ = "Pokemon"

    PokemonId = Column(Integer, primary_key=True, autoincrement=True)

    Species = Column(String)

    Ability = Column(String)

    Move1 = Column(String)
    Move2 = Column(String)
    Move3 = Column(String)
    Move4 = Column(String)

    TeamId = Column(Integer, ForeignKey(Team.TeamId))
    UserId = Column(Integer, ForeignKey(User.UserId))

    def json(self):
        json = dict()
        json["pokemon_id"] = self.PokemonId
        json["species"] = self.Species
        json["ability"] = self.Ability
        json["move1"] = self.Move1
        json["move2"] = self.Move2 # Fixed a typo
        json["move3"] = self.Move3
        json["move4"] = self.Move4
        json["team_id"] = self.TeamId
        json["user_id"] = self.UserId
        return json
