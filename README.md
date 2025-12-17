# AI Healthcare Assistant

A comprehensive localhost-based web application that provides AI-powered healthcare assistance through symptom analysis, disease prediction, emergency detection, GPS tracking, doctor recommendations, and appointment booking.

## 🏥 Project Overview

The AI Healthcare Assistant is an academic project designed to demonstrate the integration of artificial intelligence and machine learning in healthcare applications. The system provides a unified dashboard interface for various healthcare services while maintaining complete privacy by running entirely on localhost.

### Key Features

- **🩺 Symptom Checker**: Interactive form for entering symptoms with checkboxes and text input
- **🔬 Disease Prediction**: AI-powered disease prediction using scikit-learn machine learning models
- **🚨 Emergency Detection**: Rule-based emergency detection with immediate alert notifications
- **📍 GPS Location Tracking**: HTML5 Geolocation API integration for finding nearby medical facilities
- **👨‍⚕️ Doctor Recommendations**: Intelligent doctor matching based on predicted diseases and specializations
- **📅 Appointment Booking**: Complete appointment scheduling system with conflict prevention
- **📊 Medical History**: Comprehensive tracking and analytics of user health data
- **💡 Health Tips**: Personalized health recommendations based on user history
- **🤖 Health Chatbot**: Rule-based chatbot for basic health guidance
- **🌙 Dark/Light Mode**: Theme toggle for improved user experience

### Technology Stack

- **Backend**: Python 3.x with Flask framework
- **Machine Learning**: scikit-learn for disease prediction models
- **Frontend**: HTML5, CSS3, JavaScript (vanilla)
- **Database**: SQLite for structured data, CSV for static datasets
- **Geolocation**: HTML5 Geolocation API
- **Model Persistence**: Python pickle for trained ML models
- **Testing**: pytest for unit tests, Hypothesis for property-based testing

## 🚀 Quick Start

### Prerequisites

- Python 3.7 or higher
- pip (Python package installer)
- Modern web browser with JavaScript enabled
- Internet connection (for initial setup only)

### Installation

1. **Clone or download the project**
   ```bash
   git clone <repository-url>
   cd ai-healthcare-assistant
   ```

2. **Install Python dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Initialize the database**
   ```bash
   python -c "from modules.database_manager import get_db_manager; get_db_manager().initialize_database()"
   ```

4. **Train the ML model (if not already present)**
   ```bash
   python train_model.py
   ```

5. **Verify installation (optional)**
   ```bash
   python verify_setup.py
   ```

6. **Start the application**
   ```bash
   python app.py
   ```

7. **Access the application**
   Open your web browser and navigate to: `http://127.0.0.1:5000/`

## 📖 User Guide

### Getting Started

1. **Dashboard Navigation**: The main dashboard provides access to all features through a clean, healthcare-themed interface
2. **Symptom Entry**: Use the Symptom Checker to enter your symptoms via checkboxes or text input
3. **Disease Prediction**: Submit symptoms to receive AI-powered disease predictions with confidence scores
4. **Emergency Detection**: The system automatically detects emergency conditions and provides immediate alerts
5. **Location Services**: Enable GPS to find nearby hospitals and emergency services
6. **Doctor Recommendations**: Get matched with appropriate specialists based on your predicted condition
7. **Appointment Booking**: Schedule appointments with recommended doctors
8. **Medical History**: Track your health journey with comprehensive history and analytics

### Feature Details

#### Symptom Checker & Disease Prediction
- Enter symptoms using checkboxes for common symptoms or text input for specific descriptions
- Receive predictions with disease name, confidence score, and severity level (Low/Medium/High)
- All predictions are stored for future reference and trend analysis

#### Emergency Detection
- Automatic emergency detection based on symptom combinations
- Prominent alert displays for emergency conditions
- Ambulance contact information and emergency service simulation
- Emergency events are logged for medical history

#### GPS & Location Services
- HTML5 Geolocation API integration for precise location tracking
- Nearby hospital and emergency service simulation
- Location data storage for emergency reference
- Works entirely offline after initial location acquisition

#### Doctor Recommendations
- Intelligent matching based on predicted diseases and doctor specializations
- Doctor ranking by relevance and availability
- Complete doctor information including contact details and ratings
- Integration with appointment booking system

#### Appointment Management
- Full-featured appointment scheduling with date/time selection
- Conflict detection and prevention
- Appointment confirmation with unique confirmation codes
- Status tracking (scheduled, confirmed, cancelled, completed)
- Patient appointment history and management

