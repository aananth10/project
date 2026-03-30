"""
Enhanced Data Generation Script for Urban Water Scarcity Tool
Generates synthetic real-time data with advanced features for accurate predictions
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import os
import requests
import json

# Define specific locations with their characteristics
LOCATIONS = {
    'Mumbai': {
        'lat': 19.0760, 'lon': 72.8777,
        'climate': 'Tropical Monsoon',
        'avg_rainfall': 2200,  # mm/year
        'population': 12442373,
        'water_sources': ['Reservoirs', 'Groundwater', 'Desalination'],
        'risk_factors': ['High Population Density', 'Industrial Use', 'Coastal Location'],
        'avg_temp': 27.5, 'humidity': 65, 'evaporation_rate': 5.2,
        'industrial_percentage': 0.25, 'agricultural_percentage': 0.05
    },
    'Delhi': {
        'lat': 28.7041, 'lon': 77.1025,
        'climate': 'Semi-Arid',
        'avg_rainfall': 800,
        'population': 30290936,
        'water_sources': ['Yamuna River', 'Groundwater', 'Canals'],
        'risk_factors': ['High Population', 'Agricultural Demand', 'Pollution'],
        'avg_temp': 25.0, 'humidity': 55, 'evaporation_rate': 6.8,
        'industrial_percentage': 0.15, 'agricultural_percentage': 0.20
    },
    'Bangalore': {
        'lat': 12.9716, 'lon': 77.5946,
        'climate': 'Tropical Savanna',
        'avg_rainfall': 970,
        'population': 8443675,
        'water_sources': ['Cauvery River', 'Groundwater', 'Reservoirs'],
        'risk_factors': ['Rapid Urbanization', 'IT Industry', 'Seasonal Rivers'],
        'avg_temp': 24.5, 'humidity': 60, 'evaporation_rate': 4.9,
        'industrial_percentage': 0.35, 'agricultural_percentage': 0.08
    },
    'Chennai': {
        'lat': 13.0827, 'lon': 80.2707,
        'climate': 'Tropical Wet and Dry',
        'avg_rainfall': 1400,
        'population': 7088000,
        'water_sources': ['Reservoirs', 'Groundwater', 'Desalination'],
        'risk_factors': ['Coastal Location', 'Industrial Growth', 'Saltwater Intrusion'],
        'avg_temp': 28.5, 'humidity': 70, 'evaporation_rate': 5.8,
        'industrial_percentage': 0.20, 'agricultural_percentage': 0.03
    },
    'Kolkata': {
        'lat': 22.5726, 'lon': 88.3639,
        'climate': 'Tropical Wet and Dry',
        'avg_rainfall': 1600,
        'population': 4486679,
        'water_sources': ['Hooghly River', 'Groundwater', 'Canals'],
        'risk_factors': ['River Pollution', 'Monsoon Flooding', 'Urban Expansion'],
        'avg_temp': 26.8, 'humidity': 75, 'evaporation_rate': 4.2,
        'industrial_percentage': 0.18, 'agricultural_percentage': 0.12
    },
    'Hyderabad': {
        'lat': 17.3850, 'lon': 78.4867,
        'climate': 'Tropical Wet and Dry',
        'avg_rainfall': 800,
        'population': 6809970,
        'water_sources': ['Reservoirs', 'Groundwater', 'Krishna River'],
        'risk_factors': ['Rapid Growth', 'Agricultural Competition', 'Drought Prone'],
        'avg_temp': 26.5, 'humidity': 58, 'evaporation_rate': 6.5,
        'industrial_percentage': 0.22, 'agricultural_percentage': 0.15
    },
    'Ahmedabad': {
        'lat': 23.0225, 'lon': 72.5714,
        'climate': 'Arid',
        'avg_rainfall': 800,
        'population': 5570585,
        'water_sources': ['Sabarmati River', 'Groundwater', 'Narmada Canal'],
        'risk_factors': ['Arid Climate', 'Industrial Demand', 'Groundwater Depletion'],
        'avg_temp': 27.2, 'humidity': 45, 'evaporation_rate': 7.8,
        'industrial_percentage': 0.28, 'agricultural_percentage': 0.25
    },
    'Pune': {
        'lat': 18.5204, 'lon': 73.8567,
        'climate': 'Tropical Wet and Dry',
        'avg_rainfall': 720,
        'population': 3124458,
        'water_sources': ['Reservoirs', 'Groundwater', 'Rivers'],
        'risk_factors': ['Hillside Location', 'Urban Sprawl', 'Seasonal Water'],
        'avg_temp': 24.8, 'humidity': 52, 'evaporation_rate': 5.5,
        'industrial_percentage': 0.30, 'agricultural_percentage': 0.10
    }
}

def generate_water_data(days=365, locations=None):
    """
    Generate synthetic water scarcity data for specific locations with enhanced real-time features
    """
    if locations is None:
        locations = list(LOCATIONS.keys())
    
    np.random.seed(42)
    
    # Create date range
    dates = pd.date_range(start='2023-01-01', periods=days, freq='D')
    
    all_data = []
    
    for location_name in locations:
        location = LOCATIONS[location_name]
        
        print(f"Generating enhanced data for {location_name}...")
        
        # Generate location-specific features
        base_rainfall = generate_location_rainfall(location, days)
        groundwater = generate_location_groundwater(location, days)
        consumption = generate_location_consumption(location, days)
        
        # NEW: Real-time weather features
        temperature = generate_temperature(location, days)
        humidity = generate_humidity(location, days)
        evaporation = generate_evaporation(location, temperature, humidity, days)
        
        # NEW: Water quality parameters
        tds_level = generate_tds_levels(location, days)
        ph_level = generate_ph_levels(location, days)
        
        # NEW: IoT sensor data
        reservoir_level = generate_reservoir_levels(location, days)
        pipeline_pressure = generate_pipeline_pressure(location, days)
        
        # NEW: Agricultural and industrial usage
        agricultural_usage = generate_agricultural_usage(location, days)
        industrial_usage = generate_industrial_usage(location, days)
        
        # NEW: Environmental indicators
        soil_moisture = generate_soil_moisture(location, base_rainfall, days)
        vegetation_index = generate_vegetation_index(location, soil_moisture, days)
        
        # NEW: Economic and social factors
        water_price = generate_water_pricing(location, days)
        population_density = generate_population_density(location, days)
        
        # Population data (with growth trend)
        population_base = location['population']
        population = population_base + np.linspace(0, population_base * 0.1, days) + np.random.normal(0, population_base * 0.02, days)
        
        # Calculate enhanced scarcity index
        scarcity_index = calculate_enhanced_scarcity(
            base_rainfall, groundwater, consumption, population, temperature, 
            humidity, evaporation, tds_level, reservoir_level, agricultural_usage,
            industrial_usage, soil_moisture, location
        )
        
        # Classify risk level with more granularity
        risk_levels = [classify_enhanced_risk(idx) for idx in scarcity_index]
        
        # Create location data with all new features
        location_data = pd.DataFrame({
            'Date': dates,
            'Location': location_name,
            'Latitude': location['lat'],
            'Longitude': location['lon'],
            'Climate_Zone': location['climate'],
            
            # Original features
            'Rainfall_mm': base_rainfall,
            'Groundwater_Level_m': groundwater,
            'Water_Consumption_MLiters': consumption,
            'Population': population.astype(int),
            
            # NEW: Real-time weather features
            'Temperature_C': temperature,
            'Humidity_%': humidity,
            'Evaporation_mm': evaporation,
            
            # NEW: Water quality
            'TDS_ppm': tds_level,
            'pH_Level': ph_level,
            
            # NEW: IoT sensor data
            'Reservoir_Level_%': reservoir_level,
            'Pipeline_Pressure_bar': pipeline_pressure,
            
            # NEW: Sector-specific usage
            'Agricultural_Usage_MLiters': agricultural_usage,
            'Industrial_Usage_MLiters': industrial_usage,
            
            # NEW: Environmental indicators
            'Soil_Moisture_%': soil_moisture,
            'Vegetation_Index': vegetation_index,
            
            # NEW: Economic factors
            'Water_Price_INR': water_price,
            'Population_Density_per_sqkm': population_density,
            
            # Calculated outputs
            'Scarcity_Index': scarcity_index,
            'Risk_Level': risk_levels,
            'Water_Sources': str(location['water_sources']),
            'Risk_Factors': str(location['risk_factors'])
        })
        
        all_data.append(location_data)
    
    # Combine all locations
    final_df = pd.concat(all_data, ignore_index=True)
    return final_df

def generate_location_rainfall(location, days):
    """Generate rainfall data specific to location's climate"""
    base_rainfall = location['avg_rainfall'] / 365  # Daily average
    
    if location['climate'] == 'Tropical Monsoon':
        # Heavy monsoon rains, dry rest of year
        seasonal_pattern = np.sin(np.linspace(0, 4*np.pi, days)) * 0.8
        rainfall = base_rainfall * (1 + seasonal_pattern) + np.random.exponential(scale=5, size=days)
    elif location['climate'] == 'Semi-Arid':
        # Low rainfall, some seasonal variation
        seasonal_pattern = np.sin(np.linspace(0, 2*np.pi, days)) * 0.3
        rainfall = base_rainfall * (1 + seasonal_pattern) + np.random.exponential(scale=2, size=days)
    elif location['climate'] == 'Arid':
        # Very low rainfall
        rainfall = np.random.exponential(scale=3, size=days) + base_rainfall * 0.5
    else:  # Tropical Wet and Dry, Tropical Savanna
        # Moderate seasonal variation
        seasonal_pattern = np.sin(np.linspace(0, 4*np.pi, days)) * 0.5
        rainfall = base_rainfall * (1 + seasonal_pattern) + np.random.exponential(scale=4, size=days)
    
    return np.clip(rainfall, 0, 150)

