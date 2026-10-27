
from pathlib import Path

import pandas as pd
import pyodbc
from src.data_validation import validate_products


# Configuration
ROOT = Path(__file__).resolve().parent.parent
CSV_PATH = ROOT / "data" / "raw" / "olist_products_dataset.csv"

COLUMNS = [
    "product_id",
    "product_category_name",
    "product_name_lenght",
    "product_description_lenght",
    "product_photos_qty",
    "product_weight_g",
    "product_length_cm",
    "product_height_cm",
    "product_width_cm",
]

NUMERIC_COLUMNS = COLUMNS[2:]
BATCH_SIZE = 1000


def prepare_product_rows(df):
    validate_products(df)

    rows = []

    for record in df.itertuples(index=False, name=None):
        values = []

        for index, value in enumerate(record):
            if pd.isna(value):
                values.append(None)
            elif index >= 2:
                values.append(int(value))
            else:
                values.append(str(value))

        rows.append(tuple(values))

    return rows


def main():
    # 1. Extraction
    df = pd.read_csv(
        CSV_PATH,
        dtype={
            "product_id": "string",
            "product_category_name": "string",
        },
    )

    print(f"Produits lus : {len(df)}")

    # 2. Validation

    
    # 2. Validation centralisee
    validate_products(df)

    print("Validation des produits reussie.")
    print("Valeurs NULL par colonne :")
    print(df.isna().sum().to_string())

   

    # 3. Preparation des lignes
    rows = prepare_product_rows(df)

    for record in df.itertuples(index=False, name=None):
        values = []

        for index, value in enumerate(record):
            if pd.isna(value):
                values.append(None)
            elif index >= 2:
                values.append(int(value))
            else:
                values.append(str(value))

        rows.append(tuple(values))

    # 4. Connexion SQL Server
    drivers = pyodbc.drivers()

    if "ODBC Driver 18 for SQL Server" in drivers:
        driver = "ODBC Driver 18 for SQL Server"
    elif "ODBC Driver 17 for SQL Server" in drivers:
        driver = "ODBC Driver 17 for SQL Server"
    else:
        raise RuntimeError("Pilote SQL Server introuvable.")

    connection_string = (
        f"DRIVER={{{driver}}};"
        r"SERVER=.\SQLEXPRESS;"
        "DATABASE=ShopFlowDB;"
        "Trusted_Connection=yes;"
        "Encrypt=yes;"
        "TrustServerCertificate=yes;"
    )

    placeholders = ", ".join(["?"] * len(COLUMNS))
    column_names = ", ".join(COLUMNS)

    insert_sql = (
        f"INSERT INTO dbo.products ({column_names}) "
        f"VALUES ({placeholders})"
    )

    # 5. Chargement transactionnel
    connection = pyodbc.connect(
        connection_string,
        autocommit=False,
        timeout=10,
    )

    try:
        cursor = connection.cursor()

        cursor.execute("SELECT COUNT(*) FROM dbo.products")
        existing_count = cursor.fetchone()[0]

        if existing_count != 0:
            raise RuntimeError(
                f"Chargement refuse : {existing_count} "
                "produits existent deja."
            )

        for start in range(0, len(rows), BATCH_SIZE):
            batch = rows[start:start + BATCH_SIZE]

            cursor.executemany(insert_sql, batch)

            print(
                f"Produits inseres : "
                f"{min(start + BATCH_SIZE, len(rows))}"
                f"/{len(rows)}"
            )

        cursor.execute(
            "SELECT COUNT(*) FROM dbo.products"
        )
        loaded_count = cursor.fetchone()[0]

        if loaded_count != len(df):
            raise RuntimeError(
                f"Volume incorrect : {loaded_count}"
            )

        connection.commit()

        print(
            f"Chargement termine : "
            f"{loaded_count} produits."
        )

    except Exception:
        connection.rollback()
        raise

    finally:
        connection.close()


if __name__ == "__main__":
    main()