#### Medical History & Analytics
- Comprehensive tracking of all user interactions
- Prediction history with trend analysis
- Appointment records and status tracking
- Emergency event logs
- Data export functionality (JSON, CSV, TXT formats)
- Health score calculation and risk assessment

## 🔧 Technical Documentation

### Project Structure

```
ai-healthcare-assistant/
├── app.py                          # Main Flask application
├── requirements.txt                # Python dependencies
├── train_model.py                  # ML model training script
├── verify_setup.py                 # Installation verification script
├── README.md                       # This documentation
├── data/                           # Data files and database
│   ├── healthcare.db              # SQLite database
│   ├── init_database.sql          # Database schema
│   ├── doctors.csv                # Doctor information
│   ├── hospitals.csv              # Hospital data
│   └── symptoms_diseases.csv      # Training data
├── models/                         # ML models
│   └── disease_model.pkl          # Trained prediction model
├── modules/                        # Backend modules
│   ├── database_manager.py        # Database operations
│   ├── prediction_engine.py       # ML prediction logic
│   ├── emergency_detector.py      # Emergency detection
│   ├── gps_service.py             # Location services
│   ├── doctor_recommender.py      # Doctor matching
│   ├── appointment_manager.py     # Appointment system
│   ├── health_tips_engine.py      # Health recommendations
│   ├── analytics_engine.py        # Data analytics
│   ├── health_chatbot.py          # Advanced chatbot functionality
│   ├── simple_chatbot.py          # Basic chatbot implementation
│   └── __init__.py                # Module initialization
├── templates/                      # HTML templates
│   ├── base.html                  # Base template
│   ├── dashboard.html             # Main dashboard
│   ├── symptom_checker.html       # Symptom input form
│   ├── doctors.html               # Doctor listings
│   ├── appointment.html           # Appointment booking
│   ├── location.html              # GPS interface
│   ├── history.html               # Medical history
│   └── error.html                 # Error pages
└── static/                         # Static assets
    ├── css/                       # Stylesheets
    │   ├── main.css              # Main styles
    │   └── responsive.css        # Responsive design
    └── js/                        # JavaScript files
        ├── main.js               # Main functionality
        ├── emergency.js          # Emergency handling
        └── location.js           # GPS functionality
```

### API Endpoints

#### Core Application Routes

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Main dashboard with navigation |
| GET | `/symptom-checker` | Symptom input form |
| POST | `/predict-disease` | Disease prediction API |
| POST | `/check-emergency` | Emergency detection API |
| GET/POST | `/get-location` | GPS location services |
| GET | `/doctors` | Doctor listings page |
| GET | `/doctors/<disease>` | Disease-specific doctor recommendations |
| GET/POST | `/book-appointment` | Appointment booking interface |
| GET | `/medical-history` | User medical history page |

#### Appointment Management

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/get-available-slots` | Get available appointment slots |
| POST | `/cancel-appointment` | Cancel existing appointment |
| GET | `/my-appointments` | User's appointment list |
| GET | `/appointment-summary` | Appointment system summary |

#### Health Services

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET/POST | `/health-tips` | Personalized health recommendations |
| GET | `/daily-tip` | Daily health tip |
| GET | `/search-tips` | Search health tips by keyword |
| POST | `/chatbot` | Health chatbot interaction |
| GET | `/chatbot-history` | Chatbot conversation history |
| GET | `/clear-chat` | Clear chatbot history |

#### Analytics & Data

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/analytics/user-history` | Comprehensive user analytics |
| POST | `/analytics/export` | Export user data (JSON/CSV/TXT) |
| GET | `/analytics/system` | System-wide analytics |
| GET | `/analytics/summary` | Summary statistics |

### Database Schema

#### Users Table
```sql
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    session_id TEXT UNIQUE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_active TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

#### Predictions Table
```sql
CREATE TABLE predictions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_session TEXT NOT NULL,
    symptoms TEXT NOT NULL,
    predicted_disease TEXT NOT NULL,
    confidence REAL NOT NULL,
    severity TEXT NOT NULL CHECK (severity IN ('Low', 'Medium', 'High')),
    emergency BOOLEAN NOT NULL DEFAULT 0,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

