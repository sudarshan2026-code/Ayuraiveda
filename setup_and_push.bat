@echo off
echo Setting up Git repository and pushing to GitHub...

echo Step 1: Initialize Git repository
git init

echo Step 2: Add all files
git add .

echo Step 3: Initial commit
git commit -m "Fix 500 error - minimal Flask app for Vercel"

echo Step 4: Add GitHub remote (replace YOUR_USERNAME with actual username)
echo Please replace YOUR_USERNAME in the next command with your GitHub username
git remote add origin https://github.com/YOUR_USERNAME/Ayurveda.git

echo Step 5: Push to GitHub
git branch -M main
git push -u origin main

echo.
echo Setup completed! 
echo Note: Replace YOUR_USERNAME with your actual GitHub username in the script
echo Then run this script again
pause