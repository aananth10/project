@echo off
REM Complete Render Deployment Setup
REM This script prepares your project for Render hosting

echo 🚀 Setting up Enhanced Water Scarcity Tool for Render Deployment...
echo.

echo 📦 Step 1: Ensuring all dependencies are installed...
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo ❌ Failed to install dependencies
    pause
    exit /b 1
)

echo ✅ Dependencies installed
echo.

echo 📊 Step 2: Generating training data...
python data_generator.py
if %errorlevel% neq 0 (
    echo ❌ Failed to generate data
    pause
    exit /b 1
)

echo ✅ Training data generated
echo.

echo 🤖 Step 3: Training ML model...
python train_model.py
if %errorlevel% neq 0 (
    echo ❌ Failed to train model
    pause
    exit /b 1
)

echo ✅ ML model trained
echo.

echo 🔧 Step 4: Testing application locally...
python -c "from backend.app import app; print('✅ Flask app loads successfully')"
if %errorlevel% neq 0 (
    echo ❌ Flask app failed to load
    pause
    exit /b 1
)

echo ✅ Application ready for deployment
echo.

echo 📝 Step 5: Preparing for GitHub...
if not exist .git (
    echo Initializing git repository...
    git init
    git add .
    git commit -m "Ready for Render deployment: Enhanced water scarcity tool"
) else (
    echo Adding any new changes...
    git add .
    git commit -m "Updated for Render deployment" 2>nul || echo No changes to commit
)

echo ✅ Git repository ready
echo.

echo 🌐 DEPLOYMENT INSTRUCTIONS:
echo ===========================
echo.
echo 1. 📝 Create GitHub repository:
echo    - Go to: https://github.com/new
echo    - Name: enhanced-water-scarcity-tool
echo    - Make it PUBLIC
echo    - DON'T initialize with README
echo.
echo 2. 📤 Push to GitHub:
echo    - Run: push_to_github.bat
echo    - Enter your GitHub repo URL when prompted
echo.
echo 3. 🚀 Deploy on Render:
echo    - Go to: https://render.com
echo    - Create new Web Service
echo    - Connect your GitHub repo
echo    - Use these settings:
echo      * Runtime: Python 3
echo      * Build Command: pip install -r requirements.txt
echo      * Start Command: gunicorn --bind 0.0.0.0:$PORT backend.app:app --workers 2 --threads 2
echo.
echo 🎉 Your enhanced water scarcity tool will be live!
echo.

pause