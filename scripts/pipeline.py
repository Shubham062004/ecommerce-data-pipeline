import os
import logging
from dotenv import load_dotenv

from extract import extract_data
from transform import process_data
from load import load_data

# Load environment variables
load_dotenv()

# Configure logging
if not logging.getLogger().hasHandlers():
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Constants from Environment
# Use default paths if env vars are not set
DATA_SOURCE = os.getenv('DATA_SOURCE', 'data/raw_data.csv')
DB_PATH = os.getenv('DB_FILE', 'data/ecommerce.db')

def run_pipeline():
    """
    Orchestrates the ETL process using modular scripts.
    """
    logger.info("=== Starting Production ETL Pipeline ===")
    
    try:
        # Step 1: Extract
        logger.info("PHASE 1: Extracting data from source.")
        raw_df = extract_data(DATA_SOURCE)
        
        # Step 2: Transform
        logger.info("PHASE 2: Cleaning and Engineering features.")
        transformed_df = process_data(raw_df)
        
        # Step 3: Load
        logger.info("PHASE 3: Loading data into destination warehouse.")
        load_data(transformed_df, db_path=DB_PATH, table_name='transactions')
        
        logger.info("=== ETL Pipeline Completed Successfully ===")
        
    except Exception as e:
        logger.error(f"Pipeline failed during execution: {e}")
        raise

if __name__ == "__main__":
    run_pipeline()
