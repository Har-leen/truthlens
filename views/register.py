import re
import streamlit as st
from utils.auth import register_user


def is_valid_email(email: str) -> bool:
    """Check email has format: something@something.something"""
    pattern = r'^[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None


def show():
    st.title(" Create an Account")
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        with st.form("register_form"):
            username = st.text_input("Username")
            email    = st.text_input("Email", placeholder="example@domain.com")
            password = st.text_input("Password", type="password")
            confirm  = st.text_input("Confirm Password", type="password")
            submitted = st.form_submit_button("Register", use_container_width=True)

        if submitted:
            if not username or not email or not password:
                st.error("Please fill in all fields.")
            elif not is_valid_email(email):
                st.error("Please enter a valid email address (e.g. abc@example.com).")
            elif password != confirm:
                st.error("Passwords do not match.")
            elif len(password) < 6:
                st.error("Password must be at least 6 characters.")
            else:
                ok, msg = register_user(username, email, password)
                if ok:
                    st.success("Account created! Please log in.")
                else:
                    if "Duplicate" in msg:
                        st.error("Username or email already exists.")
                    else:
                        st.error(f"Registration failed: {msg}")
