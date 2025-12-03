@echo off
REM SyAvi Time Predictor - Machine Unlock Utility
REM Run as Administrator to remove the installation lock
REM Master Key Required: @Hg3505050

echo Checking for administrator privileges...
net session >nul 2>&1
if %errorlevel% neq 0 (
    echo.
    echo ERROR: This utility must be run as Administrator
    echo.
    echo Right-click this file and select "Run as Administrator"
    echo.
    pause
    exit /b 1
)

REM Change to the directory where this batch file is located
cd /d "%~dp0"

echo.
python unlock_installer.py
pause
