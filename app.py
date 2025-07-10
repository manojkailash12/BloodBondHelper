import streamlit as st
import json
import os
from datetime import datetime
import pandas as pd

# Import modules conditionally to avoid import errors
try:
    from dashboard import show_dashboard
    from auth import (
        login_user, logout_user, register_user,
        initiate_password_reset, reset_password
    )
    from blood_management import donate_blood, request_blood, get_blood_inventory, load_donations, load_requests
    from maps import show_blood_bank_map
    from request_management import get_pending_requests_for_donor, respond_to_request, get_requester_notifications
    from notifications import get_user_notifications
    IMPORTS_SUCCESS = True
except ImportError as e:
    IMPORTS_SUCCESS = False
    IMPORT_ERROR = str(e)

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
                # Initialize with some sample blood bank locations
                sample_data = [
                    {"name": "City Blood Bank", "lat": 28.6139, "lng": 77.2090, "address": "Delhi, India", "contact": "+91-9876543210"},
                    {"name": "Central Hospital Blood Bank", "lat": 19.0760, "lng": 72.8777, "address": "Mumbai, India", "contact": "+91-9876543211"},
                    {"name": "Metro Blood Center", "lat": 12.9716, "lng": 77.5946, "address": "Bangalore, India", "contact": "+91-9876543212"},
                    {"name": "Regional Blood Bank", "lat": 13.0827, "lng": 80.2707, "address": "Chennai, India", "contact": "+91-9876543213"}
                ]
            elif "blood_inventory.json" in file_path:
                # Initialize blood inventory
                sample_data = {
                    "A+": 0, "A-": 0, "B+": 0, "B-": 0,
                    "AB+": 0, "AB-": 0, "O+": 0, "O-": 0
                }
            elif "otps.json" in file_path:
                sample_data = {}
            elif "notifications.json" in file_path or "request_responses.json" in file_path:
                sample_data = []
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
    if 'reset_step' not in st.session_state:
        st.session_state.reset_step = 1
    
    # Main header
    st.title("🩸 Blood Bank Management System")
    st.markdown("---")
    
    # Check if imports succeeded
    if not IMPORTS_SUCCESS:
        st.error(f"Import error: {IMPORT_ERROR}")
        st.info("Please check that all required modules are available.")
        return
    
    # Sidebar navigation
    if st.session_state.logged_in:
        st.sidebar.success(f"Welcome, {st.session_state.username}!")
        st.sidebar.markdown(f"**Role:** {st.session_state.user_type.title()}")
        
        if st.sidebar.button("Logout"):
            logout_user()
            st.rerun()
        
        st.sidebar.markdown("---")
        
        # Navigation menu
        if st.session_state.user_type == "donor":
            menu_options = ["Dashboard", "Donate Blood", "Blood Requests", "Blood Bank Map", "My Donations", "My Notifications"]
        elif st.session_state.user_type == "receiver":
            menu_options = ["Dashboard", "Request Blood", "Blood Bank Map", "My Requests", "Request Responses", "My Notifications"]
        else:
            menu_options = ["Dashboard", "Blood Bank Map", "My Notifications"]
            
        selected_page = st.sidebar.selectbox("Navigation", menu_options)
        
        # Main content area
        if selected_page == "Dashboard":
            show_dashboard()
        elif selected_page == "Donate Blood":
            donate_blood_page()
        elif selected_page == "Request Blood":
            request_blood_page()
        elif selected_page == "Blood Requests":
            show_blood_requests_for_donor()
        elif selected_page == "Request Responses":
            show_request_responses()
        elif selected_page == "Blood Bank Map":
            show_blood_bank_map()
        elif selected_page == "My Donations":
            show_my_donations()
        elif selected_page == "My Requests":
            show_my_requests()
        elif selected_page == "My Notifications":
            show_my_notifications()
    else:
        # Login/Register interface
        auth_tab1, auth_tab2, auth_tab3 = st.tabs(["Login", "Register", "Forgot Password"])
        
        with auth_tab1:
            login_form()
        
        with auth_tab2:
            register_form()
        
        with auth_tab3:
            forgot_password_form()

def login_form():
    """Display login form"""
    st.subheader("Login to Your Account")
    
    with st.form("login_form"):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        user_type = st.selectbox("I am a:", ["donor", "receiver"])
        
        submitted = st.form_submit_button("Login")
        
        if submitted:
            if username and password:
                if login_user(username, password, user_type):
                    st.success("Login successful!")
                    st.rerun()
                else:
                    st.error("Invalid credentials or user type mismatch.")
            else:
                st.error("Please fill in all fields.")

