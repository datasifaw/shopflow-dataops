
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
