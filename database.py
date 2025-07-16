import sqlite3

DB_NAME = "UniHub_app.db"

def connect_db():
    conn = sqlite3.connect(DB_NAME)
    return conn

def init_db():
    create_tables()
    print(f"Database '{DB_NAME}' initialized successfully.")

def create_tables():
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute('''
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            personal_id TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    ''')
    cur.execute('''
        CREATE TABLE IF NOT EXISTS universities (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE,
            faculty TEXT,
            credits INTEGER,
            price REAL,
            places INTEGER
        )
    ''')
    
    cur.execute('''
        CREATE TABLE IF NOT EXISTS admin (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            code TEXT UNIQUE NOT NULL
        )
    ''')

    cur.execute('''
        CREATE TABLE IF NOT EXISTS admin_login (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            code TEXT UNIQUE NOT NULL
        )
    ''')
    conn.commit()  
    conn.close()



