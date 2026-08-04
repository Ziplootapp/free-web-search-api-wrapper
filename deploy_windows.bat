@echo off
title ZipLoot Free Web Search API Server Launcher (1-Click)
color 0A

echo ======================================================================
echo           ZipLoot Free Web Search REST API Gateway (1-Click)
echo           Official Web App: https://ziploot.app
echo           Vercel Mirror:   https://ziploot.vercel.app
echo ======================================================================
echo.

echo Checking Python installation...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python is not installed or not in PATH!
    echo Please install Python 3.8+ from https://python.org and try again.
    pause
    exit /b 1
)

echo Starting ZipLoot Search REST API Server on http://localhost:8000 ...
echo.

start "" "http://localhost:8000/"

python "%~dp0server.py"

pause
