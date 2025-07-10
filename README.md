# BloodBondHelper - Blood Bank Management System

A comprehensive blood bank management system built with Streamlit that facilitates blood donation, requests, and inventory management.

## Features

- **User Authentication**: Secure login/register system for donors and receivers
- **Blood Donation Management**: Record and track blood donations
- **Blood Request System**: Submit and manage blood requests with donor matching
- **Interactive Maps**: Find nearby blood banks with interactive mapping
- **Real-time Dashboard**: Analytics and blood inventory tracking
- **Notification System**: Email and SMS notifications for blood requests
- **Donor-Recipient Matching**: Automatic compatible donor notifications

## Quick Start

### Local Development

1. Clone the repository:
```bash
git clone https://github.com/manojkailash12/BloodBondHelper.git
cd BloodBondHelper
```

2. Install dependencies:
```bash
pip install streamlit plotly folium streamlit-folium pandas
```

3. Run the application:
```bash
streamlit run app.py
```

### Streamlit Cloud Deployment

1. Fork this repository
2. Connect your GitHub account to [Streamlit Cloud](https://share.streamlit.io/)
3. Deploy directly from your GitHub repository
4. Set main file path as `app.py`

## Project Structure

```
BloodBondHelper/
├── app.py                 # Main application file
├── auth.py               # Authentication module
├── blood_management.py   # Blood donation and request management
├── dashboard.py          # Analytics dashboard
├── maps.py              # Interactive blood bank maps
├── request_management.py # Request processing and matching
├── notifications.py     # Notification system
├── data/                # JSON data storage
│   ├── users.json
│   ├── blood_inventory.json
│   ├── donations.json
│   ├── requests.json
│   ├── blood_banks.json
│   └── notifications.json
└── .streamlit/
    └── config.toml      # Streamlit configuration
```

## User Types

- **Donors**: Register, donate blood, respond to requests
- **Receivers**: Register, submit blood requests, track responses
- **System**: Automated matching and notifications

## Technology Stack

- **Frontend**: Streamlit
- **Visualization**: Plotly, Folium
- **Data Storage**: JSON files
- **Authentication**: SHA256 password hashing
- **Maps**: OpenStreetMap with Folium

## Configuration

The application uses `.streamlit/config.toml` for deployment settings:

```toml
[server]
headless = true
address = "0.0.0.0"
port = 5000
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## License

This project is open source and available under the [MIT License](LICENSE).

## Support

For issues and questions, please open an issue on GitHub.