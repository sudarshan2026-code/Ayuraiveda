@echo off
echo Trying versioned Python runtime...

cd /d "c:\Users\jayde\Documents\Ayurveda"

git add vercel.json
git commit -m "Try @vercel/python@4.0.0 runtime"
git push origin main

echo.
echo If this fails, we'll try removing vercel.json for auto-detection.
pause