import sqlite3

def init_db():
    conn = sqlite3.connect("users.db")
    cur = conn.cursor()
    cur.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE,
            email TEXT UNIQUE,
            password TEXT,
            face_descriptor BLOB
        )
    ''')
    conn.commit()
    conn.close()

def insert_user(username, email, password, descriptor_blob):
    conn = sqlite3.connect("users.db")
    cur = conn.cursor()
    sql = "INSERT INTO users (username, email, password, face_descriptor) VALUES (?, ?, ?, ?)"
    cur.execute(sql, (username, email, password, descriptor_blob))
    conn.commit()
    conn.close()

def get_all_users():
    conn = sqlite3.connect("users.db")
    cur = conn.cursor()
    cur.execute("SELECT * FROM users")
    rows = cur.fetchall()
    conn.close()
    return rows

def get_user_by_email(email):
    conn = sqlite3.connect("users.db")
    cur = conn.cursor()
    cur.execute("SELECT * FROM users WHERE email=?", (email,))
    user = cur.fetchone()
    conn.close()
    return user
