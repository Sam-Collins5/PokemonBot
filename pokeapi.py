import requests

BASE_URL = "https://pokeapi.co/api/v2/"

def get_pokemon(name_or_id):
    url = BASE_URL + f"pokemon/{name_or_id}"
    response = requests.get(url)

    if response.status_code != 200:
        return None

    data = response.json()
    return {
        "name": data["name"],
        "species": data["species"]["name"],
        "ability": data["abilities"][0]["ability"]["name"],
        "move1": data["moves"][0]["move"]["name"],
        "move2": data["moves"][1]["move"]["name"],
        "move3": data["moves"][2]["move"]["name"]
        }

#[a["ability"]["name"] for a in data["abilities"]]

def get_move(name_or_id):
    url = BASE_URL + f"move/{name_or_id}"
    response = requests.get(url)

    if response.status_code != 200:
        return None

    data = response.json()
    return {
        "name": data["name"],
        "power": data["power"],
        "accuracy": data["accuracy"],
        "type": data["type"]["name"],
        "category": data["damage_class"]["name"],
        "description": data["effect_entries"][0]["short_effect"]
    }

def get_ability(name_or_id):
    url = BASE_URL + f"ability/{name_or_id}"
    response = requests.get(url)

    if response.status_code != 200:
        return None

    data = response.json()
    return {
        "name": data["name"],
        "effect": data["effect_entries"][0]["short_effect"]
    }
def get_item(name_or_id):
    url = BASE_URL + f"item/{name_or_id}"
    response = requests.get(url)

    if response.status_code != 200:
        return None

    data = response.json()
    return {
        "name": data["name"],
        "category": data["category"]["name"],
        "effect": data["effect_entries"][0]["short_effect"]

    }

def get_berry(name_or_id):
    url = BASE_URL + f"berry/{name_or_id}"
    response = requests.get(url)

    if response.status_code != 200:
        return None

    data = response.json()
    return {
        "name": data["name"],
        "firmness": data["firmness"]["name"],
        "growth_time": data["growth_time"],
        "flavors": {f["flavor"]["name"]: f["potency"] for f in data["flavors"]}
    }



poke = get_pokemon("Gengar")

print(poke["move1"])