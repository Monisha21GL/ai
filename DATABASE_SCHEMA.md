# AI Healthcare Assistant - Database Schema Documentation

## Overview

The AI Healthcare Assistant uses SQLite as its primary database for storing user interactions, predictions, appointments, and system logs. This document provides comprehensive documentation of the database schema, relationships, and usage patterns.

## Database Configuration

- **Database Type**: SQLite 3
- **File Location**: `data/healthcare.db`
- **Initialization Script**: `data/init_database.sql`
- **Character Encoding**: UTF-8
- **Connection Pool**: Single connection (development mode)

## Schema Overview

The database consists of 5 main tables with relationships designed to track user healthcare interactions:

```
users (1) ──── (N) predictions
  │
  ├─── (N) appointments  
  │
  ├─── (N) emergency_logs
  │
  └─── (N) location_logs
```

## Table Definitions

### 1. Users Table

**Purpose**: Manages user sessions and tracks user activity

```sql
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    session_id TEXT UNIQUE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_active TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

**Columns**:
- `id`: Auto-incrementing primary key
- `session_id`: Unique session identifier for user tracking
- `created_at`: Timestamp when user session was created
- `last_active`: Timestamp of last user activity

**Relationships**: One-to-many with predictions, appointments, emergency_logs, and location_logs

---

### 2. Predictions Table

**Purpose**: Stores disease prediction results and analysis history

```sql
CREATE TABLE predictions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_session TEXT NOT NULL,
    symptoms TEXT NOT NULL,
    predicted_disease TEXT NOT NULL,
    confidence REAL NOT NULL,
    severity TEXT NOT NULL CHECK (severity IN ('Low', 'Medium', 'High')),
    emergency BOOLEAN NOT NULL DEFAULT 0,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_session) REFERENCES users(session_id)
);
```

**Columns**:
- `id`: Auto-incrementing primary key
- `user_session`: Foreign key referencing users.session_id
- `symptoms`: Comma-separated list of symptoms entered by user
- `predicted_disease`: AI-predicted disease name
- `confidence`: Prediction confidence score (0.0 to 1.0)
- `severity`: Disease severity level (Low, Medium, High)
- `emergency`: Boolean flag indicating emergency condition
- `timestamp`: When prediction was made

**Indexes**:
- `idx_predictions_user_session`: Index on user_session for faster queries
- `idx_predictions_timestamp`: Index on timestamp for chronological queries

---

### 3. Appointments Table

**Purpose**: Manages appointment bookings and scheduling

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
    duration_minutes INTEGER DEFAULT 30,
    symptoms TEXT,
    notes TEXT,
    status TEXT DEFAULT 'scheduled' CHECK (status IN ('scheduled', 'confirmed', 'cancelled', 'completed')),
    confirmation_code TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_session) REFERENCES users(session_id)
);
```

**Columns**:
- `id`: Auto-incrementing primary key
- `user_session`: Foreign key referencing users.session_id
- `patient_name`: Name of the patient booking the appointment
- `doctor_name`: Name of the doctor for the appointment
- `doctor_specialization`: Doctor's medical specialization
- `appointment_date`: Date of the appointment (YYYY-MM-DD)
- `appointment_time`: Time of the appointment (HH:MM)
- `appointment_type`: Type of appointment (consultation, follow-up, etc.)
- `duration_minutes`: Expected duration of appointment in minutes
- `symptoms`: Symptoms or reason for the appointment
- `notes`: Additional notes or special instructions
- `status`: Current status (scheduled, confirmed, cancelled, completed)
- `confirmation_code`: Unique confirmation code for the appointment
- `created_at`: When appointment was booked

**Indexes**:
- `idx_appointments_user_session`: Index on user_session
- `idx_appointments_date`: Index on appointment_date for scheduling queries

---

### 4. Emergency Logs Table

