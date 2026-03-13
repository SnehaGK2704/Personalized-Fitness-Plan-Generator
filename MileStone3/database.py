import sqlite3


def get_db():
    return sqlite3.connect("database.db", timeout=10)


def create_tables():

    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        email TEXT UNIQUE,
        password TEXT,
        name TEXT,
        age INTEGER,
        height REAL,
        weight REAL
    )
    """)

    conn.commit()
    conn.close()