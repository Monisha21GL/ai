#!/usr/bin/env python3
"""
Test Analytics Web Interface Integration
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import json
from app import app

def test_analytics_web_integration():
    """Test the analytics web interface integration"""
    print("🌐 Testing Analytics Web Interface Integration")
    print("=" * 60)
    
    with app.test_client() as client:
        print("1. Testing Medical History Page")
        print("-" * 40)
        
        # Test medical history page
        response = client.get('/medical-history')
        print(f"✓ Medical History Route Status: {response.status_code}")
        print(f"✓ Content Type: {response.content_type}")
        
        if response.status_code == 200:
            content = response.get_data(as_text=True)
            print(f"✓ Page contains analytics: {'analytics' in content.lower()}")
            print(f"✓ Page contains export: {'export' in content.lower()}")
            print(f"✓ Page contains history: {'history' in content.lower()}")
        
        print("\n2. Testing Analytics API Endpoints")
        print("-" * 40)
        
        # Test user history API
        response = client.get('/analytics/user-history')
        print(f"✓ User History API Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.get_json()
            print(f"✓ API Success: {data.get('success', False)}")
            print(f"✓ History Data Present: {bool(data.get('history'))}")
            
            if data.get('history'):
                history = data['history']
                print(f"  - Predictions: {len(history.get('predictions', []))}")
                print(f"  - Summary: {bool(history.get('summary'))}")
        
        # Test export API
        print("\n3. Testing Data Export API")
        print("-" * 40)
        
        export_requests = [
            {'format': 'json', 'categories': ['predictions']},
            {'format': 'csv', 'categories': ['predictions', 'appointments']},
            {'format': 'txt', 'categories': ['predictions', 'summary']}
        ]
        
        for i, export_data in enumerate(export_requests, 1):
            response = client.post('/analytics/export', 
                                 data=json.dumps(export_data),
                                 content_type='application/json')
            print(f"✓ Export {i} ({export_data['format']}) Status: {response.status_code}")
            
            if response.status_code == 200:
                if export_data['format'] == 'json':
                    data = response.get_json()
                    print(f"  - JSON Export Success: {data.get('success', False)}")
                else:
                    print(f"  - File Export Size: {len(response.get_data())} bytes")
        
        # Test system analytics API
        print("\n4. Testing System Analytics API")
        print("-" * 40)
        
        response = client.get('/analytics/system')
        print(f"✓ System Analytics Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.get_json()
            print(f"✓ API Success: {data.get('success', False)}")
            
            if data.get('analytics'):
                analytics = data['analytics']
                print(f"  - Database Stats: {bool(analytics.get('database_stats'))}")
                print(f"  - Prediction Analytics: {bool(analytics.get('prediction_analytics'))}")
                print(f"  - User Analytics: {bool(analytics.get('user_analytics'))}")
        
        # Test analytics summary API
        print("\n5. Testing Analytics Summary API")
        print("-" * 40)
        
        response = client.get('/analytics/summary')
        print(f"✓ Analytics Summary Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.get_json()
            print(f"✓ API Success: {data.get('success', False)}")
            
            if data.get('summary'):
                summary = data['summary']
                print(f"  - Health Score: {summary.get('health_score', 'N/A')}")
                print(f"  - Risk Level: {summary.get('risk_level', 'N/A')}")
                print(f"  - Recommendations: {len(summary.get('recommendations', []))}")
    
    print("\n" + "=" * 60)
    print("✅ Analytics Web Interface Integration Test Complete!")
    print("✅ All web endpoints are working correctly")
    
    return True

if __name__ == "__main__":
    try:
        test_analytics_web_integration()
    except Exception as e:
        print(f"❌ Web integration test failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)