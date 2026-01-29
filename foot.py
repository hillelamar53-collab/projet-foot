from manager import (
    add_player_cli,
    add_fake_player_cli,
    list_players_cli,
    delete_player_cli,
    update_player_cli,
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
    while True:
        show_menu()
        choice = input("Ton choix : ").strip()

        if choice == "1":
            add_player_cli()
        elif choice == "2":
            add_fake_player_cli()
        elif choice == "3":
            list_players_cli()
        elif choice == "4":
            update_player_cli()
        elif choice == "5":
            delete_player_cli()
        elif choice == "0":
            print("👋 Bye")
            break
        else:
            print("❌ Choix invalide")

if __name__ == "__main__":
    main()