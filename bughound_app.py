import os
import difflib
import streamlit as st
from dotenv import load_dotenv
from bughound_agent import BugHoundAgent
from llm_client import GeminiClient, MockClient

# ----------------------------
# App setup
# ----------------------------
# Load environment variables from .env if present
# WK09 Part 4–5: Local web UI for BugHound


load_dotenv()

st.set_page_config(page_title="BugHound", layout="wide")
st.title("🐶 BugHound")
st.caption("A cautious agent that analyzes code and defers when unsure.")

# Sidebar
st.sidebar.header("Settings")
mode_ui = st.sidebar.selectbox(
    "Mode",
    ["Heuristic only (no API)", "Gemini (requires API key)"]
)

agent_mode = "gemini" if mode_ui.startswith("Gemini") else "heuristic"

# Input
code = st.text_area("Paste Python code", height=300)
run = st.button("Run BugHound")

if run and code.strip():
    agent = BugHoundAgent(mode=agent_mode)
    result = agent.run(code)

    # Side-by-side issues
    st.subheader("Issue Comparison")
    c1, c2, c3 = st.columns(3)
    c1.json(result["issues_heuristic"])
    c2.json(result["issues_ai"])
    c3.json(result["issues_final"])

    # Fix
    st.subheader("Proposed Fix")
    st.code(result["fixed_code"], language="python")

    # Risk
    st.subheader("Risk Report")
    st.json(result["risk"])

    # Trace (color-coded)
    st.subheader("Agent Trace")
    COLORS = {
        "INFO": "gray",
        "ACCEPTED": "green",
        "REJECTED": "red",
        "LOCKED": "orange"
    }

    for t in result["logs"]:
        st.markdown(
            f"<span style='color:{COLORS.get(t['status'], 'black')}'>"
            f"[{t['stage']}] [{t['source']}] "
            f"[{t['status']}] {t['message']}</span>",
            unsafe_allow_html=True
        )

    # Export
    st.download_button(
        "Download Trace JSON",
        agent.export_trace_json(),
        file_name="bughound_trace.json"
    )