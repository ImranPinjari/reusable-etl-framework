# Data Dictionary

## 1. Customers Dataset

| Column | Data type | Constraint | Description |
|---|---|---|---|
| customer_id | Integer | Primary key, required, unique | Unique customer identifier |
| name | String | Required | Customer full name |
| email | String | Required, valid email | Customer email address |
| city | String | Required | Customer city |
| registration_date | Date | Required, valid date | Customer registration date |

### Validation rules
- Customer ID must not be null or duplicated.
- Name, email, city, and registration date are required.
- Email must follow a valid email format.
- Registration date must be a valid date.

## 2. Orders Dataset

| Column | Data type | Constraint | Description |
|---|---|---|---|
| order_id | Integer | Primary key, required, unique | Unique order identifier |
| customer_id | Integer | Foreign key, required | References customers.customer_id |
| order_date | Date | Required, valid date | Date the order was placed |
| amount | Float | Required, greater than zero | Order amount |
| status | String | Required, allowed values | Current order status |

### Allowed order statuses
- completed
- pending
- cancelled

### Validation rules
- Order ID must not be null or duplicated.
- Customer ID must reference an existing customer.
- Order date must be valid.
- Amount must be numeric and greater than zero.
- Status must be one of the allowed values.

## 3. Dataset Relationship

One customer can have multiple orders.

Relationship:

customers.customer_id (Primary Key)
        |
        | One-to-Many
        |
orders.customer_id (Foreign Key)

## 4. Data Lineage and Audit Fields

The ETL pipeline also maintains metadata for traceability:

| Field | Description |
|---|---|
| run_id | Identifies the ETL execution |
| source_file | Original input file name |
| source_record_number | Record position in the source file |
| rejection_reason | Explains why a record was rejected |
| ingested_at | Timestamp when the record was loaded, where supported |

