"""
AI Healthcare Assistant - GPS Tracking Service

This module implements GPS location tracking and nearby medical facility simulation
for the healthcare assistant application.

Author: AI Healthcare Assistant Team
Date: 2024
Purpose: Academic project for healthcare AI demonstration
"""

import json
import logging
import os
import math
from typing import List, Dict, Any, Tuple, Optional
from datetime import datetime
import pandas as pd

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class GPSService:
    """
    GPS tracking and location services for healthcare assistance
    """
    
    def __init__(self):
        """Initialize GPS service with hospital data and location utilities"""
        # Initialize database manager with error handling
        self.db_manager = None
        try:
            from modules.database_manager import get_db_manager
            self.db_manager = get_db_manager()
            logger.info("Database manager loaded successfully")
        except Exception as e:
            logger.warning(f"Database manager not available: {e}")
        
        # Load hospitals data
        self.hospitals_data = self._load_hospitals_data()
        
        # Default location (City center coordinates for simulation)
        self.default_location = {
            'latitude': 40.7128,
            'longitude': -74.0060,
            'city': 'New York',
            'state': 'NY'
        }

    def _load_hospitals_data(self) -> pd.DataFrame:
        """Load hospitals data from CSV file"""
        try:
            if self.db_manager:
                return self.db_manager.load_hospitals_data()
            else:
                # Try to load directly from CSV
                csv_path = "data/hospitals.csv"
                if os.path.exists(csv_path):
                    return pd.read_csv(csv_path)
                else:
                    logger.warning("Hospitals CSV file not found, using default data")
                    return self._get_default_hospitals_data()
        except Exception as e:
            logger.error(f"Error loading hospitals data: {e}")
            return self._get_default_hospitals_data()

    def _get_default_hospitals_data(self) -> pd.DataFrame:
        """Get default hospitals data for simulation"""
        default_hospitals = [
            {
                'name': 'City General Hospital',
                'latitude': 40.7128,
                'longitude': -74.0060,
                'contact': '+1234567800',
                'emergency_services': True,
                'specialties': 'General, Emergency, Cardiology',
                'rating': 4.2
            },
            {
                'name': "St. Mary's Medical Center",
                'latitude': 40.7589,
                'longitude': -73.9851,
                'contact': '+1234567801',
                'emergency_services': True,
                'specialties': 'General, Emergency, Neurology',
                'rating': 4.5
            },
            {
                'name': 'Downtown Emergency Clinic',
                'latitude': 40.7505,
                'longitude': -73.9934,
                'contact': '+1234567802',
                'emergency_services': True,
                'specialties': 'Emergency, Urgent Care',
                'rating': 4.0
            },
            {
                'name': 'Metropolitan Health Center',
                'latitude': 40.7282,
                'longitude': -73.9942,
                'contact': '+1234567803',
                'emergency_services': False,
                'specialties': 'General, Pediatrics, Dermatology',
                'rating': 4.3
            }
        ]
        return pd.DataFrame(default_hospitals)

    def process_location(self, latitude: float, longitude: float) -> Dict[str, Any]:
        """
        Process GPS coordinates and return location information with nearby facilities
        
        Args:
            latitude: GPS latitude coordinate
            longitude: GPS longitude coordinate
            
        Returns:
            Dictionary containing location data and nearby facilities
        """
        try:
            # Validate coordinates
            if not self._validate_coordinates(latitude, longitude):
                raise ValueError("Invalid GPS coordinates")
            
            # Store location data
            location_data = {
                'latitude': latitude,
                'longitude': longitude,
                'timestamp': datetime.now().isoformat(),
                'accuracy': 'high',  # Simulated accuracy
                'source': 'html5_geolocation'
            }
            
            # Find nearby hospitals
            nearby_hospitals = self._find_nearby_hospitals(latitude, longitude)
            
            # Simulate ambulance availability
            ambulance_info = self._simulate_ambulance_availability(latitude, longitude)
            
            # Generate location summary
            location_summary = {
                'success': True,
                'coordinates': location_data,
                'nearby_hospitals': nearby_hospitals,
                'ambulance_info': ambulance_info,
                'emergency_contacts': self._get_emergency_contacts(),
                'location_quality': self._assess_location_quality(latitude, longitude)
            }
            
            # Store location for emergency reference
            self._store_location_data(location_data)
            
            logger.info(f"Processed location: {latitude}, {longitude}")
            return location_summary
            
        except Exception as e:
            logger.error(f"Error processing location: {str(e)}")
            return self._get_fallback_location_data(str(e))

    def _validate_coordinates(self, latitude: float, longitude: float) -> bool:
        """Validate GPS coordinates are within valid ranges"""
        return (-90 <= latitude <= 90) and (-180 <= longitude <= 180)

    def _find_nearby_hospitals(self, latitude: float, longitude: float, 
                              max_distance: float = 50.0, max_results: int = 5) -> List[Dict[str, Any]]:
        """
        Find hospitals within specified distance from coordinates
        
        Args:
            latitude: User's latitude
            longitude: User's longitude
            max_distance: Maximum distance in kilometers
            max_results: Maximum number of hospitals to return
            
        Returns:
            List of nearby hospitals with distance and details
        """
        nearby_hospitals = []
        
        for _, hospital in self.hospitals_data.iterrows():
            # Calculate distance
            distance = self._calculate_distance(
                latitude, longitude,
                hospital['latitude'], hospital['longitude']
            )
            
            if distance <= max_distance:
                hospital_info = {
                    'name': hospital['name'],
                    'distance_km': round(distance, 2),
                    'estimated_travel_time': self._estimate_travel_time(distance),
                    'coordinates': {
                        'latitude': hospital['latitude'],
                        'longitude': hospital['longitude']
                    },
                    'contact': hospital['contact'],
                    'emergency_services': hospital.get('emergency_services', False),
                    'specialties': hospital.get('specialties', 'General'),
                    'rating': hospital.get('rating', 0.0),
                    'directions_url': self._generate_directions_url(
                        latitude, longitude, hospital['latitude'], hospital['longitude']
                    )
                }
                nearby_hospitals.append(hospital_info)
        
        # Sort by distance and return top results
        nearby_hospitals.sort(key=lambda x: x['distance_km'])
        return nearby_hospitals[:max_results]

    def _calculate_distance(self, lat1: float, lon1: float, lat2: float, lon2: float) -> float:
        """
        Calculate distance between two GPS coordinates using Haversine formula
        
        Returns:
            Distance in kilometers
        """
        # Convert latitude and longitude from degrees to radians
        lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])
        
        # Haversine formula
        dlat = lat2 - lat1
        dlon = lon2 - lon1
        a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
        c = 2 * math.asin(math.sqrt(a))
        
        # Radius of earth in kilometers
        r = 6371
        
        return c * r

    def _estimate_travel_time(self, distance_km: float) -> str:
        """Estimate travel time based on distance"""
        # Assume average speed of 40 km/h in city traffic
        time_hours = distance_km / 40
        time_minutes = int(time_hours * 60)
        
        if time_minutes < 5:
            return "< 5 minutes"
        elif time_minutes < 60:
            return f"{time_minutes} minutes"
        else:
            hours = time_minutes // 60
            minutes = time_minutes % 60
            return f"{hours}h {minutes}m"

    def _generate_directions_url(self, from_lat: float, from_lon: float, 
                                to_lat: float, to_lon: float) -> str:
        """Generate Google Maps directions URL"""
        return (f"https://www.google.com/maps/dir/{from_lat},{from_lon}/"
                f"{to_lat},{to_lon}")

    def _simulate_ambulance_availability(self, latitude: float, longitude: float) -> Dict[str, Any]:
        """
        Simulate ambulance availability and response information
        
        Returns:
            Dictionary with ambulance availability and response details
        """
        # Simulate ambulance locations (in real app, this would be live data)
        ambulance_units = [
            {
                'unit_id': 'AMB-001',
                'latitude': latitude + 0.01,  # Nearby location
                'longitude': longitude - 0.01,
                'status': 'available',
                'crew_type': 'paramedic'
            },
            {
                'unit_id': 'AMB-002',
                'latitude': latitude - 0.02,
                'longitude': longitude + 0.015,
                'status': 'busy',
                'crew_type': 'emt'
            },
            {
                'unit_id': 'AMB-003',
                'latitude': latitude + 0.025,
                'longitude': longitude + 0.02,
                'status': 'available',
                'crew_type': 'paramedic'
            }
        ]
        
        # Find closest available ambulance
        available_ambulances = [amb for amb in ambulance_units if amb['status'] == 'available']
        
        if available_ambulances:
            closest_ambulance = min(available_ambulances, 
                                  key=lambda amb: self._calculate_distance(
                                      latitude, longitude, amb['latitude'], amb['longitude']
                                  ))
            
            distance = self._calculate_distance(
                latitude, longitude, 
                closest_ambulance['latitude'], closest_ambulance['longitude']
            )
            
            return {
                'available': True,
                'closest_unit': closest_ambulance['unit_id'],
                'distance_km': round(distance, 2),
                'estimated_arrival': self._estimate_ambulance_arrival(distance),
                'crew_type': closest_ambulance['crew_type'],
                'dispatch_number': '911',
                'status_message': f"Ambulance {closest_ambulance['unit_id']} available for dispatch"
            }
        else:
            return {
                'available': False,
                'status_message': 'All ambulances currently busy',
                'estimated_wait': '15-20 minutes',
                'dispatch_number': '911',
                'alternative': 'Consider transport to nearest hospital'
            }

    def _estimate_ambulance_arrival(self, distance_km: float) -> str:
        """Estimate ambulance arrival time"""
        # Ambulances travel faster with emergency lights (average 60 km/h)
        time_hours = distance_km / 60
        time_minutes = max(3, int(time_hours * 60))  # Minimum 3 minutes
        
        return f"{time_minutes}-{time_minutes + 2} minutes"

    def _get_emergency_contacts(self) -> Dict[str, str]:
        """Get emergency contact information"""
        return {
            'emergency_services': '911',
            'poison_control': '1-800-222-1222',
            'mental_health_crisis': '988',
            'non_emergency_medical': '311'
        }

    def _assess_location_quality(self, latitude: float, longitude: float) -> Dict[str, Any]:
        """Assess the quality and coverage of the location"""
        # Count nearby hospitals
        nearby_count = len(self._find_nearby_hospitals(latitude, longitude, max_distance=10))
        
        # Assess coverage quality
        if nearby_count >= 3:
            coverage = 'excellent'
        elif nearby_count >= 2:
            coverage = 'good'
        elif nearby_count >= 1:
            coverage = 'fair'
        else:
            coverage = 'limited'
        
        return {
            'coverage_quality': coverage,
            'nearby_facilities': nearby_count,
            'coordinates_accuracy': 'high',  # Simulated
            'location_services': 'enabled'
        }

    def _store_location_data(self, location_data: Dict[str, Any]) -> None:
        """Store location data for emergency reference"""
        try:
            if self.db_manager:
                # Use default session for now (in real app, would use actual user session)
                user_session = "default_session"
                
                self.db_manager.save_location(
                    user_session=user_session,
                    latitude=location_data['latitude'],
                    longitude=location_data['longitude'],
                    accuracy=10.0  # Default accuracy in meters
                )
                logger.info("Location data stored successfully")
            else:
                logger.info("Location data not stored (no database manager)")
        except Exception as e:
            logger.error(f"Failed to store location data: {str(e)}")

    def _get_fallback_location_data(self, error_message: str) -> Dict[str, Any]:
        """Get fallback location data when GPS fails"""
        return {
            'success': False,
            'error': error_message,
            'coordinates': {
                'latitude': self.default_location['latitude'],
                'longitude': self.default_location['longitude'],
                'timestamp': datetime.now().isoformat(),
                'accuracy': 'low',
                'source': 'fallback'
            },
            'nearby_hospitals': self._find_nearby_hospitals(
                self.default_location['latitude'], 
                self.default_location['longitude']
            ),
            'ambulance_info': {
                'available': True,
                'status_message': 'Using default location - GPS unavailable',
                'dispatch_number': '911'
            },
            'emergency_contacts': self._get_emergency_contacts(),
            'location_quality': {
                'coverage_quality': 'unknown',
                'coordinates_accuracy': 'low',
                'location_services': 'unavailable'
            },
            'error': error_message,
            'fallback_used': True
        }

    def get_location_display_data(self, latitude: float = None, longitude: float = None) -> Dict[str, Any]:
        """
        Get formatted location data for dashboard display
        
        Args:
            latitude: Optional latitude (uses default if not provided)
            longitude: Optional longitude (uses default if not provided)
            
        Returns:
            Formatted location data for UI display
        """
        try:
            # Use provided coordinates or default
            if latitude is None or longitude is None:
                latitude = self.default_location['latitude']
                longitude = self.default_location['longitude']
            
            location_info = self.process_location(latitude, longitude)
            
            # Format for display
            display_data = {
                'current_location': {
                    'latitude': latitude,
                    'longitude': longitude,
                    'formatted': f"{latitude:.4f}, {longitude:.4f}",
                    'timestamp': location_info['coordinates']['timestamp']
                },
                'nearest_hospital': None,
                'ambulance_status': location_info['ambulance_info'],
                'emergency_info': {
                    'contacts': location_info['emergency_contacts'],
                    'coverage': location_info['location_quality']['coverage_quality']
                },
                'hospitals_nearby': len(location_info['nearby_hospitals'])
            }
            
            # Add nearest hospital info
            if location_info['nearby_hospitals']:
                nearest = location_info['nearby_hospitals'][0]
                display_data['nearest_hospital'] = {
                    'name': nearest['name'],
                    'distance': f"{nearest['distance_km']} km",
                    'travel_time': nearest['estimated_travel_time'],
                    'contact': nearest['contact'],
                    'emergency_services': nearest['emergency_services']
                }
            
            return display_data
            
        except Exception as e:
            logger.error(f"Error getting location display data: {str(e)}")
            return {
                'current_location': {
                    'latitude': 0.0,
                    'longitude': 0.0,
                    'formatted': 'Location unavailable',
                    'timestamp': datetime.now().isoformat()
                },
                'nearest_hospital': None,
                'ambulance_status': {'available': False, 'status_message': 'Service unavailable'},
                'emergency_info': {'contacts': self._get_emergency_contacts(), 'coverage': 'unknown'},
                'hospitals_nearby': 0,
                'error': str(e)
            }

    def find_nearby_hospitals(self, latitude: float, longitude: float) -> List[Dict[str, Any]]:
        """
        Public method to find nearby hospitals
        
        Args:
            latitude: User's latitude
            longitude: User's longitude
            
        Returns:
            List of nearby hospitals
        """
        return self._find_nearby_hospitals(latitude, longitude)

    def get_ambulance_info(self, latitude: float, longitude: float) -> Dict[str, Any]:
        """
        Get ambulance information for location
        
        Args:
            latitude: User's latitude
            longitude: User's longitude
            
        Returns:
            Ambulance information dictionary
        """
        ambulance_info = self._simulate_ambulance_availability(latitude, longitude)
        return {
            'success': True,
            'ambulance_info': ambulance_info
        }

    def format_location_display(self, latitude: float, longitude: float) -> str:
        """
        Format location for display
        
        Args:
            latitude: Latitude coordinate
            longitude: Longitude coordinate
            
        Returns:
            Formatted location string
        """
        return f"Lat: {latitude:.4f}, Lng: {longitude:.4f}"