**Purpose**: Tracks emergency events and responses

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
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_session) REFERENCES users(session_id)
);
```

**Columns**:
- `id`: Auto-incrementing primary key
- `user_session`: Foreign key referencing users.session_id
- `symptoms`: Symptoms that triggered emergency detection
- `emergency_type`: Type of emergency detected (cardiac, respiratory, etc.)
- `severity_level`: Severity of the emergency condition
- `location_lat`: Latitude coordinate when emergency was detected
- `location_lng`: Longitude coordinate when emergency was detected
- `ambulance_called`: Boolean flag indicating if ambulance was contacted
- `timestamp`: When emergency was detected

**Indexes**:
- `idx_emergency_logs_user_session`: Index on user_session
- `idx_emergency_logs_timestamp`: Index on timestamp for emergency response analysis

---

### 5. Location Logs Table

**Purpose**: Tracks GPS location data for emergency services and facility finding

```sql
CREATE TABLE location_logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_session TEXT NOT NULL,
    latitude REAL NOT NULL,
    longitude REAL NOT NULL,
    accuracy REAL,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_session) REFERENCES users(session_id)
);
```

**Columns**:
- `id`: Auto-incrementing primary key
- `user_session`: Foreign key referencing users.session_id
- `latitude`: GPS latitude coordinate
- `longitude`: GPS longitude coordinate
- `accuracy`: GPS accuracy in meters (if available)
- `timestamp`: When location was recorded

**Indexes**:
- `idx_location_logs_user_session`: Index on user_session for user location history

---

## Data Relationships

### Entity Relationship Diagram

```
┌─────────────┐     1:N     ┌─────────────────┐
│    users    │─────────────│   predictions   │
│             │             │                 │
│ session_id  │             │ user_session    │
│ created_at  │             │ symptoms        │
│ last_active │             │ predicted_disease│
└─────────────┘             │ confidence      │
       │                    │ severity        │
       │                    │ emergency       │
       │                    └─────────────────┘
       │
       │ 1:N     ┌─────────────────┐
       ├─────────│  appointments   │
       │         │                 │
       │         │ user_session    │
       │         │ patient_name    │
       │         │ doctor_name     │
       │         │ appointment_date│
       │         │ status          │
       │         └─────────────────┘
       │
       │ 1:N     ┌─────────────────┐
       ├─────────│ emergency_logs  │
       │         │                 │
       │         │ user_session    │
       │         │ symptoms        │
       │         │ emergency_type  │
       │         │ location_lat    │
       │         │ location_lng    │
       │         └─────────────────┘
       │
       │ 1:N     ┌─────────────────┐
       └─────────│ location_logs   │
                 │                 │
                 │ user_session    │
                 │ latitude        │
                 │ longitude       │
                 │ accuracy        │
                 └─────────────────┘
```

## Data Types and Constraints

### Data Type Specifications

- **INTEGER**: Used for IDs and numeric values
- **TEXT**: Used for strings and JSON data
- **REAL**: Used for floating-point numbers (coordinates, confidence scores)
- **TIMESTAMP**: SQLite datetime format (YYYY-MM-DD HH:MM:SS)
- **DATE**: Date format (YYYY-MM-DD)
- **TIME**: Time format (HH:MM)
- **BOOLEAN**: Stored as INTEGER (0 = false, 1 = true)

### Constraints and Validation

#### Check Constraints
- `predictions.severity`: Must be 'Low', 'Medium', or 'High'
- `appointments.status`: Must be 'scheduled', 'confirmed', 'cancelled', or 'completed'

#### Foreign Key Constraints
- All tables reference `users.session_id` to maintain data integrity
- Cascading deletes are not enabled to preserve historical data

#### Unique Constraints
- `users.session_id`: Ensures unique user sessions
- No other unique constraints to allow duplicate entries for historical tracking

## Performance Optimization

### Indexing Strategy

The database uses strategic indexing for optimal query performance:

1. **User-based queries**: Indexes on `user_session` columns for fast user data retrieval
2. **Time-based queries**: Indexes on timestamp columns for chronological analysis
3. **Appointment scheduling**: Index on `appointment_date` for availability checking

### Query Optimization Tips

1. **Use session-based filtering**: Always filter by `user_session` when possible
2. **Limit result sets**: Use LIMIT clauses for large datasets
3. **Index-friendly WHERE clauses**: Structure queries to use existing indexes
4. **Avoid SELECT ***: Select only needed columns for better performance

## Data Management

### Data Retention Policy

- **User sessions**: Maintained indefinitely for historical analysis
- **Predictions**: Kept for trend analysis and model improvement
- **Appointments**: Preserved for medical history tracking
- **Emergency logs**: Retained for safety analysis and improvement
- **Location logs**: Stored for emergency response optimization

### Backup and Recovery

```sql
-- Create backup
.backup data/healthcare_backup.db

