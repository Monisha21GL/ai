"""
AI Healthcare Assistant - Disease Prediction Engine

This module implements machine learning-based disease prediction using scikit-learn.
It handles symptom preprocessing, feature engineering, model training, and prediction.

Author: AI Healthcare Assistant Team
Date: 2024
Purpose: Academic project for healthcare AI demonstration
"""

import pandas as pd
import numpy as np
import pickle
import os
import json
from typing import List, Dict, Any, Tuple, Optional
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.preprocessing import LabelEncoder, MultiLabelBinarizer
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class PredictionEngine:
    """
    Machine learning engine for disease prediction based on symptoms
    """
    
    def __init__(self, model_path: str = "models/disease_model.pkl"):
        """
        Initialize prediction engine
        
        Args:
            model_path: Path to save/load the trained model
        """
        self.model_path = model_path
        self.model = None
        self.symptom_encoder = None
        self.disease_encoder = None
        self.feature_names = []
        self.disease_names = []
        self.model_metadata = {}
        
        # Ensure models directory exists
        os.makedirs(os.path.dirname(model_path), exist_ok=True)
        
        # Try to load existing model
        self.load_model()
    
    def preprocess_symptoms_data(self, df: pd.DataFrame) -> Tuple[np.ndarray, np.ndarray]:
        """
        Preprocess symptoms data for machine learning
        
        Args:
            df: DataFrame with symptoms and diseases
            
        Returns:
            Tuple of (features, labels) as numpy arrays
        """
        try:
            # Extract symptom columns (all columns except 'disease', 'severity', 'emergency')
            symptom_columns = [col for col in df.columns 
                             if col not in ['disease', 'severity', 'emergency']]
            
            # Create symptom lists for each row
            symptom_lists = []
            for _, row in df.iterrows():
                symptoms = []
                for col in symptom_columns:
                    if pd.notna(row[col]) and row[col] != '':
                        symptoms.append(str(row[col]).strip().lower())
                symptom_lists.append(symptoms)
            
            # Use MultiLabelBinarizer to create binary feature matrix
            self.symptom_encoder = MultiLabelBinarizer()
            X = self.symptom_encoder.fit_transform(symptom_lists)
            self.feature_names = list(self.symptom_encoder.classes_)
            
            # Encode diseases
            self.disease_encoder = LabelEncoder()
            y = self.disease_encoder.fit_transform(df['disease'])
            self.disease_names = list(self.disease_encoder.classes_)
            
            logger.info(f"Preprocessed data: {X.shape[0]} samples, {X.shape[1]} features, {len(self.disease_names)} diseases")
            
            return X, y
            
        except Exception as e:
            logger.error(f"Error preprocessing symptoms data: {e}")
            raise
    
    def train_model(self, training_data_path: str = "data/symptoms_diseases.csv") -> Dict[str, Any]:
        """
        Train the disease prediction model
        
        Args:
            training_data_path: Path to training data CSV file
            
        Returns:
            Dictionary with training results and metrics
        """
        try:
            # Load training data
            if not os.path.exists(training_data_path):
                raise FileNotFoundError(f"Training data not found: {training_data_path}")
            
            df = pd.read_csv(training_data_path)
            logger.info(f"Loaded training data: {len(df)} samples")
            
            # Preprocess data
            X, y = self.preprocess_symptoms_data(df)
            
            # For small datasets, use the entire dataset for training and testing
            # This is acceptable for academic/demo purposes
            if len(df) < 100:
                logger.info("Small dataset detected, using entire dataset for training")
                X_train, X_test = X, X
                y_train, y_test = y, y
            else:
                # Split data for larger datasets
                unique_classes, class_counts = np.unique(y, return_counts=True)
                min_class_count = np.min(class_counts)
                
                if min_class_count >= 2:
                    X_train, X_test, y_train, y_test = train_test_split(
                        X, y, test_size=0.2, random_state=42, stratify=y
                    )
                else:
                    X_train, X_test, y_train, y_test = train_test_split(
                        X, y, test_size=0.2, random_state=42
                    )
            
            # Initialize and train Random Forest model
            self.model = RandomForestClassifier(
                n_estimators=100,
                max_depth=10,
                min_samples_split=5,
                min_samples_leaf=2,
                random_state=42,
                class_weight='balanced'
            )
            
            logger.info("Training Random Forest model...")
            self.model.fit(X_train, y_train)
            
            # Evaluate model
            train_accuracy = self.model.score(X_train, y_train)
            test_accuracy = self.model.score(X_test, y_test)
            
            # Cross-validation (adjust CV folds for small datasets)
            cv_folds = min(5, min_class_count) if len(df) >= 100 else min(3, len(df) // 2)
            if cv_folds >= 2:
                cv_scores = cross_val_score(self.model, X, y, cv=cv_folds)
            else:
                # Skip cross-validation for very small datasets
                cv_scores = np.array([test_accuracy])
            
            # Predictions for detailed metrics
            y_pred = self.model.predict(X_test)
            
            # Store model metadata
            self.model_metadata = {
                'training_samples': len(df),
                'features_count': X.shape[1],
                'diseases_count': len(self.disease_names),
                'train_accuracy': train_accuracy,
                'test_accuracy': test_accuracy,
                'cv_mean_accuracy': cv_scores.mean(),
                'cv_std_accuracy': cv_scores.std(),
                'feature_names': self.feature_names,
                'disease_names': self.disease_names
            }
            
            # Save the trained model
            self.save_model()
            
            logger.info(f"Model training completed. Test accuracy: {test_accuracy:.3f}")
            
            return {
                'success': True,
                'train_accuracy': train_accuracy,
                'test_accuracy': test_accuracy,
                'cv_mean_accuracy': cv_scores.mean(),
                'cv_std_accuracy': cv_scores.std(),
                'features_count': X.shape[1],
                'diseases_count': len(self.disease_names),
                'classification_report': classification_report(y_test, y_pred, 
                                                             target_names=self.disease_names,
                                                             output_dict=True)
            }
            
        except Exception as e:
            logger.error(f"Error training model: {e}")
            return {'success': False, 'error': str(e)}
    
    def predict_disease(self, symptoms: List[str]) -> Dict[str, Any]:
        """
        Predict disease based on input symptoms
        
        Args:
            symptoms: List of symptom strings
            
        Returns:
            Dictionary with prediction results
        """
        try:
            if self.model is None or self.symptom_encoder is None:
                raise ValueError("Model not trained or loaded")
            
            if not symptoms:
                raise ValueError("No symptoms provided")
            
            # Preprocess input symptoms
            processed_symptoms = [symptom.strip().lower() for symptom in symptoms if symptom.strip()]
            
            if not processed_symptoms:
                raise ValueError("No valid symptoms provided")
            
            # Transform symptoms to feature vector
            X = self.symptom_encoder.transform([processed_symptoms])
            
            # Get prediction probabilities
            probabilities = self.model.predict_proba(X)[0]
            
            # Get top predictions
            top_indices = np.argsort(probabilities)[::-1][:3]  # Top 3 predictions
            
            predictions = []
            for i, idx in enumerate(top_indices):
                disease = self.disease_names[idx]
                confidence = probabilities[idx]
                
                # Determine severity based on disease and confidence
                severity = self.determine_severity(disease, confidence)
                
                predictions.append({
                    'disease': disease,
                    'confidence': float(confidence),
                    'severity': severity,
                    'rank': i + 1
                })
            
            # Primary prediction
            primary_prediction = predictions[0]
            
            # Check if it's an emergency
            is_emergency = self.check_emergency_condition(processed_symptoms, primary_prediction)
            
            result = {
                'success': True,
                'primary_prediction': primary_prediction,
                'all_predictions': predictions,
                'emergency': is_emergency,
                'symptoms_analyzed': processed_symptoms,
                'model_info': {
                    'features_used': len([s for s in processed_symptoms if s in self.feature_names]),
                    'total_features': len(self.feature_names),
                    'model_accuracy': self.model_metadata.get('test_accuracy', 'Unknown')
                }
            }
            
            logger.info(f"Prediction completed: {primary_prediction['disease']} ({primary_prediction['confidence']:.3f})")
            
            return result
            
        except Exception as e:
            logger.error(f"Error predicting disease: {e}")
            return {
                'success': False,
                'error': str(e),
                'primary_prediction': {
                    'disease': 'Unknown',
                    'confidence': 0.0,
                    'severity': 'Low'
                },
                'emergency': False
            }
    
    def determine_severity(self, disease: str, confidence: float) -> str:
        """
        Determine severity level based on disease and confidence
        
        Args:
            disease: Predicted disease name
            confidence: Prediction confidence
            
        Returns:
            Severity level (Low/Medium/High)
        """
        # High severity diseases
        high_severity_diseases = [
            'heart attack', 'meningitis', 'appendicitis', 'stroke', 
            'pneumonia', 'sepsis', 'anaphylaxis', 'pulmonary embolism'
        ]
        
        # Medium severity diseases
        medium_severity_diseases = [
            'influenza', 'bronchitis', 'gastroenteritis', 'migraine',
            'asthma', 'diabetes', 'hypertension', 'depression'
        ]
        
        disease_lower = disease.lower()
        
        # Check disease severity
        if any(severe_disease in disease_lower for severe_disease in high_severity_diseases):
            return 'High'
        elif any(medium_disease in disease_lower for medium_disease in medium_severity_diseases):
            return 'Medium' if confidence > 0.6 else 'Low'
        else:
            # Base severity on confidence
            if confidence > 0.8:
                return 'Medium'
            else:
                return 'Low'
    
    def check_emergency_condition(self, symptoms: List[str], prediction: Dict[str, Any]) -> bool:
        """
        Check if symptoms indicate an emergency condition
        
        Args:
            symptoms: List of processed symptoms
            prediction: Primary disease prediction
            
        Returns:
            True if emergency, False otherwise
        """
        # Emergency symptoms
        emergency_symptoms = [
            'chest pain', 'chest_pain', 'shortness of breath', 'shortness_of_breath',
            'severe headache', 'severe_headache', 'difficulty breathing', 'difficulty_breathing',
            'unconsciousness', 'seizures', 'severe bleeding', 'severe_bleeding',
            'stroke symptoms', 'heart attack', 'anaphylaxis', 'severe allergic reaction'
        ]
        
        # Emergency diseases
        emergency_diseases = [
            'heart attack', 'stroke', 'meningitis', 'appendicitis', 
            'anaphylaxis', 'sepsis', 'pulmonary embolism'
        ]
        
        # Check for emergency symptoms
        for symptom in symptoms:
            if any(emergency_symptom in symptom for emergency_symptom in emergency_symptoms):
                return True
        
        # Check for emergency diseases with high confidence
        disease_lower = prediction['disease'].lower()
        if (any(emergency_disease in disease_lower for emergency_disease in emergency_diseases) 
            and prediction['confidence'] > 0.7):
            return True
        
        # High severity with high confidence
        if prediction['severity'] == 'High' and prediction['confidence'] > 0.8:
            return True
        
        return False
    
    def get_feature_importance(self, top_n: int = 20) -> List[Dict[str, Any]]:
        """
        Get feature importance from the trained model
        
        Args:
            top_n: Number of top features to return
            
        Returns:
            List of feature importance dictionaries
        """
        try:
            if self.model is None or not hasattr(self.model, 'feature_importances_'):
                return []
            
            importances = self.model.feature_importances_
            feature_importance = []
            
            for i, importance in enumerate(importances):
                if i < len(self.feature_names):
                    feature_importance.append({
                        'feature': self.feature_names[i],
                        'importance': float(importance)
                    })
            
            # Sort by importance and return top N
            feature_importance.sort(key=lambda x: x['importance'], reverse=True)
            return feature_importance[:top_n]
            
        except Exception as e:
            logger.error(f"Error getting feature importance: {e}")
            return []
    
    def save_model(self):
        """Save the trained model and encoders to file"""
        try:
            model_data = {
                'model': self.model,
                'symptom_encoder': self.symptom_encoder,
                'disease_encoder': self.disease_encoder,
                'feature_names': self.feature_names,
                'disease_names': self.disease_names,
                'metadata': self.model_metadata
            }
            
            with open(self.model_path, 'wb') as f:
                pickle.dump(model_data, f)
            
            logger.info(f"Model saved to {self.model_path}")
            
        except Exception as e:
            logger.error(f"Error saving model: {e}")
    
    def load_model(self) -> bool:
        """
        Load trained model from file
        
        Returns:
            True if model loaded successfully, False otherwise
        """
        try:
            if not os.path.exists(self.model_path):
                logger.info(f"No existing model found at {self.model_path}")
                return False
            
            with open(self.model_path, 'rb') as f:
                model_data = pickle.load(f)
            
            self.model = model_data['model']
            self.symptom_encoder = model_data['symptom_encoder']
            self.disease_encoder = model_data['disease_encoder']
            self.feature_names = model_data['feature_names']
            self.disease_names = model_data['disease_names']
            self.model_metadata = model_data.get('metadata', {})
            
            logger.info(f"Model loaded successfully from {self.model_path}")
            return True
            
        except Exception as e:
            logger.error(f"Error loading model: {e}")
            return False
    
    def get_model_info(self) -> Dict[str, Any]:
        """
        Get information about the current model
        
        Returns:
            Dictionary with model information
        """
        if self.model is None:
            return {'status': 'No model loaded'}
        
        return {
            'status': 'Model loaded',
            'model_type': type(self.model).__name__,
            'features_count': len(self.feature_names),
            'diseases_count': len(self.disease_names),
            'metadata': self.model_metadata
        }
    
    def validate_symptoms(self, symptoms: List[str]) -> Dict[str, Any]:
        """
        Validate input symptoms against known features
        
        Args:
            symptoms: List of symptom strings
            
        Returns:
            Dictionary with validation results
        """
        if not self.feature_names:
            return {'valid': False, 'message': 'Model not loaded'}
        
        processed_symptoms = [symptom.strip().lower() for symptom in symptoms if symptom.strip()]
        
        if not processed_symptoms:
            return {'valid': False, 'message': 'No valid symptoms provided'}
        
        # Check which symptoms are recognized
        recognized_symptoms = [s for s in processed_symptoms if s in self.feature_names]
        unrecognized_symptoms = [s for s in processed_symptoms if s not in self.feature_names]
        
        return {
            'valid': len(recognized_symptoms) > 0,
            'recognized_symptoms': recognized_symptoms,
            'unrecognized_symptoms': unrecognized_symptoms,
            'recognition_rate': len(recognized_symptoms) / len(processed_symptoms) if processed_symptoms else 0
        }

    def get_model_summary(self) -> Dict[str, Any]:
        """
        Get model summary information
        
        Returns:
            Dictionary with model information
        """
        try:
            summary = {
                'model_loaded': self.model is not None,
                'model_type': type(self.model).__name__ if self.model else None,
                'feature_count': len(self.feature_names) if self.feature_names else 0,
                'disease_classes': len(self.disease_classes) if self.disease_classes else 0,
                'available_symptoms': len(self.available_symptoms),
                'prediction_ready': self.model is not None and self.feature_names is not None
            }
            
            if self.model and hasattr(self.model, 'n_estimators'):
                summary['model_estimators'] = self.model.n_estimators
            
            return summary
            
        except Exception as e:
            logger.error(f"Error generating model summary: {str(e)}")
            return {'error': str(e)}


# Global prediction engine instance
prediction_engine = None

def get_prediction_engine() -> PredictionEngine:
    """
    Get global prediction engine instance (singleton pattern)
    
    Returns:
        PredictionEngine instance
    """
    global prediction_engine
    if prediction_engine is None:
        prediction_engine = PredictionEngine()
    return prediction_engine


# Factory function for dependency injection
def get_prediction_engine() -> PredictionEngine:
    """Factory function to create and return PredictionEngine instance"""
    return PredictionEngine()


if __name__ == "__main__":
    # Test the prediction engine
    print("Testing Prediction Engine...")
    
    engine = PredictionEngine()
    
    # Train model if not already trained
    if engine.model is None:
        print("Training model...")
        training_results = engine.train_model()
        print(f"Training results: {training_results}")
    
    # Test prediction
    test_symptoms = ["headache", "fever", "fatigue"]
    print(f"\nTesting prediction with symptoms: {test_symptoms}")
    
    prediction = engine.predict_disease(test_symptoms)
    print(f"Prediction result: {prediction}")
    
    # Test model info
    model_info = engine.get_model_info()
    print(f"\nModel info: {model_info}")
    
    # Test feature importance
    importance = engine.get_feature_importance(10)
    print(f"\nTop 10 important features: {importance}")
    
    print("Prediction Engine test completed!")