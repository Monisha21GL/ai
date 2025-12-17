"""
AI Healthcare Assistant - Health Guidance Chatbot

This module provides a simple rule-based chatbot for basic health guidance
and information. It uses pattern matching and predefined responses.

Author: AI Healthcare Assistant Team
Date: 2024
Purpose: Academic project for healthcare AI demonstration
"""

import re
import json
import random
import logging
from typing import List, Dict, Any, Optional, Tuple
from datetime import datetime

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class HealthChatbot:
    """
    Simple rule-based chatbot for health guidance and information
    """
    
    def __init__(self):
        """Initialize the health chatbot"""
        self.patterns = self._load_response_patterns()
        self.conversation_history = []
        self.user_context = {}
        
    def _load_response_patterns(self) -> List[Dict[str, Any]]:
        """Load response patterns for the chatbot"""
        return [
            # Greetings
            {
                'patterns': [r'\b(hello|hi|hey|good morning|good afternoon|good evening)\b'],
                'responses': [
                    "Hello! I'm your AI Health Assistant. How can I help you with your health questions today?",
                    "Hi there! I'm here to provide basic health guidance. What would you like to know?",
                    "Good day! I'm your virtual health companion. How may I assist you?"
                ],
                'category': 'greeting',
                'priority': 1
            },
            
            # Symptoms inquiry
            {
                'patterns': [r'\b(symptom|symptoms|feel|feeling|pain|hurt|ache|sick|ill)\b'],
                'responses': [
                    "I understand you're experiencing symptoms. While I can provide general information, it's important to consult with a healthcare professional for proper diagnosis. Would you like to use our symptom checker?",
                    "Symptoms can be concerning. For accurate assessment, I recommend using our AI-powered symptom checker or consulting with a doctor. Can I help you navigate to the symptom checker?",
                    "I'm here to help with general health information. For specific symptoms, our symptom checker tool can provide AI-powered analysis. Would you like me to guide you there?"
                ],
                'category': 'symptoms',
                'priority': 2,
                'action': 'suggest_symptom_checker'
            },
            
            # Emergency situations
            {
                'patterns': [r'\b(emergency|urgent|chest pain|can\'t breathe|breathing|heart attack|stroke|severe|critical)\b'],
                'responses': [
                    "🚨 If this is a medical emergency, please call emergency services immediately (911 in the US) or go to the nearest emergency room. Don't wait for online advice in emergency situations.",
                    "⚠️ For any emergency symptoms like chest pain, difficulty breathing, or severe injuries, seek immediate medical attention. Call emergency services right away.",
                    "🏥 Emergency situations require immediate professional medical care. Please contact emergency services or visit the nearest hospital emergency department immediately."
                ],
                'category': 'emergency',
                'priority': 10,
                'action': 'emergency_protocol'
            },
            
            # Medication questions
            {
                'patterns': [r'\b(medication|medicine|drug|pill|prescription|dosage|side effect)\b'],
                'responses': [
                    "For medication questions, it's crucial to consult with your doctor or pharmacist. They can provide accurate information about dosages, interactions, and side effects specific to your situation.",
                    "Medication advice should always come from qualified healthcare professionals. Please contact your doctor, pharmacist, or healthcare provider for medication-related questions.",
                    "I cannot provide specific medication advice. For safety, please consult with your healthcare provider or pharmacist about any medication concerns."
                ],
                'category': 'medication',
                'priority': 5
            },
            
            # General health questions
            {
                'patterns': [r'\b(healthy|health|wellness|fitness|diet|nutrition|exercise)\b'],
                'responses': [
                    "Great question about health! I can provide general wellness information. For specific health advice, our symptom checker and doctor recommendations are great resources.",
                    "Health and wellness are important topics. I can share general information, but for personalized advice, consider using our health assessment tools.",
                    "I'm happy to discuss general health topics. For specific concerns, our AI-powered symptom checker can provide more detailed analysis."
                ],
                'category': 'general_health',
                'priority': 3
            },
            
            # Appointment questions
            {
                'patterns': [r'\b(appointment|book|schedule|doctor|visit|consultation)\b'],
                'responses': [
                    "I can help you with appointment booking! You can use our appointment booking feature to schedule consultations with recommended doctors.",
                    "To book an appointment, use our appointment booking system. It will help you find available doctors and schedule consultations.",
                    "Our appointment booking feature makes it easy to schedule visits with healthcare providers. Would you like me to guide you there?"
                ],
                'category': 'appointments',
                'priority': 4,
                'action': 'suggest_appointment_booking'
            },
            
            # Location and GPS questions
            {
                'patterns': [r'\b(location|gps|hospital|nearby|near me|ambulance|emergency room)\b'],
                'responses': [
                    "I can help you find nearby medical facilities! Use our GPS location feature to find hospitals and emergency services in your area.",
                    "Our GPS tracking feature can locate nearby hospitals and medical facilities. It's especially useful in emergency situations.",
                    "To find nearby medical facilities, try our location services feature. It will show you hospitals and emergency services in your area."
                ],
                'category': 'location',
                'priority': 6,
                'action': 'suggest_location_services'
            },
            
            # Goodbye/farewell
            {
                'patterns': [r'\b(bye|goodbye|thanks|thank you|see you|farewell)\b'],
                'responses': [
                    "Thank you for using AI Healthcare Assistant! Remember, this is for informational purposes only. Always consult healthcare professionals for medical advice.",
                    "Goodbye! Stay healthy and don't hesitate to return if you need health information. Take care!",
                    "Thanks for chatting! Remember to consult with healthcare professionals for any serious health concerns. Have a great day!"
                ],
                'category': 'farewell',
                'priority': 1
            },
            
            # Default/fallback responses
            {
                'patterns': [r'.*'],  # Matches anything
                'responses': [
                    "I'm here to help with general health information. You can ask me about symptoms, appointments, or use our health assessment tools.",
                    "I can provide general health guidance and help you navigate our healthcare features. What would you like to know?",
                    "I'm your AI health assistant! I can help with general health questions or guide you to our symptom checker and appointment booking features."
                ],
                'category': 'default',
                'priority': 0
            }
        ]
    
    def get_response(self, user_input: str) -> Dict[str, Any]:
        """
        Get chatbot response for user input
        
        Args:
            user_input: User's message/question
            
        Returns:
            Dictionary containing response and metadata
        """
        try:
            user_input_lower = user_input.lower().strip()
            
            # Store conversation
            self.conversation_history.append({
                'user': user_input,
                'timestamp': datetime.now().isoformat()
            })
            
            # Find matching patterns
            matches = []
            for pattern_group in self.patterns:
                for pattern in pattern_group['patterns']:
                    if re.search(pattern, user_input_lower):
                        matches.append(pattern_group)
                        break
            
            # Sort matches by priority (higher priority first)
            matches.sort(key=lambda x: x['priority'], reverse=True)
            
            # Select response from highest priority match
            if matches:
                selected_pattern = matches[0]
                response_text = self._select_response(selected_pattern['responses'])
                
                response = {
                    'success': True,
                    'response': response_text,
                    'category': selected_pattern['category'],
                    'priority': selected_pattern['priority'],
                    'action': selected_pattern.get('action'),
                    'timestamp': datetime.now().isoformat()
                }
            else:
                # Fallback to default response
                default_responses = [
                    "I'm here to help with health-related questions. Could you please rephrase your question?",
                    "I can assist with general health information. What specific health topic would you like to discuss?",
                    "I'm your AI health assistant. Feel free to ask about symptoms, health tips, or our healthcare features."
                ]
                response = {
                    'success': True,
                    'response': self._select_response(default_responses),
                    'category': 'default',
                    'priority': 0,
                    'action': None,
                    'timestamp': datetime.now().isoformat()
                }
            
            # Store bot response
            self.conversation_history.append({
                'bot': response['response'],
                'category': response['category'],
                'timestamp': response['timestamp']
            })
            
            return response
            
        except Exception as e:
            logger.error(f"Chatbot response error: {e}")
            return {
                'success': False,
                'response': "I'm sorry, I'm having trouble processing your request. Please try again or contact a healthcare professional if you have urgent concerns.",
                'category': 'error',
                'priority': 0,
                'action': None,
                'timestamp': datetime.now().isoformat(),
                'error': str(e)
            }
    
    def _select_response(self, responses: List[str]) -> str:
        """Select a random response from the list"""
        return random.choice(responses)
    
    def get_conversation_history(self) -> List[Dict[str, Any]]:
        """Get conversation history"""
        return self.conversation_history.copy()
    
    def clear_conversation(self) -> None:
        """Clear conversation history"""
        self.conversation_history.clear()
        self.user_context.clear()
    
    def set_user_context(self, context: Dict[str, Any]) -> None:
        """Set user context for personalized responses"""
        self.user_context.update(context)
    
    def get_suggested_actions(self, category: str) -> List[Dict[str, str]]:
        """Get suggested actions based on conversation category"""
        suggestions = {
            'symptoms': [
                {'text': 'Use Symptom Checker', 'action': 'symptom_checker'},
                {'text': 'Check for Emergency', 'action': 'emergency_check'}
            ],
            'emergency': [
                {'text': 'Call Emergency Services', 'action': 'call_emergency'},
                {'text': 'Find Nearest Hospital', 'action': 'find_hospital'}
            ],
            'appointments': [
                {'text': 'Book Appointment', 'action': 'book_appointment'},
                {'text': 'View My Appointments', 'action': 'view_appointments'}
            ],
            'location': [
                {'text': 'Find Nearby Hospitals', 'action': 'find_hospitals'},
                {'text': 'Get GPS Location', 'action': 'get_location'}
            ],
            'general_health': [
                {'text': 'Get Health Tips', 'action': 'health_tips'},
                {'text': 'View Medical History', 'action': 'medical_history'}
            ]
        }
        
        return suggestions.get(category, [])


# Global chatbot instance
health_chatbot = None

def get_health_chatbot() -> HealthChatbot:
    """
    Get global health chatbot instance (singleton pattern)
    
    Returns:
        HealthChatbot instance
    """
    global health_chatbot
    if health_chatbot is None:
        health_chatbot = HealthChatbot()
    return health_chatbot


if __name__ == "__main__":
    # Test the health chatbot
    print("Testing Health Chatbot...")
    
    chatbot = HealthChatbot()
    
    # Test conversations
    test_inputs = [
        "Hello, I need help",
        "I have a headache and fever",
        "Is this an emergency?",
        "I want to book an appointment",
        "Where is the nearest hospital?",
        "Thank you for your help"
    ]
    
    for user_input in test_inputs:
        print(f"\nUser: {user_input}")
        response = chatbot.get_response(user_input)
        print(f"Bot: {response['response']}")
        print(f"Category: {response['category']}")
        
        # Show suggested actions
        suggestions = chatbot.get_suggested_actions(response['category'])
        if suggestions:
            print("Suggested actions:", [s['text'] for s in suggestions])
    
    print("\nHealth Chatbot test completed!")