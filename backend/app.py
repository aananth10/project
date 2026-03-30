"""
Flask Backend API for Urban Water Scarcity Prediction Tool
"""

from flask import Flask, jsonify, request, render_template
import pandas as pd
import numpy as np
import joblib
import os
from datetime import datetime, timedelta
import sys

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Get the project root directory
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

app = Flask(__name__, 
            template_folder=os.path.join(PROJECT_ROOT, 'frontend'),
            static_folder=os.path.join(PROJECT_ROOT, 'frontend', 'static'))

# Load models and encoders
try:
    model = joblib.load(os.path.join(PROJECT_ROOT, 'models', 'gb_model.pkl'))
    scaler = joblib.load(os.path.join(PROJECT_ROOT, 'models', 'scaler.pkl'))
    location_encoder = joblib.load(os.path.join(PROJECT_ROOT, 'models', 'location_encoder.pkl'))
    print("✓ Models and encoders loaded successfully")
except Exception as e:
    print(f"Error loading models: {e}")
    location_encoder = None

# Load data
try:
    data = pd.read_csv(os.path.join(PROJECT_ROOT, 'data', 'water_scarcity_data.csv'))
    print("✓ Data loaded successfully")
except Exception as e:
    print(f"Error loading data: {e}")

@app.route('/')
def index():
    """Serve the main dashboard"""
    return render_template('dashboard.html')

