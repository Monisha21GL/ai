"""
AI Healthcare Assistant - Main Flask Application

This is the main Flask application file that handles routing and serves
the healthcare assistance web application on localhost:5000.

Author: AI Healthcare Assistant Team
Date: 2024
Purpose: Academic project for healthcare AI demonstration
"""

from flask import Flask, render_template, request, jsonify, session
import os
import uuid
import logging
import json
from datetime import datetime

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Import our custom modules
from modules.database_manager import get_db_manager
from modules.prediction_engine import get_prediction_engine
from modules.appointment_manager import get_appointment_manager
from modules.emergency_detector import get_emergency_detector
from modules.gps_service import get_gps_service
from modules.doctor_recommender import get_doctor_recommender
from modules.health_tips_engine import get_health_tips_engine
from modules.analytics_engine import get_analytics_engine

# Import health chatbot with fallback
try:
    from modules.health_chatbot import get_health_chatbot
except ImportError as e:
    logger.warning(f"Could not import health chatbot, using simple fallback: {e}")
    from modules.simple_chatbot import get_health_chatbot

# Initialize Flask application
app = Flask(__name__)
app.secret_key = 'healthcare_assistant_secret_key_2024'  # For session management

# Configuration
app.config['DEBUG'] = True
app.config['HOST'] = '127.0.0.1'
app.config['PORT'] = 5000

# Global variables for modules
db_manager = get_db_manager()
prediction_engine = get_prediction_engine()
appointment_manager = get_appointment_manager()
emergency_detector = get_emergency_detector()
gps_service = get_gps_service()
doctor_recommender = get_doctor_recommender()
health_tips_engine = get_health_tips_engine()
analytics_engine = get_analytics_engine()

# Initialize health chatbot
health_chatbot = get_health_chatbot()

def initialize_session():
    """Initialize user session with unique ID"""
    if 'user_id' not in session:
        session['user_id'] = str(uuid.uuid4())
        session['created_at'] = datetime.now().isoformat()
        
        # Create user in database
        db_manager.create_user(session['user_id'])
    else:
        # Update user activity
        db_manager.update_user_activity(session['user_id'])
    
    return session['user_id']

@app.route('/')
def dashboard():
    """
    Main dashboard route - displays the healthcare assistant interface with navigation
    
    Returns:
        Rendered dashboard template with navigation panel and system status
    """
    user_id = initialize_session()
    
    try:
        # Get recent user activity for dashboard
        recent_predictions = []
        recent_appointments = []
        emergency_status = {'active': False, 'level': 'none'}
        
        try:
            # Get recent predictions (last 5)
            recent_predictions = db_manager.get_user_predictions(user_id, limit=5)
        except Exception as e:
            logger.warning(f"Could not load recent predictions: {e}")
        
        try:
            # Get upcoming appointments
            recent_appointments = db_manager.get_user_appointments(user_id)
        except Exception as e:
            logger.warning(f"Could not load appointments: {e}")
        
        # Dashboard data with navigation and recent activity
        dashboard_data = {
            'user_id': user_id,
            'app_title': 'AI Healthcare Assistant',
            'version': '1.0.0',
            'navigation_features': [
                {
                    'name': 'Symptom Checker',
                    'url': '/symptom-checker',
                    'icon': '🩺',
                    'description': 'Enter symptoms for AI analysis'
                },
                {
                    'name': 'Disease Prediction',
                    'url': '/predict-disease',
                    'icon': '🔬',
                    'description': 'Get AI-powered health predictions'
                },
                {
                    'name': 'Emergency Detection',
                    'url': '/check-emergency',
                    'icon': '🚨',
                    'description': 'Check for emergency conditions'
                },
                {
                    'name': 'GPS Location',
                    'url': '/get-location',
                    'icon': '📍',
                    'description': 'Find nearby medical facilities'
                },
                {
                    'name': 'Doctor Recommendations',
                    'url': '/doctors',
                    'icon': '👨‍⚕️',
                    'description': 'Find specialists for your condition'
                },
                {
                    'name': 'Appointment Booking',
                    'url': '/book-appointment',
                    'icon': '📅',
                    'description': 'Schedule medical appointments'
                }
            ],
            'recent_activity': {
                'predictions': recent_predictions,
                'appointments': recent_appointments,
                'emergency_status': emergency_status
            },
            'system_status': {
                'ml_model': 'operational',
                'database': 'connected',
                'emergency_services': 'available',
                'gps_services': 'enabled'
            }
        }
        
        return render_template('dashboard.html', data=dashboard_data)
        
    except Exception as e:
        logger.error(f"Dashboard loading error: {str(e)}")
        # Fallback dashboard data
        fallback_data = {
            'user_id': user_id,
            'app_title': 'AI Healthcare Assistant',
            'version': '1.0.0',
            'navigation_features': [],
            'recent_activity': {'predictions': [], 'appointments': [], 'emergency_status': {'active': False}},
            'system_status': {'status': 'limited'},
            'error': 'Some features may be unavailable'
        }
        return render_template('dashboard.html', data=fallback_data)

