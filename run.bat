@echo off
title Python Project Launcher
cls

REM Check if the venv directory exists
IF NOT EXIST "venv" (
    echo =====================================================
    echo Virtual environment folder "venv" not found.
    echo Creating a new virtual environment...
    echo =====================================================
    python -m venv venv

    REM Check if the virtual environment was created successfully
    IF ERRORLEVEL 1 (
        echo [ERROR] Failed to create virtual environment.
        pause
        exit /b
    )
    
    echo [INFO] Virtual environment created successfully.
    echo =====================================================
    echo Activating virtual environment and installing packages...
    echo =====================================================
    call venv\Scripts\activate
) ELSE (
    echo =====================================================
    echo Virtual environment detected. Activating...
    echo =====================================================
    call venv\Scripts\activate
)

REM Check if the "requirements.txt" file exists
IF NOT EXIST "requirements.txt" (
    echo =====================================================
    echo "requirements.txt" not found.
    echo Creating a blank "requirements.txt"...
    echo =====================================================
    echo # Add your project dependencies here > requirements.txt
)

REM Check if the "src" directory exists
IF NOT EXIST "src" (
    echo =====================================================
    echo "src" folder not found. Creating "src" folder and "main.py"...
    echo =====================================================
    mkdir src
    echo # Your main Python script goes here > src\main.py
) ELSE (
    REM Check if "main.py" exists inside the "src" folder
    IF NOT EXIST "src\main.py" (
        echo =====================================================
        echo "main.py" not found in "src" folder. Creating "main.py"...
        echo =====================================================
        echo # Your main Python script goes here > src\main.py
    )
)

REM Install required packages
echo =====================================================
echo [INFO] Installing required packages from "requirements.txt"...
echo =====================================================
pip install -r requirements.txt

REM Check if the packages were installed successfully
IF ERRORLEVEL 1 (
    echo [ERROR] Failed to install packages.
    pause
    exit /b
)

REM Run main.py with Python from the virtual environment
echo =====================================================
echo Running "src\main.py"...
echo =====================================================
python src\main.py

REM Pause to allow the user to see the output
echo =====================================================
echo [INFO] Script execution completed.
echo Press any key to exit.
echo =====================================================
pause >nul
