@echo off
echo ======================================
echo ONGC Project - Git Update Script
echo ======================================
echo.

echo Adding all files to git...
git add .

echo.
echo Current status:
git status --short

echo.
set /p commit_msg="Enter commit message (or press Enter for default): "
if "%commit_msg%"=="" set commit_msg="Update project files"

echo.
echo Committing changes with message: "%commit_msg%"
git commit -m "%commit_msg%"

echo.
echo Pushing to GitHub repository...
git push origin master

echo.
echo ======================================
echo Update completed successfully!
echo ======================================
pause