@app.route('/symptom-checker')
def symptom_checker():
    """
    Symptom checker form route
    
    Returns:
        Rendered symptom checker template with form
    """
    user_id = initialize_session()
    return render_template('symptom_checker.html', user_id=user_id)

@app.route('/predict-disease', methods=['POST'])
def predict_disease():
    """
    Disease prediction API endpoint
    
    Returns:
        JSON response with prediction results
    """
    try:
        user_id = initialize_session()
        
        # Get symptoms from form data
        symptoms = request.form.getlist('symptoms')
        symptom_text = request.form.get('symptom_text', '')
        
        # Combine symptoms from checkboxes and text input
        all_symptoms = symptoms.copy()
        if symptom_text:
            # Split text input by commas and add to symptoms list
            text_symptoms = [s.strip() for s in symptom_text.split(',') if s.strip()]
            all_symptoms.extend(text_symptoms)
        
        if not all_symptoms:
            return jsonify({
                'success': False,
                'error': 'No symptoms provided',
                'message': 'Please select or enter at least one symptom.'
            }), 400
        
        # Use ML prediction engine
        prediction_result = prediction_engine.predict_disease(all_symptoms)
        
        if prediction_result['success']:
            # Save prediction to database
            primary_pred = prediction_result['primary_prediction']
            db_manager.save_prediction(
                user_id,
                all_symptoms,
                primary_pred['disease'],
                primary_pred['confidence'],
                primary_pred['severity'],
                prediction_result['emergency']
            )
            
            # Format response for frontend
            prediction_result.update({
                'disease': primary_pred['disease'],
                'confidence': primary_pred['confidence'],
                'severity': primary_pred['severity'],
                'symptoms_analyzed': all_symptoms,
                'timestamp': datetime.now().isoformat()
            })
        
        return jsonify(prediction_result)
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e),
            'message': 'Prediction failed. Please try again.'
        }), 500

@app.route('/check-emergency', methods=['POST'])
def check_emergency():
    """
    Emergency detection API endpoint
    
    Returns:
        JSON response with emergency status and alert display
    """
    try:
        user_id = initialize_session()
        
        # Get symptoms and optional prediction result
        data = request.get_json() or {}
        symptoms = data.get('symptoms', [])
        prediction_result = data.get('prediction_result', None)
        
        if not symptoms:
            return jsonify({
                'success': False,
                'error': 'No symptoms provided',
                'message': 'Please provide symptoms for emergency assessment.'
            }), 400
        
        # Use emergency detector
        emergency_response = emergency_detector.detect_emergency(symptoms, prediction_result)
        
        # Format response for frontend
        emergency_result = {
            'success': True,
            'emergency': emergency_response['is_emergency'],
            'severity': emergency_response['severity'],
            'confidence': emergency_response['confidence'],
            'alerts': emergency_response['alerts'],
            'recommendations': emergency_response['recommendations'],
            'emergency_contacts': emergency_response['emergency_contacts'],
            'ambulance_info': emergency_response.get('ambulance_info'),
            'timestamp': emergency_response['timestamp']
        }
        
        # Log emergency if detected
        if emergency_response['is_emergency']:
            logger.info(f"Emergency detected for user {user_id}: {emergency_response['severity']}")
        
        return jsonify(emergency_result)
        
    except Exception as e:
        logger.error(f"Emergency check failed: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e),
            'message': 'Emergency check failed. Please seek immediate medical attention if experiencing severe symptoms.'
        }), 500

