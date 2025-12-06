import os
from typing import Any, Dict, List, Optional

import httpx
from dotenv import load_dotenv

load_dotenv()

API_BASE_URL = os.getenv("API_BASE_URL", "http://127.0.0.1:8000")


class ApiError(Exception):
    pass


async def _request(
    method: str,
    path: str,
    *,
    json: Optional[Dict[str, Any]] = None,
    params: Optional[Dict[str, Any]] = None,
) -> Any:
    url = API_BASE_URL.rstrip("/") + path

    async with httpx.AsyncClient(timeout=10.0) as client:
        response = await client.request(method, url, json=json, params=params)

    if response.status_code >= 400:
        try:
            detail = response.json()
        except Exception:
            detail = response.text
        raise ApiError(f"{method} {url} failed: {response.status_code} {detail}")

    if response.headers.get("content-type", "").startswith("application/json"):
        return response.json()
    return response.text


#  Users 

async def get_user_by_discord_id(discord_id: int) -> Optional[Dict[str, Any]]:
    user = await _request("GET", f"/users/discordId/{discord_id}")
    if not user:
        return None
    return user


async def create_user(discord_id: int) -> Dict[str, Any]:
    payload = {"discord_id": discord_id}
    user = await _request("POST", "/users/", json=payload)
    if not user:
        raise ApiError("API returned empty response when creating user")
    return user


async def get_or_create_user(discord_id: int) -> Dict[str, Any]:
    user = await get_user_by_discord_id(discord_id)
    if user:
        return user
    return await create_user(discord_id)


#  Teams 

async def list_teams_for_user(user_id: int) -> List[Dict[str, Any]]:
    teams = await _request("GET", f"/teams/userId/{user_id}")
    if not teams:
        return []
    return list(teams)


async def create_team_for_user(
    user_id: int,
    name: str,
    pokemon_ids: List[int],
) -> Dict[str, Any]:
    if len(pokemon_ids) != 6:
        raise ValueError("Exactly 6 Pokémon IDs are required")

    payload = {
        "team_name": name,
        "user_id": user_id,
        "pokemon_id1": pokemon_ids[0],
        "pokemon_id2": pokemon_ids[1],
        "pokemon_id3": pokemon_ids[2],
        "pokemon_id4": pokemon_ids[3],
        "pokemon_id5": pokemon_ids[4],
        "pokemon_id6": pokemon_ids[5],
    }

    team = await _request("POST", "/teams/", json=payload)
    if not team:
        raise ApiError("API returned empty response when creating team")
    return team
