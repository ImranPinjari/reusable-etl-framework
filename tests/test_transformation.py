import pandas as pd

from src.transform.transformer import DataTransformer
from src.transform.orders_transformer import OrdersTransformer


def test_customer_transformation_standardizes_values():
    df = pd.DataFrame({
        "customer_id": ["1"],
        "name": [" Imran "],
        "email": [" IMRAN@EXAMPLE.COM "],
        "city": [" Pune "],
        "registration_date": ["2026-01-10"]
    })

    result = DataTransformer().transform(df)

    assert result.iloc[0]["customer_id"] == 1
    assert result.iloc[0]["name"] == "Imran"
    assert result.iloc[0]["email"] == "imran@example.com"
    assert result.iloc[0]["city"] == "Pune"
    assert result.iloc[0]["registration_date"] == "2026-01-10"


def test_customer_transformation_preserves_original_data():
    df = pd.DataFrame({
        "customer_id": ["1"],
        "name": [" Imran "],
        "email": [" IMRAN@EXAMPLE.COM "],
        "city": [" Pune "],
        "registration_date": ["2026-01-10"]
    })

    DataTransformer().transform(df)

    assert df.iloc[0]["name"] == " Imran "
    assert df.iloc[0]["email"] == " IMRAN@EXAMPLE.COM "


def test_orders_transformation_standardizes_values():
    df = pd.DataFrame({
        "order_id": ["1001"],
        "customer_id": ["1"],
        "order_date": ["2026-06-10"],
        "amount": ["1500.567"],
        "status": [" COMPLETED "]
    })

    result = OrdersTransformer().transform(df)

    assert result.iloc[0]["order_id"] == 1001
    assert result.iloc[0]["customer_id"] == 1
    assert result.iloc[0]["order_date"] == "2026-06-10"
    assert result.iloc[0]["amount"] == 1500.57
    assert result.iloc[0]["status"] == "completed"


def test_orders_transformation_preserves_original_data():
    df = pd.DataFrame({
        "order_id": ["1001"],
        "customer_id": ["1"],
        "order_date": ["2026-06-10"],
        "amount": ["1500.50"],
        "status": [" COMPLETED "]
    })

    OrdersTransformer().transform(df)

    assert df.iloc[0]["status"] == " COMPLETED "
    assert df.iloc[0]["amount"] == "1500.50"