@app.route('/get-location', methods=['GET', 'POST'])
def get_location():
    """
    GPS location tracking route with coordinate display
    
    Returns:
        GET: Rendered location template
        POST: JSON response with location data and nearby facilities
    """
    user_id = initialize_session()
    
    if request.method == 'GET':
        # Return location tracking page
        return render_template('location.html', user_id=user_id)
    
    try:
        # Process GPS coordinates from POST request
        data = request.get_json() or {}
        latitude = data.get('latitude')
        longitude = data.get('longitude')
        
        if latitude is None or longitude is None:
            return jsonify({
                'success': False,
                'error': 'Missing coordinates',
                'message': 'Please provide both latitude and longitude.'
            }), 400
        
        # Use GPS service to process location
        location_data = gps_service.process_location(float(latitude), float(longitude))
        
        # Format response for frontend
        location_result = {
            'success': True,
            'coordinates': location_data['coordinates'],
            'nearby_hospitals': location_data['nearby_hospitals'],
            'ambulance_info': location_data['ambulance_info'],
            'emergency_contacts': location_data['emergency_contacts'],
            'location_quality': location_data['location_quality'],
            'display_data': gps_service.get_location_display_data(latitude, longitude)
        }
        
        logger.info(f"Location processed for user {user_id}: {latitude}, {longitude}")
        return jsonify(location_result)
        
    except ValueError as e:
        return jsonify({
            'success': False,
            'error': 'Invalid coordinates',
            'message': str(e)
        }), 400
    except Exception as e:
        logger.error(f"Location processing failed: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e),
            'message': 'Location processing failed. Using default location data.'
        }), 500

@app.route('/doctors')
def doctors_page():
    """
    General doctors page route
    
    Returns:
        Rendered doctors template for browsing all doctors
    """
    user_id = initialize_session()
    
    try:
        # Get all available doctors
        all_doctors = doctor_recommender.doctors_data.to_dict('records')
        
        # Group doctors by specialization
        specializations = {}
        for doctor in all_doctors:
            spec = doctor['specialization']
            if spec not in specializations:
                specializations[spec] = []
            specializations[spec].append(doctor)
        
        doctors_data = {
            'user_id': user_id,
            'all_doctors': all_doctors,
            'specializations': specializations,
            'total_doctors': len(all_doctors)
        }
        
        return render_template('doctors.html', data=doctors_data)
        
    except Exception as e:
        logger.error(f"Doctors page error: {str(e)}")
        return render_template('doctors.html', data={'error': str(e)})

@app.route('/doctors/<disease>')
def get_doctors(disease):
    """
    Doctor recommendations API endpoint with specialization matching
    
    Args:
        disease: Predicted disease name
        
    Returns:
        JSON response with ranked doctor recommendations
    """
    try:
        user_id = initialize_session()
        
        # Get query parameters for filtering
        max_recommendations = int(request.args.get('limit', 5))
        availability_filter = request.args.get('availability', None)
        
        # Use doctor recommender to get recommendations
        recommendation_result = doctor_recommender.recommend_doctors(
            predicted_disease=disease,
            max_recommendations=max_recommendations,
            availability_filter=availability_filter
        )
        
        # Get recommendation summary for additional context
        summary = doctor_recommender.get_recommendation_summary(disease, max_recommendations)
        
        # Extract doctors list from result
        recommendations = recommendation_result.get('doctors', [])
        
        # Format response
        result = {
            'success': True,
            'disease': disease,
            'recommendations': recommendations,
            'summary': summary,
            'count': len(recommendations),
            'filters_applied': {
                'max_recommendations': max_recommendations,
                'availability_filter': availability_filter
            }
        }
        
        logger.info(f"Generated {len(recommendations)} doctor recommendations for {disease}")
        return jsonify(result)
        
    except Exception as e:
        logger.error(f"Doctor recommendation failed: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e),
            'message': 'Failed to load doctor recommendations. Please try again.'
        }), 500

