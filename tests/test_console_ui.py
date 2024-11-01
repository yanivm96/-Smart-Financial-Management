import pytest
import os
from unittest.mock import patch
from UI.console_ui import handle_monthly_savings_goal,get_user_transactions_file_name

def test_handle_monthly_savings_goal_valid():
    with patch('builtins.input', side_effect=['100']):
        assert handle_monthly_savings_goal() == 100

def test_handle_monthly_savings_goal_invalid_then_valid():
    with patch('builtins.input', side_effect=['-50', 'abc', '200']):
        assert handle_monthly_savings_goal() == 200

def test_get_user_transactions_file_name_exists():
    with patch('builtins.input', side_effect=['transactions.csv']), \
         patch('os.path.exists', return_value=True):
        assert get_user_transactions_file_name() == os.path.join(os.getcwd(), "data", "transactions.csv")

def test_get_user_transactions_file_name_exit():
    with patch('builtins.input', side_effect=['exit']):
        assert get_user_transactions_file_name() is None

def test_get_user_transactions_file_name_not_exists():
    with patch('builtins.input', side_effect=['invalid.csv', 'transactions.csv']), \
         patch('os.path.exists', side_effect=[False, True]):
        assert get_user_transactions_file_name() == os.path.join(os.getcwd(), "data", "transactions.csv")