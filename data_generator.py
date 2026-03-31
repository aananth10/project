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

# Define specific locations with their characteristics - EXPANDED FOR LARGE SCALE
LOCATIONS = {
    # Major Metropolitan Cities with Multiple Areas
    'Mumbai': {
        'areas': {
            'South Mumbai': {
                'lat': 18.9220, 'lon': 72.8347, 'type': 'residential_commercial',
                'industrial_percentage': 0.15, 'agricultural_percentage': 0.02,
                'population_density': 25000, 'water_stress': 'high'
            },
            'Andheri': {
                'lat': 19.1136, 'lon': 72.8697, 'type': 'mixed_industrial',
                'industrial_percentage': 0.35, 'agricultural_percentage': 0.01,
                'population_density': 18000, 'water_stress': 'critical'
            },
            'Thane': {
                'lat': 19.2183, 'lon': 72.9781, 'type': 'industrial_suburban',
                'industrial_percentage': 0.45, 'agricultural_percentage': 0.05,
                'population_density': 12000, 'water_stress': 'high'
            },
            'Navi Mumbai': {
                'lat': 19.0330, 'lon': 73.0297, 'type': 'new_township',
                'industrial_percentage': 0.25, 'agricultural_percentage': 0.03,
                'population_density': 8000, 'water_stress': 'medium'
            }
        },
        'climate': 'Tropical Monsoon',
        'avg_rainfall': 2200,
        'population': 12442373,
        'water_sources': ['Reservoirs', 'Groundwater', 'Desalination'],
        'risk_factors': ['High Population Density', 'Industrial Use', 'Coastal Location'],
        'avg_temp': 27.5, 'humidity': 65, 'evaporation_rate': 5.2,
        'industrial_percentage': 0.30, 'agricultural_percentage': 0.03
    },
    'Delhi': {
        'areas': {
            'Connaught Place': {
                'lat': 28.6304, 'lon': 77.2177, 'type': 'central_business',
                'industrial_percentage': 0.08, 'agricultural_percentage': 0.01,
                'population_density': 15000, 'water_stress': 'critical'
            },
            'Karol Bagh': {
                'lat': 28.6517, 'lon': 77.1907, 'type': 'residential_commercial',
                'industrial_percentage': 0.12, 'agricultural_percentage': 0.02,
                'population_density': 22000, 'water_stress': 'high'
            },
            'Rohini': {
                'lat': 28.7383, 'lon': 77.0825, 'type': 'residential_suburban',
                'industrial_percentage': 0.05, 'agricultural_percentage': 0.08,
                'population_density': 10000, 'water_stress': 'medium'
            },
            'Noida': {
                'lat': 28.5355, 'lon': 77.3910, 'type': 'industrial_tech',
                'industrial_percentage': 0.40, 'agricultural_percentage': 0.03,
                'population_density': 6000, 'water_stress': 'high'
            },
            'Gurgaon': {
                'lat': 28.4595, 'lon': 77.0266, 'type': 'corporate_industrial',
                'industrial_percentage': 0.50, 'agricultural_percentage': 0.02,
                'population_density': 4000, 'water_stress': 'critical'
            }
        },
        'climate': 'Semi-Arid',
        'avg_rainfall': 800,
        'population': 30290936,
        'water_sources': ['Yamuna River', 'Groundwater', 'Canals'],
        'risk_factors': ['High Population', 'Agricultural Demand', 'Pollution'],
        'avg_temp': 25.0, 'humidity': 55, 'evaporation_rate': 6.8
    },
    'Bangalore': {
        'areas': {
            'Whitefield': {
                'lat': 12.9698, 'lon': 77.7500, 'type': 'tech_industrial',
                'industrial_percentage': 0.55, 'agricultural_percentage': 0.01,
                'population_density': 8000, 'water_stress': 'high'
            },
            'Koramangala': {
                'lat': 12.9352, 'lon': 77.6245, 'type': 'residential_commercial',
                'industrial_percentage': 0.15, 'agricultural_percentage': 0.02,
                'population_density': 12000, 'water_stress': 'medium'
            },
            'Electronic City': {
                'lat': 12.8399, 'lon': 77.6770, 'type': 'industrial_tech_park',
                'industrial_percentage': 0.70, 'agricultural_percentage': 0.01,
                'population_density': 3000, 'water_stress': 'critical'
            },
            'Jayanagar': {
                'lat': 12.9299, 'lon': 77.5824, 'type': 'residential',
                'industrial_percentage': 0.05, 'agricultural_percentage': 0.03,
                'population_density': 15000, 'water_stress': 'medium'
            }
        },
        'climate': 'Tropical Savanna',
        'avg_rainfall': 970,
        'population': 8443675,
        'water_sources': ['Cauvery River', 'Groundwater', 'Reservoirs'],
        'risk_factors': ['Rapid Urbanization', 'IT Industry', 'Seasonal Rivers'],
        'avg_temp': 24.5, 'humidity': 60, 'evaporation_rate': 4.9
    },
    'Chennai': {
        'areas': {
            'T. Nagar': {
                'lat': 13.0418, 'lon': 80.2341, 'type': 'residential_commercial',
                'industrial_percentage': 0.10, 'agricultural_percentage': 0.01,
                'population_density': 18000, 'water_stress': 'high'
            },
            'Anna Nagar': {
                'lat': 13.0850, 'lon': 80.2101, 'type': 'residential',
                'industrial_percentage': 0.08, 'agricultural_percentage': 0.02,
                'population_density': 14000, 'water_stress': 'medium'
            },
            'Guindy': {
                'lat': 13.0067, 'lon': 80.2206, 'type': 'industrial_educational',
                'industrial_percentage': 0.25, 'agricultural_percentage': 0.01,
                'population_density': 9000, 'water_stress': 'high'
            },
            'Velachery': {
                'lat': 12.9758, 'lon': 80.2205, 'type': 'residential_suburban',
                'industrial_percentage': 0.12, 'agricultural_percentage': 0.04,
                'population_density': 7000, 'water_stress': 'medium'
            }
        },
        'climate': 'Tropical Wet and Dry',
        'avg_rainfall': 1400,
        'population': 7088000,
        'water_sources': ['Reservoirs', 'Groundwater', 'Desalination'],
        'risk_factors': ['Coastal Location', 'Industrial Growth', 'Saltwater Intrusion'],
        'avg_temp': 28.5, 'humidity': 70, 'evaporation_rate': 5.8
    },
    'Hyderabad': {
        'areas': {
            'Banjara Hills': {
                'lat': 17.4156, 'lon': 78.4349, 'type': 'residential_luxury',
                'industrial_percentage': 0.05, 'agricultural_percentage': 0.01,
                'population_density': 8000, 'water_stress': 'high'
            },
            'HITEC City': {
                'lat': 17.4435, 'lon': 78.3772, 'type': 'tech_industrial',
                'industrial_percentage': 0.60, 'agricultural_percentage': 0.01,
                'population_density': 5000, 'water_stress': 'critical'
            },
            'Secunderabad': {
                'lat': 17.4399, 'lon': 78.4983, 'type': 'industrial_military',
                'industrial_percentage': 0.35, 'agricultural_percentage': 0.02,
                'population_density': 10000, 'water_stress': 'high'
            },
            'Kukatpally': {
                'lat': 17.4948, 'lon': 78.3996, 'type': 'residential_suburban',
                'industrial_percentage': 0.15, 'agricultural_percentage': 0.06,
                'population_density': 6000, 'water_stress': 'medium'
            }
        },
        'climate': 'Tropical Wet and Dry',
        'avg_rainfall': 800,
        'population': 6809970,
        'water_sources': ['Reservoirs', 'Groundwater', 'Krishna River'],
        'risk_factors': ['Rapid Growth', 'Agricultural Competition', 'Drought Prone'],
        'avg_temp': 26.5, 'humidity': 58, 'evaporation_rate': 6.5
    },
    'Pune': {
        'areas': {
            'Koregaon Park': {
                'lat': 18.5362, 'lon': 73.8940, 'type': 'residential_commercial',
                'industrial_percentage': 0.08, 'agricultural_percentage': 0.03,
                'population_density': 9000, 'water_stress': 'medium'
            },
            'Hinjewadi': {
                'lat': 18.5913, 'lon': 73.7389, 'type': 'industrial_tech_park',
                'industrial_percentage': 0.65, 'agricultural_percentage': 0.01,
                'population_density': 4000, 'water_stress': 'critical'
            },
            'Aundh': {
                'lat': 18.5625, 'lon': 73.8078, 'type': 'residential_suburban',
                'industrial_percentage': 0.10, 'agricultural_percentage': 0.05,
                'population_density': 7000, 'water_stress': 'medium'
            },
            'Chakan': {
                'lat': 18.7606, 'lon': 73.8635, 'type': 'industrial_manufacturing',
                'industrial_percentage': 0.75, 'agricultural_percentage': 0.02,
                'population_density': 3000, 'water_stress': 'high'
            }
        },
        'climate': 'Tropical Wet and Dry',
        'avg_rainfall': 720,
        'population': 3124458,
        'water_sources': ['Reservoirs', 'Groundwater', 'Rivers'],
        'risk_factors': ['Hillside Location', 'Urban Sprawl', 'Seasonal Water'],
        'avg_temp': 24.8, 'humidity': 52, 'evaporation_rate': 5.5
    },
    'Ahmedabad': {
        'areas': {
            'Navrangpura': {
                'lat': 23.0301, 'lon': 72.5714, 'type': 'residential_commercial',
                'industrial_percentage': 0.12, 'agricultural_percentage': 0.02,
                'population_density': 12000, 'water_stress': 'high'
            },
            'Vatva': {
                'lat': 22.9609, 'lon': 72.6284, 'type': 'industrial_manufacturing',
                'industrial_percentage': 0.80, 'agricultural_percentage': 0.01,
                'population_density': 5000, 'water_stress': 'critical'
            },
            'Satellite': {
                'lat': 23.0276, 'lon': 72.5161, 'type': 'residential_suburban',
                'industrial_percentage': 0.08, 'agricultural_percentage': 0.04,
                'population_density': 8000, 'water_stress': 'medium'
            },
            'Sanand': {
                'lat': 22.9923, 'lon': 72.3811, 'type': 'industrial_logistics',
                'industrial_percentage': 0.55, 'agricultural_percentage': 0.08,
                'population_density': 2000, 'water_stress': 'high'
            }
        },
        'climate': 'Arid',
        'avg_rainfall': 800,
        'population': 5570585,
        'water_sources': ['Sabarmati River', 'Groundwater', 'Narmada Canal'],
        'risk_factors': ['Arid Climate', 'Industrial Demand', 'Groundwater Depletion'],
        'avg_temp': 27.2, 'humidity': 45, 'evaporation_rate': 7.8
    },
    'Kolkata': {
        'areas': {
            'Salt Lake': {
                'lat': 22.5733, 'lon': 88.4128, 'type': 'tech_industrial',
                'industrial_percentage': 0.40, 'agricultural_percentage': 0.01,
                'population_density': 6000, 'water_stress': 'high'
            },
            'Park Street': {
                'lat': 22.5550, 'lon': 88.3508, 'type': 'central_business',
                'industrial_percentage': 0.06, 'agricultural_percentage': 0.01,
                'population_density': 15000, 'water_stress': 'critical'
            },
            'Howrah': {
                'lat': 22.5958, 'lon': 88.2636, 'type': 'industrial_transport',
                'industrial_percentage': 0.30, 'agricultural_percentage': 0.02,
                'population_density': 10000, 'water_stress': 'high'
            },
            'New Town': {
                'lat': 22.6200, 'lon': 88.4600, 'type': 'new_township',
                'industrial_percentage': 0.20, 'agricultural_percentage': 0.03,
                'population_density': 4000, 'water_stress': 'medium'
            }
        },
        'climate': 'Tropical Wet and Dry',
        'avg_rainfall': 1600,
        'population': 4486679,
        'water_sources': ['Hooghly River', 'Groundwater', 'Canals'],
        'risk_factors': ['River Pollution', 'Monsoon Flooding', 'Urban Expansion'],
        'avg_temp': 26.8, 'humidity': 75, 'evaporation_rate': 4.2
    },
    # Additional Major Cities
    'Jaipur': {
        'areas': {
            'Malviya Nagar': {
                'lat': 26.8500, 'lon': 75.8000, 'type': 'residential_commercial',
                'industrial_percentage': 0.10, 'agricultural_percentage': 0.05,
                'population_density': 6000, 'water_stress': 'high'
            },
            'Sitapura': {
                'lat': 26.7800, 'lon': 75.8500, 'type': 'industrial_logistics',
                'industrial_percentage': 0.45, 'agricultural_percentage': 0.03,
                'population_density': 3000, 'water_stress': 'critical'
            }
        },
        'climate': 'Arid',
        'avg_rainfall': 650,
        'population': 3073350,
        'water_sources': ['Groundwater', 'Canals', 'Reservoirs'],
        'risk_factors': ['Arid Climate', 'Tourism Demand', 'Groundwater Depletion'],
        'avg_temp': 26.0, 'humidity': 45, 'evaporation_rate': 7.5
    },
    'Surat': {
        'areas': {
            'Adajan': {
                'lat': 21.1900, 'lon': 72.7900, 'type': 'residential_commercial',
                'industrial_percentage': 0.15, 'agricultural_percentage': 0.02,
                'population_density': 8000, 'water_stress': 'medium'
            },
            'Sachin': {
                'lat': 21.0800, 'lon': 72.8900, 'type': 'industrial_manufacturing',
                'industrial_percentage': 0.70, 'agricultural_percentage': 0.01,
                'population_density': 2500, 'water_stress': 'critical'
            }
        },
        'climate': 'Arid',
        'avg_rainfall': 900,
        'population': 4462002,
        'water_sources': ['Tapi River', 'Groundwater', 'Canals'],
        'risk_factors': ['Industrial Pollution', 'Drought Prone', 'Coastal'],
        'avg_temp': 27.8, 'humidity': 55, 'evaporation_rate': 6.2
    },
    'Lucknow': {
        'areas': {
            'Gomti Nagar': {
                'lat': 26.8500, 'lon': 81.0000, 'type': 'residential_commercial',
                'industrial_percentage': 0.12, 'agricultural_percentage': 0.04,
                'population_density': 7000, 'water_stress': 'high'
            },
            'Amausi': {
                'lat': 26.7800, 'lon': 80.9500, 'type': 'industrial_airport',
                'industrial_percentage': 0.35, 'agricultural_percentage': 0.02,
                'population_density': 4000, 'water_stress': 'medium'
            }
        },
        'climate': 'Subtropical',
        'avg_rainfall': 1000,
        'population': 3382000,
        'water_sources': ['Gomti River', 'Groundwater', 'Canals'],
        'risk_factors': ['River Pollution', 'Urban Growth', 'Seasonal Rivers'],
        'avg_temp': 25.5, 'humidity': 60, 'evaporation_rate': 5.0
    },
    'Nagpur': {
        'areas': {
            'Dharampeth': {
                'lat': 21.1500, 'lon': 79.1000, 'type': 'residential_commercial',
                'industrial_percentage': 0.18, 'agricultural_percentage': 0.03,
                'population_density': 5000, 'water_stress': 'medium'
            },
            'Hingna': {
                'lat': 21.1000, 'lon': 79.0500, 'type': 'industrial_manufacturing',
                'industrial_percentage': 0.55, 'agricultural_percentage': 0.02,
                'population_density': 3500, 'water_stress': 'high'
            }
        },
        'climate': 'Tropical Wet and Dry',
        'avg_rainfall': 1200,
        'population': 2405665,
        'water_sources': ['Groundwater', 'Reservoirs', 'Rivers'],
        'risk_factors': ['Industrial Growth', 'Urban Expansion', 'Seasonal Water'],
        'avg_temp': 27.0, 'humidity': 50, 'evaporation_rate': 6.0
    },
    # Additional Major Cities with Industrial and Climate Focus
    'Visakhapatnam': {
        'areas': {
            'Dwaraka Nagar': {
                'lat': 17.7417, 'lon': 83.3017, 'type': 'residential_commercial',
                'industrial_percentage': 0.12, 'agricultural_percentage': 0.02,
                'population_density': 9000, 'water_stress': 'high'
            },
            'Gajuwaka': {
                'lat': 17.7000, 'lon': 83.2167, 'type': 'industrial_port',
                'industrial_percentage': 0.65, 'agricultural_percentage': 0.01,
                'population_density': 6000, 'water_stress': 'critical'
            },
            'Steel Plant Area': {
                'lat': 17.6833, 'lon': 83.2167, 'type': 'heavy_industrial',
                'industrial_percentage': 0.85, 'agricultural_percentage': 0.01,
                'population_density': 2000, 'water_stress': 'severe'
            }
        },
        'climate': 'Tropical Wet and Dry',
        'avg_rainfall': 1100,
        'population': 2035922,
        'water_sources': ['Reservoirs', 'Groundwater', 'Rivers'],
        'risk_factors': ['Heavy Industry', 'Port Operations', 'Coastal Erosion'],
        'avg_temp': 28.2, 'humidity': 70, 'evaporation_rate': 5.8
    },
    'Coimbatore': {
        'areas': {
            'RS Puram': {
                'lat': 11.0167, 'lon': 76.9667, 'type': 'residential_commercial',
                'industrial_percentage': 0.15, 'agricultural_percentage': 0.05,
                'population_density': 8000, 'water_stress': 'medium'
            },
            'Peelamedu': {
                'lat': 11.0333, 'lon': 76.9833, 'type': 'industrial_textile',
                'industrial_percentage': 0.60, 'agricultural_percentage': 0.02,
                'population_density': 5000, 'water_stress': 'high'
            },
            'Saravanampatti': {
                'lat': 11.0833, 'lon': 77.0000, 'type': 'industrial_engineering',
                'industrial_percentage': 0.70, 'agricultural_percentage': 0.01,
                'population_density': 4000, 'water_stress': 'critical'
            }
        },
        'climate': 'Tropical Wet and Dry',
        'avg_rainfall': 700,
        'population': 2158130,
        'water_sources': ['Reservoirs', 'Groundwater', 'Cauvery Canal'],
        'risk_factors': ['Textile Industry', 'Manufacturing', 'Urban Growth'],
        'avg_temp': 26.5, 'humidity': 65, 'evaporation_rate': 5.2
    },
    'Indore': {
        'areas': {
            'Vijay Nagar': {
                'lat': 22.7500, 'lon': 75.9000, 'type': 'residential_commercial',
                'industrial_percentage': 0.20, 'agricultural_percentage': 0.08,
                'population_density': 7000, 'water_stress': 'high'
            },
            'Pithampur': {
                'lat': 22.6167, 'lon': 75.6833, 'type': 'industrial_manufacturing',
                'industrial_percentage': 0.75, 'agricultural_percentage': 0.02,
                'population_density': 3000, 'water_stress': 'critical'
            },
            'Dewas': {
                'lat': 22.9667, 'lon': 76.0667, 'type': 'industrial_auto',
                'industrial_percentage': 0.55, 'agricultural_percentage': 0.05,
                'population_density': 4000, 'water_stress': 'high'
            }
        },
        'climate': 'Semi-Arid',
        'avg_rainfall': 950,
        'population': 1994397,
        'water_sources': ['Narmada River', 'Groundwater', 'Canals'],
        'risk_factors': ['Industrial Hubs', 'Agricultural Demand', 'Groundwater Depletion'],
        'avg_temp': 26.8, 'humidity': 45, 'evaporation_rate': 7.0
    },
    'Vadodara': {
        'areas': {
            'Alkapuri': {
                'lat': 22.3167, 'lon': 73.1833, 'type': 'residential_commercial',
                'industrial_percentage': 0.18, 'agricultural_percentage': 0.04,
                'population_density': 6000, 'water_stress': 'medium'
            },
            'Makarpura': {
                'lat': 22.2333, 'lon': 73.1833, 'type': 'industrial_chemical',
                'industrial_percentage': 0.80, 'agricultural_percentage': 0.01,
                'population_density': 2500, 'water_stress': 'critical'
            },
            'Waghodia': {
                'lat': 22.3000, 'lon': 73.4000, 'type': 'industrial_pharma',
                'industrial_percentage': 0.65, 'agricultural_percentage': 0.02,
                'population_density': 3500, 'water_stress': 'high'
            }
        },
        'climate': 'Semi-Arid',
        'avg_rainfall': 950,
        'population': 1829590,
        'water_sources': ['Sabarmati River', 'Groundwater', 'Narmada Canal'],
        'risk_factors': ['Chemical Industry', 'Pharmaceuticals', 'Industrial Pollution'],
        'avg_temp': 27.5, 'humidity': 50, 'evaporation_rate': 6.8
    },
    'Ludhiana': {
        'areas': {
            'Model Town': {
                'lat': 30.9000, 'lon': 75.8500, 'type': 'residential_commercial',
                'industrial_percentage': 0.25, 'agricultural_percentage': 0.15,
                'population_density': 8000, 'water_stress': 'high'
            },
            'Industrial Area': {
                'lat': 30.8833, 'lon': 75.8333, 'type': 'industrial_manufacturing',
                'industrial_percentage': 0.70, 'agricultural_percentage': 0.03,
                'population_density': 4000, 'water_stress': 'critical'
            },
            'Dugri': {
                'lat': 30.8500, 'lon': 75.8000, 'type': 'industrial_auto',
                'industrial_percentage': 0.60, 'agricultural_percentage': 0.05,
                'population_density': 5000, 'water_stress': 'high'
            }
        },
        'climate': 'Semi-Arid',
        'avg_rainfall': 650,
        'population': 1618879,
        'water_sources': ['Sutlej River', 'Groundwater', 'Canals'],
        'risk_factors': ['Manufacturing Hub', 'Agricultural Runoff', 'Groundwater Pollution'],
        'avg_temp': 24.0, 'humidity': 55, 'evaporation_rate': 6.5
    },
    'Agra': {
        'areas': {
            'Civil Lines': {
                'lat': 27.1833, 'lon': 78.0167, 'type': 'residential_tourist',
                'industrial_percentage': 0.08, 'agricultural_percentage': 0.12,
                'population_density': 9000, 'water_stress': 'critical'
            },
            'Sikandra': {
                'lat': 27.2167, 'lon': 77.9500, 'type': 'industrial_small',
                'industrial_percentage': 0.30, 'agricultural_percentage': 0.08,
                'population_density': 4000, 'water_stress': 'high'
            },
            'Fatehabad Road': {
                'lat': 27.1500, 'lon': 78.0333, 'type': 'industrial_logistics',
                'industrial_percentage': 0.40, 'agricultural_percentage': 0.06,
                'population_density': 3000, 'water_stress': 'medium'
            }
        },
        'climate': 'Semi-Arid',
        'avg_rainfall': 650,
        'population': 1585704,
        'water_sources': ['Yamuna River', 'Groundwater', 'Canals'],
        'risk_factors': ['Tourism Demand', 'River Pollution', 'Industrial Waste'],
        'avg_temp': 25.8, 'humidity': 50, 'evaporation_rate': 7.2
    },
    'Nashik': {
        'areas': {
            'College Road': {
                'lat': 19.9833, 'lon': 73.8000, 'type': 'residential_commercial',
                'industrial_percentage': 0.20, 'agricultural_percentage': 0.25,
                'population_density': 6000, 'water_stress': 'high'
            },
            'Satpur': {
                'lat': 19.9667, 'lon': 73.7833, 'type': 'industrial_winery',
                'industrial_percentage': 0.55, 'agricultural_percentage': 0.15,
                'population_density': 3500, 'water_stress': 'critical'
            },
            'Ambad': {
                'lat': 19.9500, 'lon': 73.7667, 'type': 'industrial_manufacturing',
                'industrial_percentage': 0.65, 'agricultural_percentage': 0.08,
                'population_density': 4000, 'water_stress': 'high'
            }
        },
        'climate': 'Tropical Wet and Dry',
        'avg_rainfall': 750,
        'population': 1486973,
        'water_sources': ['Godavari River', 'Groundwater', 'Reservoirs'],
        'risk_factors': ['Wine Industry', 'Manufacturing', 'Agricultural Irrigation'],
        'avg_temp': 26.2, 'humidity': 55, 'evaporation_rate': 6.0
    },
    'Faridabad': {
        'areas': {
            'Sector 15': {
                'lat': 28.3833, 'lon': 77.3167, 'type': 'residential_commercial',
                'industrial_percentage': 0.15, 'agricultural_percentage': 0.05,
                'population_density': 10000, 'water_stress': 'critical'
            },
            'Industrial Area': {
                'lat': 28.3667, 'lon': 77.3000, 'type': 'industrial_manufacturing',
                'industrial_percentage': 0.75, 'agricultural_percentage': 0.02,
                'population_density': 3000, 'water_stress': 'severe'
            },
            'Badarpur': {
                'lat': 28.5000, 'lon': 77.3000, 'type': 'industrial_power',
                'industrial_percentage': 0.60, 'agricultural_percentage': 0.03,
                'population_density': 2500, 'water_stress': 'high'
            }
        },
        'climate': 'Semi-Arid',
        'avg_rainfall': 650,
        'population': 1414050,
        'water_sources': ['Yamuna River', 'Groundwater', 'Canals'],
        'risk_factors': ['Industrial Pollution', 'Delhi Overspill', 'Groundwater Depletion'],
        'avg_temp': 25.5, 'humidity': 55, 'evaporation_rate': 6.8
    },
    'Meerut': {
        'areas': {
            'Ganga Nagar': {
                'lat': 28.9833, 'lon': 77.7000, 'type': 'residential_commercial',
                'industrial_percentage': 0.18, 'agricultural_percentage': 0.20,
                'population_density': 7000, 'water_stress': 'high'
            },
            'Partapur': {
                'lat': 28.9500, 'lon': 77.6833, 'type': 'industrial_sugar',
                'industrial_percentage': 0.50, 'agricultural_percentage': 0.25,
                'population_density': 4000, 'water_stress': 'critical'
            },
            'Modipuram': {
                'lat': 28.9333, 'lon': 77.7167, 'type': 'industrial_manufacturing',
                'industrial_percentage': 0.45, 'agricultural_percentage': 0.10,
                'population_density': 5000, 'water_stress': 'high'
            }
        },
        'climate': 'Semi-Arid',
        'avg_rainfall': 800,
        'population': 1305429,
        'water_sources': ['Ganges Canal', 'Groundwater', 'Rivers'],
        'risk_factors': ['Sugar Industry', 'Agricultural Runoff', 'Urban Pollution'],
        'avg_temp': 24.8, 'humidity': 60, 'evaporation_rate': 6.2
    }
}