@app.route('/api/current-status', methods=['GET'])
def get_current_status():
    """Get current water scarcity status for a specific location"""
    try:
        location = request.args.get('location', None)
        
        if location:
            # Get data for specific location
            location_data = data[data['Location'] == location]
            if len(location_data) == 0:
                return jsonify({'status': 'error', 'message': f'No data for location: {location}'}), 404
            latest = location_data.iloc[-1]
        else:
            # Get latest overall data
            latest = data.iloc[-1]
        
        latest_date = pd.to_datetime(latest['Date'])
        from data_generator import LOCATIONS
        location_info = LOCATIONS.get(latest.get('Location', 'Unknown'), {})
        
        return jsonify({
            'status': 'success',
            'data': {
                'location': latest.get('Location', 'Unknown'),
                'date': latest_date.strftime('%Y-%m-%d'),
                'rainfall': float(latest['Rainfall_mm']),
                'groundwater': float(latest['Groundwater_Level_m']),
                'consumption': float(latest['Water_Consumption_MLiters']),
                'population': int(latest['Population']),
                'scarcity_index': float(latest['Scarcity_Index']),
                'risk_level': latest['Risk_Level'],
                'risk_color': get_risk_color(latest['Risk_Level']),
                'climate': location_info.get('climate', 'N/A'),
                'water_sources': location_info.get('water_sources', []),
                'risk_factors': location_info.get('risk_factors', [])
            }
        })
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/api/predict', methods=['POST'])
def predict():
    """Predict water scarcity for given parameters with enhanced real-time features"""
    try:
        data_input = request.json

        location = data_input.get('location', 'Delhi')  # Default to Delhi
        
        # Basic features (required)
        rainfall = float(data_input.get('rainfall', 10))
        groundwater = float(data_input.get('groundwater', 500))
        consumption = float(data_input.get('consumption', 50))
        population = float(data_input.get('population', 1000000))
        
        # Enhanced real-time features (optional with defaults)
        temperature = float(data_input.get('temperature', 25))
        humidity = float(data_input.get('humidity', 60))
        evaporation = float(data_input.get('evaporation', 5))
        tds = float(data_input.get('tds', 300))
        ph = float(data_input.get('ph', 7.2))
        reservoir_level = float(data_input.get('reservoir_level', 70))
        pipeline_pressure = float(data_input.get('pipeline_pressure', 3.5))
        agricultural_usage = float(data_input.get('agricultural_usage', 10))
        industrial_usage = float(data_input.get('industrial_usage', 15))
        soil_moisture = float(data_input.get('soil_moisture', 40))
        vegetation_index = float(data_input.get('vegetation_index', 0.4))
        water_price = float(data_input.get('water_price', 15))
        population_density = float(data_input.get('population_density', 5000))

        # Validate inputs
        if rainfall < 0 or groundwater < 0 or consumption < 0 or population < 0:
            return jsonify({'status': 'error', 'message': 'Invalid input values'}), 400

        # Encode location
        try:
            location_encoded = location_encoder.transform([location])[0]
        except:
            return jsonify({'status': 'error', 'message': f'Unknown location: {location}'}), 400

        # Make prediction with enhanced features
        features = np.array([[
            location_encoded, rainfall, groundwater, consumption, population,
            temperature, humidity, evaporation, tds, ph,
            reservoir_level, pipeline_pressure, agricultural_usage, industrial_usage,
            soil_moisture, vegetation_index, water_price, population_density
        ]])
        features_scaled = features.copy()
        features_scaled[:, 1:] = scaler.transform(features[:, 1:])  # Scale only numerical columns

        prediction = model.predict(features_scaled)[0]
        probabilities = model.predict_proba(features_scaled)[0]

        # Get probability breakdown
        class_labels = list(model.classes_)
        prob_dict = {label: float(probabilities[i]) * 100 for i, label in enumerate(class_labels)}

        confidence = max(probabilities) * 100

        # Get location information
        from data_generator import LOCATIONS
        location_info = LOCATIONS.get(location, {})

        return jsonify({
            'status': 'success',
            'data': {
                'location': location,
                'coordinates': {
                    'lat': location_info.get('lat'),
                    'lon': location_info.get('lon')
                },
                'climate_zone': location_info.get('climate'),
                'input': {
                    'rainfall': rainfall,
                    'groundwater': groundwater,
                    'consumption': consumption,
                    'population': int(population),
                    'temperature': temperature,
                    'humidity': humidity,
                    'evaporation': evaporation,
                    'tds': tds,
                    'ph': ph,
                    'reservoir_level': reservoir_level,
                    'pipeline_pressure': pipeline_pressure,
                    'agricultural_usage': agricultural_usage,
                    'industrial_usage': industrial_usage,
                    'soil_moisture': soil_moisture,
                    'vegetation_index': vegetation_index,
                    'water_price': water_price,
                    'population_density': population_density
                },
                'prediction': prediction,
                'confidence': confidence,
                'probabilities': prob_dict,
                'risk_color': get_risk_color(prediction),
                'recommendation': get_enhanced_recommendation(prediction, location_info),
                'water_sources': location_info.get('water_sources', []),
                'risk_factors': location_info.get('risk_factors', []),
                'enhanced_features': True
            }
        })
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/api/locations', methods=['GET'])
def get_locations():
    """Get list of available locations with their information and live data"""
    try:
        from data_generator import LOCATIONS
        locations_data = []

        for name, info in LOCATIONS.items():
            # Get current risk level for this location
            location_data = data[data['Location'] == name]
            if len(location_data) > 0:
                current_risk = location_data['Risk_Level'].iloc[-1]
                avg_rainfall = location_data['Rainfall_mm'].mean()
                latest_date = pd.to_datetime(location_data['Date'].iloc[-1])
                current_rainfall = location_data['Rainfall_mm'].iloc[-1]
                current_groundwater = location_data['Groundwater_Level_m'].iloc[-1]
            else:
                current_risk = 'Unknown'
                avg_rainfall = info['avg_rainfall'] / 365
                latest_date = datetime.now()
                current_rainfall = 0
                current_groundwater = 0

            locations_data.append({
                'name': name,
                'coordinates': {'lat': info['lat'], 'lon': info['lon']},
                'climate': info['climate'],
                'population': info['population'],
                'avg_rainfall': round(avg_rainfall, 1),
                'current_risk': current_risk,
                'current_rainfall': round(current_rainfall, 1),
                'current_groundwater': round(current_groundwater, 1),
                'last_updated': latest_date.strftime('%Y-%m-%d %H:%M:%S'),
                'water_sources': info['water_sources'],
                'risk_factors': info['risk_factors']
            })

        return jsonify({
            'status': 'success',
            'data': locations_data
        })
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/api/location/<location_name>/data', methods=['GET'])
def get_location_live_data(location_name):
    """Get live data for a specific location and area"""
    try:
        location_data = data[data['Location'] == location_name]
        if len(location_data) == 0:
            return jsonify({'status': 'error', 'message': f'No data for location: {location_name}'}), 404
        
        from data_generator import LOCATIONS
        location_info = LOCATIONS.get(location_name, {})
        latest = location_data.iloc[-1]
        
        # Get recent data for trends
        recent = location_data.tail(7)
        
        return jsonify({
            'status': 'success',
            'location_name': location_name,
            'area_info': {
                'city': location_name,
                'latitude': location_info.get('lat'),
                'longitude': location_info.get('lon'),
                'climate_zone': location_info.get('climate'),
                'population': location_info.get('population'),
                'annual_rainfall': location_info.get('avg_rainfall'),
                'water_sources': location_info.get('water_sources', []),
                'risk_factors': location_info.get('risk_factors', [])
            },
            'live_data': {
                'date': pd.to_datetime(latest['Date']).strftime('%Y-%m-%d'),
                'rainfall_mm': float(latest['Rainfall_mm']),
                'groundwater_level_m': float(latest['Groundwater_Level_m']),
                'water_consumption_mliters': float(latest['Water_Consumption_MLiters']),
                'population': int(latest['Population']),
                'scarcity_index': float(latest['Scarcity_Index']),
                'risk_level': latest['Risk_Level'],
                'risk_color': get_risk_color(latest['Risk_Level'])
            },
            'trending_data': {
                'dates': pd.to_datetime(recent['Date']).dt.strftime('%Y-%m-%d').tolist(),
                'rainfall': recent['Rainfall_mm'].tolist(),
                'groundwater': recent['Groundwater_Level_m'].tolist(),
                'risk_levels': recent['Risk_Level'].tolist()
            },
            'statistics': {
                'avg_rainfall': round(location_data['Rainfall_mm'].mean(), 1),
                'avg_groundwater': round(location_data['Groundwater_Level_m'].mean(), 1),
                'min_rainfall': round(location_data['Rainfall_mm'].min(), 1),
                'max_rainfall': round(location_data['Rainfall_mm'].max(), 1),
                'high_risk_days': int((location_data['Risk_Level'] == 'High').sum()),
                'medium_risk_days': int((location_data['Risk_Level'] == 'Medium').sum()),
                'low_risk_days': int((location_data['Risk_Level'] == 'Low').sum())
            }
        })
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/api/historical-data', methods=['GET'])
def get_historical_data():
    """Get historical data for charts"""
    try:
        days = request.args.get('days', 30, type=int)
        
        # Limit to available data
        days = min(days, len(data))
        
        recent_data = data.tail(days).copy()
        recent_data['Date'] = pd.to_datetime(recent_data['Date'])
        
        return jsonify({
            'status': 'success',
            'data': {
                'dates': recent_data['Date'].dt.strftime('%Y-%m-%d').tolist(),
                'rainfall': recent_data['Rainfall_mm'].tolist(),
                'groundwater': recent_data['Groundwater_Level_m'].tolist(),
                'consumption': recent_data['Water_Consumption_MLiters'].tolist(),
                'scarcity_index': recent_data['Scarcity_Index'].tolist(),
                'risk_levels': recent_data['Risk_Level'].tolist()
            }
        })
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/api/statistics', methods=['GET'])
def get_statistics():
    """Get statistical summary"""
    try:
        stats = {
            'status': 'success',
            'data': {
                'total_days': len(data),
                'rainfall': {
                    'avg': float(data['Rainfall_mm'].mean()),
                    'max': float(data['Rainfall_mm'].max()),
                    'min': float(data['Rainfall_mm'].min())
                },
                'groundwater': {
                    'avg': float(data['Groundwater_Level_m'].mean()),
                    'max': float(data['Groundwater_Level_m'].max()),
                    'min': float(data['Groundwater_Level_m'].min())
                },
                'consumption': {
                    'avg': float(data['Water_Consumption_MLiters'].mean()),
                    'max': float(data['Water_Consumption_MLiters'].max()),
                    'min': float(data['Water_Consumption_MLiters'].min())
                },
                'risk_distribution': {
                    'Low': int((data['Risk_Level'] == 'Low').sum()),
                    'Medium': int((data['Risk_Level'] == 'Medium').sum()),
                    'High': int((data['Risk_Level'] == 'High').sum())
                }
            }
        }
        return jsonify(stats)
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/api/forecast', methods=['GET'])
def get_forecast():
    """Generate 7-day forecast"""
    try:
        latest = data.iloc[-1]
        forecasts = []
        
        for day in range(1, 8):
            # Simple extrapolation with seasonal pattern
            rainfall = max(0, latest['Rainfall_mm'] + np.random.normal(0, 2))
            groundwater = latest['Groundwater_Level_m'] + np.random.normal(-5, 10)
            consumption = latest['Water_Consumption_MLiters'] + np.random.normal(0, 5)
            population = latest['Population'] + 1370  # Average daily growth
            
            # Make prediction
            features = np.array([[rainfall, groundwater, consumption, population]])
            features_scaled = scaler.transform(features)
            prediction = model.predict(features_scaled)[0]
            
            forecast_date = pd.to_datetime(latest['Date']) + timedelta(days=day)
            
            forecasts.append({
                'date': forecast_date.strftime('%Y-%m-%d'),
                'rainfall': float(rainfall),
                'risk_level': prediction,
                'risk_color': get_risk_color(prediction)
            })
        
        return jsonify({
            'status': 'success',
            'data': forecasts
        })
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

