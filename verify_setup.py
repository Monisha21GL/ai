#!/usr/bin/env python3
"""
AI Healthcare Assistant - Setup Verification Script

This script verifies that all components of the AI Healthcare Assistant
are properly installed and configured.

Usage: python verify_setup.py
"""

import sys
import os
import importlib
import sqlite3
from pathlib import Path

def check_python_version():
    """Check if Python version is compatible"""
    print("🐍 Checking Python version...")
    version = sys.version_info
    if version.major == 3 and version.minor >= 7:
        print(f"   ✓ Python {version.major}.{version.minor}.{version.micro} (compatible)")
        return True
    else:
        print(f"   ✗ Python {version.major}.{version.minor}.{version.micro} (requires 3.7+)")
        return False

def check_required_packages():
    """Check if all required packages are installed"""
    print("\n📦 Checking required packages...")
    
    required_packages = [
        'flask',
        'sklearn',
        'pandas',
        'numpy',
        'pytest',
        'hypothesis'
    ]
    
    all_installed = True
    for package in required_packages:
        try:
            importlib.import_module(package)
            print(f"   ✓ {package}")
        except ImportError:
            print(f"   ✗ {package} (not installed)")
            all_installed = False
    
    return all_installed

def check_project_structure():
    """Check if project structure is correct"""
    print("\n📁 Checking project structure...")
    
    required_paths = [
        'app.py',
        'requirements.txt',
        'train_model.py',
        'data/',
        'data/init_database.sql',
        'data/doctors.csv',
        'data/hospitals.csv',
        'data/symptoms_diseases.csv',
        'modules/',
        'modules/__init__.py',
        'modules/database_manager.py',
        'modules/prediction_engine.py',
        'modules/emergency_detector.py',
        'modules/gps_service.py',
        'modules/doctor_recommender.py',
        'modules/appointment_manager.py',
        'modules/health_tips_engine.py',
        'modules/analytics_engine.py',
        'modules/health_chatbot.py',
        'modules/simple_chatbot.py',
        'templates/',
        'templates/base.html',
        'templates/dashboard.html',
        'static/',
        'static/css/',
        'static/js/'
    ]
    
    all_present = True
    for path in required_paths:
        if Path(path).exists():
            print(f"   ✓ {path}")
        else:
            print(f"   ✗ {path} (missing)")
            all_present = False
    
    return all_present

def check_database():
    """Check if database can be initialized"""
    print("\n🗄️  Checking database...")
    
    try:
        # Try to import database manager
        sys.path.append('modules')
        from database_manager import get_db_manager
        
        # Test database connection
        db_manager = get_db_manager()
        print("   ✓ Database manager imported")
        print("   ✓ Database connection successful")
        return True
        
    except Exception as e:
        print(f"   ✗ Database error: {e}")
        return False

def check_ml_model():
    """Check if ML model can be loaded"""
    print("\n🤖 Checking ML model...")
    
    try:
        # Check if model file exists
        model_path = Path('models/disease_model.pkl')
        if not model_path.exists():
            print("   ⚠️  Model file not found, will need training")
            return True  # Not critical, can be trained
        
        # Try to import prediction engine
        sys.path.append('modules')
        from prediction_engine import get_prediction_engine
        
        # Test model loading
        engine = get_prediction_engine()
        print("   ✓ Prediction engine imported")
        print("   ✓ ML model loaded successfully")
        return True
        
    except Exception as e:
        print(f"   ✗ ML model error: {e}")
        return False

def check_flask_app():
    """Check if Flask app can be imported"""
    print("\n🌐 Checking Flask application...")
    
    try:
        from app import app
        print("   ✓ Flask app imported successfully")
        print("   ✓ All modules loaded correctly")
        return True
        
    except Exception as e:
        print(f"   ✗ Flask app error: {e}")
        return False

def run_verification():
    """Run all verification checks"""
    print("AI Healthcare Assistant - Setup Verification")
    print("=" * 50)
    
    checks = [
        check_python_version(),
        check_required_packages(),
        check_project_structure(),
        check_database(),
        check_ml_model(),
        check_flask_app()
    ]
    
    print("\n" + "=" * 50)
    
    if all(checks):
        print("🎉 All checks passed! Your setup is ready.")
        print("\nNext steps:")
        print("1. Train the ML model (if needed): python train_model.py")
        print("2. Start the application: python app.py")
        print("3. Open browser to: http://127.0.0.1:5000/")
        return True
    else:
        print("❌ Some checks failed. Please fix the issues above.")
        print("\nCommon solutions:")
        print("- Install missing packages: pip install -r requirements.txt")
        print("- Check file paths and project structure")
        print("- Initialize database: python -c \"from modules.database_manager import get_db_manager; get_db_manager().initialize_database()\"")
        return False

if __name__ == "__main__":
    success = run_verification()
    sys.exit(0 if success else 1)