@echo off
setlocal
echo ========================================
echo   Starting NeuroCode Platform
echo ========================================
echo.

REM 1. Start Backend
echo [1/2] Launching Backend Server...
start "NeuroCode Backend" cmd /k "cd backend && call start_server.bat"

REM 2. Start Frontend
echo [2/2] Launching Frontend...
start "NeuroCode Frontend" cmd /k "cd frontend && npm run dev"

echo.
echo ========================================
echo   NeuroCode is starting!
echo ========================================
echo.
echo Backend API: http://localhost:8000
echo Frontend UI: http://localhost:5173
echo.
echo Use the opened windows to see logs.
echo.
pause
