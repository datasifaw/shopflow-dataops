
from pathlib import Path
from decimal import Decimal, InvalidOperation

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


def parse_money(value, column):
    try:
        number = Decimal(str(value))
    except InvalidOperation:
        raise ValueError(f"Montant invalide : {column}")

    if not number.is_finite():
        raise ValueError(f"Montant non fini : {column}")

    if number < 0 or number.as_tuple().exponent < -2:
        raise ValueError(f"Montant incorrect : {column}")

    if number >= Decimal("10000000000"):
        raise ValueError(f"Montant hors DECIMAL(12,2) : {column}")

    return number


def main():
    # 1. Extraction
    df = pd.read_csv(CSV_PATH, dtype="string")
    print(f"Articles lus : {len(df)}")
    
     # Validation centralisee
    validate_order_items(df)
    print("Validation des articles reussie.")

    

    # 5. Preparation des enregistrements
    rows = []

    for record in df.itertuples(index=False, name=None):
        order_id, item_id, product_id, seller_id, date, price, freight = record

        rows.append((
            str(order_id),
            int(item_id),
            str(product_id),
            str(seller_id),
            date.to_pydatetime(),
            parse_money(price, "price"),
            parse_money(freight, "freight_value"),
        ))

    print("Validation des articles reussie.")

    # 6. Connexion SQL Server
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

    placeholders = ", ".join(["?"] * len(COLUMNS))
    column_names = ", ".join(COLUMNS)

    insert_sql = (
        f"INSERT INTO dbo.order_items ({column_names}) "
        f"VALUES ({placeholders})"
    )

    connection = pyodbc.connect(
        connection_string,
        autocommit=False,
        timeout=10,
    )

    try:
        cursor = connection.cursor()

        # La table cible doit etre vide
        cursor.execute("SELECT COUNT(*) FROM dbo.order_items")
        existing = cursor.fetchone()[0]

        if existing != 0:
            raise RuntimeError(
                f"Chargement refuse : {existing} articles existent."
            )

        # Tables parentes deja chargees
        cursor.execute("SELECT COUNT(*) FROM dbo.orders")
        if cursor.fetchone()[0] == 0:
            raise RuntimeError("Charger orders avant order_items.")

        cursor.execute("SELECT COUNT(*) FROM dbo.products")
        if cursor.fetchone()[0] == 0:
            raise RuntimeError("Charger products avant order_items.")

        # 7. Insertion par lots
        for start in range(0, len(rows), BATCH_SIZE):
            batch = rows[start:start + BATCH_SIZE]
            cursor.executemany(insert_sql, batch)

            print(
                f"Articles inseres : "
                f"{min(start + BATCH_SIZE, len(rows))}"
                f"/{len(rows)}"
            )

        cursor.execute("SELECT COUNT(*) FROM dbo.order_items")
        loaded = cursor.fetchone()[0]

        if loaded != len(df):
            raise RuntimeError(
                f"Volume incorrect : {loaded} != {len(df)}"
            )

        connection.commit()
        print(f"Chargement termine : {loaded} articles.")

    except Exception:
        connection.rollback()
        raise

    finally:
        connection.close()


if __name__ == "__main__":
    main()
