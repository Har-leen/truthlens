import streamlit as st
from ml.predictor import predict
from utils.analysis_db import save_analysis, publish_analysis

MIN_WORDS = 30  # minimum words for reliable prediction

def show():
    st.markdown("## 🧠 Analyze News Article")
    st.caption("Detect whether a news article is fake or real using AI")
    user = st.session_state["user"]

    st.markdown("Paste a news article or upload a `.txt` file below.")

    tab1, tab2 = st.tabs([" Paste Text", " Upload File"])

    title = ""
    text  = ""

    with tab1:
        title = st.text_input("Headline / Title (optional)", key="title_paste")
        text  = st.text_area("News Article Text", height=250, key="text_paste",
                             placeholder="Paste the full article here …")

    with tab2:
        uploaded = st.file_uploader("Upload a .txt file", type=["txt"])
        if uploaded:
            content = uploaded.read().decode("utf-8", errors="ignore")
            lines   = content.strip().splitlines()
            title   = lines[0] if lines else ""
            text    = "\n".join(lines[1:]) if len(lines) > 1 else content
            st.text_area("File Content Preview", value=content[:1000] + ("…" if len(content) > 1000 else ""),
                         height=200, disabled=True)

    if st.button(" Analyze", use_container_width=True, type="primary"):
        if not text.strip():
            st.warning("Please provide some text to analyze.")
            return

        # ── Short text warning ──────────────────────────────────────────────
        word_count = len(text.strip().split())
        if word_count < MIN_WORDS:
            st.warning(
                f"⚠️ Your text is only **{word_count} word(s)** long. "
                f"For reliable results, please paste at least **{MIN_WORDS} words** "
                f"(a full news article or paragraph). "
                f"Short text often produces inaccurate predictions."
            )
            return
        # ───────────────────────────────────────────────────────────────────

        with st.spinner("Analyzing article …"):
            try:
                result = predict(title, text)
            except FileNotFoundError as e:
                st.error(str(e))
                return

        prediction  = result["prediction"]
        confidence  = result["confidence"]
        fake_prob   = result["fake_probability"]
        real_prob   = result["real_probability"]

        st.divider()
        st.subheader(" Analysis Result")

        col1, col2 = st.columns(2)
        with col1:
            if prediction == "FAKE":
                st.error(f"###  {prediction}")
            else:
                st.success(f"###  {prediction}")
        with col2:
            st.metric("Confidence", f"{confidence * 100:.1f}%")

        st.progress(fake_prob, text=f"Fake probability: {fake_prob*100:.1f}%")

        col3, col4 = st.columns(2)
        col3.metric(" Fake Probability", f"{fake_prob*100:.1f}%")
        col4.metric(" Real Probability", f"{real_prob*100:.1f}%")

        # ── Low confidence disclaimer ───────────────────────────────────────
        if confidence < 0.75:
            st.info(
                "ℹ️ The model's confidence is relatively low. "
                "Consider providing more text for a more accurate result."
            )
        # ───────────────────────────────────────────────────────────────────

        snippet = text[:300] + ("…" if len(text) > 300 else "")
        analysis_id = save_analysis(
            user_id=user["id"],
            title=title or "(untitled)",
            text_snippet=snippet,
            full_text=text,
            prediction=prediction,
            confidence=confidence,
            is_public=False,
        )
        # Save to session state so publish button can access it
        st.session_state["last_analysis_id"] = analysis_id
        st.session_state["last_prediction"] = prediction
        st.success("Result saved to your history.")

    # Publish button OUTSIDE the Analyze button block
    if st.session_state.get("last_prediction") == "FAKE" and st.session_state.get("last_analysis_id"):
        st.divider()
        st.markdown("#### 📢 Share for Community Review")
        st.caption("Allow other users to upvote/downvote and discuss this result.")
        if st.button("🌐 Publish for Public Review"):
            publish_analysis(st.session_state["last_analysis_id"])
            st.success("Published! Other users can now review it in the Community tab.")
            st.session_state["last_analysis_id"] = None
            st.session_state["last_prediction"] = None