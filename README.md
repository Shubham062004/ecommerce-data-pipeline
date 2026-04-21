# 🛒 E-Commerce ETL Data Pipeline & Analytics System

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Pandas](https://img.shields.io/badge/Pandas-2.2+-green.svg)
![Airflow](https://img.shields.io/badge/Apache_Airflow-Orchestration-blue.svg)
![Database](https://img.shields.io/badge/SQLite%2FPostgreSQL-Database-blue.svg)

## 📌 Project Overview
This project is an end-to-end Data Engineering **ETL (Extract, Transform, Load)** pipeline built to process, clean, and analyze e-commerce transaction data. It utilizes Python, Pandas, SQL, and Apache Airflow to orchestrate the refinement of raw messy data into a structured Data Warehouse ready for **Business Intelligence (Power BI)** reporting.

---

## 🏗️ Architecture & Orchestration

![ETL Architecture](https://via.placeholder.com/800x300.png?text=Raw+CSV+-%3E+Python(Pandas)+-%3E+PostgreSQL/SQLite+-%3E+Power+BI)

### The ETL Flow
1. **Extract**: Ingests raw sales data from CSV. Handles missing files and logs execution metrics.
2. **Transform**: Cleans data (imputing missing values), standardizes data types, and engineers business features (`revenue`, `tax_amount`).
3. **Load**: Connects dynamically to SQLite (or PostgreSQL via environment variables) and loads data idempotently.
4. **Orchestrate (Airflow)**: Replaces manual scripts with a daily scheduled DAG ensuring automated, resilient execution.

---

## 🛠️ Tech Stack
* **Orchestration**: Apache Airflow
* **Data Processing**: Python 3.x, Pandas
* **Storage**: SQLite (Local) / PostgreSQL (Production)
* **Analytics**: SQL, Power BI
* **Version Control**: Git / GitHub

---

## 🚀 How to Run the Project

### 1. Set up the environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Manual Pipeline Execution (Dev Mode)
You can test the pipeline synchronously:
```bash
python scripts/pipeline.py
```

### 3. Running via Apache Airflow (Production Mode)
This project includes a DAG (`dags/ecommerce_etl_dag.py`) for automated scheduling.
1. Set your `AIRFLOW_HOME` to this project directory:
   ```bash
   export AIRFLOW_HOME=$(pwd)
   ```
2. Initialize the Airflow Database and create a user:
   ```bash
   airflow db init
   airflow users create --username admin --password admin --firstname Data --lastname Engineer --role Admin --email admin@example.com
   ```
3. Start the Scheduler and Webserver:
   ```bash
   airflow scheduler &
   airflow webserver -p 8080
   ```
4. Navigate to `http://localhost:8080`, enable the `ecommerce_daily_etl` DAG, and trigger it!

---

## 📊 Business Intelligence (Power BI Integration)

The database output (`data/ecommerce.db` or PostgreSQL) is intentionally modeled for immediate BI connection.

**How to Connect:**
1. Open Power BI Desktop -> `Get Data` -> `ODBC` (for SQLite) or `PostgreSQL database`.
2. Connect to the resulting `transactions` table.

**Recommended Dashboards:**
- **KPI Cards**: `total_base_revenue`, `total_items_sold`.
- **Bar Chart**: Total Revenue broken down by `city` (Derived from SQL Query #2).
- **Table Matrix**: Top 10 Customers and their Lifetime Value (Derived from SQL Query #3).

---

## 🔮 Future Scope & Scalability
- **Streaming Ingestion**: Introduce **Apache Kafka** to replace daily batch loads with real-time transaction streaming.
- **Big Data Processing**: Scale the Pandas transformation layer up to **Apache Spark (PySpark)** for handling terabytes of data.
- **Cloud Infrastructure**: Deploy the PostgreSQL Warehouse to **AWS RDS** and shift raw data extraction to **AWS S3**.