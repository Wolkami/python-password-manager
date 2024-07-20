from core.init import *
from core.db import *
from core.ui import *
from Crypto.Random import get_random_bytes


def main():
    init_db()

    # Проверка наличия мастер-пароля
    conn = sqlite3.connect('passwords.db')
    cursor = conn.cursor()
    cursor.execute('SELECT COUNT(*) FROM master')
    result = cursor.fetchone()
    conn.close()

    if result[0] == 0:
        # Установка нового мастер-пароля
        master_password = input("Set a new master password: ").strip()
        set_master_password(master_password)
        print("Master password set successfully.")
    else:
        # Проверка мастер-пароля
        master_password = input("Enter master password: ").strip()
        if not verify_master_password(master_password):
            print("Invalid master password. Exiting.")
            return

    key = hashlib.sha256(master_password.encode()).digest()

    while True:
        command = input("Enter command (help for list of commands): ").strip().lower()

        if command == 'add':
            service = input("Enter service name: ").strip()
            username = input("Enter username: ").strip()
            password = input("Enter password: ").strip()
            add_account(service, username, password, key)
            print("Account added successfully.")

        elif command == 'get':
            service = input("Enter service name: ").strip()
            account = get_account(service, key)
            if account:
                username, password = account
                print(f"Username: {username}, Password: {password}")
            else:
                print("No account found for the given service.")

        elif command == 'delete':
            service = input("Enter service name: ").strip()
            delete_account(service)
            print("Account deleted successfully.")

        elif command == 'list':
            accounts = list_accounts()
            if accounts:
                for account in accounts:
                    print(f"Service: {account[0]}, Username: {account[1]}")
            else:
                print("No accounts found.")

        elif command == 'help':
            display_help()

        elif command == 'exit':
            break

        else:
            print("Invalid command. Type 'help' for list of commands.")


if __name__ == "__main__":
    main()
