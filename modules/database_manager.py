"""
AI Healthcare Assistant - Database Manager

This module handles all database operations including SQLite connections,
CRUD operations, and data validation for the healthcare assistant application.

Author: AI Healthcare Assistant Team
Date: 2024
Purpose: Academic project for healthcare AI demonstration
"""

import sqlite3
import pandas as pd
import os
import json
from datetime import datetime, date, time
from typing import List, Dict, Any, Optional, Union
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DatabaseManager:
    """
    Centralized database manager for all healthcare assistant data operations
    """
    
    def __init__(self, db_path: str = "data/healthcare.db"):
        """
        Initialize database manager
        
        Args:
            db_path: Path to SQLite database file
        """
        self.db_path = db_path
        self.ensure_database_exists()
        self.initialize_database()
        
    def ensure_database_exists(self):
        """Ensure the database directory and file exist"""
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        
    def get_connection(self) -> sqlite3.Connection:
        """
        Get database connection with proper configuration
        
        Returns:
            SQLite connection object
        """
        conn = sqlite3.Connection(self.db_path)
        conn.row_factory = sqlite3.Row  # Enable column access by name
        conn.execute("PRAGMA foreign_keys = ON")  # Enable foreign key constraints
        return conn
    
    def initialize_database(self):
        """Initialize database with schema from SQL file"""
        try:
            # Read and execute schema from SQL file
            schema_path = "data/init_database.sql"
            if os.path.exists(schema_path):
                with open(schema_path, 'r') as f:
                    schema_sql = f.read()
                
                with self.get_connection() as conn:
                    conn.executescript(schema_sql)
                    conn.commit()
                    
                logger.info("Database initialized successfully")
            else:
                logger.warning(f"Schema file not found: {schema_path}")
                self.create_tables_programmatically()
                
        except Exception as e:
            logger.error(f"Error initializing database: {e}")
            self.create_tables_programmatically()
    
    def create_tables_programmatically(self):
        """Create database tables programmatically if SQL file is not available"""
        with self.get_connection() as conn:
            # Users table
            conn.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    session_id TEXT UNIQUE NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    last_active TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # Predictions table
            conn.execute("""
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
                )
            """)
            
            # Appointments table
            conn.execute("""
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
                )
            """)
            
            # Emergency logs table
            conn.execute("""
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
                )
            """)
            
            # Location logs table
            conn.execute("""
                CREATE TABLE IF NOT EXISTS location_logs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_session TEXT NOT NULL,
                    latitude REAL NOT NULL,
                    longitude REAL NOT NULL,
                    accuracy REAL,
                    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_session) REFERENCES users(session_id)
                )
            """)
            
            conn.commit()
            logger.info("Database tables created programmatically")
    
    # User Management Methods
    
    def create_user(self, session_id: str) -> bool:
        """
        Create a new user session
        
        Args:
            session_id: Unique session identifier
            
        Returns:
            True if user created successfully, False otherwise
        """
        try:
            with self.get_connection() as conn:
                conn.execute(
                    "INSERT OR IGNORE INTO users (session_id) VALUES (?)",
                    (session_id,)
                )
                conn.commit()
                return True
        except Exception as e:
            logger.error(f"Error creating user: {e}")
            return False
    
    def update_user_activity(self, session_id: str) -> bool:
        """
        Update user's last activity timestamp
        
        Args:
            session_id: User session identifier
            
        Returns:
            True if updated successfully, False otherwise
        """
        try:
            with self.get_connection() as conn:
                conn.execute(
                    "UPDATE users SET last_active = CURRENT_TIMESTAMP WHERE session_id = ?",
                    (session_id,)
                )
                conn.commit()
                return True
        except Exception as e:
            logger.error(f"Error updating user activity: {e}")
            return False
    
    def get_user(self, session_id: str) -> Optional[Dict[str, Any]]:
        """
        Get user information by session ID
        
        Args:
            session_id: User session identifier
            
        Returns:
            User data dictionary or None if not found
        """
        try:
            with self.get_connection() as conn:
                cursor = conn.execute(
                    "SELECT * FROM users WHERE session_id = ?",
                    (session_id,)
                )
                row = cursor.fetchone()
                return dict(row) if row else None
        except Exception as e:
            logger.error(f"Error getting user: {e}")
            return None
    
    # Prediction Management Methods
    
    def save_prediction(self, user_session: str, symptoms: List[str], 
                       predicted_disease: str, confidence: float, 
                       severity: str, emergency: bool) -> Optional[int]:
        """
        Save disease prediction to database
        
        Args:
            user_session: User session identifier
            symptoms: List of symptoms
            predicted_disease: Predicted disease name
            confidence: Prediction confidence (0-1)
            severity: Severity level (Low/Medium/High)
            emergency: Whether it's an emergency
            
        Returns:
            Prediction ID if saved successfully, None otherwise
        """
        try:
            # Validate inputs
            if not self.validate_severity(severity):
                raise ValueError(f"Invalid severity level: {severity}")
            
            if not 0 <= confidence <= 1:
                raise ValueError(f"Invalid confidence value: {confidence}")
            
            symptoms_json = json.dumps(symptoms)
            
            # Ensure user exists before saving prediction
            self.create_user(user_session)
            
            with self.get_connection() as conn:
                cursor = conn.execute("""
                    INSERT INTO predictions 
                    (user_session, symptoms, predicted_disease, confidence, severity, emergency)
                    VALUES (?, ?, ?, ?, ?, ?)
                """, (user_session, symptoms_json, predicted_disease, confidence, severity, emergency))
                
                conn.commit()
                return cursor.lastrowid
                
        except Exception as e:
            logger.error(f"Error saving prediction: {e}")
            return None
    
    def get_user_predictions(self, user_session: str, limit: int = 10) -> List[Dict[str, Any]]:
        """
        Get user's prediction history
        
        Args:
            user_session: User session identifier
            limit: Maximum number of predictions to return
            
        Returns:
            List of prediction dictionaries
        """
        try:
            with self.get_connection() as conn:
                cursor = conn.execute("""
                    SELECT * FROM predictions 
                    WHERE user_session = ? 
                    ORDER BY timestamp DESC 
                    LIMIT ?
                """, (user_session, limit))
                
                predictions = []
                for row in cursor.fetchall():
                    prediction = dict(row)
                    # Parse symptoms JSON
                    prediction['symptoms'] = json.loads(prediction['symptoms'])
                    predictions.append(prediction)
                
                return predictions
                
        except Exception as e:
            logger.error(f"Error getting user predictions: {e}")
            return []
    
    def get_prediction_by_id(self, prediction_id: int) -> Optional[Dict[str, Any]]:
        """
        Get specific prediction by ID
        
        Args:
            prediction_id: Prediction identifier
            
        Returns:
            Prediction dictionary or None if not found
        """
        try:
            with self.get_connection() as conn:
                cursor = conn.execute(
                    "SELECT * FROM predictions WHERE id = ?",
                    (prediction_id,)
                )
                row = cursor.fetchone()
                if row:
                    prediction = dict(row)
                    prediction['symptoms'] = json.loads(prediction['symptoms'])
                    return prediction
                return None
        except Exception as e:
            logger.error(f"Error getting prediction: {e}")
            return None
    
    # Appointment Management Methods
    
    def save_appointment(self, user_session: str, doctor_name: str, 
                        doctor_specialization: str, appointment_date: Union[str, date],
                        appointment_time: Union[str, time], notes: str = "") -> Optional[int]:
        """
        Save appointment booking to database
        
        Args:
            user_session: User session identifier
            doctor_name: Doctor's name
            doctor_specialization: Doctor's specialization
            appointment_date: Appointment date
            appointment_time: Appointment time
            notes: Additional notes
            
        Returns:
            Appointment ID if saved successfully, None otherwise
        """
        try:
            # Convert date and time to strings if needed
            if isinstance(appointment_date, date):
                appointment_date = appointment_date.isoformat()
            if isinstance(appointment_time, time):
                appointment_time = appointment_time.strftime("%H:%M")
            
            with self.get_connection() as conn:
                cursor = conn.execute("""
                    INSERT INTO appointments 
                    (user_session, doctor_name, doctor_specialization, 
                     appointment_date, appointment_time, notes)
                    VALUES (?, ?, ?, ?, ?, ?)
                """, (user_session, doctor_name, doctor_specialization, 
                      appointment_date, appointment_time, notes))
                
                conn.commit()
                return cursor.lastrowid
                
        except Exception as e:
            logger.error(f"Error saving appointment: {e}")
            return None
    
    def get_user_appointments(self, user_session: str, status: str = None) -> List[Dict[str, Any]]:
        """
        Get user's appointments
        
        Args:
            user_session: User session identifier
            status: Filter by appointment status (optional)
            
        Returns:
            List of appointment dictionaries
        """
        try:
            with self.get_connection() as conn:
                if status:
                    cursor = conn.execute("""
                        SELECT * FROM appointments 
                        WHERE user_session = ? AND status = ?
                        ORDER BY appointment_date, appointment_time
                    """, (user_session, status))
                else:
                    cursor = conn.execute("""
                        SELECT * FROM appointments 
                        WHERE user_session = ?
                        ORDER BY appointment_date, appointment_time
                    """, (user_session,))
                
                return [dict(row) for row in cursor.fetchall()]
                
        except Exception as e:
            logger.error(f"Error getting user appointments: {e}")
            return []
    
    def update_appointment_status(self, appointment_id: int, status: str) -> bool:
        """
        Update appointment status
        
        Args:
            appointment_id: Appointment identifier
            status: New status (scheduled/confirmed/cancelled/completed)
            
        Returns:
            True if updated successfully, False otherwise
        """
        try:
            valid_statuses = ['scheduled', 'confirmed', 'cancelled', 'completed']
            if status not in valid_statuses:
                raise ValueError(f"Invalid status: {status}")
            
            with self.get_connection() as conn:
                conn.execute(
                    "UPDATE appointments SET status = ? WHERE id = ?",
                    (status, appointment_id)
                )
                conn.commit()
                return True
                
        except Exception as e:
            logger.error(f"Error updating appointment status: {e}")
            return False
    
    def check_appointment_conflict(self, doctor_name: str, appointment_date: str, 
                                 appointment_time: str) -> bool:
        """
        Check if appointment time conflicts with existing bookings
        
        Args:
            doctor_name: Doctor's name
            appointment_date: Appointment date
            appointment_time: Appointment time
            
        Returns:
            True if conflict exists, False otherwise
        """
        try:
            with self.get_connection() as conn:
                cursor = conn.execute("""
                    SELECT COUNT(*) FROM appointments 
                    WHERE doctor_name = ? AND appointment_date = ? 
                    AND appointment_time = ? AND status IN ('scheduled', 'confirmed')
                """, (doctor_name, appointment_date, appointment_time))
                
                count = cursor.fetchone()[0]
                return count > 0
                
        except Exception as e:
            logger.error(f"Error checking appointment conflict: {e}")
            return True  # Assume conflict on error for safety

    def create_appointment(self, appointment_data: Dict[str, Any]) -> Optional[int]:
        """
        Create a new appointment record
        
        Args:
            appointment_data: Dictionary containing appointment details
            
        Returns:
            Appointment ID if successful, None otherwise
        """
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT INTO appointments (
                        user_session, patient_name, doctor_name, doctor_specialization,
                        appointment_date, appointment_time, appointment_type, duration_minutes,
                        symptoms, notes, status, confirmation_code
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    appointment_data.get('user_session', 'default'),
                    appointment_data['patient_name'],
                    appointment_data['doctor_name'],
                    appointment_data.get('doctor_specialization', ''),
                    appointment_data['appointment_date'],
                    appointment_data['appointment_time'],
                    appointment_data['appointment_type'],
                    appointment_data.get('duration_minutes', 30),
                    appointment_data.get('symptoms', ''),
                    appointment_data.get('notes', ''),
                    appointment_data.get('status', 'scheduled'),
                    appointment_data.get('confirmation_code', '')
                ))
                
                appointment_id = cursor.lastrowid
                conn.commit()
                logger.info(f"Appointment created with ID: {appointment_id}")
                return appointment_id
                
        except Exception as e:
            logger.error(f"Error creating appointment: {str(e)}")
            return None

    def get_appointments_by_doctor_date(self, doctor_name: str, appointment_date: str) -> List[Dict[str, Any]]:
        """
        Get all appointments for a doctor on a specific date
        
        Args:
            doctor_name: Name of the doctor
            appointment_date: Date in YYYY-MM-DD format
            
        Returns:
            List of appointment dictionaries
        """
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    SELECT * FROM appointments 
                    WHERE doctor_name = ? AND appointment_date = ? AND status != 'cancelled'
                    ORDER BY appointment_time
                """, (doctor_name, appointment_date))
                
                columns = [description[0] for description in cursor.description]
                appointments = []
                
                for row in cursor.fetchall():
                    appointment = dict(zip(columns, row))
                    appointments.append(appointment)
                
                return appointments
                
        except Exception as e:
            logger.error(f"Error getting doctor appointments: {str(e)}")
            return []

    def get_appointments_by_patient(self, patient_name: str) -> List[Dict[str, Any]]:
        """
        Get all appointments for a patient
        
        Args:
            patient_name: Name of the patient
            
        Returns:
            List of appointment dictionaries
        """
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    SELECT * FROM appointments 
                    WHERE patient_name = ? 
                    ORDER BY appointment_date DESC, appointment_time DESC
                """, (patient_name,))
                
                columns = [description[0] for description in cursor.description]
                appointments = []
                
                for row in cursor.fetchall():
                    appointment = dict(zip(columns, row))
                    appointments.append(appointment)
                
                return appointments
                
        except Exception as e:
            logger.error(f"Error getting patient appointments: {str(e)}")
            return []

    def get_appointments_by_date(self, appointment_date: str) -> List[Dict[str, Any]]:
        """
        Get all appointments for a specific date
        
        Args:
            appointment_date: Date in YYYY-MM-DD format
            
        Returns:
            List of appointment dictionaries
        """
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    SELECT * FROM appointments 
                    WHERE appointment_date = ? AND status != 'cancelled'
                    ORDER BY appointment_time
                """, (appointment_date,))
                
                columns = [description[0] for description in cursor.description]
                appointments = []
                
                for row in cursor.fetchall():
                    appointment = dict(zip(columns, row))
                    appointments.append(appointment)
                
                return appointments
                
        except Exception as e:
            logger.error(f"Error getting appointments by date: {str(e)}")
            return []

    def get_all_appointments(self) -> List[Dict[str, Any]]:
        """
        Get all appointments in the system
        
        Returns:
            List of all appointment dictionaries
        """
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    SELECT * FROM appointments 
                    ORDER BY appointment_date DESC, appointment_time DESC
                """)
                
                columns = [description[0] for description in cursor.description]
                appointments = []
                
                for row in cursor.fetchall():
                    appointment = dict(zip(columns, row))
                    appointments.append(appointment)
                
                return appointments
                
        except Exception as e:
            logger.error(f"Error getting all appointments: {str(e)}")
            return []

    def cancel_appointment(self, appointment_id: int, reason: str = '') -> bool:
        """
        Cancel an appointment
        
        Args:
            appointment_id: ID of the appointment to cancel
            reason: Reason for cancellation
            
        Returns:
            True if successful, False otherwise
        """
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    UPDATE appointments 
                    SET status = 'cancelled', notes = COALESCE(notes, '') || ? || ?
                    WHERE id = ?
                """, ('\nCancellation reason: ', reason, appointment_id))
                
                if cursor.rowcount > 0:
                    conn.commit()
                    logger.info(f"Appointment {appointment_id} cancelled successfully")
                    return True
                else:
                    logger.warning(f"No appointment found with ID: {appointment_id}")
                    return False
                
        except Exception as e:
            logger.error(f"Error cancelling appointment: {str(e)}")
            return False
    
    # Emergency Management Methods
    
    def log_emergency(self, user_session: str, symptoms: List[str], 
                     emergency_type: str, severity_level: str,
                     location_lat: float = None, location_lng: float = None,
                     ambulance_called: bool = False) -> Optional[int]:
        """
        Log emergency event to database
        
        Args:
            user_session: User session identifier
            symptoms: List of symptoms
            emergency_type: Type of emergency
            severity_level: Severity level
            location_lat: Latitude (optional)
            location_lng: Longitude (optional)
            ambulance_called: Whether ambulance was called
            
        Returns:
            Emergency log ID if saved successfully, None otherwise
        """
        try:
            symptoms_json = json.dumps(symptoms)
            
            # Ensure user exists before logging emergency
            self.create_user(user_session)
            
            with self.get_connection() as conn:
                cursor = conn.execute("""
                    INSERT INTO emergency_logs 
                    (user_session, symptoms, emergency_type, severity_level,
                     location_lat, location_lng, ambulance_called)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                """, (user_session, symptoms_json, emergency_type, severity_level,
                      location_lat, location_lng, ambulance_called))
                
                conn.commit()
                return cursor.lastrowid
                
        except Exception as e:
            logger.error(f"Error logging emergency: {e}")
            return None
    
    def get_user_emergency_logs(self, user_session: str) -> List[Dict[str, Any]]:
        """
        Get user's emergency logs
        
        Args:
            user_session: User session identifier
            
        Returns:
            List of emergency log dictionaries
        """
        try:
            with self.get_connection() as conn:
                cursor = conn.execute("""
                    SELECT * FROM emergency_logs 
                    WHERE user_session = ? 
                    ORDER BY timestamp DESC
                """, (user_session,))
                
                logs = []
                for row in cursor.fetchall():
                    log = dict(row)
                    log['symptoms'] = json.loads(log['symptoms'])
                    logs.append(log)
                
                return logs
                
        except Exception as e:
            logger.error(f"Error getting emergency logs: {e}")
            return []
    
    # Location Management Methods
    
    def save_location(self, user_session: str, latitude: float, 
                     longitude: float, accuracy: float = None) -> Optional[int]:
        """
        Save user location to database
        
        Args:
            user_session: User session identifier
            latitude: Latitude coordinate
            longitude: Longitude coordinate
            accuracy: GPS accuracy in meters (optional)
            
        Returns:
            Location log ID if saved successfully, None otherwise
        """
        try:
            # Ensure user exists before saving location
            self.create_user(user_session)
            
            with self.get_connection() as conn:
                cursor = conn.execute("""
                    INSERT INTO location_logs 
                    (user_session, latitude, longitude, accuracy)
                    VALUES (?, ?, ?, ?)
                """, (user_session, latitude, longitude, accuracy))
                
                conn.commit()
                return cursor.lastrowid
                
        except Exception as e:
            logger.error(f"Error saving location: {e}")
            return None
    
    def get_user_latest_location(self, user_session: str) -> Optional[Dict[str, Any]]:
        """
        Get user's latest location
        
        Args:
            user_session: User session identifier
            
        Returns:
            Location dictionary or None if not found
        """
        try:
            with self.get_connection() as conn:
                cursor = conn.execute("""
                    SELECT * FROM location_logs 
                    WHERE user_session = ? 
                    ORDER BY timestamp DESC 
                    LIMIT 1
                """, (user_session,))
                
                row = cursor.fetchone()
                return dict(row) if row else None
                
        except Exception as e:
            logger.error(f"Error getting latest location: {e}")
            return None
    
    # CSV Data Loading Methods
    
    def load_doctors_data(self) -> pd.DataFrame:
        """
        Load doctors data from CSV file
        
        Returns:
            Pandas DataFrame with doctors data
        """
        try:
            csv_path = "data/doctors.csv"
            if os.path.exists(csv_path):
                return pd.read_csv(csv_path)
            else:
                logger.warning(f"Doctors CSV file not found: {csv_path}")
                return pd.DataFrame()
        except Exception as e:
            logger.error(f"Error loading doctors data: {e}")
            return pd.DataFrame()
    
    def load_hospitals_data(self) -> pd.DataFrame:
        """
        Load hospitals data from CSV file
        
        Returns:
            Pandas DataFrame with hospitals data
        """
        try:
            csv_path = "data/hospitals.csv"
            if os.path.exists(csv_path):
                return pd.read_csv(csv_path)
            else:
                logger.warning(f"Hospitals CSV file not found: {csv_path}")
                return pd.DataFrame()
        except Exception as e:
            logger.error(f"Error loading hospitals data: {e}")
            return pd.DataFrame()
    
    def load_symptoms_diseases_data(self) -> pd.DataFrame:
        """
        Load symptoms-diseases training data from CSV file
        
        Returns:
            Pandas DataFrame with symptoms-diseases data
        """
        try:
            csv_path = "data/symptoms_diseases.csv"
            if os.path.exists(csv_path):
                return pd.read_csv(csv_path)
            else:
                logger.warning(f"Symptoms-diseases CSV file not found: {csv_path}")
                return pd.DataFrame()
        except Exception as e:
            logger.error(f"Error loading symptoms-diseases data: {e}")
            return pd.DataFrame()
    
    # Validation Methods
    
    def validate_severity(self, severity: str) -> bool:
        """
        Validate severity level
        
        Args:
            severity: Severity level to validate
            
        Returns:
            True if valid, False otherwise
        """
        return severity in ['Low', 'Medium', 'High']
    
    def validate_appointment_status(self, status: str) -> bool:
        """
        Validate appointment status
        
        Args:
            status: Status to validate
            
        Returns:
            True if valid, False otherwise
        """
        return status in ['scheduled', 'confirmed', 'cancelled', 'completed']
    
    # Utility Methods
    
    def get_database_stats(self) -> Dict[str, int]:
        """
        Get database statistics
        
        Returns:
            Dictionary with table row counts
        """
        try:
            stats = {}
            tables = ['users', 'predictions', 'appointments', 'emergency_logs', 'location_logs']
            
            with self.get_connection() as conn:
                for table in tables:
                    cursor = conn.execute(f"SELECT COUNT(*) FROM {table}")
                    stats[table] = cursor.fetchone()[0]
            
            return stats
            
        except Exception as e:
            logger.error(f"Error getting database stats: {e}")
            return {}
    
    def cleanup_old_data(self, days_old: int = 30) -> bool:
        """
        Clean up old data from database
        
        Args:
            days_old: Number of days to keep data
            
        Returns:
            True if cleanup successful, False otherwise
        """
        try:
            with self.get_connection() as conn:
                # Clean up old location logs
                conn.execute("""
                    DELETE FROM location_logs 
                    WHERE timestamp < datetime('now', '-{} days')
                """.format(days_old))
                
                # Clean up old predictions (keep emergency ones)
                conn.execute("""
                    DELETE FROM predictions 
                    WHERE timestamp < datetime('now', '-{} days') 
                    AND emergency = 0
                """.format(days_old))
                
                conn.commit()
                return True
                
        except Exception as e:
            logger.error(f"Error cleaning up old data: {e}")
            return False


# Global database manager instance
db_manager = None

def get_db_manager() -> DatabaseManager:
    """
    Get global database manager instance (singleton pattern)
    
    Returns:
        DatabaseManager instance
    """
    global db_manager
    if db_manager is None:
        db_manager = DatabaseManager()
    return db_manager


if __name__ == "__main__":
    # Test the database manager
    print("Testing Database Manager...")
    
    db = DatabaseManager()
    
    # Test user creation
    test_session = "test_session_123"
    print(f"Creating user: {db.create_user(test_session)}")
    
    # Test prediction saving
    prediction_id = db.save_prediction(
        test_session, 
        ["headache", "fever"], 
        "Common Cold", 
        0.85, 
        "Low", 
        False
    )
    print(f"Saved prediction ID: {prediction_id}")
    
    # Test data loading
    doctors_df = db.load_doctors_data()
    print(f"Loaded {len(doctors_df)} doctors")
    
    # Test database stats
    stats = db.get_database_stats()
    print(f"Database stats: {stats}")
    
    print("Database Manager test completed!")