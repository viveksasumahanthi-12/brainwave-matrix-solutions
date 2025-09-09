import json
import os
import getpass
from datetime import datetime

# File to store user data
DATA_FILE = 'atm_users.json'

# Initialize data if file does not exist
if not os.path.exists(DATA_FILE):
    with open(DATA_FILE, 'w') as f:
        json.dump({}, f)


def load_data():
    with open(DATA_FILE, 'r') as f:
        return json.load(f)


def save_data(data):
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f, indent=4)


def create_account():
    data = load_data()
    print("\n=== Create New Account ===")
    username = input("Enter username: ").strip()
    if username in data:
        print("Account already exists.")
        return

    pin = getpass.getpass("Set a 4-digit PIN: ").strip()
    if len(pin) != 4 or not pin.isdigit():
        print("Invalid PIN. Must be exactly 4 digits.")
        return

    data[username] = {
        'pin': pin,
        'balance': 0.0,
        'transactions': []
    }
    save_data(data)
    print(f"Account created successfully for {username}!")


def login():
    data = load_data()
    print("\n=== ATM Login ===")
    username = input("Enter username: ").strip()
    if username not in data:
        print("User not found.")
        return None

    pin = getpass.getpass("Enter PIN: ").strip()
    if pin != data[username]['pin']:
        print("Incorrect PIN.")
        return None

    print(f"Welcome, {username}!")
    return username


def show_balance(user, data):
    print(f"\nYour current balance is: ₹{data[user]['balance']:.2f}")


def deposit(user, data):
    amount = input("\nEnter amount to deposit: ₹").strip()
    if not amount.replace('.', '', 1).isdigit():
        print("Invalid amount.")
        return

    amount = float(amount)
    data[user]['balance'] += amount
    data[user]['transactions'].append(
        f"{datetime.now()} - Deposited ₹{amount:.2f}")
    save_data(data)
    print(f"₹{amount:.2f} deposited successfully!")


def withdraw(user, data):
    amount = input("\nEnter amount to withdraw: ₹").strip()
    if not amount.replace('.', '', 1).isdigit():
        print("Invalid amount.")
        return

    amount = float(amount)
    if amount > data[user]['balance']:
        print("Insufficient balance!")
        return

    data[user]['balance'] -= amount
    data[user]['transactions'].append(
        f"{datetime.now()} - Withdrawn ₹{amount:.2f}")
    save_data(data)
    print(f"₹{amount:.2f} withdrawn successfully!")


def transaction_history(user, data):
    print("\n=== Transaction History ===")
    transactions = data[user]['transactions']
    if not transactions:
        print("No transactions found.")
    else:
        for txn in transactions:
            print(txn)


def atm_interface():
    while True:
        print("\n====== Welcome to Python ATM ======")
        print("1. Create New Account")
        print("2. Login")
        print("3. Exit")

        choice = input("Choose an option: ").strip()

        if choice == '1':
            create_account()

        elif choice == '2':
            user = login()
            if user:
                while True:
                    print("\n--- ATM Menu ---")
                    print("1. Balance Inquiry")
                    print("2. Deposit Money")
                    print("3. Withdraw Money")
                    print("4. Transaction History")
                    print("5. Logout")

                    option = input("Select option: ").strip()
                    data = load_data()

                    if option == '1':
                        show_balance(user, data)

                    elif option == '2':
                        deposit(user, data)

                    elif option == '3':
                        withdraw(user, data)

                    elif option == '4':
                        transaction_history(user, data)

                    elif option == '5':
                        print("Logging out...")
                        break

                    else:
                        print("Invalid option.")

        elif choice == '3':
            print("Thank you for using Python ATM. Goodbye!")
            break

        else:
            print("Invalid choice. Please select 1, 2, or 3.")


if __name__ == '__main__':
    atm_interface()
