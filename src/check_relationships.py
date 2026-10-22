
from pathlib import Path
import pandas as pd

DATA_DIR = Path(__file__).resolve().parent.parent / "data" / "raw"

orders = pd.read_csv(DATA_DIR / "olist_orders_dataset.csv")
items = pd.read_csv(DATA_DIR / "olist_order_items_dataset.csv")

print(f"Commandes : {len(orders)}")
print(f"Lignes d'articles : {len(items)}")

print(f"order_id uniques dans orders : {orders['order_id'].nunique()}")
print(f"order_id uniques dans items : {items['order_id'].nunique()}")

missing_orders = ~items["order_id"].isin(orders["order_id"])
print(f"Articles sans commande correspondante : {missing_orders.sum()}")




customers = pd.read_csv(DATA_DIR / "olist_customers_dataset.csv")
products = pd.read_csv(DATA_DIR / "olist_products_dataset.csv")

print("\n--- RELATION CLIENTS / COMMANDES ---")
print(f"customer_id dupliqués dans customers : {customers['customer_id'].duplicated().sum()}")
print(f"Commandes sans customer_id : {orders['customer_id'].isna().sum()}")

missing_customers = (
    orders["customer_id"].notna()
    & ~orders["customer_id"].isin(customers["customer_id"])
)
print(f"Commandes sans client correspondant : {missing_customers.sum()}")

print("\n--- RELATION PRODUITS / ARTICLES ---")
print(f"product_id dupliqués dans products : {products['product_id'].duplicated().sum()}")
print(f"Articles sans product_id : {items['product_id'].isna().sum()}")

missing_products = (
    items["product_id"].notna()
    & ~items["product_id"].isin(products["product_id"])
)
print(f"Articles sans produit correspondant : {missing_products.sum()}")





print("\n--- VÉRIFICATION DES CLÉS ---")

print(f"order_id nuls dans orders : {orders['order_id'].isna().sum()}")
print(f"order_id dupliqués dans orders : {orders['order_id'].duplicated().sum()}")

print(f"order_id nuls dans items : {items['order_id'].isna().sum()}")
print(f"order_item_id nuls : {items['order_item_id'].isna().sum()}")

duplicate_items = items.duplicated(
    subset=["order_id", "order_item_id"]
)
print(f"Clés composites dupliquées dans items : {duplicate_items.sum()}")

print(f"customer_id nuls dans customers : {customers['customer_id'].isna().sum()}")
print(f"product_id nuls dans products : {products['product_id'].isna().sum()}")

orders_without_items = ~orders["order_id"].isin(items["order_id"])
print(f"Commandes sans article : {orders_without_items.sum()}")

print("\n--- STATUTS DES COMMANDES SANS ARTICLE ---")
print(
    orders.loc[orders_without_items, "order_status"]
    .value_counts(dropna=False)
)
  