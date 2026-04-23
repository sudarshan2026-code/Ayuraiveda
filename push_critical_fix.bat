@echo off
echo Pushing critical Vercel configuration fix...

cd /d "c:\Users\jayde\Documents\Ayurveda"

echo Adding changes...
git add vercel.json
git add .vercelignore

echo Committing fix...
git commit -m "CRITICAL FIX: Configure Vercel to use api/index.py instead of app.py"

echo Pushing to GitHub...
git push origin main

echo.
echo Critical fix pushed! Vercel will now use the minimal Flask app.
echo This should resolve the SQLite database error.
pause