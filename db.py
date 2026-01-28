import sqlite3
from pathlib import Path

# =========================
# DATABASE CONFIG
# =========================

DB_PATH = Path(__file__).parent / "foot.db"


def get_connection():
    return sqlite3.connect(DB_PATH)


# =========================
# TABLES
# =========================

def create_tables():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS teams (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT UNIQUE NOT NULL
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS players (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        position TEXT,
        age INTEGER,
        nationality TEXT,
        club TEXT,
        rating INTEGER,
        team_id INTEGER,
        FOREIGN KEY (team_id) REFERENCES teams(id)
    )
    """)

    conn.commit()
    conn.close()


# =========================
# TEAMS
# =========================

def save_team(name: str):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "INSERT OR IGNORE INTO teams (name) VALUES (?)",
        (name,)
    )

    conn.commit()
    conn.close()


def get_team_id(name: str):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT id FROM teams WHERE name = ?",
        (name,)
    )

    row = cursor.fetchone()
    conn.close()

    return row[0] if row else None


# =========================
# PLAYERS
# =========================

def add_player(name, position, age, nationality, club, rating, team_name):
    team_id = get_team_id(team_name)

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO players (name, position, age, nationality, club, rating, team_id)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (name, position, age, nationality, club, rating, team_id))

    conn.commit()
    conn.close()


def list_players():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT players.id, players.name, position, age, nationality, club, rating, teams.name
        FROM players
        LEFT JOIN teams ON players.team_id = teams.id
    """)

    rows = cursor.fetchall()
    conn.close()

    return rows


def delete_player(player_id: int):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM players WHERE id = ?",
        (player_id,)
    )

    conn.commit()
    conn.close()


def update_player(player_id: int, **fields):
    allowed = {"name", "position", "age", "nationality", "club", "rating"}

    updates = {k: v for k, v in fields.items() if k in allowed}
    if not updates:
        return

    set_clause = ", ".join(f"{k} = ?" for k in updates.keys())
    params = list(updates.values()) + [player_id]

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        f"UPDATE players SET {set_clause} WHERE id = ?",
        params
    )

    conn.commit()
    conn.close()