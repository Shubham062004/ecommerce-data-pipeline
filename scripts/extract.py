import pandas as pd
import logging
import os

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def extract_data(file_path: str) -> pd.DataFrame:
    """
    Extracts data from a CSV file.
    
    Args:
        file_path (str): The path to the source CSV file.
        
    Returns:
        pd.DataFrame: The extracted data as a pandas DataFrame.
    """
    try:
        logging.info(f"Starting data extraction from {file_path}")
        
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Source file not found at: {file_path}")
            
        df = pd.read_csv(file_path)
        logging.info(f"Successfully extracted {len(df)} rows and {len(df.columns)} columns.")
        
        # Basic edge-case validation
        if df.empty:
            logging.warning("The extracted dataset is empty.")
            
        return df
        
    except Exception as e:
        logging.error(f"Data extraction failed: {str(e)}")
        raise
