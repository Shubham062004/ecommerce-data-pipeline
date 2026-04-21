# 🛒 E-Commerce ETL Data Pipeline & Analytics System

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Pandas](https://img.shields.io/badge/Pandas-2.2+-green.svg)
![Airflow](https://img.shields.io/badge/Apache_Airflow-Orchestration-blue.svg)
![Kafka](https://img.shields.io/badge/Apache_Kafka-Streaming-red.svg)
![Database](https://img.shields.io/badge/SQLite%2FPostgreSQL-Database-blue.svg)

## 📌 Project Overview
This project is an end-to-end Data Engineering ecosystem built to process, clean, and analyze e-commerce transaction data. It features a **Hybrid Architecture** combining robust **Batch ETL** (Python, Airflow) with real-time **Streaming Ingestion** (Kafka).

---

## 🏗️ Architecture & Orchestration

![ETL Architecture](https://via.placeholder.com/800x400.png?text=Hybrid+Data+Pipeline:+Batch+(Airflow)+%2B+Streaming+(Kafka))

### 1. Batch Pipeline (Historical Data)
* **Orchestration**: Managed by **Apache Airflow** (`dags/ecommerce_etl_dag.py`).
* **Process**: Extracts bulk CSV data, transforms it via Pandas, and loads it into the Data Warehouse.

### 2. Real-Time Pipeline (Streaming Data)
* **Ingestion**: **Apache Kafka** acts as the message broker.
* **Producer**: `scripts/producer.py` simulates real-time order generation.
* **Consumer**: `scripts/consumer.py` processes incoming streams and stores them in the `transactions_stream` table.

---

## 🚀 Getting Started

### 1. Environment Setup
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Kafka Setup (Streaming Mode)
1. **Download Kafka**: [Download here](https://kafka.apache.org/downloads).
2. **Start Zookeeper**:
   ```bash
   bin/zookeeper-server-start.sh config/zookeeper.properties
   ```
3. **Start Kafka Broker**:
   ```bash
   bin/kafka-server-start.sh config/server.properties
   ```
4. **Create Topic**:
   ```bash
   bin/kafka-topics.sh --create --topic orders_stream --bootstrap-server localhost:9092
   ```

### 3. Running the Pipeline
* **Start Streaming**:
  Run the producer and consumer in separate terminals:
  ```bash
  python scripts/producer.py
  python scripts/consumer.py
  ```
* **Start Batch ETL**:
  ```bash
  python scripts/pipeline.py
  ```

---

## 📊 Business Intelligence & Analytics

**Dashboard Insights:**
- **Real-Time Monitor**: Track incoming orders as they happen.
- **Revenue Trends**: Compare historical batch data vs. recent streaming data.
- **Regional Heatmap**: Identify peak performance cities using SQL Query #2.

---

## 🔮 Future Roadmap
- **Spark Streaming**: Replace the Python consumer with PySpark for micro-batch processing.
- **Cloud Migration**: Move Kafka to **Confluent Cloud** and the database to **Amazon RDS**.
- **Data Quality (Great Expectations)**: Integrate automated data testing into the streaming flow.