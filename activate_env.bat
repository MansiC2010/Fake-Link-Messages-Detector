@echo off
REM Quick activation script for Windows Command Prompt

if exist venv\Scripts\activate.bat (
    call venv\Scripts\activate.bat
    echo Virtual environment activated!
    echo.
    echo You can now run:
    echo   python train_models.py
    echo   python demo.py
    echo.
) else (
    echo Error: Virtual environment not found!
    echo Please run setup.bat or setup.py first to create the virtual environment.
    pause
)



