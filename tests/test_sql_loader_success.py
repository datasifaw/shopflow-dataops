
from datetime import datetime
from decimal import Decimal
from unittest.mock import MagicMock, call, patch

import pandas as pd

from src import load_orders, load_products, load_order_items


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


def test_orders_loader_commits_on_success():
    connection = MagicMock()
    cursor = connection.cursor.return_value

    # Orders vide, Customers charge, puis 2 commandes.
    cursor.fetchone.side_effect = [
        (0,),
        (99441,),
        (2,),
    ]

    with (
        patch.object(
            load_orders.pd,
            "read_csv",
            return_value=sample_orders(),
        ),
        patch.object(
            load_orders.pyodbc,
            "drivers",
            return_value=["ODBC Driver 18 for SQL Server"],
        ),
        patch.object(
            load_orders.pyodbc,
            "connect",
            return_value=connection,
        ) as mock_connect,
    ):
        load_orders.main()

    mock_connect.assert_called_once()

    assert cursor.execute.call_args_list == [
        call("SELECT COUNT(*) FROM dbo.orders"),
        call("SELECT COUNT(*) FROM dbo.customers"),
        call("SELECT COUNT(*) FROM dbo.orders"),
    ]

    cursor.executemany.assert_called_once()

    insert_sql, rows = cursor.executemany.call_args.args

    assert "INSERT INTO dbo.orders" in insert_sql
    assert len(rows) == 2
    assert rows[0][0] == "a" * 32
    assert rows[1][0] == "b" * 32

    assert isinstance(rows[0][3], datetime)
    assert rows[1][4] is None

    connection.commit.assert_called_once()
    connection.rollback.assert_not_called()
    connection.close.assert_called_once()


def test_products_loader_commits_on_success():
    connection = MagicMock()
    cursor = connection.cursor.return_value

    # Products vide, puis 2 produits charges.
    cursor.fetchone.side_effect = [
        (0,),
        (2,),
    ]

    with (
        patch.object(
            load_products.pd,
            "read_csv",
            return_value=sample_products(),
        ),
        patch.object(
            load_products.pyodbc,
            "drivers",
            return_value=["ODBC Driver 18 for SQL Server"],
        ),
        patch.object(
            load_products.pyodbc,
            "connect",
            return_value=connection,
        ) as mock_connect,
    ):
        load_products.main()

    mock_connect.assert_called_once()

    assert cursor.execute.call_args_list == [
        call("SELECT COUNT(*) FROM dbo.products"),
        call("SELECT COUNT(*) FROM dbo.products"),
    ]

    cursor.executemany.assert_called_once()

    insert_sql, rows = cursor.executemany.call_args.args

    assert "INSERT INTO dbo.products" in insert_sql
    assert len(rows) == 2

    assert rows[0][0] == "a" * 32
    assert rows[1][0] == "b" * 32

    assert rows[1][1] is None
    assert rows[1][2] is None
    assert rows[1][4] is None

    assert rows[0][4] == 2
    assert rows[0][5] == 500
    assert isinstance(rows[0][5], int)

    connection.commit.assert_called_once()
    connection.rollback.assert_not_called()
    connection.close.assert_called_once()


def test_order_items_loader_commits_on_success():
    """
    Simuler un chargement reussi des articles.

    Verifier les tables parentes, les lignes inserees,
    les montants Decimal, le commit et la fermeture.
    """
    connection = MagicMock()
    cursor = connection.cursor.return_value

    # Quatre SELECT COUNT(*) :
    # 1. dbo.order_items est vide
    # 2. dbo.orders contient des commandes
    # 3. dbo.products contient des produits
    # 4. dbo.order_items contient 2 lignes apres INSERT
    cursor.fetchone.side_effect = [
        (0,),
        (99441,),
        (32951,),
        (2,),
    ]

    with (
        patch.object(
            load_order_items.pd,
            "read_csv",
            return_value=sample_order_items(),
        ),
        patch.object(
            load_order_items.pyodbc,
            "drivers",
            return_value=["ODBC Driver 18 for SQL Server"],
        ),
        patch.object(
            load_order_items.pyodbc,
            "connect",
            return_value=connection,
        ) as mock_connect,
    ):
        load_order_items.main()

    # La connexion simulee est ouverte une seule fois.
    mock_connect.assert_called_once()

    # Les requetes COUNT sont executees dans l'ordre.
    assert cursor.execute.call_args_list == [
        call("SELECT COUNT(*) FROM dbo.order_items"),
        call("SELECT COUNT(*) FROM dbo.orders"),
        call("SELECT COUNT(*) FROM dbo.products"),
        call("SELECT COUNT(*) FROM dbo.order_items"),
    ]

    # Deux articles envoyes dans un seul lot.
    cursor.executemany.assert_called_once()

    insert_sql, rows = cursor.executemany.call_args.args

    assert "INSERT INTO dbo.order_items" in insert_sql
    assert len(rows) == 2

    # Cle primaire composite :
    # une meme commande peut avoir plusieurs articles.
    assert rows[0][0] == "a" * 32
    assert rows[1][0] == "a" * 32
    assert rows[0][1] == 1
    assert rows[1][1] == 2
    assert isinstance(rows[0][1], int)

    # Date compatible avec pyodbc.
    assert isinstance(rows[0][4], datetime)

    # Montants financiers exacts.
    assert rows[0][5] == Decimal("58.90")
    assert rows[0][6] == Decimal("0.00")
    assert rows[1][5] == Decimal("120.00")
    assert rows[1][6] == Decimal("15.50")

    assert isinstance(rows[0][5], Decimal)
    assert isinstance(rows[1][6], Decimal)

    # Transaction reussie.
    connection.commit.assert_called_once()
    connection.rollback.assert_not_called()

    # Connexion toujours fermee.
    connection.close.assert_called_once()
