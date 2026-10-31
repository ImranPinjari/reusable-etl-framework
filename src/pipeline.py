import sqlite3
from pathlib import Path

import pandas as pd

from src.extract.csv_extractor import CSVExtractor
from src.utils.config_loader import ConfigLoader
from src.validation.schema_validator import SchemaValidator
from src.validation.business_validator import BusinessValidator
from src.validation.orders_validator import OrdersValidator
from src.transform.transformer import DataTransformer
from src.transform.orders_transformer import OrdersTransformer
from src.load.sqlite_loader import SQLiteLoader
from src.load.orders_loader import OrdersLoader
from src.monitoring.logger import get_logger
from src.monitoring.metrics import PipelineMetrics


class ETLPipeline:

    def __init__(self, db_path="data/output/etl_database.db"):
        self.db_path = Path(db_path)

        self.extractor = CSVExtractor()
        self.config_loader = ConfigLoader()
        self.schema_validator = SchemaValidator()

        self.business_validator = BusinessValidator()
        self.orders_validator = OrdersValidator()

        self.customer_transformer = DataTransformer()
        self.orders_transformer = OrdersTransformer()

        self.customer_loader = SQLiteLoader(str(self.db_path))
        self.orders_loader = OrdersLoader(str(self.db_path))

        self.logger = get_logger()
        self.metrics = PipelineMetrics()

    def _get_customer_ids(self):
        if not self.db_path.exists():
            raise ValueError(
                "Customer database does not exist. "
                "Run the customers pipeline first."
            )

        try:
            with sqlite3.connect(self.db_path) as connection:
                rows = connection.execute(
                    "SELECT customer_id FROM customers"
                ).fetchall()

            return {row[0] for row in rows}

        except sqlite3.OperationalError as error:
            raise ValueError(
                "Customers table is missing. "
                "Run the customers pipeline first."
            ) from error

    def run(
        self,
        file_path: str,
        run_id: str,
        dataset_name: str = None
    ):

        dataset_name = (
            dataset_name or Path(file_path).stem.lower()
        )

        if dataset_name not in {"customers", "orders"}:
            raise ValueError(
                f"Unsupported dataset: {dataset_name}"
            )

        self.metrics.start()

        self.logger.info(
            f"Pipeline started | Dataset: {dataset_name} | "
            f"Run ID: {run_id}"
        )

        try:
            # 1. Extraction
            self.logger.info("Starting data extraction")

            extracted_data = self.extractor.extract(
                file_path,
                run_id
            )

            total_records = len(extracted_data)

            self.logger.info(
                f"Extraction completed | Records: {total_records}"
            )

            # 2. Load dataset schema
            schema = self.config_loader.get_dataset_schema(
                dataset_name
            )

            # 3. Schema validation
            self.logger.info("Starting schema validation")

            self.schema_validator.validate(
                extracted_data,
                schema
            )

            # 4. Dataset-specific validation and transformation
            if dataset_name == "customers":

                self.logger.info("Starting customer validation")

                valid_records, rejected_records = (
                    self.business_validator.validate(
                        extracted_data
                    )
                )

                self.logger.info(
                    "Starting customer transformation"
                )

                transformed_data = (
                    self.customer_transformer.transform(
                        valid_records
                    )
                )

                loader = self.customer_loader

            else:

                self.logger.info("Loading existing customer IDs")

                customer_ids = self._get_customer_ids()

                self.logger.info("Starting orders validation")

                valid_records, rejected_records = (
                    self.orders_validator.validate(
                        extracted_data,
                        customer_ids
                    )
                )

                self.logger.info(
                    "Starting orders transformation"
                )

                transformed_data = (
                    self.orders_transformer.transform(
                        valid_records
                    )
                )

                loader = self.orders_loader

            # 5. Database loading
            self.logger.info("Starting database loading")

            loaded_records = loader.load(transformed_data)

            # 6. Save rejected records
            if not rejected_records.empty:

                rejected_path = Path(
                    f"data/output/rejected_{dataset_name}.csv"
                )

                rejected_path.parent.mkdir(
                    parents=True,
                    exist_ok=True
                )

                write_header = not rejected_path.exists()

                rejected_records.to_csv(
                    rejected_path,
                    mode="a",
                    index=False,
                    header=write_header
                )

            # 7. Record metrics
            self.metrics.record_counts(
                total=total_records,
                valid=len(valid_records),
                rejected=len(rejected_records),
                loaded=loaded_records
            )

            # 8. Reconciliation
            if total_records != (
                len(valid_records) + len(rejected_records)
            ):
                raise RuntimeError(
                    "Record reconciliation failed"
                )

            self.metrics.finish()
            summary = self.metrics.get_summary()

            self.logger.info(
                f"Pipeline completed successfully | "
                f"Dataset: {dataset_name} | Run ID: {run_id}"
            )

            self.logger.info(f"Pipeline metrics: {summary}")

            return summary

        except Exception:

            self.metrics.finish()

            self.logger.exception(
                f"Pipeline failed | Dataset: {dataset_name} | "
                f"Run ID: {run_id}"
            )

            raise
