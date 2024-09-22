import sqlite3
import matplotlib.pyplot as plt
import csv

# Initialize the SQLite database
def init_db():
    conn = sqlite3.connect('finance_tracker.db')
    c = conn.cursor()

    # Create users table
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            email TEXT NOT NULL,
            password TEXT NOT NULL
        )
    ''')

    # Create transactions table
    c.execute('''
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            amount REAL NOT NULL,
            type TEXT NOT NULL, -- 'income' or 'expense'
            category TEXT NOT NULL,
            date TEXT NOT NULL,
            FOREIGN KEY(user_id) REFERENCES users(id)
        )
    ''')

    # Create budgets table
    c.execute('''
        CREATE TABLE IF NOT EXISTS budgets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            category TEXT NOT NULL,
            budget_amount REAL NOT NULL,
            FOREIGN KEY(user_id) REFERENCES users(id)
        )
    ''')

    conn.commit()
    conn.close()

# User registration function
def register_user():
    username = input("Enter your username: ")
    email = input("Enter your email: ")
    password = input("Enter your password: ")

    conn = sqlite3.connect('finance_tracker.db')
    c = conn.cursor()

    c.execute('INSERT INTO users (username, email, password) VALUES (?, ?, ?)', (username, email, password))

    conn.commit()
    conn.close()

    print(f"User {username} registered successfully!")

# User login function
def login_user():
    email = input("Enter your email: ")
    password = input("Enter your password: ")

    conn = sqlite3.connect('finance_tracker.db')
    c = conn.cursor()

    c.execute('SELECT * FROM users WHERE email = ? AND password = ?', (email, password))
    user = c.fetchone()

    conn.close()

    if user:
        print(f"Welcome, {user[1]}!")
        return user[0]  # Return user ID
    else:
        print("Invalid login credentials.")
        return None

# Add a transaction
def add_transaction(user_id):
    amount = float(input("Enter the amount: "))
    type = input("Enter transaction type (income/expense): ").lower()
    category = input("Enter the category (e.g., food, rent, salary): ")
    date = input("Enter the date (YYYY-MM-DD): ")

    conn = sqlite3.connect('finance_tracker.db')
    c = conn.cursor()

    c.execute('INSERT INTO transactions (user_id, amount, type, category, date) VALUES (?, ?, ?, ?, ?)',
              (user_id, amount, type, category, date))

    conn.commit()

    # Check if user exceeded their budget
    if type == 'expense':
        # Total expenses for this category
        c.execute('SELECT SUM(amount) FROM transactions WHERE user_id = ? AND category = ? AND type = "expense"', 
                  (user_id, category))
        total_expense = c.fetchone()[0] or 0

        # Fetch budget for the category
        c.execute('SELECT budget_amount FROM budgets WHERE user_id = ? AND category = ?', (user_id, category))
        budget = c.fetchone()

        if budget and total_expense > budget[0]:
            print(f"Warning: You have exceeded your budget for {category}! Total expenses: {total_expense}, Budget: {budget[0]}")

    conn.close()

    print(f"{type.capitalize()} of {amount} added successfully!")

# View transactions (income/expenses)
def view_transactions(user_id, transaction_type):
    conn = sqlite3.connect('finance_tracker.db')
    c = conn.cursor()

    c.execute('SELECT * FROM transactions WHERE user_id = ? AND type = ?', (user_id, transaction_type))
    transactions = c.fetchall()

    conn.close()

    print(f"\nYour {transaction_type} transactions:")
    for transaction in transactions:
        print(f"Amount: {transaction[2]}, Category: {transaction[4]}, Date: {transaction[5]}")

# View income vs expense summary
def view_summary(user_id):
    conn = sqlite3.connect('finance_tracker.db')
    c = conn.cursor()

    c.execute('SELECT SUM(amount) FROM transactions WHERE user_id = ? AND type = "income"', (user_id,))
    total_income = c.fetchone()[0] or 0

    c.execute('SELECT SUM(amount) FROM transactions WHERE user_id = ? AND type = "expense"', (user_id,))
    total_expense = c.fetchone()[0] or 0

    conn.close()

    print(f"\nSummary:")
    print(f"Total Income: {total_income}")
    print(f"Total Expenses: {total_expense}")
    print(f"Balance: {total_income - total_expense}")

# Set budget for a category
def set_budget(user_id):
    category = input("Enter the category for the budget (e.g., food, rent, salary): ")
    budget_amount = float(input(f"Enter the budget amount for {category}: "))

    conn = sqlite3.connect('finance_tracker.db')
    c = conn.cursor()

    # Check if the budget already exists for the category
    c.execute('SELECT * FROM budgets WHERE user_id = ? AND category = ?', (user_id, category))
    budget = c.fetchone()

    if budget:
        c.execute('UPDATE budgets SET budget_amount = ? WHERE user_id = ? AND category = ?', 
                  (budget_amount, user_id, category))
        print(f"Updated the budget for {category}.")
    else:
        c.execute('INSERT INTO budgets (user_id, category, budget_amount) VALUES (?, ?, ?)', 
                  (user_id, category, budget_amount))
        print(f"Budget set for {category}: {budget_amount}")

    conn.commit()
    conn.close()

# View budgets
def view_budgets(user_id):
    conn = sqlite3.connect('finance_tracker.db')
    c = conn.cursor()

    c.execute('SELECT * FROM budgets WHERE user_id = ?', (user_id,))
    budgets = c.fetchall()

    conn.close()

    print("\nYour Budgets:")
    for budget in budgets:
        print(f"Category: {budget[2]}, Budget: {budget[3]}")

# Export transactions to CSV
def export_transactions_to_csv(user_id):
    filename = f"user_{user_id}_transactions.csv"
    conn = sqlite3.connect('finance_tracker.db')
    c = conn.cursor()

    c.execute('SELECT * FROM transactions WHERE user_id = ?', (user_id,))
    transactions = c.fetchall()

    conn.close()

    with open(filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Transaction ID", "User ID", "Amount", "Type", "Category", "Date"])

        for transaction in transactions:
            writer.writerow(transaction)

    print(f"Transactions exported to {filename}")

# Visualize income vs. expenses
def visualize_income_vs_expense(user_id):
    conn = sqlite3.connect('finance_tracker.db')
    c = conn.cursor()

    # Get total income
    c.execute('SELECT SUM(amount) FROM transactions WHERE user_id = ? AND type = "income"', (user_id,))
    total_income = c.fetchone()[0] or 0

    # Get total expenses
    c.execute('SELECT SUM(amount) FROM transactions WHERE user_id = ? AND type = "expense"', (user_id,))
    total_expense = c.fetchone()[0] or 0

    conn.close()

    # Create a bar chart
    categories = ['Income', 'Expense']
    amounts = [total_income, total_expense]

    plt.bar(categories, amounts, color=['green', 'red'])
    plt.title('Income vs. Expense')
    plt.ylabel('Amount')
    plt.show()

    print(f"Total Income: {total_income}")
    print(f"Total Expenses: {total_expense}")

# Visualize expense by category
def visualize_expense_by_category(user_id):
    conn = sqlite3.connect('finance_tracker.db')
    c = conn.cursor()

    # Get expenses for each category
    c.execute('SELECT category, SUM(amount) FROM transactions WHERE user_id = ? AND type = "expense" GROUP BY category', (user_id,))
    results = c.fetchall()

    conn.close()

    categories = [result[0] for result in results]
    amounts = [result[1] for result in results]

    plt.pie(amounts, labels=categories, autopct='%1.1f%%', startangle=140)
    plt.title('Expenses by Category')
    plt.axis('equal')
    plt.show()

    print("Category-wise Expense Breakdown:")
    for category, amount in zip(categories, amounts):
        print(f"{category}: {amount}")

# Main menu
def main_menu():
    while True:
        print("\n--- Personal Finance Tracker ---")
        print("1. Register")
        print("2. Login")
        print("3. Quit")
        choice = input("Enter choice: ")

        if choice == "1":
            register_user()
        elif choice == "2":
            user_id = login_user()
            if user_id:
                user_menu(user_id)
        elif choice == "3":
            break
        else:
            print("Invalid choice. Try again.")

def user_menu(user_id):
    while True:
        print("\n--- User Menu ---")
        print("1. Add Transaction")
        print("2. View Income")
        print("3. View Expenses")
        print("4. View Summary")
        print("5. Set Budget")
        print("6. View Budgets")
        print("7. Export Transactions to CSV")
        print("8. Visualize Income vs. Expenses")
        print("9. Visualize Expenses by Category")
        print("10. Logout")

        choice = input("Enter choice: ")

        if choice == "1":
            add_transaction(user_id)
        elif choice == "2":
            view_transactions(user_id, "income")
        elif choice == "3":
            view_transactions(user_id, "expense")
        elif choice == "4":
            view_summary(user_id)
        elif choice == "5":
            set_budget(user_id)
        elif choice == "6":
            view_budgets(user_id)
        elif choice == "7":
            export_transactions_to_csv(user_id)
        elif choice == "8":
            visualize_income_vs_expense(user_id)
        elif choice == "9":
            visualize_expense_by_category(user_id)
        elif choice == "10":
            break
        else:
            print("Invalid choice. Try again.")

if __name__ == "__main__":
    init_db()  # Ensure the database is initialized
    main_menu()

