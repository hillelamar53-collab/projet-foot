import sqlite3

DB_NAME = "foot.db"


def create_connection():
    return sqlite3.connect(DB_NAME)


def create_table():
    conn = create_connection()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS teams (
        id INTEGER PRIMARY KEY,
        name TEXT,
        country_id INTEGER
    )
    """)

    conn.commit()
    conn.close()


def insert_teams(teams):
    conn = create_connection()
    cursor = conn.cursor()

    for team in teams:
        cursor.execute("""
        INSERT OR REPLACE INTO teams (id, name, country_id)
        VALUES (?, ?, ?)
        """, (
            team.get("id"),
            team.get("name"),
            team.get("country_id")
        ))

    conn.commit()
    conn.close()


def get_all_teams():
    conn = create_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM teams")
    teams = cursor.fetchall()

    conn.close()
    return teams
