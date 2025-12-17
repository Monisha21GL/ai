# AI Healthcare Assistant - API Documentation

## Overview

The AI Healthcare Assistant provides a RESTful API built with Flask that handles healthcare-related operations including disease prediction, emergency detection, appointment booking, and medical history management.

**Base URL**: `http://127.0.0.1:5000`

## Authentication

The API uses session-based authentication. Sessions are automatically created and managed through Flask's session system. Each user receives a unique session ID that persists across requests.

## Response Format

All API responses follow a consistent JSON format:

```json
{
    "success": true|false,
    "data": {...},
    "message": "Human readable message",
    "error": "Error details (if applicable)",
    "timestamp": "ISO 8601 timestamp"
}
```

## Core Endpoints

### Dashboard & Navigation

#### GET /
**Description**: Main dashboard with navigation panel and system status

**Response**:
```html
<!-- Rendered HTML dashboard template -->
```

**Features**:
- Navigation menu for all healthcare features
- Recent user activity summary
- System status indicators
- User session initialization

---

### Symptom Analysis & Prediction

#### GET /symptom-checker
**Description**: Symptom input form interface

**Response**:
```html
<!-- Rendered symptom checker form -->
```

#### POST /predict-disease
**Description**: AI-powered disease prediction from symptoms

**Request Body** (Form Data):
```
symptoms[]: ["headache", "fever", "nausea"]
symptom_text: "additional symptoms as text"
```

**Response**:
```json
{
    "success": true,
    "disease": "Common Cold",
    "confidence": 0.85,
    "severity": "Low",
    "emergency": false,
    "symptoms_analyzed": ["headache", "fever", "nausea"],
    "primary_prediction": {
        "disease": "Common Cold",
        "confidence": 0.85,
        "severity": "Low"
    },
    "alternative_predictions": [
        {
            "disease": "Flu",
            "confidence": 0.72,
            "severity": "Medium"
        }
    ],
    "timestamp": "2024-12-17T10:30:00Z"
}
```

**Error Responses**:
- `400`: No symptoms provided
- `500`: Prediction engine failure

---

### Emergency Detection

#### POST /check-emergency
**Description**: Emergency condition detection and alert generation

**Request Body** (JSON):
```json
{
    "symptoms": ["chest_pain", "shortness_of_breath", "nausea"],
    "prediction_result": {
        "disease": "Heart Attack",
        "confidence": 0.92,
        "severity": "High"
    }
}
```

**Response**:
```json
{
    "success": true,
    "emergency": true,
    "severity": "Critical",
    "confidence": 0.95,
    "alerts": [
        "EMERGENCY: Potential heart attack detected",
        "Seek immediate medical attention"
    ],
    "recommendations": [
        "Call emergency services immediately",
        "Do not drive yourself to hospital",
        "Take aspirin if not allergic"
    ],
    "emergency_contacts": {
        "ambulance": "911",
        "poison_control": "1-800-222-1222",
        "local_emergency": "+1234567890"
    },
    "ambulance_info": {
        "estimated_arrival": "8-12 minutes",
        "nearest_station": "Station 5",
        "contact": "+1234567800"
    },
    "timestamp": "2024-12-17T10:30:00Z"
}
```

---

### Location Services

#### GET /get-location
**Description**: GPS location tracking interface

**Response**:
```html
<!-- Rendered location tracking page -->
```

#### POST /get-location
**Description**: Process GPS coordinates and find nearby facilities

**Request Body** (JSON):
```json
{
    "latitude": 40.7128,
    "longitude": -74.0060
}
```

**Response**:
```json
{
    "success": true,
    "coordinates": {
        "latitude": 40.7128,
        "longitude": -74.0060,
        "accuracy": 10
    },
    "nearby_hospitals": [
        {
            "name": "City General Hospital",
            "distance": 1.2,
            "contact": "+1234567800",
            "emergency_services": true,
            "estimated_travel_time": "5 minutes"
        }
    ],
    "ambulance_info": {
        "nearest_station": "Station 3",
        "estimated_arrival": "6-10 minutes",
        "contact": "+1234567801"
    },
    "emergency_contacts": {
        "local_emergency": "911",
        "hospital_direct": "+1234567800"
    },
    "location_quality": "high",
    "display_data": {
        "formatted_address": "New York, NY",
        "coordinates_display": "40.7128°N, 74.0060°W"
    }
}
```

---

### Doctor Services

#### GET /doctors
**Description**: Browse all available doctors

**Response**:
```html
<!-- Rendered doctors listing page -->
```

#### GET /doctors/<disease>
**Description**: Get doctor recommendations for specific disease

