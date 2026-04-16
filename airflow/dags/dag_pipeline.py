from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
import sys
import os

# Add scripts directory to sys.path to import modules
sys.path.append(os.path.join(os.path.dirname(__file__), '../../scripts'))

from extract import extract_data
from transform import process_data
from load import load_data

# Default arguments for the DAG
default_args = {
    'owner': 'data_engineer',
    'depends_on_past': False,
    'start_date': datetime(2024, 1, 1),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

# Define the DAG
dag = DAG(
    'ecommerce_etl_pipeline',
    default_args=default_args,
    description='A production-level E-commerce ETL pipeline',
    schedule_interval=timedelta(days=1),
    catchup=False
)

def extract_task_fn(**kwargs):
    # Get file path from env or use default
    data_source = os.getenv('DATA_SOURCE', 'data/raw_data.csv')
    df = extract_data(data_source)
    # In a real Airflow setup, we might save to a temp file or XCom
    # For this simplified beginner-friendly version, we pass small dataframes as XComs
    # Note: large dataframes should be stored in S3/HDFS/etc
    return df.to_json()

def transform_task_fn(**kwargs):
    ti = kwargs['ti']
    extracted_data_json = ti.xcom_pull(task_ids='extract_task')
    import pandas as pd
    df = pd.read_json(extracted_data_json)
    transformed_df = process_data(df)
    return transformed_df.to_json()

def load_task_fn(**kwargs):
    ti = kwargs['ti']
    transformed_data_json = ti.xcom_pull(task_ids='transform_task')
    import pandas as pd
    df = pd.read_json(transformed_data_json)
    load_data(df, table_name='transactions')

# Define Tasks
extract_task = PythonOperator(
    task_id='extract_task',
    python_callable=extract_task_fn,
    dag=dag,
)

transform_task = PythonOperator(
    task_id='transform_task',
    python_callable=transform_task_fn,
    dag=dag,
)

load_task = PythonOperator(
    task_id='load_task',
    python_callable=load_task_fn,
    dag=dag,
)

# Set dependencies
extract_task >> transform_task >> load_task
