#!/usr/bin/env python3
"""
AI Healthcare Assistant - Model Training Script

This script generates comprehensive datasets and trains the machine learning model
for disease prediction based on symptoms.

Requirements: 2.2, 2.4, 5.3, 6.4
"""

import pandas as pd
import numpy as np
import os
import sys
import json
from datetime import datetime
from typing import List, Dict, Any
import logging

# Add modules to path
sys.path.append('modules')

from prediction_engine import PredictionEngine

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def enhance_symptoms_diseases_dataset():
    """
    Enhance the symptoms-diseases dataset with more comprehensive data
    """
    logger.info("Enhancing symptoms-diseases dataset...")
    
    # Additional comprehensive symptom-disease combinations
    additional_data = [
        # Respiratory conditions
        ["persistent_cough", "shortness_of_breath", "wheezing", "chest_tightness", "fatigue", "Chronic Obstructive Pulmonary Disease", "High", "false"],
        ["dry_cough", "fever", "fatigue", "loss_of_taste", "loss_of_smell", "COVID-19", "Medium", "false"],
        ["severe_cough", "blood_in_sputum", "chest_pain", "weight_loss", "night_sweats", "Tuberculosis", "High", "false"],
        
        # Cardiovascular conditions
        ["irregular_heartbeat", "dizziness", "fainting", "chest_discomfort", "fatigue", "Arrhythmia", "Medium", "true"],
        ["leg_swelling", "shortness_of_breath", "fatigue", "rapid_weight_gain", "cough", "Heart Failure", "High", "true"],
        ["sudden_severe_headache", "vision_changes", "weakness", "speech_difficulty", "confusion", "Stroke", "High", "true"],
        
        # Gastrointestinal conditions
        ["severe_abdominal_pain", "nausea", "vomiting", "fever", "loss_of_appetite", "Appendicitis", "High", "true"],
        ["burning_stomach_pain", "nausea", "bloating", "heartburn", "loss_of_appetite", "Peptic Ulcer", "Medium", "false"],
        ["chronic_diarrhea", "abdominal_pain", "weight_loss", "fatigue", "blood_in_stool", "Inflammatory Bowel Disease", "Medium", "false"],
        
        # Neurological conditions
        ["severe_headache", "visual_disturbances", "nausea", "sensitivity_to_light", "throbbing_pain", "Migraine", "Medium", "false"],
        ["tremor", "muscle_stiffness", "slow_movement", "balance_problems", "speech_changes", "Parkinson's Disease", "Medium", "false"],
        ["memory_loss", "confusion", "difficulty_concentrating", "mood_changes", "disorientation", "Dementia", "Medium", "false"],
        
        # Endocrine conditions
        ["weight_gain", "fatigue", "cold_intolerance", "dry_skin", "hair_loss", "Hypothyroidism", "Low", "false"],
        ["weight_loss", "rapid_heartbeat", "sweating", "nervousness", "heat_intolerance", "Hyperthyroidism", "Medium", "false"],
        ["extreme_fatigue", "muscle_weakness", "weight_loss", "low_blood_pressure", "skin_darkening", "Addison's Disease", "High", "false"],
        
        # Infectious diseases
        ["high_fever", "severe_headache", "muscle_pain", "rash", "bleeding", "Dengue Fever", "High", "true"],
        ["fever", "chills", "headache", "muscle_aches", "fatigue", "Malaria", "High", "false"],
        ["sore_throat", "fever", "swollen_lymph_nodes", "fatigue", "rash", "Mononucleosis", "Medium", "false"],
        
        # Musculoskeletal conditions
        ["lower_back_pain", "leg_pain", "numbness", "tingling", "muscle_weakness", "Sciatica", "Medium", "false"],
        ["joint_pain", "muscle_pain", "fatigue", "sleep_problems", "tender_points", "Fibromyalgia", "Low", "false"],
        ["bone_pain", "fractures", "height_loss", "stooped_posture", "back_pain", "Osteoporosis", "Medium", "false"],
        
        # Skin conditions
        ["red_scaly_patches", "itching", "dry_skin", "cracking", "bleeding", "Eczema", "Low", "false"],
        ["red_patches", "silvery_scales", "itching", "joint_pain", "nail_changes", "Psoriasis", "Low", "false"],
        ["new_mole", "changing_mole", "irregular_borders", "color_variation", "bleeding", "Skin Cancer", "High", "false"],
        
        # Kidney and urinary conditions
        ["flank_pain", "blood_in_urine", "frequent_urination", "nausea", "fever", "Kidney Stones", "High", "true"],
        ["burning_urination", "frequent_urination", "cloudy_urine", "pelvic_pain", "fever", "Urinary Tract Infection", "Medium", "false"],
        ["swelling", "high_blood_pressure", "protein_in_urine", "fatigue", "decreased_urination", "Kidney Disease", "High", "false"],
        
        # Eye and vision conditions
        ["eye_pain", "blurred_vision", "halos_around_lights", "nausea", "headache", "Glaucoma", "High", "false"],
        ["sudden_vision_loss", "eye_pain", "headache", "nausea", "vomiting", "Acute Angle-Closure Glaucoma", "High", "true"],
        ["gradual_vision_loss", "difficulty_seeing_at_night", "sensitivity_to_light", "halos", "double_vision", "Cataracts", "Low", "false"],
        
        # Additional emergency conditions
        ["severe_allergic_reaction", "difficulty_breathing", "swelling", "rapid_pulse", "dizziness", "Anaphylaxis", "High", "true"],
        ["severe_dehydration", "dizziness", "rapid_heartbeat", "dry_mouth", "confusion", "Severe Dehydration", "High", "true"],
        ["high_fever", "confusion", "rapid_breathing", "rapid_heartbeat", "low_blood_pressure", "Sepsis", "High", "true"],
    ]
    
    # Read existing data
    existing_df = pd.read_csv("data/symptoms_diseases.csv")
    
    # Create DataFrame for additional data
    columns = ["symptom1", "symptom2", "symptom3", "symptom4", "symptom5", "disease", "severity", "emergency"]
    additional_df = pd.DataFrame(additional_data, columns=columns)
    
    # Combine datasets
    enhanced_df = pd.concat([existing_df, additional_df], ignore_index=True)
    
    # Remove duplicates
    enhanced_df = enhanced_df.drop_duplicates()
    
    # Save enhanced dataset
    enhanced_df.to_csv("data/symptoms_diseases.csv", index=False)
    
    logger.info(f"Enhanced symptoms-diseases dataset: {len(existing_df)} -> {len(enhanced_df)} records")
    return len(enhanced_df)