**Parameters**:
- `disease` (path): Disease name for doctor matching
- `limit` (query): Maximum number of recommendations (default: 5)
- `availability` (query): Filter by availability status

**Example**: `/doctors/Heart%20Attack?limit=3&availability=Available`

**Response**:
```json
{
    "success": true,
    "disease": "Heart Attack",
    "recommendations": [
        {
            "name": "Dr. Sarah Johnson",
            "specialization": "Cardiology",
            "availability": "Available",
            "contact": "+1234567891",
            "rating": 4.8,
            "experience_years": 15,
            "hospital_affiliation": "City General Hospital",
            "next_available": "2024-12-18T09:00:00Z"
        }
    ],
    "summary": {
        "total_matches": 3,
        "available_now": 2,
        "specializations_matched": ["Cardiology", "Emergency Medicine"]
    },
    "count": 3,
    "filters_applied": {
        "max_recommendations": 3,
        "availability_filter": "Available"
    }
}
```

---

### Appointment Management

#### GET /book-appointment
**Description**: Appointment booking form interface

**Response**:
```html
<!-- Rendered appointment booking form -->
```

#### POST /book-appointment
**Description**: Book new appointment with doctor

**Request Body** (Form Data):
```
patient_name: "John Doe"
doctor_name: "Dr. Sarah Johnson"
appointment_date: "2024-12-20"
appointment_time: "10:00"
appointment_type: "consultation"
symptoms: "chest pain, shortness of breath"
notes: "Follow-up for emergency visit"
```

**Response**:
```json
{
    "success": true,
    "message": "Appointment booked successfully",
    "appointment": {
        "id": 123,
        "confirmation_code": "CONF789X",
        "patient_name": "John Doe",
        "doctor_name": "Dr. Sarah Johnson",
        "doctor_specialization": "Cardiology",
        "appointment_date": "2024-12-20",
        "appointment_time": "10:00",
        "appointment_type": "consultation",
        "duration_minutes": 30,
        "status": "scheduled",
        "symptoms": "chest pain, shortness of breath",
        "notes": "Follow-up for emergency visit"
    },
    "next_steps": [
        "Save your confirmation code: CONF789X",
        "Arrive 15 minutes early",
        "Bring insurance information"
    ]
}
```

#### GET /get-available-slots
**Description**: Get available appointment slots for doctor

**Parameters**:
- `doctor_name` (query): Doctor's name
- `date` (query): Date in YYYY-MM-DD format

**Example**: `/get-available-slots?doctor_name=Dr.%20Sarah%20Johnson&date=2024-12-20`

**Response**:
```json
{
    "success": true,
    "doctor_name": "Dr. Sarah Johnson",
    "date": "2024-12-20",
    "slots": [
        {
            "time": "09:00",
            "available": true,
            "duration": 30
        },
        {
            "time": "10:00",
            "available": false,
            "reason": "Already booked"
        },
        {
            "time": "11:00",
            "available": true,
            "duration": 30
        }
    ]
}
```

#### POST /cancel-appointment
**Description**: Cancel existing appointment

**Request Body** (Form Data):
```
appointment_id: "123"
reason: "Patient requested cancellation"
```

**Response**:
```json
{
    "success": true,
    "message": "Appointment cancelled successfully",
    "appointment_id": 123,
    "cancellation_reason": "Patient requested cancellation",
    "refund_eligible": true
}
```

#### GET /my-appointments
**Description**: Get user's appointment list

**Parameters**:
- `patient_name` (query): Patient name for filtering

**Response**:
```json
{
    "success": true,
    "appointments": [
        {
            "id": 123,
            "confirmation_code": "CONF789X",
            "doctor_name": "Dr. Sarah Johnson",
            "appointment_date": "2024-12-20",
            "appointment_time": "10:00",
            "status": "scheduled"
        }
    ],
    "count": 1
}
```

#### GET /appointment-summary
**Description**: Get appointment system summary and statistics

**Response**:
```json
{
    "success": true,
    "summary": {
        "total_appointments": 15,
        "scheduled": 8,
        "completed": 5,
        "cancelled": 2,
        "today_appointments": 3,
        "upcoming_appointments": 5
    },
    "recent_activity": [
        {
            "action": "appointment_booked",
            "doctor": "Dr. Sarah Johnson",
            "date": "2024-12-20",
            "timestamp": "2024-12-17T10:30:00Z"
        }
    ],
    "timestamp": "2024-12-17T10:30:00Z"
}
```

---

### Medical History & Analytics

#### GET /medical-history
**Description**: Comprehensive medical history interface

**Response**:
```html
<!-- Rendered medical history page with analytics -->
```

#### GET /analytics/user-history
**Description**: Get comprehensive user medical history and analytics

