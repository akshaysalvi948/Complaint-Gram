@echo off
echo Starting PostgreSQL to StarRocks Live Demo...
echo.

REM Check if Docker is running
docker ps >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Docker is not running. Please start Docker Desktop first.
    pause
    exit /b 1
)

REM Check if demo services are running
docker-compose ps | findstr "Up" >nul 2>&1
if %errorlevel% neq 0 (
    echo Starting demo services...
    docker-compose up -d
    echo Waiting for services to start...
    timeout /t 30 /nobreak >nul
)

echo.
echo Starting Live Demo Python Script...
echo.

REM Run the live demo
python live_demo.py

pause
