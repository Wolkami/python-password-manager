import sqlite3
from core.cypher import encrypt, decrypt
import hashlib


# Функции для работы с базой данных
def add_account(service, username, password, key):
    encrypted_password = encrypt(password, key)
    conn = sqlite3.connect('passwords.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO accounts (service, username, password) VALUES (?, ?, ?)',
                   (service, username, encrypted_password))
    conn.commit()
    conn.close()


def get_account(service, key):
    conn = sqlite3.connect('passwords.db')
    cursor = conn.cursor()
    cursor.execute('SELECT username, password FROM accounts WHERE service = ?', (service,))
    result = cursor.fetchone()
    conn.close()
    if result:
        username, encrypted_password = result
        password = decrypt(encrypted_password, key)
        return username, password
    else:
        return None


def delete_account(service):
    conn = sqlite3.connect('passwords.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM accounts WHERE service = ?', (service,))
    conn.commit()
    conn.close()


def list_accounts():
    conn = sqlite3.connect('passwords.db')
    cursor = conn.cursor()
    cursor.execute('SELECT service, username FROM accounts')
    result = cursor.fetchall()
    conn.close()
    return result


def set_master_password(master_password):
    key = hashlib.sha256(master_password.encode()).digest()
    encrypted_password = encrypt(master_password, key)
    conn = sqlite3.connect('passwords.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO master (password) VALUES (?)', (encrypted_password,))
    conn.commit()
    conn.close()


def verify_master_password(master_password):
    conn = sqlite3.connect('passwords.db')
    cursor = conn.cursor()
    cursor.execute('SELECT password FROM master')
    result = cursor.fetchone()
    conn.close()
    if result:
        encrypted_password = result[0]
        key = hashlib.sha256(master_password.encode()).digest()
        try:
            decrypted_password = decrypt(encrypted_password, key)
            return decrypted_password == master_password
        except:
            return False
    else:
        return False
