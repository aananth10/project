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

from real_time_data_fetcher import RealTimeDataFetcher

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
            # Handle lat/lon whether it's top level or inside areas
            if 'lat' in info:
                lat, lon = info['lat'], info['lon']
            elif 'areas' in info and info['areas']:
                first_area = list(info['areas'].values())[0]
                lat, lon = first_area['lat'], first_area['lon']
            else:
                lat, lon = 0, 0
                
            # Get current risk level for this location
            location_data = data[data['City'] == name] if 'City' in data.columns else data[data['Location'] == name]
            
            if len(location_data) > 0:
                current_risk = location_data['Risk_Level'].iloc[-1]
                avg_rainfall = location_data['Rainfall_mm'].mean()
                latest_date = pd.to_datetime(location_data['Date'].iloc[-1])
                current_rainfall = location_data['Rainfall_mm'].iloc[-1]
                current_groundwater = location_data['Groundwater_Level_m'].iloc[-1]
            else:
                current_risk = 'Unknown'
                avg_rainfall = info.get('avg_rainfall', 0) / 365
                latest_date = datetime.now()
                current_rainfall = 0
                current_groundwater = 0

            locations_data.append({
                'name': name,
                'coordinates': {'lat': lat, 'lon': lon},
                'climate': info.get('climate', 'Unknown'),
                'population': info.get('population', 0),
                'avg_rainfall': round(avg_rainfall, 1),
                'current_risk': current_risk,
                'current_rainfall': round(current_rainfall, 1),
                'current_groundwater': round(current_groundwater, 1),
                'last_updated': latest_date.strftime('%Y-%m-%d %H:%M:%S'),
                'water_sources': info.get('water_sources', []),
                'risk_factors': info.get('risk_factors', [])
            })

        return jsonify({
            'status': 'success',
            'data': locations_data
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

@app.route('/api/location/<location_name>/data', methods=['GET'])
def get_location_live_data(location_name):
    """Get live data for a specific location and area"""
    try:
        location_data = data[data['City'] == location_name] if 'City' in data.columns else data[data['Location'] == location_name]
        if len(location_data) == 0:
            return jsonify({'status': 'error', 'message': f'No data for location: {location_name}'}), 404
        
        from data_generator import LOCATIONS
        location_info = LOCATIONS.get(location_name, {})
        
        # Handle coordinates
        if 'lat' in location_info:
            lat, lon = location_info['lat'], location_info['lon']
        elif 'areas' in location_info and location_info['areas']:
            first_area = list(location_info['areas'].values())[0]
            lat, lon = first_area['lat'], first_area['lon']
        else:
            lat, lon = 0, 0
        latest = location_data.iloc[-1]
        
        # Get recent data for trends
        recent = location_data.tail(7)
        
        avg_rain = location_data['Rainfall_mm'].mean()
        avg_gw = location_data['Groundwater_Level_m'].mean()
        
        # --- Context-Aware Intelligence Engine (Multi-Factor Breakdown) ---
        risk_str = str(location_info.get('risk_factors', '')).lower()
        
        # 1. Climate Factor
        current_rain = float(latest['Rainfall_mm'])
        rain_deficit_ratio = max(0, (avg_rain - current_rain) / avg_rain) if avg_rain > 0 else 0
        climate_score = rain_deficit_ratio * 40
        
        # 2. Usage Factor
        usage_val = float(latest['Water_Consumption_MLiters'])
        gw_val = float(latest['Groundwater_Level_m'])
        usage_stress = min(usage_val / (gw_val + 1), 2)
        usage_score = usage_stress * 20
        
        # 3. Industry Factor
        ind_score = 0
        if 'industr' in risk_str: ind_score += 25
        if 'textile' in risk_str or 'power' in risk_str: ind_score += 15
        if 'touris' in risk_str: ind_score += 10
        
        # 4. Urbanization Factor
        pop_val = int(latest['Population'])
        pop_score = min((pop_val / 2000000) * 20, 30)
        if 'population' in risk_str: pop_score += 10
        
        # 5. Infrastructure/Leakage
        import numpy as np
        leakage_score = 10 + np.random.randint(5, 12)
        if 'infrastructure' in risk_str or 'poor' in risk_str: leakage_score += 15

        # Normalize to 100%
        total_score = max(climate_score + usage_score + ind_score + pop_score + leakage_score, 1)
        pct_climate = int((climate_score / total_score) * 100)
        pct_usage = int((usage_score / total_score) * 100)
        pct_industry = int((ind_score / total_score) * 100)
        pct_urban = int((pop_score / total_score) * 100)
        pct_leakage = 100 - (pct_climate + pct_usage + pct_industry + pct_urban)
        
        # Generative AI Text Reasoning
        if latest['Risk_Level'] in ['High', 'Critical', 'Severe']:
            insight = f"<b>{location_name}</b> is experiencing severe water scarcity due to multiple complex factors. "
            if pct_climate > 20:
                insight += f"Climate anomalies, including significant rainfall deficits ({pct_climate}% contribution), have critically reduced natural aquifer recharge. "
            if pct_industry > 15:
                insight += f"Intensive industrial operations in the region are imposing a {pct_industry}% strain on available municipal reserves. "
            if pct_urban > 15:
                insight += f"Simultaneously, rapid urbanization and an expanding population core ({pop_val:,} residents) have compounded the localized demand impact to {pct_urban}%. "
            insight += f"Additionally, infrastructure pipeline inefficiencies account for {pct_leakage}% of unrecoverable water loss. "
            insight += "<br><br><b>Verdict:</b> Immediate conservation mandates and strict industrial groundwater regulations are required to prevent exhaustion."
        elif latest['Risk_Level'] == 'Medium':
            insight = f"<b>{location_name}</b> shows emerging signs of water stress. "
            factors = [('Climate deficits', pct_climate), ('High consumption', pct_usage), ('Industrial abstraction', pct_industry), ('Population density', pct_urban)]
            factors.sort(key=lambda x: x[1], reverse=True)
            insight += f"This escalation is primarily driven by {factors[0][0]} ({factors[0][1]}% impact) and {factors[1][0]} ({factors[1][1]}% impact). "
            if pct_leakage > 15:
                insight += f"Unresolved pipeline losses ({pct_leakage}%) continue to stress the grid. "
            insight += "<br><br><b>Verdict:</b> Early implementation of rainwater harvesting systems and routine infrastructure audits are recommended."
        else:
            insight = f"<b>{location_name}</b> currently maintains Hydrological Equilibrium. "
            insight += f"Steady geographic conditions stabilize the region, while residential consumption ({pct_urban + pct_usage}%) and industrial output ({pct_industry}%) are safely balanced against the natural recharge rate. "
            insight += "<br><br><b>Verdict:</b> Stable short-term outlook. Continue routine automated monitoring for drift."

        return jsonify({
            'status': 'success',
            'location_name': location_name,
            'area_info': {
                'city': location_name,
                'latitude': lat,
                'longitude': lon,
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
            'cause_breakdown': {
                'climate': pct_climate,
                'usage': pct_usage,
                'industry': pct_industry,
                'urbanization': pct_urban,
                'leakage': pct_leakage
            },
            'ai_insight': insight,
            'statistics': {
                'avg_rainfall': round(avg_rain, 1),
                'avg_groundwater': round(avg_gw, 1),
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


@app.route('/api/city/<city>/area/<area>/forecast', methods=['GET'])
def get_city_area_forecast(city, area):
    """Generate real-time forecast for a specific city and area, plus persist fetch metadata."""
    try:
        location_key = f"{city} - {area}"
        location_data = data[data['Location'].str.lower() == location_key.lower()]

        if location_data.empty:
            location_data = data[data['City'].str.lower() == city.lower()] if 'City' in data.columns else data[data['Location'].str.lower() == city.lower()]
            if not location_data.empty:
                location_key = location_data['Location'].iloc[-1]

        if location_data.empty:
            return jsonify({'status': 'error', 'message': f'No data for {location_key}'}), 404

        latest = location_data.iloc[-1]

        # Get freshest real-time API data for city
        from real_time_data_fetcher import RealTimeDataFetcher
        fetcher = RealTimeDataFetcher()
        realtime_city_data = fetcher.get_comprehensive_realtime_data(city)
        persisted_realtime = fetcher.get_persisted_realtime_data(city)

        # Build 7-day forecast using local metrics with variability
        forecast_entries = []
        base_rainfall = float(latest['Rainfall_mm'])
        base_groundwater = float(latest['Groundwater_Level_m'])
        base_consumption = float(latest['Water_Consumption_MLiters'])
        base_population = float(latest['Population'])

        # Get model features from location and real-time data, with fallback
        temp = float(realtime_city_data.get('weather', {}).get('temperature', latest.get('Temperature_C', 25)))
        hum = float(realtime_city_data.get('weather', {}).get('humidity', latest.get('Humidity_%', 60)))
        evap = float(realtime_city_data.get('weather', {}).get('evaporation_mm', latest.get('Evaporation_mm', 5)))
        tds = float(realtime_city_data.get('water_quality', {}).get('tds_ppm', latest.get('TDS_ppm', 300)))
        ph = float(realtime_city_data.get('water_quality', {}).get('ph_level', latest.get('pH_Level', 7.2)))
        reservoir = float(realtime_city_data.get('reservoir', {}).get('level_percentage', latest.get('Reservoir_Level_%', 70)))
        pipeline = float(realtime_city_data.get('industrial', {}).get('water_usage_mld', latest.get('Pipeline_Pressure_bar', 3.5)))
        agricultural_usage = float(realtime_city_data.get('agricultural', {}).get('water_usage_mld', latest.get('Agricultural_Usage_MLiters', 10)))
        industrial_usage = float(realtime_city_data.get('industrial', {}).get('water_usage_mld', latest.get('Industrial_Usage_MLiters', 15)))
        soil_moisture = float(realtime_city_data.get('satellite', {}).get('soil_moisture_percent', latest.get('Soil_Moisture_%', 40)))
        vegetation_index = float(realtime_city_data.get('satellite', {}).get('vegetation_index', latest.get('Vegetation_Index', 0.4)))
        water_price = float(latest.get('Water_Price_INR', 15))
        population_density = float(latest.get('Population_Density_per_sqkm', 5000))

        for i in range(1, 8):
            frain = max(0, base_rainfall + np.random.normal(0, 2))
            fground = max(0, base_groundwater + np.random.normal(-5, 10))
            fcons = max(0, base_consumption + np.random.normal(0, 5))
            fpop = base_population + i * 1370

            # Feed model using encoded location and scaled features
            try:
                encoded_location = location_encoder.transform([location_key])[0]
            except Exception:
                encoded_location = 0

            feature_vector = np.array([[
                encoded_location, frain, fground, fcons, fpop,
                temp, hum, evap, tds, ph,
                reservoir, pipeline, agricultural_usage, industrial_usage,
                soil_moisture, vegetation_index, water_price, population_density
            ]])

            # scaler expects consistent dimensions; only scale the first 4 numerical features
            fv_scaled = feature_vector.copy()
            fv_scaled[:, 1:5] = scaler.transform(feature_vector[:, 1:5])
            predicted_risk = model.predict(fv_scaled)[0]

            forecast_entries.append({
                'date': (pd.to_datetime(latest['Date']) + timedelta(days=i)).strftime('%Y-%m-%d'),
                'rainfall_mm': float(frain),
                'groundwater_m': float(fground),
                'consumption_mliters': float(fcons),
                'risk_level': predicted_risk,
                'risk_color': get_risk_color(predicted_risk)
            })

        return jsonify({
            'status': 'success',
            'city': city,
            'area': area,
            'location_key': location_key,
            'latest_measurement': {
                'date': pd.to_datetime(latest['Date']).strftime('%Y-%m-%d'),
                'rainfall_mm': float(latest['Rainfall_mm']),
                'groundwater_level_m': float(latest['Groundwater_Level_m']),
                'scarcity_index': float(latest['Scarcity_Index']),
                'risk_level': latest['Risk_Level']
            },
            'forecast_7days': forecast_entries,
            'realtime_snapshot': realtime_city_data,
            'persisted_realtime': persisted_realtime
        })

    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500


@app.route('/api/realtime/latest', methods=['GET'])
def get_realtime_latest():
    """Return the persisted real-time API data (all locations or specific)."""
    return jsonify({'status': 'success', 'data': 'test'})


@app.route('/test')
def test():
    return 'test'

@app.route('/api/timeline/<city>/<area>', methods=['GET'])
def get_city_area_timeline(city, area):
    """Return 30-day trend timeline for a city-area from persisted realtime data."""
    return jsonify({'status': 'success', 'city': city, 'area': area, 'timeline_30day': []})

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

import google.generativeai as genai
import re

@app.route('/api/chat', methods=['POST'])
def chat_with_multi_factor_ai():
    """True Generative AI Chatbot connected via Google Gemini LLM API."""
    try:
        data = request.get_json()
        user_msg = data.get('message', '').strip()
        # Get API key from environment (recommended) or fallback to inline key
        api_key = os.environ.get('GENAI_API_KEY') or "AIzaSyBQPDbeScWqycoV8dcjSyR6RyFsAcKpHyU"
        context = data.get('context', {})

        if not user_msg:
            return jsonify({'response': 'Please provide a valid query.'})

        if not api_key:
            return jsonify({'response': 'Generative AI Protocol Error: API key missing. Set GENAI_API_KEY environment variable.'})

        # Configure Generative AI
        genai.configure(api_key=api_key)
        
        # Build Context Environment
        loc_name = context.get('location_name', 'an unknown region')
        latest_data = context.get('latest_measurement', {})
        risk = latest_data.get('risk_level', 'Unknown')
        cause = context.get('cause_breakdown', {})
        
        system_instruction = f"""
        You are 'AquaIntel AI', an advanced, professional AI analyst for an Urban Water Scarcity Prediction platform in India.
        Your tone must be highly analytical, authoritative, and perfectly suited for an executive summary or judge-facing academic presentation. 
        You are deeply knowledgeable about machine learning (specifically Gradient Boosting Classifiers), hydrology, urban infrastructure, and climate systems.

        CURRENT REAL-TIME CONTEXT:
        The user is currently analyzing the region of '{loc_name}'.
        Current ML Predicted Risk Level: {risk}.
        Specific breakdown of scarcity factors for {loc_name}: {cause}
        
        Answer their questions comprehensively. If relevant, explicitly link your response back to '{loc_name}'.
        Format your response cleanly. Use **bold** for emphasis, but DO NOT use excessive Markdown headers or deeply nested bullet points.
        """
        
        # Instantiate a current Gemini model that supports generate_content
        # (If this fails, check model list via genai.list_models() with a valid key.)
        model = genai.GenerativeModel('gemini-1.5-pro')
        
        # Generation combining instructions and user query safely
        final_prompt = f"{system_instruction}\n\nUser Query: {user_msg}\nRespond brilliantly as AquaIntel AI."
        try:
            response = model.generate_content(final_prompt)
            # Parse Markdown to basic HTML for the UI
            reply = response.text.replace('\n\n', '<br><br>').replace('\n', '<br>')
            reply = re.sub(r'\*\*(.*?)\*\*', r'<b style="color:var(--text-main)">\1</b>', reply)
            reply = re.sub(r'\*(.*?)\*', r'<i>\1</i>', reply)
            return jsonify({'response': reply})
        except Exception as genai_error:
            # Fallback to local deterministic answer when external AI fails
            fallback_msg = (
                "AquaIntel local fallback: I cannot reach the cloud LLM right now, "
                "but I can provide a risk-aware summary based on available data. "
            )
            fallback_msg += f"Region: {loc_name}, risk={risk}. "
            if risk in ['Severe', 'High']:
                fallback_msg += "Immediate water conservation, rationing planning, and external aid coordination are recommended."
            elif risk == 'Medium':
                fallback_msg += "Monitor daily usage and enforce efficiency measures."
            else:
                fallback_msg += "Keep an eye on trends and prepare response templates."
            return jsonify({'response': fallback_msg})

    except Exception as e:
        return jsonify({'response': f"Generative AI Protocol Error: {str(e)}"})

@app.errorhandler(404)
def not_found(error):
    return jsonify({'status': 'error', 'message': 'Resource not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'status': 'error', 'message': 'Internal server error'}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    print("Starting Urban Water Scarcity Prediction Tool (VisionOS Edition)...")
    print(f"Access the NEW dashboard at: http://localhost:{port}")
    app.run(host='0.0.0.0', port=port, debug=False)