EXTRA_CITIES = [
    ("Kanpur", 26.4499, 80.3319, "Semi-Arid", 800, 2765348, ["Ganges River", "Groundwater"], ["Pollution from leather tanneries", "Overpopulation"]),
    ("Srinagar", 34.0837, 74.7973, "Humid Subtropical", 720, 1180570, ["Jhelum River", "Dal Lake"], ["Rapid Urbanization", "Climate Change disrupting snowfall"]),
    ("Patna", 25.5941, 85.1376, "Humid Subtropical", 1100, 2350000, ["Ganges River", "Groundwater"], ["Poor Water Management", "Arsenic contamination"]),
    ("Bhopal", 23.2599, 77.4126, "Tropical Wet and Dry", 1100, 2371061, ["Upper Lake", "Narmada Water System"], ["Agricultural run-off", "Untreated sewage"]),
    ("Kochi", 9.9312, 76.2673, "Tropical Monsoon", 3000, 2119724, ["Periyar River", "Groundwater"], ["Saltwater Intrusion", "High Population Density"]),
    ("Thiruvananthapuram", 8.5241, 76.9366, "Tropical Monsoon", 1700, 2584752, ["Karamana River", "Groundwater"], ["Urban Sprawl", "Deforestation in Ghats"]),
    ("Madurai", 9.9252, 78.1198, "Tropical Wet and Dry", 800, 1470755, ["Vaigai River", "Groundwater"], ["River Drying", "Agricultural Over-extraction"]),
    ("Varanasi", 25.3176, 82.9739, "Humid Subtropical", 1000, 1435113, ["Ganges River", "Groundwater"], ["Tourist Influx", "Religious Gatherings", "Pollution"]),
    ("Jodhpur", 26.2389, 73.0243, "Arid", 360, 1033918, ["Indira Gandhi Canal", "Groundwater"], ["Severe Desert Conditions", "Low Rainfall", "Tourism"]),
    ("Ranchi", 23.3441, 85.3096, "Humid Subtropical", 1300, 1073440, ["Subarnarekha River", "Reservoirs"], ["Industrial Growth", "Mining impacts"]),
    ("Raipur", 21.2514, 81.6296, "Tropical Wet and Dry", 1100, 1010087, ["Mahanadi River", "Groundwater"], ["Heavy Industrial Output", "Coal Mining Runoff"]),
    ("Chandigarh", 30.7333, 76.7794, "Humid Subtropical", 1100, 1055450, ["Groundwater", "Canals"], ["High per-capita usage", "Groundwater depletion"]),
    ("Guwahati", 26.1445, 91.7362, "Humid Subtropical", 1600, 962334, ["Brahmaputra River", "Groundwater"], ["Topographical runoff", "Poor drainage infrastructure"]),
    ("Bhubaneswar", 20.2961, 85.8245, "Tropical Wet and Dry", 1500, 843402, ["Mahanadi River", "Groundwater"], ["Rapid IT Sector Growth", "Urban heating"]),
    ("Jabalpur", 23.1815, 79.9864, "Humid Subtropical", 1100, 1267564, ["Narmada River", "Groundwater"], ["Deforestation", "Agricultural usage"]),
    ("Gwalior", 26.2124, 78.1772, "Humid Subtropical", 900, 1101981, ["Tigra Dam", "Groundwater"], ["Old infrastructure", "High temperatures"]),
    ("Vijayawada", 16.5062, 80.6480, "Tropical Wet and Dry", 1000, 1476931, ["Krishna River", "Groundwater"], ["Industrial Corridors", "Aquaculture demand"]),
    ("Mysore", 12.2958, 76.6394, "Tropical Savanna", 800, 920550, ["Cauvery River", "Groundwater"], ["Tourism", "Increasing Urbanization"]),
    ("Bareilly", 28.3670, 79.4304, "Humid Subtropical", 1000, 903668, ["Ramganga River", "Groundwater"], ["Over-reliance on groundwater", "Agriculture"]),
    ("Aligarh", 27.8974, 78.0880, "Humid Subtropical", 800, 909989, ["Ganges Canal", "Groundwater"], ["Lock Industry usage", "Poor water recycling"]),
    ("Moradabad", 28.8386, 78.7733, "Humid Subtropical", 900, 889810, ["Ramganga River", "Groundwater"], ["Brass Industry pollution", "Heavy extraction"]),
    ("Gurgaon", 28.4595, 77.0266, "Semi-Arid", 700, 1153000, ["Yamuna Canal", "Groundwater"], ["Explosive Corporate Growth", "Concrete structures preventing recharge"]),
    ("Noida", 28.5355, 77.3910, "Semi-Arid", 700, 1000000, ["Yamuna River", "Groundwater"], ["IT Industry expansion", "High-rise residential strain"]),
    ("Jalandhar", 31.3260, 75.5762, "Humid Subtropical", 700, 862886, ["Groundwater", "Canals"], ["Sports/Leather Industry", "Agricultural overuse"]),
    ("Kota", 25.2138, 75.8648, "Semi-Arid", 600, 1001694, ["Chambal River", "Groundwater"], ["Education Hub Influx", "Industrial cooling"]),
    ("Dehradun", 30.3165, 78.0322, "Humid Subtropical", 2200, 714223, ["Springs", "Groundwater", "Rivers"], ["Tourism Boom", "Deforestation leading to spring drying", "Climate change"]),
    ("Jammu", 32.7266, 74.8570, "Humid Subtropical", 1000, 502197, ["Tawi River", "Groundwater"], ["Irregular monsoons", "High military/tourism presence"]),
    ("Mangalore", 12.9141, 74.8560, "Tropical Monsoon", 3400, 499486, ["Netravati River", "Groundwater"], ["Coastal Saline Intrusion", "Heavy Industrial operations (Refineries)"]),
    ("Trivandrum", 8.4855, 76.9492, "Tropical Monsoon", 1800, 957730, ["Karamana/Neyyar Rivers", "Groundwater"], ["Rapid Urbanization", "Topographical drainage issues"])
]

