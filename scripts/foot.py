# scripts/foot.py

from manager import (
    add_player_cli,
    add_fake_player_cli,
    list_players_cli,
    update_player_cli,
    delete_player_cli,
)

def show_menu():
    print("\n⚽ FOOT PLAYER MANAGER")
    print("1. Ajouter un joueur")
    print("2. Ajouter un faux joueur (faker)")
    print("3. Voir les joueurs")
    print("4. Modifier un joueur")
    print("5. Supprimer un joueur")
    print("0. Quitter")

def main():
    actions = {
        "1": add_player_cli,
        "2": add_fake_player_cli,
        "3": list_players_cli,
        "4": update_player_cli,
        "5": delete_player_cli,
    }

    while True:
        show_menu()
        choice = input("Ton choix : ").strip()  # <-- IMPORTANT: string

        if choice == "0":
            print("👋 Bye.")
            break

        action = actions.get(choice)
        if action:
            action()
        else:
            print("❌ Choix invalide.")

if __name__ == "__main__":
    main()
