import sqlite3


DB_PATH = "foot.db"


def get_conn():
    return sqlite3.connect(DB_PATH)


def init_db():
    """Crée la table si elle n'existe pas (au cas où)."""
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS players (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            age INTEGER NOT NULL,
            position TEXT NOT NULL,
            club TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()


def add_player_cli():
    name = input("Nom du joueur: ").strip()
    age_str = input("Âge: ").strip()
    position = input("Poste (ex: FW, MF, DF, GK): ").strip()
    club = input("Club: ").strip()

    if not name or not age_str or not position or not club:
        print("❌ Tous les champs sont obligatoires.")
        return

    try:
        age = int(age_str)
    except ValueError:
        print("❌ L'âge doit être un nombre.")
        return

    conn = get_conn()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO players (name, age, position, club) VALUES (?, ?, ?, ?)",
        (name, age, position, club)
    )
    conn.commit()
    conn.close()
    print("✅ Joueur ajouté.")


def add_fake_player_cli():
    # Fake player MAIS avec club rempli (sinon NOT NULL error)
    name = "John Doe"
    age = 24
    position = "FW"
    club = "Fake Club"

    conn = get_conn()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO players (name, age, position, club) VALUES (?, ?, ?, ?)",
        (name, age, position, club)
    )
    conn.commit()
    conn.close()
    print("✅ Fake joueur ajouté.")


def list_players_cli():
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT id, name, age, position, club FROM players ORDER BY id ASC")
    rows = cur.fetchall()
    conn.close()

    print("\n--- Liste des joueurs ---")
    if not rows:
        print("(vide)")
        return

    for r in rows:
        pid, name, age, pos, club = r
        print(f"{pid}. {name} | {age} ans | {pos} | {club}")
    print("------------------------\n")


def delete_player_cli():
    pid_str = input("ID du joueur à supprimer: ").strip()
    try:
        pid = int(pid_str)
    except ValueError:
        print("❌ ID invalide.")
        return

    conn = get_conn()
    cur = conn.cursor()
    cur.execute("DELETE FROM players WHERE id = ?", (pid,))
    conn.commit()
    deleted = cur.rowcount
    conn.close()

    if deleted:
        print("✅ Joueur supprimé.")
    else:
        print("❌ Aucun joueur avec cet ID.")


def update_player_cli():
    pid_str = input("ID du joueur à modifier: ").strip()
    try:
        pid = int(pid_str)
    except ValueError:
        print("❌ ID invalide.")
        return

    # On récupère l’existant
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT id, name, age, position, club FROM players WHERE id = ?", (pid,))
    row = cur.fetchone()

    if not row:
        conn.close()
        print("❌ Aucun joueur avec cet ID.")
        return

    _, old_name, old_age, old_pos, old_club = row

    print("Laisse vide pour garder la valeur actuelle.")
    name = input(f"Nom [{old_name}]: ").strip() or old_name
    age_input = input(f"Âge [{old_age}]: ").strip()
    position = input(f"Poste [{old_pos}]: ").strip() or old_pos
    club = input(f"Club [{old_club}]: ").strip() or old_club

    if age_input.strip() == "":
        age = old_age
    else:
        try:
            age = int(age_input)
        except ValueError:
            conn.close()
            print("❌ Âge invalide.")
            return

    cur.execute(
        "UPDATE players SET name = ?, age = ?, position = ?, club = ? WHERE id = ?",
        (name, age, position, club, pid)
    )
    conn.commit()
    updated = cur.rowcount
    conn.close()

    if updated:
        print("✅ Joueur modifié.")
    else:
        print("❌ Modification échouée.")


def show_menu():
    print("⚽ FOOT PLAYER MANAGER")
    print("1. Ajouter un joueur")
    print("2. Ajouter un faux joueur (faker)")
    print("3. Voir les joueurs")
    print("4. Modifier un joueur")
    print("5. Supprimer un joueur")
    print("0. Quitter")


def main():
    init_db()
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
            print("👋 Bye.")
            break
        else:
            print("❌ Choix invalide.")


if __name__ == "__main__":
    main()
