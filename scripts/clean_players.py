
import pandas as pd


def main():
    print("Lecture du fichier players_final.csv...")

    # 1️⃣ Lire le fichier CSV
    df = pd.read_csv("players_final.csv")

    # 2️⃣ Afficher nombre total de lignes
    print("\nNombre total de lignes :", len(df))

    # 3️⃣ Nettoyer les données

    # enlever les lignes sans nom
    df = df.dropna(subset=["name"])

    # convertir age en nombre (au cas où)
    df["age"] = pd.to_numeric(df["age"], errors="coerce")

    # enlever les lignes sans age valide
    df = df.dropna(subset=["age"])

    # garder uniquement les joueurs football
    df_clean = df[df["role_type"] == "football"]

    # 4️⃣ Statistiques
    print("\nNombre de joueurs de football :", len(df_clean))

    age_moyen = df_clean["age"].mean()
    print("\nAge moyen :", age_moyen)

    # 5️⃣ Sauvegarder fichier propre
    df_clean.to_csv("players_clean.csv", index=False)

    print("\nplayers_clean.csv créé avec succès")

    # 6️⃣ Afficher le résultat clean
    print("\nAperçu des joueurs clean :")
    print(df_clean.head())


# lancer le script
if __name__ == "__main__":
    main()