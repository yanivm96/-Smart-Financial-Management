import pandas 
import pytest
from src.data_loader import load_transactions_data, check_transactions_file

@pytest.fixture
def valid_data():
    """Fixture for a valid DataFrame."""
    data = {
        'Date': ['2024-01-01', '2024-01-05', '2024-02-01'],
        'Category': ['Salary', 'Food', 'Rent'],
        'Amount': [5000, -200, -1500]
    }
    return pandas.DataFrame(data)

@pytest.fixture
def invalid_data_missing_columns():
    """Fixture for DataFrame missing required columns."""
    data = {
        'Date': ['2024-02-02', '2024-01-01'],
        'Category': ['Salary', 'Food'],
    }
    return pandas.DataFrame(data)

@pytest.fixture
def invalid_data_bad_amount():
    """Fixture for DataFrame with invalid amount values."""
    data = {
        'Date': ['2024-02-02', '2024-01-01'],
        'Category': ['Salary', 'Food'],
        'Amount': ['Not a number', -200] 
    }
    return pandas.DataFrame(data)

@pytest.fixture
def invalid_data_bad_date():
    """Fixture for DataFrame with invalid date values."""
    data = {
        'Date': ['Invalid Date', '2024-01-01'],
        'Category': ['Salary', 'Food'],
        'Amount': [5000, -200]
    }
    return pandas.DataFrame(data)

def test_load_transactions_data_valid_data(tmp_path, valid_data):
    # Save the valid_data DataFrame to a CSV file
    file_path = tmp_path / "valid_transactions.csv"
    valid_data.to_csv(file_path, index=False)
    dataframe = load_transactions_data(file_path)
    assert dataframe is not None, "Data should load successfully."
    assert len(dataframe) == 3, "All rows should be loaded for valid data."

def test_check_transactions_file_valid_data(valid_data):
    dataframe = check_transactions_file(valid_data)
    assert dataframe is not None, "Validation should pass with valid data."
    assert len(dataframe) == 3, "All rows should be validated for valid data."

def test_check_transactions_file_missing_columns(invalid_data_missing_columns):
    dataframe = check_transactions_file(invalid_data_missing_columns)
    assert dataframe is None, "Validation should fail if required columns are missing."

def test_check_transactions_file_bad_amount(invalid_data_bad_amount):
    dataframe = check_transactions_file(invalid_data_bad_amount)
    assert dataframe is not None, "DataFrame should be returned, skipping invalid rows."
    assert len(dataframe) == 1, "One invalid row with bad amount should be skipped."

def test_check_transactions_file_bad_date(invalid_data_bad_date):
    dataframe = check_transactions_file(invalid_data_bad_date)
    assert dataframe is not None, "DataFrame should be returned, skipping invalid rows."
    assert len(dataframe) == 1, "One invalid row with bad date should be skipped."