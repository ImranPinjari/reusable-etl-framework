import argparse
from pathlib import Path

import numpy as np
import pandas as pd
from faker import Faker


def generate_data(customer_count=100_000, order_count=200_000, seed=42):
    output_dir = Path("data/generated")
    output_dir.mkdir(parents=True, exist_ok=True)

    fake = Faker()
    Faker.seed(seed)
    rng = np.random.default_rng(seed)

    print(f"Generating {customer_count:,} customers...")

    customer_ids = np.arange(1, customer_count + 1)

    customers = pd.DataFrame({
        "customer_id": customer_ids,
        "name": [fake.name() for _ in range(customer_count)],
        "email": [
            f"customer{i}@example.com"
            for i in customer_ids
        ],
        "city": rng.choice(
            ["Pune", "Mumbai", "Delhi", "Bengaluru", "Hyderabad"],
            size=customer_count
        ),
        "registration_date": (
            pd.Timestamp("2020-01-01")
            + pd.to_timedelta(
                rng.integers(0, 2400, size=customer_count),
                unit="D"
            )
        ).strftime("%Y-%m-%d")
    })

    customer_file = output_dir / "customers_100k.csv"
    customers.to_csv(customer_file, index=False)

    print(f"Generating {order_count:,} orders...")

    order_ids = np.arange(100001, 100001 + order_count)

    orders = pd.DataFrame({
        "order_id": order_ids,
        "customer_id": rng.choice(
            customer_ids,
            size=order_count
        ),
        "order_date": (
            pd.Timestamp("2025-01-01")
            + pd.to_timedelta(
                rng.integers(0, 365, size=order_count),
                unit="D"
            )
        ).strftime("%Y-%m-%d"),
        "amount": np.round(
            rng.uniform(100, 10000, size=order_count),
            2
        ),
        "status": rng.choice(
            ["completed", "pending", "cancelled"],
            size=order_count,
            p=[0.65, 0.20, 0.15]
        )
    })

    orders_file = output_dir / "orders_200k.csv"
    orders.to_csv(orders_file, index=False)

    print("\nData generation completed.")
    print(f"Customers: {len(customers):,} -> {customer_file}")
    print(f"Orders:    {len(orders):,} -> {orders_file}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Generate reproducible ETL benchmark datasets."
    )
    parser.add_argument("--customers", type=int, default=100_000)
    parser.add_argument("--orders", type=int, default=200_000)
    parser.add_argument("--seed", type=int, default=42)

    args = parser.parse_args()

    if args.customers <= 0 or args.orders <= 0:
        parser.error("Record counts must be positive.")

    generate_data(
        customer_count=args.customers,
        order_count=args.orders,
        seed=args.seed
    )
