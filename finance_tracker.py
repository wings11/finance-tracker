import sqlite3
import matplotlib.pyplot as plt
from datetime import datetime

# Database setup
def init_db():
    conn = sqlite3.connect("finance.db")
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS transactions
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  type TEXT,
                  amount REAL,
                  category TEXT,
                  date TEXT)''')
    conn.commit()
    conn.close()

# Add a transaction
def add_transaction(type_, amount, category):
    try:
        amount = float(amount)
        if amount <= 0:
            raise ValueError("Amount must be positive")
        conn = sqlite3.connect("finance.db")
        c = conn.cursor()
        date = datetime.now().strftime("%Y-%m-%d")
        c.execute("INSERT INTO transactions (type, amount, category, date) VALUES (?, ?, ?, ?)",
                  (type_, amount, category, date))
        conn.commit()
        print(f"Added {type_}: {amount} in {category}")
    except ValueError as e:
        print(f"Error: {e}")
    finally:
        conn.close()

# View summary
def view_summary():
    conn = sqlite3.connect("finance.db")
    c = conn.cursor()
    c.execute("SELECT type, SUM(amount) FROM transactions GROUP BY type")
    summary = c.fetchall()
    total_income = sum(amount for type_, amount in summary if type_ == "Income")
    total_expense = sum(amount for type_, amount in summary if type_ == "Expense")
    savings = total_income - total_expense
    print(f"Total Income: ${total_income:.2f}")
    print(f"Total Expenses: ${total_expense:.2f}")
    print(f"Savings: ${savings:.2f}")
    conn.close()

# Visualize spending by category
def plot_spending():
    conn = sqlite3.connect("finance.db")
    c = conn.cursor()
    c.execute("SELECT category, SUM(amount) FROM transactions WHERE type='Expense' GROUP BY category")
    data = c.fetchall()
    if not data:
        print("No expenses to plot.")
        return
    categories, amounts = zip(*data)
    plt.figure(figsize=(8, 6))
    plt.pie(amounts, labels=categories, autopct="%1.1f%%")
    plt.title("Spending by Category")
    plt.show()
    conn.close()

# Main menu
def main():
    init_db()
    while True:
        print("\nPersonal Finance Tracker")
        print("1. Add Income")
        print("2. Add Expense")
        print("3. View Summary")
        print("4. View Spending Chart")
        print("5. Exit")
        choice = input("Choose an option (1-5): ")
        
        if choice == "1":
            amount = input("Enter income amount: ")
            category = input("Enter category (e.g., Salary, Freelance): ")
            add_transaction("Income", amount, category)
        elif choice == "2":
            amount = input("Enter expense amount: ")
            category = input("Enter category (e.g., Food, Rent): ")
            add_transaction("Expense", amount, category)
        elif choice == "3":
            view_summary()
        elif choice == "4":
            plot_spending()
        elif choice == "5":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Try again.")

if __name__ == "__main__":
    main()
