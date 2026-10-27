
import pandas as pd
import pytest

from src.data_validation import validate_orders


def sample_orders():
    return pd.DataFrame({
        "order_id": ["a" * 32, "b" * 32],
        "customer_id": ["c" * 32, "d" * 32],
        "order_status": ["delivered", "shipped"],
        "order_purchase_timestamp": [
            "2018-01-10 10:00:00",
            "2018-02-10 11:00:00",
        ],
        "order_approved_at": [
            "2018-01-10 11:00:00",
            None,
        ],
        "order_delivered_carrier_date": [
            "2018-01-12 09:00:00",
            None,
        ],
        "order_delivered_customer_date": [
            "2018-01-15 16:00:00",
            None,
        ],
        "order_estimated_delivery_date": [
            "2018-01-20 00:00:00",
            "2018-02-25 00:00:00",
        ],
    })


def test_valid_orders():
    validate_orders(sample_orders())


def test_duplicate_order_id():
    df = sample_orders()
    df.loc[1, "order_id"] = df.loc[0, "order_id"]

    with pytest.raises(ValueError, match="doublon"):
        validate_orders(df)


def test_missing_customer_id():
    df = sample_orders()
    df.loc[0, "customer_id"] = None

    with pytest.raises(ValueError, match="manquante"):
        validate_orders(df)


def test_invalid_order_id_length():
    df = sample_orders()
    df.loc[0, "order_id"] = "abc"

    with pytest.raises(ValueError, match="Identifiant"):
        validate_orders(df)


def test_invalid_purchase_date():
    df = sample_orders()
    df.loc[0, "order_purchase_timestamp"] = "date_invalide"

    with pytest.raises(ValueError, match="Date invalide"):
        validate_orders(df)


def test_missing_required_delivery_estimate():
    df = sample_orders()
    df.loc[0, "order_estimated_delivery_date"] = None

    with pytest.raises(ValueError, match="obligatoire"):
        validate_orders(df)




def test_orders_loader_uses_shared_validator():
    from src.load_orders import validate_orders as loader_validator

    assert loader_validator is validate_orders
