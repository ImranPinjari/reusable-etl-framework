from typing import Dict, Any

import pandas as pd


class SchemaValidator:

    def validate(
        self,
        df: pd.DataFrame,
        schema: Dict[str, Any]
    ) -> None:
        """
        Validate DataFrame structure using a YAML schema.
        """

        # Check whether input DataFrame is empty
        if df.empty:
            raise ValueError("Input DataFrame is empty.")

        # Get required columns from the schema
        required_columns = schema.get("required_columns", [])

        if not required_columns:
            raise ValueError(
                "Schema does not define required_columns."
            )

        # Identify missing columns
        missing_columns = [
            column
            for column in required_columns
            if column not in df.columns
        ]

        if missing_columns:
            raise ValueError(
                f"Missing required columns: {missing_columns}"
            )

        print(
            f"Schema validation successful: {schema.get('dataset', 'unknown')}"
        )
