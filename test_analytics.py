#!/usr/bin/env python3
"""
Test script for analytics functionality
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from modules.analytics_engine import get_analytics_engine
from modules.database_manager import get_db_manager
import json

def test_analytics_functionality():
    """Test the analytics engine functionality"""
    print("Testing Analytics Engine...")
    
    # Get instances
    db_manager = get_db_manager()
    analytics_engine = get_analytics_engine()
    
    # Test user session
    test_session = "test_analytics_session_123"
    
    print(f"1. Testing with session: {test_session}")
    
    # Create test user
    db_manager.create_user(test_session)
    print("✓ Test user created")
    
    # Add some test data
    prediction_id = db_manager.save_prediction(
        test_session,
        ["headache", "fever", "fatigue"],
        "Common Cold",
        0.85,
        "Medium",
        False
    )
    print(f"✓ Test prediction saved with ID: {prediction_id}")
    
    # Test medical history retrieval
    print("\n2. Testing medical history retrieval...")
    history = analytics_engine.get_user_medical_history(test_session)
    print(f"✓ Retrieved history with {len(history.get('predictions', []))} predictions")
    print(f"✓ Summary generated: {bool(history.get('summary'))}")
    
    # Test data export
    print("\n3. Testing data export...")
    
    # Test JSON export
    json_export = analytics_engine.export_user_data(test_session, 'json')
    print(f"✓ JSON export generated ({len(json_export)} characters)")
    
    # Test CSV export
    csv_export = analytics_engine.export_user_data(test_session, 'csv')
    print(f"✓ CSV export generated ({len(csv_export)} characters)")
    
    # Test TXT export
    txt_export = analytics_engine.export_user_data(test_session, 'txt')
    print(f"✓ TXT export generated ({len(txt_export)} characters)")
    
    # Test system analytics
    print("\n4. Testing system analytics...")
    system_analytics = analytics_engine.get_system_analytics()
    print(f"✓ System analytics generated: {bool(system_analytics)}")
    if system_analytics:
        print(f"  - Database stats: {bool(system_analytics.get('database_stats'))}")
        print(f"  - Prediction analytics: {bool(system_analytics.get('prediction_analytics'))}")
        print(f"  - User analytics: {bool(system_analytics.get('user_analytics'))}")
    
    # Test user interaction logging
    print("\n5. Testing user interaction logging...")
    logged = analytics_engine.log_user_interaction(test_session, 'test_interaction', {'test': True})
    print(f"✓ User interaction logged: {logged}")
    
    print("\n✅ All analytics tests completed successfully!")
    return True

if __name__ == "__main__":
    try:
        test_analytics_functionality()
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)