@echo off
title PostgreSQL to StarRocks Live Demo
color 0A

echo.
echo ============================================================
echo    POSTGRESQL TO STARROCKS REAL-TIME DATA SYNC DEMO
echo ============================================================
echo.

REM Check if Python is available
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Python is not installed or not in PATH
    pause
    exit /b 1
)

REM Check if required packages are installed
python -c "import psycopg2, pymysql, yaml" >nul 2>&1
if %errorlevel% neq 0 (
    echo Installing required packages...
    pip install -r live_demo_requirements.txt
)

echo Starting Live Demo...
echo.

REM Run the live demo
python live_demo.py

echo.
echo Demo completed. Press any key to exit.
pause >nul
