# Reusable Python ETL Framework

A modular Python ETL framework that extracts CSV datasets, validates data quality, transforms records, loads data into SQLite, and captures execution logs and processing metrics.

The framework demonstrates reusable ETL processing using two related datasets: Customers and Orders.

## Key Features

- Modular extraction, validation, transformation, and loading components.
- Customer and order business validation.
- Separation of valid and rejected records.
- Rejection reasons and source-record traceability.
- SQLite primary-key and foreign-key constraints.
- Duplicate prevention during repeated loads.
- Execution logging and pipeline metrics.
- Synthetic data generation for large-volume testing.
- Automated testing using Pytest.
- Performance benchmarking and reconciliation reports.

## Architecture

```text
CSV Input
    |
    v
Extraction
    |
    v
Schema Validation
    |
    v
Business Validation
    |
    +--------------------+
    |                    |
    v                    v
Valid Records       Rejected Records
    |                    |
    v                    v
Transformation      Rejected CSV
    |
    v
SQLite Loading
    |
    v
Metrics and Reconciliation
```

## Technology Stack

| Technology | Purpose |
|---|---|
| Python 3.12 | Core implementation |
| Pandas | Data processing |
| NumPy | Synthetic data generation |
| PyYAML | Configuration and schema definitions |
| SQLite | Target database |
| Pytest | Automated testing |
| Faker | Synthetic data generation |
| Python logging | Execution logs |

## Project Structure

```text
reusable-etl-framework/
├── config/
│   ├── config.yaml
│   └── schemas/
│       ├── customers.yaml
│       └── orders.yaml
├── data/
│   ├── input/
│   ├── generated/
│   └── output/
├── docs/
│   ├── data_dictionary.md
│   └── design_decisions.md
├── reports/
│   ├── performance_report.md
│   └── reconciliation_report.md
├── scripts/
│   ├── generate_data.py
│   └── run_pipeline.py
├── src/
│   ├── extract/
│   ├── validation/
│   ├── transform/
│   ├── load/
│   ├── monitoring/
│   ├── utils/
│   └── pipeline.py
├── tests/
├── requirements.txt
└── README.md
```

## Dataset Overview

### Customers Dataset

| Field | Description |
|---|---|
| customer_id | Unique customer identifier |
| name | Customer name |
| email | Customer email |
| city | Customer city |
| registration_date | Customer registration date |

### Orders Dataset

| Field | Description |
|---|---|
| order_id | Unique order identifier |
| customer_id | Reference to the customer |
| order_date | Order date |
| amount | Order amount |
| status | Order status |

Orders reference customers through `customer_id`, establishing a one-to-many relationship.

See [Data Dictionary](docs/data_dictionary.md).

## Setup and Installation

### 1. Clone the repository

```bash
git clone https://github.com/ImranPinjari/reusable-etl-framework.git
cd reusable-etl-framework
```

### 2. Create a virtual environment

For Windows:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```bash
python -m pip install -r requirements.txt
```

## Run the ETL Pipeline

Ensure the following sample input files exist:

- `data/input/customers.csv`
- `data/input/orders.csv`

### Run Customers Pipeline

```bash
python -m scripts.run_pipeline
```

### Run Orders Pipeline

Run the customers pipeline first because orders depend on existing customer records.

```bash
python -c "from src.pipeline import ETLPipeline; print(ETLPipeline().run('data/input/orders.csv', 'ORDERS_RUN_001', 'orders'))"
```

The default SQLite database is created under:

`data/output/etl_database.db`

## Generate Synthetic Data

Generate 100,000 customers and 200,000 orders:

```bash
python -m scripts.generate_data --customers 100000 --orders 200000
```

Generate a smaller dataset:

```bash
python -m scripts.generate_data --customers 1000 --orders 2000
```

Generated files are saved under `data/generated/`.

## Automated Testing

Run the complete test suite:

```bash
python -m pytest tests/ -v
```

The test suite covers:

- CSV extraction and metadata generation.
- Missing input files.
- Empty CSV files.
- Malformed CSV input.
- Schema and business validation.
- Missing and duplicate records.
- Invalid email addresses.
- Invalid order amounts and statuses.
- Unknown customer references.
- Data transformations.
- Database loading and duplicate prevention.
- Foreign-key integrity.
- End-to-end pipeline execution.

**Latest verified test result: 28 passed.**

## Performance Benchmark

The framework was tested using synthetic datasets:

| Metric | Customers | Orders |
|---|---:|---:|
| Input records | 100,000 | 200,000 |
| Valid records | 100,000 | 200,000 |
| Rejected records | 0 | 0 |
| Loaded records | 100,000 | 200,000 |
| Execution time | 1.3929 seconds | 3.1239 seconds |

**Combined measured execution time: 4.5168 seconds.**

Benchmark environment:

- Python 3.12.4
- Pandas
- SQLite
- Windows

These measurements represent local synthetic-data benchmark results and are not a production throughput guarantee.

See [Performance Report](reports/performance_report.md).

## Data Quality and Reconciliation

The framework separates invalid records from valid records and captures rejection reasons.

Reconciliation checks include:

- Extracted records = valid records + rejected records.
- Valid records are accounted for during database loading.
- Customer and order relationships maintain referential integrity.
- Repeated loading does not create duplicate database records.

See [Reconciliation Report](reports/reconciliation_report.md).

## Logging and Monitoring

Execution logs are written to:

`logs/etl_pipeline.log`

Pipeline metrics include:

- Total records.
- Valid records.
- Rejected records.
- Loaded records.
- Execution time.

## Idempotency and Recovery

Primary keys and `INSERT OR IGNORE` loading prevent duplicate database entries during repeated processing.

Failed executions are logged and raised to the caller. After correcting an input or database issue, the pipeline can be rerun.

Automatic retry scheduling, checkpoint-based recovery, and automated backfill orchestration are not currently implemented.

## Design Decisions and Limitations

Customer and order business rules are implemented in Python. YAML files provide dataset metadata and required-column definitions.

Current limitations:

- CSV is the implemented source format.
- SQLite is the target database.
- Not all declared YAML validation rules are dynamically executed.
- Configured batch size is not currently used for chunk-based processing.
- Pipeline metrics are logged rather than persisted in a dedicated metrics table.
- Automated retries and checkpoint-based recovery are future enhancements.

See [Design Decisions](docs/design_decisions.md).

## Future Enhancements

- Configurable chunk-based processing.
- Fully YAML-driven validation.
- Persistent pipeline execution history and metrics.
- Automated retries and checkpoint recovery.
- Additional source and target database connectors.
- Workflow scheduling and monitoring.
- Distributed processing for larger datasets.

## Author

**Imran Pinjari**
