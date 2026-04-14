import os
import logging

from extract import extract_data
from transform import process_data
from load import load_data

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Define absolute paths dynamically
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_PATH = os.path.join(BASE_DIR, 'data', 'raw_data.csv')
DB_PATH = os.path.join(BASE_DIR, 'data', 'ecommerce.db')

def run_pipeline():
    """
    Main ETL Orchestration Component.
    Executes the Extract, Transform, and Load steps sequentially.
    """
    logging.info("=== Starting E-Commerce ETL Pipeline ===")
    
    try:
        # Step 1: Extract
        logging.info("--- Phase 1: EXTRACT ---")
        raw_df = extract_data(DATA_PATH)
        
        # Step 2: Transform
        logging.info("--- Phase 2: TRANSFORM ---")
        transformed_df = process_data(raw_df)
        
        # Step 3: Load
        logging.info("--- Phase 3: LOAD ---")
        load_data(transformed_df, DB_PATH, table_name='transactions')
        
        logging.info("=== ETL Pipeline Completed Successfully! ===")
        
    except Exception as e:
        logging.error(f"=== ETL Pipeline Failed: {str(e)} ===")
        raise

if __name__ == "__main__":
    run_pipeline()
