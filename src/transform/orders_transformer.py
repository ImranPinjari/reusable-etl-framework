import pandas as pd


class OrdersTransformer:

    def transform(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Clean and standardize order records.
        """

        transformed_df = df.copy()

        # 1. Standardize order IDs
        transformed_df["order_id"] = pd.to_numeric(
            transformed_df["order_id"],
            errors="raise"
        ).astype("int64")

        # 2. Standardize customer IDs
        transformed_df["customer_id"] = pd.to_numeric(
            transformed_df["customer_id"],
            errors="raise"
        ).astype("int64")

        # 3. Standardize order dates
        transformed_df["order_date"] = pd.to_datetime(
            transformed_df["order_date"],
            errors="raise"
        ).dt.strftime("%Y-%m-%d")

        # 4. Standardize order amounts
        transformed_df["amount"] = pd.to_numeric(
            transformed_df["amount"],
            errors="raise"
        ).round(2)

        # 5. Standardize order status
        transformed_df["status"] = (
            transformed_df["status"]
            .astype("string")
            .str.strip()
            .str.lower()
        )

        return transformed_df