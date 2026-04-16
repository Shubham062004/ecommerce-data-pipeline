import pandas as pd
import logging

# Configure logging if not already configured
if not logging.getLogger().hasHandlers():
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Cleans the DataFrame by handling missing values, type conversions, and duplicates.
    """
    logger.info("Cleaning data: handling nulls, types, and duplicates.")
    df_clean = df.copy()

    # 1. Handle missing values
    if 'price' in df_clean.columns:
        df_clean['price'] = df_clean['price'].fillna(df_clean.groupby('category')['price'].transform('median'))
        df_clean['price'] = df_clean['price'].fillna(df_clean['price'].median())

    if 'status' in df_clean.columns:
        df_clean['status'] = df_clean['status'].fillna('unknown')

    # 2. Remove duplicates
    initial_row_count = len(df_clean)
    df_clean = df_clean.drop_duplicates()
    duplicates_removed = initial_row_count - len(df_clean)
    if duplicates_removed > 0:
        logger.info(f"Removed {duplicates_removed} duplicate rows.")

    # 3. Type conversion
    if 'transaction_date' in df_clean.columns:
        df_clean['transaction_date'] = pd.to_datetime(df_clean['transaction_date'], errors='coerce')
        
    if 'quantity' in df_clean.columns:
        df_clean.loc[df_clean['quantity'] < 0, 'quantity'] = 0
        df_clean['quantity'] = df_clean['quantity'].fillna(0).astype(int)

    return df_clean

def engineer_features(df: pd.DataFrame, tax_rate: float = 0.08) -> pd.DataFrame:
    """
    Engineers new business features like 'revenue' and 'tax_amount'.
    """
    logger.info("Engineering features: revenue, tax, and totals.")
    df_feat = df.copy()

    if 'price' in df_feat.columns and 'quantity' in df_feat.columns:
        df_feat['revenue'] = df_feat['price'] * df_feat['quantity']
        df_feat['tax_amount'] = (df_feat['revenue'] * tax_rate).round(2)
        df_feat['total_amount'] = df_feat['revenue'] + df_feat['tax_amount']
        
    return df_feat

def validate_data(df: pd.DataFrame) -> bool:
    """
    Performs critical data quality checks for production readiness.
    """
    logger.info("Validating transformed data for production readiness.")
    
    # Check 1: No negative prices
    if (df['price'] < 0).any():
        logger.error("Validation Error: Negative prices found.")
        return False
        
    # Check 2: No null transaction IDs
    if df['transaction_id'].isnull().any():
        logger.error("Validation Error: Null transaction IDs found.")
        return False

    # Check 3: Schema validation (ensuring essential columns exist)
    required_columns = ['transaction_id', 'transaction_date', 'total_amount']
    for col in required_columns:
        if col not in df.columns:
            logger.error(f"Validation Error: Missing required column {col}.")
            return False
            
    logger.info("Data validation passed successfully.")
    return True

def process_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Main transformation pipeline.
    """
    try:
        df_clean = clean_data(df)
        df_transformed = engineer_features(df_clean)
        
        if not validate_data(df_transformed):
            raise ValueError("Transformed data failed validation.")
            
        return df_transformed
    except Exception as e:
        logger.error(f"Transformation failed: {e}")
        raise