def register_form():
    """Display registration form"""
    st.subheader("Create New Account")
    
    with st.form("register_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            username = st.text_input("Username")
            email = st.text_input("Email")
            phone = st.text_input("Phone Number")
            
        with col2:
            password = st.text_input("Password", type="password")
            confirm_password = st.text_input("Confirm Password", type="password")
            user_type = st.selectbox("I want to:", ["donor", "receiver"])
        
        # Additional fields for donors
        if user_type == "donor":
            st.markdown("**Additional Information for Donors:**")
            col3, col4 = st.columns(2)
            with col3:
                blood_group = st.selectbox("Blood Group", ["A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"])
            with col4:
                age = st.number_input("Age", min_value=18, max_value=65, value=25)
        else:
            blood_group = None
            age = None
        
        submitted = st.form_submit_button("Create Account")
        
        if submitted:
            if username and email and phone and password and confirm_password:
                if password != confirm_password:
                    st.error("Passwords do not match.")
                elif len(password) < 6:
                    st.error("Password must be at least 6 characters long.")
                else:
                    result = register_user(username, email, phone, password, user_type, blood_group, age)
                    if result['success']:
                        st.success("🎉 Registration successful! Please login to continue.")
                        st.balloons()
                    else:
                        st.error(f"Registration failed: {result['error']}")
            else:
                st.error("Please fill in all required fields.")

def forgot_password_form():
    """Display forgot password form"""
    st.subheader("Reset Your Password")
    
    if st.session_state.reset_step == 1:
        st.markdown("### Step 1: Enter Email")
        
        with st.form("email_form"):
            email = st.text_input("Enter your registered email address")
            submitted = st.form_submit_button("Send Reset Instructions")
            
            if submitted:
                if email:
                    result = initiate_password_reset(email)
                    if result['success']:
                        st.success(result['message'])
                        st.session_state.reset_email = email
                        st.session_state.reset_step = 2
                        st.info(f"Reset Token: {result['token']}")
                        st.rerun()
                    else:
                        st.error(result['error'])
                else:
                    st.error("Please enter your email address.")
    
    elif st.session_state.reset_step == 2:
        st.markdown("### Step 2: Enter Reset Token")
        st.info(f"Reset instructions sent to: {st.session_state.reset_email}")
        
        with st.form("reset_form"):
            token = st.text_input("Enter Reset Token")
            new_password = st.text_input("New Password", type="password")
            confirm_password = st.text_input("Confirm New Password", type="password")
            
            submitted = st.form_submit_button("Reset Password")
            
            if submitted:
                if token and new_password and confirm_password:
                    if new_password != confirm_password:
                        st.error("Passwords do not match.")
                    elif len(new_password) < 6:
                        st.error("Password must be at least 6 characters long.")
                    else:
                        result = reset_password(st.session_state.reset_email, token, new_password)
                        if result['success']:
                            st.success("Password reset successful! Please login with your new password.")
                            st.session_state.reset_step = 1
                            st.balloons()
                        else:
                            st.error(result['error'])
                else:
                    st.error("Please fill in all fields.")

def donate_blood_page():
    """Display blood donation page"""
    st.header("🩸 Donate Blood")
    
    with st.form("donate_blood_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            donor_name = st.text_input("Donor Name", value=st.session_state.username)
            blood_group = st.selectbox("Blood Group", ["A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"])
            quantity = st.number_input("Quantity (ml)", min_value=100, max_value=500, value=350, step=50)
        
        with col2:
            donation_date = st.date_input("Donation Date", value=datetime.now().date())
            blood_bank = st.text_input("Blood Bank")
            notes = st.text_area("Additional Notes")
        
        submitted = st.form_submit_button("Record Donation")
        
        if submitted:
            if donor_name and blood_group and quantity and blood_bank:
                if donate_blood(donor_name, blood_group, quantity, donation_date, blood_bank, notes):
                    st.success("Blood donation recorded successfully!")
                    st.balloons()
                else:
                    st.error("Failed to record donation.")
            else:
                st.error("Please fill in all required fields.")

def request_blood_page():
    """Display blood request page"""
    st.header("🩸 Request Blood")
    
    with st.form("request_blood_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            requester_name = st.text_input("Requester Name", value=st.session_state.username)
            blood_group = st.selectbox("Blood Group Needed", ["A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"])
            quantity = st.number_input("Quantity Needed (ml)", min_value=100, max_value=2000, value=350, step=50)
            urgency = st.selectbox("Urgency Level", ["Low", "Medium", "High", "Critical"])
        
        with col2:
            required_date = st.date_input("Required By", value=datetime.now().date())
            reason = st.text_area("Reason for Request")
            contact_info = st.text_input("Contact Information")
        
        submitted = st.form_submit_button("Submit Request")
        
        if submitted:
            if requester_name and blood_group and quantity and reason and contact_info:
                result = request_blood(requester_name, blood_group, quantity, urgency, required_date, reason, contact_info)
                if result['success']:
                    st.success("Blood request submitted successfully!")
                    st.info(f"Request ID: {result['request_id']}")
                    st.balloons()
                else:
                    st.error(result['error'])
            else:
                st.error("Please fill in all required fields.")

def show_blood_requests_for_donor():
    """Display blood requests for donor"""
    st.header("🩸 Available Blood Requests")
    
    requests = get_pending_requests_for_donor(st.session_state.username)
    
    if requests:
        for request in requests:
            with st.expander(f"Request #{request['id']} - {request['blood_group']} - {request['urgency']} Priority"):
                col1, col2 = st.columns(2)
                
                with col1:
                    st.write(f"**Requester:** {request['requester']}")
                    st.write(f"**Blood Group:** {request['blood_group']}")
                    st.write(f"**Quantity:** {request['quantity']} ml")
                    st.write(f"**Urgency:** {request['urgency']}")
                
                with col2:
                    st.write(f"**Required By:** {request['required_date']}")
                    st.write(f"**Reason:** {request['reason']}")
                    st.write(f"**Contact:** {request['contact_info']}")
                
                # Response form
                with st.form(f"response_form_{request['id']}"):
                    response_type = st.selectbox("Response", ["accept", "decline"], key=f"response_{request['id']}")
                    if response_type == "accept":
                        quantity_offered = st.number_input("Quantity You Can Offer (ml)", min_value=100, max_value=request['quantity'], value=request['quantity'], key=f"quantity_{request['id']}")
                    else:
                        quantity_offered = 0
                    
                    message = st.text_area("Message to Requester", key=f"message_{request['id']}")
                    
                    if st.form_submit_button(f"Submit Response", key=f"submit_{request['id']}"):
                        if respond_to_request(request['id'], st.session_state.username, response_type, message, quantity_offered):
                            st.success("Response submitted successfully!")
                            st.rerun()
                        else:
                            st.error("Failed to submit response.")
    else:
        st.info("No blood requests available for your blood group at the moment.")

def show_request_responses():
    """Display request responses for receiver"""
    st.header("📬 Request Responses")
    
    responses = get_requester_notifications(st.session_state.username)
    
    if responses:
        for response in responses:
            with st.expander(f"Response to Request #{response['request_id']} - {response['response_type'].title()}"):
                col1, col2 = st.columns(2)
                
                with col1:
                    st.write(f"**Donor:** {response['donor_username']}")
                    st.write(f"**Response:** {response['response_type'].title()}")
                    st.write(f"**Date:** {response['response_date']}")
                    
                with col2:
                    if response['response_type'] == 'accept':
                        st.write(f"**Quantity Offered:** {response['quantity_offered']} ml")
                    st.write(f"**Message:** {response['message']}")
                    
                st.markdown("**Original Request:**")
                st.write(f"Blood Group: {response['request_details']['blood_group']}, Quantity: {response['request_details']['quantity']} ml")
    else:
        st.info("No responses received yet.")

def show_my_donations():
    """Display user's donations"""
    st.header("📋 My Donations")
    
    donations = load_donations()
    user_donations = [d for d in donations if d['donor'] == st.session_state.username]
    
    if user_donations:
        df = pd.DataFrame(user_donations)
        st.dataframe(df[['date', 'blood_group', 'quantity', 'blood_bank', 'notes']], use_container_width=True)
        
        # Summary
        total_donated = sum(d['quantity'] for d in user_donations)
        st.metric("Total Donated", f"{total_donated} ml")
    else:
        st.info("No donations recorded yet.")

def show_my_requests():
    """Display user's requests"""
    st.header("📋 My Requests")
    
    requests = load_requests()
    user_requests = [r for r in requests if r['requester'] == st.session_state.username]
    
    if user_requests:
        df = pd.DataFrame(user_requests)
        st.dataframe(df[['date', 'blood_group', 'quantity', 'urgency', 'status', 'reason']], use_container_width=True)
    else:
        st.info("No requests submitted yet.")

def show_my_notifications():
    """Display user notifications"""
    st.header("📧 My Notifications")
    
    # Get user info to get email
    from auth import get_user_info
    user_info = get_user_info(st.session_state.username)
    
    if user_info:
        notifications = get_user_notifications(user_info['email'])
        
        if notifications:
            for notification in notifications:
                with st.expander(f"{notification['type'].upper()} - {notification['timestamp'][:10]}"):
                    if notification['type'] == 'email':
                        st.write(f"**Subject:** {notification['subject']}")
                    st.write(f"**Message:** {notification['message']}")
                    st.write(f"**Status:** {notification['status']}")
        else:
            st.info("No notifications yet.")
    else:
        st.error("Unable to load user information.")

if __name__ == "__main__":
    main()
