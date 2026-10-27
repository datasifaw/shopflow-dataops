
from pathlib import Path

import pandas as pd
import pyodbc

from src.data_validation import validate_orders


ROOT = Path(__file__).resolve().parent.parent
CSV_PATH = ROOT / "data" / "raw" / "olist_orders_dataset.csv"

COLUMNS = [
    "order_id",
    "customer_id",
    "order_status",
    "order_purchase_timestamp",
    "order_approved_at",
    "order_delivered_carrier_date",
    "order_delivered_customer_date",
    "order_estimated_delivery_date",
]

DATE_COLUMNS = COLUMNS[3:]

BATCH_SIZE = 1000


def prepare_order_rows(df: pd.DataFrame) -> list[tuple]:
    """
    Valide les commandes et prépare les lignes pour SQL Server.

    Aucune connexion SQL et aucune insertion.
    """
    validate_orders(df)

    prepared = df.copy()

    # Conversion des dates
    for column in DATE_COLUMNS:
        prepared[column] = pd.to_datetime(
            prepared[column],
            format="%Y-%m-%d %H:%M:%S",
            errors="raise",
        )

    # Preparation des valeurs Python compatibles pyodbc
    rows = []

    for record in prepared.itertuples(index=False, name=None):
        values = []

        for value in record:
            if pd.isna(value):
                values.append(None)
            elif isinstance(value, pd.Timestamp):
                values.append(value.to_pydatetime())
            else:
                values.append(str(value))

        rows.append(tuple(values))

    return rows


def main():
    # 1. Extraction
    df = pd.read_csv(CSV_PATH, dtype="string")

    print(f"Commandes lues : {len(df)}")

    # 2. Validation et transformation centralisees
    rows = prepare_order_rows(df)

    print("Validation des commandes reussie.")
    print(f"Commandes preparees : {len(rows)}")

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

    # 4. Configuration de la connexion SQL Server
    connection_string = (
        f"DRIVER={{{driver}}};"
        r"SERVER=.\SQLEXPRESS;"
        "DATABASE=ShopFlowDB;"
        "Trusted_Connection=yes;"
        "Encrypt=yes;"
        "TrustServerCertificate=yes;"
    )

    # 5. Requete d'insertion
    placeholders = ", ".join(["?"] * len(COLUMNS))
    columns_sql = ", ".join(COLUMNS)

    insert_sql = (
        f"INSERT INTO dbo.orders ({columns_sql}) "
        f"VALUES ({placeholders})"
    )

    # 6. Connexion SQL Server
    connection = pyodbc.connect(
        connection_string,
        autocommit=False,
        timeout=10,
    )

    try:
        cursor = connection.cursor()

        # Refuser le chargement si des commandes existent
        cursor.execute("SELECT COUNT(*) FROM dbo.orders")
        existing = cursor.fetchone()[0]

        if existing != 0:
            raise RuntimeError(
                f"Chargement refuse : "
                f"{existing} commandes existent."
            )

        # Verifier que les clients sont deja charges
        cursor.execute(
            "SELECT COUNT(*) FROM dbo.customers"
        )

        customers_count = cursor.fetchone()[0]

        if customers_count == 0:
            raise RuntimeError(
                "Charger customers avant orders."
            )

        # 7. Chargement transactionnel par lots
        for start in range(0, len(rows), BATCH_SIZE):
            batch = rows[start:start + BATCH_SIZE]

            cursor.executemany(insert_sql, batch)

            print(
                f"Commandes inserees : "
                f"{min(start + BATCH_SIZE, len(rows))}"
                f"/{len(rows)}"
            )

        # 8. Verification du volume
        cursor.execute(
            "SELECT COUNT(*) FROM dbo.orders"
        )

        loaded = cursor.fetchone()[0]

        if loaded != len(df):
            raise RuntimeError(
                f"Volume incorrect : {loaded} != {len(df)}"
            )

        # 9. Validation de la transaction
        connection.commit()

        print(
            f"Chargement termine : {loaded} commandes."
        )

    except Exception:
        connection.rollback()
        raise

    finally:
        connection.close()


if __name__ == "__main__":
    main()
