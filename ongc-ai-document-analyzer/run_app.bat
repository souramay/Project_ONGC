@echo off
echo Starting ONGC Well Report Viewer...
echo.
echo Using virtual environment Python...
".venv\Scripts\python.exe" --version
if %errorlevel% neq 0 (
    echo Error: Virtual environment not found or Python not available
    echo Please ensure the .venv folder exists and Python is properly installed
    pause
    exit /b 1
)

echo.
echo Checking dependencies...
python -c "import tkinter, docx, PIL, transformers" 2>nul
if %errorlevel% neq 0 (
    echo Installing required packages...
    pip install -r requirements.txt
    if %errorlevel% neq 0 (
        echo Error installing dependencies
        pause
        exit /b 1
    )
)

echo.
echo Starting application...
".venv\Scripts\python.exe" t.py

pause