# Factory function for dependency injection
def get_gps_service() -> GPSService:
    """Factory function to create and return GPSService instance"""
    return GPSService()


    def find_nearby_hospitals(self, latitude: float, longitude: float) -> List[Dict[str, Any]]:
        """
        Public method to find nearby hospitals
        
        Args:
            latitude: User's latitude
            longitude: User's longitude
            
        Returns:
            List of nearby hospitals
        """
        return self._find_nearby_hospitals(latitude, longitude)

    def get_ambulance_info(self, latitude: float, longitude: float) -> Dict[str, Any]:
        """
        Get ambulance information for location
        
        Args:
            latitude: User's latitude
            longitude: User's longitude
            
        Returns:
            Ambulance information dictionary
        """
        ambulance_info = self._simulate_ambulance_availability(latitude, longitude)
        return {
            'success': True,
            'ambulance_info': ambulance_info
        }

    def format_location_display(self, latitude: float, longitude: float) -> str:
        """
        Format location for display
        
        Args:
            latitude: Latitude coordinate
            longitude: Longitude coordinate
            
        Returns:
            Formatted location string
        """
        return f"Lat: {latitude:.4f}, Lng: {longitude:.4f}"


# Factory function for dependency injection
def get_gps_service() -> GPSService:
    """Factory function to create and return GPSService instance"""
    return GPSService()


