import streamlit as st
import json
import os
from datetime import datetime

# Simple test imports to check which one is failing
try:
    st.write("Testing imports...")
    
    try:
        from dashboard import show_dashboard
        st.write("✓ Dashboard import successful")
    except Exception as e:
        st.write(f"✗ Dashboard import failed: {e}")
    
    try:
        from auth import login_user, logout_user, register_user
        st.write("✓ Auth import successful")
    except Exception as e:
        st.write(f"✗ Auth import failed: {e}")
    
    try:
        from blood_management import donate_blood, request_blood
        st.write("✓ Blood management import successful")
    except Exception as e:
        st.write(f"✗ Blood management import failed: {e}")
    
    try:
        from maps import show_blood_bank_map
        st.write("✓ Maps import successful")
    except Exception as e:
        st.write(f"✗ Maps import failed: {e}")
    
    try:
        from request_management import get_pending_requests_for_donor
        st.write("✓ Request management import successful")
    except Exception as e:
        st.write(f"✗ Request management import failed: {e}")
    
    try:
        from notifications import get_user_notifications
        st.write("✓ Notifications import successful")
    except Exception as e:
        st.write(f"✗ Notifications import failed: {e}")
    
    st.write("All imports checked!")
    
except Exception as e:
    st.write(f"Error during import testing: {e}")
    import traceback
    st.write(traceback.format_exc())