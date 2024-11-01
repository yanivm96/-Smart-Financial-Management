import pandas
import logging
from typing import Optional
from src.config import configure_logging

# Initialize logging
configure_logging()

def load_transactions_data(filepath: str) -> Optional[pandas.DataFrame]:
    """Loads transaction data from a CSV file and validates it.

    Args:
        Path to the CSV file.

    Returns:
        Validated DataFrame if successful, None if not.
    """
    try:
        csv_data = pandas.read_csv(filepath)
        validated_data = check_transactions_file(csv_data)
        return validated_data

    except FileNotFoundError:
        logging.error(f"File {filepath} not found.")
        return None
    except Exception as e:
        logging.error(f"An error occurred: {e}")
        return None
    

def check_transactions_file(csv_data: pandas.DataFrame) -> Optional[pandas.DataFrame]:
    """Validates the transaction data from a CSV file.

    Args:
        DataFrame containing CSV data.

    Returns:
        DataFrame with valid rows or None if all data is invalid.
    """
    valid_rows = []
    required_data_columns = {'Date', 'Category', 'Amount'}
    
    # Check if required columns are present
    if not required_data_columns.issubset(csv_data.columns):
        logging.error("CSV file is missing required columns.")
        return None
    
    # Validate each row individually
    for index, row in csv_data.iterrows():
        # Validate date
        try:
            date = pandas.to_datetime(row['Date'], errors='raise')
        except ValueError:
            logging.error(f"Invalid date at row {index + 1}: {row['Date']}")
            continue 
        
        # Validate amount 
        amount = row['Amount']
        if not isinstance(amount, (int, float)) or amount == 0:
            logging.error(f"Invalid amount at row {index + 1}: {amount}")
            continue 

        valid_rows.append(row)

    return pandas.DataFrame(valid_rows) if valid_rows else None