def generate_location_groundwater(location, days):
    """Generate groundwater levels based on location characteristics"""
    base_level = 500
    
    if 'Groundwater' in location['water_sources']:
        # Locations with good groundwater have more stable levels
        seasonal_factor = np.sin(np.linspace(0, 4*np.pi, days)) * 100
        groundwater = base_level + seasonal_factor + np.random.normal(0, 30, days)
    else:
        # Locations dependent on surface water have more variable groundwater
        seasonal_factor = np.sin(np.linspace(0, 4*np.pi, days)) * 150
        groundwater = base_level + seasonal_factor + np.random.normal(0, 50, days)
    
    # Adjust for arid climates
    if location['climate'] == 'Arid':
        groundwater = groundwater * 0.7  # Lower groundwater in arid areas
    
    return np.clip(groundwater, 50, 800)

def generate_temperature(location, days):
    """Generate temperature data based on location and season"""
    base_temp = location['avg_temp']
    seasonal_variation = 8 * np.sin(np.linspace(0, 2*np.pi, days))  # Annual cycle
    daily_variation = np.random.normal(0, 2, days)  # Daily fluctuations
    return np.clip(base_temp + seasonal_variation + daily_variation, 15, 45)

def generate_humidity(location, days):
    """Generate humidity data based on location climate"""
    base_humidity = location['humidity']
    seasonal_factor = np.sin(np.linspace(0, 2*np.pi, days)) * 10
    monsoon_effect = np.where(np.sin(np.linspace(0, 4*np.pi, days)) > 0.5, 15, 0)  # Monsoon boost
    return np.clip(base_humidity + seasonal_factor + monsoon_effect + np.random.normal(0, 5, days), 20, 95)

