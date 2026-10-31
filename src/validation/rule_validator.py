import re
import pandas as pd


class RuleValidator:

    def validate(self, df, schema):
        valid_df = df.copy()
        rejected_df = pd.DataFrame()

        rules = schema.get("rules", {})

        for column, rule in rules.items():

            if column not in valid_df.columns:
                continue

            errors = pd.Series("", index=valid_df.index, dtype="object")

            # Null validation
            if not rule.get("nullable", True):
                null_mask = valid_df[column].isna()
                errors.loc[null_mask] = "Missing required value"

            # Data type validation
            data_type = rule.get("type")

            if data_type == "integer":
                converted = pd.to_numeric(
                    valid_df[column], errors="coerce"
                )
                invalid = converted.isna() & valid_df[column].notna()
                errors.loc[invalid] = "Invalid integer value"

            elif data_type == "float":
                converted = pd.to_numeric(
                    valid_df[column], errors="coerce"
                )
                invalid = converted.isna() & valid_df[column].notna()
                errors.loc[invalid] = "Invalid numeric value"

            elif data_type == "email":
                email_mask = valid_df[column].astype("string").str.match(
                    r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$",
                    na=False
                )
                invalid = ~email_mask & valid_df[column].notna()
                errors.loc[invalid] = "Invalid email address"

            elif data_type == "date":
                converted = pd.to_datetime(
                    valid_df[column], errors="coerce"
                )
                invalid = converted.isna() & valid_df[column].notna()
                errors.loc[invalid] = "Invalid date value"

            # Minimum value validation
            if "min" in rule:
                numeric_values = pd.to_numeric(
                    valid_df[column], errors="coerce"
                )
                invalid = numeric_values < rule["min"]
                errors.loc[invalid.fillna(False)] = (
                    f"Value must be at least {rule['min']}"
                )

            # Allowed values validation
            if "allowed_values" in rule:
                allowed = [
                    str(value).strip().lower()
                    for value in rule["allowed_values"]
                ]
                invalid = (
                    ~valid_df[column].astype("string")
                    .str.strip().str.lower().isin(allowed)
                )
                errors.loc[invalid.fillna(False)] = (
                    "Value is not in allowed values"
                )

            failed = errors != ""

            if failed.any():
                rejected_part = valid_df.loc[failed].copy()
                rejected_part["rejection_reason"] = (
                    column + ": " + errors.loc[failed]
                )

                rejected_df = pd.concat(
                    [rejected_df, rejected_part],
                    ignore_index=True
                )

                valid_df = valid_df.loc[~failed].copy()

        return valid_df, rejected_df
