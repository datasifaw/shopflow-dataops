
from datetime import datetime
from decimal import Decimal
from pathlib import Path

import pandas as pd
import pyodbc

from src.data_validation import validate_order_items


ROOT = Path(__file__).resolve().parent.parent
CSV_PATH = ROOT / "data" / "raw" / "olist_order_items_dataset.csv"

COLUMNS = [
    "order_id",
    "order_item_id",
    "product_id",
    "seller_id",
    "shipping_limit_date",
    "price",
    "freight_value",
]

BATCH_SIZE = 1000


def prepare_order_item_rows(df: pd.DataFrame) -> list[tuple]:
    """
    Valide et transforme les articles commandes.

    Aucune connexion SQL Server et aucune insertion.
    """
    validate_order_items(df)

    rows = []

    for record in df.itertuples(index=False, name=None):
        (
            order_id,
            order_item_id,
            product_id,
            seller_id,
            shipping_limit_date,
            price,
            freight_value,
        ) = record

        shipping_date = pd.to_datetime(
            shipping_limit_date,
            format="%Y-%m-%d %H:%M:%S",
            errors="raise",
        )

        if isinstance(shipping_date, pd.Timestamp):
            shipping_date = shipping_date.to_pydatetime()

        row = (
            str(order_id),
            int(order_item_id),
            str(product_id),
            str(seller_id),
            shipping_date,
            Decimal(str(price)),
            Decimal(str(freight_value)),
        )

        rows.append(row)

    return rows


def main():
    # 1. Extraction CSV
    df = pd.read_csv(CSV_PATH, dtype="string")

    print(f"Articles lus : {len(df)}")

    # 2. Validation et transformation
    rows = prepare_order_item_rows(df)

    print("Validation des articles reussie.")
    print(f"Articles prepares : {len(rows)}")

    # 3. Recherche du pilote SQL Server
    drivers = pyodbc.drivers()

    if "ODBC Driver 18 for SQL Server" in drivers:
        driver = "ODBC Driver 18 for SQL Server"
    elif "ODBC Driver 17 for SQL Server" in drivers:
        driver = "ODBC Driver 17 for SQL Server"
    else:
        raise RuntimeError(
            "Pilote ODBC SQL Server introuvable."
        )

    # 4. Connexion SQL Server
    connection_string = (
        f"DRIVER={{{driver}}};"
        r"SERVER=.\SQLEXPRESS;"
        "DATABASE=ShopFlowDB;"
        "Trusted_Connection=yes;"
        "Encrypt=yes;"
        "TrustServerCertificate=yes;"
    )

    placeholders = ", ".join(["?"] * len(COLUMNS))
    columns_sql = ", ".join(COLUMNS)

    insert_sql = (
        f"INSERT INTO dbo.order_items ({columns_sql}) "
        f"VALUES ({placeholders})"
    )

    connection = pyodbc.connect(
        connection_string,
        autocommit=False,
        timeout=10,
    )

    try:
        cursor = connection.cursor()

        # 5. Eviter les doubles chargements
        cursor.execute(
            "SELECT COUNT(*) FROM dbo.order_items"
        )

        existing = cursor.fetchone()[0]

        if existing != 0:
            raise RuntimeError(
                f"Chargement refuse : "
                f"{existing} articles existent deja."
            )

        # 6. Verifier les tables parentes
        cursor.execute(
            "SELECT COUNT(*) FROM dbo.orders"
        )
        orders_count = cursor.fetchone()[0]

        if orders_count == 0:
            raise RuntimeError(
                "Charger orders avant order_items."
            )

        cursor.execute(
            "SELECT COUNT(*) FROM dbo.products"
        )
        products_count = cursor.fetchone()[0]

        if products_count == 0:
            raise RuntimeError(
                "Charger products avant order_items."
            )

        # 7. Chargement transactionnel par lots
        for start in range(0, len(rows), BATCH_SIZE):
            batch = rows[start:start + BATCH_SIZE]

            cursor.executemany(insert_sql, batch)

            print(
                f"Articles inseres : "
                f"{min(start + BATCH_SIZE, len(rows))}"
                f"/{len(rows)}"
            )

        # 8. Verification du volume
        cursor.execute(
            "SELECT COUNT(*) FROM dbo.order_items"
        )

        loaded = cursor.fetchone()[0]

        if loaded != len(rows):
            raise RuntimeError(
                f"Volume incorrect : {loaded} != {len(rows)}"
            )

        # 9. Validation de la transaction
        connection.commit()

        print(
            f"Chargement termine : {loaded} articles."
        )

    except Exception:
        connection.rollback()
        raise

    finally:
        connection.close()


if __name__ == "__main__":
    main()
