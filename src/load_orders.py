
from pathlib import Path

import pandas as pd
import pyodbc


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
REQUIRED_DATES = [
    "order_purchase_timestamp",
    "order_estimated_delivery_date",
]

BATCH_SIZE = 1000


def main():
    # Extraction
    df = pd.read_csv(CSV_PATH, dtype="string")

    print(f"Commandes lues : {len(df)}")

    # Validation des colonnes et identifiants
    if list(df.columns) != COLUMNS:
        raise ValueError("Structure CSV inattendue.")

    for column in ["order_id", "customer_id", "order_status"]:
        if df[column].isna().any():
            raise ValueError(f"Valeur manquante : {column}")

    if df["order_id"].duplicated().any():
        raise ValueError("order_id en doublon.")

    if (df["order_id"].str.len() > 32).any():
        raise ValueError("order_id trop long.")

    if (df["customer_id"].str.len() > 32).any():
        raise ValueError("customer_id trop long.")

    if (df["order_status"].str.len() > 20).any():
        raise ValueError("order_status trop long.")

    # Conversion des dates
    for column in DATE_COLUMNS:
        original = df[column]

        parsed = pd.to_datetime(
            original,
            format="%Y-%m-%d %H:%M:%S",
            errors="coerce",
        )

        invalid = original.notna() & parsed.isna()

        if invalid.any():
            raise ValueError(
                f"{invalid.sum()} dates invalides : {column}"
            )

        df[column] = parsed

    for column in REQUIRED_DATES:
        if df[column].isna().any():
            raise ValueError(
                f"Date obligatoire manquante : {column}"
            )

    print("Validation des commandes reussie.")

    # Preparation des enregistrements SQL
    rows = []

    for record in df.itertuples(index=False, name=None):
        values = []

        for value in record:
            if pd.isna(value):
                values.append(None)
            elif isinstance(value, pd.Timestamp):
                values.append(value.to_pydatetime())
            else:
                values.append(str(value))

        rows.append(tuple(values))

    # Connexion SQL Server
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
    columns_sql = ", ".join(COLUMNS)

    insert_sql = (
        f"INSERT INTO dbo.orders ({columns_sql}) "
        f"VALUES ({placeholders})"
    )

    connection = pyodbc.connect(
        connection_string,
        autocommit=False,
        timeout=10,
    )

    try:
        cursor = connection.cursor()

        # Refuser le chargement si la table est remplie
        cursor.execute("SELECT COUNT(*) FROM dbo.orders")
        existing = cursor.fetchone()[0]

        if existing != 0:
            raise RuntimeError(
                f"Chargement refuse : {existing} commandes existent."
            )

        # Verifier les clients avant insertion
        cursor.execute(
            "SELECT COUNT(*) FROM dbo.customers"
        )
        customers_count = cursor.fetchone()[0]

        if customers_count == 0:
            raise RuntimeError(
                "Charger customers avant orders."
            )

        # Chargement transactionnel par lots
        for start in range(0, len(rows), BATCH_SIZE):
            batch = rows[start:start + BATCH_SIZE]

            cursor.executemany(insert_sql, batch)

            print(
                f"Commandes inserees : "
                f"{min(start + BATCH_SIZE, len(rows))}"
                f"/{len(rows)}"
            )

        cursor.execute("SELECT COUNT(*) FROM dbo.orders")
        loaded = cursor.fetchone()[0]

        if loaded != len(df):
            raise RuntimeError(
                f"Volume incorrect : {loaded} != {len(df)}"
            )

        connection.commit()
        print(f"Chargement termine : {loaded} commandes.")

    except Exception:
        connection.rollback()
        raise

    finally:
        connection.close()


if __name__ == "__main__":
    main()