def generate_evaporation(location, temperature, humidity, days):
    """Calculate evaporation rate based on temperature and humidity"""
    base_evaporation = location['evaporation_rate']
    temp_factor = (temperature - 20) * 0.1  # Higher temp = more evaporation
    humidity_factor = (100 - humidity) * 0.02  # Lower humidity = more evaporation
    return np.clip(base_evaporation + temp_factor + humidity_factor + np.random.normal(0, 0.5, days), 1, 12)

def generate_tds_levels(location, days):
    """Generate Total Dissolved Solids levels (water quality indicator)"""
    base_tds = 250  # Base TDS in ppm
    
    # Industrial areas have higher TDS
    industrial_factor = location['industrial_percentage'] * 300
    
    # Seasonal variation (higher in dry seasons)
    seasonal_factor = np.sin(np.linspace(0, 2*np.pi, days)) * 50
    
    # Random fluctuations
    noise = np.random.normal(0, 30, days)
    
    return np.clip(base_tds + industrial_factor + seasonal_factor + noise, 50, 2000)

def generate_ph_levels(location, days):
    """Generate pH levels for water quality monitoring"""
    base_ph = 7.2
    
    # Industrial pollution can affect pH
    industrial_effect = location['industrial_percentage'] * np.random.choice([-0.5, 0.3], days)
    
    # Seasonal variation
    seasonal_effect = np.sin(np.linspace(0, 2*np.pi, days)) * 0.2
    
    return np.clip(base_ph + industrial_effect + seasonal_effect + np.random.normal(0, 0.1, days), 6.0, 8.5)

def generate_reservoir_levels(location, days):
    """Generate reservoir water levels as percentage"""
    base_level = 70  # Starting level
    
    # Seasonal patterns based on rainfall
    seasonal_pattern = np.sin(np.linspace(0, 4*np.pi, days)) * 20
    
    # Depletion over time (consumption)
    depletion = np.linspace(0, -15, days)
    
    # Random fluctuations
    noise = np.random.normal(0, 5, days)
    
    return np.clip(base_level + seasonal_pattern + depletion + noise, 10, 95)

