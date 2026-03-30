@echo off
REM GitHub Push Script for Render Deployment
REM Run this AFTER creating your GitHub repository

echo 🚀 Pushing Enhanced Water Scarcity Tool to GitHub...
echo.

set /p github_url="Enter your GitHub repository URL (https://github.com/aananth10/enhanced-water-scarcity-tool .git): "

echo 🔗 Connecting to GitHub repository...
git remote add origin %github_url%

echo 📤 Pushing to GitHub...
git branch -M main
git push -u origin main

echo.
echo ✅ Successfully pushed to GitHub!
echo.
echo 🌐 Next steps:
echo 1. Go to https://render.com
echo 2. Create new Web Service
echo 3. Connect your GitHub repo: enhanced-water-scarcity-tool
echo 4. Use these settings:
echo    - Runtime: Python 3
echo    - Build Command: pip install -r requirements.txt
echo    - Start Command: gunicorn --bind 0.0.0.0:$PORT backend.app:app --workers 2 --threads 2
echo.
echo 🎉 Your enhanced water scarcity tool will be live on Render!
echo.

pause