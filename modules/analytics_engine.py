"""
AI Healthcare Assistant - Analytics Engine

This module provides comprehensive analytics and historical data management
for the healthcare assistant application, including data export, statistics,
and user interaction logging.

Author: AI Healthcare Assistant Team
Date: 2024
Purpose: Academic project for healthcare AI demonstration
"""

import json
import csv
import io
import pandas as pd
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional, Union
import logging
from collections import Counter, defaultdict

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AnalyticsEngine:
    """
    Analytics engine for healthcare data analysis and export
    """
    
    def __init__(self, db_manager=None):
        """
        Initialize analytics engine
        
        Args:
            db_manager: Database manager instance
        """
        self.db_manager = db_manager
        
    def get_user_medical_history(self, user_session: str, limit: int = None) -> Dict[str, Any]:
        """
        Retrieve comprehensive medical history for a user
        
        Args:
            user_session: User session identifier
            limit: Maximum number of records per category
            
        Returns:
            Dictionary containing complete medical history
        """
        try:
            history = {
                'user_session': user_session,
                'generated_at': datetime.now().isoformat(),
                'predictions': [],
                'appointments': [],
                'emergency_logs': [],
                'location_logs': [],
                'summary': {}
            }
            
            if not self.db_manager:
                logger.warning("Database manager not available")
                return history
            
            # Get predictions history
            predictions = self.db_manager.get_user_predictions(user_session, limit or 50)
            history['predictions'] = predictions
            
            # Get appointments history
            appointments = self.db_manager.get_user_appointments(user_session)
            if limit:
                appointments = appointments[:limit]
            history['appointments'] = appointments
            
            # Get emergency logs
            emergency_logs = self.db_manager.get_user_emergency_logs(user_session)
            if limit:
                emergency_logs = emergency_logs[:limit]
            history['emergency_logs'] = emergency_logs
            
            # Get location history (if available)
            try:
                # Get recent locations
                with self.db_manager.get_connection() as conn:
                    cursor = conn.execute("""
                        SELECT * FROM location_logs 
                        WHERE user_session = ? 
                        ORDER BY timestamp DESC 
                        LIMIT ?
                    """, (user_session, limit or 20))
                    
                    location_logs = [dict(row) for row in cursor.fetchall()]
                    history['location_logs'] = location_logs
            except Exception as e:
                logger.warning(f"Could not retrieve location logs: {e}")
                history['location_logs'] = []
            
            # Generate summary statistics
            history['summary'] = self.generate_user_summary(history)
            
            return history
            
        except Exception as e:
            logger.error(f"Error retrieving medical history: {e}")
            return {
                'user_session': user_session,
                'generated_at': datetime.now().isoformat(),
                'predictions': [],
                'appointments': [],
                'emergency_logs': [],
                'location_logs': [],
                'summary': {},
                'error': str(e)
            }
    
    def generate_user_summary(self, history_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate summary statistics from user history
        
        Args:
            history_data: User's medical history data
            
        Returns:
            Dictionary containing summary statistics
        """
        try:
            summary = {
                'total_predictions': len(history_data.get('predictions', [])),
                'total_appointments': len(history_data.get('appointments', [])),
                'total_emergencies': len(history_data.get('emergency_logs', [])),
                'total_locations': len(history_data.get('location_logs', [])),
                'prediction_stats': {},
                'appointment_stats': {},
                'emergency_stats': {},
                'health_trends': {}
            }
            
            # Analyze predictions
            predictions = history_data.get('predictions', [])
            if predictions:
                diseases = [p.get('predicted_disease', '') for p in predictions]
                severities = [p.get('severity', '') for p in predictions]
                emergency_count = sum(1 for p in predictions if p.get('emergency', False))
                
                summary['prediction_stats'] = {
                    'most_common_diseases': dict(Counter(diseases).most_common(5)),
                    'severity_distribution': dict(Counter(severities)),
                    'emergency_predictions': emergency_count,
                    'average_confidence': sum(p.get('confidence', 0) for p in predictions) / len(predictions) if predictions else 0
                }
            
            # Analyze appointments
            appointments = history_data.get('appointments', [])
            if appointments:
                statuses = [a.get('status', '') for a in appointments]
                specializations = [a.get('doctor_specialization', '') for a in appointments if a.get('doctor_specialization')]
                
                summary['appointment_stats'] = {
                    'status_distribution': dict(Counter(statuses)),
                    'specialization_distribution': dict(Counter(specializations).most_common(5)),
                    'completed_appointments': sum(1 for a in appointments if a.get('status') == 'completed'),
                    'cancelled_appointments': sum(1 for a in appointments if a.get('status') == 'cancelled')
                }
            
            # Analyze emergency events
            emergencies = history_data.get('emergency_logs', [])
            if emergencies:
                emergency_types = [e.get('emergency_type', '') for e in emergencies]
                severity_levels = [e.get('severity_level', '') for e in emergencies]
                
                summary['emergency_stats'] = {
                    'emergency_types': dict(Counter(emergency_types)),
                    'severity_levels': dict(Counter(severity_levels)),
                    'ambulance_calls': sum(1 for e in emergencies if e.get('ambulance_called', False))
                }
            
            # Generate health trends
            summary['health_trends'] = self.analyze_health_trends(history_data)
            
            return summary
            
        except Exception as e:
            logger.error(f"Error generating user summary: {e}")
            return {}
    
    def analyze_health_trends(self, history_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyze health trends over time
        
        Args:
            history_data: User's medical history data
            
        Returns:
            Dictionary containing trend analysis
        """
        try:
            trends = {
                'prediction_frequency': {},
                'severity_trends': {},
                'emergency_patterns': {},
                'recent_activity': {}
            }
            
            predictions = history_data.get('predictions', [])
            
            # Analyze prediction frequency by month
            if predictions:
                monthly_counts = defaultdict(int)
                severity_by_month = defaultdict(list)
                
                for prediction in predictions:
                    timestamp = prediction.get('timestamp', '')
                    if timestamp:
                        try:
                            # Parse timestamp and get month-year
                            dt = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
                            month_key = dt.strftime('%Y-%m')
                            monthly_counts[month_key] += 1
                            severity_by_month[month_key].append(prediction.get('severity', ''))
                        except Exception:
                            continue
                
                trends['prediction_frequency'] = dict(monthly_counts)
                
                # Analyze severity trends
                severity_trends = {}
                for month, severities in severity_by_month.items():
                    severity_counts = Counter(severities)
                    severity_trends[month] = dict(severity_counts)
                
                trends['severity_trends'] = severity_trends
            
            # Analyze recent activity (last 30 days)
            recent_cutoff = datetime.now() - timedelta(days=30)
            recent_predictions = []
            recent_appointments = []
            recent_emergencies = []
            
            for prediction in predictions:
                timestamp = prediction.get('timestamp', '')
                if timestamp:
                    try:
                        dt = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
                        if dt >= recent_cutoff:
                            recent_predictions.append(prediction)
                    except Exception:
                        continue
            
            appointments = history_data.get('appointments', [])
            for appointment in appointments:
                created_at = appointment.get('created_at', '')
                if created_at:
                    try:
                        dt = datetime.fromisoformat(created_at.replace('Z', '+00:00'))
                        if dt >= recent_cutoff:
                            recent_appointments.append(appointment)
                    except Exception:
                        continue
            
            emergencies = history_data.get('emergency_logs', [])
            for emergency in emergencies:
                timestamp = emergency.get('timestamp', '')
                if timestamp:
                    try:
                        dt = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
                        if dt >= recent_cutoff:
                            recent_emergencies.append(emergency)
                    except Exception:
                        continue
            
            trends['recent_activity'] = {
                'predictions_last_30_days': len(recent_predictions),
                'appointments_last_30_days': len(recent_appointments),
                'emergencies_last_30_days': len(recent_emergencies)
            }
            
            return trends
            
        except Exception as e:
            logger.error(f"Error analyzing health trends: {e}")
            return {}
    
    def export_user_data(self, user_session: str, format_type: str = 'json', 
                        include_categories: List[str] = None) -> Union[str, bytes]:
        """
        Export user medical data in specified format
        
        Args:
            user_session: User session identifier
            format_type: Export format ('json', 'csv', 'txt')
            include_categories: List of data categories to include
            
        Returns:
            Exported data as string or bytes
        """
        try:
            # Get complete medical history
            history = self.get_user_medical_history(user_session)
            
            # Filter categories if specified
            if include_categories:
                filtered_history = {
                    'user_session': history['user_session'],
                    'generated_at': history['generated_at']
                }
                for category in include_categories:
                    if category in history:
                        filtered_history[category] = history[category]
                history = filtered_history
            
            if format_type.lower() == 'json':
                return json.dumps(history, indent=2, default=str)
            
            elif format_type.lower() == 'csv':
                return self._export_to_csv(history)
            
            elif format_type.lower() == 'txt':
                return self._export_to_text(history)
            
            else:
                raise ValueError(f"Unsupported export format: {format_type}")
                
        except Exception as e:
            logger.error(f"Error exporting user data: {e}")
            return f"Export failed: {str(e)}"
    
    def _export_to_csv(self, history: Dict[str, Any]) -> str:
        """
        Export history data to CSV format
        
        Args:
            history: Medical history data
            
        Returns:
            CSV formatted string
        """
        output = io.StringIO()
        
        # Export predictions
        if history.get('predictions'):
            output.write("=== DISEASE PREDICTIONS ===\n")
            predictions_df = pd.DataFrame(history['predictions'])
            predictions_df.to_csv(output, index=False)
            output.write("\n")
        
        # Export appointments
        if history.get('appointments'):
            output.write("=== APPOINTMENTS ===\n")
            appointments_df = pd.DataFrame(history['appointments'])
            appointments_df.to_csv(output, index=False)
            output.write("\n")
        
        # Export emergency logs
        if history.get('emergency_logs'):
            output.write("=== EMERGENCY LOGS ===\n")
            emergency_df = pd.DataFrame(history['emergency_logs'])
            emergency_df.to_csv(output, index=False)
            output.write("\n")
        
        # Export summary statistics
        if history.get('summary'):
            output.write("=== SUMMARY STATISTICS ===\n")
            summary_data = []
            for key, value in history['summary'].items():
                if isinstance(value, dict):
                    for subkey, subvalue in value.items():
                        summary_data.append({'Category': key, 'Metric': subkey, 'Value': subvalue})
                else:
                    summary_data.append({'Category': 'General', 'Metric': key, 'Value': value})
            
            if summary_data:
                summary_df = pd.DataFrame(summary_data)
                summary_df.to_csv(output, index=False)
        
        return output.getvalue()
    
    def _export_to_text(self, history: Dict[str, Any]) -> str:
        """
        Export history data to human-readable text format
        
        Args:
            history: Medical history data
            
        Returns:
            Text formatted string
        """
        output = []
        output.append("=" * 60)
        output.append("MEDICAL HISTORY REPORT")
        output.append("=" * 60)
        output.append(f"User Session: {history.get('user_session', 'Unknown')}")
        output.append(f"Generated: {history.get('generated_at', 'Unknown')}")
        output.append("")
        
        # Summary section
        summary = history.get('summary', {})
        if summary:
            output.append("SUMMARY STATISTICS")
            output.append("-" * 30)
            output.append(f"Total Predictions: {summary.get('total_predictions', 0)}")
            output.append(f"Total Appointments: {summary.get('total_appointments', 0)}")
            output.append(f"Total Emergencies: {summary.get('total_emergencies', 0)}")
            output.append("")
        
        # Predictions section
        predictions = history.get('predictions', [])
        if predictions:
            output.append("DISEASE PREDICTIONS")
            output.append("-" * 30)
            for i, pred in enumerate(predictions, 1):
                output.append(f"{i}. {pred.get('predicted_disease', 'Unknown')}")
                output.append(f"   Symptoms: {', '.join(pred.get('symptoms', []))}")
                output.append(f"   Severity: {pred.get('severity', 'Unknown')}")
                output.append(f"   Confidence: {pred.get('confidence', 0):.2f}")
                output.append(f"   Date: {pred.get('timestamp', 'Unknown')}")
                if pred.get('emergency'):
                    output.append("   ⚠️  EMERGENCY DETECTED")
                output.append("")
        
        # Appointments section
        appointments = history.get('appointments', [])
        if appointments:
            output.append("APPOINTMENTS")
            output.append("-" * 30)
            for i, apt in enumerate(appointments, 1):
                output.append(f"{i}. Dr. {apt.get('doctor_name', 'Unknown')}")
                output.append(f"   Specialization: {apt.get('doctor_specialization', 'Unknown')}")
                output.append(f"   Date: {apt.get('appointment_date', 'Unknown')} at {apt.get('appointment_time', 'Unknown')}")
                output.append(f"   Status: {apt.get('status', 'Unknown')}")
                if apt.get('symptoms'):
                    output.append(f"   Symptoms: {apt.get('symptoms')}")
                output.append("")
        
        # Emergency logs section
        emergencies = history.get('emergency_logs', [])
        if emergencies:
            output.append("EMERGENCY EVENTS")
            output.append("-" * 30)
            for i, emg in enumerate(emergencies, 1):
                output.append(f"{i}. {emg.get('emergency_type', 'Unknown Emergency')}")
                output.append(f"   Severity: {emg.get('severity_level', 'Unknown')}")
                symptoms = emg.get('symptoms', [])
                if isinstance(symptoms, list):
                    output.append(f"   Symptoms: {', '.join(symptoms)}")
                else:
                    output.append(f"   Symptoms: {symptoms}")
                output.append(f"   Date: {emg.get('timestamp', 'Unknown')}")
                if emg.get('ambulance_called'):
                    output.append("   🚑 Ambulance Called")
                output.append("")
        
        output.append("=" * 60)
        output.append("End of Report")
        output.append("=" * 60)
        
        return "\n".join(output)
    
    def get_system_analytics(self) -> Dict[str, Any]:
        """
        Get system-wide analytics and statistics
        
        Returns:
            Dictionary containing system analytics
        """
        try:
            if not self.db_manager:
                logger.warning("Database manager not available")
                return {}
            
            analytics = {
                'generated_at': datetime.now().isoformat(),
                'database_stats': {},
                'prediction_analytics': {},
                'appointment_analytics': {},
                'emergency_analytics': {},
                'user_analytics': {}
            }
            
            # Get database statistics
            analytics['database_stats'] = self.db_manager.get_database_stats()
            
            # Get prediction analytics
            analytics['prediction_analytics'] = self._get_prediction_analytics()
            
            # Get appointment analytics
            analytics['appointment_analytics'] = self._get_appointment_analytics()
            
            # Get emergency analytics
            analytics['emergency_analytics'] = self._get_emergency_analytics()
            
            # Get user analytics
            analytics['user_analytics'] = self._get_user_analytics()
            
            return analytics
            
        except Exception as e:
            logger.error(f"Error getting system analytics: {e}")
            return {'error': str(e)}
    
    def _get_prediction_analytics(self) -> Dict[str, Any]:
        """Get prediction-related analytics"""
        try:
            with self.db_manager.get_connection() as conn:
                # Get all predictions
                cursor = conn.execute("SELECT * FROM predictions ORDER BY timestamp DESC")
                predictions = [dict(row) for row in cursor.fetchall()]
                
                if not predictions:
                    return {}
                
                # Analyze predictions
                diseases = [p['predicted_disease'] for p in predictions]
                severities = [p['severity'] for p in predictions]
                confidences = [p['confidence'] for p in predictions]
                emergency_count = sum(1 for p in predictions if p['emergency'])
                
                return {
                    'total_predictions': len(predictions),
                    'most_common_diseases': dict(Counter(diseases).most_common(10)),
                    'severity_distribution': dict(Counter(severities)),
                    'average_confidence': sum(confidences) / len(confidences) if confidences else 0,
                    'emergency_predictions': emergency_count,
                    'emergency_rate': emergency_count / len(predictions) if predictions else 0
                }
                
        except Exception as e:
            logger.error(f"Error getting prediction analytics: {e}")
            return {}
    
    def _get_appointment_analytics(self) -> Dict[str, Any]:
        """Get appointment-related analytics"""
        try:
            with self.db_manager.get_connection() as conn:
                # Get all appointments
                cursor = conn.execute("SELECT * FROM appointments ORDER BY created_at DESC")
                appointments = [dict(row) for row in cursor.fetchall()]
                
                if not appointments:
                    return {}
                
                # Analyze appointments
                statuses = [a['status'] for a in appointments]
                specializations = [a.get('doctor_specialization', '') for a in appointments if a.get('doctor_specialization')]
                doctors = [a['doctor_name'] for a in appointments]
                
                return {
                    'total_appointments': len(appointments),
                    'status_distribution': dict(Counter(statuses)),
                    'specialization_distribution': dict(Counter(specializations).most_common(10)),
                    'popular_doctors': dict(Counter(doctors).most_common(10)),
                    'completion_rate': sum(1 for a in appointments if a['status'] == 'completed') / len(appointments) if appointments else 0,
                    'cancellation_rate': sum(1 for a in appointments if a['status'] == 'cancelled') / len(appointments) if appointments else 0
                }
                
        except Exception as e:
            logger.error(f"Error getting appointment analytics: {e}")
            return {}
    
    def _get_emergency_analytics(self) -> Dict[str, Any]:
        """Get emergency-related analytics"""
        try:
            with self.db_manager.get_connection() as conn:
                # Get all emergency logs
                cursor = conn.execute("SELECT * FROM emergency_logs ORDER BY timestamp DESC")
                emergencies = [dict(row) for row in cursor.fetchall()]
                
                if not emergencies:
                    return {}
                
                # Analyze emergencies
                emergency_types = [e['emergency_type'] for e in emergencies]
                severity_levels = [e['severity_level'] for e in emergencies]
                ambulance_calls = sum(1 for e in emergencies if e.get('ambulance_called', False))
                
                return {
                    'total_emergencies': len(emergencies),
                    'emergency_types': dict(Counter(emergency_types)),
                    'severity_distribution': dict(Counter(severity_levels)),
                    'ambulance_calls': ambulance_calls,
                    'ambulance_call_rate': ambulance_calls / len(emergencies) if emergencies else 0
                }
                
        except Exception as e:
            logger.error(f"Error getting emergency analytics: {e}")
            return {}
    
    def _get_user_analytics(self) -> Dict[str, Any]:
        """Get user-related analytics"""
        try:
            with self.db_manager.get_connection() as conn:
                # Get user statistics
                cursor = conn.execute("SELECT COUNT(*) as total_users FROM users")
                total_users = cursor.fetchone()['total_users']
                
                # Get active users (users with recent activity)
                cursor = conn.execute("""
                    SELECT COUNT(*) as active_users 
                    FROM users 
                    WHERE last_active >= datetime('now', '-30 days')
                """)
                active_users = cursor.fetchone()['active_users']
                
                return {
                    'total_users': total_users,
                    'active_users_30_days': active_users,
                    'user_retention_rate': active_users / total_users if total_users > 0 else 0
                }
                
        except Exception as e:
            logger.error(f"Error getting user analytics: {e}")
            return {}
    
    def log_user_interaction(self, user_session: str, interaction_type: str, 
                           interaction_data: Dict[str, Any]) -> bool:
        """
        Log user interaction for analytics
        
        Args:
            user_session: User session identifier
            interaction_type: Type of interaction (prediction, appointment, etc.)
            interaction_data: Additional interaction data
            
        Returns:
            True if logged successfully, False otherwise
        """
        try:
            # Update user activity
            if self.db_manager:
                self.db_manager.update_user_activity(user_session)
            
            # Log interaction (this could be extended to a separate interactions table)
            logger.info(f"User interaction logged: {user_session} - {interaction_type}")
            
            return True
            
        except Exception as e:
            logger.error(f"Error logging user interaction: {e}")
            return False


# Global analytics engine instance
analytics_engine = None

def get_analytics_engine():
    """
    Get global analytics engine instance (singleton pattern)
    
    Returns:
        AnalyticsEngine instance
    """
    global analytics_engine
    if analytics_engine is None:
        # Import here to avoid circular imports
        from modules.database_manager import get_db_manager
        analytics_engine = AnalyticsEngine(get_db_manager())
    return analytics_engine


if __name__ == "__main__":
    # Test the analytics engine
    print("Testing Analytics Engine...")
    
    analytics = AnalyticsEngine()
    
    # Test system analytics
    system_stats = analytics.get_system_analytics()
    print(f"System analytics: {system_stats}")
    
    print("Analytics Engine test completed!")