# Example usage and testing
if __name__ == "__main__":
    # Initialize GPS service
    gps_service = get_gps_service()
    
    # Test location processing
    print("=== GPS Service Test ===")
    
    # Test coordinates (New York City area)
    test_coordinates = [
        (40.7128, -74.0060),  # NYC
        (40.7589, -73.9851),  # Central Park area
        (40.6892, -74.0445)   # Statue of Liberty area
    ]
    
    for lat, lon in test_coordinates:
        print(f"\n--- Testing location: {lat}, {lon} ---")
        result = gps_service.process_location(lat, lon)
        
        print(f"Coordinates: {result['coordinates']['latitude']}, {result['coordinates']['longitude']}")
        print(f"Nearby hospitals: {len(result['nearby_hospitals'])}")
        
        if result['nearby_hospitals']:
            nearest = result['nearby_hospitals'][0]
            print(f"Nearest hospital: {nearest['name']} ({nearest['distance_km']} km)")
        
        print(f"Ambulance available: {result['ambulance_info']['available']}")
        print(f"Location quality: {result['location_quality']['coverage_quality']}")
    
    # Test display data
    print(f"\n--- Display Data Test ---")
    display_data = gps_service.get_location_display_data(40.7128, -74.0060)
    print(f"Formatted location: {display_data['current_location']['formatted']}")
    print(f"Hospitals nearby: {display_data['hospitals_nearby']}")
    
    if display_data['nearest_hospital']:
        print(f"Nearest hospital: {display_data['nearest_hospital']['name']}")
        print(f"Distance: {display_data['nearest_hospital']['distance']}")
    
    print("\nGPS Service test completed!")