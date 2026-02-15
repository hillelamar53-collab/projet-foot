import os
import requests
from dotenv import load_dotenv

load_dotenv()

API_TOKEN = os.getenv("SPORTMONKS_API_TOKEN")
BASE_URL = os.getenv("SPORTMONKS_BASE_URL")

if not API_TOKEN or not BASE_URL:
    raise RuntimeError("❌ Variables d’environnement manquantes")

def get_countries():
    url = f"{BASE_URL}/countries"
    params = {"api_token": API_TOKEN}

    r = requests.get(url, params=params)
    print("STATUS:", r.status_code)

    if r.status_code != 200:
        print(r.text)
        return None

    return r.json()
