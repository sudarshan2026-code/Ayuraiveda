@echo off
echo Pushing Vercel runtime fix...

cd /d "c:\Users\jayde\Documents\Ayurveda"

git add vercel.json
git commit -m "Fix Vercel runtime configuration"
git push origin main

echo.
echo Runtime fix pushed! Check Vercel deployment.
pause