import pandas as pd
import pytest

from src.validation.business_validator import BusinessValidator
from src.validation.orders_validator import OrdersValidator
from src.validation.schema_validator import SchemaValidator


def test_customer_validation_accepts_valid_record():
    df = pd.DataFrame({
        "customer_id": [1],
        "name": ["Imran"],
        "email": ["imran@example.com"],
        "city": ["Pune"],
        "registration_date": ["2026-01-10"]
    })

    valid, rejected = BusinessValidator().validate(df)

    assert len(valid) == 1
    assert len(rejected) == 0


def test_customer_validation_rejects_invalid_email():
    df = pd.DataFrame({
        "customer_id": [1],
        "name": ["Imran"],
        "email": ["invalid-email"],
        "city": ["Pune"],
        "registration_date": ["2026-01-10"]
    })

    valid, rejected = BusinessValidator().validate(df)

    assert len(valid) == 0
    assert len(rejected) == 1
    assert "Invalid email" in rejected.iloc[0]["rejection_reason"]


def test_customer_validation_rejects_duplicate_ids():
    df = pd.DataFrame({
        "customer_id": [1, 1],
        "name": ["Imran", "Rahul"],
        "email": ["imran@example.com", "rahul@example.com"],
        "city": ["Pune", "Mumbai"],
        "registration_date": ["2026-01-10", "2026-01-11"]
    })

    valid, rejected = BusinessValidator().validate(df)

    assert len(valid) == 1
    assert len(rejected) == 1
    assert "Duplicate customer_id" in rejected.iloc[0]["rejection_reason"]


def test_customer_validation_rejects_missing_values():
    df = pd.DataFrame({
        "customer_id": [None],
        "name": [None],
        "email": [None],
        "city": [None],
        "registration_date": [None]
    })

    valid, rejected = BusinessValidator().validate(df)

    assert len(valid) == 0
    assert len(rejected) == 1
    assert "Missing customer_id" in rejected.iloc[0]["rejection_reason"]


def test_orders_validation_accepts_valid_order():
    df = pd.DataFrame({
        "order_id": [1001],
        "customer_id": [1],
        "order_date": ["2026-06-10"],
        "amount": [1500.50],
        "status": ["completed"]
    })

    valid, rejected = OrdersValidator().validate(df, {1})

    assert len(valid) == 1
    assert len(rejected) == 0


def test_orders_validation_rejects_unknown_customer():
    df = pd.DataFrame({
        "order_id": [1001],
        "customer_id": [99],
        "order_date": ["2026-06-10"],
        "amount": [1500.50],
        "status": ["completed"]
    })

    valid, rejected = OrdersValidator().validate(df, {1})

    assert len(valid) == 0
    assert len(rejected) == 1
    assert "Customer does not exist" in rejected.iloc[0]["rejection_reason"]


def test_orders_validation_rejects_invalid_amount():
    df = pd.DataFrame({
        "order_id": [1001],
        "customer_id": [1],
        "order_date": ["2026-06-10"],
        "amount": [0],
        "status": ["completed"]
    })

    valid, rejected = OrdersValidator().validate(df, {1})

    assert len(valid) == 0
    assert len(rejected) == 1
    assert "Invalid order amount" in rejected.iloc[0]["rejection_reason"]


def test_orders_validation_rejects_invalid_status():
    df = pd.DataFrame({
        "order_id": [1001],
        "customer_id": [1],
        "order_date": ["2026-06-10"],
        "amount": [500],
        "status": ["unknown"]
    })

    valid, rejected = OrdersValidator().validate(df, {1})

    assert len(valid) == 0
    assert len(rejected) == 1
    assert "Invalid order status" in rejected.iloc[0]["rejection_reason"]


def test_schema_validation_rejects_missing_columns():
    df = pd.DataFrame({
        "customer_id": [1],
        "name": ["Imran"]
    })

    schema = {
        "dataset": "customers",
        "required_columns": [
            "customer_id",
            "name",
            "email",
            "city",
            "registration_date"
        ]
    }

    with pytest.raises(ValueError, match="Missing required columns"):
        SchemaValidator().validate(df, schema)


def test_schema_validation_rejects_empty_input():
    df = pd.DataFrame(columns=["customer_id", "name"])

    schema = {
        "dataset": "customers",
        "required_columns": ["customer_id", "name"]
    }

    with pytest.raises(ValueError, match="Input DataFrame is empty"):
        SchemaValidator().validate(df, schema)
