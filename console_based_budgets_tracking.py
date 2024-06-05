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

def add_transaction(transactions, trans_type):
    category = input(f"Enter the {trans_type} category: ")
    amount = float(input(f"Enter the {trans_type} amount: "))
    date = input("Enter the date (YYYY-MM-DD) or leave blank for today: ")
    if not date:
        date = datetime.today().strftime('%Y-%m-%d')
    transaction = {
        "type": trans_type,
        "category": category,
        "amount": amount,
        "date": date
    }
    transactions.append(transaction)
    save_data(transactions)
    print(f"{trans_type.capitalize()} added successfully!")

def calculate_budget(transactions):
    total_income = sum(t['amount'] for t in transactions if t['type'] == 'income')
    total_expenses = sum(t['amount'] for t in transactions if t['type'] == 'expense')
    remaining_budget = total_income - total_expenses
    return total_income, total_expenses, remaining_budget

def analyze_expenses(transactions):
    categories = {}
    for t in transactions:
        if t['type'] == 'expense':
            categories[t['category']] = categories.get(t['category'], 0) + t['amount']
    if not categories:
        print("No expenses to analyze.")
    else:
        for category, amount in categories.items():
            print(f"Category: {category}, Amount Spent: {amount}")

def main():
    transactions = load_data()

    while True:
        print("\nBudget Tracker Menu")
        print("1. Add Income")
        print("2. Add Expense")
        print("3. View Budget")
        print("4. Analyze Expenses")
        print("5. Exit")

        choice = input("Choose an option: ")

        if choice == '1':
            add_transaction(transactions, 'income')
        elif choice == '2':
            add_transaction(transactions, 'expense')
        elif choice == '3':
            total_income, total_expenses, remaining_budget = calculate_budget(transactions)
            print(f"Total Income: {total_income}")
            print(f"Total Expenses: {total_expenses}")
            print(f"Remaining Budget: {remaining_budget}")
        elif choice == '4':
            analyze_expenses(transactions)
        elif choice == '5':
            print("Exiting Budget Tracker.")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
