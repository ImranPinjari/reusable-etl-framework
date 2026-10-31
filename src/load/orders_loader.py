import sqlite3
from pathlib import Path

import pandas as pd


class OrdersLoader:

    def __init__(self, db_path="data/output/etl_database.db"):
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)

    def create_table(self):
        """Create orders table with customer foreign key."""

        with sqlite3.connect(self.db_path) as connection:
            connection.execute("PRAGMA foreign_keys = ON")

            connection.execute("""
                CREATE TABLE IF NOT EXISTS orders (
                    order_id INTEGER PRIMARY KEY,
                    customer_id INTEGER NOT NULL,
                    order_date TEXT NOT NULL,
                    amount REAL NOT NULL CHECK(amount > 0),
                    status TEXT NOT NULL,
                    source_file TEXT,
                    source_record_number INTEGER,
                    run_id TEXT,
                    FOREIGN KEY (customer_id)
                        REFERENCES customers(customer_id)
                )
            """)

    def load(self, df: pd.DataFrame) -> int:
        """Load transformed orders into SQLite."""

        if df.empty:
            return 0

        self.create_table()

        columns = [
            "order_id",
            "customer_id",
            "order_date",
            "amount",
            "status",
            "source_file",
            "source_record_number",
            "run_id"
        ]

        records = df.copy()

        if "source_file" not in records.columns:
            records["source_file"] = "orders.csv"

        if "source_record_number" not in records.columns:
            records["source_record_number"] = range(1, len(records) + 1)

        if "run_id" not in records.columns:
            records["run_id"] = "UNKNOWN"

        records = records[columns].astype(object).where(
            pd.notna(records[columns]), None
        )

        placeholders = ", ".join(["?"] * len(columns))
        column_names = ", ".join(columns)

        query = f"""
            INSERT OR IGNORE INTO orders ({column_names})
            VALUES ({placeholders})
        """

        with sqlite3.connect(self.db_path) as connection:
            connection.execute("PRAGMA foreign_keys = ON")

            before_changes = connection.total_changes

            connection.executemany(
                query,
                records.itertuples(index=False, name=None)
            )

            inserted_count = (
                connection.total_changes - before_changes
            )

        return inserted_count
