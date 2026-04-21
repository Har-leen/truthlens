import streamlit as st
from utils.analysis_db import get_user_history, publish_analysis, delete_analysis


def show():
    st.title(" My Analysis History")
    user = st.session_state["user"]

    history = get_user_history(user["id"])

    if not history:
        st.info("You haven't analyzed any articles yet. Head to the Analyze tab!")
        return

    fake_count = sum(1 for h in history if h["prediction"] == "FAKE")
    real_count = len(history) - fake_count

    c1, c2, c3 = st.columns(3)
    c1.metric("Total Analyses", len(history))
    c2.metric(" Fake", fake_count)
    c3.metric(" Real", real_count)

    st.divider()

    # Filter
    filter_opt = st.selectbox("Filter", ["All", "FAKE", "REAL"])

    shown = [h for h in history if filter_opt == "All" or h["prediction"] == filter_opt]

    for item in shown:
        icon = "🚨" if item["prediction"] == "FAKE" else "✅"
        pub  = " Public" if item["is_public"] else " Private"
        with st.expander(
            f"{icon} {item['title']}  —  {item['confidence']*100:.0f}% confidence  |  {pub}  |  {str(item['created_at'])[:10]}"
        ):
            st.markdown(f"**Snippet:** {item['text_snippet']}")
            colA, colB = st.columns(2)
            colA.metric("Prediction",  item["prediction"])
            colB.metric("Confidence", f"{item['confidence']*100:.1f}%")

            if not item["is_public"] and item["prediction"] == "FAKE":
                if st.button(" Publish for Community Review", key=f"pub_{item['id']}"):
                    publish_analysis(item["id"])
                    st.success("Published!")
                    st.rerun()

            if st.button(" Delete", key=f"del_{item['id']}"):
                delete_analysis(item["id"])
                st.warning("Deleted.")
                st.rerun()
