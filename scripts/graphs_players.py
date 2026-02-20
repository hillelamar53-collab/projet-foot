# scripts/graphs_players.py

import pandas as pd
import matplotlib.pyplot as plt
import os


# ============================================
# 1. Charger les données
# ============================================

df = pd.read_csv("players_clean.csv")

print("Data loaded:")
print(df.head())


# ============================================
# 2. Créer le dossier plots si nécessaire
# ============================================

if not os.path.exists("plots"):
    os.makedirs("plots")


# ============================================
# 3. GRAPH 1 — Players per team
# ============================================

team_counts = df["team"].value_counts().head(10)

print("\nPlayers per team:")
print(team_counts)

plt.figure(figsize=(10,6))

team_counts.plot(kind="bar")

plt.title("Top 10 Teams by Number of Players")
plt.xlabel("Team")
plt.ylabel("Number of Players")

plt.xticks(rotation=45)

plt.tight_layout()

plt.savefig("plots/players_by_team.png")

plt.show()


# ============================================
# 4. GRAPH 2 — Players per age
# ============================================

age_counts = df["age"].value_counts().sort_index()

print("\nPlayers per age:")
print(age_counts)

plt.figure(figsize=(10,6))

age_counts.plot(kind="bar")

plt.title("Number of Players per Age")
plt.xlabel("Age")
plt.ylabel("Number of Players")

plt.tight_layout()

plt.savefig("plots/age_histogram.png")

plt.show()


# ============================================
# 5. GRAPH 3 — Players per position (if exists)
# ============================================

if "position" in df.columns:

    position_counts = df["position"].value_counts().head(10)

    print("\nPlayers per position:")
    print(position_counts)

    plt.figure(figsize=(10,6))

    position_counts.plot(kind="bar")

    plt.title("Top 10 Positions")
    plt.xlabel("Position")
    plt.ylabel("Number of Players")

    plt.xticks(rotation=45)

    plt.tight_layout()

    plt.savefig("plots/players_by_position.png")

    plt.show()


print("\nAll graphs generated and saved in /plots")