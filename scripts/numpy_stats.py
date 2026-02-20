import numpy as np


def analyze_players():
    """
    Analyse les stats des joueurs avec NumPy
    """

    # Liste de joueurs (temporaire pour test)
    players = [
        {"name": "Messi", "goals": 30, "assists": 12},
        {"name": "Ronaldo", "goals": 25, "assists": 8},
        {"name": "Mbappe", "goals": 28, "assists": 10},
        {"name": "Haaland", "goals": 35, "assists": 5},
    ]

    # extraire goals et assists
    goals = np.array([player["goals"] for player in players])
    assists = np.array([player["assists"] for player in players])

    print("\n=== ANALYSE NUMPY ===")

    print("Goals:", goals)
    print("Assists:", assists)

    print("\nTotal goals:", goals.sum())
    print("Average goals:", goals.mean())
    print("Max goals:", goals.max())

    print("\nTotal assists:", assists.sum())
    print("Average assists:", assists.mean())
    print("Max assists:", assists.max())

    best_index = goals.argmax()

    print("\nBest scorer:", players[best_index]["name"])


if __name__ == "__main__":
    analyze_players()
