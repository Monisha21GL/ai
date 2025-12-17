"""
AI Healthcare Assistant - Appointment Booking System

This module implements appointment scheduling logic with conflict detection,
confirmation system, and data persistence for healthcare appointments.

Author: AI Healthcare Assistant Team
Date: 2024
Purpose: Academic project for healthcare AI demonstration
"""

import json
import logging
from typing import List, Dict, Any, Optional, Tuple
from datetime import datetime, timedelta, time
import pandas as pd

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AppointmentManager:
    """
    Appointment booking system with scheduling logic and conflict prevention
    """
    
    def __init__(self):
        """Initialize appointment manager with database connection"""
        # Initialize database manager with error handling
        self.db_manager = None
        try:
            import sys
            import os
            sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
            from modules.database_manager import get_db_manager
            self.db_manager = get_db_manager()
            logger.info("Database manager loaded successfully")
        except Exception as e:
            logger.warning(f"Database manager not available: {e}")
        
        # Doctor working hours (24-hour format)
        self.working_hours = {
            'start_time': time(9, 0),   # 9:00 AM
            'end_time': time(17, 0),    # 5:00 PM
            'lunch_start': time(12, 0), # 12:00 PM
            'lunch_end': time(13, 0)    # 1:00 PM
        }
        
        # Appointment duration in minutes
        self.appointment_duration = 30
        
        # Available time slots per day
        self.daily_slots = self._generate_daily_slots()
        
        # Appointment types and their durations
        self.appointment_types = {
            'consultation': 30,
            'follow_up': 20,
            'emergency': 15,
            'routine_checkup': 45,
            'specialist_consultation': 60
        }

    def _generate_daily_slots(self) -> List[time]:
        """Generate available appointment time slots for a day"""
        slots = []
        current_time = datetime.combine(datetime.today(), self.working_hours['start_time'])
        end_time = datetime.combine(datetime.today(), self.working_hours['end_time'])
        lunch_start = datetime.combine(datetime.today(), self.working_hours['lunch_start'])
        lunch_end = datetime.combine(datetime.today(), self.working_hours['lunch_end'])
        
        while current_time < end_time:
            # Skip lunch hour
            if not (lunch_start <= current_time < lunch_end):
                slots.append(current_time.time())
            current_time += timedelta(minutes=self.appointment_duration)
        
        return slots

    def book_appointment(self, patient_name: str, doctor_name: str, 
                        appointment_date: str, appointment_time: str,
                        appointment_type: str = 'consultation',
                        symptoms: str = '', notes: str = '') -> Dict[str, Any]:
        """
        Book an appointment with conflict detection and validation
        
        Args:
            patient_name: Name of the patient
            doctor_name: Name of the doctor
            appointment_date: Date in YYYY-MM-DD format
            appointment_time: Time in HH:MM format
            appointment_type: Type of appointment
            symptoms: Patient symptoms (optional)
            notes: Additional notes (optional)
            
        Returns:
            Dictionary with booking result and details
        """
        try:
            # Validate input data
            validation_result = self._validate_appointment_data(
                patient_name, doctor_name, appointment_date, appointment_time, appointment_type
            )
            
            if not validation_result['valid']:
                return {
                    'success': False,
                    'message': validation_result['message'],
                    'appointment_id': None
                }
            
            # Check for conflicts
            conflict_check = self._check_appointment_conflicts(
                doctor_name, appointment_date, appointment_time, appointment_type
            )
            
            if conflict_check['has_conflict']:
                return {
                    'success': False,
                    'message': f"Appointment conflict: {conflict_check['message']}",
                    'suggested_times': conflict_check.get('suggested_times', []),
                    'appointment_id': None
                }
            
            # Create appointment record
            appointment_data = {
                'patient_name': patient_name,
                'doctor_name': doctor_name,
                'appointment_date': appointment_date,
                'appointment_time': appointment_time,
                'appointment_type': appointment_type,
                'duration_minutes': self.appointment_types.get(appointment_type, 30),
                'symptoms': symptoms,
                'notes': notes,
                'status': 'scheduled',
                'created_at': datetime.now().isoformat(),
                'confirmation_code': self._generate_confirmation_code()
            }
            
            # Save to database
            appointment_id = self._save_appointment(appointment_data)
            
            if appointment_id:
                # Generate confirmation details
                confirmation = self._generate_confirmation(appointment_data, appointment_id)
                
                logger.info(f"Appointment booked successfully: ID {appointment_id}")
                return {
                    'success': True,
                    'message': 'Appointment booked successfully',
                    'appointment_id': appointment_id,
                    'confirmation': confirmation
                }
            else:
                return {
                    'success': False,
                    'message': 'Failed to save appointment to database',
                    'appointment_id': None
                }
                
        except Exception as e:
            logger.error(f"Error booking appointment: {str(e)}")
            return {
                'success': False,
                'message': f'Booking failed: {str(e)}',
                'appointment_id': None
            }

    def _validate_appointment_data(self, patient_name: str, doctor_name: str,
                                  appointment_date: str, appointment_time: str,
                                  appointment_type: str) -> Dict[str, Any]:
        """Validate appointment booking data"""
        try:
            # Check required fields
            if not all([patient_name, doctor_name, appointment_date, appointment_time]):
                return {
                    'valid': False,
                    'message': 'All required fields must be provided'
                }
            
            # Validate date format and future date
            try:
                date_obj = datetime.strptime(appointment_date, '%Y-%m-%d').date()
                if date_obj < datetime.now().date():
                    return {
                        'valid': False,
                        'message': 'Appointment date must be in the future'
                    }
                
                # Check if date is too far in future (max 3 months)
                max_date = datetime.now().date() + timedelta(days=90)
                if date_obj > max_date:
                    return {
                        'valid': False,
                        'message': 'Appointment date cannot be more than 3 months in advance'
                    }
                    
            except ValueError:
                return {
                    'valid': False,
                    'message': 'Invalid date format. Use YYYY-MM-DD'
                }
            
            # Validate time format and working hours
            try:
                time_obj = datetime.strptime(appointment_time, '%H:%M').time()
                if not self._is_valid_appointment_time(time_obj):
                    return {
                        'valid': False,
                        'message': f'Appointment time must be between {self.working_hours["start_time"]} and {self.working_hours["end_time"]}, excluding lunch hour'
                    }
            except ValueError:
                return {
                    'valid': False,
                    'message': 'Invalid time format. Use HH:MM (24-hour format)'
                }
            
            # Validate appointment type
            if appointment_type not in self.appointment_types:
                return {
                    'valid': False,
                    'message': f'Invalid appointment type. Available types: {list(self.appointment_types.keys())}'
                }
            
            # Validate weekend (assuming no weekend appointments)
            if date_obj.weekday() >= 5:  # Saturday = 5, Sunday = 6
                return {
                    'valid': False,
                    'message': 'Weekend appointments are not available'
                }
            
            return {'valid': True, 'message': 'Validation successful'}
            
        except Exception as e:
            return {
                'valid': False,
                'message': f'Validation error: {str(e)}'
            }

    def _is_valid_appointment_time(self, appointment_time: time) -> bool:
        """Check if appointment time is within working hours"""
        # Check if within working hours
        if not (self.working_hours['start_time'] <= appointment_time < self.working_hours['end_time']):
            return False
        
        # Check if not during lunch hour
        if self.working_hours['lunch_start'] <= appointment_time < self.working_hours['lunch_end']:
            return False
        
        # Check if time aligns with available slots
        return appointment_time in self.daily_slots

    def _check_appointment_conflicts(self, doctor_name: str, appointment_date: str,
                                   appointment_time: str, appointment_type: str) -> Dict[str, Any]:
        """Check for appointment conflicts and suggest alternatives"""
        try:
            # Get existing appointments for the doctor on the same date
            existing_appointments = self._get_doctor_appointments(doctor_name, appointment_date)
            
            # Parse requested time
            requested_time = datetime.strptime(appointment_time, '%H:%M').time()
            requested_duration = self.appointment_types.get(appointment_type, 30)
            
            # Check for conflicts
            for appointment in existing_appointments:
                existing_time = datetime.strptime(appointment['appointment_time'], '%H:%M').time()
                existing_duration = appointment.get('duration_minutes', 30)
                
                # Calculate time ranges
                requested_start = datetime.combine(datetime.today(), requested_time)
                requested_end = requested_start + timedelta(minutes=requested_duration)
                
                existing_start = datetime.combine(datetime.today(), existing_time)
                existing_end = existing_start + timedelta(minutes=existing_duration)
                
                # Check for overlap
                if (requested_start < existing_end and requested_end > existing_start):
                    # Conflict found, suggest alternative times
                    suggested_times = self._suggest_alternative_times(
                        doctor_name, appointment_date, requested_duration
                    )
                    
                    return {
                        'has_conflict': True,
                        'message': f'Time slot conflicts with existing appointment at {existing_time}',
                        'suggested_times': suggested_times
                    }
            
            return {'has_conflict': False, 'message': 'No conflicts found'}
            
        except Exception as e:
            logger.error(f"Error checking conflicts: {str(e)}")
            return {
                'has_conflict': True,
                'message': f'Error checking availability: {str(e)}'
            }

    def _get_doctor_appointments(self, doctor_name: str, appointment_date: str) -> List[Dict[str, Any]]:
        """Get existing appointments for a doctor on a specific date"""
        try:
            if self.db_manager:
                return self.db_manager.get_appointments_by_doctor_date(doctor_name, appointment_date)
            else:
                # Return empty list if no database manager
                logger.warning("No database manager available, assuming no conflicts")
                return []
        except Exception as e:
            logger.error(f"Error fetching doctor appointments: {str(e)}")
            return []

    def _suggest_alternative_times(self, doctor_name: str, appointment_date: str,
                                  duration_minutes: int) -> List[str]:
        """Suggest alternative appointment times"""
        try:
            existing_appointments = self._get_doctor_appointments(doctor_name, appointment_date)
            occupied_slots = set()
            
            # Mark occupied time slots
            for appointment in existing_appointments:
                start_time = datetime.strptime(appointment['appointment_time'], '%H:%M').time()
                duration = appointment.get('duration_minutes', 30)
                
                # Mark all slots occupied by this appointment
                current_slot = datetime.combine(datetime.today(), start_time)
                end_slot = current_slot + timedelta(minutes=duration)
                
                while current_slot < end_slot:
                    occupied_slots.add(current_slot.time())
                    current_slot += timedelta(minutes=self.appointment_duration)
            
            # Find available slots
            available_times = []
            for slot in self.daily_slots:
                # Check if this slot and required duration are available
                slot_datetime = datetime.combine(datetime.today(), slot)
                required_end = slot_datetime + timedelta(minutes=duration_minutes)
                
                # Check if all required slots are free
                is_available = True
                check_slot = slot_datetime
                while check_slot < required_end:
                    if check_slot.time() in occupied_slots:
                        is_available = False
                        break
                    check_slot += timedelta(minutes=self.appointment_duration)
                
                if is_available:
                    available_times.append(slot.strftime('%H:%M'))
                
                # Limit suggestions to 5
                if len(available_times) >= 5:
                    break
            
            return available_times
            
        except Exception as e:
            logger.error(f"Error suggesting alternative times: {str(e)}")
            return []

    def _save_appointment(self, appointment_data: Dict[str, Any]) -> Optional[int]:
        """Save appointment to database"""
        try:
            if self.db_manager:
                # Ensure user session exists
                user_session = appointment_data.get('user_session', 'default')
                self.db_manager.create_user(user_session)
                return self.db_manager.create_appointment(appointment_data)
            else:
                # Simulate saving without database
                logger.warning("No database manager available, simulating appointment save")
                return 12345  # Simulated appointment ID
        except Exception as e:
            logger.error(f"Error saving appointment: {str(e)}")
            return None

    def _generate_confirmation_code(self) -> str:
        """Generate unique confirmation code for appointment"""
        import random
        import string
        return ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))

    def _generate_confirmation(self, appointment_data: Dict[str, Any], 
                             appointment_id: int) -> Dict[str, Any]:
        """Generate appointment confirmation details"""
        return {
            'appointment_id': appointment_id,
            'confirmation_code': appointment_data['confirmation_code'],
            'patient_name': appointment_data['patient_name'],
            'doctor_name': appointment_data['doctor_name'],
            'appointment_datetime': f"{appointment_data['appointment_date']} {appointment_data['appointment_time']}",
            'appointment_type': appointment_data['appointment_type'],
            'duration': f"{appointment_data['duration_minutes']} minutes",
            'status': appointment_data['status'],
            'instructions': self._generate_appointment_instructions(appointment_data),
            'contact_info': 'For changes or cancellations, call +1-800-HEALTH',
            'reminder': 'Please arrive 15 minutes early for your appointment'
        }

    def _generate_appointment_instructions(self, appointment_data: Dict[str, Any]) -> List[str]:
        """Generate appointment-specific instructions"""
        instructions = [
            "Bring a valid ID and insurance card",
            "Arrive 15 minutes before your scheduled time"
        ]
        
        appointment_type = appointment_data['appointment_type']
        
        if appointment_type == 'routine_checkup':
            instructions.extend([
                "Fast for 8-12 hours if blood work is required",
                "Bring list of current medications"
            ])
        elif appointment_type == 'specialist_consultation':
            instructions.extend([
                "Bring any relevant medical records",
                "Prepare list of questions for the specialist"
            ])
        elif appointment_type == 'follow_up':
            instructions.append("Bring previous test results or reports")
        
        return instructions

    def get_available_slots(self, doctor_name: str, date: str) -> List[Dict[str, Any]]:
        """Get available appointment slots for a doctor on a specific date"""
        try:
            existing_appointments = self._get_doctor_appointments(doctor_name, date)
            occupied_slots = set()
            
            # Mark occupied slots
            for appointment in existing_appointments:
                start_time = datetime.strptime(appointment['appointment_time'], '%H:%M').time()
                duration = appointment.get('duration_minutes', 30)
                
                current_slot = datetime.combine(datetime.today(), start_time)
                end_slot = current_slot + timedelta(minutes=duration)
                
                while current_slot < end_slot:
                    occupied_slots.add(current_slot.time())
                    current_slot += timedelta(minutes=self.appointment_duration)
            
            # Generate available slots
            available_slots = []
            for slot in self.daily_slots:
                if slot not in occupied_slots:
                    available_slots.append({
                        'time': slot.strftime('%H:%M'),
                        'display_time': slot.strftime('%I:%M %p'),
                        'available': True
                    })
                else:
                    available_slots.append({
                        'time': slot.strftime('%H:%M'),
                        'display_time': slot.strftime('%I:%M %p'),
                        'available': False
                    })
            
            return available_slots
            
        except Exception as e:
            logger.error(f"Error getting available slots: {str(e)}")
            return []

    def cancel_appointment(self, appointment_id: int, reason: str = '') -> Dict[str, Any]:
        """Cancel an existing appointment"""
        try:
            if self.db_manager:
                success = self.db_manager.cancel_appointment(appointment_id, reason)
                if success:
                    return {
                        'success': True,
                        'message': 'Appointment cancelled successfully',
                        'appointment_id': appointment_id
                    }
                else:
                    return {
                        'success': False,
                        'message': 'Failed to cancel appointment',
                        'appointment_id': appointment_id
                    }
            else:
                # Simulate cancellation
                return {
                    'success': True,
                    'message': 'Appointment cancelled successfully (simulated)',
                    'appointment_id': appointment_id
                }
                
        except Exception as e:
            logger.error(f"Error cancelling appointment: {str(e)}")
            return {
                'success': False,
                'message': f'Cancellation failed: {str(e)}',
                'appointment_id': appointment_id
            }

    def get_patient_appointments(self, patient_name: str) -> List[Dict[str, Any]]:
        """Get all appointments for a patient"""
        try:
            if self.db_manager:
                return self.db_manager.get_appointments_by_patient(patient_name)
            else:
                # Return empty list if no database
                return []
        except Exception as e:
            logger.error(f"Error getting patient appointments: {str(e)}")
            return []

    def get_appointment_summary(self) -> Dict[str, Any]:
        """Get summary of appointment system status"""
        try:
            summary = {
                'working_hours': {
                    'start': self.working_hours['start_time'].strftime('%H:%M'),
                    'end': self.working_hours['end_time'].strftime('%H:%M'),
                    'lunch_break': f"{self.working_hours['lunch_start'].strftime('%H:%M')} - {self.working_hours['lunch_end'].strftime('%H:%M')}"
                },
                'appointment_types': list(self.appointment_types.keys()),
                'default_duration': f"{self.appointment_duration} minutes",
                'daily_slots_count': len(self.daily_slots),
                'booking_window': '3 months in advance',
                'weekend_availability': False
            }
            
            if self.db_manager:
                # Add database statistics if available
                today = datetime.now().date().isoformat()
                total_appointments = len(self.db_manager.get_all_appointments())
                today_appointments = len(self.db_manager.get_appointments_by_date(today))
                
                summary.update({
                    'total_appointments': total_appointments,
                    'today_appointments': today_appointments
                })
            
            return summary
            
        except Exception as e:
            logger.error(f"Error generating appointment summary: {str(e)}")
            return {'error': str(e)}


