import tkinter as tk
from tkinter import messagebox
import json
from datetime import datetime


DATA_FILE = "budget_data.json"


def load_data():
    try:
        with open(DATA_FILE, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return []


def save_data(transactions):
    with open(DATA_FILE, 'w') as file:
        json.dump(transactions, file, indent=4)


def add_transaction(trans_type, category, amount, date):
    transactions.append({
        "type": trans_type,
        "category": category,
        "amount": float(amount),
        "date": date
    })
    save_data(transactions)
    messagebox.showinfo("Success", f"{trans_type.capitalize()} added successfully!")


def calculate_budget():
    total_income = sum(t['amount'] for t in transactions if t['type'] == 'income')
    total_expenses = sum(t['amount'] for t in transactions if t['type'] == 'expense')
    remaining_budget = total_income - total_expenses
    return total_income, total_expenses, remaining_budget


def analyze_expenses():
    categories = {}
    for t in transactions:
        if t['type'] == 'expense':
            categories[t['category']] = categories.get(t['category'], 0) + t['amount']
    return categories


def show_add_income():
    show_add_transaction_window("income")


def show_add_expense():
    show_add_transaction_window("expense")

def show_add_transaction_window(trans_type):
    window = tk.Toplevel(root)
    window.title(f"Add {trans_type.capitalize()}")

    tk.Label(window, text=f"{trans_type.capitalize()} Category:").grid(row=0, column=0)
    tk.Label(window, text=f"{trans_type.capitalize()} Amount:").grid(row=1, column=0)
    tk.Label(window, text="Date (YYYY-MM-DD):").grid(row=2, column=0)

    category_entry = tk.Entry(window)
    amount_entry = tk.Entry(window)
    date_entry = tk.Entry(window)

    category_entry.grid(row=0, column=1)
    amount_entry.grid(row=1, column=1)
    date_entry.grid(row=2, column=1)

    if trans_type == 'expense':
        category_entry.insert(0, "General")  # Default category for expenses

    def add_and_close():
        category = category_entry.get()
        amount = amount_entry.get()
        date = date_entry.get() or datetime.today().strftime('%Y-%m-%d')
        add_transaction(trans_type, category, amount, date)
        window.destroy()

    tk.Button(window, text="Add", command=add_and_close).grid(row=3, column=0, columnspan=2)

def show_budget():
    total_income, total_expenses, remaining_budget = calculate_budget()
    budget_info = (
        f"Total Income: {total_income}\n"
        f"Total Expenses: {total_expenses}\n"
        f"Remaining Budget: {remaining_budget}"
    )
    messagebox.showinfo("Budget", budget_info)

def show_expense_analysis():
    categories = analyze_expenses()
    if not categories:
        messagebox.showinfo("Expense Analysis", "No expenses to analyze.")
    else:
        analysis = "\n".join(f"Category: {category}, Amount Spent: {amount}" for category, amount in categories.items())
        messagebox.showinfo("Expense Analysis", analysis)

root = tk.Tk()
root.title("Budget Tracker")

transactions = load_data()

menu = tk.Menu(root)
root.config(menu=menu)

add_menu = tk.Menu(menu)
menu.add_cascade(label="Add", menu=add_menu)
add_menu.add_command(label="Income", command=show_add_income)
add_menu.add_command(label="Expense", command=show_add_expense)

view_menu = tk.Menu(menu)
menu.add_cascade(label="View", menu=view_menu)
view_menu.add_command(label="Budget", command=show_budget)
view_menu.add_command(label="Expense Analysis", command=show_expense_analysis)

root.mainloop()
