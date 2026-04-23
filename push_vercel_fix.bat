@echo off
echo Pushing corrected Vercel runtime configuration...

cd /d "c:\Users\jayde\Documents\Ayurveda"

git add vercel.json
git commit -m "Fix: Use @vercel/python runtime instead of python3.9"
git push origin main

echo.
echo Corrected runtime configuration pushed!
echo Vercel should now build successfully.
pause