#### Appointments Table
```sql
CREATE TABLE appointments (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_session TEXT NOT NULL,
    patient_name TEXT NOT NULL,
    doctor_name TEXT NOT NULL,
    doctor_specialization TEXT,
    appointment_date DATE NOT NULL,
    appointment_time TIME NOT NULL,
    appointment_type TEXT DEFAULT 'consultation',
    status TEXT DEFAULT 'scheduled',
    confirmation_code TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

#### Emergency Logs Table
```sql
CREATE TABLE emergency_logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_session TEXT NOT NULL,
    symptoms TEXT NOT NULL,
    emergency_type TEXT NOT NULL,
    severity_level TEXT NOT NULL,
    location_lat REAL,
    location_lng REAL,
    ambulance_called BOOLEAN DEFAULT 0,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### Machine Learning Model

The disease prediction system uses a scikit-learn classification model trained on symptom-disease pairs:

- **Algorithm**: Random Forest Classifier or Support Vector Machine
- **Input Features**: Binary encoding of symptoms (one-hot encoding)
- **Target Variable**: Disease categories (multi-class classification)
- **Training Data**: Symptom-disease pairs from medical datasets
- **Validation**: Cross-validation with 80/20 train-test split
- **Serialization**: Pickle format for model persistence

## 🧪 Testing

The project includes comprehensive testing with both unit tests and property-based tests:

### Running Tests

```bash
# Run all tests
pytest

# Run specific test files
pytest test_integration.py
pytest test_analytics.py

# Run with coverage
pytest --cov=modules

# Run property-based tests
pytest -k "property" -v
```

### Test Categories

- **Unit Tests**: Test individual functions and components
- **Integration Tests**: Test component interactions and workflows
- **Property-Based Tests**: Test universal properties across all inputs
- **API Tests**: Test all Flask endpoints and responses

## 🔒 Security & Privacy

- **Local Operation**: All data remains on localhost - no external data transmission
- **Session Management**: Secure session handling with unique user IDs
- **Input Validation**: Comprehensive input sanitization and validation
- **Error Handling**: Graceful error handling without exposing sensitive information
- **Data Integrity**: Transaction-based database operations with rollback support

## 🚨 Troubleshooting

### Common Issues

1. **Setup Verification**
   ```bash
   # Run setup verification to identify issues
   python verify_setup.py
   ```

2. **Port Already in Use**
   ```bash
   # Kill process using port 5000
   lsof -ti:5000 | xargs kill -9
   ```

2. **Database Connection Errors**
   ```bash
   # Reinitialize database
   rm data/healthcare.db
   python -c "from modules.database_manager import get_db_manager; get_db_manager().initialize_database()"
   ```

3. **Missing ML Model**
   ```bash
   # Retrain the model
   python train_model.py
   ```

4. **Import Errors**
   ```bash
   # Reinstall dependencies
   pip install -r requirements.txt --force-reinstall
   ```

### Performance Optimization

- **Database Indexing**: Indexes are created for frequently queried columns
- **Model Caching**: ML models are loaded once and cached in memory
- **Session Management**: Efficient session handling with minimal database queries
- **Static File Serving**: Optimized static file serving for CSS/JS resources

## 📝 Development Notes

### Adding New Features

1. **Backend Logic**: Add new modules in the `modules/` directory
2. **Database Changes**: Update `data/init_database.sql` for schema changes
3. **API Endpoints**: Add new routes in `app.py`
4. **Frontend**: Create templates in `templates/` and styles in `static/`
5. **Testing**: Add corresponding tests for new functionality

### Code Style

- Follow PEP 8 for Python code
- Use descriptive variable and function names
- Include comprehensive docstrings for all functions
- Add error handling for all external dependencies
- Maintain separation of concerns between modules

## 📄 License

This project is developed for academic purposes. Please ensure compliance with relevant healthcare data regulations and privacy laws when adapting for production use.

## 🤝 Contributing

This is an academic project. For educational purposes, you may:
- Study the code structure and implementation
- Extend functionality for learning purposes
- Use as a reference for similar projects
- Adapt components for other healthcare applications

## 📞 Support

For technical issues or questions about the implementation:
1. Check the troubleshooting section above
2. Review the code documentation and comments
3. Examine the test files for usage examples
4. Consult the Flask and scikit-learn documentation for framework-specific issues

---

**Disclaimer**: This application is for educational and demonstration purposes only. It should not be used for actual medical diagnosis or treatment. Always consult qualified healthcare professionals for medical advice.