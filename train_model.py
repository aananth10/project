"""
ML Model Training Script
Trains a predictive model for water scarcity classification
"""

import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
import joblib
import os

# Import location data
try:
    from data_generator import LOCATIONS
except ImportError:
    # Fallback if import fails
    LOCATIONS = {}

def train_scarcity_model():
    """Train the water scarcity prediction model with location-specific data"""

    print("Loading location-based data...")
    data = pd.read_csv('data/water_scarcity_data.csv')

    print(f"Loaded data for {data['Location'].nunique()} locations: {data['Location'].unique()}")
    print(f"Total records: {len(data)}")

    # Prepare features and target with enhanced real-time features
    # Include location as a categorical feature
    feature_cols = [
        'Location', 'Rainfall_mm', 'Groundwater_Level_m', 'Water_Consumption_MLiters', 'Population',
        'Temperature_C', 'Humidity_%', 'Evaporation_mm', 'TDS_ppm', 'pH_Level',
        'Reservoir_Level_%', 'Pipeline_Pressure_bar', 'Agricultural_Usage_MLiters', 'Industrial_Usage_MLiters',
        'Soil_Moisture_%', 'Vegetation_Index', 'Water_Price_INR', 'Population_Density_per_sqkm'
    ]
    
    X = data[feature_cols]
    y = data['Risk_Level']

    # Convert categorical location to numerical
    from sklearn.preprocessing import LabelEncoder
    location_encoder = LabelEncoder()
    X['Location_encoded'] = location_encoder.fit_transform(X['Location'])

    # Select final features for training (include encoded location)
    final_feature_cols = [
        'Location_encoded', 'Rainfall_mm', 'Groundwater_Level_m', 'Water_Consumption_MLiters', 'Population',
        'Temperature_C', 'Humidity_%', 'Evaporation_mm', 'TDS_ppm', 'pH_Level',
        'Reservoir_Level_%', 'Pipeline_Pressure_bar', 'Agricultural_Usage_MLiters', 'Industrial_Usage_MLiters',
        'Soil_Moisture_%', 'Vegetation_Index', 'Water_Price_INR', 'Population_Density_per_sqkm'
    ]
    X_features = X[final_feature_cols]

    # Scale numerical features
    scaler = StandardScaler()
    numerical_cols = ['Rainfall_mm', 'Groundwater_Level_m', 'Water_Consumption_MLiters', 'Population']
    X_features[numerical_cols] = scaler.fit_transform(X_features[numerical_cols])

    # Split data
    X_train, X_test, y_train, y_test = train_test_split(
        X_features, y, test_size=0.2, random_state=42, stratify=y
    )

    print(f"Training set size: {len(X_train)}")
    print(f"Test set size: {len(X_test)}")

    # Train multiple models
    print("\nTraining Gradient Boosting model...")
    model = GradientBoostingClassifier(
        n_estimators=100,
        learning_rate=0.1,
        max_depth=6,
        random_state=42
    )
    model.fit(X_train, y_train)

    print("Training Random Forest model...")
    rf_model = RandomForestClassifier(
        n_estimators=100,
        max_depth=10,
        random_state=42,
        n_jobs=-1
    )
    rf_model.fit(X_train, y_train)

    # Evaluate
    y_pred_gb = model.predict(X_test)
    y_pred_rf = rf_model.predict(X_test)

    accuracy_gb = accuracy_score(y_test, y_pred_gb)
    accuracy_rf = accuracy_score(y_test, y_pred_rf)

    print("\n" + "="*60)
    print("GRADIENT BOOSTING MODEL RESULTS")
    print("="*60)
    print(f"Accuracy: {accuracy_gb:.4f}")
    print("\nClassification Report:")
    print(classification_report(y_test, y_pred_gb))

    print("\n" + "="*60)
    print("RANDOM FOREST MODEL RESULTS")
    print("="*60)
    print(f"Accuracy: {accuracy_rf:.4f}")
    print("\nClassification Report:")
    print(classification_report(y_test, y_pred_rf))

    # Feature importance with enhanced features
    print("\n" + "="*60)
    print("FEATURE IMPORTANCE (Enhanced Model)")
    print("="*60)
    feature_names = [
        'Location', 'Rainfall_mm', 'Groundwater_Level_m', 'Water_Consumption_MLiters', 'Population',
        'Temperature_C', 'Humidity_%', 'Evaporation_mm', 'TDS_ppm', 'pH_Level',
        'Reservoir_Level_%', 'Pipeline_Pressure_bar', 'Agricultural_Usage_MLiters', 'Industrial_Usage_MLiters',
        'Soil_Moisture_%', 'Vegetation_Index', 'Water_Price_INR', 'Population_Density_per_sqkm'
    ]
    
    # Sort features by importance
    feature_importance_pairs = list(zip(feature_names, model.feature_importances_))
    feature_importance_pairs.sort(key=lambda x: x[1], reverse=True)
    
    for name, importance in feature_importance_pairs[:10]:  # Show top 10
        print(f"{name}: {importance:.4f}")

    # Location-wise performance
    print("\n" + "="*60)
    print("LOCATION-WISE PERFORMANCE")
    print("="*60)
    test_data_with_location = X_test.copy()
    test_data_with_location['Location'] = location_encoder.inverse_transform(test_data_with_location['Location_encoded'])
    test_data_with_location['Actual'] = y_test.values
    test_data_with_location['Predicted'] = y_pred_gb

    for location in data['Location'].unique():
        loc_data = test_data_with_location[test_data_with_location['Location'] == location]
        if len(loc_data) > 0:
            loc_accuracy = accuracy_score(loc_data['Actual'], loc_data['Predicted'])
            print(f"{location}: {loc_accuracy:.3f} accuracy ({len(loc_data)} samples)")

    # Save models and encoders
    os.makedirs('models', exist_ok=True)

    joblib.dump(model, 'models/gb_model.pkl')
    joblib.dump(rf_model, 'models/rf_model.pkl')
    joblib.dump(scaler, 'models/scaler.pkl')
    joblib.dump(location_encoder, 'models/location_encoder.pkl')

    print("\n✓ Models and encoders saved to 'models/' directory")

    return model, rf_model, scaler, location_encoder

