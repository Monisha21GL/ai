"""
AI Healthcare Assistant - Health Tips Recommendation Engine

This module provides personalized health tips and recommendations based on
user's medical history, predictions, and health patterns.

Author: AI Healthcare Assistant Team
Date: 2024
Purpose: Academic project for healthcare AI demonstration
"""

import json
import logging
from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta
from collections import Counter

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class HealthTipsEngine:
    """
    Health tips recommendation engine that generates personalized advice
    based on user's medical history and health patterns
    """
    
    def __init__(self):
        """Initialize the health tips engine"""
        self.general_tips = self._load_general_tips()
        self.condition_specific_tips = self._load_condition_specific_tips()
        self.lifestyle_tips = self._load_lifestyle_tips()
        self.emergency_tips = self._load_emergency_tips()
    
    def _load_general_tips(self) -> List[Dict[str, Any]]:
        """Load general health tips"""
        return [
            {
                'id': 'general_001',
                'category': 'General Health',
                'icon': '🌟',
                'title': 'Balanced Nutrition',
                'content': 'Maintain a balanced diet rich in fruits, vegetables, whole grains, and lean proteins to support your immune system and overall health.',
                'priority': 'medium',
                'frequency': 'daily'
            },
            {
                'id': 'general_002',
                'category': 'Preventive Care',
                'icon': '🛡️',
                'title': 'Regular Check-ups',
                'content': 'Schedule regular check-ups with your healthcare provider to catch potential issues early and maintain optimal health.',
                'priority': 'high',
                'frequency': 'annual'
            },
            {
                'id': 'general_003',
                'category': 'Hydration',
                'icon': '💧',
                'title': 'Stay Hydrated',
                'content': 'Drink at least 8 glasses of water daily to maintain proper hydration and support bodily functions.',
                'priority': 'medium',
                'frequency': 'daily'
            },
            {
                'id': 'general_004',
                'category': 'Exercise',
                'icon': '🏃‍♂️',
                'title': 'Regular Physical Activity',
                'content': 'Aim for at least 150 minutes of moderate-intensity exercise per week to maintain cardiovascular health.',
                'priority': 'high',
                'frequency': 'weekly'
            },
            {
                'id': 'general_005',
                'category': 'Sleep Health',
                'icon': '😴',
                'title': 'Quality Sleep',
                'content': 'Maintain a consistent sleep schedule and aim for 7-9 hours of quality sleep per night for optimal recovery.',
                'priority': 'high',
                'frequency': 'daily'
            },
            {
                'id': 'general_006',
                'category': 'Mental Health',
                'icon': '🧘‍♀️',
                'title': 'Stress Management',
                'content': 'Practice stress management techniques like deep breathing, meditation, or yoga to maintain mental well-being.',
                'priority': 'medium',
                'frequency': 'daily'
            },
            {
                'id': 'general_007',
                'category': 'Hygiene',
                'icon': '🧼',
                'title': 'Hand Hygiene',
                'content': 'Wash your hands frequently with soap and water for at least 20 seconds to prevent infections.',
                'priority': 'high',
                'frequency': 'daily'
            }
        ]
    
    def _load_condition_specific_tips(self) -> Dict[str, List[Dict[str, Any]]]:
        """Load condition-specific health tips"""
        return {
            'common cold': [
                {
                    'id': 'cold_001',
                    'category': 'Cold Management',
                    'icon': '🤧',
                    'title': 'Rest and Recovery',
                    'content': 'Get plenty of rest and stay hydrated. Consider warm liquids like tea or soup to soothe symptoms.',
                    'priority': 'high'
                },
                {
                    'id': 'cold_002',
                    'category': 'Prevention',
                    'icon': '🛡️',
                    'title': 'Boost Immunity',
                    'content': 'Increase vitamin C intake through citrus fruits and consider zinc supplements to support immune function.',
                    'priority': 'medium'
                }
            ],
            'flu': [
                {
                    'id': 'flu_001',
                    'category': 'Flu Management',
                    'icon': '🤒',
                    'title': 'Antiviral Treatment',
                    'content': 'Consult your doctor about antiviral medications if symptoms started within 48 hours.',
                    'priority': 'high'
                },
                {
                    'id': 'flu_002',
                    'category': 'Prevention',
                    'icon': '💉',
                    'title': 'Annual Vaccination',
                    'content': 'Get an annual flu vaccine to reduce your risk of contracting influenza.',
                    'priority': 'high'
                }
            ],
            'headache': [
                {
                    'id': 'headache_001',
                    'category': 'Headache Relief',
                    'icon': '🧠',
                    'title': 'Hydration and Rest',
                    'content': 'Ensure adequate hydration and rest in a quiet, dark room. Consider gentle neck stretches.',
                    'priority': 'medium'
                },
                {
                    'id': 'headache_002',
                    'category': 'Prevention',
                    'icon': '📱',
                    'title': 'Screen Time Management',
                    'content': 'Take regular breaks from screens and maintain good posture to prevent tension headaches.',
                    'priority': 'medium'
                }
            ],
            'hypertension': [
                {
                    'id': 'hyper_001',
                    'category': 'Blood Pressure Management',
                    'icon': '❤️',
                    'title': 'DASH Diet',
                    'content': 'Follow a DASH diet rich in fruits, vegetables, and low-fat dairy while reducing sodium intake.',
                    'priority': 'high'
                },
                {
                    'id': 'hyper_002',
                    'category': 'Monitoring',
                    'icon': '📊',
                    'title': 'Regular Monitoring',
                    'content': 'Monitor your blood pressure regularly and keep a log to share with your healthcare provider.',
                    'priority': 'high'
                }
            ],
            'diabetes': [
                {
                    'id': 'diabetes_001',
                    'category': 'Blood Sugar Management',
                    'icon': '🩸',
                    'title': 'Glucose Monitoring',
                    'content': 'Monitor blood glucose levels as recommended by your doctor and maintain a food diary.',
                    'priority': 'high'
                },
                {
                    'id': 'diabetes_002',
                    'category': 'Foot Care',
                    'icon': '🦶',
                    'title': 'Daily Foot Inspection',
                    'content': 'Inspect your feet daily for cuts, sores, or changes, and maintain proper foot hygiene.',
                    'priority': 'high'
                }
            ]
        }
    
    def _load_lifestyle_tips(self) -> List[Dict[str, Any]]:
        """Load lifestyle-based health tips"""
        return [
            {
                'id': 'lifestyle_001',
                'category': 'Nutrition',
                'icon': '🥗',
                'title': 'Meal Planning',
                'content': 'Plan your meals in advance to ensure balanced nutrition and avoid unhealthy food choices.',
                'priority': 'medium',
                'triggers': ['frequent_fast_food', 'irregular_eating']
            },
            {
                'id': 'lifestyle_002',
                'category': 'Exercise',
                'icon': '🚶‍♀️',
                'title': 'Daily Walking',
                'content': 'Take a 30-minute walk daily to improve cardiovascular health and mental well-being.',
                'priority': 'medium',
                'triggers': ['sedentary_lifestyle', 'stress']
            },
            {
                'id': 'lifestyle_003',
                'category': 'Social Health',
                'icon': '👥',
                'title': 'Social Connections',
                'content': 'Maintain regular social connections with friends and family to support mental health.',
                'priority': 'medium',
                'triggers': ['isolation', 'depression']
            },
            {
                'id': 'lifestyle_004',
                'category': 'Work-Life Balance',
                'icon': '⚖️',
                'title': 'Stress Reduction',
                'content': 'Set boundaries between work and personal time to reduce stress and prevent burnout.',
                'priority': 'medium',
                'triggers': ['work_stress', 'anxiety']
            }
        ]
    
    def _load_emergency_tips(self) -> List[Dict[str, Any]]:
        """Load emergency preparedness tips"""
        return [
            {
                'id': 'emergency_001',
                'category': 'Emergency Preparedness',
                'icon': '🚨',
                'title': 'Emergency Contacts',
                'content': 'Keep an updated list of emergency contacts including doctors, family, and local emergency services.',
                'priority': 'high'
            },
            {
                'id': 'emergency_002',
                'category': 'Medical Information',
                'icon': '🏥',
                'title': 'Medical Alert Bracelet',
                'content': 'Consider wearing a medical alert bracelet if you have chronic conditions or severe allergies.',
                'priority': 'high'
            },
            {
                'id': 'emergency_003',
                'category': 'Medication Management',
                'icon': '💊',
                'title': 'Emergency Medication Kit',
                'content': 'Keep an emergency kit with essential medications and a current medication list.',
                'priority': 'high'
            }
        ]
    
    def generate_personalized_tips(self, user_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Generate personalized health tips based on user's medical history
        
        Args:
            user_data: Dictionary containing user's medical history and patterns
            
        Returns:
            List of personalized health tip dictionaries
        """
        try:
            tips = []
            
            # Always include some general tips
            tips.extend(self._select_general_tips(user_data))
            
            # Add condition-specific tips based on predictions
            if 'predictions' in user_data:
                tips.extend(self._get_condition_specific_tips(user_data['predictions']))
            
            # Add emergency tips if user has emergency history
            if 'emergency_logs' in user_data and user_data['emergency_logs']:
                tips.extend(self._get_emergency_tips(user_data['emergency_logs']))
            
            # Add lifestyle tips based on patterns
            tips.extend(self._get_lifestyle_tips(user_data))
            
            # Remove duplicates and sort by priority
            unique_tips = self._remove_duplicates(tips)
            sorted_tips = self._sort_by_priority(unique_tips)
            
            # Limit to top 10 tips
            return sorted_tips[:10]
            
        except Exception as e:
            logger.error(f"Error generating personalized tips: {e}")
            return self._get_fallback_tips()
    
    def _select_general_tips(self, user_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Select relevant general tips"""
        # Always include high-priority general tips
        selected = [tip for tip in self.general_tips if tip['priority'] == 'high']
        
        # Add some medium-priority tips
        medium_tips = [tip for tip in self.general_tips if tip['priority'] == 'medium']
        selected.extend(medium_tips[:3])
        
        return selected
    
    def _get_condition_specific_tips(self, predictions: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Get tips specific to predicted conditions"""
        tips = []
        
        # Analyze recent predictions
        recent_conditions = []
        for prediction in predictions[-5:]:  # Last 5 predictions
            condition = prediction.get('predicted_disease', '').lower()
            recent_conditions.append(condition)
        
        # Get tips for most common conditions
        condition_counts = Counter(recent_conditions)
        for condition, count in condition_counts.most_common(3):
            if condition in self.condition_specific_tips:
                tips.extend(self.condition_specific_tips[condition])
        
        return tips
    
    def _get_emergency_tips(self, emergency_logs: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Get emergency preparedness tips"""
        if emergency_logs:
            return self.emergency_tips
        return []
    
    def _get_lifestyle_tips(self, user_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Get lifestyle-based tips"""
        tips = []
        
        # Analyze patterns and add relevant lifestyle tips
        predictions_count = len(user_data.get('predictions', []))
        appointments_count = len(user_data.get('appointments', []))
        
        # If user has many predictions, suggest symptom tracking
        if predictions_count > 3:
            tips.append({
                'id': 'pattern_001',
                'category': 'Health Tracking',
                'icon': '📊',
                'title': 'Symptom Diary',
                'content': 'Keep a detailed symptom diary to help identify patterns and triggers for your health conditions.',
                'priority': 'medium'
            })
        
        # If user has appointments, suggest preparation tips
        if appointments_count > 0:
            tips.append({
                'id': 'appointment_001',
                'category': 'Appointment Management',
                'icon': '📋',
                'title': 'Appointment Preparation',
                'content': 'Prepare questions before appointments and bring a current list of medications and symptoms.',
                'priority': 'medium'
            })
        
        # Add some general lifestyle tips
        tips.extend(self.lifestyle_tips[:2])
        
        return tips
    
    def _remove_duplicates(self, tips: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Remove duplicate tips based on ID"""
        seen_ids = set()
        unique_tips = []
        
        for tip in tips:
            tip_id = tip.get('id', tip.get('title', ''))
            if tip_id not in seen_ids:
                seen_ids.add(tip_id)
                unique_tips.append(tip)
        
        return unique_tips
    
    def _sort_by_priority(self, tips: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Sort tips by priority (high > medium > low)"""
        priority_order = {'high': 3, 'medium': 2, 'low': 1}
        
        return sorted(tips, key=lambda x: priority_order.get(x.get('priority', 'low'), 1), reverse=True)
    
    def _get_fallback_tips(self) -> List[Dict[str, Any]]:
        """Get fallback tips in case of error"""
        return self.general_tips[:5]
    
    def get_tip_by_category(self, category: str) -> List[Dict[str, Any]]:
        """
        Get tips by specific category
        
        Args:
            category: Category name to filter by
            
        Returns:
            List of tips in the specified category
        """
        all_tips = self.general_tips + self.lifestyle_tips + self.emergency_tips
        
        # Add condition-specific tips
        for condition_tips in self.condition_specific_tips.values():
            all_tips.extend(condition_tips)
        
        return [tip for tip in all_tips if tip.get('category', '').lower() == category.lower()]
    
    def search_tips(self, query: str) -> List[Dict[str, Any]]:
        """
        Search tips by keyword
        
        Args:
            query: Search query string
            
        Returns:
            List of matching tips
        """
        query_lower = query.lower()
        all_tips = self.general_tips + self.lifestyle_tips + self.emergency_tips
        
        # Add condition-specific tips
        for condition_tips in self.condition_specific_tips.values():
            all_tips.extend(condition_tips)
        
        matching_tips = []
        for tip in all_tips:
            if (query_lower in tip.get('title', '').lower() or 
                query_lower in tip.get('content', '').lower() or 
                query_lower in tip.get('category', '').lower()):
                matching_tips.append(tip)
        
        return self._sort_by_priority(matching_tips)
    
    def get_daily_tip(self) -> Dict[str, Any]:
        """
        Get a daily health tip
        
        Returns:
            Random health tip for daily display
        """
        import random
        
        # Prefer high-priority general tips for daily tips
        high_priority_tips = [tip for tip in self.general_tips if tip['priority'] == 'high']
        
        if high_priority_tips:
            return random.choice(high_priority_tips)
        else:
            return random.choice(self.general_tips)


# Global health tips engine instance
health_tips_engine = None

def get_health_tips_engine() -> HealthTipsEngine:
    """
    Get global health tips engine instance (singleton pattern)
    
    Returns:
        HealthTipsEngine instance
    """
    global health_tips_engine
    if health_tips_engine is None:
        health_tips_engine = HealthTipsEngine()
    return health_tips_engine


if __name__ == "__main__":
    # Test the health tips engine
    print("Testing Health Tips Engine...")
    
    engine = HealthTipsEngine()
    
    # Test personalized tips generation
    test_user_data = {
        'predictions': [
            {'predicted_disease': 'Common Cold', 'severity': 'Low'},
            {'predicted_disease': 'Headache', 'severity': 'Medium'}
        ],
        'appointments': [
            {'doctor_name': 'Dr. Smith', 'status': 'scheduled'}
        ],
        'emergency_logs': []
    }
    
    tips = engine.generate_personalized_tips(test_user_data)
    print(f"Generated {len(tips)} personalized tips")
    
    for tip in tips[:3]:
        print(f"- {tip['category']}: {tip['title']}")
    
    # Test daily tip
    daily_tip = engine.get_daily_tip()
    print(f"Daily tip: {daily_tip['title']}")
    
    print("Health Tips Engine test completed!")