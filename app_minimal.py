import streamlit as st
import json
import os
from datetime import datetime
import pandas as pd

# Initialize data directories
def init_data_dirs():
    """Initialize data directories and files"""
    os.makedirs("data", exist_ok=True)
    
    # Initialize empty data files if they don't exist
    files = [
        "data/users.json",
        "data/blood_inventory.json", 
        "data/donations.json",
        "data/requests.json",
        "data/blood_banks.json",
        "data/otps.json",
        "data/notifications.json",
        "data/request_responses.json"
    ]
    
    for file_path in files:
        if not os.path.exists(file_path):
            if "blood_banks.json" in file_path:
                sample_data = [
                    {"name": "City Blood Bank", "lat": 28.6139, "lng": 77.2090, "address": "Delhi, India", "contact": "+91-9876543210"}
                ]
            elif "blood_inventory.json" in file_path:
                sample_data = {
                    "A+": 0, "A-": 0, "B+": 0, "B-": 0,
                    "AB+": 0, "AB-": 0, "O+": 0, "O-": 0
                }
            elif "otps.json" in file_path:
                sample_data = {}
            else:
                sample_data = []
            
            with open(file_path, 'w') as f:
                json.dump(sample_data, f, indent=2)

def main():
    st.set_page_config(
        page_title="Blood Bank Management System",
        page_icon="🩸",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Initialize data
    init_data_dirs()
    
    # Initialize session state
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False
    if 'user_type' not in st.session_state:
        st.session_state.user_type = None
    if 'username' not in st.session_state:
        st.session_state.username = None
    
    # Main header
    st.title("🩸 Blood Bank Management System")
    st.markdown("---")
    
    # Simple test interface
    st.write("Application is loading...")
    
    # Test login interface
    if not st.session_state.logged_in:
        st.subheader("Login Test")
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        user_type = st.selectbox("User Type", ["donor", "receiver"])
        
        if st.button("Login"):
            if username and password:
                st.session_state.logged_in = True
                st.session_state.username = username
                st.session_state.user_type = user_type
                st.success("Login successful!")
                st.rerun()
            else:
                st.error("Please fill in all fields")
    else:
        st.success(f"Welcome, {st.session_state.username}!")
        if st.button("Logout"):
            st.session_state.logged_in = False
            st.session_state.username = None
            st.session_state.user_type = None
            st.rerun()

if __name__ == "__main__":
    main()