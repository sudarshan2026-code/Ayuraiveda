@echo off
echo Removing vercel.json for auto-detection...

cd /d "c:\Users\jayde\Documents\Ayurveda"

del vercel.json
git add -A
git commit -m "Remove vercel.json - let Vercel auto-detect Python function"
git push origin main

echo.
echo vercel.json removed. Vercel will auto-detect the api/index.py function.
pause