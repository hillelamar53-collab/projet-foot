from storage import load_players, save_players


# =========================
# AJOUTER UN JOUEUR
# =========================
def add_player_cli():
    name = input("Nom du joueur : ")
    position = input("Poste : ")
    age = int(input("Âge : "))
    club = input("Club : ")

    players = load_players()

    player = {
        "name": name,
        "position": position,
        "age": age,
        "club": club
    }

    players.append(player)
    save_players(players)

    print("✅ Joueur ajouté")


# =========================
# LISTER LES JOUEURS
# =========================
def list_players():
    players = load_players()

    if not players:
        print("📭 Aucun joueur enregistré")
        return

    print("\n📋 Liste des joueurs")
    for p in players:
        print(f"- {p['name']} | {p['position']} | {p['age']} ans | {p['club']}")


# =========================
# SUPPRIMER UN JOUEUR
# =========================
def delete_player_cli():
    players = load_players()

    if not players:
        print("⚠️ Aucun joueur à supprimer")
        return

    print("\n📋 Joueurs :")
    for i, p in enumerate(players, start=1):
        print(f"{i}. {p['name']} | {p['position']} | {p['age']} ans | {p['club']}")

    try:
        choice = int(input("Numéro du joueur à supprimer : "))
        if choice < 1 or choice > len(players):
            print("❌ Choix invalide")
            return
    except ValueError:
        print("❌ Entrée invalide")
        return

    removed = players.pop(choice - 1)
    save_players(players)

    print(f"✅ Joueur supprimé : {removed['name']}")


# =========================
# MODIFIER UN JOUEUR
# =========================
def update_player_cli():
    players = load_players()

    if not players:
        print("⚠️ Aucun joueur à modifier")
        return

    print("\n📋 Joueurs :")
    for i, p in enumerate(players, start=1):
        print(f"{i}. {p['name']} | {p['position']} | {p['age']} ans | {p['club']}")

    try:
        choice = int(input("Numéro du joueur à modifier : "))
        if choice < 1 or choice > len(players):
            print("❌ Choix invalide")
            return
    except ValueError:
        print("❌ Entrée invalide")
        return

    player = players[choice - 1]

    print("\n✏️ Laisser vide pour conserver la valeur actuelle")
    name = input(f"Nom ({player['name']}) : ") or player["name"]
    position = input(f"Poste ({player['position']}) : ") or player["position"]

    age_input = input(f"Âge ({player['age']}) : ")
    age = int(age_input) if age_input else player["age"]

    club = input(f"Club ({player['club']}) : ") or player["club"]

    player.update({
        "name": name,
        "position": position,
        "age": age,
        "club": club
    })

    save_players(players)
    print("✅ Joueur modifié avec succès")