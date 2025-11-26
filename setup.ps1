# Setup script for Windows PowerShell - Creates virtual environment and installs dependencies

Write-Host "======================================================================" -ForegroundColor Cyan
Write-Host "Fake Message and Link Detection System - Setup (PowerShell)" -ForegroundColor Cyan
Write-Host "======================================================================" -ForegroundColor Cyan
Write-Host ""

# Check if Python is installed
try {
    $pythonVersion = python --version 2>&1
    Write-Host "Python found: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "Error: Python is not installed or not in PATH" -ForegroundColor Red
    Write-Host "Please install Python 3.7 or higher from https://www.python.org/" -ForegroundColor Yellow
    exit 1
}

Write-Host ""

# Create virtual environment
if (Test-Path "venv") {
    Write-Host "Virtual environment 'venv' already exists." -ForegroundColor Yellow
} else {
    Write-Host "Creating virtual environment..." -ForegroundColor Cyan
    python -m venv venv
    if ($LASTEXITCODE -ne 0) {
        Write-Host "Error: Failed to create virtual environment" -ForegroundColor Red
        exit 1
    }
    Write-Host "Virtual environment created successfully!" -ForegroundColor Green
}

Write-Host ""
Write-Host "Installing dependencies..." -ForegroundColor Cyan
& "venv\Scripts\Activate.ps1"
python -m pip install --upgrade pip
pip install -r requirements.txt

if ($LASTEXITCODE -ne 0) {
    Write-Host "Error: Failed to install dependencies" -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "======================================================================" -ForegroundColor Cyan
Write-Host "Setup Complete!" -ForegroundColor Green
Write-Host "======================================================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "To activate the virtual environment, run:" -ForegroundColor Yellow
Write-Host "  venv\Scripts\Activate.ps1" -ForegroundColor White
Write-Host ""
Write-Host "Next steps:" -ForegroundColor Yellow
Write-Host "  1. Activate the virtual environment (see above)" -ForegroundColor White
Write-Host "  2. Run: python train_models.py" -ForegroundColor White
Write-Host "  3. Run: python demo.py" -ForegroundColor White
Write-Host ""



