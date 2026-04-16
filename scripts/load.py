import pandas as pd
import logging
import os
from sqlalchemy import create_engine
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging if not already configured
if not logging.getLogger().hasHandlers():
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def get_db_connection():
    """
    Creates a database connection based on environment variables.
    Supports SQLite and PostgreSQL.
    """
    db_type = os.getenv('DB_TYPE', 'sqlite').lower()
    
    if db_type == 'sqlite':
        db_file = os.getenv('DB_FILE', 'data/ecommerce.db')
        # Ensure the directory exists
        os.makedirs(os.path.dirname(db_file), exist_ok=True)
        return create_engine(f'sqlite:///{db_file}')
    
    elif db_type == 'postgresql':
        user = os.getenv('DB_USER')
        password = os.getenv('DB_PASSWORD')
        host = os.getenv('DB_HOST', 'localhost')
        port = os.getenv('DB_PORT', '5432')
        name = os.getenv('DB_NAME')
        return create_engine(f'postgresql://{user}:{password}@{host}:{port}/{name}')
    
    else:
        raise ValueError(f"Unsupported database type: {db_type}")

def load_data(df: pd.DataFrame, table_name: str = 'transactions'):
    """
    Loads transformed data into the database.
    """
    logger.info(f"Initiating load to table: '{table_name}'")
    
    try:
        engine = get_db_connection()
        
        # Load data (if_exists='replace' ensures idempotency for full refresh)
        with engine.connect() as conn:
            df.to_sql(table_name, conn, if_exists='replace', index=False)
            
        logger.info(f"Load successful: {len(df)} records written to {table_name}.")
            
    except Exception as e:
        logger.error(f"Load failed: {e}")
        raise
