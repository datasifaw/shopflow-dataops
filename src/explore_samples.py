
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
    print(f"Dimensions : {df.shape}")

    print("\n5 premières lignes :")
    print(df.head().to_string(index=False))

    print("\n5 lignes aléatoires :")
    print(
        df.sample(
            n=min(5, len(df)),
            random_state=42
        ).to_string(index=False)
    )

orders = pd.read_csv(DATA_DIR / "olist_orders_dataset.csv")
products = pd.read_csv(DATA_DIR / "olist_products_dataset.csv")

print("\n--- STATUTS DES COMMANDES ---")
print(
    orders["order_status"]
    .value_counts(dropna=False)
    .to_string()
)

print("\n--- TOP 10 CATÉGORIES PRODUITS ---")
print(
    products["product_category_name"]
    .value_counts(dropna=False)
    .head(10)
    .to_string()
)