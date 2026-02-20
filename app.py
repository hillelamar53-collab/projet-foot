import sqlite3


def get_all_teams():

    conn = sqlite3.connect("foot.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM teams")

    teams = cursor.fetchall()

    conn.close()

    return teams


def main():

    teams = get_all_teams()

    print(f"Nombre d'équipes dans la database : {len(teams)}")

    print("Première équipe :")
    print(teams[0])


if __name__ == "__main__":
    main()
