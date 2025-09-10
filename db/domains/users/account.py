'''
# db/database.py
import sqlite3
import os

DB_NAME = "db/database.db"

# DB 연결 헬퍼 함수
def get_connection():
    conn = sqlite3.connect(DB_NAME, timeout=10, check_same_thread=False)
    conn.row_factory = sqlite3.Row  # dict처럼 접근 가능
    return conn


# DB 초기화
def init_db():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            salt TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """
    )
    conn.commit()
    conn.close()


# 유저 추가
def add_user(username, password, salt=None):
    # salt 없으면 랜덤 생성
    if not salt:
        salt = os.urandom(16).hex()

    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO users (username, password, salt) VALUES (?, ?, ?)",
            (username, password, salt),
        )
        conn.commit()
        return True
    except Exception as e:
        print("DB error:", e)
        return False
    finally:
        conn.close()


# 유저 조회
def get_user_by_id(username: str):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
    user = cursor.fetchone()
    conn.close()
    return user


# 비밀번호 업데이트
def update_password(username: str, new_password: str, new_salt: str = None):
    if not new_salt:
        new_salt = os.urandom(16).hex()

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE users SET password = ?, salt = ? WHERE username = ?",
        (new_password, new_salt, username),
    )
    conn.commit()
    conn.close()


# 유저 삭제
def delete_user(username: str):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM users WHERE username = ?", (username,))
    conn.commit()
    conn.close()
