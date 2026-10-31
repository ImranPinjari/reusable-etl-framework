# ETL Performance Benchmark Report

## Environment
- Language: Python 3.12.4
- Data processing: Pandas
- Database: SQLite
- Operating environment: Windows

## Benchmark results

| Metric | Customers | Orders |
|---|---:|---:|
| Input records | 100,000 | 200,000 |
| Valid records | 100,000 | 200,000 |
| Rejected records | 0 | 0 |
| Loaded records | 100,000 | 200,000 |
| Execution time | 1.3929 seconds | 3.1239 seconds |

Combined execution time: 4.5168 seconds.

## Data integrity verification

- Customers loaded: 100,000
- Orders loaded: 200,000
- Invalid customer references: 0
- Total records loaded: 300,000

## Observations

1. Both datasets were processed successfully.
2. All generated records passed validation.
3. All valid records were loaded into SQLite.
4. No invalid order-to-customer references were found.
5. The pipeline recorded execution time and record counts.
6. Duplicate prevention was separately verified through automated tests.

## Limitations

- Results represent a local synthetic-data benchmark.
- Performance depends on hardware, storage, and dataset characteristics.
- This benchmark does not establish production-scale throughput.
