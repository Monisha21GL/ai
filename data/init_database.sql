-- AI Healthcare Assistant Database Schema
-- SQLite database initialization script

-- Users table for session management
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    session_id TEXT UNIQUE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_active TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Predictions table for storing disease prediction results
CREATE TABLE IF NOT EXISTS predictions (
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

-- Appointments table for booking management
CREATE TABLE IF NOT EXISTS appointments (
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

-- Emergency logs table for tracking emergency events
CREATE TABLE IF NOT EXISTS emergency_logs (
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

-- Location logs table for GPS tracking
CREATE TABLE IF NOT EXISTS location_logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_session TEXT NOT NULL,
    latitude REAL NOT NULL,
    longitude REAL NOT NULL,
    accuracy REAL,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_session) REFERENCES users(session_id)
);

-- Create indexes for better performance
CREATE INDEX IF NOT EXISTS idx_predictions_user_session ON predictions(user_session);
CREATE INDEX IF NOT EXISTS idx_predictions_timestamp ON predictions(timestamp);
CREATE INDEX IF NOT EXISTS idx_appointments_user_session ON appointments(user_session);
CREATE INDEX IF NOT EXISTS idx_appointments_date ON appointments(appointment_date);
CREATE INDEX IF NOT EXISTS idx_emergency_logs_user_session ON emergency_logs(user_session);
CREATE INDEX IF NOT EXISTS idx_emergency_logs_timestamp ON emergency_logs(timestamp);
CREATE INDEX IF NOT EXISTS idx_location_logs_user_session ON location_logs(user_session);

-- Insert sample data for testing
INSERT OR IGNORE INTO users (session_id) VALUES ('sample_user_123');

-- Sample prediction data
INSERT OR IGNORE INTO predictions (user_session, symptoms, predicted_disease, confidence, severity, emergency) 
VALUES 
    ('sample_user_123', 'headache,fever,fatigue', 'Common Cold', 0.85, 'Low', 0),
    ('sample_user_123', 'chest_pain,shortness_of_breath', 'Heart Attack', 0.92, 'High', 1);

-- Sample appointment data
INSERT OR IGNORE INTO appointments (user_session, patient_name, doctor_name, doctor_specialization, appointment_date, appointment_time, appointment_type, status, confirmation_code)
VALUES 
    ('sample_user_123', 'John Doe', 'Dr. John Smith', 'General Medicine', '2024-12-20', '10:00', 'consultation', 'scheduled', 'CONF123A'),
    ('sample_user_123', 'John Doe', 'Dr. Sarah Johnson', 'Cardiology', '2024-12-22', '14:30', 'specialist_consultation', 'confirmed', 'CONF456B');