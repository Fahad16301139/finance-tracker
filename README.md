
# Personal Finance Tracker

**Personal Finance Tracker** is a command-line-based Python application that allows users to manage their finances by tracking income, expenses, and budgets. The application features user authentication, transaction management, budget alerts, data export to CSV, and data visualization using **Matplotlib**.

## Features

- **User Registration & Login**: Users can create an account and log in securely.
- **Income/Expense Tracking**: Users can log and track their income and expenses by category and date.
- **Budget Management**: Set budget limits for specific categories and receive alerts when expenses exceed the set budget.
- **Data Export**: Export transaction history to a CSV file for external analysis.
- **Data Visualization**: Visualize income vs. expenses and expense breakdowns by category using **Matplotlib**.
- **Persistent Data Storage**: All data is stored locally using **SQLite** for easy access and management.

## Installation

1. **Clone the repository**:
    ```bash
    git clone https://github.com/yourusername/personal-finance-tracker.git
    cd personal-finance-tracker
    ```

2. **Set up a virtual environment**:
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```

3. **Install the required packages**:
    ```bash
    pip install -r requirements.txt
    ```

4. **Initialize the database**:
    Run the application for the first time to initialize the database:
    ```bash
    python tracker.py
    ```

## Usage

1. **Run the application**:
    ```bash
    python tracker.py
    ```

2. **Main Menu**:
    - **Register**: Create a new user account.
    - **Login**: Log in with your account credentials.
    - **Quit**: Exit the program.

3. **User Menu** (after logging in):
    - **Add Transaction**: Log a new income or expense.
    - **View Income**: View a list of all logged income.
    - **View Expenses**: View a list of all logged expenses.
    - **View Summary**: View total income, total expenses, and the balance.
    - **Set Budget**: Set a budget limit for a specific category.
    - **View Budgets**: View the budget limits for all categories.
    - **Export to CSV**: Export all transactions to a CSV file.
    - **Visualize Income vs Expenses**: Generate a bar chart comparing total income and expenses.
    - **Visualize Expense Breakdown by Category**: Generate a pie chart showing a breakdown of expenses by category.
    - **Logout**: Log out of your account.

## Dependencies

- **Python 3.6+**
- **SQLite** (built-in with Python)
- **Matplotlib** (for visualizations)

## Running Tests

To run tests, simply execute the following command:

```bash
python -m unittest discover tests
```

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contributions

Contributions are welcome! If you have any ideas for new features or find any issues, please submit a pull request or open an issue on the repository.

---

Feel free to customize this **README** to better match your project structure or include additional details specific to your application.
