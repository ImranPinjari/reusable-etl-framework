import pandas as pd


class BusinessValidator:

    def validate(self, df: pd.DataFrame):
        """
        Validate customer records and separate valid and rejected records.
        """

        df = df.copy()

        # Store rejection reasons for each record
        rejection_reasons = pd.Series("", index=df.index, dtype="object")

        # 1. Validate customer ID
        missing_id = df["customer_id"].isna()
        rejection_reasons.loc[missing_id] += "Missing customer_id; "

        # 2. Validate duplicate customer IDs
        duplicate_id = (
            df["customer_id"].notna()
            & df["customer_id"].duplicated(keep="first")
        )
        rejection_reasons.loc[duplicate_id] += "Duplicate customer_id; "

        # 3. Validate customer name
        missing_name = (
            df["name"].isna()
            | df["name"].astype(str).str.strip().eq("")
        )
        rejection_reasons.loc[missing_name] += "Missing name; "

        # 4. Validate email format
        email_pattern = r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$"

        invalid_email = (
            df["email"].isna()
            | ~df["email"].astype(str).str.strip().str.match(email_pattern)
        )
        rejection_reasons.loc[invalid_email] += "Invalid email; "

        # 5. Validate city
        missing_city = (
            df["city"].isna()
            | df["city"].astype(str).str.strip().eq("")
        )
        rejection_reasons.loc[missing_city] += "Missing city; "

        # 6. Validate registration date
        parsed_dates = pd.to_datetime(
            df["registration_date"],
            errors="coerce"
        )

        invalid_date = parsed_dates.isna()
        rejection_reasons.loc[invalid_date] += "Invalid registration_date; "

        # Separate valid and rejected records
        valid_mask = rejection_reasons.eq("")

        valid_records = df.loc[valid_mask].copy()
        rejected_records = df.loc[~valid_mask].copy()

        # Attach rejection reasons
        rejected_records["rejection_reason"] = (
            rejection_reasons.loc[~valid_mask].str.rstrip("; ")
        )

        return valid_records, rejected_records