@echo off
REM Setup script for Windows - Creates virtual environment and installs dependencies

echo ======================================================================
echo Fake Message and Link Detection System - Setup (Windows)
echo ======================================================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python is not installed or not in PATH
    echo Please install Python 3.7 or higher from https://www.python.org/
    pause
    exit /b 1
)

echo Python found:
python --version
echo.

REM Create virtual environment
if exist venv (
    echo Virtual environment 'venv' already exists.
) else (
    echo Creating virtual environment...
    python -m venv venv
    if errorlevel 1 (
        echo Error: Failed to create virtual environment
        pause
        exit /b 1
    )
    echo Virtual environment created successfully!
)

echo.
echo Installing dependencies...
call venv\Scripts\activate.bat
python -m pip install --upgrade pip
pip install -r requirements.txt

if errorlevel 1 (
    echo Error: Failed to install dependencies
    pause
    exit /b 1
)

echo.
echo ======================================================================
echo Setup Complete!
echo ======================================================================
echo.
echo To activate the virtual environment, run:
echo   venv\Scripts\activate
echo.
echo Next steps:
echo   1. Activate the virtual environment (see above)
echo   2. Run: python train_models.py
echo   3. Run: python demo.py
echo.
pause


