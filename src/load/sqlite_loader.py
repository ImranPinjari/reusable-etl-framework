import sqlite3
from pathlib import Path

import pandas as pd


class SQLiteLoader:

    def __init__(self, db_path: str = "data/output/etl_database.db"):
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)

    def create_table(self):
        """Create the customers table if it does not exist."""

        with sqlite3.connect(self.db_path) as connection:
            connection.execute("""
                CREATE TABLE IF NOT EXISTS customers (
                    customer_id INTEGER PRIMARY KEY,
                    name TEXT NOT NULL,
                    email TEXT NOT NULL,
                    city TEXT NOT NULL,
                    registration_date TEXT NOT NULL,
                    source_file TEXT,
                    source_record_number INTEGER,
                    run_id TEXT
                )
            """)

    def load(self, df: pd.DataFrame) -> int:
        """Load customer records and return newly inserted row count."""

        if df.empty:
            return 0

        self.create_table()

        columns = [
            "customer_id",
            "name",
            "email",
            "city",
            "registration_date",
            "source_file",
            "source_record_number",
            "run_id"
        ]

        records = df[columns].copy()

        records = records.astype(object).where(
            pd.notna(records), None
        )

        placeholders = ", ".join(["?"] * len(columns))
        column_names = ", ".join(columns)

        query = f"""
            INSERT OR IGNORE INTO customers ({column_names})
            VALUES ({placeholders})
        """

        with sqlite3.connect(self.db_path) as connection:

            before_changes = connection.total_changes

            connection.executemany(
                query,
                records.itertuples(index=False, name=None)
            )

            inserted_count = (
                connection.total_changes - before_changes
            )

        return inserted_count
