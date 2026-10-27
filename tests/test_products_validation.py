
import pandas as pd
import pytest

from src.data_validation import validate_products


def sample_products():
    return pd.DataFrame({
        "product_id": ["a" * 32, "b" * 32],
        "product_category_name": ["informatica", None],
        "product_name_lenght": [30, None],
        "product_description_lenght": [150, None],
        "product_photos_qty": [2, None],
        "product_weight_g": [500, 1000],
        "product_length_cm": [20, 30],
        "product_height_cm": [10, 15],
        "product_width_cm": [15, 20],
    })


def test_valid_products():
    validate_products(sample_products())


def test_duplicate_product_id():
    df = sample_products()
    df.loc[1, "product_id"] = df.loc[0, "product_id"]

    with pytest.raises(ValueError, match="doublon"):
        validate_products(df)


def test_missing_product_id():
    df = sample_products()
    df.loc[0, "product_id"] = None

    with pytest.raises(ValueError, match="manquant"):
        validate_products(df)


def test_negative_product_weight():
    df = sample_products()
    df.loc[0, "product_weight_g"] = -10

    with pytest.raises(ValueError, match="negative"):
        validate_products(df)


def test_fractional_photo_quantity():
    df = sample_products()
    df.loc[0, "product_photos_qty"] = 1.5

    with pytest.raises(ValueError, match="non entiere"):
        validate_products(df)


def test_missing_product_column():
    df = sample_products().drop(
        columns=["product_width_cm"]
    )

    with pytest.raises(ValueError, match="Colonnes"):
        validate_products(df)




def test_products_loader_uses_shared_validator():
    from src.load_products import validate_products as loader_validator

    assert loader_validator is validate_products
