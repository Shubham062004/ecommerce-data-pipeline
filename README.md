# 🛒 E-Commerce ETL Data Pipeline & Analytics System

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Pandas](https://img.shields.io/badge/Pandas-2.2+-green.svg)
![SQLite](https://img.shields.io/badge/SQLite-Database-blue.svg)

## 📌 Project Overview
This project is an end-to-end Data Engineering **ETL (Extract, Transform, Load)** pipeline built to process, clean, and analyze e-commerce transaction data. It simulates a real-world scenario where raw, messy data is refined into a highly structured database ready for Business Intelligence (BI) and Data Analytics.

The resulting dataset provides actionable insights into revenue streams, regional performance, and customer lifetime value.

---

## 🏗️ Architecture (The ETL Flow)

1. **Extract (`scripts/extract.py`)**: Ingests raw sales data from a CSV file. Implements safeguards to handle missing files and empty datasets.
2. **Transform (`scripts/transform.py`)**: 
   - **Data Cleaning**: Imputes missing values, enforces typing (e.g., negative quantities handled, valid timestamps), and removes duplicates.
   - **Feature Engineering**: Dynamically calculates business metrics (`revenue`, `tax_amount`, `total_amount`).
   - **Data Quality Validations**: Failsafes and checks to ensure no corrupt metrics pass through.
3. **Load (`scripts/load.py`)**: Connects to an SQLite database (adaptable to PostgreSQL) using secure context managers and loads the polished dataset into a `transactions` table.
4. **Analyze (`sql/queries.sql`)**: Sophisticated SQL aggregations and Window Functions developed for extracting KPI reports.

---

## 🛠️ Tech Stack
* **Language**: Python 3.x
* **Data Processing**: Pandas, NumPy
* **Data Storage**: SQLite3 (Standard RDBMS structure)
* **Analytics**: SQL (CTEs, Window Functions, Aggregations)
* **Version Control**: Git / GitHub

---

## 🚀 How to Run the Project

### 1. Clone the repository
```bash
git clone https://github.com/Shubham062004/ecommerce-data-pipeline.git
cd ecommerce-data-pipeline
```

### 2. Set up the environment
It is recommended to use a virtual environment.
```bash
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Run the ETL Pipeline
Trigger the main orchestration script to process the data:
```bash
python scripts/pipeline.py
```
*Behind the scenes, this will read `data/raw_data.csv`, clean it, and output the refined version to `data/ecommerce.db`.*

### 4. Query the Database
You can execute the queries listed in `sql/queries.sql` using any SQL client (like DBeaver, DB Browser for SQLite, or Python's `sqlite3` CLI) against the generated `data/ecommerce.db` database.

---

## 📊 Sample Insights & Output

By querying the transformed database, we solve specific business questions like:
- **Total Regional Valuation (Query 2):** Identifies highly localized spending patterns for dynamic marketing allocation.
- **Top Customer Rankings (Query 4):** Employs the `DENSE_RANK() OVER(PARTITION BY city)` function to pinpoint exact localized VIP spenders across different geographical hubs.

```log
=== Starting E-Commerce ETL Pipeline ===
--- Phase 1: EXTRACT ---
Successfully extracted 10 rows and 9 columns.
--- Phase 2: TRANSFORM ---
Data cleaning completed.
Feature engineering completed.
Data validation passed successfully.
--- Phase 3: LOAD ---
Successfully loaded 10 records into the 'transactions' table.
=== ETL Pipeline Completed Successfully! ===
```

---

## 🔮 Future Improvements
To take this pipeline from a batch-processed script to an enterprise-grade ecosystem, I plan to integrate:
- **Apache Airflow**: For robust, scheduled task orchestration and dependency management.
- **PostgreSQL / Snowflake**: Migrate from local SQLite to a scalable, cloud-hosted Data Warehouse.
- **Power BI / Tableau Component**: Connect BI tools directly to the Data Warehouse for interactive management dashboards.
- **Cloud Storage (AWS S3)**: Move `raw_data.csv` to an S3 Data Lake for real-world distributed extraction.