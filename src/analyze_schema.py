
from pathlib import Path
import pandas as pd

DATA_DIR = Path(__file__).resolve().parent.parent / "data" / "raw"

files = [
    "olist_orders_dataset.csv",
    "olist_customers_dataset.csv",
    "olist_order_items_dataset.csv",
    "olist_products_dataset.csv",
]

for filename in files:
    df = pd.read_csv(DATA_DIR / filename)

    print(f"\n--- {filename} ---")
    print(f"Nombre de lignes : {len(df)}")

    for column in df.columns:
        dtype = df[column].dtype
        missing = df[column].isna().sum()

        print(f"\nColonne : {column}")
        print(f"Type Pandas : {dtype}")
        print(f"Valeurs manquantes : {missing}")

        if pd.api.types.is_string_dtype(dtype) or dtype == object:
            max_length = df[column].dropna().astype(str).str.len().max()
            print(f"Longueur maximale : {max_length}")




print("\n--- ANALYSE DES COLONNES NUMÉRIQUES ---")

for filename in files:
    df = pd.read_csv(DATA_DIR / filename)
    print(f"\nFichier : {filename}")

    for column in df.select_dtypes(include="number").columns:
        values = df[column].dropna()

        if values.empty:
            print(f"{column} : aucune valeur numérique")
            continue

        has_decimals = (values % 1 != 0).any()

        print(f"\nColonne : {column}")
        print(f"Minimum : {values.min()}")
        print(f"Maximum : {values.max()}")
        print(f"Contient des décimales : {has_decimals}")