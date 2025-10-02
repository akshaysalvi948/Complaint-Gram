@echo off
echo ========================================
echo    Mangesh's Portfolio - Streamlit App
echo ========================================
echo.
echo Checking Python installation...
python --version
if %errorlevel% neq 0 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.8+ from https://python.org
    pause
    exit /b 1
)

echo.
echo Installing/Updating dependencies...
pip install -r requirements.txt

echo.
echo Starting Portfolio Application...
echo The app will open in your browser automatically
echo If not, navigate to: http://localhost:8501
echo Press Ctrl+C to stop the application
echo.
echo ========================================

streamlit run portfolio_app.py --server.headless false

pause