**Parameters**:
- `limit` (query): Maximum number of records
- `include_summary` (query): Include summary statistics (default: true)

**Response**:
```json
{
    "success": true,
    "history": {
        "predictions": [
            {
                "id": 1,
                "symptoms": "headache,fever,fatigue",
                "predicted_disease": "Common Cold",
                "confidence": 0.85,
                "severity": "Low",
                "emergency": false,
                "timestamp": "2024-12-17T10:30:00Z"
            }
        ],
        "appointments": [
            {
                "id": 123,
                "doctor_name": "Dr. Sarah Johnson",
                "appointment_date": "2024-12-20",
                "status": "scheduled"
            }
        ],
        "emergency_logs": [],
        "location_logs": [
            {
                "latitude": 40.7128,
                "longitude": -74.0060,
                "timestamp": "2024-12-17T10:25:00Z"
            }
        ],
        "summary": {
            "total_predictions": 1,
            "total_appointments": 1,
            "emergency_count": 0,
            "most_common_symptoms": ["headache", "fever"],
            "health_score": 85,
            "risk_level": "Low"
        }
    },
    "timestamp": "2024-12-17T10:30:00Z"
}
```

#### POST /analytics/export
**Description**: Export user medical data in various formats

**Request Body** (JSON):
```json
{
    "format": "json",
    "categories": ["predictions", "appointments", "emergency_logs"]
}
```

**Response** (JSON format):
```json
{
    "success": true,
    "data": {
        "predictions": [...],
        "appointments": [...],
        "emergency_logs": [...]
    },
    "format": "json",
    "timestamp": "2024-12-17T10:30:00Z"
}
```

**Response** (CSV/TXT format):
```
Content-Type: application/octet-stream
Content-Disposition: attachment; filename=medical_history_12345678_20241217_103000.csv

<!-- File download with exported data -->
```

#### GET /analytics/system
**Description**: Get system-wide analytics and statistics

**Response**:
```json
{
    "success": true,
    "system_stats": {
        "total_users": 25,
        "total_predictions": 150,
        "total_appointments": 45,
        "emergency_events": 3,
        "active_sessions": 5
    },
    "performance_metrics": {
        "average_prediction_time": "0.25s",
        "database_response_time": "0.05s",
        "uptime": "99.8%"
    },
    "usage_patterns": {
        "most_common_symptoms": ["headache", "fever", "fatigue"],
        "most_predicted_diseases": ["Common Cold", "Flu", "Allergies"],
        "peak_usage_hours": ["10:00-12:00", "14:00-16:00"]
    },
    "timestamp": "2024-12-17T10:30:00Z"
}
```

#### GET /analytics/summary
**Description**: Get summary statistics for dashboard

**Response**:
```json
{
    "success": true,
    "summary": {
        "total_predictions": 5,
        "total_appointments": 2,
        "emergency_count": 0,
        "health_score": 85,
        "risk_level": "Low",
        "recommendations": [
            "Continue maintaining good health practices",
            "Consider scheduling regular check-ups"
        ],
        "recent_activity": {
            "last_prediction": "2024-12-17T10:30:00Z",
            "last_appointment": "2024-12-20T10:00:00Z"
        }
    },
    "timestamp": "2024-12-17T10:30:00Z"
}
```

---

### Health Services

#### GET /health-tips
**Description**: Get personalized health recommendations

**Response**:
```json
{
    "success": true,
    "tips": [
        {
            "category": "General Health",
            "title": "Stay Hydrated",
            "description": "Drink at least 8 glasses of water daily",
            "priority": "medium",
            "personalized": false
        },
        {
            "category": "Based on History",
            "title": "Monitor Blood Pressure",
            "description": "Based on your recent symptoms, consider regular BP monitoring",
            "priority": "high",
            "personalized": true
        }
    ],
    "count": 2,
    "timestamp": "2024-12-17T10:30:00Z"
}
```

#### POST /health-tips
**Description**: Get health tips based on provided user data

**Request Body** (JSON):
```json
{
    "predictions": [...],
    "appointments": [...],
    "emergency_logs": [...]
}
```

#### GET /daily-tip
**Description**: Get daily health tip

**Response**:
```json
{
    "success": true,
    "tip": {
        "category": "Nutrition",
        "title": "Eat Colorful Vegetables",
        "description": "Include vegetables of different colors in your meals for varied nutrients",
        "source": "General Health Guidelines"
    },
    "timestamp": "2024-12-17T10:30:00Z"
}
```

#### GET /search-tips
**Description**: Search health tips by keyword or category

**Parameters**:
- `q` (query): Search keyword
- `category` (query): Tip category

