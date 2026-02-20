import sys
import os
import numpy as np

# Permet d'importer api.py (qui est à la racine du projet)
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, ROOT_DIR)

from api import get_players


def analyze_players(players):
    ratings = np.array([p["rating"] for p in players], dtype=float)

    mean_ = np.mean(ratings)
    median_ = np.median(ratings)
    std_ = np.std(ratings)
    p25 = np.percentile(ratings, 25)
    p75 = np.percentile(ratings, 75)

    print(f"Mean rating: {mean_:.2f}")
    print(f"Median rating: {median_:.2f}")
    print(f"Standard deviation: {std_:.2f}")
    print(f"25th percentile: {p25:.2f}")
    print(f"75th percentile: {p75:.2f}")

    # Ex: joueurs “elite” = rating >= 90 (cours: array comparisons + boolean mask)
    elite_mask = ratings >= 90
    elite_ratings = ratings[elite_mask]
    print(f"\nElite player ratings: {elite_ratings.astype(int)}")
    print(f"Number of elite players: {elite_ratings.size}")

    # Ex: label via np.where (cours)
    labels = np.where(ratings >= 90, "Elite", "Regular")
    print(f"\nLabels: {labels}")


def main():
    players = get_players()
    analyze_players(players)


if __name__ == "__main__":
    main()
