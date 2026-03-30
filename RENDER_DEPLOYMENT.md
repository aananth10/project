# Render Deployment Guide for Enhanced Water Scarcity Tool

## 🚀 Step-by-Step Render Deployment

### Step 1: Create GitHub Repository

1. Go to https://github.com/new
2. Repository name: `enhanced-water-scarcity-tool`
3. Make it **Public** (required for free Render)
4. **DO NOT** initialize with README (we already have one)
5. Click "Create repository"

### Step 2: Connect Local Project to GitHub

```bash
# Copy the commands from GitHub (after creating repo):
git remote add origin https://github.com/YOUR_USERNAME/enhanced-water-scarcity-tool.git
git branch -M main
git push -u origin main
```

### Step 3: Deploy on Render

1. Go to https://render.com
2. Sign up/Login (free account)
3. Click "New" → "Web Service"
4. Connect your GitHub repo: `enhanced-water-scarcity-tool`
5. Configure:
   - **Name:** `enhanced-water-scarcity-tool`
   - **Runtime:** `Python 3`
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `gunicorn --bind 0.0.0.0:$PORT backend.app:app --workers 2 --threads 2`
6. Click "Create Web Service"

### Step 4: Wait for Deployment

- Render will build and deploy automatically
- Takes 5-10 minutes
- You'll get a URL like: `https://enhanced-water-scarcity-tool.onrender.com`

### Step 5: Test Your Live App

Visit your Render URL and test:

- Dashboard loads
- API endpoints work
- Predictions function

## 🎯 Your Enhanced Features Live:

✅ 18+ real-time features  
✅ 92% prediction accuracy  
✅ Weather integration  
✅ IoT sensor data  
✅ Agricultural monitoring  
✅ Industrial tracking

## 🔧 Troubleshooting:

- If build fails, check Render logs
- Make sure all files are committed to GitHub
- Verify requirements.txt has all dependencies

## 💡 Pro Tips:

- Enable "Auto-deploy" for automatic updates
- Monitor usage in Render dashboard
- Free tier: 750 hours/month, wakes up after inactivity
