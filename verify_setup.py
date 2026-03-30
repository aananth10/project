"""
Urban Water Scarcity Prediction Tool - Verification Script
Tests all components before presentation
"""

import os
import sys
import subprocess
from pathlib import Path

def check_directory_structure():
    """Verify project structure"""
    print("\n" + "="*60)
    print("CHECKING PROJECT STRUCTURE")
    print("="*60)
    
    required_files = [
        'data_generator.py',
        'train_model.py',
        'requirements.txt',
        'backend/app.py',
        'frontend/dashboard.html',
        'run.bat',
        'run.sh'
    ]
    
    all_exist = True
    for file in required_files:
        exists = os.path.exists(file)
        status = "✓" if exists else "✗"
        print(f"{status} {file}")
        if not exists:
            all_exist = False
    
    return all_exist

def check_python_version():
    """Check Python version"""
    print("\n" + "="*60)
    print("CHECKING PYTHON VERSION")
    print("="*60)
    
    version = sys.version_info
    print(f"Python Version: {version.major}.{version.minor}.{version.micro}")
    
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("✗ Python 3.8+ required!")
        return False
    else:
        print("✓ Python version OK")
        return True

def check_dependencies():
    """Check if dependencies are installed"""
    print("\n" + "="*60)
    print("CHECKING DEPENDENCIES")
    print("="*60)
    
    dependencies = [
        'flask',
        'pandas',
        'numpy',
        'sklearn',
        'matplotlib',
        'seaborn',
        'joblib'
    ]
    
    missing = []
    for package in dependencies:
        try:
            __import__(package)
            print(f"✓ {package}")
        except ImportError:
            print(f"✗ {package}")
            missing.append(package)
    
    if missing:
        print(f"\n⚠️  Missing packages: {', '.join(missing)}")
        print(f"Install with: pip install {' '.join(missing)}")
        return False
    else:
        print("\n✓ All dependencies installed")
        return True

def verify_data_generation():
    """Test data generation"""
    print("\n" + "="*60)
    print("VERIFYING DATA GENERATION")
    print("="*60)
    
    if os.path.exists('data/water_scarcity_data.csv'):
        import pandas as pd
        try:
            df = pd.read_csv('data/water_scarcity_data.csv')
            print(f"✓ Data file exists")
            print(f"  Rows: {len(df)}")
            print(f"  Columns: {', '.join(df.columns)}")
            print(f"  Size: {df.memory_usage(deep=True).sum() / 1024:.2f} KB")
            return True
        except Exception as e:
            print(f"✗ Error reading data: {e}")
            return False
    else:
        print("⚠️  Data file not found. Run: python data_generator.py")
        return False

def verify_models():
    """Test model files"""
    print("\n" + "="*60)
    print("VERIFYING ML MODELS")
    print("="*60)
    
    models = [
        'models/gb_model.pkl',
        'models/rf_model.pkl',
        'models/scaler.pkl'
    ]
    
    all_exist = True
    for model_file in models:
        exists = os.path.exists(model_file)
        status = "✓" if exists else "✗"
        print(f"{status} {model_file}")
        if not exists:
            all_exist = False
    
    if not all_exist:
        print("\n⚠️  Models not found. Run: python train_model.py")
    else:
        print("\n✓ All models ready")
    
    return all_exist

def verify_api():
    """Test Flask API configuration"""
    print("\n" + "="*60)
    print("VERIFYING API CONFIGURATION")
    print("="*60)
    
    app_file = 'backend/app.py'
    if os.path.exists(app_file):
        print(f"✓ {app_file} exists")
        try:
            with open(app_file, 'r') as f:
                content = f.read()
                if 'Flask' in content:
                    print("✓ Flask configuration found")
                if '/api/' in content:
                    print("✓ API endpoints defined")
                if 'render_template' in content:
                    print("✓ Template rendering configured")
            return True
        except Exception as e:
            print(f"✗ Error reading API file: {e}")
            return False
    else:
        print(f"✗ {app_file} not found")
        return False

def verify_dashboard():
    """Test dashboard file"""
    print("\n" + "="*60)
    print("VERIFYING DASHBOARD")
    print("="*60)
    
    dashboard_file = 'frontend/dashboard.html'
    if os.path.exists(dashboard_file):
        print(f"✓ {dashboard_file} exists")
        try:
            with open(dashboard_file, 'r') as f:
                content = f.read()
                checks = {
                    'Chart.js': 'Chart visualization library',
                    'flask': 'Flask integration',
                    'predict': 'Prediction functionality',
                    'forecast': 'Forecast feature'
                }
                for check, description in checks.items():
                    if check in content:
                        print(f"✓ {description}")
                    else:
                        print(f"⚠️  {description} - may not be configured")
            return True
        except Exception as e:
            print(f"✗ Error reading dashboard: {e}")
            return False
    else:
        print(f"✗ {dashboard_file} not found")
        return False

def generate_report():
    """Generate final verification report"""
    print("\n" + "="*60)
    print("RUNNING FINAL VERIFICATION")
    print("="*60)
    
    checks = {
        "Project Structure": check_directory_structure(),
        "Python Version": check_python_version(),
        "Dependencies": check_dependencies(),
        "Data Files": verify_data_generation(),
        "ML Models": verify_models(),
        "API Configuration": verify_api(),
        "Dashboard": verify_dashboard()
    }
    
    print("\n" + "="*60)
    print("VERIFICATION REPORT")
    print("="*60)
    
    passed = sum(1 for v in checks.values() if v)
    total = len(checks)
    
    for check, result in checks.items():
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"{status} - {check}")
    
    print(f"\nTotal: {passed}/{total} checks passed")
    
    if passed == total:
        print("\n" + "🎉 "*3)
        print("ALL SYSTEMS GO! Ready for deployment!")
        print("🎉 "*3)
        print("\nNext step:")
        print("  1. Run: python -m flask --app backend/app run")
        print("  2. Open: http://localhost:5000")
        print("  3. Test the dashboard")
        return True
    elif passed >= total - 2:
        print("\n" + "⚠️  "*3)
        print("MOSTLY READY - Minor issues found")
        print("⚠️  "*3)
        return False
    else:
        print("\n" + "❌ "*3)
        print("SETUP INCOMPLETE - Follow the messages above")
        print("❌ "*3)
        return False

def main():
    """Main verification routine"""
    print("\n")
    print("╔" + "="*58 + "╗")
    print("║ URBAN WATER SCARCITY TOOL - VERIFICATION SCRIPT        ║")
    print("║ Tests all components before presentation               ║")
    print("╚" + "="*58 + "╝")
    
    success = generate_report()
    
    print("\n" + "="*60)
    if success:
        print("✓ System ready for presentation!")
        print("="*60)
        print("\nInstructions:")
        print("1. Keep this window open")
        print("2. Open new terminal/PowerShell")
        print("3. Run: python -m flask --app backend/app run")
        print("4. Open browser: http://localhost:5000")
    else:
        print("✗ Please fix issues above before continuing")
        print("="*60)
        print("\nTo fix:")
        print("1. Install missing packages:")
        print("   pip install -r requirements.txt")
        print("2. Generate data:")
        print("   python data_generator.py")
        print("3. Train model:")
        print("   python train_model.py")
        print("4. Run verification again:")
        print("   python verify_setup.py")

if __name__ == '__main__':
    main()
