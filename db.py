import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent / "foot.db"


def get_conn():
    return sqlite3.connect(DB_PATH)


def init_db():
    conn = get_conn()
    cur = conn.cursor()
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS players (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            age INTEGER NOT NULL,
            position TEXT NOT NULL,
            club TEXT NOT NULL
        )
        """
    )
    conn.commit()
    conn.close()


def add_player(name: str, age: int, position: str, club: str):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO players (name, age, position, club) VALUES (?, ?, ?, ?)",
        (name, age, position, club),
    )
    conn.commit()
    conn.close()


def list_players():
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT id, name, age, position, club FROM players ORDER BY id ASC")
    rows = cur.fetchall()
    conn.close()
    return rows


def delete_player(player_id: int):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("DELETE FROM players WHERE id = ?", (player_id,))
    conn.commit()
    conn.close()


def update_player(player_id: int, name=None, age=None, position=None, club=None):
    # Build dynamic update based on provided fields
    fields = []
    values = []

    if name is not None:
        fields.append("name = ?")
        values.append(name)
    if age is not None:
        fields.append("age = ?")
        values.append(age)
    if position is not None:
        fields.append("position = ?")
        values.append(position)
    if club is not None:
        fields.append("club = ?")
        values.append(club)

    if not fields:
        return  # nothing to update

    values.append(player_id)

    conn = get_conn()
    cur = conn.cursor()
    cur.execute(f"UPDATE players SET {', '.join(fields)} WHERE id = ?", values)
    conn.commit()
    conn.close()