for city, lat, lon, clim, rain, pop, water, risks in EXTRA_CITIES:
    LOCATIONS[city] = {
        'areas': {
            f'{city} Central': {
                'lat': lat, 'lon': lon, 'type': 'residential_commercial',
                'industrial_percentage': 0.20, 'agricultural_percentage': 0.05,
                'population_density': 10000, 'water_stress': 'high'
            }
        },
        'climate': clim,
        'avg_rainfall': rain,
        'population': pop,
        'water_sources': water,
        'risk_factors': risks,
        'avg_temp': 28.0 if clim != "Humid Subtropical" else 22.0,
        'humidity': 60,
        'evaporation_rate': 6.0
    }


def generate_water_data(days=365, locations=None):
    """
    Generate synthetic water scarcity data for specific locations with enhanced real-time features
    """
    if locations is None:
        locations = list(LOCATIONS.keys())
    
    np.random.seed(42)
    
    # Create date range - REAL-TIME: Use current date minus days for recent data
    end_date = datetime.now().date()
    start_date = end_date - timedelta(days=days-1)
    dates = pd.date_range(start=start_date, end=end_date, freq='D')
    
    all_data = []
    
    for location_name in locations:
        location = LOCATIONS[location_name]
        
        print(f"Generating enhanced data for {location_name}...")
        
        # Generate data for each area within the location
        for area_name, area_info in location['areas'].items():
            # Generate area-specific features
            base_rainfall = generate_location_rainfall(location, days)
            groundwater = generate_location_groundwater(location, days)
            consumption = generate_location_consumption(location, days)
            
            # NEW: Real-time weather features
            temperature = generate_temperature(location, days)
            humidity = generate_humidity(location, days)
            evaporation = generate_evaporation(location, temperature, humidity, days)
            
            # NEW: Water quality parameters
            tds_level = generate_tds_levels(area_info, days)
            ph_level = generate_ph_levels(area_info, days)
            
            # NEW: IoT sensor data
            reservoir_level = generate_reservoir_levels(location, days)
            pipeline_pressure = generate_pipeline_pressure(location, days)
            
            # NEW: Agricultural and industrial usage
            agricultural_usage = generate_agricultural_usage(area_info, days)
            industrial_usage = generate_industrial_usage(area_info, days)
            
            # NEW: Environmental indicators
            soil_moisture = generate_soil_moisture(location, base_rainfall, days)
            vegetation_index = generate_vegetation_index(location, soil_moisture, days)
            
            # NEW: Economic and social factors
            water_price = generate_water_pricing(location, days)
            population_density = generate_population_density(area_info, days)
            
            # Population data (with growth trend)
            population_base = location['population'] * (area_info['population_density'] / sum(a['population_density'] for a in location['areas'].values()))
            population = population_base + np.linspace(0, population_base * 0.1, days) + np.random.normal(0, population_base * 0.02, days)
            
            # Calculate enhanced scarcity index
            scarcity_index = calculate_enhanced_scarcity(
                base_rainfall, groundwater, consumption, population, temperature, 
                humidity, evaporation, tds_level, reservoir_level, agricultural_usage,
                industrial_usage, soil_moisture, location
            )
            
            # Classify risk level with more granularity
            risk_levels = [classify_enhanced_risk(idx) for idx in scarcity_index]
            
            # Create area data with all new features
            area_data = pd.DataFrame({
                'Date': dates,
                'Location': f"{location_name} - {area_name}",
                'City': location_name,
                'Area': area_name,
                'Latitude': area_info['lat'],
                'Longitude': area_info['lon'],
                'Area_Type': area_info['type'],
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
            
            all_data.append(area_data)
    
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

def generate_tds_levels(area_info, days):
    """Generate Total Dissolved Solids levels (water quality indicator)"""
    base_tds = 250  # Base TDS in ppm
    
    # Industrial areas have higher TDS
    industrial_factor = area_info['industrial_percentage'] * 300
    
    # Seasonal variation (higher in dry seasons)
    seasonal_factor = np.sin(np.linspace(0, 2*np.pi, days)) * 50
    
    # Random fluctuations
    noise = np.random.normal(0, 30, days)
    
    return np.clip(base_tds + industrial_factor + seasonal_factor + noise, 50, 2000)

def generate_ph_levels(area_info, days):
    """Generate pH levels for water quality monitoring"""
    base_ph = 7.2
    
    # Industrial pollution can affect pH
    industrial_effect = area_info['industrial_percentage'] * np.random.choice([-0.5, 0.3], days)
    
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

def generate_agricultural_usage(area_info, days):
    """Generate agricultural water usage based on crop cycles"""
    base_usage = area_info['agricultural_percentage'] * 50  # Base daily usage in million liters
    
    # Crop cycle patterns (higher during planting/growth seasons)
    crop_cycle = np.sin(np.linspace(0, 2*np.pi, days)) * 15
    
    # Irrigation efficiency variations
    efficiency_factor = np.random.normal(1, 0.1, days)
    
    return np.clip((base_usage + crop_cycle) * efficiency_factor, 0, 200)

def generate_industrial_usage(area_info, days):
    """Generate industrial water usage patterns"""
    base_usage = area_info['industrial_percentage'] * 30  # Base daily usage in million liters
    
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
    scarcity_factor = location.get('industrial_percentage', 0.2) * 2  # Industrial areas pay more
    
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

def generate_population_density(area_info, days):
    """Generate population density variations"""
    base_density = area_info['population_density']
    
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
    industrial_pressure = location.get('industrial_percentage', 0.2) * 0.5
    agricultural_pressure = location.get('agricultural_percentage', 0.05) * 0.3
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
