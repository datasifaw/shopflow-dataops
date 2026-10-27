
import pandas as pd
import pytest

from src.data_validation import validate_customers


def sample_customers():
    return pd.DataFrame({
        "customer_id": ["client_001", "client_002"],
        "customer_unique_id": ["unique_001", "unique_002"],
        "customer_zip_code_prefix": ["01234", "56789"],
        "customer_city": ["sao paulo", "rio de janeiro"],
        "customer_state": ["SP", "RJ"],
    })


def test_valid_customers():
    df = sample_customers()
    validate_customers(df)


def test_duplicate_customer_id():
    df = sample_customers()
    df.loc[1, "customer_id"] = "client_001"

    with pytest.raises(ValueError, match="doublon"):
        validate_customers(df)


def test_missing_customer_id():
    df = sample_customers()
    df.loc[0, "customer_id"] = None

    with pytest.raises(ValueError, match="manquantes"):
        validate_customers(df)


def test_invalid_zip_code():
    df = sample_customers()
    df.loc[0, "customer_zip_code_prefix"] = "123"

    with pytest.raises(ValueError, match="postal"):
        validate_customers(df)


def test_missing_column():
    df = sample_customers().drop(columns=["customer_state"])

    with pytest.raises(ValueError, match="Colonnes"):
        validate_customers(df)
