import streamlit as st
import os
from dotenv import load_dotenv

load_dotenv()

# Model Identifier
MODEL_NAME = "gemini-3.1-flash-lite"

def get_api_key():
    """Retrieve API key from system environment or secrets."""
    return os.getenv("GOOGLE_API_KEY") or st.secrets.get("GOOGLE_API_KEY", "")

def inject_custom_css():
    """Applies UI styling."""
    st.markdown("""
        <style>
        /* Main background color tuning */
        .stApp { background-color: #0f111a; color: #f4f5f7; }
        
        /*Chat Input Box */
        .stChatInputContainer {
            background-color: #1e2235 !important;
            border-radius: 12px !important;
            border: 1px solid #3b4261 !important;
        }
        
        /* Sidebar styling */
        section[data-testid="stSidebar"] {
            background-color: #161925 !important;
            border-right: 1px solid #23283d;
        }
        
        /* Status Badges */
        .status-badge {
            padding: 4px 10px;
            border-radius: 20px;
            font-size: 0.8rem;
            font-weight: 600;
            background-color: #1e3a8a;
            color: #93c5fd;
        }
        </style>
    """, unsafe_allow_html=True)