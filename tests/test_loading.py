import sqlite3

import pandas as pd
import pytest

from src.load.sqlite_loader import SQLiteLoader
from src.load.orders_loader import OrdersLoader


def test_customer_loader_inserts_records(tmp_path):
    db_path = tmp_path / "test.db"
    loader = SQLiteLoader(str(db_path))

    df = pd.DataFrame({
        "customer_id": [1],
        "name": ["Imran"],
        "email": ["imran@example.com"],
        "city": ["Pune"],
        "registration_date": ["2026-01-10"],
        "source_file": ["customers.csv"],
        "source_record_number": [1],
        "run_id": ["TEST001"]
    })

    inserted = loader.load(df)

    assert inserted == 1

    with sqlite3.connect(db_path) as connection:
        count = connection.execute(
            "SELECT COUNT(*) FROM customers"
        ).fetchone()[0]

    assert count == 1


def test_customer_loader_prevents_duplicate_insertion(tmp_path):
    db_path = tmp_path / "test.db"
    loader = SQLiteLoader(str(db_path))

    df = pd.DataFrame({
        "customer_id": [1],
        "name": ["Imran"],
        "email": ["imran@example.com"],
        "city": ["Pune"],
        "registration_date": ["2026-01-10"],
        "source_file": ["customers.csv"],
        "source_record_number": [1],
        "run_id": ["TEST001"]
    })

    first_insert = loader.load(df)
    second_insert = loader.load(df)

    assert first_insert == 1
    assert second_insert == 0

    with sqlite3.connect(db_path) as connection:
        count = connection.execute(
            "SELECT COUNT(*) FROM customers"
        ).fetchone()[0]

    assert count == 1


def test_orders_loader_inserts_valid_order(tmp_path):
    db_path = tmp_path / "test.db"

    customer_loader = SQLiteLoader(str(db_path))
    customer_loader.load(pd.DataFrame({
        "customer_id": [1],
        "name": ["Imran"],
        "email": ["imran@example.com"],
        "city": ["Pune"],
        "registration_date": ["2026-01-10"],
        "source_file": ["customers.csv"],
        "source_record_number": [1],
        "run_id": ["TEST001"]
    }))

    orders_loader = OrdersLoader(str(db_path))

    df = pd.DataFrame({
        "order_id": [1001],
        "customer_id": [1],
        "order_date": ["2026-06-10"],
        "amount": [1500.50],
        "status": ["completed"],
        "source_file": ["orders.csv"],
        "source_record_number": [1],
        "run_id": ["TEST002"]
    })

    inserted = orders_loader.load(df)

    assert inserted == 1

    with sqlite3.connect(db_path) as connection:
        count = connection.execute(
            "SELECT COUNT(*) FROM orders"
        ).fetchone()[0]

    assert count == 1


def test_orders_loader_prevents_duplicate_insertion(tmp_path):
    db_path = tmp_path / "test.db"

    customer_loader = SQLiteLoader(str(db_path))
    customer_loader.load(pd.DataFrame({
        "customer_id": [1],
        "name": ["Imran"],
        "email": ["imran@example.com"],
        "city": ["Pune"],
        "registration_date": ["2026-01-10"],
        "source_file": ["customers.csv"],
        "source_record_number": [1],
        "run_id": ["TEST001"]
    }))

    orders_loader = OrdersLoader(str(db_path))

    df = pd.DataFrame({
        "order_id": [1001],
        "customer_id": [1],
        "order_date": ["2026-06-10"],
        "amount": [1500.50],
        "status": ["completed"],
        "source_file": ["orders.csv"],
        "source_record_number": [1],
        "run_id": ["TEST002"]
    })

    first_insert = orders_loader.load(df)
    second_insert = orders_loader.load(df)

    assert first_insert == 1
    assert second_insert == 0

    with sqlite3.connect(db_path) as connection:
        count = connection.execute(
            "SELECT COUNT(*) FROM orders"
        ).fetchone()[0]

    assert count == 1


def test_orders_loader_rejects_invalid_foreign_key(tmp_path):
    db_path = tmp_path / "test.db"

    customer_loader = SQLiteLoader(str(db_path))
    customer_loader.create_table()

    orders_loader = OrdersLoader(str(db_path))

    df = pd.DataFrame({
        "order_id": [1001],
        "customer_id": [999],
        "order_date": ["2026-06-10"],
        "amount": [1500.50],
        "status": ["completed"],
        "source_file": ["orders.csv"],
        "source_record_number": [1],
        "run_id": ["TEST003"]
    })

    with pytest.raises(sqlite3.IntegrityError):
        orders_loader.load(df)