@app.route('/book-appointment', methods=['GET', 'POST'])
def book_appointment():
    """
    Appointment booking route
    
    Returns:
        GET: Rendered appointment booking template
        POST: JSON response with booking confirmation
    """
    user_id = initialize_session()
    
    if request.method == 'GET':
        return render_template('appointment.html', user_id=user_id)
    
    try:
        # Get appointment data from form
        patient_name = request.form.get('patient_name', 'Anonymous Patient')
        doctor_name = request.form.get('doctor_name')
        appointment_date = request.form.get('appointment_date')
        appointment_time = request.form.get('appointment_time')
        appointment_type = request.form.get('appointment_type', 'consultation')
        symptoms = request.form.get('symptoms', '')
        notes = request.form.get('notes', '')
        
        # Validate required fields
        if not all([doctor_name, appointment_date, appointment_time]):
            return jsonify({
                'success': False,
                'message': 'Doctor name, date, and time are required'
            }), 400
        
        # Use appointment manager to book appointment
        booking_result = appointment_manager.book_appointment(
            patient_name=patient_name,
            doctor_name=doctor_name,
            appointment_date=appointment_date,
            appointment_time=appointment_time,
            appointment_type=appointment_type,
            symptoms=symptoms,
            notes=notes
        )
        
        return jsonify(booking_result)
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e),
            'message': 'Appointment booking failed'
        }), 500

@app.route('/get-available-slots')
def get_available_slots():
    """
    Get available appointment slots for a doctor on a specific date
    
    Returns:
        JSON response with available time slots
    """
    try:
        user_id = initialize_session()
        
        doctor_name = request.args.get('doctor_name')
        date = request.args.get('date')
        
        if not doctor_name or not date:
            return jsonify({
                'success': False,
                'message': 'Doctor name and date are required'
            }), 400
        
        slots = appointment_manager.get_available_slots(doctor_name, date)
        
        return jsonify({
            'success': True,
            'doctor_name': doctor_name,
            'date': date,
            'slots': slots
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e),
            'message': 'Failed to get available slots'
        }), 500

@app.route('/cancel-appointment', methods=['POST'])
def cancel_appointment():
    """
    Cancel an existing appointment
    
    Returns:
        JSON response with cancellation result
    """
    try:
        user_id = initialize_session()
        
        appointment_id = request.form.get('appointment_id')
        reason = request.form.get('reason', 'Patient requested cancellation')
        
        if not appointment_id:
            return jsonify({
                'success': False,
                'message': 'Appointment ID is required'
            }), 400
        
        result = appointment_manager.cancel_appointment(int(appointment_id), reason)
        
        return jsonify(result)
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e),
            'message': 'Appointment cancellation failed'
        }), 500

@app.route('/my-appointments')
def my_appointments():
    """
    Get user's appointments
    
    Returns:
        JSON response with user's appointment list
    """
    try:
        user_id = initialize_session()
        
        # Get patient name from query parameter or use default
        patient_name = request.args.get('patient_name', 'Anonymous Patient')
        
        appointments = appointment_manager.get_patient_appointments(patient_name)
        
        return jsonify({
            'success': True,
            'appointments': appointments,
            'count': len(appointments)
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e),
            'message': 'Failed to get appointments'
        }), 500

@app.route('/appointment-summary')
def appointment_summary():
    """
    Get appointment system summary
    
    Returns:
        JSON response with system summary
    """
    try:
        user_id = initialize_session()
        
        summary = appointment_manager.get_appointment_summary()
        
        return jsonify({
            'success': True,
            'summary': summary
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e),
            'message': 'Failed to get appointment summary'
        }), 500

@app.route('/medical-history')
def medical_history():
    """
    Medical history route with enhanced analytics
    
    Returns:
        Rendered medical history template with comprehensive data
    """
    user_id = initialize_session()
    
    # Get comprehensive history data using analytics engine
    try:
        # Get complete medical history with analytics
        complete_history = analytics_engine.get_user_medical_history(user_id, limit=50)
        
        # Extract data for template
        history_data = {
            'user_id': user_id,
            'predictions': complete_history.get('predictions', []),
            'appointments': complete_history.get('appointments', []),
            'emergency_logs': complete_history.get('emergency_logs', []),
            'location_logs': complete_history.get('location_logs', []),
            'summary': complete_history.get('summary', {}),
            'analytics_available': True
        }
        
        # Log history access
        analytics_engine.log_user_interaction(user_id, 'medical_history_view', {})
        
    except Exception as e:
        logger.error(f"Enhanced medical history failed, falling back to basic: {e}")
        # Fallback to basic data if analytics engine fails
        try:
            predictions = db_manager.get_user_predictions(user_id, limit=10)
            appointments = db_manager.get_user_appointments(user_id)
            emergency_logs = db_manager.get_user_emergency_logs(user_id)
            
            history_data = {
                'user_id': user_id,
                'predictions': predictions,
                'appointments': appointments,
                'emergency_logs': emergency_logs,
                'location_logs': [],
                'summary': {},
                'analytics_available': False,
                'error': str(e)
            }
        except Exception as fallback_error:
            # Ultimate fallback to empty data
            history_data = {
                'user_id': user_id,
                'predictions': [],
                'appointments': [],
                'emergency_logs': [],
                'location_logs': [],
                'summary': {},
                'analytics_available': False,
                'error': str(fallback_error)
            }
    
    return render_template('history.html', data=history_data)