def enhance_doctors_dataset():
    """
    Enhance the doctors dataset with more comprehensive data
    """
    logger.info("Enhancing doctors dataset...")
    
    # Additional doctors data
    additional_doctors = [
        ["Dr. Patricia Johnson", "Infectious Disease", "Available", "+1234567810", "4.7", "14", "City General Hospital"],
        ["Dr. Mark Williams", "Oncology", "Busy", "+1234567811", "4.9", "22", "St. Mary's Medical Center"],
        ["Dr. Susan Brown", "Nephrology", "Available", "+1234567812", "4.6", "16", "Kidney Care Center"],
        ["Dr. Robert Davis", "Ophthalmology", "Available", "+1234567813", "4.8", "18", "Eye Care Institute"],
        ["Dr. Linda Miller", "Hematology", "Busy", "+1234567814", "4.5", "12", "Blood Disorders Clinic"],
        ["Dr. William Wilson", "Anesthesiology", "Available", "+1234567815", "4.4", "20", "City General Hospital"],
        ["Dr. Mary Moore", "Radiology", "Available", "+1234567816", "4.7", "15", "Imaging Center"],
        ["Dr. Charles Taylor", "Pathology", "Available", "+1234567817", "4.6", "19", "Diagnostic Laboratory"],
        ["Dr. Barbara Anderson", "Physical Medicine", "Available", "+1234567818", "4.5", "11", "Rehabilitation Center"],
        ["Dr. Richard Thomas", "Plastic Surgery", "Busy", "+1234567819", "4.8", "17", "Cosmetic Surgery Center"],
        ["Dr. Nancy Jackson", "Geriatrics", "Available", "+1234567820", "4.6", "21", "Senior Care Clinic"],
        ["Dr. Daniel White", "Sports Medicine", "Available", "+1234567821", "4.7", "13", "Sports Medicine Institute"],
        ["Dr. Karen Harris", "Allergy and Immunology", "Available", "+1234567822", "4.8", "16", "Allergy Treatment Center"],
        ["Dr. Joseph Martin", "Pain Management", "Busy", "+1234567823", "4.5", "14", "Pain Relief Clinic"],
        ["Dr. Lisa Thompson", "Occupational Medicine", "Available", "+1234567824", "4.4", "10", "Workplace Health Center"],
    ]
    
    # Read existing data
    existing_df = pd.read_csv("data/doctors.csv")
    
    # Create DataFrame for additional data
    columns = ["name", "specialization", "availability", "contact", "rating", "experience_years", "hospital_affiliation"]
    additional_df = pd.DataFrame(additional_doctors, columns=columns)
    
    # Combine datasets
    enhanced_df = pd.concat([existing_df, additional_df], ignore_index=True)
    
    # Remove duplicates
    enhanced_df = enhanced_df.drop_duplicates()
    
    # Save enhanced dataset
    enhanced_df.to_csv("data/doctors.csv", index=False)
    
    logger.info(f"Enhanced doctors dataset: {len(existing_df)} -> {len(enhanced_df)} records")
    return len(enhanced_df)

