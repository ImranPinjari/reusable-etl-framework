import pandas as pd


class IntegrityValidator:

    def validate_orders(self, orders, customers):
        valid = orders.copy()
        rejected = pd.DataFrame()

        # 1. Detect duplicate order IDs
        duplicate_mask = valid.duplicated(
            subset=["order_id"], keep="first"
        )

        if duplicate_mask.any():
            duplicate_records = valid.loc[duplicate_mask].copy()
            duplicate_records["rejection_reason"] = (
                "Duplicate order_id"
            )

            rejected = pd.concat(
                [rejected, duplicate_records],
                ignore_index=True
            )

            valid = valid.loc[~duplicate_mask].copy()

        # 2. Validate customer foreign keys
        customer_ids = set(customers["customer_id"].dropna())

        invalid_fk = ~valid["customer_id"].isin(customer_ids)

        if invalid_fk.any():
            invalid_records = valid.loc[invalid_fk].copy()
            invalid_records["rejection_reason"] = (
                "Customer ID does not exist"
            )

            rejected = pd.concat(
                [rejected, invalid_records],
                ignore_index=True
            )

            valid = valid.loc[~invalid_fk].copy()

        return valid, rejected
