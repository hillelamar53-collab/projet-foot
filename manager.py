from storage import load_players, save_players
from faker import Faker

fake = Faker("fr_FR")


# =========================
# AJOUTER UN JOUEUR (MANUEL)
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
    print("✅ Joueur ajouté avec succès")


# =========================
# AJOUTER UN JOUEUR (FAKER)
# =========================
def add_fake_player():
    players = load_players()

    player = {
        "name": fake.name(),
        "position": fake.random_element(
            elements=("Attaquant", "Milieu", "Défenseur", "Gardien")
        ),
        "age": fake.random_int(min=17, max=40),
        "club": fake.company()
    }

    players.append(player)
    save_players(players)
    print("🤖 Joueur fictif ajouté avec Faker")


# =========================
# AFFICHER LES JOUEURS
# =========================
def list_players():
    players = load_players()

    if not players:
        print("⚠️ Aucun joueur enregistré")
        return

    print("\n📋 Liste des joueurs :")
    for i, p in enumerate(players, start=1):
        print(f"{i}. {p['name']} | {p['position']} | {p['age']} ans | {p['club']}")


# =========================
# SUPPRIMER UN JOUEUR
# =========================
def delete_player_cli():
    players = load_players()

    if not players:
        print("⚠️ Aucun joueur à supprimer")
        return

    list_players()

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
    print(f"🗑️ Joueur supprimé : {removed['name']}")


# =========================
# MENU PRINCIPAL
# =========================
def menu():
    while True:
        print("\n⚽ FOOT PLAYER MANAGER")
        print("1. Ajouter un joueur (manuel)")
        print("2. Ajouter un joueur (faker)")
        print("3. Voir les joueurs")
        print("4. Supprimer un joueur")
        print("0. Quitter")

        choice = input("Ton choix : ")

        if choice == "1":
            add_player_cli()
        elif choice == "2":
            add_fake_player()
        elif choice == "3":
            list_players()
        elif choice == "4":
            delete_player_cli()
        elif choice == "0":
            print("👋 Bye")
            break
        else:
            print("❌ Choix invalide")