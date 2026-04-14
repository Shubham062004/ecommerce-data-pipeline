import pandas as pd
import sqlite3
import logging
import os

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def load_data(df: pd.DataFrame, db_path: str, table_name: str = 'sales_data'):
    """
    Loads transformed data into a SQLite database. 
    Can be easily swapped for a SQLAlchemy connection to PostgreSQL/MySQL.
    
    Args:
        df (pd.DataFrame): The transformed dataframe to load.
        db_path (str): The path to the SQLite database file.
        table_name (str): The name of the target database table.
    """
    logging.info(f"Starting data load into database at {db_path}, table: '{table_name}'...")
    
    # Ensure directory exists before connecting
    os.makedirs(os.path.dirname(db_path), exist_ok=True)
    
    try:
        # Connect to SQLite. Using a context manager ensures safe connection handling.
        with sqlite3.connect(db_path) as conn:
            # Write records to the database. 'replace' drops the table if it already exists.
            df.to_sql(table_name, conn, if_exists='replace', index=False)
            logging.info(f"Successfully loaded {len(df)} records into the '{table_name}' table.")
            
    except Exception as e:
        logging.error(f"Failed to load data into database: {str(e)}")
        raise
    
    logging.info("Database connection closed gracefully.")
