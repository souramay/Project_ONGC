@echo off
echo Starting ONGC Gas Production Dashboard...
echo.

REM Change to the directory containing the script
cd /d "%~dp0"

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python is not installed or not in PATH
    echo Please install Python and add it to your system PATH
    pause
    exit /b 1
)

REM Check if the required CSV file exists
if not exist "Monthly_Production_Volume_Students.csv" (
    echo Error: Monthly_Production_Volume_Students.csv not found
    echo Please ensure the CSV file is in the same directory as this batch file
    pause
    exit /b 1
)

REM Check if the logo files exist
if not exist "logo.png" (
    echo Warning: logo.png not found - splash screen may not work properly
)

if not exist "ongc.png" (
    echo Warning: ongc.png not found - header logo may not display
)

echo Checking and installing required Python packages...
echo.

REM Install required packages if not already installed
pip install pandas matplotlib pillow tkinter --quiet

REM Run the Python script
echo Starting the dashboard application...
python Monthly_Production.py

REM Pause to see any error messages if the script fails
if errorlevel 1 (
    echo.
    echo The application encountered an error.
    pause
)
