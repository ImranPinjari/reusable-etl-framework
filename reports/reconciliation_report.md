# ETL Data Reconciliation Report

## 1. Objective

Verify that extracted records are accounted for during validation and that valid records are successfully loaded into the target database.

## 2. Customer reconciliation

| Metric | Count |
|---|---:|
| Extracted records | 100,000 |
| Valid records | 100,000 |
| Rejected records | 0 |
| Loaded records | 100,000 |

Reconciliation:
Extracted = Valid + Rejected

100,000 = 100,000 + 0

Result: PASSED

## 3. Orders reconciliation

| Metric | Count |
|---|---:|
| Extracted records | 200,000 |
| Valid records | 200,000 |
| Rejected records | 0 |
| Loaded records | 200,000 |

Reconciliation:
Extracted = Valid + Rejected

200,000 = 200,000 + 0

Result: PASSED

## 4. Referential integrity

| Check | Result |
|---|---:|
| Customers in database | 100,000 |
| Orders in database | 200,000 |
| Orders with invalid customer references | 0 |

Result: PASSED

## 5. Idempotency verification

Automated tests verified that running the same customer or order records again does not create duplicate database entries.

Result: PASSED

## 6. Overall result

- Customer record reconciliation: PASSED
- Order record reconciliation: PASSED
- Database loading verification: PASSED
- Foreign-key integrity: PASSED
- Duplicate prevention: PASSED

The benchmark datasets were successfully processed and reconciled.
