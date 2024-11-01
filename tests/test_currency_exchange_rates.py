import pytest
import os
from unittest.mock import patch
from src.currency_exchange_rates import get_exchange_rates


def test_get_exchange_rates_valid():
    amount, error_message  = get_exchange_rates('USD', 'EUR', 1)
    assert amount > 0 and error_message == ""

def test_get_exchange_rates_invalid_current_currency():
    amount, error_message  = get_exchange_rates('abccc', 'EUR', 1)
    assert amount is None and 'abccc' in error_message 

def test_get_exchange_rates_invalid_target_currency():
    amount, error_message  = get_exchange_rates('USD', 'abccc', 1)
    assert amount is None and 'abccc' in error_message 

def test_get_exchange_rates_invalid_amount():
    amount, error_message  = get_exchange_rates('USD', 'EUR', -1)
    assert amount is None and "amount must be greater that 0" in error_message 