-- Restore from backup
.restore data/healthcare_backup.db
```

### Data Cleanup Procedures

```sql
-- Remove old location logs (older than 30 days)
DELETE FROM location_logs 
WHERE timestamp < datetime('now', '-30 days');

-- Archive completed appointments (older than 1 year)
CREATE TABLE archived_appointments AS 
SELECT * FROM appointments 
WHERE status = 'completed' AND created_at < datetime('now', '-1 year');

DELETE FROM appointments 
WHERE status = 'completed' AND created_at < datetime('now', '-1 year');
```

## Security Considerations

### Data Protection

1. **Session isolation**: Each user's data is isolated by session_id
2. **No personal identifiers**: System uses anonymous session IDs
3. **Local storage only**: No external data transmission
4. **Input validation**: All inputs are sanitized before database insertion

### Access Control

- **Single-user application**: Designed for localhost use only
- **No authentication system**: Relies on session-based access
- **File-level security**: Database file permissions control access

## Common Queries

### User Analytics

```sql
-- Get user prediction history
SELECT predicted_disease, confidence, severity, timestamp 
FROM predictions 
WHERE user_session = ? 
ORDER BY timestamp DESC;

-- Count predictions by severity
SELECT severity, COUNT(*) as count 
FROM predictions 
WHERE user_session = ? 
GROUP BY severity;
```

### Appointment Management

```sql
-- Get upcoming appointments
SELECT doctor_name, appointment_date, appointment_time, status 
FROM appointments 
WHERE user_session = ? AND appointment_date >= date('now') 
ORDER BY appointment_date, appointment_time;

-- Check doctor availability
SELECT appointment_date, appointment_time 
FROM appointments 
WHERE doctor_name = ? AND appointment_date = ? AND status != 'cancelled';
```

### Emergency Analysis

```sql
-- Get emergency events
SELECT emergency_type, severity_level, symptoms, timestamp 
FROM emergency_logs 
WHERE user_session = ? 
ORDER BY timestamp DESC;

-- Emergency statistics
SELECT emergency_type, COUNT(*) as occurrences 
FROM emergency_logs 
GROUP BY emergency_type;
```

### Location Tracking

```sql
-- Get recent locations
SELECT latitude, longitude, accuracy, timestamp 
FROM location_logs 
WHERE user_session = ? 
ORDER BY timestamp DESC 
LIMIT 10;

-- Location history for emergency reference
SELECT latitude, longitude, timestamp 
FROM location_logs 
WHERE user_session = ? AND timestamp >= datetime('now', '-24 hours');
```

## Database Maintenance

### Regular Maintenance Tasks

1. **Weekly**: Analyze query performance and update statistics
2. **Monthly**: Review and optimize indexes
3. **Quarterly**: Perform database integrity checks
4. **As needed**: Clean up old location logs and temporary data

### Integrity Checks

```sql
-- Check foreign key integrity
PRAGMA foreign_key_check;

-- Verify database integrity
PRAGMA integrity_check;

-- Analyze database statistics
ANALYZE;
```

### Performance Monitoring

```sql
-- Check table sizes
SELECT name, COUNT(*) as row_count 
FROM sqlite_master 
CROSS JOIN (
    SELECT COUNT(*) FROM users UNION ALL
    SELECT COUNT(*) FROM predictions UNION ALL
    SELECT COUNT(*) FROM appointments UNION ALL
    SELECT COUNT(*) FROM emergency_logs UNION ALL
    SELECT COUNT(*) FROM location_logs
);

-- Monitor query performance
EXPLAIN QUERY PLAN SELECT * FROM predictions WHERE user_session = ?;
```

---

**Note**: This database schema is designed for educational and development purposes. For production use, consider additional security measures, data encryption, and compliance with healthcare data regulations.