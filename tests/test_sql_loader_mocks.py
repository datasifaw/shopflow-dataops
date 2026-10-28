
from unittest.mock import MagicMock, patch

import pandas as pd
import pytest

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


def mock_database(*counts):
    """
    Prepare une fausse connexion SQL Server.

    Chaque COUNT correspond a un fetchone()
    execute par le chargeur.
    """
    connection = MagicMock()
    cursor = connection.cursor.return_value

    cursor.fetchone.side_effect = [
        (count,) for count in counts
    ]

    return connection, cursor


def run_loader_with_mocks(loader, dataframe, connection):
    """
    Execute main() avec lecture CSV et connexion
    SQL Server entierement simulees.
    """
    with (
        patch.object(
            loader.pd,
            "read_csv",
            return_value=dataframe,
        ),
        patch.object(
            loader.pyodbc,
            "drivers",
            return_value=["ODBC Driver 18 for SQL Server"],
        ),
        patch.object(
            loader.pyodbc,
            "connect",
            return_value=connection,
        ) as mock_connect,
    ):
        loader.main()

    mock_connect.assert_called_once()


# =========================================================
# ORDERS
# =========================================================

def test_orders_loader_refuses_existing_data():
    connection, cursor = mock_database(99441)

    with pytest.raises(
        RuntimeError,
        match="Chargement refuse",
    ):
        run_loader_with_mocks(
            load_orders,
            sample_orders(),
            connection,
        )

    cursor.executemany.assert_not_called()
    connection.rollback.assert_called_once()
    connection.commit.assert_not_called()
    connection.close.assert_called_once()


def test_orders_loader_rolls_back_on_insert_error():
    # Orders est vide ; Customers est deja charge.
    connection, cursor = mock_database(0, 99441)

    cursor.executemany.side_effect = RuntimeError(
        "Erreur SQL simulee pendant INSERT"
    )

    with pytest.raises(
        RuntimeError,
        match="Erreur SQL simulee",
    ):
        run_loader_with_mocks(
            load_orders,
            sample_orders(),
            connection,
        )

    cursor.executemany.assert_called_once()
    connection.rollback.assert_called_once()
    connection.commit.assert_not_called()
    connection.close.assert_called_once()


# =========================================================
# PRODUCTS
# =========================================================

def test_products_loader_refuses_existing_data():
    connection, cursor = mock_database(32951)

    with pytest.raises(
        RuntimeError,
        match="Chargement refuse",
    ):
        run_loader_with_mocks(
            load_products,
            sample_products(),
            connection,
        )

    cursor.executemany.assert_not_called()
    connection.rollback.assert_called_once()
    connection.commit.assert_not_called()
    connection.close.assert_called_once()


def test_products_loader_rolls_back_on_insert_error():
    # Products est vide.
    connection, cursor = mock_database(0)

    cursor.executemany.side_effect = RuntimeError(
        "Erreur SQL simulee pendant INSERT"
    )

    with pytest.raises(
        RuntimeError,
        match="Erreur SQL simulee",
    ):
        run_loader_with_mocks(
            load_products,
            sample_products(),
            connection,
        )

    cursor.executemany.assert_called_once()
    connection.rollback.assert_called_once()
    connection.commit.assert_not_called()
    connection.close.assert_called_once()


# =========================================================
# ORDER ITEMS
# =========================================================

def test_order_items_loader_refuses_existing_data():
    # La table contient deja 112650 articles.
    connection, cursor = mock_database(112650)

    with pytest.raises(
        RuntimeError,
        match="Chargement refuse",
    ):
        run_loader_with_mocks(
            load_order_items,
            sample_order_items(),
            connection,
        )

    cursor.executemany.assert_not_called()
    connection.rollback.assert_called_once()
    connection.commit.assert_not_called()
    connection.close.assert_called_once()


def test_order_items_loader_requires_orders():
    # Order Items est vide, mais Orders est vide aussi.
    connection, cursor = mock_database(0, 0)

    with pytest.raises(
        RuntimeError,
        match="Charger orders avant order_items",
    ):
        run_loader_with_mocks(
            load_order_items,
            sample_order_items(),
            connection,
        )

    cursor.executemany.assert_not_called()
    connection.rollback.assert_called_once()
    connection.commit.assert_not_called()
    connection.close.assert_called_once()


def test_order_items_loader_requires_products():
    # Order Items vide, Orders charge, Products vide.
    connection, cursor = mock_database(0, 99441, 0)

    with pytest.raises(
        RuntimeError,
        match="Charger products avant order_items",
    ):
        run_loader_with_mocks(
            load_order_items,
            sample_order_items(),
            connection,
        )

    cursor.executemany.assert_not_called()
    connection.rollback.assert_called_once()
    connection.commit.assert_not_called()
    connection.close.assert_called_once()


def test_order_items_loader_rolls_back_on_insert_error():
    # Tables parentes chargees et Order Items vide.
    connection, cursor = mock_database(
        0,
        99441,
        32951,
    )

    cursor.executemany.side_effect = RuntimeError(
        "Erreur SQL simulee pendant INSERT"
    )

    with pytest.raises(
        RuntimeError,
        match="Erreur SQL simulee",
    ):
        run_loader_with_mocks(
            load_order_items,
            sample_order_items(),
            connection,
        )

    cursor.executemany.assert_called_once()
    connection.rollback.assert_called_once()
    connection.commit.assert_not_called()
    connection.close.assert_called_once()
