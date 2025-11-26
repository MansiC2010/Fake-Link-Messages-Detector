@echo off
REM Start Web UI for Fake Detection System

echo ======================================================================
echo AI Fake Detection System - Web Interface
echo ======================================================================
echo.

REM Check if virtual environment exists
if not exist venv\Scripts\activate.bat (
    echo Error: Virtual environment not found!
    echo Please run setup.bat first.
    pause
    exit /b 1
)

REM Activate virtual environment
call venv\Scripts\activate.bat

REM Check if models exist
if not exist models\url_model.pkl (
    echo.
    echo WARNING: Models not found!
    echo Please train models first: python train_models.py
    echo.
    pause
)

echo Starting web server...
echo.
echo Open your browser and go to: http://localhost:5000
echo.
echo Press Ctrl+C to stop the server
echo ======================================================================
echo.

python run_ui.py

pause



