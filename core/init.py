import sqlite3


# Инициализация базы данных
def init_db():
    conn = sqlite3.connect('passwords.db')
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS accounts (
        id INTEGER PRIMARY KEY,
        service TEXT NOT NULL,
        username TEXT NOT NULL,
        password BLOB NOT NULL
    )
    ''')
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS master (
        id INTEGER PRIMARY KEY,
        password BLOB NOT NULL
    )
    ''')
    conn.commit()
    conn.close()
