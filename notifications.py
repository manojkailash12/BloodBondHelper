import json
import os
from datetime import datetime, timedelta
import random
import string

def generate_otp(length=6):
    """Generate a random OTP"""
    return ''.join(random.choices(string.digits, k=length))

def generate_reset_token(length=32):
    """Generate a random reset token"""
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

def load_otps():
    """Load OTPs from JSON file"""
    try:
        with open("data/otps.json", 'r') as f:
            return json.load(f)
    except:
        return {}

def save_otps(otps):
    """Save OTPs to JSON file"""
    try:
        os.makedirs("data", exist_ok=True)
        with open("data/otps.json", 'w') as f:
            json.dump(otps, f, indent=2)
        return True
    except:
        return False

def load_notifications():
    """Load notifications from JSON file"""
    try:
        with open("data/notifications.json", 'r') as f:
            return json.load(f)
    except:
        return []

def save_notifications(notifications):
    """Save notifications to JSON file"""
    try:
        os.makedirs("data", exist_ok=True)
        with open("data/notifications.json", 'w') as f:
            json.dump(notifications, f, indent=2)
        return True
    except:
        return False

def store_otp(identifier, otp, purpose, expires_in_minutes=10):
    """Store OTP with expiration"""
    otps = load_otps()
    
    expiry_time = datetime.now() + timedelta(minutes=expires_in_minutes)
    
    otps[identifier] = {
        'otp': otp,
        'purpose': purpose,
        'expires_at': expiry_time.isoformat(),
        'created_at': datetime.now().isoformat()
    }
    
    return save_otps(otps)

def verify_otp(identifier, otp):
    """Verify OTP"""
    otps = load_otps()
    
    if identifier not in otps:
        return False
    
    stored_otp = otps[identifier]
    
    # Check if OTP has expired
    expiry_time = datetime.fromisoformat(stored_otp['expires_at'])
    if datetime.now() > expiry_time:
        # Remove expired OTP
        del otps[identifier]
        save_otps(otps)
        return False
    
    # Check if OTP matches
    if stored_otp['otp'] == otp:
        # Remove used OTP
        del otps[identifier]
        save_otps(otps)
        return True
    
    return False

def is_otp_verified(identifier):
    """Check if OTP was verified"""
    otps = load_otps()
    return identifier not in otps

def store_reset_token(email, token, expires_in_minutes=15):
    """Store password reset token"""
    otps = load_otps()
    
    expiry_time = datetime.now() + timedelta(minutes=expires_in_minutes)
    
    otps[f"reset_{email}"] = {
        'token': token,
        'purpose': 'password_reset',
        'expires_at': expiry_time.isoformat(),
        'created_at': datetime.now().isoformat()
    }
    
    return save_otps(otps)

def verify_reset_token(email, token):
    """Verify password reset token"""
    otps = load_otps()
    identifier = f"reset_{email}"
    
    if identifier not in otps:
        return False
    
    stored_token = otps[identifier]
    
    # Check if token has expired
    expiry_time = datetime.fromisoformat(stored_token['expires_at'])
    if datetime.now() > expiry_time:
        # Remove expired token
        del otps[identifier]
        save_otps(otps)
        return False
    
    # Check if token matches
    if stored_token['token'] == token:
        # Remove used token
        del otps[identifier]
        save_otps(otps)
        return True
    
    return False

def send_email_notification(email, subject, message):
    """Store email notification (simulated)"""
    notifications = load_notifications()
    
    notification = {
        'type': 'email',
        'recipient': email,
        'subject': subject,
        'message': message,
        'timestamp': datetime.now().isoformat(),
        'status': 'sent'
    }
    
    notifications.append(notification)
    save_notifications(notifications)
    return True

def send_sms_notification(phone, message):
    """Store SMS notification (simulated)"""
    notifications = load_notifications()
    
    notification = {
        'type': 'sms',
        'recipient': phone,
        'message': message,
        'timestamp': datetime.now().isoformat(),
        'status': 'sent'
    }
    
    notifications.append(notification)
    save_notifications(notifications)
    return True

def send_registration_email(email, username):
    """Send registration confirmation email"""
    subject = "Welcome to Blood Bank Management System"
    message = f"""
Dear {username},

Welcome to the Blood Bank Management System!

Your account has been successfully created. You can now:
- Donate blood and track your donations
- Request blood when needed
- Find nearby blood banks
- View real-time blood inventory

Thank you for joining our life-saving community!

Best regards,
Blood Bank Management Team
"""
    
    return send_email_notification(email, subject, message)

def send_password_reset_email(email, username, token):
    """Send password reset email"""
    subject = "Password Reset Link - Blood Bank Management System"
    message = f"""
Dear {username},

You have requested to reset your password for the Blood Bank Management System.

Reset Token: {token}

This token will expire in 15 minutes. If you did not request this reset, please ignore this email.

Best regards,
Blood Bank Management Team
"""
    
    return send_email_notification(email, subject, message)

def get_user_notifications(user_email):
    """Get notifications for a specific user"""
    notifications = load_notifications()
    user_notifications = []
    
    for notification in notifications:
        if notification['recipient'] == user_email:
            user_notifications.append(notification)
    
    # Sort by timestamp (most recent first)
    user_notifications.sort(key=lambda x: x['timestamp'], reverse=True)
    return user_notifications
