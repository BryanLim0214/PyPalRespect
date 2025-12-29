@echo off
REM NeuroCode Backend Startup Script for Windows
echo ========================================
echo   NeuroCode - ADHD Python Tutor
echo ========================================
echo.

REM Check if we're in the right directory
if not exist "app\main.py" (
    echo ERROR: Please run this from the backend directory!
    echo   cd d:\RespectResearch\neurocode\backend
    pause
    exit /b 1
)

REM Check if dependencies are installed
pip show fastapi >nul 2>&1
if errorlevel 1 (
    echo Installing dependencies...
    pip install -e ".[dev]"
)

echo.
echo Starting NeuroCode server...
echo.
echo API Documentation: http://localhost:8000/docs
echo Health Check:      http://localhost:8000/health
echo.
echo Press Ctrl+C to stop the server.
echo ========================================
echo.

python -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
