import streamlit as st
from utils.analysis_db import (
    get_public_analyses, cast_vote, get_vote, add_comment, get_comments,
)


def show():
    st.title(" Community Review")
    st.caption("Browse AI-flagged fake news shared by users. Vote and discuss!")

    user = st.session_state["user"]
    posts = get_public_analyses(limit=50)

    if not posts:
        st.info("No public analyses yet. Be the first to share one from the Analyze tab!")
        return

    for post in posts:
        with st.expander(
            f"{'' if post['prediction']=='FAKE' else ''}  {post['title'] or '(untitled)'}  "
            f"— {post['confidence']*100:.0f}% confidence  |   Anonymous  |  🗓 {str(post['created_at'])[:10]}"
        ):
            st.markdown(f"> {post['text_snippet']}")

            col1, col2, col3 = st.columns(3)
            col1.metric("Prediction", post["prediction"])
            col2.metric("👍 Upvotes",   post["upvotes"])
            col3.metric("👎 Downvotes", post["downvotes"])

            my_vote = get_vote(post["id"], user["id"])

            v1, v2 = st.columns(2)
            with v1:
                up_label = f"👍 Agree ({post['upvotes']})" + (" ✔" if my_vote=="up" else "")
                if st.button(up_label, key=f"up_{post['id']}"):
                    cast_vote(post["id"], user["id"], "up")
                    st.rerun()
            with v2:
                dn_label = f"👎 Disagree ({post['downvotes']})" + (" ✔" if my_vote=="down" else "")
                if st.button(dn_label, key=f"dn_{post['id']}"):
                    cast_vote(post["id"], user["id"], "down")
                    st.rerun()

            st.markdown("** Discussion**")
            comments = get_comments(post["id"])
            if comments:
                for c in comments:
                    st.markdown(
                        f"<div style='background:#f0f2f6;padding:8px;border-radius:6px;margin:4px 0'>"
                        f"<b>Anonymous</b> · <small>{str(c['created_at'])[:16]}</small><br>{c['content']}"
                        f"</div>",
                        unsafe_allow_html=True,
                    )
            else:
                st.caption("No comments yet.")

            with st.form(key=f"comment_form_{post['id']}"):
                new_comment = st.text_input("Add a comment …", key=f"ctext_{post['id']}")
                if st.form_submit_button("Post"):
                    if new_comment.strip():
                        add_comment(post["id"], user["id"], new_comment.strip())
                        st.rerun()
                    else:
                        st.warning("Comment cannot be empty.")