# Factory function for dependency injection
def get_appointment_manager() -> AppointmentManager:
    """Factory function to create and return AppointmentManager instance"""
    return AppointmentManager()


# Example usage and testing
if __name__ == "__main__":
    # Initialize appointment manager
    manager = get_appointment_manager()
    
    print("=== Appointment Manager Test ===")
    
    # Test appointment booking
    print("\n--- Testing Appointment Booking ---")
    
    # Test valid appointment (using future date)
    from datetime import datetime, timedelta
    future_date = (datetime.now() + timedelta(days=7)).strftime('%Y-%m-%d')
    
    result = manager.book_appointment(
        patient_name="John Doe",
        doctor_name="Dr. Sarah Johnson",
        appointment_date=future_date,
        appointment_time="10:00",
        appointment_type="consultation",
        symptoms="Regular checkup",
        notes="First visit"
    )
    
    print(f"Booking result: {result['success']}")
    print(f"Message: {result['message']}")
    if result['success']:
        print(f"Appointment ID: {result['appointment_id']}")
        print(f"Confirmation Code: {result['confirmation']['confirmation_code']}")
    
    # Test conflict detection
    print("\n--- Testing Conflict Detection ---")
    conflict_result = manager.book_appointment(
        patient_name="Jane Smith",
        doctor_name="Dr. Sarah Johnson",
        appointment_date=future_date,
        appointment_time="10:00",  # Same time as above
        appointment_type="consultation"
    )
    
    print(f"Conflict booking result: {conflict_result['success']}")
    print(f"Message: {conflict_result['message']}")
    if 'suggested_times' in conflict_result:
        print(f"Suggested times: {conflict_result['suggested_times']}")
    
    # Test available slots
    print("\n--- Testing Available Slots ---")
    tomorrow_date = (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d')
    slots = manager.get_available_slots("Dr. Sarah Johnson", tomorrow_date)
    available_count = sum(1 for slot in slots if slot['available'])
    print(f"Available slots for tomorrow: {available_count}/{len(slots)}")
    
    # Test appointment summary
    print("\n--- Appointment System Summary ---")
    summary = manager.get_appointment_summary()
    print(f"Working hours: {summary['working_hours']['start']} - {summary['working_hours']['end']}")
    print(f"Daily slots: {summary['daily_slots_count']}")
    print(f"Appointment types: {summary['appointment_types']}")
    
    print("\nAppointment Manager test completed!")