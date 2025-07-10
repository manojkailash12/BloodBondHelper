# Blood Bank Management System

## Overview

This is a comprehensive blood bank management system built with Streamlit that facilitates blood donation, requests, and inventory management. The system serves three main user types: donors, receivers, and administrators, providing a complete workflow for blood bank operations including real-time inventory tracking, donor-recipient matching, and location-based services.

## User Preferences

Preferred communication style: Simple, everyday language.

## System Architecture

### Frontend Architecture
- **Framework**: Streamlit web application framework
- **UI Components**: Interactive dashboard with charts, maps, and forms
- **Visualization**: Plotly for charts and graphs, Folium for interactive maps
- **User Interface**: Multi-page application with role-based access control

### Backend Architecture
- **Data Storage**: JSON file-based storage system
- **Authentication**: Custom authentication with password hashing (SHA256)
- **Session Management**: Streamlit session state for user sessions
- **Notification System**: Email and SMS notifications for user interactions

### Data Storage Solution
- **Primary Storage**: Local JSON files in `/data` directory
- **File Structure**:
  - `users.json` - User accounts and profiles
  - `blood_inventory.json` - Current blood stock levels
  - `donations.json` - Donation history records
  - `requests.json` - Blood request records
  - `blood_banks.json` - Blood bank locations
  - `notifications.json` - Notification history
  - `otps.json` - OTP verification data
  - `request_responses.json` - Donor responses to requests

## Key Components

### Authentication System (`auth.py`)
- User registration with email/phone verification
- Password hashing and secure login
- Password reset functionality with tokens
- Role-based access (donor, receiver, admin)

### Blood Management (`blood_management.py`)
- Blood inventory tracking by blood group
- Donation recording and history
- Blood request management
- Compatibility matching between donors and recipients

### Dashboard (`dashboard.py`)
- Real-time analytics and metrics
- Blood inventory visualizations
- User statistics and trends
- Interactive charts using Plotly

### Maps Integration (`maps.py`)
- Interactive map showing blood bank locations
- Folium-based mapping with custom markers
- Contact information and directions

### Request Management (`request_management.py`)
- Blood request processing
- Donor-recipient matching algorithm
- Response tracking and notifications
- Automated notifications to compatible donors

### Notifications (`notifications.py`)
- Email and SMS notification system
- OTP generation and verification
- User registration confirmations
- Blood request alerts

## Data Flow

1. **User Registration**: New users register with personal details and blood group information
2. **Authentication**: Users login with credentials, session maintained via Streamlit state
3. **Blood Donation**: Donors record donations, updating inventory levels
4. **Blood Requests**: Recipients submit requests, system finds compatible donors
5. **Matching**: Automated notification to compatible donors about requests
6. **Response Processing**: Donors respond to requests, system tracks responses
7. **Inventory Management**: Real-time updates to blood stock levels
8. **Analytics**: Dashboard displays current statistics and trends

## External Dependencies

### Required Python Packages
- `streamlit` - Web application framework
- `plotly` - Interactive charts and visualizations
- `folium` - Interactive maps
- `streamlit-folium` - Folium integration for Streamlit
- `pandas` - Data manipulation and analysis
- `hashlib` - Password hashing (built-in)
- `json` - Data serialization (built-in)
- `datetime` - Date/time handling (built-in)

### Third-Party Services
- Email service integration (configured for notifications)
- SMS service integration (configured for phone notifications)
- OpenStreetMap tiles for map visualization

## Deployment Strategy

### Current Setup
- Local development with Streamlit server
- File-based data storage for simplicity
- Single-instance deployment model

### Production Considerations
- JSON files provide reliable data persistence in `/data` folder
- No external database dependencies - fully self-contained
- Notification services need API key configuration
- Map services use free OpenStreetMap tiles

### Scalability Notes
- File-based storage chosen for simplicity and reliability
- Data stored in structured JSON format in `/data` directory
- Modular design allows for easy maintenance and updates
- Stateless design except for session management

### Security Features
- Password hashing with SHA256
- Session-based authentication
- Input validation and sanitization
- OTP verification for sensitive operations