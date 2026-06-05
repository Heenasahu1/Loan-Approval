@echo off
REM Loan Approval Dashboard - Quick Launch Script
REM This script sets up and runs the Streamlit application

echo.
echo ========================================
echo   Loan Approval Prediction Dashboard
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo.
    echo ERROR: Python is not installed or not in your PATH
    echo Please install Python 3.8 or higher from https://www.python.org/
    echo Make sure to check "Add Python to PATH" during installation
    echo.
    pause
    exit /b 1
)

REM Check if dependencies are installed
echo Checking dependencies...
python -c "import streamlit, pandas, numpy, sklearn, plotly" 2>nul
if errorlevel 1 (
    echo.
    echo Installing required packages...
    echo This may take a few minutes...
    echo.
    pip install -r requirements.txt
    if errorlevel 1 (
        echo.
        echo ERROR: Failed to install dependencies
        echo Please run: pip install -r requirements.txt
        echo.
        pause
        exit /b 1
    )
)

REM Check if data file exists
if not exist "loan_data_new.csv" (
    echo.
    echo ERROR: loan_data_new.csv not found!
    echo Please ensure the data file is in the same directory as this script
    echo.
    pause
    exit /b 1
)

echo.
echo ✓ All dependencies are installed
echo ✓ Data file found
echo.
echo Launching Loan Approval Dashboard...
echo.
echo The application will open in your browser at: http://localhost:8501
echo Press Ctrl+C in the console to stop the server
echo.

REM Run Streamlit
streamlit run app.py

pause