**Example**: `/search-tips?q=exercise&category=fitness`

**Response**:
```json
{
    "success": true,
    "tips": [
        {
            "category": "Fitness",
            "title": "Regular Exercise Benefits",
            "description": "30 minutes of moderate exercise daily improves cardiovascular health",
            "keywords": ["exercise", "fitness", "cardiovascular"]
        }
    ],
    "count": 1,
    "query": "exercise",
    "category": "fitness",
    "timestamp": "2024-12-17T10:30:00Z"
}
```

---

### Chatbot Services

#### POST /chatbot
**Description**: Interact with health chatbot

**Request Body** (JSON):
```json
{
    "message": "I have a headache, what should I do?"
}
```

**Response**:
```json
{
    "success": true,
    "response": "For headaches, try resting in a quiet, dark room and staying hydrated. If severe or persistent, consult a healthcare provider.",
    "category": "symptom_advice",
    "confidence": 0.8,
    "suggestions": [
        "Use the symptom checker for detailed analysis",
        "Book an appointment if symptoms persist",
        "Check emergency detection if severe"
    ],
    "timestamp": "2024-12-17T10:30:00Z"
}
```

#### GET /chatbot-history
**Description**: Get chatbot conversation history

**Response**:
```json
{
    "success": true,
    "history": [
        {
            "user_message": "I have a headache",
            "bot_response": "For headaches, try resting...",
            "timestamp": "2024-12-17T10:30:00Z"
        }
    ],
    "count": 1,
    "timestamp": "2024-12-17T10:30:00Z"
}
```

#### GET /clear-chat
**Description**: Clear chatbot conversation history

**Response**:
```json
{
    "success": true,
    "message": "Conversation history cleared",
    "timestamp": "2024-12-17T10:30:00Z"
}
```

---

## Error Handling

### Standard Error Responses

#### 400 Bad Request
```json
{
    "success": false,
    "error": "Invalid input",
    "message": "Please provide valid symptoms",
    "timestamp": "2024-12-17T10:30:00Z"
}
```

#### 404 Not Found
```json
{
    "success": false,
    "error": "Resource not found",
    "message": "The requested endpoint does not exist",
    "timestamp": "2024-12-17T10:30:00Z"
}
```

#### 500 Internal Server Error
```json
{
    "success": false,
    "error": "Internal server error",
    "message": "An unexpected error occurred. Please try again.",
    "timestamp": "2024-12-17T10:30:00Z"
}
```

### Error Categories

1. **Validation Errors**: Invalid input data or missing required fields
2. **Model Errors**: ML model loading or prediction failures
3. **Database Errors**: Database connection or query failures
4. **External Service Errors**: GPS or other external service failures
5. **System Errors**: Unexpected application errors

## Rate Limiting

Currently, no rate limiting is implemented as this is a localhost application for academic purposes. In production, consider implementing:

- Request rate limiting per session
- API endpoint throttling
- Resource usage monitoring

## Security Considerations

### Input Validation
- All user inputs are sanitized and validated
- SQL injection prevention through parameterized queries
- XSS protection through template escaping

### Session Security
- Secure session management with unique session IDs
- Session timeout handling
- CSRF protection for form submissions

### Data Privacy
- All data remains on localhost
- No external data transmission
- User data isolation by session

## Testing the API

### Using curl

```bash
# Test disease prediction
curl -X POST http://127.0.0.1:5000/predict-disease \
  -d "symptoms=headache&symptoms=fever&symptom_text=nausea"

# Test emergency detection
curl -X POST http://127.0.0.1:5000/check-emergency \
  -H "Content-Type: application/json" \
  -d '{"symptoms": ["chest_pain", "shortness_of_breath"]}'

# Test location services
curl -X POST http://127.0.0.1:5000/get-location \
  -H "Content-Type: application/json" \
  -d '{"latitude": 40.7128, "longitude": -74.0060}'
```

### Using Python requests

```python
import requests

# Disease prediction
response = requests.post('http://127.0.0.1:5000/predict-disease', 
                        data={'symptoms': ['headache', 'fever']})
print(response.json())

# Emergency detection
response = requests.post('http://127.0.0.1:5000/check-emergency',
                        json={'symptoms': ['chest_pain', 'shortness_of_breath']})
print(response.json())
```

## API Versioning

Currently, the API does not use versioning as it's a single-version academic project. For future development, consider:

- URL versioning: `/api/v1/predict-disease`
- Header versioning: `Accept: application/vnd.api+json;version=1`
- Parameter versioning: `/predict-disease?version=1`

---

**Note**: This API is designed for educational purposes and should not be used for actual medical diagnosis or treatment. Always consult qualified healthcare professionals for medical advice.