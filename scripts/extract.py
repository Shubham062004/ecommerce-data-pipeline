import pandas as pd
import logging
import os

# Configure logging if not already configured
if not logging.getLogger().hasHandlers():
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def extract_data(file_path: str) -> pd.DataFrame:
    """
    Extracts data from a CSV file.
    
    Args:
        file_path (str): The path to the source CSV file.
        
    Returns:
        pd.DataFrame: The extracted data as a pandas DataFrame.
    """
    logger.info(f"Initiating extraction from {file_path}")
    
    try:
        # Check if file exists
        if not os.path.exists(file_path):
            error_msg = f"Critical Error: Source file not found at {file_path}"
            logger.error(error_msg)
            raise FileNotFoundError(error_msg)
            
        # Read CSV
        df = pd.read_csv(file_path)
        
        # Validation
        if df.empty:
            logger.warning("Extraction completed but the dataset is empty.")
        else:
            logger.info(f"Extraction successful: {len(df)} rows found.")
            
        return df
        
    except pd.errors.EmptyDataError:
        logger.error("The source CSV file is empty.")
        raise
    except Exception as e:
        logger.error(f"Unexpected error during extraction: {e}")
        raise
