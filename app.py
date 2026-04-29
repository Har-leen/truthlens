import streamlit as st

st.set_page_config(
    page_title="TruthLens",
    page_icon="assets/logo.png", 
    layout="wide",
    initial_sidebar_state="expanded"
)
col1, col2 = st.columns([1, 5])

with col1:
    st.image("assets/logo.png", width=80)

# with col2:
    # st.title("TruthLens")

st.sidebar.image("assets/logo.png", width=120)
# st.sidebar.title("TruthLens")

from utils.auth import init_session
from views import home, analyze, community, history, admin, login, register

init_session()

PAGES = {
    "Home": home,
    "Analyze News": analyze,
    "Community Review": community,
    "My History": history,
}

ADMIN_PAGES = {
    "Admin Dashboard": admin,
}

with st.sidebar:
    # st.image("https://img.icons8.com/fluency/96/news.png", width=80)
    st.title("TruthLens")
    st.caption("AI-Powered Fake News Detector")
    st.divider()

    if st.session_state.get("logged_in"):
        user = st.session_state["user"]
        st.success(f"{user['username']}")
        st.caption(f"Role: {user['role'].capitalize()}")
        st.divider()

        nav_options = list(PAGES.keys())
        if user["role"] == "admin":
            nav_options += list(ADMIN_PAGES.keys())

        selected = st.radio("Navigate", nav_options, label_visibility="collapsed")

        st.divider()
        if st.button("Logout", use_container_width=True):
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.rerun()
    else:
        auth_choice = st.radio("", ["Login", "Register"], label_visibility="collapsed")
        selected = auth_choice

# Page router
if not st.session_state.get("logged_in"):
    if selected == "Login":
        login.show()
    else:
        register.show()
else:
    all_pages = {**PAGES, **ADMIN_PAGES}
    if selected in all_pages:
        all_pages[selected].show()
