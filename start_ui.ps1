# Start Web UI for Fake Detection System

Write-Host "======================================================================" -ForegroundColor Cyan
Write-Host "AI Fake Detection System - Web Interface" -ForegroundColor Cyan
Write-Host "======================================================================" -ForegroundColor Cyan
Write-Host ""

# Check if virtual environment exists
if (-not (Test-Path "venv\Scripts\Activate.ps1")) {
    Write-Host "Error: Virtual environment not found!" -ForegroundColor Red
    Write-Host "Please run setup.ps1 first." -ForegroundColor Yellow
    exit 1
}

# Activate virtual environment
& "venv\Scripts\Activate.ps1"

# Check if models exist
if (-not (Test-Path "models\url_model.pkl")) {
    Write-Host ""
    Write-Host "WARNING: Models not found!" -ForegroundColor Yellow
    Write-Host "Please train models first: python train_models.py" -ForegroundColor Yellow
    Write-Host ""
}

Write-Host "Starting web server..." -ForegroundColor Green
Write-Host ""
Write-Host "Open your browser and go to: http://localhost:5000" -ForegroundColor Yellow
Write-Host ""
Write-Host "Press Ctrl+C to stop the server" -ForegroundColor Gray
Write-Host "======================================================================" -ForegroundColor Cyan
Write-Host ""

python run_ui.py



