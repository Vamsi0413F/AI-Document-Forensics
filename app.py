import streamlit as st
from frontend.dashboard import render_dashboard
from storage.database import init_db

# Configure Streamlit application
st.set_page_config(
    page_title="VERIDOC — AI Document Forensics",
    page_icon="🔎",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Initialize database
init_db()

# Render main dashboard
if __name__ == "__main__":
    render_dashboard()