def create_prediction_function():
    """Create a function for making location-based predictions"""
    model = joblib.load('models/gb_model.pkl')
    scaler = joblib.load('models/scaler.pkl')
    location_encoder = joblib.load('models/location_encoder.pkl')

    def predict_scarcity(location, rainfall, groundwater, consumption, population,
                        temperature=25, humidity=60, evaporation=5, tds=300, ph=7.2,
                        reservoir_level=70, pipeline_pressure=3.5, agricultural_usage=10, 
                        industrial_usage=15, soil_moisture=40, vegetation_index=0.4,
                        water_price=15, population_density=5000):
        """
        Predict water scarcity risk level using enhanced real-time features
        """
        try:
            # Encode location
            location_encoded = location_encoder.transform([location])[0]

            # Prepare features with all enhanced parameters
            features = np.array([[
                location_encoded, rainfall, groundwater, consumption, population,
                temperature, humidity, evaporation, tds, ph,
                reservoir_level, pipeline_pressure, agricultural_usage, industrial_usage,
                soil_moisture, vegetation_index, water_price, population_density
            ]])

            # Scale numerical features
            features_scaled = features.copy()
            features_scaled[:, 1:] = scaler.transform(features[:, 1:])  # Scale only numerical columns

            # Make prediction
            prediction = model.predict(features_scaled)[0]

            # Get probabilities
            probabilities = model.predict_proba(features_scaled)[0]
            confidence = max(probabilities) * 100

            # Get location info
            location_info = LOCATIONS.get(location, {})

            return {
                'location': location,
                'coordinates': {'lat': location_info.get('lat'), 'lon': location_info.get('lon')},
                'climate_zone': location_info.get('climate'),
                'risk_level': prediction,
                'confidence': confidence,
                'probabilities': {
                    'Low': float(probabilities[list(model.classes_).index('Low')]) * 100,
                    'Medium': float(probabilities[list(model.classes_).index('Medium')]) * 100,
                    'High': float(probabilities[list(model.classes_).index('High')]) * 100,
                    'Critical': float(probabilities[list(model.classes_).index('Critical')]) * 100 if 'Critical' in model.classes_ else 0,
                    'Severe': float(probabilities[list(model.classes_).index('Severe')]) * 100 if 'Severe' in model.classes_ else 0
                },
                'water_sources': location_info.get('water_sources', []),
                'risk_factors': location_info.get('risk_factors', []),
                'enhanced_features_used': [
                    'Real-time Weather (Temp, Humidity, Evaporation)',
                    'Water Quality (TDS, pH)',
                    'IoT Sensors (Reservoir Level, Pipeline Pressure)',
                    'Sector Usage (Agricultural, Industrial)',
                    'Environmental (Soil Moisture, Vegetation Index)',
                    'Economic (Water Pricing)',
                    'Social (Population Density)'
                ]
            }
        except Exception as e:
            return {'error': f'Enhanced prediction failed: {str(e)}'}

    return predict_scarcity

if __name__ == '__main__':
    train_scarcity_model()
