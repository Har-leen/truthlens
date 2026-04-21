import streamlit as st
import pandas as pd
from utils.analysis_db import get_stats, get_all_analyses_admin, delete_analysis
from utils.auth import get_all_users, delete_user, update_user_role


def show():
    user = st.session_state["user"]
    if user["role"] != "admin":
        st.error("Access denied.")
        return

    st.title(" Admin Dashboard")

    stats = get_stats()
    c1, c2, c3, c4, c5 = st.columns(5)
    c1.metric("Total Analyses", stats["total"])
    c2.metric(" Fake",        stats["fake"])
    c3.metric(" Real",        stats["real"])
    c4.metric(" Users",       stats["users"])
    c5.metric(" Public Posts",stats["public"])

    st.divider()
    tab1, tab2 = st.tabs([" Manage Users", " Manage Analyses"])

    # ── Users ──────────────────────────────────────────────────────────────
    with tab1:
        st.subheader("All Users")
        users = get_all_users()
        if not users:
            st.info("No users found.")
        else:
            for u in users:
                col1, col2, col3, col4 = st.columns([3, 2, 2, 1])
                col1.write(f"**{u['username']}** ({u['email']})")
                col2.write(u["role"].capitalize())
                col3.write(str(u["created_at"])[:10])
                with col4:
                    if u["id"] != user["id"]:
                        if st.button("", key=f"del_user_{u['id']}", help="Delete user"):
                            delete_user(u["id"])
                            st.rerun()

                # Role toggle
                if u["id"] != user["id"]:
                    new_role = "admin" if u["role"] == "user" else "user"
                    if st.button(
                        f"Make {new_role.capitalize()}",
                        key=f"role_{u['id']}",
                        use_container_width=False,
                    ):
                        update_user_role(u["id"], new_role)
                        st.success(f"{u['username']} is now {new_role}.")
                        st.rerun()
                st.divider()

    # ── Analyses ────────────────────────────────────────────────────────────
    with tab2:
        st.subheader("All Analyses (latest 200)")
        analyses = get_all_analyses_admin()
        if not analyses:
            st.info("No analyses yet.")
        else:
            rows = []
            for a in analyses:
                rows.append({
                    "ID":         a["id"],
                    "User":       a["username"],
                    "Title":      a["title"][:60] if a["title"] else "",
                    "Prediction": a["prediction"],
                    "Confidence": f"{a['confidence']*100:.1f}%",
                    "Public":     "Yes" if a["is_public"] else "No",
                    "Date":       str(a["created_at"])[:10],
                })
            df = pd.DataFrame(rows)
            st.dataframe(df, use_container_width=True, hide_index=True)

            st.markdown("#### Delete an Analysis")
            del_id = st.number_input("Enter Analysis ID to delete", min_value=1, step=1)
            if st.button("Delete Analysis", type="primary"):
                delete_analysis(int(del_id))
                st.success(f"Analysis {del_id} deleted.")
                st.rerun()
