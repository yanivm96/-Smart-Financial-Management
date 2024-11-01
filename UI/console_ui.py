import os
import logging
from src.data_loader import load_transactions_data
from src.reports_generator import create_expenses_by_categories_graph, create_monthly_summary_graph, create_recommendation_report
from src.config import configure_logging
from src.saving_recommendations import find_categories_exceeding_average, calculate_savings_reductions
from src.currency_exchange_rates import get_exchange_rates

configure_logging() # Initialize logging

def start_app_ui() -> None:
    """
    Launches the main user interface for the Smart Financial Management application.
    The function runs in a loop until the user selects the exit option ('0').
    """
    logging.info("Starting UI")
    menu_options = {
        '1': ("Start smart financial management process", handle_smart_financial_management),
        '2': ("Exchange foreign currency", handle_currency_exchange),
        '0': ("Exit", exit_program)
    }

    while True:
        print("\nHello, welcome to our smart financial management")
        for key, (description, _) in menu_options.items():
            print(f"{key}. {description}")
        
        user_input = input("Please enter your choice: ")
        action = menu_options.get(user_input)
        
        if action:
            _, func = action
            func()
        else:
            print("Invalid choice, please enter a valid option.")


def handle_smart_financial_management() -> None:
    """
    Handles the smart financial management process.
    Prompts the user to select a file with transaction data and optionally sets a monthly savings goal.
    Calls the start_smart_financial_process function with the provided file and savings goal if applicable.
    """
    menu_options = {
        '1': ("Enter monthly savings goal", handle_monthly_savings_goal),
        '2': ("Skip monthly savings goal", None),
    }

    transactions_filepath = get_user_transactions_file_name()
    if transactions_filepath:
        print("Choose an option:")
        for key, (description, _) in menu_options.items():
            print(f"{key}. {description}")

        user_choice = input("Please enter your choice: ")
        action = menu_options.get(user_choice)
        
        if action:
            _, func = action
            saving_goal = func() if func else 0 
            start_smart_financial_process(transactions_filepath, saving_goal)
        else:
            print("Invalid choice. Exiting the process.")
        


def handle_monthly_savings_goal() -> int:
    """
    Prompts the user to enter a positive integer amount for the monthly savings goal.
    Continues to ask until a valid positive integer is provided.

    Returns:
        int: The amount the user wants to save per month.
    """
    amount = 0
    while True:
        try:
            amount = int(input("\nPlease enter the amount of money you want to save or 0 to quit: \n"))
            if amount >= 0:
                break
            else:
                print("Amount must be a positive number. Please try again.")
        except ValueError:
            print("Invalid input. Please enter a positive integer.")

    return amount

def get_user_transactions_file_name() -> str:
    """
    Prompts the user to enter the full file name of the transactions file.
    Verifies if the file exists within a predefined directory.
    Allows the user to exit by typing 'exit'.

    Returns:
        str: The full path of the transactions file if it exists, or None if the user exits.
    """
    logging.info("getting transactions file name")
    file_exists = False
    transactions_filepath = None
    while(not file_exists):
        transactions_filepath = input("\nPlease enter the transactions file full name or exit to quit:\n")
        if transactions_filepath == 'exit':
            print("See you next time")
            transactions_filepath = None
            break

        transactions_filepath = os.path.join(os.getcwd(),"data",transactions_filepath)
        file_exists = os.path.exists(transactions_filepath)
        if not file_exists:
            print("File not found. Please check the file name and try again.")
    
    return transactions_filepath


def start_smart_financial_process(transactions_filepath: str, saving_goal: int) -> None:
    """
    Starts the financial management process by analyzing transaction data.
    Loads transaction data, creates graphs, generates recommendations, and produces a report
    based on a monthly savings goal.

    Args:
        transactions_filepath (str): The path to the transactions file.
        saving_goal (int): The target amount for monthly savings.
    """
    logging.info(f"Transaction file path is: {transactions_filepath}")
    saving_goal_recommendations = None
    reductions = None
    data = load_transactions_data(transactions_filepath)
    if data is not None:
        expenses_dataframe = create_expenses_by_categories_graph(data)
        monthly_summary_dataframe, created = create_monthly_summary_graph(data)
        
        if expenses_dataframe is not None and monthly_summary_dataframe is not None and created:
            general_recommendations = find_categories_exceeding_average(expenses_dataframe, monthly_summary_dataframe['Amount'][0])
            saving_goal = saving_goal - (monthly_summary_dataframe['Amount'][0] - monthly_summary_dataframe['Amount'][1]) # the net minus the saving goal
            
            if saving_goal > 0:
                 saving_goal_recommendations, reductions = calculate_savings_reductions(expenses_dataframe, saving_goal)
            
            is_graph_created = create_recommendation_report(general_recommendations, saving_goal_recommendations, reductions)
            if is_graph_created:
                print("\nYour reporst have been created under the reports folder.")
            
            else:
                print('there is a problem with creating the recommendation report')
                logging.error("recommendationr report.")
        
        elif not created:
            print('there is a problem with creating the monthly summary report')
            logging.error("recommendationr report.")
    else:
        logging.warning("No valid data to display.")


def handle_currency_exchange():
    """
    Handles currency exchange by prompting the user for input on the current and target currencies,
    and the amount they wish to exchange.
    """
    while True:
        try:
            current_currency_name = input("Please enter the current currency name (e.g., NIS, EUR): ").upper()
            target_currency_name = input("Please enter the target currency name (e.g., NIS, EUR): ").upper()
            
            if current_currency_name == target_currency_name:
                print("The current and target currencies must be different. Please try again.")
                continue

            amount_to_exchange = float(input("Please enter the amount to exchange: "))
            if amount_to_exchange <= 0:
                print("Amount must be a positive number. Please try again.")
                continue

            exchanged_amount, error_message = get_exchange_rates(current_currency_name, target_currency_name, amount_to_exchange)
            if error_message != "":
                print(error_message)
            else: 
                print(f"{amount_to_exchange} {current_currency_name} worth {exchanged_amount:.2f} {target_currency_name}")
                break  

        except ValueError:
            print("Invalid amount. Please enter a valid number.")
        except Exception as e:
            logging.error(f"An unexpected error occurred: {e}")
            print("An error occurred. Please try again.")


def exit_program() -> None:
    """
    Exits the application.
    """
    print("See you next time")
    exit(0)