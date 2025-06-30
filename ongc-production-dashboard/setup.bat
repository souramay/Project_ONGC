@echo off
title ONGC Monthly Production Dashboard - Setup
color 0A
echo.
echo ========================================================
echo    ONGC Monthly Production Dashboard - Setup
echo ========================================================
echo.
echo This script will install all required dependencies
echo for the Monthly Production Dashboard application.
echo.

REM Change to the directory containing the script
cd /d "%~dp0"

echo [1/6] Checking Python installation...
echo ----------------------------------------

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ ERROR: Python is not installed or not in PATH
    echo.
    echo Please install Python from: https://www.python.org/downloads/
    echo Make sure to check "Add Python to PATH" during installation
    echo.
    pause
    exit /b 1
)

REM Get Python version
for /f "tokens=2" %%i in ('python --version 2^>^&1') do set PYTHON_VERSION=%%i
echo ✅ Python %PYTHON_VERSION% found

echo.
echo [2/6] Checking pip installation...
echo ----------------------------------------

REM Check if pip is available
pip --version >nul 2>&1
if errorlevel 1 (
    echo ❌ ERROR: pip is not installed
    echo Installing pip...
    python -m ensurepip --upgrade
    if errorlevel 1 (
        echo ❌ Failed to install pip
        pause
        exit /b 1
    )
)

for /f "tokens=2" %%i in ('pip --version 2^>^&1') do set PIP_VERSION=%%i
echo ✅ pip %PIP_VERSION% found

echo.
echo [3/6] Upgrading pip to latest version...
echo ----------------------------------------
python -m pip install --upgrade pip
if errorlevel 1 (
    echo ⚠️  Warning: Could not upgrade pip, continuing with current version
) else (
    echo ✅ pip upgraded successfully
)

echo.
echo [4/6] Installing required packages...
echo ----------------------------------------

REM Check if requirements.txt exists
if not exist "requirements.txt" (
    echo ⚠️  requirements.txt not found, installing packages individually...
    
    echo Installing pandas...
    pip install pandas>=1.5.0
    
    echo Installing matplotlib...
    pip install matplotlib>=3.6.0
    
    echo Installing Pillow...
    pip install Pillow>=9.0.0
    
    echo Installing numpy...
    pip install numpy>=1.20.0
    
    echo Installing openpyxl...
    pip install openpyxl>=3.0.0
    
) else (
    echo Installing packages from requirements.txt...
    pip install -r requirements.txt
)

if errorlevel 1 (
    echo ❌ ERROR: Failed to install some packages
    echo Please check your internet connection and try again
    pause
    exit /b 1
)

echo ✅ All packages installed successfully

echo.
echo [5/6] Verifying installation...
echo ----------------------------------------

echo Checking pandas...
python -c "import pandas; print('✅ pandas', pandas.__version__)" 2>nul
if errorlevel 1 echo ❌ pandas not working

echo Checking matplotlib...
python -c "import matplotlib; print('✅ matplotlib', matplotlib.__version__)" 2>nul
if errorlevel 1 echo ❌ matplotlib not working

echo Checking Pillow...
python -c "import PIL; print('✅ Pillow', PIL.__version__)" 2>nul
if errorlevel 1 echo ❌ Pillow not working

echo Checking tkinter...
python -c "import tkinter; print('✅ tkinter available')" 2>nul
if errorlevel 1 (
    echo ❌ tkinter not available
    echo Please install tkinter or use a Python distribution that includes it
)

echo Checking numpy...
python -c "import numpy; print('✅ numpy', numpy.__version__)" 2>nul
if errorlevel 1 echo ❌ numpy not working

echo.
echo [6/6] Checking required files...
echo ----------------------------------------

REM Check if required files exist
if exist "Monthly_Production.py" (
    echo ✅ Monthly_Production.py found
) else (
    echo ❌ Monthly_Production.py not found
)

if exist "Monthly_Production_Volume_Students.csv" (
    echo ✅ CSV data file found
) else (
    echo ⚠️  Monthly_Production_Volume_Students.csv not found
    echo Please ensure this file is in the same directory
)

if exist "logo.png" (
    echo ✅ logo.png found
) else (
    echo ⚠️  logo.png not found (splash screen may not work)
)

if exist "ongc.png" (
    echo ✅ ongc.png found
) else (
    echo ⚠️  ongc.png not found (header logo may not display)
)

echo.
echo ========================================================
echo                    SETUP COMPLETE
echo ========================================================
echo.
echo ✅ All dependencies have been installed successfully!
echo.
echo You can now run the dashboard using:
echo   • Double-click: run_dashboard.bat
echo   • Command line: python Monthly_Production.py
echo.
echo If you encounter any issues, please ensure:
echo   1. All required files are in the same directory
echo   2. Python is properly installed with tkinter support
echo   3. Internet connection is available for package downloads
echo.
echo Press any key to exit...
pause >nul
