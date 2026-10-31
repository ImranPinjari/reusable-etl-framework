import sqlite3

import pandas as pd
import pytest

from src.pipeline import ETLPipeline


def create_customer_csv(path):
    df = pd.DataFrame({
        "customer_id": [1, 2],
        "name": ["Imran", "Rahul"],
        "email": ["imran@example.com", "rahul@example.com"],
        "city": ["Pune", "Mumbai"],
        "registration_date": ["2026-01-10", "2026-01-11"]
    })
    df.to_csv(path, index=False)


def create_orders_csv(path):
    df = pd.DataFrame({
        "order_id": [1001, 1002],
        "customer_id": [1, 2],
        "order_date": ["2026-06-10", "2026-06-12"],
        "amount": [1500.50, 2500.00],
        "status": ["completed", "pending"]
    })
    df.to_csv(path, index=False)


def test_customer_pipeline_end_to_end(tmp_path):
    customer_file = tmp_path / "customers.csv"
    db_path = tmp_path / "test.db"

    create_customer_csv(customer_file)

    pipeline = ETLPipeline(db_path=str(db_path))

    result = pipeline.run(
        str(customer_file),
        "TEST_CUSTOMER_001",
        "customers"
    )

    assert result["total_records"] == 2
    assert result["valid_records"] == 2
    assert result["rejected_records"] == 0
    assert result["loaded_records"] == 2

    with sqlite3.connect(db_path) as connection:
        count = connection.execute(
            "SELECT COUNT(*) FROM customers"
        ).fetchone()[0]

    assert count == 2


def test_orders_pipeline_end_to_end(tmp_path):
    customer_file = tmp_path / "customers.csv"
    orders_file = tmp_path / "orders.csv"
    db_path = tmp_path / "test.db"

    create_customer_csv(customer_file)
    create_orders_csv(orders_file)

    customer_pipeline = ETLPipeline(db_path=str(db_path))
    customer_pipeline.run(
        str(customer_file),
        "TEST_CUSTOMER_002",
        "customers"
    )

    orders_pipeline = ETLPipeline(db_path=str(db_path))
    result = orders_pipeline.run(
        str(orders_file),
        "TEST_ORDERS_001",
        "orders"
    )

    assert result["total_records"] == 2
    assert result["valid_records"] == 2
    assert result["rejected_records"] == 0
    assert result["loaded_records"] == 2

    with sqlite3.connect(db_path) as connection:
        count = connection.execute(
            "SELECT COUNT(*) FROM orders"
        ).fetchone()[0]

        invalid_references = connection.execute("""
            SELECT COUNT(*)
            FROM orders o
            LEFT JOIN customers c
            ON o.customer_id = c.customer_id
            WHERE c.customer_id IS NULL
        """).fetchone()[0]

    assert count == 2
    assert invalid_references == 0


def test_customer_pipeline_is_idempotent(tmp_path):
    customer_file = tmp_path / "customers.csv"
    db_path = tmp_path / "test.db"

    create_customer_csv(customer_file)

    first_pipeline = ETLPipeline(db_path=str(db_path))
    first_result = first_pipeline.run(
        str(customer_file),
        "TEST_RERUN_001",
        "customers"
    )

    second_pipeline = ETLPipeline(db_path=str(db_path))
    second_result = second_pipeline.run(
        str(customer_file),
        "TEST_RERUN_002",
        "customers"
    )

    assert first_result["loaded_records"] == 2
    assert second_result["loaded_records"] == 0

    with sqlite3.connect(db_path) as connection:
        count = connection.execute(
            "SELECT COUNT(*) FROM customers"
        ).fetchone()[0]

    assert count == 2


def test_pipeline_rejects_unsupported_dataset(tmp_path):
    pipeline = ETLPipeline(
        db_path=str(tmp_path / "test.db")
    )

    with pytest.raises(ValueError, match="Unsupported dataset"):
        pipeline.run(
            "unknown.csv",
            "TEST_INVALID_001",
            "unknown"
        )
