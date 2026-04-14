import pandas as pd
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Cleans the DataFrame by handling missing values, type conversions, and duplicates.
    """
    logging.info("Starting data cleaning process...")
    # Create a copy to prevent SettingWithCopyWarning
    df_clean = df.copy()

    # 1. Handle missing values
    if 'price' in df_clean.columns:
        # Fill missing price with the median price of the matching category
        df_clean['price'] = df_clean['price'].fillna(df_clean.groupby('category')['price'].transform('median'))
        # If category median is also NaN, fill with overall median
        df_clean['price'] = df_clean['price'].fillna(df_clean['price'].median())

    if 'status' in df_clean.columns:
        df_clean['status'] = df_clean['status'].fillna('unknown')

    # 2. Remove duplicates
    initial_row_count = len(df_clean)
    df_clean = df_clean.drop_duplicates()
    duplicates_removed = initial_row_count - len(df_clean)
    if duplicates_removed > 0:
        logging.info(f"Removed {duplicates_removed} duplicate rows.")

    # 3. Type conversion & Data Correction
    if 'transaction_date' in df_clean.columns:
        df_clean['transaction_date'] = pd.to_datetime(df_clean['transaction_date'], errors='coerce')
        
    if 'quantity' in df_clean.columns:
        # Fix negative quantities (assuming they are errors)
        df_clean.loc[df_clean['quantity'] < 0, 'quantity'] = 0
        df_clean['quantity'] = df_clean['quantity'].fillna(0).astype(int)

    logging.info("Data cleaning completed.")
    return df_clean

def engineer_features(df: pd.DataFrame, tax_rate: float = 0.08) -> pd.DataFrame:
    """
    Engineers new business features like 'revenue' and 'tax_amount'.
    """
    logging.info("Starting feature engineering...")
    df_feat = df.copy()

    if 'price' in df_feat.columns and 'quantity' in df_feat.columns:
        # Calculate base revenue
        df_feat['revenue'] = df_feat['price'] * df_feat['quantity']
        # Calculate tax amount based on fixed tax_rate
        df_feat['tax_amount'] = (df_feat['revenue'] * tax_rate).round(2)
        # Calculate final total amount
        df_feat['total_amount'] = df_feat['revenue'] + df_feat['tax_amount']
        
    logging.info("Feature engineering completed.")
    return df_feat

def validate_data(df: pd.DataFrame) -> bool:
    """
    Performs data quality checks to ensure constraints are met.
    """
    logging.info("Validating transformed data...")
    is_valid = True
    
    if (df['price'] < 0).any():
        logging.error("Validation failed: Negative prices detected.")
        is_valid = False
        
    if df['transaction_id'].isnull().any():
        logging.error("Validation failed: Null transaction_ids detected.")
        is_valid = False
        
    if is_valid:
        logging.info("Data validation passed successfully.")
        
    return is_valid

def process_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Main transformation pipeline combining cleaning, feature engineering, and validation.
    """
    df_clean = clean_data(df)
    df_transformed = engineer_features(df_clean)
    
    is_valid = validate_data(df_transformed)
    if not is_valid:
        logging.warning("Data validation identified anomalies. Please verify data upstream.")
        
    return df_transformed