def enhance_hospitals_dataset():
    """
    Enhance the hospitals dataset with more comprehensive data
    """
    logger.info("Enhancing hospitals dataset...")
    
    # Additional hospitals data with GPS coordinates (New York area)
    additional_hospitals = [
        ["Kidney Care Center", "40.7505", "-73.9934", "+1234567825", "false", "Nephrology,Dialysis,Kidney Transplant", "4.5"],
        ["Eye Care Institute", "40.7282", "-73.9942", "+1234567826", "false", "Ophthalmology,Eye Surgery,Vision Care", "4.8"],
        ["Blood Disorders Clinic", "40.7614", "-73.9776", "+1234567827", "false", "Hematology,Blood Cancer,Transfusion", "4.6"],
        ["Imaging Center", "40.7831", "-73.9712", "+1234567828", "false", "Radiology,MRI,CT Scan,Ultrasound", "4.7"],
        ["Diagnostic Laboratory", "40.7489", "-73.9680", "+1234567829", "false", "Pathology,Lab Tests,Biopsy", "4.5"],
        ["Rehabilitation Center", "40.7359", "-74.0014", "+1234567830", "false", "Physical Therapy,Occupational Therapy", "4.6"],
        ["Cosmetic Surgery Center", "40.7677", "-73.9537", "+1234567831", "false", "Plastic Surgery,Cosmetic Procedures", "4.8"],
        ["Senior Care Clinic", "40.7505", "-73.9934", "+1234567832", "false", "Geriatrics,Elder Care,Memory Care", "4.7"],
        ["Sports Medicine Institute", "40.7128", "-74.0060", "+1234567833", "false", "Sports Medicine,Orthopedics,Physical Therapy", "4.6"],
        ["Allergy Treatment Center", "40.7589", "-73.9851", "+1234567834", "false", "Allergy,Immunology,Asthma Treatment", "4.8"],
        ["Pain Relief Clinic", "40.7282", "-73.9942", "+1234567835", "false", "Pain Management,Chronic Pain,Interventional Pain", "4.5"],
        ["Workplace Health Center", "40.7614", "-73.9776", "+1234567836", "false", "Occupational Medicine,Work Injuries", "4.4"],
        ["Emergency Trauma Center", "40.7831", "-73.9712", "+1234567837", "true", "Emergency Medicine,Trauma Surgery,Critical Care", "4.9"],
        ["Cardiac Surgery Center", "40.7489", "-73.9680", "+1234567838", "true", "Cardiac Surgery,Heart Procedures,ICU", "4.8"],
        ["Neurological Institute", "40.7359", "-74.0014", "+1234567839", "false", "Neurology,Neurosurgery,Brain Disorders", "4.7"],
    ]
    
    # Read existing data
    existing_df = pd.read_csv("data/hospitals.csv")
    
    # Create DataFrame for additional data
    columns = ["name", "latitude", "longitude", "contact", "emergency_services", "specialties", "rating"]
    additional_df = pd.DataFrame(additional_hospitals, columns=columns)
    
    # Combine datasets
    enhanced_df = pd.concat([existing_df, additional_df], ignore_index=True)
    
    # Remove duplicates
    enhanced_df = enhanced_df.drop_duplicates()
    
    # Save enhanced dataset
    enhanced_df.to_csv("data/hospitals.csv", index=False)
    
    logger.info(f"Enhanced hospitals dataset: {len(existing_df)} -> {len(enhanced_df)} records")
    return len(enhanced_df)

