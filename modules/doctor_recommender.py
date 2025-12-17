"""
AI Healthcare Assistant - Doctor Recommendation Engine

This module implements doctor recommendation logic based on predicted diseases,
specialization matching, availability checking, and ranking algorithms.

Author: AI Healthcare Assistant Team
Date: 2024
Purpose: Academic project for healthcare AI demonstration
"""

import json
import logging
import os
from typing import List, Dict, Any, Optional
from datetime import datetime
import pandas as pd

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DoctorRecommender:
    """
    Doctor recommendation system with specialization matching and ranking
    """
    
    def __init__(self):
        """Initialize doctor recommender with specialization mappings and data"""
        # Initialize database manager with error handling
        self.db_manager = None
        try:
            from modules.database_manager import get_db_manager
            self.db_manager = get_db_manager()
            logger.info("Database manager loaded successfully")
        except Exception as e:
            logger.warning(f"Database manager not available: {e}")
        
        # Disease to specialization mapping
        self.disease_specialization_map = {
            # Cardiovascular diseases
            'heart attack': ['Cardiology', 'Emergency Medicine', 'Internal Medicine'],
            'myocardial infarction': ['Cardiology', 'Emergency Medicine'],
            'cardiac arrest': ['Cardiology', 'Emergency Medicine'],
            'hypertension': ['Cardiology', 'Internal Medicine', 'General Medicine'],
            'high blood pressure': ['Cardiology', 'Internal Medicine', 'General Medicine'],
            'arrhythmia': ['Cardiology'],
            'heart disease': ['Cardiology', 'Internal Medicine'],
            'chest pain': ['Cardiology', 'Emergency Medicine', 'Internal Medicine'],
            
            # Neurological diseases
            'stroke': ['Neurology', 'Emergency Medicine'],
            'migraine': ['Neurology', 'General Medicine'],
            'headache': ['Neurology', 'General Medicine', 'Internal Medicine'],
            'seizure': ['Neurology', 'Emergency Medicine'],
            'epilepsy': ['Neurology'],
            
            # Respiratory diseases
            'asthma': ['Pulmonology', 'Internal Medicine', 'General Medicine'],
            'pneumonia': ['Pulmonology', 'Internal Medicine', 'Emergency Medicine'],
            'bronchitis': ['Pulmonology', 'Internal Medicine', 'General Medicine'],
            'copd': ['Pulmonology', 'Internal Medicine'],
            
            # Gastrointestinal diseases
            'gastritis': ['Gastroenterology', 'Internal Medicine'],
            'ulcer': ['Gastroenterology', 'Internal Medicine'],
            'ibs': ['Gastroenterology', 'Internal Medicine'],
            
            # Endocrine diseases
            'diabetes': ['Endocrinology', 'Internal Medicine', 'General Medicine'],
            'thyroid disease': ['Endocrinology', 'Internal Medicine'],
            'hyperthyroidism': ['Endocrinology'],
            'hypothyroidism': ['Endocrinology'],
            
            # Musculoskeletal diseases
            'arthritis': ['Rheumatology', 'Orthopedics'],
            'osteoporosis': ['Rheumatology', 'Orthopedics', 'Endocrinology'],
            'fracture': ['Orthopedics', 'Emergency Medicine'],
            'back pain': ['Orthopedics', 'Neurology'],
            'joint pain': ['Rheumatology', 'Orthopedics'],
            
            # Dermatological diseases
            'eczema': ['Dermatology'],
            'psoriasis': ['Dermatology'],
            'skin cancer': ['Dermatology', 'Oncology'],
            'acne': ['Dermatology', 'General Medicine'],
            'rash': ['Dermatology', 'General Medicine'],
            
            # Mental health
            'depression': ['Psychiatry'],
            'anxiety': ['Psychiatry'],
            'bipolar disorder': ['Psychiatry'],
            
            # Women's health
            'pregnancy': ['Gynecology', 'Obstetrics'],
            'menstrual disorders': ['Gynecology'],
            
            # Urological diseases
            'kidney stones': ['Urology', 'Nephrology'],
            'uti': ['Urology', 'Internal Medicine', 'General Medicine'],
            'prostate disease': ['Urology'],
            
            # General/Common conditions
            'common cold': ['General Medicine', 'Internal Medicine'],
            'flu': ['General Medicine', 'Internal Medicine'],
            'fever': ['General Medicine', 'Internal Medicine', 'Emergency Medicine'],
            'fatigue': ['General Medicine', 'Internal Medicine'],
            'weight loss': ['General Medicine', 'Internal Medicine', 'Endocrinology'],
            'insomnia': ['General Medicine', 'Psychiatry'],
            'allergies': ['General Medicine', 'Internal Medicine']
        }
        
        # Specialization priority weights (higher = more specialized)
        self.specialization_weights = {
            'Emergency Medicine': 10,
            'Cardiology': 9,
            'Neurology': 9,
            'Oncology': 9,
            'Pulmonology': 8,
            'Gastroenterology': 8,
            'Endocrinology': 8,
            'Rheumatology': 8,
            'Dermatology': 7,
            'Orthopedics': 7,
            'Urology': 7,
            'Psychiatry': 7,
            'Gynecology': 7,
            'Pediatrics': 7,
            'Internal Medicine': 5,
            'General Medicine': 4
        }
        
        # Load doctors data
        self.doctors_data = self._load_doctors_data()

    def _load_doctors_data(self) -> pd.DataFrame:
        """Load doctors data from CSV file"""
        try:
            if self.db_manager:
                return self.db_manager.load_doctors_data()
            else:
                # Try to load directly from CSV
                csv_path = "data/doctors.csv"
                if os.path.exists(csv_path):
                    return pd.read_csv(csv_path)
                else:
                    logger.warning("Doctors CSV file not found, using default data")
                    return self._get_default_doctors_data()
        except Exception as e:
            logger.error(f"Error loading doctors data: {e}")
            return self._get_default_doctors_data()

    def _get_default_doctors_data(self) -> pd.DataFrame:
        """Get default doctors data for simulation"""
        default_doctors = [
            {
                'name': 'Dr. John Smith',
                'specialization': 'General Medicine',
                'availability': 'Available',
                'contact': '+1234567890',
                'rating': 4.5,
                'experience_years': 15,
                'hospital_affiliation': 'City General Hospital'
            },
            {
                'name': 'Dr. Sarah Johnson',
                'specialization': 'Cardiology',
                'availability': 'Available',
                'contact': '+1234567891',
                'rating': 4.8,
                'experience_years': 12,
                'hospital_affiliation': "St. Mary's Medical Center"
            },
            {
                'name': 'Dr. Michael Brown',
                'specialization': 'Neurology',
                'availability': 'Busy',
                'contact': '+1234567892',
                'rating': 4.6,
                'experience_years': 18,
                'hospital_affiliation': 'City General Hospital'
            },
            {
                'name': 'Dr. Emily Davis',
                'specialization': 'Dermatology',
                'availability': 'Available',
                'contact': '+1234567893',
                'rating': 4.7,
                'experience_years': 10,
                'hospital_affiliation': 'Skin Care Clinic'
            },
            {
                'name': 'Dr. Maria Garcia',
                'specialization': 'Endocrinology',
                'availability': 'Available',
                'contact': '+1234567801',
                'rating': 4.4,
                'experience_years': 9,
                'hospital_affiliation': 'Diabetes & Hormone Clinic'
            }
        ]
        return pd.DataFrame(default_doctors)

    def recommend_doctors(self, predicted_disease: str, max_recommendations: int = 5,
                         availability_filter: str = None) -> Dict[str, Any]:
        """
        Recommend doctors based on predicted disease
        
        Args:
            predicted_disease: Disease name from prediction engine
            max_recommendations: Maximum number of doctors to recommend
            availability_filter: Filter by availability ('Available', 'Busy', None for all)
            
        Returns:
            Dictionary with success status and list of recommended doctors
        """
        try:
            # Normalize disease name for matching
            disease_normalized = predicted_disease.lower().strip()
            
            # Find relevant specializations
            relevant_specializations = self._find_relevant_specializations(disease_normalized)
            
            if not relevant_specializations:
                logger.warning(f"No specializations found for disease: {predicted_disease}")
                # Fallback to general medicine
                relevant_specializations = ['General Medicine', 'Internal Medicine']
            
            # Get matching doctors
            matching_doctors = self._find_matching_doctors(
                relevant_specializations, availability_filter
            )
            
            # Rank doctors by relevance
            ranked_doctors = self._rank_doctors(matching_doctors, relevant_specializations)
            
            # Format recommendations
            recommendations = self._format_recommendations(
                ranked_doctors[:max_recommendations], predicted_disease
            )
            
            logger.info(f"Generated {len(recommendations)} doctor recommendations for {predicted_disease}")
            
            return {
                'success': True,
                'disease': predicted_disease,
                'doctors': recommendations,
                'count': len(recommendations),
                'specializations_matched': relevant_specializations
            }
            
        except Exception as e:
            logger.error(f"Error recommending doctors: {str(e)}")
            return {
                'success': False,
                'error': str(e),
                'disease': predicted_disease,
                'doctors': [],
                'count': 0
            }

    def _find_relevant_specializations(self, disease: str) -> List[str]:
        """Find relevant medical specializations for a disease"""
        relevant_specializations = []
        
        # Direct match
        if disease in self.disease_specialization_map:
            relevant_specializations.extend(self.disease_specialization_map[disease])
        
        # Partial match (for compound disease names)
        for disease_key, specializations in self.disease_specialization_map.items():
            if disease_key in disease or disease in disease_key:
                relevant_specializations.extend(specializations)
        
        # Remove duplicates while preserving order
        seen = set()
        unique_specializations = []
        for spec in relevant_specializations:
            if spec not in seen:
                seen.add(spec)
                unique_specializations.append(spec)
        
        return unique_specializations

    def _find_matching_doctors(self, specializations: List[str], 
                              availability_filter: str = None) -> List[Dict[str, Any]]:
        """Find doctors matching the required specializations"""
        matching_doctors = []
        
        for _, doctor in self.doctors_data.iterrows():
            # Check specialization match
            doctor_specialization = doctor['specialization']
            if doctor_specialization in specializations:
                # Check availability filter
                if availability_filter and doctor['availability'] != availability_filter:
                    continue
                
                doctor_info = {
                    'name': doctor['name'],
                    'specialization': doctor['specialization'],
                    'availability': doctor['availability'],
                    'contact': doctor['contact'],
                    'rating': doctor.get('rating', 0.0),
                    'experience_years': doctor.get('experience_years', 0),
                    'hospital_affiliation': doctor.get('hospital_affiliation', 'Unknown')
                }
                matching_doctors.append(doctor_info)
        
        return matching_doctors

    def _rank_doctors(self, doctors: List[Dict[str, Any]], 
                     relevant_specializations: List[str]) -> List[Dict[str, Any]]:
        """Rank doctors by relevance, specialization, rating, and experience"""
        for doctor in doctors:
            score = 0
            
            # Specialization relevance score
            specialization = doctor['specialization']
            if specialization in relevant_specializations:
                # Higher score for earlier (more relevant) specializations
                relevance_index = relevant_specializations.index(specialization)
                specialization_score = (len(relevant_specializations) - relevance_index) * 10
                
                # Add specialization weight
                weight = self.specialization_weights.get(specialization, 1)
                score += specialization_score + weight
            
            # Rating score (0-5 scale, multiply by 10)
            rating_score = doctor.get('rating', 0) * 10
            score += rating_score
            
            # Experience score (years / 2, max 25 points)
            experience_score = min(doctor.get('experience_years', 0) / 2, 25)
            score += experience_score
            
            # Availability bonus
            if doctor['availability'] == 'Available':
                score += 20
            elif doctor['availability'] == 'Busy':
                score += 5  # Still some points for being potentially available
            
            doctor['relevance_score'] = round(score, 2)
        
        # Sort by relevance score (highest first)
        return sorted(doctors, key=lambda x: x['relevance_score'], reverse=True)

    def _format_recommendations(self, doctors: List[Dict[str, Any]], 
                               disease: str) -> List[Dict[str, Any]]:
        """Format doctor recommendations for display"""
        recommendations = []
        
        for i, doctor in enumerate(doctors):
            recommendation = {
                'rank': i + 1,
                'doctor_info': {
                    'name': doctor['name'],
                    'specialization': doctor['specialization'],
                    'availability': doctor['availability'],
                    'contact': doctor['contact'],
                    'rating': doctor['rating'],
                    'experience_years': doctor['experience_years'],
                    'hospital_affiliation': doctor['hospital_affiliation']
                },
                'relevance': {
                    'score': doctor['relevance_score'],
                    'reason': self._generate_relevance_reason(doctor, disease),
                    'match_quality': self._calculate_match_quality(doctor['relevance_score'])
                },
                'availability_info': {
                    'status': doctor['availability'],
                    'next_available': self._estimate_next_availability(doctor['availability']),
                    'booking_urgency': self._assess_booking_urgency(doctor['availability'])
                }
            }
            recommendations.append(recommendation)
        
        return recommendations

    def _generate_relevance_reason(self, doctor: Dict[str, Any], disease: str) -> str:
        """Generate explanation for why this doctor is relevant"""
        specialization = doctor['specialization']
        rating = doctor['rating']
        experience = doctor['experience_years']
        
        reasons = []
        
        # Specialization relevance
        if specialization in ['Emergency Medicine', 'Cardiology', 'Neurology', 'Oncology']:
            reasons.append(f"Specialist in {specialization}")
        else:
            reasons.append(f"Experienced in {specialization}")
        
        # Rating
        if rating >= 4.7:
            reasons.append("Highly rated by patients")
        elif rating >= 4.5:
            reasons.append("Well-rated by patients")
        
        # Experience
        if experience >= 15:
            reasons.append(f"{experience} years of experience")
        elif experience >= 10:
            reasons.append("Experienced practitioner")
        
        return ", ".join(reasons)

    def _calculate_match_quality(self, score: float) -> str:
        """Calculate match quality based on relevance score"""
        if score >= 80:
            return "Excellent match"
        elif score >= 60:
            return "Very good match"
        elif score >= 40:
            return "Good match"
        elif score >= 20:
            return "Fair match"
        else:
            return "Basic match"

    def _estimate_next_availability(self, availability: str) -> str:
        """Estimate next available appointment time"""
        if availability == 'Available':
            return "Today or tomorrow"
        elif availability == 'Busy':
            return "Within 1-2 weeks"
        else:
            return "Contact for availability"

    def _assess_booking_urgency(self, availability: str) -> str:
        """Assess urgency of booking with this doctor"""
        if availability == 'Available':
            return "Book soon - currently available"
        elif availability == 'Busy':
            return "Book early - limited availability"
        else:
            return "Contact to check availability"

    def get_recommendation_summary(self, disease: str, max_doctors: int = 3) -> Dict[str, Any]:
        """Get a summary of doctor recommendations for dashboard display"""
        try:
            recommendations = self.recommend_doctors(disease, max_doctors)
            
            summary = {
                'disease': disease,
                'total_recommendations': len(recommendations),
                'top_doctors': [],
                'specializations_needed': self._find_relevant_specializations(disease.lower()),
                'booking_advice': self._generate_booking_advice(recommendations),
                'timestamp': datetime.now().isoformat()
            }
            
            for rec in recommendations:
                doctor_summary = {
                    'name': rec['doctor_info']['name'],
                    'specialization': rec['doctor_info']['specialization'],
                    'rating': rec['doctor_info']['rating'],
                    'availability': rec['doctor_info']['availability'],
                    'match_quality': rec['relevance']['match_quality'],
                    'contact': rec['doctor_info']['contact']
                }
                summary['top_doctors'].append(doctor_summary)
            
            return summary
            
        except Exception as e:
            logger.error(f"Error generating recommendation summary: {str(e)}")
            return {
                'disease': disease,
                'total_recommendations': 0,
                'top_doctors': [],
                'specializations_needed': [],
                'booking_advice': 'Please consult with a healthcare professional',
                'timestamp': datetime.now().isoformat(),
                'error': str(e)
            }

    def _generate_booking_advice(self, recommendations: List[Dict[str, Any]]) -> str:
        """Generate advice for booking appointments"""
        if not recommendations:
            return "No doctors available. Please try again later or contact emergency services if urgent."
        
        available_count = sum(1 for rec in recommendations 
                            if rec['doctor_info']['availability'] == 'Available')
        
        if available_count > 0:
            return f"{available_count} doctor(s) currently available. Book soon for earliest appointment."
        else:
            return "All recommended doctors are busy. Consider booking in advance or checking for cancellations."

    def get_availability_summary(self) -> Dict[str, Any]:
        """
        Get summary of doctor availability
        
        Returns:
            Dictionary with availability statistics
        """
        try:
            total_doctors = len(self.doctors_data)
            available_doctors = len(self.doctors_data[self.doctors_data['availability'] == 'Available'])
            busy_doctors = len(self.doctors_data[self.doctors_data['availability'] == 'Busy'])
            
            return {
                'total_doctors': total_doctors,
                'available_doctors': available_doctors,
                'busy_doctors': busy_doctors,
                'availability_rate': available_doctors / total_doctors if total_doctors > 0 else 0
            }
        except Exception as e:
            logger.error(f"Error getting availability summary: {str(e)}")
            return {'error': str(e)}


