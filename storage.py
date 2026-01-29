import json
import os
import uuid

FILE_PATH = "players.json"


# =========================
# CHARGER LES JOUEURS
# =========================
def load_players():
    if not os.path.exists(FILE_PATH):
        return []

    with open(FILE_PATH, "r") as f:
        return json.load(f)


# =========================
# SAUVEGARDER LES JOUEURS
# =========================
def save_players(players):
    with open(FILE_PATH, "w") as f:
        json.dump(players, f, indent=4)


# =========================
# AJOUTER UN JOUEUR
# =========================
def add_player(player: dict):
    players = load_players()

    # sécurité : id auto si pas fourni
    if "id" not in player:
        player["id"] = str(uuid.uuid4())

    players.append(player)
    save_players(players)
    return player


# =========================
# MODIFIER UN JOUEUR
# =========================
def update_player(player_id: str, updates: dict):
    players = load_players()

    for p in players:
        if str(p.get("id")) == str(player_id):
            p.update(updates)
            save_players(players)
            return p

    raise ValueError("Player not found")


# =========================
# SUPPRIMER UN JOUEUR
# =========================
def delete_player(player_id: str):
    players = load_players()

    new_players = [p for p in players if str(p.get("id")) != str(player_id)]

    if len(new_players) == len(players):
        raise ValueError("Player not found")

    save_players(new_players)
    return True