@app.route('/health-tips', methods=['GET', 'POST'])
def health_tips():
    """
    Health tips route - generates personalized health recommendations
    
    Returns:
        GET: JSON response with personalized health tips
        POST: JSON response with tips based on provided user data
    """
    try:
        user_id = initialize_session()
        
        if request.method == 'POST':
            # Get user data from request
            user_data = request.get_json() or {}
        else:
            # Get user data from database for GET requests
            try:
                predictions = db_manager.get_user_predictions(user_id, limit=10)
                appointments = db_manager.get_user_appointments(user_id)
                emergency_logs = db_manager.get_user_emergency_logs(user_id)
                
                user_data = {
                    'predictions': predictions,
                    'appointments': appointments,
                    'emergency_logs': emergency_logs
                }
            except Exception as e:
                logger.warning(f"Could not load user data for tips: {e}")
                user_data = {}
        
        # Generate personalized tips
        tips = health_tips_engine.generate_personalized_tips(user_data)
        
        return jsonify({
            'success': True,
            'tips': tips,
            'count': len(tips),
            'user_id': user_id,
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        logger.error(f"Health tips generation failed: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e),
            'message': 'Failed to generate health tips. Please try again.'
        }), 500

@app.route('/daily-tip')
def daily_tip():
    """
    Get daily health tip
    
    Returns:
        JSON response with daily health tip
    """
    try:
        user_id = initialize_session()
        
        tip = health_tips_engine.get_daily_tip()
        
        return jsonify({
            'success': True,
            'tip': tip,
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        logger.error(f"Daily tip generation failed: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e),
            'message': 'Failed to get daily tip.'
        }), 500

@app.route('/search-tips')
def search_tips():
    """
    Search health tips by keyword
    
    Returns:
        JSON response with matching tips
    """
    try:
        user_id = initialize_session()
        
        query = request.args.get('q', '').strip()
        category = request.args.get('category', '').strip()
        
        if query:
            tips = health_tips_engine.search_tips(query)
        elif category:
            tips = health_tips_engine.get_tip_by_category(category)
        else:
            return jsonify({
                'success': False,
                'message': 'Please provide a search query or category'
            }), 400
        
        return jsonify({
            'success': True,
            'tips': tips,
            'count': len(tips),
            'query': query,
            'category': category,
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        logger.error(f"Tip search failed: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e),
            'message': 'Failed to search tips.'
        }), 500

@app.route('/chatbot', methods=['POST'])
def chatbot():
    """
    Health chatbot endpoint
    
    Returns:
        JSON response with chatbot reply
    """
    try:
        user_id = initialize_session()
        

        
        data = request.get_json() or {}
        user_message = data.get('message', '').strip()
        
        if not user_message:
            return jsonify({
                'success': False,
                'message': 'Please provide a message'
            }), 400
        
        # Get chatbot response
        response = health_chatbot.get_response(user_message)
        
        # Add suggested actions
        suggestions = health_chatbot.get_suggested_actions(response['category'])
        response['suggestions'] = suggestions
        
        logger.info(f"Chatbot interaction for user {user_id}: {response['category']}")
        
        return jsonify(response)
        
    except Exception as e:
        logger.error(f"Chatbot interaction failed: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e),
            'message': 'Chatbot is temporarily unavailable. Please try again.'
        }), 500

@app.route('/chatbot-history')
def chatbot_history():
    """
    Get chatbot conversation history
    
    Returns:
        JSON response with conversation history
    """
    try:
        user_id = initialize_session()
        
        history = health_chatbot.get_conversation_history()
        
        return jsonify({
            'success': True,
            'history': history,
            'count': len(history),
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        logger.error(f"Chatbot history retrieval failed: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e),
            'message': 'Failed to get conversation history.'
        }), 500

@app.route('/clear-chat')
def clear_chat():
    """
    Clear chatbot conversation history
    
    Returns:
        JSON response with success status
    """
    try:
        user_id = initialize_session()
        
        health_chatbot.clear_conversation()
        
        return jsonify({
            'success': True,
            'message': 'Conversation history cleared',
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        logger.error(f"Chat clearing failed: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e),
            'message': 'Failed to clear conversation.'
        }), 500

@app.route('/analytics/user-history')
def get_user_analytics():
    """
    Get comprehensive user medical history and analytics
    
    Returns:
        JSON response with complete user history and statistics
    """
    try:
        user_id = initialize_session()
        
        # Get query parameters
        limit = request.args.get('limit', type=int)
        include_summary = request.args.get('include_summary', 'true').lower() == 'true'
        
        # Get comprehensive medical history
        history = analytics_engine.get_user_medical_history(user_id, limit)
        
        # Log user interaction
        analytics_engine.log_user_interaction(user_id, 'analytics_view', {
            'limit': limit,
            'include_summary': include_summary
        })
        
        return jsonify({
            'success': True,
            'history': history,
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        logger.error(f"User analytics retrieval failed: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e),
            'message': 'Failed to retrieve user analytics.'
        }), 500

@app.route('/analytics/export', methods=['POST'])
def export_user_data():
    """
    Export user medical data in various formats
    
    Returns:
        File download or JSON response with export data
    """
    try:
        user_id = initialize_session()
        
        # Get export parameters
        data = request.get_json() or {}
        format_type = data.get('format', 'json').lower()
        include_categories = data.get('categories', None)
        
        # Validate format
        if format_type not in ['json', 'csv', 'txt']:
            return jsonify({
                'success': False,
                'message': 'Invalid format. Supported formats: json, csv, txt'
            }), 400
        
        # Export data
        exported_data = analytics_engine.export_user_data(
            user_id, 
            format_type, 
            include_categories
        )
        
        # Log export activity
        analytics_engine.log_user_interaction(user_id, 'data_export', {
            'format': format_type,
            'categories': include_categories
        })
        
        # Return appropriate response based on format
        if format_type == 'json':
            return jsonify({
                'success': True,
                'data': json.loads(exported_data) if isinstance(exported_data, str) else exported_data,
                'format': format_type,
                'timestamp': datetime.now().isoformat()
            })
        else:
            # For CSV and TXT, return as downloadable content
            from flask import Response
            
            filename = f"medical_history_{user_id[:8]}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.{format_type}"
            
            return Response(
                exported_data,
                mimetype='text/plain' if format_type == 'txt' else 'text/csv',
                headers={
                    'Content-Disposition': f'attachment; filename={filename}',
                    'Content-Type': 'application/octet-stream'
                }
            )
        
    except Exception as e:
        logger.error(f"Data export failed: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e),
            'message': 'Data export failed.'
        }), 500

@app.route('/analytics/system')
def get_system_analytics():
    """
    Get system-wide analytics and statistics
    
    Returns:
        JSON response with system analytics
    """
    try:
        user_id = initialize_session()
        
        # Get system analytics
        system_analytics = analytics_engine.get_system_analytics()
        
        # Log analytics access
        analytics_engine.log_user_interaction(user_id, 'system_analytics_view', {})
        
        return jsonify({
            'success': True,
            'analytics': system_analytics,
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        logger.error(f"System analytics retrieval failed: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e),
            'message': 'Failed to retrieve system analytics.'
        }), 500

@app.route('/analytics/summary')
def get_analytics_summary():
    """
    Get summary statistics for user dashboard
    
    Returns:
        JSON response with summary statistics
    """
    try:
        user_id = initialize_session()
        
        # Get user history for summary
        history = analytics_engine.get_user_medical_history(user_id, limit=100)
        summary = history.get('summary', {})
        
        # Add additional computed metrics
        enhanced_summary = {
            **summary,
            'health_score': calculate_health_score(history),
            'risk_level': assess_risk_level(history),
            'recommendations': generate_summary_recommendations(history)
        }
        
        # Log summary access
        analytics_engine.log_user_interaction(user_id, 'summary_view', {})
        
        return jsonify({
            'success': True,
            'summary': enhanced_summary,
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        logger.error(f"Analytics summary retrieval failed: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e),
            'message': 'Failed to retrieve analytics summary.'
        }), 500

def calculate_health_score(history: dict) -> int:
    """
    Calculate a simple health score based on user history
    
    Args:
        history: User medical history
        
    Returns:
        Health score (0-100)
    """
    try:
        score = 100  # Start with perfect score
        
        predictions = history.get('predictions', [])
        emergencies = history.get('emergency_logs', [])
        appointments = history.get('appointments', [])
        
        # Deduct points for emergencies
        emergency_count = len(emergencies)
        score -= min(emergency_count * 20, 60)  # Max 60 points deduction
        
        # Deduct points for high severity predictions
        high_severity_count = sum(1 for p in predictions if p.get('severity') == 'High')
        score -= min(high_severity_count * 10, 30)  # Max 30 points deduction
        
        # Add points for completed appointments (proactive care)
        completed_appointments = sum(1 for a in appointments if a.get('status') == 'completed')
        score += min(completed_appointments * 5, 20)  # Max 20 points addition
        
        # Ensure score is within bounds
        return max(0, min(100, score))
        
    except Exception:
        return 75  # Default moderate score

def assess_risk_level(history: dict) -> str:
    """
    Assess user's health risk level based on history
    
    Args:
        history: User medical history
        
    Returns:
        Risk level string
    """
    try:
        emergencies = len(history.get('emergency_logs', []))
        predictions = history.get('predictions', [])
        high_severity = sum(1 for p in predictions if p.get('severity') == 'High')
        
        if emergencies > 2 or high_severity > 5:
            return 'High'
        elif emergencies > 0 or high_severity > 2:
            return 'Medium'
        else:
            return 'Low'
            
    except Exception:
        return 'Unknown'

def generate_summary_recommendations(history: dict) -> list:
    """
    Generate health recommendations based on user history
    
    Args:
        history: User medical history
        
    Returns:
        List of recommendation strings
    """
    try:
        recommendations = []
        
        predictions = history.get('predictions', [])
        appointments = history.get('appointments', [])
        emergencies = history.get('emergency_logs', [])
        
        # Check for patterns and generate recommendations
        if len(emergencies) > 0:
            recommendations.append("Consider creating an emergency action plan with your healthcare provider")
        
        if len(predictions) > 5:
            recommendations.append("Regular health monitoring shows good health awareness")
        
        completed_appointments = sum(1 for a in appointments if a.get('status') == 'completed')
        if completed_appointments == 0 and len(predictions) > 0:
            recommendations.append("Consider scheduling a check-up with a healthcare provider")
        
        if not recommendations:
            recommendations.append("Continue maintaining good health practices")
        
        return recommendations
        
    except Exception:
        return ["Consult with healthcare professionals for personalized advice"]

@app.errorhandler(404)
def not_found_error(error):
    """Handle 404 errors"""
    return render_template('error.html', 
                         error_code=404, 
                         error_message='Page not found'), 404

@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    return render_template('error.html', 
                         error_code=500, 
                         error_message='Internal server error'), 500

if __name__ == '__main__':
    """
    Main application entry point
    Runs the Flask development server on localhost:5000
    """
    print("Starting AI Healthcare Assistant...")
    print("Server will run on http://127.0.0.1:5000/")
    print("Press Ctrl+C to stop the server")
    
    # Create necessary directories
    os.makedirs('templates', exist_ok=True)
    os.makedirs('static/css', exist_ok=True)
    os.makedirs('static/js', exist_ok=True)
    os.makedirs('static/images', exist_ok=True)
    os.makedirs('data', exist_ok=True)
    os.makedirs('modules', exist_ok=True)
    os.makedirs('models', exist_ok=True)
    
    # Run the Flask application
    app.run(
        host=app.config['HOST'],
        port=app.config['PORT'],
        debug=app.config['DEBUG']
    )