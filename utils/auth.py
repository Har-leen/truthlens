import hashlib
import streamlit as st
from utils.db import get_connection


def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()


def init_session():
    if "logged_in" not in st.session_state:
        st.session_state["logged_in"] = False
    if "user" not in st.session_state:
        st.session_state["user"] = None


def register_user(username: str, email: str, password: str, role: str = "user") -> tuple[bool, str]:
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute(
            "INSERT INTO users (username, email, password, role) VALUES (%s, %s, %s, %s)",
            (username, email, hash_password(password), role),
        )
        conn.commit()
        return True, "Registered successfully."
    except Exception as e:
        return False, str(e)
    finally:
        cur.close()
        conn.close()


def login_user(username: str, password: str) -> tuple[bool, dict | str]:
    conn = get_connection()
    cur = conn.cursor(dictionary=True)
    try:
        cur.execute(
            "SELECT * FROM users WHERE username = %s AND password = %s",
            (username, hash_password(password)),
        )
        user = cur.fetchone()
        if user:
            return True, user
        return False, "Invalid username or password."
    finally:
        cur.close()
        conn.close()


def get_all_users():
    conn = get_connection()
    cur = conn.cursor(dictionary=True)
    cur.execute("SELECT id, username, email, role, created_at FROM users ORDER BY created_at DESC")
    users = cur.fetchall()
    cur.close()
    conn.close()
    return users


def delete_user(user_id: int):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM users WHERE id = %s", (user_id,))
    conn.commit()
    cur.close()
    conn.close()


def update_user_role(user_id: int, new_role: str):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("UPDATE users SET role = %s WHERE id = %s", (new_role, user_id))
    conn.commit()
    cur.close()
    conn.close()
