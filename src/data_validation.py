
import pandas as pd


def validate_customers(df: pd.DataFrame) -> None:
    required_columns = [
        "customer_id",
        "customer_unique_id",
        "customer_zip_code_prefix",
        "customer_city",
        "customer_state",
    ]

    if list(df.columns) != required_columns:
        raise ValueError("Colonnes clients inattendues.")

    if df[required_columns].isna().any().any():
        raise ValueError("Valeurs clients manquantes.")

    if df["customer_id"].duplicated().any():
        raise ValueError("customer_id en doublon.")

    zip_codes = df["customer_zip_code_prefix"].astype("string")

    if not zip_codes.str.fullmatch(r"\d{5}").all():
        raise ValueError("Prefixe postal invalide.")




def validate_products(df: pd.DataFrame) -> None:
    required_columns = [
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

    if list(df.columns) != required_columns:
        raise ValueError("Colonnes produits inattendues.")

    if df["product_id"].isna().any():
        raise ValueError("product_id manquant.")

    if df["product_id"].duplicated().any():
        raise ValueError("product_id en doublon.")

    if (df["product_id"].astype("string").str.len() != 32).any():
        raise ValueError("Longueur product_id invalide.")

    categories = df["product_category_name"].dropna()

    if (categories.astype("string").str.len() > 100).any():
        raise ValueError("Categorie produit trop longue.")

    numeric_columns = required_columns[2:]

    for column in numeric_columns:
        original = df[column]
        values = pd.to_numeric(original, errors="coerce")

        invalid = original.notna() & values.isna()

        if invalid.any():
            raise ValueError(f"Valeur non numerique : {column}")

        non_null = values.dropna()

        if (non_null < 0).any():
            raise ValueError(f"Valeur negative : {column}")

        if ((non_null % 1) != 0).any():
            raise ValueError(f"Valeur non entiere : {column}")

        if (non_null > 2147483647).any():
            raise ValueError(f"Valeur hors plage INT : {column}")



def validate_orders(df: pd.DataFrame) -> None:
    required_columns = [
        "order_id",
        "customer_id",
        "order_status",
        "order_purchase_timestamp",
        "order_approved_at",
        "order_delivered_carrier_date",
        "order_delivered_customer_date",
        "order_estimated_delivery_date",
    ]

    if list(df.columns) != required_columns:
        raise ValueError("Colonnes commandes inattendues.")

    for column in ["order_id", "customer_id", "order_status"]:
        if df[column].isna().any():
            raise ValueError(f"Valeur manquante : {column}")

    if df["order_id"].duplicated().any():
        raise ValueError("order_id en doublon.")

    for column in ["order_id", "customer_id"]:
        lengths = df[column].astype("string").str.len()
        if (lengths != 32).any():
            raise ValueError(f"Identifiant invalide : {column}")

    if (df["order_status"].astype("string").str.len() > 20).any():
        raise ValueError("Statut trop long.")

    date_columns = required_columns[3:]
    required_dates = [
        "order_purchase_timestamp",
        "order_estimated_delivery_date",
    ]

    for column in date_columns:
        original = df[column]

        parsed = pd.to_datetime(
            original,
            format="%Y-%m-%d %H:%M:%S",
            errors="coerce",
        )

        invalid = original.notna() & parsed.isna()

        if invalid.any():
            raise ValueError(f"Date invalide : {column}")

        if column in required_dates and parsed.isna().any():
            raise ValueError(f"Date obligatoire manquante : {column}")




from decimal import Decimal, InvalidOperation


def validate_order_items(df: pd.DataFrame) -> None:
    required_columns = [
        "order_id",
        "order_item_id",
        "product_id",
        "seller_id",
        "shipping_limit_date",
        "price",
        "freight_value",
    ]

    if list(df.columns) != required_columns:
        raise ValueError("Colonnes articles inattendues.")

    if df[required_columns].isna().any().any():
        raise ValueError("Valeurs obligatoires manquantes.")

    for column in ["order_id", "product_id", "seller_id"]:
        lengths = df[column].astype("string").str.len()

        if (lengths != 32).any():
            raise ValueError(f"Identifiant invalide : {column}")

    item_ids = pd.to_numeric(
        df["order_item_id"], errors="coerce"
    )

    if item_ids.isna().any():
        raise ValueError("order_item_id non numerique.")

    if (
        (item_ids % 1 != 0).any()
        or (item_ids < 1).any()
        or (item_ids > 2147483647).any()
    ):
        raise ValueError("order_item_id invalide.")

    if df.duplicated(
        subset=["order_id", "order_item_id"]
    ).any():
        raise ValueError("Cle composite en doublon.")

    dates = pd.to_datetime(
        df["shipping_limit_date"],
        format="%Y-%m-%d %H:%M:%S",
        errors="coerce",
    )

    if dates.isna().any():
        raise ValueError("Date shipping invalide.")

    for column in ["price", "freight_value"]:
        for value in df[column]:
            try:
                amount = Decimal(str(value))
            except (InvalidOperation, ValueError, TypeError):
                raise ValueError(
                    f"Montant non numerique : {column}"
                )

            if not amount.is_finite():
                raise ValueError(f"Montant non fini : {column}")

            if amount < 0:
                raise ValueError(f"Montant negatif : {column}")

            if amount.as_tuple().exponent < -2:
                raise ValueError(
                    f"Montant avec trop de decimales : {column}"
                )

            if amount >= Decimal("10000000000"):
                raise ValueError(
                    f"Montant hors DECIMAL(12,2) : {column}"
                )
