# SyAvi Time Predictor - PowerShell Installer Builder
# Run this on Windows with Inno Setup installed

Write-Host "========================================"
Write-Host "SyAvi Time Predictor - Installer Builder"
Write-Host "========================================"
Write-Host ""

# Set location to script directory
$scriptPath = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $scriptPath

# Check if Inno Setup is installed
$issPath = "C:\Program Files (x86)\Inno Setup 6\iscc.exe"
if (-not (Test-Path $issPath)) {
    Write-Host "ERROR: Inno Setup not found at: $issPath" -ForegroundColor Red
    Write-Host "Download and install from: https://jrsoftware.org/isdl.php" -ForegroundColor Yellow
    Read-Host "Press Enter to exit"
    exit 1
}

# Set paths
$issFile = "attached_assets\SyAviTimePredictorInstaller_1764276236527.iss"
$outputDir = "dist\installer"

# Create output directory
if (-not (Test-Path $outputDir)) {
    New-Item -ItemType Directory -Path $outputDir | Out-Null
}

Write-Host "Compiling installer..." -ForegroundColor Cyan
Write-Host "ISS File: $issFile"
Write-Host "Output Dir: $outputDir"
Write-Host ""

# Compile
& $issPath /O"$outputDir" $issFile

if ($LASTEXITCODE -eq 0) {
    Write-Host ""
    Write-Host "========================================"
    Write-Host "SUCCESS! Installer created" -ForegroundColor Green
    Write-Host "Output: $outputDir\SyAviTimePredictorSetup.exe"
    Write-Host "========================================"
} else {
    Write-Host ""
    Write-Host "ERROR: Compilation failed!" -ForegroundColor Red
}

Read-Host "Press Enter to exit"
