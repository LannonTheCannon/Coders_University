import streamlit as st
import hmac
import sqlite3
from datetime import datetime
import hashlib


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
    conn.commit()
    conn.close()


def hash_password(password: str) -> str:
    """Hash password using SHA256"""
    return hashlib.sha256(password.encode()).hexdigest()


def verify_password(password: str, hash: str) -> bool:
    """Verify password against hash"""
    return hmac.compare_digest(hash_password(password), hash)


def add_user(username: str, password: str):
    """Add new user to database"""
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    try:
        c.execute(
            "INSERT INTO users (username, password_hash) VALUES (?, ?)",
            (username, hash_password(password))
        )
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()


def verify_user(username: str, password: str) -> bool:
    """Verify user credentials"""
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute("SELECT password_hash FROM users WHERE username = ?", (username,))
    result = c.fetchone()
    conn.close()

    if result is None:
        return False
    return verify_password(password, result[0])


def login_page():
    """Display login page"""
    st.title("Login")

    # Check if user is already logged in
    if 'logged_in' in st.session_state and st.session_state.logged_in:
        st.success(f"Already logged in as {st.session_state.username}")
        if st.button("Logout"):
            st.session_state.logged_in = False
            st.session_state.username = None
            st.rerun()
        return True

    # Login form
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    col1, col2 = st.columns(2)
    with col1:
        if st.button("Login"):
            if verify_user(username, password):
                st.session_state.logged_in = True
                st.session_state.username = username
                st.success("Logged in successfully!")
                st.rerun()
            else:
                st.error("Invalid username or password")

    with col2:
        if st.button("Register"):
            if username and password:
                if add_user(username, password):
                    st.success("Registration successful! Please login.")
                else:
                    st.error("Username already exists")
            else:
                st.error("Please enter both username and password")

    return False


def main():
    # Initialize session state
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False
        st.session_state.username = None

    # Initialize database
    init_db()

    # Show login page
    if not login_page():
        return

    # Main app content (only shown when logged in)
    st.title("Protected Content")
    st.write(f"Welcome {st.session_state.username}! This is the protected content of your app.")

    # Add your protected app content here
    st.write("Add your protected Streamlit app content here...")


if __name__ == "__main__":
    main()