import requests
import logging
from src.config import configure_logging

configure_logging() # Initialize logging

def get_exchange_rates(current_currency: str, target_currency: str, amount: float) -> (float, str):
    """this function make currency exchange

    Args:
        current_currency to exchange as str
        target_currency to exchange as str
        amount of the current currency as float

    Returns:
        float : amount after the exchange
    """
    if amount > 0:
        try:
            URL = 'https://api.frankfurter.app/latest?base='
            request_result = requests.get(URL+current_currency).json()
            if request_result.get('message'):
                return None, f"\n{current_currency} - {request_result.get('message')}"
            
            target_currency_worth = request_result.get('rates', None).get(target_currency, None)
            if target_currency_worth is None:
                return None, f"\n{target_currency} is not in the database"

            return amount * target_currency_worth, ""
                    
        except Exception as e:
            logging.error(e)
    
    else:
        return None, "amount must be greater that 0"