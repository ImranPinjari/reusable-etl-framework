from pathlib import Path

import pandas as pd


class CSVExtractor:

    def extract(self, file_path: str, run_id: str) -> pd.DataFrame:
        """
        Extract records from a CSV file and attach tracking information.
        """

        path = Path(file_path)

        # 1. Check whether the file exists
        if not path.exists():
            raise FileNotFoundError(f"CSV file not found: {path}")

        # 2. Check whether the path is a file
        if not path.is_file():
            raise ValueError(f"Path is not a file: {path}")

        # 3. Read the CSV file
        try:
            df = pd.read_csv(path)

        except pd.errors.EmptyDataError:
            raise ValueError(f"CSV file is empty: {path}")

        except pd.errors.ParserError as error:
            raise ValueError(f"Unable to parse CSV file: {error}") from error

        # 4. Attach source tracking information
        df["source_file"] = path.name
        df["source_record_number"] = range(1, len(df) + 1)
        df["run_id"] = run_id

        return df