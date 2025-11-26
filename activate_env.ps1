# Quick activation script for Windows PowerShell

if (Test-Path "venv\Scripts\Activate.ps1") {
    & "venv\Scripts\Activate.ps1"
    Write-Host "Virtual environment activated!" -ForegroundColor Green
    Write-Host ""
    Write-Host "You can now run:" -ForegroundColor Yellow
    Write-Host "  python train_models.py" -ForegroundColor White
    Write-Host "  python demo.py" -ForegroundColor White
    Write-Host ""
} else {
    Write-Host "Error: Virtual environment not found!" -ForegroundColor Red
    Write-Host "Please run setup.ps1 or setup.py first to create the virtual environment." -ForegroundColor Yellow
}