def generate_pipeline_pressure(location, days):
    """Generate pipeline pressure readings"""
    base_pressure = 3.5  # Base pressure in bar
    
    # Time of day variation (higher during peak hours)
    daily_pattern = np.sin(np.linspace(0, 4*np.pi, days)) * 0.5
    
    # Seasonal variation
    seasonal_pattern = np.sin(np.linspace(0, 2*np.pi, days)) * 0.3
    
    # Random fluctuations and potential leaks
    noise = np.random.normal(0, 0.2, days)
    
    return np.clip(base_pressure + daily_pattern + seasonal_pattern + noise, 1.5, 6.0)

def generate_agricultural_usage(location, days):
    """Generate agricultural water usage based on crop cycles"""
    base_usage = location['agricultural_percentage'] * 50  # Base daily usage in million liters
    
    # Crop cycle patterns (higher during planting/growth seasons)
    crop_cycle = np.sin(np.linspace(0, 2*np.pi, days)) * 15
    
    # Irrigation efficiency variations
    efficiency_factor = np.random.normal(1, 0.1, days)
    
    return np.clip((base_usage + crop_cycle) * efficiency_factor, 0, 200)

def generate_industrial_usage(location, days):
    """Generate industrial water usage patterns"""
    base_usage = location['industrial_percentage'] * 30  # Base daily usage in million liters
    
    # Industrial production cycles (weekday vs weekend)
    weekly_pattern = np.sin(np.linspace(0, 12.57, days)) * 5  # 2 weeks cycle
    
    # Economic factors affecting production
    economic_factor = 1 + np.random.normal(0, 0.1, days)
    
    return np.clip((base_usage + weekly_pattern) * economic_factor, 0, 150)

def generate_soil_moisture(location, rainfall, days):
    """Generate soil moisture levels based on rainfall and evaporation"""
    base_moisture = 40  # Base soil moisture percentage
    
    # Rainfall impact (with lag effect)
    rainfall_effect = np.convolve(rainfall, np.ones(3)/3, mode='same') * 0.1
    
    # Evaporation reduces moisture
    evaporation_effect = -location['evaporation_rate'] * 0.5
    
    # Seasonal patterns
    seasonal_pattern = np.sin(np.linspace(0, 4*np.pi, days)) * 10
    
    return np.clip(base_moisture + rainfall_effect + evaporation_effect + seasonal_pattern + np.random.normal(0, 5, days), 5, 80)

def generate_vegetation_index(location, soil_moisture, days):
    """Generate NDVI-like vegetation index"""
    base_index = 0.4
    
    # Soil moisture correlation
    moisture_effect = (soil_moisture - 40) * 0.005
    
    # Seasonal vegetation growth
    seasonal_growth = np.sin(np.linspace(0, 2*np.pi, days)) * 0.2
    
    # Climate-specific adjustments
    if location['climate'] == 'Arid':
        base_index -= 0.1
    elif location['climate'] == 'Tropical Monsoon':
        base_index += 0.1
    
    return np.clip(base_index + moisture_effect + seasonal_growth + np.random.normal(0, 0.05, days), 0.1, 0.8)

def generate_water_pricing(location, days):
    """Generate water pricing data (cost per cubic meter)"""
    base_price = 15  # Base price in INR per cubic meter
    
    # Seasonal pricing (higher in dry seasons)
    seasonal_adjustment = np.sin(np.linspace(0, 2*np.pi, days)) * 3
    
    # Scarcity-based pricing
    scarcity_factor = location['industrial_percentage'] * 2  # Industrial areas pay more
    
    # Market fluctuations
    market_noise = np.random.normal(0, 1, days)
    
    return np.clip(base_price + seasonal_adjustment + scarcity_factor + market_noise, 8, 35)

def generate_location_consumption(location, days):
    """Generate water consumption based on population and usage patterns"""
    population_factor = location['population'] / 1000000  # Normalize by million

    # Base consumption per million people (in million liters per day)
    base_consumption = 2.0 * population_factor  # Higher consumption - 2 million liters per million people

    # Seasonal variation (higher in summer)
    seasonal_factor = np.sin(np.linspace(0, 4*np.pi, days)) * 0.3
    consumption = base_consumption + seasonal_factor + np.random.normal(0, 0.1, days)

    # Adjust for industrial areas
    if 'Industrial' in str(location['risk_factors']):
        consumption = consumption * 1.3

    return np.clip(consumption, 0.5, 10.0)  # Higher range

