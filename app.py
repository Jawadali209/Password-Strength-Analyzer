import pandas as pd
import streamlit as st
import plotly.express as px

from analyzer import analyze_password
from simulator import simulate_cracking
from config import DATASET_FILE

st.set_page_config(
    page_title="Password Strength Analyzer",
    page_icon="🔐",
    layout="wide",
    initial_sidebar_state="expanded",
)

STRENGTH_COLORS = {
    "Very Weak": "#d62728",
    "Weak": "#ff7f0e",
    "Moderate": "#f2c744",
    "Strong": "#2ca02c",
    "Excellent": "#1f77b4",
}

# Sidebar
st.sidebar.title("🔐 Password Analyzer")
st.sidebar.markdown("---")
st.sidebar.info(
    "An educational tool that evaluates password strength and runs a "
    "controlled simulation of password guessing."
)
st.sidebar.markdown("---")
st.sidebar.warning(
    "Ethical use only. No real accounts or systems are attacked. "
    "Do not enter a password you actually use."
)
st.sidebar.success("Developed for Educational Purposes")

# Header
st.markdown(
    "<h1 style='text-align:center;color:#1f77b4;'>🔐 Password Strength Analyzer</h1>"
    "<p style='text-align:center;color:gray;font-size:18px;'>"
    "Password Strength Analyzer and Cracking Simulation Tool</p>",
    unsafe_allow_html=True,
)

tab_analyze, tab_simulate, tab_data, tab_about = st.tabs(
    ["🔎 Analyzer", "🧪 Cracking Simulation", "📊 Dataset Analytics", "ℹ️ About"]
)

# Analyzer tab
with tab_analyze:
    password = st.text_input(
        "Enter a password to analyze",
        type="password",
        placeholder="Type a sample password here...",
    )

    if st.button("Analyze Password"):
        if not password.strip():
            st.warning("Please enter a password.")
        else:
            report = analyze_password(password)
            color = STRENGTH_COLORS.get(report["Strength"], "#1f77b4")

            st.subheader("Password Score")
            st.progress(report["Score"] / 100)
            st.markdown(
                f"<h3 style='color:{color};'>{report['Score']} / 100 — "
                f"{report['Strength']}</h3>",
                unsafe_allow_html=True,
            )
            st.markdown("---")

            c1, c2, c3, c4 = st.columns(4)
            c1.metric("Strength", report["Strength"])
            c2.metric("Entropy", f"{report['Entropy']} bits")
            c3.metric("Attack Type", report["Attack Type"])
            c4.metric("Crack Time", report["Estimated Crack Time"])

            st.markdown("---")
            st.subheader("Password Statistics")
            stats = report["Statistics"]
            st.dataframe(
                pd.DataFrame({"Metric": stats.keys(), "Value": stats.values()}),
                hide_index=True,
            )

            st.subheader("Weaknesses")
            if report["Weaknesses"]:
                for w in report["Weaknesses"]:
                    st.error(w)
            else:
                st.success("No weaknesses found.")

            st.subheader("Recommendations")
            for rec in report["Recommendations"]:
                st.info(rec)

# Cracking simulation tab
with tab_simulate:
    st.markdown(
        "This runs a controlled, educational simulation. Nothing is sent "
        "anywhere and no real system is contacted."
    )
    sim_password = st.text_input(
        "Enter a password to simulate an attack on",
        type="password",
        placeholder="Type a sample password here...",
        key="sim_input",
    )

    if st.button("Run Cracking Simulation"):
        if not sim_password.strip():
            st.warning("Please enter a password.")
        else:
            result = simulate_cracking(sim_password)
            d = result["dictionary"]
            b = result["brute_force"]

            c1, c2, c3 = st.columns(3)
            c1.metric("Entropy", f"{result['entropy_bits']} bits")
            c2.metric("Attack Type", result["attack_type"])
            c3.metric("Estimated Time", result["estimated_time"])

            st.markdown("---")
            st.subheader("1. Dictionary Attack (word + common mutations)")
            if d["cracked"]:
                st.error(f"Cracked in ~{d['guesses']:,} guesses ({d['time_label']}). {d['note']}")
            else:
                st.success(f"Not cracked within {d['guesses']:,} common-mutation guesses. {d['note']}")

            st.subheader("2. Brute-Force Estimate")
            st.write(
                f"Character pool: **{b['character_pool']}** · "
                f"Theoretical search space: **{b['search_space']:.2e}** combinations"
            )
            st.info(f"Realistic crack time (after detecting patterns): **{b['time_label']}**")
            st.caption(
                "The realistic time uses effective entropy, so a large search space "
                "can still be guessed quickly if the password has predictable patterns. "
                "Assumes about 1 billion guesses per second (educational estimate)."
            )

# Dataset analytics tab
with tab_data:
    st.subheader("Sample Dataset Analytics")
    try:
        df = pd.read_csv(DATASET_FILE)
        st.caption(f"Total sample passwords: {len(df)}")

        col1, col2 = st.columns(2)
        with col1:
            dist = df["Actual Strength"].value_counts().reset_index()
            dist.columns = ["Strength", "Count"]
            fig1 = px.bar(
                dist, x="Strength", y="Count", color="Strength",
                color_discrete_map=STRENGTH_COLORS,
                title="Passwords by Strength Band",
            )
            st.plotly_chart(fig1)

        with col2:
            fig2 = px.scatter(
                df, x="Effective Entropy", y="Score", color="Actual Strength",
                color_discrete_map=STRENGTH_COLORS, hover_data=["Category"],
                title="Score vs Effective Entropy",
            )
            st.plotly_chart(fig2)

        fig3 = px.histogram(
            df, x="Attack Type", color="Actual Strength",
            color_discrete_map=STRENGTH_COLORS,
            title="Predicted Attack Type by Strength",
        )
        st.plotly_chart(fig3)

        st.dataframe(df.head(20), hide_index=True)
    except FileNotFoundError:
        st.warning(f"{DATASET_FILE} not found. Run generate_dataset.py first.")

# About tab
with tab_about:
    st.markdown(
        """
### About This Project

This tool evaluates password security using multiple explainable techniques
and demonstrates, in a safe controlled setting, why weak passwords are easy
to guess.

**Analysis:** strength scoring, entropy and effective entropy, dictionary /
keyboard / sequential / repeated-pattern detection, statistics, recommendations,
attack-type prediction and crack-time estimation.

**Simulation:** controlled dictionary attack and brute-force estimation.

**Ethical boundary:** only synthetic sample data and user-supplied input are
used. No real accounts, systems or leaked password lists are attacked.

**Technologies:** Python, Streamlit, Pandas, NumPy, Plotly.
"""
    )

st.markdown(
    "<div style='text-align:center;padding:15px;color:gray;'>"
    "Password Strength Analyzer &copy; 2026 · Built with Python & Streamlit"
    "</div>",
    unsafe_allow_html=True,
)
