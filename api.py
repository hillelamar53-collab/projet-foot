import os
import requests
from dotenv import load_dotenv

# importer les fonctions database
from db import create_table, insert_teams

# charger le fichier .env
load_dotenv()

# récupérer le token
API_TOKEN = os.getenv("SPORTMONKS_API_TOKEN")

# URL de base
BASE_URL = "https://api.sportmonks.com/v3/football"

print("API TOKEN loaded:", API_TOKEN is not None)


def get_teams():
    url = f"{BASE_URL}/teams?api_token={API_TOKEN}"

    response = requests.get(url)

    print("Status code:", response.status_code)

    if response.status_code != 200:
        print(response.text)
        return []

    data = response.json()

    teams = data.get("data", [])

    return teams


def main():

    # créer la table si elle n'existe pas
    create_table()

    # récupérer les équipes depuis l'API
    teams = get_teams()

    if not teams:
        print("Aucune équipe récupérée")
        return

    # insérer dans la database
    insert_teams(teams)

    print(f"Equipes sauvegardées dans foot.db : {len(teams)}")

    print("Première équipe :", teams[0]["name"])


if __name__ == "__main__":
    main()
