import logging
import pandas
import os
from src.config import configure_logging
from typing import Optional
import matplotlib.pyplot as pyplot

FONT_SIZE = 12
TEXT_ROTATION = 45
CATEGORY_LABLEPAD = 20

configure_logging() # Initialize logging

def create_expenses_by_categories_graph(data : pandas.DataFrame) -> Optional[pandas.DataFrame]:
    """creates a sorted data graph by expense categories.

    Args:
        data as pandas.DataFrame object

    Returns:
        Sort data by expense categories as pandas.DataFrame object
    """
    try:
        expense_data = data[data['Amount'] < 0].copy()
        expense_data['Amount'] = expense_data['Amount'].abs()
        sorted_data = expense_data.groupby('Category')['Amount'].sum().sort_values(ascending=False)
        num_categories = len(sorted_data) # Adjust figure width dynamically based on the number of categories
        pyplot.figure(figsize=(max(14, num_categories * 2), 14))  # Adjust width, keep height constant
        bars = sorted_data.plot(kind='bar', color='skyblue', legend=False)

        for bar in bars.containers[0]:  # adding the amount in the middle of the column
            height = bar.get_height()
            bars.text(
                bar.get_x() + bar.get_width() / 2, height / 2,  
                f"{int(height)}",                              
                ha='center', va='center', fontsize=FONT_SIZE, color='black'
            )
            
        sorted_data.plot(kind='bar', x='Category', y='Amount', legend = False, )
        pyplot.xlabel('Category', fontsize=FONT_SIZE, labelpad=CATEGORY_LABLEPAD)
        pyplot.ylabel('Amount', fontsize=FONT_SIZE)
        pyplot.title('Sorted data by expense categories', fontsize=FONT_SIZE, weight='bold')
        pyplot.xticks(rotation=TEXT_ROTATION, ha='right')
        pyplot.savefig("reports/Sort_data_by_expense_categories.pdf", format='pdf')
        pyplot.close()
        logging.info('Sort_data_by_expense_categories.pdf have been created.')
        return sorted_data

    except Exception as e:
        logging.error(f"An error occurred: {e}")
        return None


def create_monthly_summary_graph(data : pandas.DataFrame) -> (Optional[pandas.DataFrame], bool):
    """creates a monthly summary graph - total income and expenses.

    Args:
        data as DataFrame object

    Returns:
        monthly summary as pandas.DataFrame object
    """
    try:
        graph_created = False
        income_data = data[data['Amount'] > 0]
        expense_data = data[data['Amount'] < 0]
        total_income = income_data['Amount'].sum()
        total_expenses = expense_data['Amount'].abs().sum()
        net_income = total_income - total_expenses
        summary_data = {
            'Type': ['Total Income', 'Total Expenses', 'Net Income'],
            'Amount': [total_income, total_expenses, net_income]
        }
        pyplot.figure(figsize=(8, 10))
        summary_df = pandas.DataFrame(summary_data)
        bars = pyplot.bar(summary_df['Type'], summary_df['Amount'], color=['green', 'red', 'blue'])
        pyplot.xlabel('Category', labelpad=CATEGORY_LABLEPAD)
        pyplot.ylabel('Amount')
        pyplot.title('Income and Expenses')

        for bar, amount in zip(bars, summary_df['Amount']): # adding the amount in the middle of the column
            pyplot.text(
                bar.get_x() + bar.get_width() / 2,  
                bar.get_height() / 2,               
                f"{amount}",                        
                ha='center', va='center', fontsize=10, color='white'  
            )

        pyplot.savefig("reports/monthly_summary.pdf", format='pdf')
        pyplot.close()
        if os.path.exists("reports/monthly_summary.pdf"):
            graph_created = True
            logging.info('monthly_summary.pdf have been created.')

        return summary_df, graph_created

    except Exception as e:
        logging.error(f"An error occurred: {e}")
    
    return None, False


def create_recommendation_report(general_recommendations: list, saving_goal_recommendations: list, category_reductions: dict) -> bool:
    """creates a recommendations graph - general and for saving goal that the user asks.

    Args:
       general_recommendations (list)
       saving_goal_recommendations(list)
       category_reductions(dict) with the persentage of each category redcution

    Returns:
        None
    """
    try:
        graph_created = False
        show_graph = True
        pyplot.figure(figsize=(8, 10))
        pyplot.subplot(3, 1, 1)
        pyplot.axis('off')
        pyplot.title("General Recommendations", fontsize=15, weight='bold', loc='left')
        
        recommendations_text = ""
        if general_recommendations:
            recommendations_text += "\n".join(general_recommendations)
        else:
            recommendations_text = "No general recommendations."
        recommendations_text += "\n\n"
        pyplot.text(0, 1, recommendations_text, fontsize=FONT_SIZE, va='top', ha='left', wrap=True)
        pyplot.text(0, 0.25, "To achive your saving goal we recommended:", fontsize=12, weight='bold', ha='left')

        saving_goal_recommendations_text = ""
        if saving_goal_recommendations:
            saving_goal_recommendations_text += "\n".join(saving_goal_recommendations)
        else:
            show_graph = False
            saving_goal_recommendations_text += "The current budget meets the savings goal."
        
        pyplot.text(0, 0.2, saving_goal_recommendations_text, fontsize=FONT_SIZE, va='top', ha='left', wrap=True)
        if show_graph:
            pyplot.subplot(3, 1, 3)
            pyplot.title("Reduction Percentages by Category for Saving Goals", fontsize=16, weight='bold', loc='left')
            categories = list(category_reductions.keys())
            values = list(category_reductions.values())
            pyplot.bar(categories, values, color='skyblue')
            pyplot.xlabel("Category")
            pyplot.ylabel("Reduction (%)")
            pyplot.ylim(0, 100)
            pyplot.tight_layout(pad=3.0)
            
        pyplot.savefig("reports/recommendation_report.pdf", format="pdf")
        pyplot.close()
        if os.path.exists("reports/recommendation_report.pdf"):
            graph_created = True
            logging.info("PDF report saved as recommendation_report.pdf")
        return graph_created
    
    except Exception as e:
        logging.error(e)