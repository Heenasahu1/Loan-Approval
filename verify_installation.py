"""
Test script to verify the Loan Approval Dashboard installation
Run this before running the main app to ensure everything is set up correctly
"""

import sys
import subprocess
from pathlib import Path

def print_header(text):
    """Print a formatted header"""
    print("\n" + "=" * 80)
    print(f"  {text}")
    print("=" * 80)

def check_python_version():
    """Check if Python version is compatible"""
    print_header("1. Checking Python Version")
    
    version = sys.version_info
    print(f"Python version: {version.major}.{version.minor}.{version.micro}")
    
    if version.major >= 3 and version.minor >= 8:
        print("✅ Python version is compatible (3.8 or higher)")
        return True
    else:
        print("❌ Python version is too old. Please upgrade to Python 3.8 or higher")
        return False

def check_required_packages():
    """Check if all required packages are installed"""
    print_header("2. Checking Required Packages")
    
    required_packages = [
        'streamlit',
        'pandas',
        'numpy',
        'scikit-learn',
        'plotly',
        'matplotlib',
        'seaborn'
    ]
    
    missing_packages = []
    installed_packages = []
    
    for package in required_packages:
        try:
            __import__(package)
            print(f"✅ {package}")
            installed_packages.append(package)
        except ImportError:
            print(f"❌ {package} - NOT INSTALLED")
            missing_packages.append(package)
    
    print(f"\n✅ Installed: {len(installed_packages)}/{len(required_packages)}")
    
    if missing_packages:
        print(f"\n⚠️  Missing packages: {', '.join(missing_packages)}")
        print("\nTo install missing packages, run:")
        print("  pip install -r requirements.txt")
        return False
    
    return True

def check_data_file():
    """Check if the data file exists and is readable"""
    print_header("3. Checking Data File")
    
    data_file = Path('loan_data_new.csv')
    
    if not data_file.exists():
        print(f"❌ Data file '{data_file}' not found!")
        print(f"   Please ensure 'loan_data_new.csv' is in the current directory")
        return False
    
    print(f"✅ Data file found: {data_file}")
    
    try:
        import pandas as pd
        df = pd.read_csv(data_file)
        print(f"✅ Data file is readable")
        print(f"   Shape: {df.shape[0]} rows × {df.shape[1]} columns")
        
        # Check for required columns
        required_columns = [
            'Age', 'Gender', 'Education', 'Person Income', 'Employee Experience',
            'Home Onwership', 'Loan Amount', 'Loan Intent', 'Loan interest Rate',
            'Loan percentage', 'Credit History', 'Credit Score', 'Previous Loan', 'Loan Status'
        ]
        
        missing_columns = [col for col in required_columns if col not in df.columns]
        
        if missing_columns:
            print(f"❌ Missing columns: {', '.join(missing_columns)}")
            return False
        
        print(f"✅ All required columns present")
        
        # Check for missing values
        missing_pct = df.isnull().sum().sum() / (df.shape[0] * df.shape[1]) * 100
        print(f"   Missing values: {missing_pct:.2f}%")
        
        # Check target distribution
        if 'Loan Status' in df.columns:
            approved = (df['Loan Status'] == 1).sum()
            rejected = (df['Loan Status'] == 0).sum()
            print(f"   Approved loans: {approved} ({approved/len(df)*100:.1f}%)")
            print(f"   Rejected loans: {rejected} ({rejected/len(df)*100:.1f}%)")
        
        return True
        
    except Exception as e:
        print(f"❌ Error reading data file: {str(e)}")
        return False

def check_utility_files():
    """Check if utility files exist"""
    print_header("4. Checking Utility Files")
    
    utility_files = {
        'app.py': 'Main Streamlit application',
        'utils.py': 'Utility functions',
        'config.py': 'Configuration file',
        'explore_data.py': 'Data exploration script',
        'requirements.txt': 'Python dependencies',
        'README.md': 'Documentation',
        'QUICKSTART.md': 'Quick start guide'
    }
    
    found_files = 0
    
    for filename, description in utility_files.items():
        file_path = Path(filename)
        if file_path.exists():
            print(f"✅ {filename} - {description}")
            found_files += 1
        else:
            print(f"⚠️  {filename} - {description} (OPTIONAL)")
    
    print(f"\n✅ Found {found_files}/{len(utility_files)} expected files")
    return found_files > 0

def test_model_training():
    """Test if the model can be trained"""
    print_header("5. Testing Model Training")
    
    try:
        import pandas as pd
        from sklearn.model_selection import train_test_split
        from sklearn.preprocessing import LabelEncoder
        from sklearn.ensemble import RandomForestClassifier
        
        print("Loading data...")
        df = pd.read_csv('loan_data_new.csv')
        
        print("Preprocessing data...")
        data = df.copy()
        data = data.fillna(data.median(numeric_only=True))
        
        # Encode categorical features
        categorical_columns = ['Gender', 'Education', 'Home Onwership', 'Loan Intent', 'Previous Loan']
        for col in categorical_columns:
            if col in data.columns:
                le = LabelEncoder()
                data[col] = le.fit_transform(data[col].astype(str))
        
        print("Training model...")
        X = data.drop('Loan Status', axis=1)
        y = data['Loan Status']
        
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        
        model = RandomForestClassifier(n_estimators=10, random_state=42, max_depth=15)  # Fewer trees for faster testing
        model.fit(X_train, y_train)
        
        accuracy = model.score(X_test, y_test)
        print(f"✅ Model trained successfully!")
        print(f"   Test accuracy: {accuracy*100:.2f}%")
        
        return True
        
    except Exception as e:
        print(f"❌ Error training model: {str(e)}")
        return False

def test_streamlit():
    """Test if Streamlit is working"""
    print_header("6. Testing Streamlit Installation")
    
    try:
        import streamlit as st
        print(f"✅ Streamlit version: {st.__version__}")
        return True
    except Exception as e:
        print(f"❌ Error importing Streamlit: {str(e)}")
        return False

def run_all_checks():
    """Run all verification checks"""
    print("\n" + "🔍 " * 20)
    print("LOAN APPROVAL DASHBOARD - INSTALLATION VERIFICATION")
    print("🔍 " * 20)
    
    checks = [
        ("Python Version", check_python_version),
        ("Required Packages", check_required_packages),
        ("Data File", check_data_file),
        ("Utility Files", check_utility_files),
        ("Streamlit", test_streamlit),
        ("Model Training", test_model_training),
    ]
    
    results = []
    
    for check_name, check_func in checks:
        try:
            result = check_func()
            results.append((check_name, result))
        except Exception as e:
            print(f"\n❌ Unexpected error in {check_name}: {str(e)}")
            results.append((check_name, False))
    
    # Summary
    print_header("VERIFICATION SUMMARY")
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for check_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} - {check_name}")
    
    print(f"\n📊 Results: {passed}/{total} checks passed")
    
    if passed == total:
        print("\n" + "🎉 " * 20)
        print("ALL CHECKS PASSED! You're ready to run the application.")
        print("🎉 " * 20)
        print("\n🚀 To start the dashboard, run:")
        print("   streamlit run app.py")
        return True
    else:
        print("\n⚠️  Some checks failed. Please fix the issues above before running the application.")
        print("\n💡 Common solutions:")
        print("   1. Install missing packages: pip install -r requirements.txt")
        print("   2. Ensure loan_data_new.csv is in the current directory")
        print("   3. Check that Python 3.8+ is installed")
        return False

if __name__ == "__main__":
    success = run_all_checks()
    sys.exit(0 if success else 1)
