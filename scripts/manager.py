import json
import os

FILE_PATH = "players.json"


# =========================
# LOAD PLAYERS
# =========================
def load_players():
    if not os.path.exists(FILE_PATH):
        return []

    with open(FILE_PATH, "r") as file:
        try:
            return json.load(file)
        except json.JSONDecodeError:
            return []


# =========================
# SAVE PLAYERS
# =========================
def save_players(players):
    with open(FILE_PATH, "w") as file:
        json.dump(players, file, indent=4)

    print("Players saved successfully.")


# =========================
# LIST PLAYERS
# =========================
def list_players(players):
    if not players:
        print("\nNo players found.")
        return

    print("\n=== PLAYERS ===")

    for i, player in enumerate(players, 1):

        # SAFE ACCESS (prevents KeyError)
        name = player.get("name", "Unknown")
        goals = player.get("goals", 0)
        assists = player.get("assists", 0)

        print(f"{i}. {name} - Goals: {goals} - Assists: {assists}")


# =========================
# ADD PLAYER
# =========================
def add_player(players):

    print("\n=== ADD PLAYER ===")

    name = input("Enter player name: ")

    try:
        goals = int(input("Enter goals: "))
        assists = int(input("Enter assists: "))
    except ValueError:
        print("Invalid number.")
        return

    new_player = {
        "name": name,
        "goals": goals,
        "assists": assists
    }

    players.append(new_player)

    print(f"{name} added successfully.")
