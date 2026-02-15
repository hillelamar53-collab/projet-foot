"""
pandas_players.py
-----------------
Objectif:
- Se connecter à une API de football (SportMonks v3) avec un token stocké dans .env
- Récupérer des données (équipes / joueurs / stats)
- Construire un DataFrame Pandas
- Export CSV + graphiques

Prérequis:
pip install requests python-dotenv pandas matplotlib

.env (à la racine du projet):
SPORTMONKS_API_TOKEN=ton_token_ici
SPORTMONKS_BASE_URL=https://api.sportmonks.com/v3/football

⚠️ Remarque importante:
Les APIs ont parfois des endpoints / noms de champs qui varient selon l’abonnement.
Ce script est robuste: il gère la pagination et te montre quoi ajuster si besoin.
"""

from __future__ import annotations

import os
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, Generator, List, Optional, Tuple

import requests
import pandas as pd
import matplotlib.pyplot as plt
from dotenv import load_dotenv


# ----------------------------
# CONFIG / PATHS
# ----------------------------
BASE_DIR = Path.cwd()
DATA_FILE = BASE_DIR / "players_api.csv"
PLOTS_DIR = BASE_DIR / "plots_api"
PLOTS_DIR.mkdir(exist_ok=True)

load_dotenv()  # charge .env

API_TOKEN = os.getenv("SPORTMONKS_API_TOKEN", "").strip()
BASE_URL = os.getenv("SPORTMONKS_BASE_URL", "https://api.sportmonks.com/v3/football").strip()

if not API_TOKEN:
    raise RuntimeError(
        "SPORTMONKS_API_TOKEN est manquant. Ajoute-le dans un fichier .env à la racine:\n"
        "SPORTMONKS_API_TOKEN=ton_token_ici\n"
        "SPORTMONKS_BASE_URL=https://api.sportmonks.com/v3/football"
    )