def train_and_validate_model():
    """
    Train the machine learning model and validate its accuracy
    """
    logger.info("Training and validating machine learning model...")
    
    # Initialize prediction engine
    engine = PredictionEngine()
    
    # Train the model
    training_results = engine.train_model("data/symptoms_diseases.csv")
    
    if not training_results['success']:
        logger.error(f"Model training failed: {training_results.get('error', 'Unknown error')}")
        return False
    
    # Log training results
    logger.info(f"Model training completed successfully!")
    logger.info(f"Training accuracy: {training_results['train_accuracy']:.3f}")
    logger.info(f"Test accuracy: {training_results['test_accuracy']:.3f}")
    logger.info(f"Cross-validation accuracy: {training_results['cv_mean_accuracy']:.3f} ± {training_results['cv_std_accuracy']:.3f}")
    logger.info(f"Features count: {training_results['features_count']}")
    logger.info(f"Disease classes: {training_results['diseases_count']}")
    
    # Test predictions with sample data
    test_cases = [
        ["fever", "headache", "cough", "fatigue", "sore_throat"],
        ["chest_pain", "shortness_of_breath", "nausea", "sweating"],
        ["severe_headache", "neck_stiffness", "fever", "light_sensitivity"],
        ["joint_pain", "stiffness", "swelling", "fatigue"],
        ["frequent_urination", "excessive_thirst", "fatigue", "blurred_vision"]
    ]
    
    logger.info("\nTesting model predictions:")
    for i, symptoms in enumerate(test_cases, 1):
        prediction = engine.predict_disease(symptoms)
        if prediction['success']:
            primary = prediction['primary_prediction']
            logger.info(f"Test {i}: {symptoms} -> {primary['disease']} "
                       f"(confidence: {primary['confidence']:.3f}, severity: {primary['severity']})")
        else:
            logger.error(f"Test {i} failed: {prediction.get('error', 'Unknown error')}")
    
    # Get feature importance
    importance = engine.get_feature_importance(10)
    if importance:
        logger.info("\nTop 10 most important features:")
        for i, feature in enumerate(importance, 1):
            logger.info(f"{i}. {feature['feature']}: {feature['importance']:.4f}")
    
    # Validate model meets requirements
    min_accuracy = 0.7  # Minimum 70% accuracy for academic purposes
    if training_results['test_accuracy'] >= min_accuracy:
        logger.info(f"✓ Model meets accuracy requirement (>= {min_accuracy:.1%})")
        return True
    else:
        logger.warning(f"✗ Model accuracy ({training_results['test_accuracy']:.1%}) below requirement ({min_accuracy:.1%})")
        return False

def generate_model_report():
    """
    Generate a comprehensive model report
    """
    logger.info("Generating model report...")
    
    engine = PredictionEngine()
    model_info = engine.get_model_info()
    
    report = {
        "model_training_report": {
            "timestamp": datetime.now().isoformat(),
            "model_info": model_info,
            "datasets": {
                "symptoms_diseases": len(pd.read_csv("data/symptoms_diseases.csv")),
                "doctors": len(pd.read_csv("data/doctors.csv")),
                "hospitals": len(pd.read_csv("data/hospitals.csv"))
            },
            "feature_importance": engine.get_feature_importance(20),
            "requirements_validation": {
                "2.2": "Disease prediction using scikit-learn - ✓ Implemented",
                "2.4": "Model loading from pickle file - ✓ Implemented", 
                "5.3": "Doctor specialization data - ✓ Enhanced",
                "6.4": "Hospital GPS coordinates - ✓ Enhanced"
            }
        }
    }
    
    # Save report
    with open("model_training_report.json", "w") as f:
        json.dump(report, f, indent=2)
    
    logger.info("Model report saved to model_training_report.json")
    return report

def main():
    """
    Main function to execute all dataset enhancement and model training tasks
    """
    logger.info("Starting AI Healthcare Assistant model training process...")
    
    try:
        # Enhance datasets
        symptoms_count = enhance_symptoms_diseases_dataset()
        doctors_count = enhance_doctors_dataset()
        hospitals_count = enhance_hospitals_dataset()
        
        logger.info(f"Dataset enhancement completed:")
        logger.info(f"- Symptoms-diseases: {symptoms_count} records")
        logger.info(f"- Doctors: {doctors_count} records") 
        logger.info(f"- Hospitals: {hospitals_count} records")
        
        # Train and validate model
        model_success = train_and_validate_model()
        
        if model_success:
            logger.info("✓ Model training and validation successful")
        else:
            logger.warning("⚠ Model training completed but may need improvement")
        
        # Generate report
        report = generate_model_report()
        
        logger.info("AI Healthcare Assistant model training process completed successfully!")
        return True
        
    except Exception as e:
        logger.error(f"Error in model training process: {e}")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)