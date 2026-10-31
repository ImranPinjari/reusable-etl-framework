import pandas as pd


class DataTransformer:

    def transform(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Clean and standardize customer records.
        """

        # Work on a copy to preserve the original DataFrame
        transformed_df = df.copy()

        # 1. Remove unnecessary spaces
        transformed_df["name"] = (
            transformed_df["name"].astype("string").str.strip()
        )

        transformed_df["city"] = (
            transformed_df["city"].astype("string").str.strip()
        )

        # 2. Standardize email addresses
        transformed_df["email"] = (
            transformed_df["email"].astype("string").str.strip().str.lower()
        )

        # 3. Standardize registration dates
        transformed_df["registration_date"] = pd.to_datetime(
            transformed_df["registration_date"],
            errors="raise"
        ).dt.strftime("%Y-%m-%d")

        # 4. Standardize customer IDs
        transformed_df["customer_id"] = pd.to_numeric(
            transformed_df["customer_id"],
            errors="raise"
        ).astype("int64")

        return transformed_df