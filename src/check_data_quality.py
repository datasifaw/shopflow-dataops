
from pathlib import Path
import pandas as pd

DATA_DIR = Path(__file__).resolve().parent.parent / "data" / "raw"

files = [
    "olist_orders_dataset.csv",
    "olist_order_items_dataset.csv",
    "olist_customers_dataset.csv",
    "olist_products_dataset.csv",
]

for filename in files:
    df = pd.read_csv(DATA_DIR / filename)

    print(f"\n--- {filename} ---")
    print(f"Nombre de lignes : {len(df)}")
    print(f"Doublons de lignes : {df.duplicated().sum()}")

    missing_values = df.isna().sum()
    missing_values = missing_values[missing_values > 0]

    print("Valeurs manquantes par colonne :")

    if missing_values.empty:
        print("Aucune valeur manquante")
    else:
        print(missing_values.to_string())







items = pd.read_csv(DATA_DIR / "olist_order_items_dataset.csv")

print("\n--- CONTRÔLE DES PRIX ET FRAIS DE LIVRAISON ---")

for column in ["price", "freight_value"]:
    values = pd.to_numeric(items[column], errors="coerce")

    print(f"\nColonne : {column}")
    print(f"Valeurs non numériques ou manquantes : {values.isna().sum()}")
    print(f"Valeurs négatives : {(values < 0).sum()}")
    print(f"Valeurs égales à zéro : {(values == 0).sum()}")
    print(f"Valeur minimale : {values.min()}")
    print(f"Valeur maximale : {values.max()}")







orders = pd.read_csv(DATA_DIR / "olist_orders_dataset.csv")

date_columns = [
    "order_purchase_timestamp",
    "order_approved_at",
    "order_delivered_carrier_date",
    "order_delivered_customer_date",
]

for column in date_columns:
    orders[column] = pd.to_datetime(
        orders[column], errors="coerce"
    )

print("\n--- CONTRÔLE DES DATES ---")

date_checks = [
    ("Approbation avant achat",
     "order_purchase_timestamp", "order_approved_at"),
    ("Transport avant achat",
     "order_purchase_timestamp", "order_delivered_carrier_date"),
    ("Livraison avant achat",
     "order_purchase_timestamp", "order_delivered_customer_date"),
    ("Livraison avant transport",
     "order_delivered_carrier_date", "order_delivered_customer_date"),
]

for label, first, second in date_checks:
    valid_dates = orders[first].notna() & orders[second].notna()
    anomalies = valid_dates & (orders[second] < orders[first])
    print(f"{label} : {anomalies.sum()}")