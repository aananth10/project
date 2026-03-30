#!/bin/bash
# Production deployment script for Railway/Render

# Install dependencies
pip install -r requirements.txt

# Generate data if not exists
if [ ! -f "data/water_scarcity_data.csv" ]; then
    echo "Generating training data..."
    python data_generator.py
fi

# Train model if not exists
if [ ! -f "models/gb_model.pkl" ]; then
    echo "Training ML model..."
    python train_model.py
fi

# Start production server
echo "Starting production server..."
gunicorn --bind 0.0.0.0:$PORT backend.app:app --workers 2 --threads 2 --timeout 30