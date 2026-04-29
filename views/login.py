import re
import streamlit as st
from utils.auth import login_user


def is_valid_email(email: str) -> bool:
    """Check email has format: something@something.something"""
    pattern = r'^[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None


def show():
    st.title(" Login to TruthLens")
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        with st.form("login_form"):
            username = st.text_input("Username")
            email    = st.text_input("Email", placeholder="example@domain.com")
            password = st.text_input("Password", type="password")
            submitted = st.form_submit_button("Login", use_container_width=True)

        if submitted:
            if not username or not email or not password:
                st.error("Please fill in all fields.")
            elif not is_valid_email(email):
                st.error("Please enter a valid email address (e.g. abc@example.com).")
            else:
                ok, result = login_user(username, password)
                if ok:
                    st.session_state["logged_in"] = True
                    st.session_state["user"] = result
                    st.success(f"Welcome back, {result['username']}!")
                    st.rerun()
                else:
                    st.error(result)
