
from datetime import datetime
from decimal import Decimal

import pandas as pd

from src.load_products import prepare_product_rows
from src.load_orders import prepare_order_rows
from src.load_order_items import prepare_order_item_rows


def test_products_csv_to_sql_rows(tmp_path):
    csv_path = tmp_path / "products.csv"

    source = pd.DataFrame({
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

    source.to_csv(csv_path, index=False)

    df = pd.read_csv(
        csv_path,
        dtype={
            "product_id": "string",
            "product_category_name": "string",
        },
    )

    rows = prepare_product_rows(df)

    assert len(rows) == 2
    assert rows[0][0] == "a" * 32
    assert rows[0][4] == 2
    assert rows[0][5] == 500

    assert rows[1][1] is None
    assert rows[1][2] is None
    assert rows[1][4] is None

    assert isinstance(rows[0][5], int)
    assert isinstance(rows[1][5], int)


def test_orders_csv_to_sql_rows(tmp_path):
    csv_path = tmp_path / "orders.csv"

    source = pd.DataFrame({
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

    source.to_csv(csv_path, index=False)

    df = pd.read_csv(csv_path, dtype="string")
    rows = prepare_order_rows(df)

    assert len(rows) == 2
    assert rows[0][0] == "a" * 32
    assert rows[1][2] == "shipped"

    assert isinstance(rows[0][3], datetime)
    assert rows[0][3].year == 2018

    assert rows[1][4] is None
    assert rows[1][5] is None
    assert rows[1][6] is None

    assert isinstance(rows[1][7], datetime)


def test_order_items_csv_to_sql_rows(tmp_path):
    csv_path = tmp_path / "order_items.csv"

    # Deux articles pour une meme commande
    source = pd.DataFrame({
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

    source.to_csv(csv_path, index=False)

    # Extraction
    df = pd.read_csv(csv_path, dtype="string")

    # Validation et transformation
    rows = prepare_order_item_rows(df)

    # Nombre de lignes
    assert len(rows) == 2

    # Cle composite
    assert rows[0][0] == rows[1][0]
    assert rows[0][1] == 1
    assert rows[1][1] == 2
    assert isinstance(rows[0][1], int)

    # Conversion des dates
    assert isinstance(rows[0][4], datetime)
    assert rows[0][4].year == 2018

    # Montants Decimal pour SQL Server
    assert rows[0][5] == Decimal("58.90")
    assert rows[0][6] == Decimal("0.00")
    assert rows[1][5] == Decimal("120.00")
    assert rows[1][6] == Decimal("15.50")

    assert isinstance(rows[0][5], Decimal)
    assert isinstance(rows[1][6], Decimal)