# ----------------------------
# API CLIENT
# ----------------------------
@dataclass
class SportMonksClient:
    token: str
    base_url: str = "https://api.sportmonks.com/v3/football"
    timeout: int = 30
    max_retries: int = 3
    sleep_between_requests: float = 0.25  # petit throttle (évite de se faire limiter)

    def _request(self, path: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Fait un GET et renvoie le JSON.
        SportMonks accepte souvent api_token en query param.
        """
        if params is None:
            params = {}

        # Auth via query param (le plus commun chez SportMonks)
        params["api_token"] = self.token

        url = self.base_url.rstrip("/") + "/" + path.lstrip("/")

        last_err: Optional[Exception] = None
        for attempt in range(1, self.max_retries + 1):
            try:
                time.sleep(self.sleep_between_requests)
                r = requests.get(url, params=params, timeout=self.timeout)
                if r.status_code >= 400:
                    # Essaie d’afficher une erreur exploitable
                    try:
                        payload = r.json()
                    except Exception:
                        payload = {"raw": r.text[:500]}
                    raise RuntimeError(f"HTTP {r.status_code} sur {url} | {payload}")

                return r.json()

            except Exception as e:
                last_err = e
                if attempt < self.max_retries:
                    time.sleep(0.7 * attempt)
                else:
                    raise

        # ne devrait pas arriver
        raise RuntimeError(f"Erreur inconnue API: {last_err}")

    def iter_paginated(
        self, path: str, params: Optional[Dict[str, Any]] = None
    ) -> Generator[Dict[str, Any], None, None]:
        """
        Itère sur toutes les pages.
        Structure de pagination la plus fréquente:
        {
          "data": [...],
          "pagination": { "has_more": true, "current_page": 1, "next_page": 2, ... }
        }
        """
        if params is None:
            params = {}

        page = int(params.get("page", 1))
        while True:
            params["page"] = page
            payload = self._request(path, params=params)

            data = payload.get("data", [])
            if isinstance(data, list):
                for item in data:
                    yield item
            else:
                # parfois data n’est pas une liste
                yield data

            pagination = payload.get("pagination") or {}
            has_more = pagination.get("has_more")
            next_page = pagination.get("next_page")

            # Fallback si pagination absente: on stop après la première page
            if has_more is True and next_page:
                page = int(next_page)
                continue
            break


# ----------------------------
# HELPERS: extraction "safe"
# ----------------------------
def pick(d: Dict[str, Any], *keys: str, default=None):
    """Récupère le premier champ existant parmi keys."""
    for k in keys:
        if k in d and d[k] is not None:
            return d[k]
    return default


def normalize_position(player: Dict[str, Any]) -> str:
    """
    Essaie de trouver une position.
    Selon endpoints, ça peut être:
    - player['position']['name']
    - player['position_name']
    - player['detailed_position']['name']
    """
    pos = ""
    if isinstance(player.get("position"), dict):
        pos = player["position"].get("name", "") or ""
    if not pos:
        pos = pick(player, "position_name", "position", "role", default="") or ""
        if isinstance(pos, dict):
            pos = pos.get("name", "")
    if not pos and isinstance(player.get("detailed_position"), dict):
        pos = player["detailed_position"].get("name", "")
    return str(pos or "").strip() or "Unknown"


def safe_name(entity: Dict[str, Any]) -> str:
    return str(pick(entity, "name", "display_name", "fullname", "common_name", default="Unknown")).strip()


# ----------------------------
# DATA FETCH (à adapter si besoin)
# ----------------------------
def fetch_teams_for_league_season(
    api: SportMonksClient, league_id: int, season_id: int
) -> List[Dict[str, Any]]:
    """
    Beaucoup de comptes SportMonks supportent un endpoint de type:
    GET /teams  (avec filtres league_id/season_id)
    Si ton endpoint diffère, tu changes juste path + params ici.
    """
    teams = list(
        api.iter_paginated(
            "/teams",
            params={
                "league_id": league_id,
                "season_id": season_id,
                # include utile si disponible (sinon ignoré)
                "include": "country",
                "per_page": 50,
            },
        )
    )
    return teams


def fetch_players_for_team_season(
    api: SportMonksClient, team_id: int, season_id: int
) -> List[Dict[str, Any]]:
    """
    Cas fréquent:
    - endpoint squad/roster: /squads/teams/{team_id}?season_id=...
    - OU /teams/{team_id}?include=players
    - OU /players?team_id=...&season_id=...

    Comme les plans varient, on commence avec un endpoint simple /players filtré.
    Si ça ne marche pas chez toi -> dis-moi l’erreur exacte et on ajuste en 30s.
    """
    players = list(
        api.iter_paginated(
            "/players",
            params={
                "team_id": team_id,
                "season_id": season_id,
                "include": "position,team",
                "per_page": 50,
            },
        )
    )
    return players


def fetch_player_season_stats(
    api: SportMonksClient, player_id: int, season_id: int
) -> Dict[str, Any]:
    """
    Cas fréquent:
    GET /players/{id}?include=statistics
    ou GET /players/{id}?include=statistics;filters=season_id:xxx

    On tente une forme "players/{id}" + include.
    Si ton compte renvoie une autre structure, on ajustera les champs.
    """
    payload = api._request(
        f"/players/{player_id}",
        params={
            "include": "statistics",
            # certains systèmes utilisent filters. si ignoré, pas grave
            "filters": f"season_id:{season_id}",
        },
    )
    data = payload.get("data") or {}
    return data


def extract_basic_stats(player_payload: Dict[str, Any]) -> Dict[str, Any]:
    """
    Essaie d’extraire minutes/goals/assists depuis différentes structures.
    On renvoie 0 si introuvable.
    """
    minutes = 0
    goals = 0
    assists = 0
    appearances = 0

    # 1) Si statistics est une liste d’objets
    stats = player_payload.get("statistics")
    if isinstance(stats, list) and stats:
        # On prend le premier (souvent déjà filtré par season)
        s0 = stats[0] if isinstance(stats[0], dict) else {}
        minutes = int(pick(s0, "minutes", "minutes_played", default=0) or 0)
        goals = int(pick(s0, "goals", "goals_scored", default=0) or 0)
        assists = int(pick(s0, "assists", default=0) or 0)
        appearances = int(pick(s0, "appearances", "matches_played", default=0) or 0)

    # 2) Si statistics est une dict (parfois)
    elif isinstance(stats, dict):
        minutes = int(pick(stats, "minutes", "minutes_played", default=0) or 0)
        goals = int(pick(stats, "goals", "goals_scored", default=0) or 0)
        assists = int(pick(stats, "assists", default=0) or 0)
        appearances = int(pick(stats, "appearances", "matches_played", default=0) or 0)

    # 3) Parfois stats est dans "data['statistics']['data']"
    else:
        st = player_payload.get("statistics", {})
        if isinstance(st, dict) and isinstance(st.get("data"), list) and st["data"]:
            s0 = st["data"][0]
            minutes = int(pick(s0, "minutes", "minutes_played", default=0) or 0)
            goals = int(pick(s0, "goals", "goals_scored", default=0) or 0)
            assists = int(pick(s0, "assists", default=0) or 0)
            appearances = int(pick(s0, "appearances", "matches_played", default=0) or 0)

    return {
        "appearances": appearances,
        "minutes": minutes,
        "goals": goals,
        "assists": assists,
    }


# ----------------------------
# PIPELINE
# ----------------------------
def build_players_dataframe(
    api: SportMonksClient,
    league_id: int,
    season_id: int,
    limit_teams: Optional[int] = None,
    limit_players_per_team: Optional[int] = None,
    with_stats: bool = True,
) -> pd.DataFrame:
    teams = fetch_teams_for_league_season(api, league_id=league_id, season_id=season_id)
    if limit_teams:
        teams = teams[:limit_teams]

    rows: List[Dict[str, Any]] = []

    for t in teams:
        team_id = int(pick(t, "id", default=0) or 0)
        team_name = safe_name(t)

        if not team_id:
            continue

        players = fetch_players_for_team_season(api, team_id=team_id, season_id=season_id)
        if limit_players_per_team:
            players = players[:limit_players_per_team]

        for p in players:
            player_id = int(pick(p, "id", default=0) or 0)
            player_name = safe_name(p)
            position = normalize_position(p)

            stats_dict = {"appearances": 0, "minutes": 0, "goals": 0, "assists": 0}
            if with_stats and player_id:
                try:
                    full_player = fetch_player_season_stats(api, player_id=player_id, season_id=season_id)
                    stats_dict = extract_basic_stats(full_player)
                except Exception:
                    # Si le plan ne donne pas accès à stats, on garde 0
                    stats_dict = {"appearances": 0, "minutes": 0, "goals": 0, "assists": 0}

            rows.append(
                {
                    "league_id": league_id,
                    "season_id": season_id,
                    "team_id": team_id,
                    "team_name": team_name,
                    "player_id": player_id,
                    "player_name": player_name,
                    "position": position,
                    **stats_dict,
                }
            )

    df = pd.DataFrame(rows)
    if not df.empty:
        df = df.sort_values(["team_name", "position", "minutes"], ascending=[True, True, False]).reset_index(drop=True)
    return df


# ----------------------------
# EXPORT + PLOTS
# ----------------------------
def save_csv(df: pd.DataFrame, out_path: Path) -> None:
    df.to_csv(out_path, index=False)
    print(f"✅ CSV sauvegardé: {out_path}")


def plot_top_scorers(df: pd.DataFrame, out_path: Path, top_n: int = 15) -> None:
    if df.empty:
        print("⚠️ DataFrame vide, pas de plot.")
        return

    # Top buteurs
    top = df.sort_values("goals", ascending=False).head(top_n)
    plt.figure()
    plt.bar(top["player_name"], top["goals"])
    plt.xticks(rotation=60, ha="right")
    plt.title(f"Top {top_n} buteurs")
    plt.tight_layout()
    plt.savefig(out_path)
    plt.close()
    print(f"✅ Plot sauvegardé: {out_path}")


def plot_minutes_by_position(df: pd.DataFrame, out_path: Path) -> None:
    if df.empty:
        print("⚠️ DataFrame vide, pas de plot.")
        return

    g = df.groupby("position", as_index=False)["minutes"].sum().sort_values("minutes", ascending=False)
    plt.figure()
    plt.bar(g["position"], g["minutes"])
    plt.xticks(rotation=30, ha="right")
    plt.title("Minutes jouées par poste (somme)")
    plt.tight_layout()
    plt.savefig(out_path)
    plt.close()
    print(f"✅ Plot sauvegardé: {out_path}")


# ----------------------------
# MAIN
# ----------------------------
def main() -> None:
    """
    Exemple:
    python pandas_players.py

    Paramètres à ajuster:
    - league_id, season_id (tu les récupères via l’API /leagues ou /seasons)
    """
    api = SportMonksClient(token=API_TOKEN, base_url=BASE_URL)

    # ✅ Mets ici tes IDs
    # (si tu ne les connais pas encore -> on les récupère juste après avec un mini script)
    league_id = 8      # EX: Premier League (exemple)
    season_id = 21646  # EX: saison (exemple)

    # Pour tester vite sans exploser le quota:
    df = build_players_dataframe(
        api,
        league_id=league_id,
        season_id=season_id,
        limit_teams=3,              # enlève ou mets None quand ça marche
        limit_players_per_team=10,  # enlève ou mets None quand ça marche
        with_stats=True,
    )

    print(df.head(20))
    print(f"\nRows: {len(df)}")

    save_csv(df, DATA_FILE)
    plot_top_scorers(df, PLOTS_DIR / "top_scorers.png", top_n=15)
    plot_minutes_by_position(df, PLOTS_DIR / "minutes_by_position.png")


if __name__ == "__main__":
    main()
