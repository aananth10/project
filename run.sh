#!/bin/bash
# Urban Water Scarcity Prediction Tool - Automated Setup Script for Linux/Mac

echo ""
echo "============================================"
echo "Urban Water Scarcity Prediction Tool"
echo "Automated Setup Script"
echo "============================================"
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python3 is not installed"
    echo "Please install Python 3.8+ first"
    exit 1
fi

echo "[1/5] Python found. Installing dependencies..."
pip install -r requirements.txt
if [ $? -ne 0 ]; then
    echo "ERROR: Failed to install dependencies"
    exit 1
fi
echo "✓ Dependencies installed"

echo ""
echo "[2/5] Generating synthetic data..."
python3 data_generator.py
if [ $? -ne 0 ]; then
    echo "ERROR: Failed to generate data"
    exit 1
fi
echo "✓ Data generated"

echo ""
echo "[3/5] Training ML model..."
python3 train_model.py
if [ $? -ne 0 ]; then
    echo "ERROR: Failed to train model"
    exit 1
fi
echo "✓ Model trained"

echo ""
echo "============================================"
echo "Setup Complete! ✓"
echo "============================================"
echo ""
echo "[4/5] Starting Flask backend server..."
echo "Listening on: http://localhost:5000"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

python3 -m flask --app backend/app run
