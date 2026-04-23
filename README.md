# 🛒 E-Commerce ETL Data Pipeline & Analytics System

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![Pandas](https://img.shields.io/badge/Pandas-2.2+-green.svg)](https://pandas.pydata.org/)
[![Airflow](https://img.shields.io/badge/Apache_Airflow-Orchestration-017CEE.svg)](https://airflow.apache.org/)
[![Kafka](https://img.shields.io/badge/Apache_Kafka-Streaming-231F20.svg)](https://kafka.apache.org/)
[![Database](https://img.shields.io/badge/SQLite%2FPostgreSQL-Data_Warehouse-4479A1.svg)](https://www.sqlite.org/)

## 📌 Project Overview
This project is an end-to-end **Data Engineering ecosystem** designed to ingest, clean, and analyze high-velocity e-commerce transaction data. It utilizes a **Hybrid Architecture** (Lambda-style) that seamlessly bridges the gap between daily **Batch ETL** workflows and real-time **Streaming Ingestion**.

The system transforms raw, inconsistent event data into a structured Data Warehouse, enabling actionable business intelligence regarding revenue growth, regional performance, and customer lifetime value (CLV).

---

## 🏗️ Architecture & Orchestration

The pipeline is built on a modular design principle, ensuring high maintainability and production readiness.

### 1. Batch Pipeline (Historical Data)
*   **Orchestration**: Managed by **Apache Airflow**.
*   **Process**: Daily extraction of bulk CSV data, sophisticated cleaning via Pandas (imputation, type enforcement), and idempotent loading into the Warehouse.
*   **Reliability**: Includes automatic retries, dependency management, and data quality validation.

### 2. Real-Time Pipeline (Streaming Data)
*   **Broker**: **Apache Kafka** handles sub-second event ingestion.
*   **Producer**: Simulates live order generation with varying velocities.
*   **Consumer**: Processes incoming streams on-the-fly, applying consistent transformation logic before database persistence.

---

## 📂 Project Structure

```text
ecommerce-data-pipeline/
├── dags/                       # Airflow Orchestration
│   └── ecommerce_etl_dag.py    # Daily scheduled workflow logic
├── data/                       # Storage Layer
│   ├── raw_data.csv            # Source of truth (Raw input)
│   └── ecommerce.db            # Production SQLite Warehouse
├── scripts/                    # Core Python Modules
│   ├── extract.py              # Ingestion: Reads from various sources
│   ├── transform.py            # Logic: Cleaning & Feature Engineering
│   ├── load.py                 # Sink: Schema-compliant DB loading
│   ├── pipeline.py             # Orchestrator: Main ETL entry point
│   ├── verify_load.py          # QA: Quick database health check
│   ├── generate_insights.py    # BI: Automated KPI report generator
│   ├── producer.py             # Kafka: Live event producer
│   └── consumer.py             # Kafka: Real-time stream processor
├── sql/                        # Analytical Layer
│   ├── queries.sql             # Advanced SQL (CTEs, Window Functions)
│   └── bi_views.sql            # Pre-defined BI views
├── requirements.txt            # Dependency Management
└── README.md                   # Documentation
```

---

## 🌟 Key Features
-   **Production-Grade Transformation**: Handles missing data using category-median imputation and enforces schema integrity.
-   **Financial Engineering**: Automatically calculates revenue, tax, and total transaction amounts.
-   **Analytical Depth**: Leverages **Window Functions** to rank customers by region and city.
-   **Environment Agnostic**: Easily switch between SQLite and PostgreSQL via `.env` configuration.
-   **Idempotent Loading**: Safe-to-rerun logic preventing data duplication.

---

## 🚀 Getting Started

### 1. Environment Setup
```bash
# Clone the repository
git clone https://github.com/Shubham062004/ecommerce-data-pipeline.git
cd ecommerce-data-pipeline

# Install dependencies
pip install -r requirements.txt
```

### 2. Running the Batch Pipeline
```bash
# Execute the full ETL cycle
python scripts/pipeline.py

# Verify the load status
python scripts/verify_load.py

# Generate a business insights report
python scripts/generate_insights.py
```

### 3. Real-Time Streaming (Kafka)
1.  **Start Services**: Ensure Zookeeper and Kafka Broker are running.
2.  **Create Topic**: `orders_stream`
3.  **Run Stream**:
    ```bash
    python scripts/producer.py  # In Terminal 1
    python scripts/consumer.py  # In Terminal 2
    ```

---

## 📊 Sample Insights
*   **Revenue Growth**: Real-time monitoring of daily sales trends.
*   **Regional Performance**: Identification of high-growth markets (e.g., New York, Houston).
*   **VIP Identification**: Automated ranking of customers by lifetime spend within localized clusters.

---

## 🔮 Future Roadmap
-   **PySpark Integration**: Migrate consumer logic to Spark Streaming for enterprise scale.
-   **Cloud Native**: Deploy Kafka to Confluent Cloud and DB to AWS RDS.
-   **Data Quality**: Integrate **Great Expectations** for automated data unit testing.