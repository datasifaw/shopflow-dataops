
from pathlib import Path

import pandas as pd
import pyodbc


# Configuration
ROOT = Path(__file__).resolve().parent.parent
CSV_PATH = ROOT / "data" / "raw" / "olist_customers_dataset.csv"

EXPECTED_COLUMNS = [
    "customer_id",
    "customer_unique_id",
    "customer_zip_code_prefix",
    "customer_city",
    "customer_state",
]

BATCH_SIZE = 1000


def main():
    # 1. Extraction
    df = pd.read_csv(
        CSV_PATH,
        dtype={
            "customer_id": "string",
            "customer_unique_id": "string",
            "customer_zip_code_prefix": "string",
            "customer_city": "string",
            "customer_state": "string",
        },
    )

    print(f"Lignes lues : {len(df)}")

    # 2. Validation
    if list(df.columns) != EXPECTED_COLUMNS:
        raise ValueError("Colonnes du CSV inattendues.")

    if df[EXPECTED_COLUMNS].isna().any().any():
        raise ValueError("Valeurs obligatoires manquantes.")

    if df["customer_id"].duplicated().any():
        raise ValueError("customer_id en doublon.")

    if not df["customer_zip_code_prefix"].str.fullmatch(
        r"\d{5}"
    ).all():
        raise ValueError("Prefixe postal invalide.")

    print("Validation des donnees reussie.")

    # 3. Connexion SQL Server
    drivers = pyodbc.drivers()

    if "ODBC Driver 18 for SQL Server" in drivers:
        driver = "ODBC Driver 18 for SQL Server"
    elif "ODBC Driver 17 for SQL Server" in drivers:
        driver = "ODBC Driver 17 for SQL Server"
    else:
        raise RuntimeError("Pilote ODBC SQL Server introuvable.")

    connection_string = (
        f"DRIVER={{{driver}}};"
        r"SERVER=.\SQLEXPRESS;"
        "DATABASE=ShopFlowDB;"
        "Trusted_Connection=yes;"
        "Encrypt=yes;"
        "TrustServerCertificate=yes;"
    )

    columns_sql = ", ".join(EXPECTED_COLUMNS)
    placeholders = ", ".join(["?"] * len(EXPECTED_COLUMNS))

    insert_sql = (
        f"INSERT INTO dbo.customers ({columns_sql}) "
        f"VALUES ({placeholders})"
    )

    # 4. Chargement transactionnel
    with pyodbc.connect(
        connection_string,
        autocommit=False,
        timeout=10
    ) as connection:
        cursor = connection.cursor()

        cursor.execute("SELECT COUNT(*) FROM dbo.customers")
        existing_count = cursor.fetchone()[0]

        if existing_count != 0:
            raise RuntimeError(
                f"Chargement refuse : customers contient "
                f"deja {existing_count} lignes."
            )

        try:
            rows = list(
                df[EXPECTED_COLUMNS].itertuples(
                    index=False,
                    name=None
                )
            )

            for start in range(0, len(rows), BATCH_SIZE):
                batch = rows[start:start + BATCH_SIZE]
                cursor.executemany(insert_sql, batch)

                print(
                    f"Lot charge : "
                    f"{min(start + BATCH_SIZE, len(rows))}"
                    f"/{len(rows)}"
                )

            cursor.execute(
                "SELECT COUNT(*) FROM dbo.customers"
            )
            loaded_count = cursor.fetchone()[0]

            if loaded_count != len(df):
                raise RuntimeError(
                    f"Ecart de volume : "
                    f"{loaded_count} != {len(df)}"
                )

            connection.commit()
            print(
                f"Chargement termine : "
                f"{loaded_count} clients."
            )

        except Exception:
            connection.rollback()
            raise


if __name__ == "__main__":
    main()
