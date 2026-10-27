
import pandas as pd
import pytest

from src.data_validation import validate_order_items


def sample_order_items():
    return pd.DataFrame({
        "order_id": ["a" * 32, "a" * 32],
        "order_item_id": [1, 2],
        "product_id": ["b" * 32, "c" * 32],
        "seller_id": ["d" * 32, "e" * 32],
        "shipping_limit_date": [
            "2018-01-15 10:00:00",
            "2018-01-15 10:00:00",
        ],
        "price": ["58.90", "120.00"],
        "freight_value": ["0.00", "15.50"],
    })


def test_valid_order_items():
    validate_order_items(sample_order_items())


def test_duplicate_composite_key():
    df = sample_order_items()
    df.loc[1, "order_item_id"] = 1

    with pytest.raises(ValueError, match="doublon"):
        validate_order_items(df)


def test_negative_price():
    df = sample_order_items()
    df.loc[0, "price"] = "-10.00"

    with pytest.raises(ValueError, match="negatif"):
        validate_order_items(df)


def test_invalid_shipping_date():
    df = sample_order_items()
    df.loc[0, "shipping_limit_date"] = "date_invalide"

    with pytest.raises(ValueError, match="Date shipping"):
        validate_order_items(df)


def test_invalid_item_id():
    df = sample_order_items()
    df.loc[0, "order_item_id"] = 0

    with pytest.raises(ValueError, match="order_item_id invalide"):
        validate_order_items(df)


def test_excessive_price_decimals():
    df = sample_order_items()
    df.loc[0, "price"] = "12.345"

    with pytest.raises(ValueError, match="trop de decimales"):
        validate_order_items(df)
