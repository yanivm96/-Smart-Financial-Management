# -Smart-Financial-Management

# Prerequisites
- Python 3.11.10

# Set up
1. Clone the repository:
   use this command on your commendline tool: git clone https://github.com/yanivm96/Smart-Financial-Management.git

2. Navigate into the project directory: cd Smart-Financial-Management

3. Install all dependencies from requirements.txt: pip install -r requirements.txt

4. Place your transactions file inside a folder named data in the project's root directory.

5. to run the app use: python main.py 

# Approach
1.Analyze Spending: The tool examines user expenses across predefined categories, comparing each category’s spending to a target percentage of monthly income.

2.Generate Savings Recommendations: If spending in a category exceeds its target, a recommendation is generated to reduce spending. Reductions are prioritized in non-essential categories (e.g., Entertainment) before essential ones (e.g., Rent).

3.Step-by-Step Reductions: The tool applies gradual reductions to each category until the savings goal is met, or all feasible reductions are made.

4.Generate Report: A PDF report summarizes the recommendations and shows the reduction percentages by category.


# Application Structure
To enhance maintainability and flexibility, the application is divided into two layers:

1. Backend: Handles all data processing, calculations, and business logic, including expense analysis and savings recommendations. This separation allows updates to logic and calculations without affecting the user interface.

2. User Interface (UI): Focuses on displaying the recommendations and generating reports. By keeping the UI separate from the backend, future UI updates or changes can be implemented easily without impacting core functionality.


# Assumptions
1. Fixed Categories: The tool assumes that the categories in the transactions file are predefined and remain consistent over time.

2. Savings Priorities: Non-essential expenses (e.g., Entertainment, Dining) are reduced before essential ones (e.g., Rent, Transport) to minimize lifestyle impact while achieving savings goals.