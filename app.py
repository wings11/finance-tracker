import streamlit as st
import sqlite3
import matplotlib.pyplot as plt
from datetime import datetime
import os

# Set page config
st.set_page_config(page_title="Personal Finance Tracker", page_icon="💰")

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
        return True, f"Added {type_}: ${amount:.2f} in {category}"
    except ValueError as e:
        return False, str(e)
    finally:
        conn.close()

# Get summary
def get_summary():
    conn = sqlite3.connect("finance.db")
    c = conn.cursor()
    c.execute("SELECT type, SUM(amount) FROM transactions GROUP BY type")
    summary = c.fetchall()
    total_income = sum(amount for type_, amount in summary if type_ == "Income")
    total_expense = sum(amount for type_, amount in summary if type_ == "Expense")
    savings = total_income - total_expense
    conn.close()
    return total_income, total_expense, savings

# Plot spending
def plot_spending():
    conn = sqlite3.connect("finance.db")
    c = conn.cursor()
    c.execute("SELECT category, SUM(amount) FROM transactions WHERE type='Expense' GROUP BY category")
    data = c.fetchall()
    conn.close()
    if not data:
        return None
    categories, amounts = zip(*data)
    fig, ax = plt.subplots()
    ax.pie(amounts, labels=categories, autopct="%1.1f%%")
    ax.set_title("Spending by Category")
    return fig

# Streamlit UI
st.title("💸 Personal Finance Tracker 💰")
st.write("Track your income, expenses, and savings with ease!")

# Initialize database
init_db()

# Add transaction section
st.subheader("Add Transaction")
col1, col2 = st.columns(2)
with col1:
    type_ = st.selectbox("Type", ["Income", "Expense"])
with col2:
    category = st.selectbox("Category", ["Salary", "Freelance", "Food", "Rent", "Utilities", "Other"])
amount = st.number_input("Amount ($)", min_value=0.01, step=0.01)
if st.button("Add Transaction"):
    success, message = add_transaction(type_, amount, category)
    if success:
        st.success(message)
    else:
        st.error(f"Error: {message}")

# Summary section
st.subheader("Summary")
total_income, total_expense, savings = get_summary()
st.write(f"**Total Income**: ${total_income:.2f}")
st.write(f"**Total Expenses**: ${total_expense:.2f}")
st.write(f"**Savings**: ${savings:.2f}")

# Visualization section
st.subheader("Spending Breakdown")
fig = plot_spending()
if fig:
    st.pyplot(fig)
else:
    st.info("No expenses to display yet.")

# Footer
st.markdown("---")
st.write("Built with Python & Streamlit by Wings")