def generate_population_density(location, days):
    """Generate population density variations"""
    base_density = location['population'] / 100000  # People per sq km (approximate)
    
    # Urban growth trends
    growth_trend = np.linspace(0, base_density * 0.05, days)
    
    # Seasonal variations (tourism, migration)
    seasonal_variation = np.sin(np.linspace(0, 2*np.pi, days)) * (base_density * 0.02)
    
    return base_density + growth_trend + seasonal_variation + np.random.normal(0, base_density * 0.01, days)

def calculate_enhanced_scarcity(rainfall, groundwater, consumption, population, temperature, 
                              humidity, evaporation, tds_level, reservoir_level, agricultural_usage,
                              industrial_usage, soil_moisture, location):
    """
    Calculate enhanced scarcity index using multiple real-time factors
    """
    # Convert everything to million liters per day equivalent
    rainfall_volume = rainfall * 0.001  # mm to million liters (assuming 1 sq km area)
    groundwater_volume = groundwater * 0.01  # meters to million liters equivalent
    reservoir_volume = reservoir_level * 0.1  # Reservoir level % to volume equivalent
    
    # Available water = rainfall + groundwater + reservoir
    available_water = rainfall_volume + groundwater_volume + reservoir_volume
    
    # Total demand = domestic consumption + agricultural + industrial
    total_demand = consumption + agricultural_usage + industrial_usage
    
    # Environmental factors affecting water availability
    evaporation_loss = evaporation * 0.001  # Convert to million liters
    available_water = available_water - evaporation_loss
    
    # Water quality factor (higher TDS = lower usable water)
    quality_factor = 1 - (tds_level - 200) / 1800  # TDS above 200ppm reduces usability
    quality_factor = np.clip(quality_factor, 0.5, 1.0)
    available_water = available_water * quality_factor
    
    # Soil moisture factor (affects groundwater recharge)
    soil_factor = 1 + (soil_moisture - 40) / 100  # Better soil moisture = better recharge
    available_water = available_water * soil_factor
    
    # Temperature and humidity effects
    temp_factor = 1 + (temperature - 25) / 50  # Higher temp = more demand
    humidity_factor = 1 - (humidity - 50) / 100  # Higher humidity = less evaporation loss
    total_demand = total_demand * temp_factor * humidity_factor
    
    # Population density factor (higher density = more efficient distribution losses)
    density_factor = 1 + (location['population'] / 10000000)  # Normalize population
    total_demand = total_demand * density_factor
    
    # Location-specific adjustment factors
    scarcity_multiplier = 1.0

    if location['climate'] == 'Arid':
        scarcity_multiplier = 1.8  # Higher risk in arid areas
    elif location['climate'] == 'Tropical Monsoon':
        scarcity_multiplier = 0.8  # Lower risk with monsoon
    elif 'Coastal Location' in location['risk_factors']:
        scarcity_multiplier = 1.4  # Saltwater intrusion risk
    elif 'Rapid Urbanization' in location['risk_factors']:
        scarcity_multiplier = 1.3  # Urban growth pressure
    
    # Industrial and agricultural pressure
    industrial_pressure = location['industrial_percentage'] * 0.5
    agricultural_pressure = location['agricultural_percentage'] * 0.3
    scarcity_multiplier += industrial_pressure + agricultural_pressure
    
    # Calculate scarcity ratio (demand / supply)
    scarcity_index = (total_demand / (available_water + 0.01)) * scarcity_multiplier

    return scarcity_index

def classify_enhanced_risk(index):
    """Classify risk level with more granularity using enhanced features"""
    if index < 0.7:
        return 'Low'
    elif index < 1.2:
        return 'Medium'
    elif index < 2.0:
        return 'High'
    elif index < 3.0:
        return 'Critical'
    else:
        return 'Severe'

def save_data(df, filename='water_scarcity_data.csv'):
    """Save data to CSV"""
    filepath = os.path.join('data', filename)
    df.to_csv(filepath, index=False)
    print(f"✓ Data saved to {filepath}")
    return filepath

if __name__ == '__main__':
    print("Generating location-specific water scarcity data...")
    data = generate_water_data(days=365)
    save_data(data)
    print(f"\nData shape: {data.shape}")
    print(f"\nLocations included: {data['Location'].unique()}")
    print(f"\nRisk Level Distribution:\n{data['Risk_Level'].value_counts()}")
    print(f"\nSample data by location:")
    for location in data['Location'].unique()[:3]:  # Show first 3 locations
        location_data = data[data['Location'] == location]
        print(f"\n{location}:")
        print(f"  Average Rainfall: {location_data['Rainfall_mm'].mean():.1f} mm/day")
        print(f"  Risk Distribution: {location_data['Risk_Level'].value_counts().to_dict()}")
        print(f"  Population: {location_data['Population'].iloc[0]:,}")
