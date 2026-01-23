import sqlite3

DB_NAME = "foot.db"


def get_connection():
    return sqlite3.connect(DB_NAME)


def create_tables():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS teams (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE
        )
    """)

    conn.commit()
    conn.close()


def save_team(name):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        "INSERT OR IGNORE INTO teams (name) VALUES (?)",
        (name,)
    )

    conn.commit()
    conn.close()