def get_risk_color(risk_level):
    """Get color for risk level"""
    colors = {
        'Low': '#2ecc71',      # Green
        'Medium': '#f39c12',   # Orange
        'High': '#e74c3c',     # Red
        'Critical': '#8e44ad', # Purple
        'Severe': '#2c3e50'    # Dark Blue
    }
    return colors.get(risk_level, '#95a5a6')

def get_recommendation(risk_level):
    """Get enhanced recommendation based on risk level"""
    recommendations = {
        'Low': [
            'Water supply is stable. Continue current management practices.',
            'Monitor environmental indicators regularly.',
            'Plan for upcoming seasonal variations.'
        ],
        'Medium': [
            'Implement water conservation measures immediately.',
            'Monitor consumption patterns and groundwater levels closely.',
            'Review industrial and agricultural water usage efficiency.',
            'Consider public awareness campaigns for water conservation.'
        ],
        'High': [
            'URGENT: Activate emergency water rationing protocols.',
            'Mobilize additional water sources and treatment facilities.',
            'Implement strict monitoring of water quality parameters.',
            'Coordinate with local authorities for emergency distribution.'
        ],
        'Critical': [
            'EMERGENCY: Declare water crisis and implement 50% consumption reduction.',
            'Deploy emergency water tankers and mobile treatment units.',
            'Ban all non-essential water usage including landscaping.',
            'Activate military and NGO assistance for water distribution.',
            'Monitor pipeline integrity and prevent theft/diversion.'
        ],
        'Severe': [
            'CATASTROPHE: Complete shutdown of non-critical water usage.',
            'Implement total water rationing (essential use only).',
            'Coordinate international humanitarian aid.',
            'Plan for temporary relocation of affected populations.',
            'National emergency declaration and resource mobilization.'
        ]
    }
    return recommendations.get(risk_level, ['Monitor situation closely and consult experts.'])

@app.errorhandler(404)
def not_found(error):
    return jsonify({'status': 'error', 'message': 'Resource not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'status': 'error', 'message': 'Internal server error'}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    print("Starting Urban Water Scarcity Prediction Tool...")
    print(f"Access the dashboard at: http://localhost:{port}")
    app.run(host='0.0.0.0', port=port, debug=False)
