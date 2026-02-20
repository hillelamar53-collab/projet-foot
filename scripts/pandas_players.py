import sqlite3
import pandas as pd


def main():

    # connecter à la database
    conn = sqlite3.connect("foot.db")

    # charger dans pandas
    df = pd.read_sql_query("SELECT * FROM teams", conn)

    conn.close()

    # afficher infos
    print("\nDataFrame :")
    print(df.head())

    print("\nNombre d'équipes :", len(df))

    # sauvegarder en CSV
    df.to_csv("teams.csv", index=False)

    print("\nFichier teams.csv créé !")


if __name__ == "__main__":
    main()
