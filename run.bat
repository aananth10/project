@echo off
REM Urban Water Scarcity Prediction Tool - Automated Setup Script for Windows

echo.
echo ============================================
echo Urban Water Scarcity Prediction Tool
echo Automated Setup Script
echo ============================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.8+ from python.org
    pause
    exit /b 1
)

echo [1/5] Python found. Installing dependencies...
pip install -r requirements.txt
if errorlevel 1 (
    echo ERROR: Failed to install dependencies
    pause
    exit /b 1
)
echo ✓ Dependencies installed

echo.
echo [2/5] Generating synthetic data...
python data_generator.py
if errorlevel 1 (
    echo ERROR: Failed to generate data
    pause
    exit /b 1
)
echo ✓ Data generated

echo.
echo [3/5] Training ML model...
python train_model.py
if errorlevel 1 (
    echo ERROR: Failed to train model
    pause
    exit /b 1
)
echo ✓ Model trained

echo.
echo ============================================
echo Setup Complete! ✓
echo ============================================
echo.
echo [4/5] Starting Flask backend server...
echo Listening on: http://localhost:5000
echo.
echo Press Ctrl+C to stop the server
echo.

python -m flask --app backend/app run
