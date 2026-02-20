# scripts/graphs_players.py

import pandas as pd
import matplotlib.pyplot as plt
import os

print("\nLoading players_final.csv...")

# Charger le fichier CSV
df = pd.read_csv("players_final.csv")

print("File loaded successfully.")
print(f"Number of players: {len(df)}")

# Vérifier que la colonne team existe
if 'team' not in df.columns:
    print("\nERROR: Column 'team' not found.")
    print("Available columns:")
    print(df.columns)
    exit()

# Créer le dossier plots s'il n'existe pas
os.makedirs("plots", exist_ok=True)

# ==========================
# GRAPH 1: Players by Team
# ==========================

players_by_team = df['team'].value_counts()

plt.figure(figsize=(12, 6))

players_by_team.plot(
    kind='bar',
    color='skyblue',
    edgecolor='black'
)

plt.title("Number of Players by Team", fontsize=16)
plt.xlabel("Team", fontsize=12)
plt.ylabel("Number of Players", fontsize=12)

plt.xticks(rotation=45)
plt.grid(axis='y', linestyle='--', alpha=0.7)

plt.tight_layout()

# Sauvegarder le graphique
save_path = "plots/players_by_team.png"
plt.savefig(save_path)

print(f"\nGraph saved to: {save_path}")

# Afficher le graphique
plt.show()

print("\nAll graphs generated successfully.\n")