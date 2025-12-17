#!/usr/bin/env python3
"""
Test script for analytics Flask routes
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import json
from app import app

def test_analytics_routes():
    """Test the analytics Flask routes"""
    print("Testing Analytics Flask Routes...")
    
    with app.test_client() as client:
        # Test user history route
        print("\n1. Testing /analytics/user-history route...")
        response = client.get('/analytics/user-history')
        print(f"✓ Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.get_json()
            print(f"✓ Response success: {data.get('success', False)}")
            print(f"✓ History data present: {bool(data.get('history'))}")
        
        # Test export route
        print("\n2. Testing /analytics/export route...")
        export_data = {
            'format': 'json',
            'categories': ['predictions', 'appointments']
        }
        response = client.post('/analytics/export', 
                             data=json.dumps(export_data),
                             content_type='application/json')
        print(f"✓ Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.get_json()
            print(f"✓ Export success: {data.get('success', False)}")
        
        # Test system analytics route
        print("\n3. Testing /analytics/system route...")
        response = client.get('/analytics/system')
        print(f"✓ Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.get_json()
            print(f"✓ Response success: {data.get('success', False)}")
            print(f"✓ Analytics data present: {bool(data.get('analytics'))}")
        
        # Test analytics summary route
        print("\n4. Testing /analytics/summary route...")
        response = client.get('/analytics/summary')
        print(f"✓ Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.get_json()
            print(f"✓ Response success: {data.get('success', False)}")
            print(f"✓ Summary data present: {bool(data.get('summary'))}")
        
        # Test medical history route (enhanced)
        print("\n5. Testing /medical-history route...")
        response = client.get('/medical-history')
        print(f"✓ Status Code: {response.status_code}")
        print(f"✓ Content type: {response.content_type}")
        
    print("\n✅ All route tests completed!")
    return True

if __name__ == "__main__":
    try:
        test_analytics_routes()
    except Exception as e:
        print(f"❌ Route test failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)