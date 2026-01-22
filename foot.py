import sqlite3

db_name = "foot.db"
conn = sqlite3.connect(db_name)
cursor = conn.cursor()
cursor.execute("""
CREATE TABLE IF NOT EXISTS equipes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nom TEXT NOT NULL,
    ville TEXT NOT NULL
)
""")
conn.commit()
# Insertion des equipes
cursor.execute(
    "INSERT INTO equipes (nom, ville) VALUES (?, ?)",
    ("PSG", "Paris")
)

cursor.execute(
    "INSERT INTO equipes (nom, ville) VALUES (?, ?)",
    ("OM", "Marseille")
)

conn.commit()
# Lecture des equipes
cursor.execute("SELECT * FROM equipes")
equipes = cursor.fetchall()

print("Liste des équipes :")
for equipe in equipes:
    print(equipe)
# Mise à jour d'une equipe
cursor.execute(
    "UPDATE equipes SET ville = ? WHERE nom = ?",
    ("Saint-Germain", "PSG")
)

conn.commit()
# Suppression d'une equipe
cursor.execute(
    "DELETE FROM equipes WHERE nom = ?",
    ("OM",)
)

conn.commit()
# Suppression d'une equipe
cursor.execute(
    "DELETE FROM equipes WHERE nom = ?",
    ("OM",)
)

conn.commit()

# Vérification finale
cursor.execute("SELECT * FROM equipes")
equipes = cursor.fetchall()

print("Liste finale des équipes :")
for equipe in equipes:
    print(equipe)

# Fermeture de la connexion
conn.close()
