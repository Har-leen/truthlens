import streamlit as st
from utils.analysis_db import get_stats


def show():
    st.title(" Welcome to TruthLens")
    st.subheader("AI-Powered Fake News Detection System")
    st.markdown("""
TruthLens helps you verify news articles in seconds using machine learning and
linguistic analysis. Paste any news text, get an instant prediction, and optionally
share your result with the community.
    """)

    st.divider()

    # Live stats
    try:
        stats = get_stats()
        c1, c2, c3, c4 = st.columns(4)
        c1.metric(" Total Analyses", stats["total"])
        c2.metric(" Fake News Found", stats["fake"])
        c3.metric(" Real News", stats["real"])
        c4.metric(" Users", stats["users"])
    except Exception:
        pass

    st.divider()

    st.markdown("### How It Works")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.info("**① Input**\nPaste news text or upload a `.txt` file")
    with col2:
        st.info("**② Analyze**\nML model scans linguistic patterns")
    with col3:
        st.info("**③ Result**\nFake/Real prediction with confidence %")
    with col4:
        st.info("**④ Community**\nOptionally share for public review")

    st.divider()
    st.markdown("""
**Key Features:**
- Instant fake-news probability score
- Supports text paste and `.txt` file upload
- Community voting on AI verdicts
- Discussion threads for shared articles
- Personal analysis history
    """)
