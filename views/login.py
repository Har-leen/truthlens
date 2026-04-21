import streamlit as st
from utils.auth import login_user


def show():
    st.title(" Login to TruthLens")
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        with st.form("login_form"):
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")
            submitted = st.form_submit_button("Login", use_container_width=True)

        if submitted:
            if not username or not password:
                st.error("Please fill in all fields.")
            else:
                ok, result = login_user(username, password)
                if ok:
                    st.session_state["logged_in"] = True
                    st.session_state["user"] = result
                    st.success(f"Welcome back, {result['username']}!")
                    st.rerun()
                else:
                    st.error(result)
