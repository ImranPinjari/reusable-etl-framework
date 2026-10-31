# ETL Framework - Design Decisions

## 1. Architecture

The framework follows a modular ETL architecture:

1. Extract records from CSV files.
2. Validate required columns and dataset-specific business rules.
3. Separate valid and rejected records.
4. Transform valid records into standardized formats.
5. Load records into SQLite.
6. Record execution logs and pipeline metrics.
7. Verify record counts and data integrity.

## 2. Technology Choices

| Technology | Purpose |
|---|---|
| Python | Core ETL implementation |
| Pandas | Data extraction, validation, and transformation |
| SQLite | Relational target database |
| PyYAML | Configuration and schema definitions |
| Pytest | Automated testing |
| Faker | Synthetic test-data generation |
| NumPy | Efficient generation of numeric data |
| Python logging | Pipeline execution logs |

## 3. Key Design Decisions

### Modular components
Extraction, validation, transformation, loading, and monitoring are maintained in separate modules. This makes the framework easier to test, maintain, and extend.

### Dataset-specific validation
Customers and orders have separate business validation logic because their data-quality rules differ.

### Data quarantine
Invalid records are separated from valid records and written to rejected-record CSV files with rejection reasons and source metadata.

### Relational integrity
SQLite primary-key and foreign-key constraints protect relationships between customers and orders.

### Idempotent loading
Primary keys and INSERT OR IGNORE loading prevent duplicate database entries when the same records are processed again.

### Execution traceability
The pipeline attaches run IDs, source file names, and source record numbers to extracted records. Execution logs capture record counts and processing time.

### Deterministic transformations
Transformations standardize text, email addresses, dates, numeric identifiers, and order amounts to produce consistent output.

## 4. Error Handling and Recovery

- Missing input files and malformed CSV files are handled by the extraction component.
- Invalid records are quarantined with rejection reasons.
- Database constraints protect primary-key and foreign-key integrity.
- Failed pipeline executions are logged and raised to the caller.
- Safe reruns are supported through duplicate prevention.

Automatic retry scheduling, checkpoint-based recovery, and automated backfill orchestration are not implemented. Recovery can be initiated by rerunning the pipeline after correcting the underlying issue.

## 5. Scalability and Performance

The framework was benchmarked using synthetic datasets containing:
- 100,000 customer records
- 200,000 order records

The measured combined pipeline execution time was 4.5168 seconds in the local test environment.

Pandas operations and SQLite transactions support efficient processing for the demonstrated workload.

For larger production workloads, further improvements could include configurable batch processing, parallel extraction, distributed processing, and a production database.

## 6. Current Limitations

- CSV is the implemented source format.
- SQLite is used as the target database.
- Customer and order business rules are implemented in Python.
- YAML schema files define dataset metadata and required columns; not all declared YAML rules are dynamically executed.
- The configured batch size is not currently used for chunked processing.
- Pipeline metrics are logged rather than persisted in a dedicated database metrics table.
- Automated retry and checkpoint-based restart are future enhancements.
- Benchmark results are based on local synthetic data and are not a production throughput guarantee.

## 7. Future Enhancements

- Add chunk-based processing for larger files.
- Integrate YAML-driven validation rules.
- Persist pipeline execution history and metrics.
- Add configurable retry and checkpoint recovery.
- Support additional source and target systems.
- Add automated scheduling and monitoring.
