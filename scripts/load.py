import pandas as pd
import sqlite3
import logging
import os

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def get_db_connection(db_path: str):
    """
    Returns a database connection dynamically based on Environment Variables.
    Allows seamless upgrading from SQLite to PostgreSQL for production.
    """
    db_type = os.getenv('DB_TYPE', 'sqlite')
    
    if db_type == 'postgres':
        # Example PostgreSQL connection using SQLAlchemy
        import sqlalchemy
        db_user = os.getenv('DB_USER', 'postgres')
        db_password = os.getenv('DB_PASSWORD', 'password')
        db_host = os.getenv('DB_HOST', 'localhost')
        db_name = os.getenv('DB_NAME', 'ecommerce_db')
        
        engine = sqlalchemy.create_engine(f"postgresql://{db_user}:{db_password}@{db_host}/{db_name}")
        logging.info("Connected to Production PostgreSQL Data Warehouse.")
        return engine
    else:
        # Default to local SQLite
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        conn = sqlite3.connect(db_path)
        logging.info("Connected to local SQLite Database.")
        return conn

def load_data(df: pd.DataFrame, db_path: str, table_name: str = 'transactions'):
    """
    Loads transformed data into the database. 
    Uses if_exists='replace' to ensure the pipeline is idempotent (safe to rerun).
    """
    logging.info(f"Starting data load into database, table: '{table_name}'...")
    
    conn = None
    try:
        conn = get_db_connection(db_path)
        
        # 'replace' ensures idempotency for batch loads
        df.to_sql(table_name, conn, if_exists='replace', index=False)
        logging.info(f"Successfully loaded {len(df)} records into '{table_name}'.")
            
    except Exception as e:
        logging.error(f"Failed to load data into database: {str(e)}")
        raise
    finally:
        # Close connection gracefully if using sqlite3
        if conn and isinstance(conn, sqlite3.Connection):
            conn.close()
            logging.info("Database connection closed.")
