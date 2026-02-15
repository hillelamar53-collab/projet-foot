import sqlite3
import numpy as np

# connexion à la database
conn = sqlite3.connect("../foot.db")
cursor = conn.cursor()

# récupérer les joueurs
cursor.execute("SELECT id FROM players")
rows = cursor.fetchall()

# convertir en array numpy
ids = np.array([row[0] for row in rows])

print("Nombre de joueurs :", len(ids))
print("Moyenne ID :", np.mean(ids))
print("Max ID :", np.max(ids))
print("Min ID :", np.min(ids))

conn.close()