# Factory function for dependency injection
def get_doctor_recommender() -> DoctorRecommender:
    """Factory function to create and return DoctorRecommender instance"""
    return DoctorRecommender()


    def get_availability_summary(self) -> Dict[str, Any]:
        """
        Get summary of doctor availability
        
        Returns:
            Dictionary with availability statistics
        """
        try:
            total_doctors = len(self.doctors_data)
            available_doctors = len(self.doctors_data[self.doctors_data['availability'] == 'Available'])
            busy_doctors = len(self.doctors_data[self.doctors_data['availability'] == 'Busy'])
            
            return {
                'total_doctors': total_doctors,
                'available_doctors': available_doctors,
                'busy_doctors': busy_doctors,
                'availability_rate': available_doctors / total_doctors if total_doctors > 0 else 0
            }
        except Exception as e:
            logger.error(f"Error getting availability summary: {str(e)}")
            return {'error': str(e)}


# Factory function for dependency injection
def get_doctor_recommender() -> DoctorRecommender:
    """Factory function to create and return DoctorRecommender instance"""
    return DoctorRecommender()


# Example usage and testing
if __name__ == "__main__":
    # Initialize doctor recommender
    recommender = get_doctor_recommender()
    
    # Test doctor recommendations
    print("=== Doctor Recommender Test ===")
    
    # Test disease recommendations
    test_diseases = ["heart attack", "diabetes", "headache", "rash"]
    
    for disease in test_diseases:
        print(f"\n--- Recommendations for {disease} ---")
        recommendations = recommender.recommend_doctors(disease, max_recommendations=3)
        
        if recommendations:
            for rec in recommendations:
                doctor = rec['doctor_info']
                print(f"Dr. {doctor['name']} - {doctor['specialization']}")
                print(f"  Rating: {doctor['rating']}/5, Experience: {doctor['experience_years']} years")
                print(f"  Availability: {doctor['availability']}")
                print(f"  Match Quality: {rec['relevance']['match_quality']}")
                print(f"  Reason: {rec['relevance']['reason']}")
        else:
            print("No recommendations found")
    
    # Test recommendation summary
    print(f"\n--- Summary for diabetes ---")
    summary = recommender.get_recommendation_summary("diabetes")
    print(f"Total recommendations: {summary['total_recommendations']}")
    print(f"Specializations needed: {summary['specializations_needed']}")
    print(f"Booking advice: {summary['booking_advice']}")
    
    print("\nDoctor Recommender test completed!")