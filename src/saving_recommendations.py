import pandas
import logging
from src.config import configure_logging

configure_logging()# Initialize logging
REDUCTION_STEP = 2 

def find_categories_exceeding_average(expenses_dataframe: pandas.DataFrame, income: int) -> list:
    """
    Identifies categories with expenses higher than the desired average and provides recommendations.

    Parameters:
    - expenses_dataframe (pandas.DataFrame): a dataframe with expense categories 
      (e.g., "Rent", "Groceries") and the amounts spent in each category.
    - income (int): Monthly income.

    Returns:
    - list of str: recommendations for reducing expenses.
    """

    # Define desired maximum percentage of income for each category
    desired_average_expenses = {
        'Rent': 30,  
        'Groceries': 10,  
        'Transport': 5, 
        'Entertainment': 5,  
        'Dining': 5,  
        'Healthcare': 7,  
        'Utilities': 5   
    }

    recommendations = []

    # Calculate each category's expense as a percentage of income and check against desired averages
    for category, amount in expenses_dataframe.items():
        if category in desired_average_expenses:
            max_percentage = desired_average_expenses[category]
            current_percentage = (amount / income) * 100
            
            # If the current percentage exceeds the max allowed percentage, recommend a reduction
            if current_percentage > max_percentage:
                reduction_percentage = ((current_percentage - max_percentage) / current_percentage) * 100
                recommendations.append(
                    f"It is recommended to reduce {category} expenses by {reduction_percentage:.1f}% because its higher than the desired average."
                )

    return recommendations


def calculate_reduction_amount(category_amount: float, reduction_step: float) -> float:
    """
    Calculate the reduction amount based on the reduction step percentage.
    """
    return (reduction_step / 100) * category_amount


def apply_reduction(expenses_dataframe: pandas.DataFrame, category: str, reduction_amount: float, reduction_percentages: dict) -> float:
    """
    Apply a reduction to a category in the expenses dataframe and update cumulative reductions.

    Parameters:
    - expenses_dataframe (pandas.DataFrame): The DataFrame of expenses.
    - category (str): The category to reduce.
    - reduction_percentages (dict): Dictionary tracking cumulative reduction percentages.

    Returns:
    - float: The actual reduction applied to the category.
    """
    original_amount = expenses_dataframe[category]
    if reduction_percentages[category] >= 100:
        return 0  # Stop if we've already reduced this category by 100%

    # Calculate actual reduction percentage and apply it
    reduction_percentage = (reduction_amount / original_amount) * 100
    if reduction_percentages[category] + reduction_percentage > 100:
        reduction_percentage = 100 - reduction_percentages[category]
        reduction_amount = (reduction_percentage / 100) * original_amount  # Adjust reduction amount because its over 100

    reduction_percentages[category] += reduction_percentage
    return reduction_amount

def reduce_expenses(expenses_dataframe: pandas.DataFrame, categories: list, remaining_goal: float) -> (dict, float):
    """
    Reduces expenses for the given categories in steps to meet the savings goal.

    Parameters:
    - expenses_dataframe (pandas.DataFrame): DataFrame with expense categories as index and values as amounts.
    - categories (list): List of categories to attempt reductions on.
    - remaining_goal (float): The amount needed to meet the savings goal.

    Returns:
    - dict: A dictionary with cumulative reduction percentages for each category.
    - float: Updated remaining goal after reductions.
    """
    reduction_percentages = {category: 0 for category in categories}

    while remaining_goal > 0 and any(reduction_percentages[category] < 100 for category in categories if category in expenses_dataframe.index):
        for category in categories:
            if remaining_goal <= 0:
                break
            if category in expenses_dataframe:
                # Calculate reduction amount and apply reduction
                current_amount = expenses_dataframe[category]
                reduction_amount = calculate_reduction_amount(current_amount, REDUCTION_STEP)
                actual_reduction = apply_reduction(expenses_dataframe, category, reduction_amount, reduction_percentages)
                remaining_goal -= actual_reduction

        if all(reduction_percentages[category] >= 100 for category in categories if category in expenses_dataframe.index):   # Check if all categories have reached 100% reduction
            break

    return reduction_percentages, remaining_goal

def calculate_savings_reductions(expenses_dataframe: pandas.DataFrame, savings_goal: float) -> (list, dict):
    """
    Provides recommendations to reduce expenses and meet a savings goal by reducing non-essential
    and then essential categories if needed.

    Parameters:
    - expenses_dataframe (pandas.DataFrame): DataFrame with expense categories as index and values as amounts.
    - income (float): Monthly income.
    - savings_goal (float): The target amount to save.

    Returns:
    - list of str: List of recommendations for expense reductions.
    - dict of percentage reductions in non_essential_categories.
    - dict of percentage reductions in essential_categories.
    """
    essential_reductions = {}
    non_essential_reductions = {}
    try:
        essential_categories = ['Utilities', 'Transport', 'Rent', 'Groceries',  'Healthcare', ]
        non_essential_categories = ['Entertainment', 'Dining']
        recommendations = []
        remaining_goal = savings_goal

        non_essential_reductions, remaining_goal = reduce_expenses(
            expenses_dataframe, non_essential_categories, remaining_goal
        )
        for category, reduction_percentage in non_essential_reductions.items():
            if reduction_percentage > 0:
                amount = int((expenses_dataframe[category] * reduction_percentage) / 100)
                recommendations.append(f"Reduce {category} expenses by {reduction_percentage:.1f}% to save {amount}.")

        if remaining_goal > 1:
            essential_reductions, remaining_goal = reduce_expenses(
                expenses_dataframe, essential_categories, remaining_goal
            )
            for category, reduction_percentage in essential_reductions.items():
                if reduction_percentage > 0:
                    amount = int((expenses_dataframe[category] * reduction_percentage) / 100)
                    recommendations.append(f"Reduce {category} expenses by {reduction_percentage:.1f}% to save {amount} and meet you goal.")

        if remaining_goal > 0:
            recommendations.append(f"Even with reductions, the savings goal could not be fully met. Additional savings of ${remaining_goal:.2f} are needed.")

        reductions = non_essential_reductions | essential_reductions
        return recommendations, reductions
    
    except Exception as e:
        logging.error(f"An error occurred: {e}")
        return None, None
    
    
