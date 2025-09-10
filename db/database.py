import sqlite3
import os
import bcrypt


DB_NAME = os.path.join(os.path.dirname(os.path.abspath(__file__)), "database.db")

def get_connection():
    conn = sqlite3.connect(DB_NAME, timeout=10, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    """)
    conn.commit()
    conn.close()

def add_user(username, password):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        # bcrypt 해시 생성
        hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
        cursor.execute(
            "INSERT INTO users (username, password) VALUES (?, ?)",
            (username, hashed.decode())
        )
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        # 이미 존재하는 사용자
        return False
    finally:
        conn.close()

def get_user_by_id(username: str):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
    user = cursor.fetchone()
    conn.close()
    return user

def verify_user(username: str, password_input: str) -> bool:
    user = get_user_by_id(username)
    if not user:
        return False
    stored_hash = user["password"]
    return bcrypt.checkpw(password_input.encode(), stored_hash.encode())
