@echo off
REM SyAvi Time Predictor - Installer Builder Script
REM Run this on Windows with Inno Setup installed

cd /d "%~dp0"
echo.
echo ========================================
echo SyAvi Time Predictor - Installer Builder
echo ========================================
echo.

REM Check if ISCC (Inno Setup Compiler) is available
where iscc >nul 2>&1
if errorlevel 1 (
    echo ERROR: Inno Setup is not installed or not in PATH
    echo Download and install from: https://jrsoftware.org/isdl.php
    echo.
    pause
    exit /b 1
)

REM Paths
set ISS_FILE=attached_assets\SyAviTimePredictorInstaller_1764276236527.iss
set OUTPUT_DIR=dist\installer

REM Create output directory
if not exist "%OUTPUT_DIR%" mkdir "%OUTPUT_DIR%"

echo Compiling installer...
echo ISS File: %ISS_FILE%
echo Output Dir: %OUTPUT_DIR%
echo.

REM Compile the installer
iscc.exe /O"%OUTPUT_DIR%" "%ISS_FILE%"

if errorlevel 1 (
    echo.
    echo ERROR: Compilation failed!
    pause
    exit /b 1
)

echo.
echo ========================================
echo SUCCESS! Installer created
echo Output: %OUTPUT_DIR%\SyAviTimePredictorSetup.exe
echo ========================================
echo.
pause
