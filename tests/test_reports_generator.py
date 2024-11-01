import pandas
import pytest
import os
from src.reports_generator import create_expenses_by_categories_graph, create_monthly_summary_graph, create_recommendation_report
import time

@pytest.fixture
def sample_data():
    data = {
        'Date': ['2024-01-01', '2024-01-05', '2024-02-01'],
        'Category': ['Salary', 'Groceries', 'Rent'],
        'Amount': [5000, -200, -1500]
    }
    return pandas.DataFrame(data)

@pytest.fixture
def report_data():
    return {
        "general_recommendations": ["Consider reducing entertainment expenses by 10%."],
        "saving_goal_recommendations": ["Re1duce dining expenses by 20% to meet your goal."],
        "category_reductions": {"Entertainment": 10, "Dining": 20}
    }

def test_create_expenses_by_categories_graph(sample_data):
    dataframe = create_expenses_by_categories_graph(sample_data)
    time.sleep(2)
    assert dataframe is not None
    assert os.path.exists("reports/Sort_data_by_expense_categories.pdf"),  "pdf should be created"
    assert len(dataframe) == 2
    os.remove("reports/Sort_data_by_expense_categories.pdf")


def test_create_monthly_summary_graph(sample_data):
    dataframe, created = create_monthly_summary_graph(sample_data)
    time.sleep(2)
    assert created == True
    assert len(dataframe) == 3
    os.remove("reports/monthly_summary.pdf")

def test_create_recommendation_report(report_data):
    created = create_recommendation_report(
        report_data["general_recommendations"],
        report_data["saving_goal_recommendations"],
        report_data["category_reductions"])
    time.sleep(2)
    assert created == True, "pdf should be created"
    os.remove("reports/recommendation_report.pdf")