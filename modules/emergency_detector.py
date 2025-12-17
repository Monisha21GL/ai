"""
AI Healthcare Assistant - Emergency Detection Module

This module implements emergency detection logic combining rule-based systems
with AI predictions to identify critical medical situations requiring immediate attention.

Author: AI Healthcare Assistant Team
Date: 2024
Purpose: Academic project for healthcare AI demonstration
"""

import json
import logging
from typing import List, Dict, Any, Tuple, Optional
from datetime import datetime

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class EmergencyDetector:
    """
    Emergency detection system combining rule-based logic with AI severity assessment
    """
    
    def __init__(self):
        """Initialize emergency detector with predefined rules and thresholds"""
        # Initialize database manager with error handling
        try:
            from modules.database_manager import get_db_manager
            self.db_manager = get_db_manager()
        except ImportError as e:
            logger.warning(f"Database manager not available: {e}")
            self.db_manager = None
        
        # Critical emergency symptoms that always trigger alerts
        self.critical_symptoms = {
            'chest_pain', 'chest pain', 'severe chest pain', 'crushing chest pain',
            'shortness_of_breath', 'shortness of breath', 'difficulty breathing', 'difficulty_breathing',
            'severe_headache', 'severe headache', 'worst headache ever',
            'unconsciousness', 'loss of consciousness', 'fainting', 'syncope',
            'seizures', 'seizure', 'convulsions',
            'severe_bleeding', 'severe bleeding', 'heavy bleeding', 'hemorrhage',
            'anaphylaxis', 'severe allergic reaction', 'allergic_reaction',
            'stroke_symptoms', 'stroke symptoms', 'facial drooping', 'slurred speech',
            'severe_abdominal_pain', 'severe abdominal pain', 'acute abdomen',
            'high_fever', 'very high fever', 'fever over 104',
            'neck_stiffness', 'neck stiffness', 'stiff neck',
            'confusion', 'altered mental state', 'disorientation',
            'severe_dehydration', 'severe dehydration',
            'rapid_heartbeat', 'rapid heart rate', 'palpitations',
            'cold_sweat', 'profuse sweating', 'diaphoresis'
        }
        
        # Emergency disease patterns
        self.emergency_diseases = {
            'heart attack', 'myocardial infarction', 'cardiac arrest',
            'stroke', 'cerebrovascular accident', 'tia',
            'meningitis', 'encephalitis',
            'appendicitis', 'acute appendicitis',
            'anaphylaxis', 'anaphylactic shock',
            'sepsis', 'septic shock',
            'pulmonary embolism', 'pe',
            'pneumothorax', 'collapsed lung',
            'diabetic ketoacidosis', 'dka',
            'severe asthma', 'status asthmaticus',
            'acute pancreatitis',
            'ectopic pregnancy',
            'aortic dissection',
            'severe trauma', 'major trauma'
        }
        
        # Symptom combinations that indicate emergencies
        self.emergency_combinations = [
            # Heart attack indicators
            {'chest_pain', 'shortness_of_breath', 'nausea'},
            {'chest_pain', 'arm_pain', 'sweating'},
            {'chest_pain', 'jaw_pain', 'dizziness'},
            
            # Stroke indicators
            {'severe_headache', 'confusion', 'weakness'},
            {'facial_drooping', 'slurred_speech', 'arm_weakness'},
            {'sudden_weakness', 'speech_problems', 'vision_problems'},
            
            # Meningitis indicators
            {'severe_headache', 'neck_stiffness', 'fever'},
            {'headache', 'neck_stiffness', 'light_sensitivity'},
            
            # Sepsis indicators
            {'fever', 'rapid_heartbeat', 'confusion'},
            {'high_fever', 'low_blood_pressure', 'rapid_breathing'},
            
            # Anaphylaxis indicators
            {'difficulty_breathing', 'swelling', 'rash'},
            {'severe_allergic_reaction', 'shortness_of_breath', 'hives'},
            
            # Appendicitis indicators
            {'severe_abdominal_pain', 'nausea', 'fever'},
            {'right_lower_quadrant_pain', 'vomiting', 'tenderness'}
        ]
        
        # Severity thresholds for AI predictions
        self.severity_thresholds = {
            'high': 0.8,      # High confidence emergency
            'medium': 0.6,    # Moderate concern
            'low': 0.4        # Low risk
        }
        
        # Emergency contact information
        self.emergency_contacts = {
            'ambulance': '911',
            'poison_control': '1-800-222-1222',
            'emergency_hotline': '1-800-EMERGENCY',
            'local_hospital': '555-HOSPITAL'
        }

    def detect_emergency(self, symptoms: List[str], prediction_result: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Main emergency detection function combining rule-based and AI assessment
        
        Args:
            symptoms: List of user-reported symptoms
            prediction_result: Optional AI prediction result with disease and confidence
            
        Returns:
            Dictionary containing emergency status, severity, alerts, and recommendations
        """
        try:
            # Normalize symptoms for consistent matching
            normalized_symptoms = self._normalize_symptoms(symptoms)
            
            # Rule-based emergency detection
            rule_based_emergency = self._check_rule_based_emergency(normalized_symptoms)
            
            # AI-based severity assessment
            ai_emergency = self._assess_ai_emergency(prediction_result) if prediction_result else False
            
            # Combine assessments
            is_emergency = rule_based_emergency or ai_emergency
            
            # Determine severity level
            severity = self._calculate_severity(normalized_symptoms, prediction_result, is_emergency)
            
            # Generate emergency response
            emergency_response = self._generate_emergency_response(
                is_emergency, severity, normalized_symptoms, prediction_result
            )
            
            # Log emergency if detected
            if is_emergency:
                self._log_emergency(normalized_symptoms, emergency_response, prediction_result)
            
            return emergency_response
            
        except Exception as e:
            logger.error(f"Emergency detection failed: {str(e)}")
            # Return safe default response
            return {
                'success': False,
                'emergency': False,
                'is_emergency': False,
                'severity_level': 'unknown',
                'severity': 'unknown',
                'confidence': 0.0,
                'alerts': ['System error - please consult healthcare professional immediately'],
                'recommendations': ['Seek immediate medical attention'],
                'emergency_contacts': self.emergency_contacts,
                'error': str(e)
            }

    def _normalize_symptoms(self, symptoms: List[str]) -> set:
        """
        Normalize symptom strings for consistent matching
        
        Args:
            symptoms: Raw symptom strings from user input
            
        Returns:
            Set of normalized symptom strings
        """
        normalized = set()
        
        for symptom in symptoms:
            if not symptom:
                continue
                
            # Convert to lowercase and strip whitespace
            clean_symptom = symptom.lower().strip()
            
            # Replace common variations
            clean_symptom = clean_symptom.replace('_', ' ')
            clean_symptom = clean_symptom.replace('-', ' ')
            
            # Add both original and underscore versions for matching
            normalized.add(clean_symptom)
            normalized.add(clean_symptom.replace(' ', '_'))
            
        return normalized

    def _check_rule_based_emergency(self, symptoms: set) -> bool:
        """
        Check for emergency conditions using predefined rules
        
        Args:
            symptoms: Set of normalized symptoms
            
        Returns:
            Boolean indicating if emergency detected by rules
        """
        # Check for critical individual symptoms
        for symptom in symptoms:
            if symptom in self.critical_symptoms:
                logger.info(f"Critical symptom detected: {symptom}")
                return True
        
        # Check for emergency symptom combinations
        for combination in self.emergency_combinations:
            if combination.issubset(symptoms):
                logger.info(f"Emergency combination detected: {combination}")
                return True
        
        return False

    def _assess_ai_emergency(self, prediction_result: Dict[str, Any]) -> bool:
        """
        Assess emergency status based on AI prediction results
        
        Args:
            prediction_result: Dictionary containing disease prediction and confidence
            
        Returns:
            Boolean indicating if emergency detected by AI
        """
        if not prediction_result:
            return False
        
        predicted_disease = prediction_result.get('disease', '').lower()
        confidence = prediction_result.get('confidence', 0.0)
        severity = prediction_result.get('severity', '').lower()
        
        # Check if predicted disease is in emergency list
        for emergency_disease in self.emergency_diseases:
            if emergency_disease in predicted_disease:
                logger.info(f"Emergency disease predicted: {predicted_disease}")
                return True
        
        # Check high confidence + high severity combination
        if confidence >= self.severity_thresholds['high'] and severity == 'high':
            logger.info(f"High confidence + high severity: {confidence}, {severity}")
            return True
        
        return False

    def _calculate_severity(self, symptoms: set, prediction_result: Optional[Dict[str, Any]], 
                          is_emergency: bool) -> str:
        """
        Calculate overall severity level combining multiple factors
        
        Args:
            symptoms: Set of normalized symptoms
            prediction_result: AI prediction results
            is_emergency: Whether emergency was detected
            
        Returns:
            Severity level string (critical, high, medium, low)
        """
        if is_emergency:
            return 'critical'
        
        # Count critical symptoms
        critical_count = sum(1 for symptom in symptoms if symptom in self.critical_symptoms)
        
        # Get AI confidence if available
        ai_confidence = prediction_result.get('confidence', 0.0) if prediction_result else 0.0
        ai_severity = prediction_result.get('severity', '').lower() if prediction_result else ''
        
        # Calculate severity score
        severity_score = 0
        
        # Add points for critical symptoms
        severity_score += critical_count * 0.3
        
        # Add points for AI confidence
        severity_score += ai_confidence * 0.4
        
        # Add points for AI severity assessment
        if ai_severity == 'high':
            severity_score += 0.3
        elif ai_severity == 'medium':
            severity_score += 0.2
        elif ai_severity == 'low':
            severity_score += 0.1
        
        # Determine final severity
        if severity_score >= 0.8:
            return 'high'
        elif severity_score >= 0.5:
            return 'medium'
        else:
            return 'low'

    def _generate_emergency_response(self, is_emergency: bool, severity: str, 
                                   symptoms: set, prediction_result: Optional[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Generate comprehensive emergency response with alerts and recommendations
        
        Args:
            is_emergency: Whether emergency was detected
            severity: Calculated severity level
            symptoms: Set of normalized symptoms
            prediction_result: AI prediction results
            
        Returns:
            Complete emergency response dictionary
        """
        response = {
            'success': True,
            'emergency': is_emergency,
            'is_emergency': is_emergency,
            'severity_level': severity,
            'severity': severity,
            'confidence': self._calculate_confidence(symptoms, prediction_result),
            'alerts': [],
            'recommendations': [],
            'emergency_contacts': self.emergency_contacts,
            'ambulance_info': None,
            'timestamp': datetime.now().isoformat()
        }
        
        if is_emergency:
            # Critical emergency alerts
            response['alerts'].extend([
                '🚨 EMERGENCY DETECTED - SEEK IMMEDIATE MEDICAL ATTENTION',
                'Call 911 or go to the nearest emergency room immediately',
                'Do not delay - this could be a life-threatening condition'
            ])
            
            # Emergency recommendations
            response['recommendations'].extend([
                'Call emergency services (911) immediately',
                'If conscious, stay calm and follow dispatcher instructions',
                'Have someone drive you to the hospital - do not drive yourself',
                'Bring a list of current medications and medical history'
            ])
            
            # Simulate ambulance information
            response['ambulance_info'] = self._simulate_ambulance_response()
            
        elif severity == 'high':
            # High severity alerts
            response['alerts'].extend([
                '⚠️ HIGH PRIORITY - Seek medical attention soon',
                'Contact your doctor or visit urgent care within 24 hours',
                'Monitor symptoms closely for any worsening'
            ])
            
            response['recommendations'].extend([
                'Schedule appointment with healthcare provider today',
                'Consider visiting urgent care if symptoms worsen',
                'Keep track of symptom progression'
            ])
            
        elif severity == 'medium':
            # Medium severity alerts
            response['alerts'].extend([
                '📋 MODERATE CONCERN - Medical consultation recommended',
                'Schedule appointment with healthcare provider within 2-3 days'
            ])
            
            response['recommendations'].extend([
                'Contact your primary care physician',
                'Monitor symptoms and seek care if they worsen',
                'Consider over-the-counter remedies as appropriate'
            ])
            
        else:
            # Low severity
            response['alerts'].extend([
                '✓ LOW RISK - Monitor symptoms',
                'Consider self-care measures and monitor for changes'
            ])
            
            response['recommendations'].extend([
                'Rest and stay hydrated',
                'Monitor symptoms for 24-48 hours',
                'Contact healthcare provider if symptoms persist or worsen'
            ])
        
        return response

    def _calculate_confidence(self, symptoms: set, prediction_result: Optional[Dict[str, Any]]) -> float:
        """
        Calculate confidence level for emergency assessment
        
        Args:
            symptoms: Set of normalized symptoms
            prediction_result: AI prediction results
            
        Returns:
            Confidence score between 0.0 and 1.0
        """
        confidence_factors = []
        
        # Rule-based confidence
        critical_matches = sum(1 for symptom in symptoms if symptom in self.critical_symptoms)
        combination_matches = sum(1 for combo in self.emergency_combinations if combo.issubset(symptoms))
        
        rule_confidence = min(1.0, (critical_matches * 0.3 + combination_matches * 0.4))
        confidence_factors.append(rule_confidence)
        
        # AI confidence
        if prediction_result:
            ai_confidence = prediction_result.get('confidence', 0.0)
            confidence_factors.append(ai_confidence)
        
        # Return average confidence
        return sum(confidence_factors) / len(confidence_factors) if confidence_factors else 0.0

    def _simulate_ambulance_response(self) -> Dict[str, Any]:
        """
        Simulate ambulance dispatch and response information
        
        Returns:
            Dictionary with simulated ambulance information
        """
        return {
            'dispatch_time': datetime.now().isoformat(),
            'estimated_arrival': '8-12 minutes',
            'ambulance_id': 'AMB-001',
            'dispatcher_message': 'Ambulance dispatched to your location. Stay on the line.',
            'instructions': [
                'Stay calm and remain where you are',
                'Unlock doors for paramedic access',
                'Have identification and insurance ready',
                'List current medications if possible'
            ],
            'contact_number': self.emergency_contacts['ambulance']
        }

    def _log_emergency(self, symptoms: set, emergency_response: Dict[str, Any], 
                      prediction_result: Optional[Dict[str, Any]]) -> None:
        """
        Log emergency event to database for tracking and analysis
        
        Args:
            symptoms: Set of normalized symptoms
            emergency_response: Generated emergency response
            prediction_result: AI prediction results
        """
        try:
            # Use a default session ID for now (in real app, this would come from user session)
            user_session = "default_session"
            
            # Convert symptoms set to list for database storage
            symptoms_list = list(symptoms)
            
            # Extract emergency details
            emergency_type = emergency_response.get('severity', 'unknown')
            severity_level = emergency_response.get('severity', 'unknown')
            
            # Store in database using database manager (if available)
            if self.db_manager:
                emergency_id = self.db_manager.log_emergency(
                    user_session=user_session,
                    symptoms=symptoms_list,
                    emergency_type=emergency_type,
                    severity_level=severity_level,
                    ambulance_called=emergency_response.get('is_emergency', False)
                )
                
                if emergency_id:
                    logger.info(f"Emergency logged with ID: {emergency_id}, Type: {emergency_type}")
                else:
                    logger.warning("Failed to log emergency to database")
            else:
                logger.info(f"Emergency detected but not logged (no database): {emergency_type}")
            
        except Exception as e:
            logger.error(f"Failed to log emergency: {str(e)}")

    def get_emergency_history(self, user_session: str = None, limit: int = 10) -> List[Dict[str, Any]]:
        """
        Retrieve emergency history for analysis
        
        Args:
            user_session: Optional user session ID for filtering
            limit: Maximum number of records to return
            
        Returns:
            List of emergency log entries
        """
        try:
            if user_session is None:
                user_session = "default_session"
            
            if self.db_manager:
                return self.db_manager.get_user_emergency_logs(user_session)
            else:
                logger.warning("Database manager not available for emergency history")
                return []
        except Exception as e:
            logger.error(f"Failed to retrieve emergency history: {str(e)}")
            return []

    def update_emergency_rules(self, new_symptoms: List[str] = None, 
                             new_combinations: List[set] = None) -> bool:
        """
        Update emergency detection rules (for system maintenance)
        
        Args:
            new_symptoms: Additional critical symptoms to add
            new_combinations: Additional symptom combinations to monitor
            
        Returns:
            Boolean indicating success of update
        """
        try:
            if new_symptoms:
                self.critical_symptoms.update(new_symptoms)
                logger.info(f"Added {len(new_symptoms)} new critical symptoms")
            
            if new_combinations:
                self.emergency_combinations.extend(new_combinations)
                logger.info(f"Added {len(new_combinations)} new emergency combinations")
            
            return True
            
        except Exception as e:
            logger.error(f"Failed to update emergency rules: {str(e)}")
            return False

    def assess_with_prediction(self, symptoms: List[str], prediction_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Assess emergency status combining symptoms and prediction data
        
        Args:
            symptoms: List of symptoms
            prediction_data: Prediction result from ML engine
            
        Returns:
            Combined emergency assessment
        """
        return self.detect_emergency(symptoms, prediction_data)


# Factory function for dependency injection
def get_emergency_detector() -> EmergencyDetector:
    """
    Factory function to create and return EmergencyDetector instance
    
    Returns:
        Configured EmergencyDetector instance
    """
    return EmergencyDetector()


# Factory function for dependency injection
def get_emergency_detector() -> EmergencyDetector:
    """Factory function to create and return EmergencyDetector instance"""
    return EmergencyDetector()


# Example usage and testing
if __name__ == "__main__":
    # Initialize detector
    detector = get_emergency_detector()
    
    # Test emergency detection
    test_symptoms = ["chest pain", "shortness of breath", "nausea"]
    test_prediction = {
        "disease": "Heart Attack",
        "confidence": 0.9,
        "severity": "High"
    }
    
    result = detector.detect_emergency(test_symptoms, test_prediction)
    print("Emergency Detection Result:")
    print(json.dumps(result, indent=2))