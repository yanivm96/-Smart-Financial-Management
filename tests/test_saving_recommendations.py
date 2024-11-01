import pandas 
import pytest
from src.saving_recommendations import (
    find_categories_exceeding_average,
    calculate_reduction_amount,
    apply_reduction,
    reduce_expenses,
    calculate_savings_reductions,
)


@pytest.fixture
def sample_data():
    return pandas.DataFrame({
    'Category': ['Rent', 'Groceries', 'Transport', 'Healthcare', 'Utilities', 'Entertainment', 'Dining'],
    'Amount': [174624, 40593, 39793, 34480, 33235, 32309, 32280]
    }).set_index('Category')['Amount']


@pytest.fixture
def sample_income():
    return 5000

@pytest.fixture
def sample_savings_goal():
    return float(20000)


def test_find_categories_exceeding_average(sample_data, sample_income):
    print(sample_data)
    recommendations = find_categories_exceeding_average(sample_data, sample_income)
    assert isinstance(recommendations, list)
    assert all(isinstance(item, str) for item in recommendations)
    assert "It is recommended to reduce Rent expenses" in recommendations[0]  


def test_calculate_reduction_amount():
    reduction_amount = calculate_reduction_amount(100, 5)
    assert reduction_amount == 5  # 5% of 100


def test_apply_reduction(sample_data):
    reduction_percentages = {'Rent': 0}
    initial_amount = sample_data['Rent']
    reduction_amount = calculate_reduction_amount(initial_amount, 2)
    actual_reduction = apply_reduction(sample_data, 'Rent', reduction_amount, reduction_percentages)
    assert actual_reduction == reduction_amount
    assert reduction_percentages['Rent'] == 2


def test_reduce_expenses(sample_data, sample_savings_goal):
    categories = ['Entertainment', 'Dining']
    reduction_percentages, remaining_goal = reduce_expenses(sample_data, categories, sample_savings_goal)
    assert isinstance(reduction_percentages, dict)
    assert isinstance(remaining_goal, float)
    assert sum(reduction_percentages.values()) <= 100


def test_calculate_savings_reductions(sample_data, sample_savings_goal):
    recommendations, reductions = calculate_savings_reductions(sample_data, sample_savings_goal)
    assert isinstance(recommendations, list)
    assert isinstance(reductions, dict)
