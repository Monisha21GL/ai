"""
Simple Health Chatbot - Fallback Implementation

A minimal chatbot implementation for health guidance.
"""

import random
from datetime import datetime
from typing import Dict, Any, List

class SimpleChatbot:
    """Simple rule-based health chatbot"""
    
    def __init__(self):
        self.responses = {
            'greeting': [
                "Hello! I'm your AI Health Assistant. How can I help you today?",
                "Hi there! I'm here to provide basic health guidance. What would you like to know?",
                "Good day! I'm your virtual health companion. How may I assist you?"
            ],
            'symptoms': [
                "For symptoms, I recommend using our symptom checker tool for AI-powered analysis.",
                "Our symptom checker can help analyze your symptoms. Would you like me to guide you there?",
                "I can help with general health information. For specific symptoms, try our symptom checker."
            ],
            'emergency': [
                "🚨 If this is a medical emergency, please call emergency services immediately!",
                "⚠️ For emergency symptoms, seek immediate medical attention. Call emergency services right away.",
                "🏥 Emergency situations require immediate professional medical care."
            ],
            'appointments': [
                "I can help you with appointment booking! Use our appointment booking feature.",
                "To book an appointment, use our appointment booking system.",
                "Our appointment booking feature makes it easy to schedule visits with healthcare providers."
            ],
            'default': [
                "I'm here to help with general health information and guide you to our healthcare features.",
                "I can provide general health guidance. What would you like to know?",
                "I'm your AI health assistant! How can I help you today?"
            ]
        }
        
    def get_response(self, user_input: str) -> Dict[str, Any]:
        """Get chatbot response"""
        user_input_lower = user_input.lower()
        
        # Simple pattern matching
        if any(word in user_input_lower for word in ['hello', 'hi', 'hey']):
            category = 'greeting'
        elif any(word in user_input_lower for word in ['symptom', 'pain', 'hurt', 'sick']):
            category = 'symptoms'
        elif any(word in user_input_lower for word in ['emergency', 'urgent', 'chest pain']):
            category = 'emergency'
        elif any(word in user_input_lower for word in ['appointment', 'book', 'doctor']):
            category = 'appointments'
        else:
            category = 'default'
            
        response_text = random.choice(self.responses[category])
        
        return {
            'success': True,
            'response': response_text,
            'category': category,
            'timestamp': datetime.now().isoformat()
        }
    
    def get_suggested_actions(self, category: str) -> List[Dict[str, str]]:
        """Get suggested actions"""
        suggestions = {
            'symptoms': [
                {'text': 'Use Symptom Checker', 'action': 'symptom_checker'},
                {'text': 'Check for Emergency', 'action': 'emergency_check'}
            ],
            'emergency': [
                {'text': 'Find Nearest Hospital', 'action': 'find_hospital'}
            ],
            'appointments': [
                {'text': 'Book Appointment', 'action': 'book_appointment'}
            ]
        }
        return suggestions.get(category, [])
    
    def get_conversation_history(self) -> List[Dict[str, Any]]:
        """Get conversation history"""
        return []
    
    def clear_conversation(self) -> None:
        """Clear conversation history"""
        pass

def get_health_chatbot():
    """Get simple chatbot instance"""
    return SimpleChatbot()