@echo off
echo Removing vercel.json for auto-detection...

cd /d "c:\Users\jayde\Documents\Ayurveda"

del vercel.json
git add -A
git commit -m "Remove vercel.json - auto-detect Python function"
git push origin main

echo.
echo Auto-detection enabled. Vercel will detect api/index.py automatically.
pause