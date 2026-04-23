@echo off
echo Pushing Vercel 500 error fix...

git add .
git commit -m "Fix 500 error - minimal Flask app for Vercel"
git push origin main

echo.
echo Push completed! Vercel will auto-deploy.
echo Check your Vercel dashboard for deployment status.
pause