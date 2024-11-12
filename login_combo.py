import streamlit as st
import hmac
import sqlite3
from datetime import datetime
import hashlib
import json


def init_db():
    """Initialize SQLite database with users table"""
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS users
        (username TEXT PRIMARY KEY,
         password_hash TEXT NOT NULL,
         created_at DATETIME DEFAULT CURRENT_TIMESTAMP)
    ''')

    # Add student_data table with correct schema
    c.execute('''
        CREATE TABLE IF NOT EXISTS student_data
        (username TEXT PRIMARY KEY,
         progress TEXT,
         achievements TEXT,
         current_module TEXT,
         test_scores TEXT,
         FOREIGN KEY (username) REFERENCES users(username))
    ''')
    conn.commit()
    conn.close()


def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()


def verify_password(password: str, hash: str) -> bool:
    return hmac.compare_digest(hash_password(password), hash)


def add_user(username: str, password: str):
    """Add new user and initialize their student data"""
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    try:
        c.execute("BEGIN")
        c.execute(
            "INSERT INTO users (username, password_hash) VALUES (?, ?)",
            (username, hash_password(password))
        )

        # Initialize student data
        initial_data = {
            'progress': {
                'python_basics': 0,
                'functions': 0,
                'web_dev': 0,
                'ai_integration': 0
            },
            'achievements': [],
            'current_module': 'Python Basics',
            'test_scores': []
        }

        c.execute(
            """INSERT INTO student_data 
               (username, progress, achievements, current_module, test_scores) 
               VALUES (?, ?, ?, ?, ?)""",
            (username,
             json.dumps(initial_data['progress']),
             json.dumps(initial_data['achievements']),
             initial_data['current_module'],
             json.dumps(initial_data['test_scores']))
        )

        conn.commit()
        return True
    except sqlite3.IntegrityError:
        conn.rollback()
        return False
    finally:
        conn.close()


def verify_user(username: str, password: str) -> bool:
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute("SELECT password_hash FROM users WHERE username = ?", (username,))
    result = c.fetchone()
    conn.close()

    if result is None:
        return False
    return verify_password(password, result[0])


def get_student_data(username: str):
    """Retrieve student data from database"""
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute("""
        SELECT progress, achievements, current_module, test_scores 
        FROM student_data 
        WHERE username = ?
    """, (username,))
    result = c.fetchone()
    conn.close()

    if result:
        return {
            'name': username,  # Use username as name
            'progress': json.loads(result[0]),
            'achievements': json.loads(result[1]),
            'current_module': result[2],
            'test_scores': json.loads(result[3])
        }
    return None


def update_student_data(username: str, data_type: str, new_data):
    """Update specific student data"""
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    try:
        if data_type in ['progress', 'achievements', 'test_scores']:
            c.execute(f"UPDATE student_data SET {data_type} = ? WHERE username = ?",
                      (json.dumps(new_data), username))
        elif data_type == 'current_module':
            c.execute("UPDATE student_data SET current_module = ? WHERE username = ?",
                      (new_data, username))
        conn.commit()
        return True
    except:
        return False
    finally:
        conn.close()


def login_page():
    """Display login page"""
    st.title("Student Portal Login")

    if 'logged_in' in st.session_state and st.session_state.logged_in:
        return True

    with st.container():
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")

        col1, col2 = st.columns(2)
        with col1:
            if st.button("Login", key="login_button"):
                if verify_user(username, password):
                    # Initialize all session state variables
                    st.session_state.logged_in = True
                    st.session_state.username = username
                    st.session_state.student_data = {
                        username: get_student_data(username)
                    }
                    st.success("Logged in successfully!")
                    st.rerun()
                else:
                    st.error("Invalid username or password")

        with col2:
            if st.button("Register", key="register_button"):
                if username and password:
                    if add_user(username, password):
                        st.success("Registration successful! Please login.")
                    else:
                        st.error("Username already exists")
                else:
                    st.error("Please enter both username and password")

    return False