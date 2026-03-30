"""
Real-Time Data Integration Module for Urban Water Scarcity Tool
Fetches live data from various APIs and IoT sensors for enhanced predictions
"""

import requests
import json
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import time
import os
from typing import Dict, List, Optional

class RealTimeDataFetcher:
    """Fetches real-time data from various sources for water scarcity prediction"""

    def __init__(self, api_keys: Dict[str, str] = None):
        self.api_keys = api_keys or {}
        self.cache = {}
        self.cache_timeout = 300  # 5 minutes

    def get_weather_data(self, lat: float, lon: float, location_name: str) -> Dict:
        """
        Fetch real-time weather data from OpenWeatherMap API
        Returns: temperature, humidity, rainfall, evaporation estimate
        """
        cache_key = f"weather_{location_name}"

        if self._is_cache_valid(cache_key):
            return self.cache[cache_key]

        try:
            api_key = self.api_keys.get('openweather', os.getenv('OPENWEATHER_API_KEY'))
            if not api_key:
                return self._get_simulated_weather(lat, lon, location_name)

            url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={api_key}&units=metric"
            response = requests.get(url, timeout=10)
            data = response.json()

            if response.status_code == 200:
                weather_data = {
                    'temperature': data['main']['temp'],
                    'humidity': data['main']['humidity'],
                    'rainfall_mm': data.get('rain', {}).get('1h', 0) * 1000,  # Convert m to mm
                    'pressure': data['main']['pressure'],
                    'wind_speed': data['wind']['speed'],
                    'cloud_cover': data['clouds']['all'],
                    'timestamp': datetime.now(),
                    'source': 'OpenWeatherMap'
                }

                # Estimate evaporation based on temperature and humidity
                weather_data['evaporation_mm'] = self._calculate_evaporation(
                    weather_data['temperature'],
                    weather_data['humidity']
                )

                self.cache[cache_key] = weather_data
                return weather_data
            else:
                print(f"OpenWeather API error: {data.get('message', 'Unknown error')}")
                return self._get_simulated_weather(lat, lon, location_name)

        except Exception as e:
            print(f"Error fetching weather data: {e}")
            return self._get_simulated_weather(lat, lon, location_name)

    def get_water_quality_data(self, lat: float, lon: float, location_name: str) -> Dict:
        """
        Fetch water quality data from various sources
        Returns: TDS, pH, turbidity, contaminants
        """
        cache_key = f"water_quality_{location_name}"

        if self._is_cache_valid(cache_key):
            return self.cache[cache_key]

        # For demo purposes, simulate water quality data
        # In production, integrate with government APIs or IoT sensors
        quality_data = {
            'tds_ppm': np.random.normal(350, 50),
            'ph_level': np.random.normal(7.2, 0.3),
            'turbidity_ntu': np.random.normal(2.5, 1.0),
            'dissolved_oxygen': np.random.normal(8.5, 1.5),
            'conductivity': np.random.normal(450, 75),
            'timestamp': datetime.now(),
            'source': 'Simulated IoT Sensors'
        }

        # Adjust based on location characteristics
        if 'Industrial' in str(LOCATIONS.get(location_name, {}).get('risk_factors', [])):
            quality_data['tds_ppm'] += np.random.normal(100, 25)
            quality_data['ph_level'] += np.random.normal(-0.2, 0.1)

        self.cache[cache_key] = quality_data
        return quality_data

    def get_reservoir_data(self, location_name: str) -> Dict:
        """
        Fetch real-time reservoir/dam level data
        In production, integrate with government hydro databases
        """
        cache_key = f"reservoir_{location_name}"

        if self._is_cache_valid(cache_key):
            return self.cache[cache_key]

        # Simulate reservoir data based on location
        location_info = LOCATIONS.get(location_name, {})
        base_level = 70

        # Adjust based on climate and time of year
        current_month = datetime.now().month
        if location_info.get('climate') == 'Tropical Monsoon':
            # Higher levels during monsoon (June-September)
            if 6 <= current_month <= 9:
                base_level += np.random.normal(15, 5)
            else:
                base_level -= np.random.normal(10, 5)

        reservoir_data = {
            'level_percentage': np.clip(base_level + np.random.normal(0, 8), 10, 95),
            'storage_volume_mcm': np.random.normal(500, 100),  # Million cubic meters
            'inflow_cusecs': np.random.normal(1000, 300),  # Cubic feet per second
            'outflow_cusecs': np.random.normal(800, 200),
            'timestamp': datetime.now(),
            'source': 'Simulated Dam Sensors'
        }

        self.cache[cache_key] = reservoir_data
        return reservoir_data

    def get_agricultural_data(self, lat: float, lon: float, location_name: str) -> Dict:
        """
        Fetch agricultural water usage and crop data
        """
        cache_key = f"agricultural_{location_name}"

        if self._is_cache_valid(cache_key):
            return self.cache[cache_key]

        location_info = LOCATIONS.get(location_name, {})
        agricultural_percentage = location_info.get('agricultural_percentage', 0.1)

        # Simulate agricultural data
        current_month = datetime.now().month
        base_usage = agricultural_percentage * 50

        # Seasonal variation (higher during planting/harvest seasons)
        if location_info.get('climate') in ['Tropical Wet and Dry', 'Semi-Arid']:
            if current_month in [6, 7, 8]:  # Monsoon planting
                base_usage *= 1.5
            elif current_month in [10, 11, 12]:  # Winter crops
                base_usage *= 1.2

        agricultural_data = {
            'water_usage_mld': base_usage + np.random.normal(0, base_usage * 0.2),
            'crop_water_requirement': np.random.normal(5, 1),  # mm/day
            'irrigation_efficiency': np.random.normal(0.7, 0.1),
            'soil_moisture_percent': np.random.normal(45, 10),
            'vegetation_index': np.random.normal(0.35, 0.1),
            'timestamp': datetime.now(),
            'source': 'Simulated Agricultural Sensors'
        }

        self.cache[cache_key] = agricultural_data
        return agricultural_data

    def get_industrial_data(self, location_name: str) -> Dict:
        """
        Fetch industrial water usage data
        """
        cache_key = f"industrial_{location_name}"

        if self._is_cache_valid(cache_key):
            return self.cache[cache_key]

        location_info = LOCATIONS.get(location_name, {})
        industrial_percentage = location_info.get('industrial_percentage', 0.15)

        # Simulate industrial data
        base_usage = industrial_percentage * 30

        # Weekly pattern (lower on weekends)
        current_day = datetime.now().weekday()
        if current_day >= 5:  # Weekend
            base_usage *= 0.7

        industrial_data = {
            'water_usage_mld': base_usage + np.random.normal(0, base_usage * 0.15),
            'recycling_rate': np.random.normal(0.4, 0.1),
            'discharge_quality_ph': np.random.normal(7.0, 0.5),
            'discharge_tds_ppm': np.random.normal(800, 200),
            'operational_hours': np.random.normal(20, 2),
            'timestamp': datetime.now(),
            'source': 'Simulated Industrial Sensors'
        }

        self.cache[cache_key] = industrial_data
        return industrial_data

    def get_satellite_data(self, lat: float, lon: float, location_name: str) -> Dict:
        """
        Fetch satellite-derived environmental data
        In production, integrate with NASA EarthData or ESA APIs
        """
        cache_key = f"satellite_{location_name}"

        if self._is_cache_valid(cache_key):
            return self.cache[cache_key]

        # Simulate satellite data
        satellite_data = {
            'soil_moisture_percent': np.random.normal(40, 8),
            'vegetation_index': np.random.normal(0.4, 0.15),
            'land_surface_temp': np.random.normal(28, 5),
            'evapotranspiration_mm': np.random.normal(4, 1.5),
            'precipitation_mm': np.random.normal(2, 3),
            'cloud_cover_percent': np.random.normal(35, 20),
            'timestamp': datetime.now(),
            'source': 'Simulated Satellite Data'
        }

        self.cache[cache_key] = satellite_data
        return satellite_data

    def get_comprehensive_realtime_data(self, location_name: str) -> Dict:
        """
        Fetch all real-time data for a location
        """
        try:
            location_info = LOCATIONS.get(location_name)
            if not location_info:
                return {'error': f'Location {location_name} not found'}

            lat, lon = location_info['lat'], location_info['lon']

            # Fetch all data sources
            weather = self.get_weather_data(lat, lon, location_name)
            water_quality = self.get_water_quality_data(lat, lon, location_name)
            reservoir = self.get_reservoir_data(location_name)
            agricultural = self.get_agricultural_data(lat, lon, location_name)
            industrial = self.get_industrial_data(location_name)
            satellite = self.get_satellite_data(lat, lon, location_name)

            # Combine into comprehensive dataset
            realtime_data = {
                'location': location_name,
                'timestamp': datetime.now(),
                'weather': weather,
                'water_quality': water_quality,
                'reservoir': reservoir,
                'agricultural': agricultural,
                'industrial': industrial,
                'satellite': satellite,
                'data_sources': [
                    weather.get('source', 'Unknown'),
                    water_quality.get('source', 'Unknown'),
                    reservoir.get('source', 'Unknown'),
                    agricultural.get('source', 'Unknown'),
                    industrial.get('source', 'Unknown'),
                    satellite.get('source', 'Unknown')
                ]
            }

            return realtime_data

        except Exception as e:
            return {'error': f'Failed to fetch comprehensive data: {str(e)}'}

    def _get_simulated_weather(self, lat: float, lon: float, location_name: str) -> Dict:
        """Generate simulated weather data when API is unavailable"""
        location_info = LOCATIONS.get(location_name, {})
        base_temp = location_info.get('avg_temp', 25)

        return {
            'temperature': base_temp + np.random.normal(0, 3),
            'humidity': location_info.get('humidity', 60) + np.random.normal(0, 10),
            'rainfall_mm': np.random.exponential(2),
            'evaporation_mm': self._calculate_evaporation(base_temp, location_info.get('humidity', 60)),
            'pressure': 1013 + np.random.normal(0, 10),
            'wind_speed': np.random.exponential(3),
            'cloud_cover': np.random.uniform(0, 100),
            'timestamp': datetime.now(),
            'source': 'Simulated Weather'
        }

    def _calculate_evaporation(self, temperature: float, humidity: float) -> float:
        """Calculate evaporation rate based on temperature and humidity"""
        base_evaporation = 4.0
        temp_factor = (temperature - 20) / 10  # Higher temp = more evaporation
        humidity_factor = (100 - humidity) / 20  # Lower humidity = more evaporation
        return max(0.5, base_evaporation + temp_factor - humidity_factor + np.random.normal(0, 0.5))

    def _is_cache_valid(self, cache_key: str) -> bool:
        """Check if cached data is still valid"""
        if cache_key not in self.cache:
            return False

        cache_time = self.cache[cache_key].get('timestamp', datetime.min)
        return (datetime.now() - cache_time).seconds < self.cache_timeout

# Import locations for reference
try:
    from data_generator import LOCATIONS
except ImportError:
    LOCATIONS = {}

def main():
    """Demo function to test real-time data fetching"""
    fetcher = RealTimeDataFetcher()

    print("Testing Real-Time Data Integration...")
    print("=" * 50)

    for location in ['Mumbai', 'Delhi', 'Bangalore']:
        print(f"\nFetching data for {location}...")
        data = fetcher.get_comprehensive_realtime_data(location)

        if 'error' in data:
            print(f"Error: {data['error']}")
            continue

        print(f"Temperature: {data['weather']['temperature']:.1f}°C")
        print(f"Reservoir Level: {data['reservoir']['level_percentage']:.1f}%")
        print(f"Water Quality TDS: {data['water_quality']['tds_ppm']:.0f} ppm")
        print(f"Agricultural Usage: {data['agricultural']['water_usage_mld']:.1f} MLD")
        print(f"Industrial Usage: {data['industrial']['water_usage_mld']:.1f} MLD")
        print(f"Soil Moisture: {data['satellite']['soil_moisture_percent']:.1f}%")

if __name__ == '__main__':
    main()