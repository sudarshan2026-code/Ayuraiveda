@echo off
echo Setting up Git repository and pushing to GitHub...

echo Changing to Ayurveda directory...
cd /d "c:\Users\jayde\Documents\Ayurveda"

echo Current directory: %cd%

echo Step 1: Initialize Git repository
git init

echo Step 2: Add all files
git add .

echo Step 3: Initial commit
git commit -m "Fix 500 error - minimal Flask app for Vercel"

echo Step 4: Add GitHub remote
echo What is your GitHub username?
set /p username="Enter GitHub username: "
git remote add origin https://github.com/%username%/Ayurveda.git

echo Step 5: Push to GitHub
git branch -M main
git push -u origin main

echo.
echo Push completed! Check Vercel for auto-deployment.
pause