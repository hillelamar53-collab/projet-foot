from faker import Faker
import json
import os

fake = Faker()
PLAYERS_FILE = "players.json"

# ---------- STORAGE ----------

def load_players():
    if not os.path.exists(PLAYERS_FILE):
        return []
    with open(PLAYERS_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_players(players):
    with open(PLAYERS_FILE, "w", encoding="utf-8") as f:
        json.dump(players, f, indent=4, ensure_ascii=False)

# ---------- HELPERS ----------

def list_players_cli():
    players = load_players()
    if not players:
        print("⚠️ Aucun joueur enregistré")
        return
    for i, p in enumerate(players, start=1):
        print(f"{i}. {p['name']} - {p['position']} - {p['age']} ans")

# ---------- CRUD ----------

def add_player_cli():
    name = input("Nom : ")
    position = input("Poste : ")
    age = input("Âge : ")

    players = load_players()
    players.append({
        "name": name,
        "position": position,
        "age": age
    })
    save_players(players)
    print("✅ Joueur ajouté")

def add_fake_player_cli():
    players = load_players()
    players.append({
        "name": fake.name(),
        "position": fake.job(),
        "age": fake.random_int(min=18, max=40)
    })
    save_players(players)
    print("🤖 Faux joueur ajouté")

def delete_player_cli():
    players = load_players()
    if not players:
        print("⚠️ Aucun joueur à supprimer")
        return

    list_players_cli()
    try:
        index = int(input("Numéro du joueur à supprimer : "))
        removed = players.pop(index - 1)
        save_players(players)
        print(f"🗑 Joueur supprimé : {removed['name']}")
    except (ValueError, IndexError):
        print("❌ Choix invalide")

def update_player_cli():
    players = load_players()
    if not players:
        print("⚠️ Aucun joueur à modifier")
        return

    list_players_cli()
    try:
        index = int(input("Numéro du joueur à modifier : "))
        player = players[index - 1]

        player["name"] = input(f"Nom ({player['name']}) : ") or player["name"]
        player["position"] = input(f"Poste ({player['position']}) : ") or player["position"]
        player["age"] = input(f"Âge ({player['age']}) : ") or player["age"]

        save_players(players)
        print("✏️ Joueur modifié")
    except (ValueError, IndexError):
        print("❌ Choix invalide")