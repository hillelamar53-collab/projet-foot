import json
import os

FILE_PATH = "players.json"


def load_players():
    if not os.path.exists(FILE_PATH):
        return []

    with open(FILE_PATH, "r") as f:
        return json.load(f)


def save_players(players):
    with open(FILE_PATH, "w") as f:
        json.dump(players, f, indent=4)