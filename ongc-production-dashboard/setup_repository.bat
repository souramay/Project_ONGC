@echo off
title Add ONGC Project to Existing Repository
color 0A

echo.
echo ========================================================
echo    Add ONGC Production Dashboard to Existing Repo
echo ========================================================
echo.

echo This script will help you add the ONGC Production Dashboard
echo to your existing repository as a separate project folder.
echo.

echo Before running this script, make sure you have:
echo 1. An existing Git repository
echo 2. Git installed and configured
echo 3. Your repository path ready
echo.

set /p REPO_PATH="Enter the full path to your existing repository: "

if not exist "%REPO_PATH%" (
    echo.
    echo ERROR: Repository path does not exist!
    echo Please check the path and try again.
    pause
    exit /b 1
)

echo.
echo Repository found: %REPO_PATH%
echo.

set /p PROJECT_NAME="Enter folder name for this project (default: ongc-production-dashboard): "
if "%PROJECT_NAME%"=="" set PROJECT_NAME=ongc-production-dashboard

echo.
echo Creating project folder: %PROJECT_NAME%
echo.

cd /d "%REPO_PATH%"
if not exist "%PROJECT_NAME%" mkdir "%PROJECT_NAME%"

echo Copying project files...
echo.

:: Copy all files from current directory to the new project folder
xcopy "%~dp0*" "%PROJECT_NAME%\" /E /I /Y /EXCLUDE:%~dp0exclude.txt

:: Create exclude file for xcopy (temporary)
echo setup_repository.bat > exclude.txt
echo MAIN_REPO_README.md >> exclude.txt
echo exclude.txt >> exclude.txt

:: Copy files excluding the setup script and main readme
xcopy "%~dp0*" "%PROJECT_NAME%\" /E /I /Y /EXCLUDE:exclude.txt

:: Clean up
del exclude.txt

echo.
echo Files copied successfully!
echo.

echo Checking Git status...
git status

echo.
echo Adding files to Git...
git add "%PROJECT_NAME%/"

echo.
echo Creating commit...
set /p COMMIT_MSG="Enter commit message (default: Add ONGC Production Dashboard project): "
if "%COMMIT_MSG%"=="" set COMMIT_MSG=Add ONGC Production Dashboard project

git commit -m "%COMMIT_MSG%"

echo.
echo Project added successfully!
echo.
echo Your project is now located at: %REPO_PATH%\%PROJECT_NAME%
echo.
echo Next steps:
echo 1. Copy the contents of MAIN_REPO_README.md to your main repository README
echo 2. Push changes: git push
echo 3. Navigate to your project: cd %PROJECT_NAME%
echo 4. Install dependencies: pip install -r requirements.txt
echo 5. Run the application: python Monthly_Production.py
echo.

echo Would you like to push the changes now? (y/n)
set /p PUSH_CHOICE=
if /i "%PUSH_CHOICE%"=="y" (
    echo.
    echo Pushing to remote repository...
    git push
    echo.
    echo Push completed!
)

echo.
echo Setup complete! Your ONGC Production Dashboard is now part of your repository.
echo.
pause
