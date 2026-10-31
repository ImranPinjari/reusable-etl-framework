import pandas as pd


class OrdersValidator:

    ALLOWED_STATUSES = {"completed", "pending", "cancelled"}

    def validate(
        self,
        df: pd.DataFrame,
        customer_ids: set
    ):
        """
        Validate orders and separate valid and rejected records.
        """

        df = df.copy()

        reasons = pd.Series("", index=df.index, dtype="object")

        # 1. Validate order ID
        missing_id = df["order_id"].isna()
        reasons.loc[missing_id] += "Missing order_id; "

        duplicate_id = (
            df["order_id"].notna()
            & df["order_id"].duplicated(keep="first")
        )
        reasons.loc[duplicate_id] += "Duplicate order_id; "

        # 2. Validate customer ID
        missing_customer = df["customer_id"].isna()
        reasons.loc[missing_customer] += "Missing customer_id; "

        unknown_customer = (
            df["customer_id"].notna()
            & ~df["customer_id"].isin(customer_ids)
        )
        reasons.loc[unknown_customer] += "Customer does not exist; "

        # 3. Validate order date
        parsed_dates = pd.to_datetime(
            df["order_date"],
            errors="coerce"
        )

        invalid_date = parsed_dates.isna()
        reasons.loc[invalid_date] += "Invalid order_date; "

        # 4. Validate amount
        numeric_amount = pd.to_numeric(
            df["amount"],
            errors="coerce"
        )

        invalid_amount = (
            numeric_amount.isna()
            | (numeric_amount <= 0)
        )
        reasons.loc[invalid_amount] += "Invalid order amount; "

        # 5. Validate order status
        normalized_status = (
            df["status"].astype("string").str.strip().str.lower()
        )

        invalid_status = ~normalized_status.isin(
            self.ALLOWED_STATUSES
        )

        reasons.loc[invalid_status] += "Invalid order status; "

        # Separate valid and rejected records
        valid_mask = reasons.eq("")

        valid_records = df.loc[valid_mask].copy()
        rejected_records = df.loc[~valid_mask].copy()

        rejected_records["rejection_reason"] = (
            reasons.loc[~valid_mask].str.rstrip("; ")
        )

        return valid_records, rejected_records