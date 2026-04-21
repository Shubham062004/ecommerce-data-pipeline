from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import os
import pandas as pd
import sys

# Dynamically add the scripts directory to path to reuse our ETL functions
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, os.path.join(BASE_DIR, 'scripts'))

from extract import extract_data
from transform import process_data
from load import load_data

# Define file paths for intermediate data handoffs (simulating S3 / Staging layer)
RAW_DATA_PATH = os.path.join(BASE_DIR, 'data', 'raw_data.csv')
EXTRACTED_DATA_PATH = os.path.join(BASE_DIR, 'data', 'extracted_data.csv')
TRANSFORMED_DATA_PATH = os.path.join(BASE_DIR, 'data', 'transformed_data.csv')
DB_PATH = os.path.join(BASE_DIR, 'data', 'ecommerce.db')

# Define default arguments for the Airflow DAG
default_args = {
    'owner': 'data_engineer',
    'depends_on_past': False,
    'start_date': datetime(2023, 10, 1),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

def extract_task():
    """Extracts data and saves it locally for the next task (Idempotent handoff)."""
    df = extract_data(RAW_DATA_PATH)
    df.to_csv(EXTRACTED_DATA_PATH, index=False)
    print(f"Extraction successful. Data staged at {EXTRACTED_DATA_PATH}")

def transform_task():
    """Reads staged data, transforms it, and saves for loading."""
    df = pd.read_csv(EXTRACTED_DATA_PATH)
    transformed_df = process_data(df)
    transformed_df.to_csv(TRANSFORMED_DATA_PATH, index=False)
    print(f"Transformation successful. Data staged at {TRANSFORMED_DATA_PATH}")

def load_task():
    """Reads transformed data and loads it into the database."""
    df = pd.read_csv(TRANSFORMED_DATA_PATH)
    load_data(df, DB_PATH, table_name='transactions')
    print("Loading successful. Data committed to database.")

# Initialize the DAG
with DAG(
    'ecommerce_daily_etl',
    default_args=default_args,
    description='Daily Scheduled ETL pipeline for E-Commerce analytics',
    schedule_interval='@daily',
    catchup=False,
) as dag:

    # Define tasks
    t1 = PythonOperator(
        task_id='extract_data',
        python_callable=extract_task,
    )

    t2 = PythonOperator(
        task_id='transform_data',
        python_callable=transform_task,
    )

    t3 = PythonOperator(
        task_id='load_data',
        python_callable=load_task,
    )

    # Set exact ETL dependencies (Airflow Workflow)
    t1 >> t2 >> t3
