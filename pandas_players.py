from pathlib import Path

import pandas as pd
import matplotlib.pyplot as plt


# =========================
# PATHS
# =========================
BASE_DIR = Path.cwd()
DATA_FILE = BASE_DIR / "players_final.csv"
PLOTS_DIR = BASE_DIR / "plots"
PLOTS_DIR.mkdir(exist_ok=True)


# =========================
# LOAD
# =========================
def load_data() -> pd.DataFrame:
    if not DATA_FILE.exists():
        raise FileNotFoundError(f"Fichier introuvable: {DATA_FILE}")

    df = pd.read_csv(DATA_FILE)
    return df


# =========================
# CLEAN + NORMALIZE
# =========================
def clean_df(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    # normalise noms de colonnes
    df.columns = [str(c).strip().lower() for c in df.columns]

    # nettoie position si existe
    if "position" in df.columns:
        df["position"] = (
            df["position"]
            .astype(str)
            .str.strip()
            .str.lower()
        )

    # nettoie age si existe
    if "age" in df.columns:
        df["age"] = pd.to_numeric(df["age"], errors="coerce")

    # optionnel: supprime lignes sans age
    if "age" in df.columns:
        df = df.dropna(subset=["age"])

    return df


# =========================
# STATS
# =========================
def print_stats(df: pd.DataFrame) -> None:
    print("\n📌 INFOS DATASET")
    print(f"- Lignes: {len(df)}")
    print(f"- Colonnes: {len(df.columns)}")
    print(f"- Colonnes disponibles: {list(df.columns)}")

    if "age" in df.columns:
        print("\n📌 STATS AGE")
        print(df["age"].describe().round(2))

    if "position" in df.columns:
        print("\n📌 COUNT PAR POSTE")
        print(df["position"].value_counts())


# =========================
# BUSINESS INSIGHTS
# =========================
def average_age_by_position(df: pd.DataFrame) -> None:
    if "position" not in df.columns or "age" not in df.columns:
        print("\n⚠️ average_age_by_position: colonnes manquantes (position/age)")
        return

    print("\n📊 Moyenne d’âge par poste")
    result = df.groupby("position")["age"].mean().sort_values()
    print(result.round(1))


def top_oldest_players(df: pd.DataFrame, n: int = 5) -> None:
    if "age" not in df.columns:
        print("\n⚠️ top_oldest_players: colonne manquante (age)")
        return

    # colonnes à afficher si dispo
    cols = []
    for c in ["name", "age", "position", "club"]:
        if c in df.columns:
            cols.append(c)

    print(f"\n👴 Top {n} joueurs les plus âgés")
    if cols:
        print(df.sort_values("age", ascending=False)[cols].head(n))
    else:
        print(df.sort_values("age", ascending=False).head(n))


# =========================
# PLOTS
# =========================
def plot_age_histogram(df: pd.DataFrame) -> None:
    if "age" not in df.columns:
        print("\n⚠️ plot_age_histogram: colonne manquante (age)")
        return

    plt.figure()
    df["age"].dropna().plot(kind="hist", bins=10)
    plt.title("Age distribution")
    plt.xlabel("Age")
    plt.ylabel("Count")

    out = PLOTS_DIR / "age_histogram.png"
    plt.savefig(out)
    plt.close()
    print(f"✅ Saved: {out}")


def plot_count_by_position(df: pd.DataFrame) -> None:
    if "position" not in df.columns:
        print("\n⚠️ plot_count_by_position: colonne manquante (position)")
        return

    plt.figure()
    df["position"].value_counts().plot(kind="bar")
    plt.title("Players by position")
    plt.xlabel("Position")
    plt.ylabel("Count")

    out = PLOTS_DIR / "players_by_position.png"
    plt.tight_layout()
    plt.savefig(out)
    plt.close()
    print(f"✅ Saved: {out}")


# =========================
# MAIN
# =========================
def main() -> None:
    print(f"📁 BASE_DIR: {BASE_DIR}")
    print(f"📄 DATA_FILE: {DATA_FILE.resolve()}")
    print(f"📊 PLOTS_DIR: {PLOTS_DIR.resolve()}")

    df = load_data()
    df = clean_df(df)

    print_stats(df)

    # Ajouts "métier"
    average_age_by_position(df)
    top_oldest_players(df, n=5)

    # Plots
    plot_age_histogram(df)
    plot_count_by_position(df)

    print("\n✅ DONE — regarde le dossier : plots/")


if __name__ == "__main__":
    main()
