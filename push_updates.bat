@echo off
color 0A
title AyurAI Veda - Push Updates to GitHub
echo.
echo ========================================================
echo   AyurAI Veda - Push Updates to GitHub
echo ========================================================
echo.
echo [1/3] Adding files to Git stage...
git add .

echo.
echo [2/3] Creating commit...
git commit -m "Auto-deploy: Multi-lingual Assessment, AI Chatbot localization, and dynamic mobile routing"

echo.
echo [3/3] Pushing updates to GitHub (triggers Vercel/Railway auto-deployment)...
git push origin main

echo.
echo ========================================================
echo   SUCCESS! Updates pushed to GitHub.
echo   Check your Vercel/Railway dashboard for deploy status.
echo ========================================================
echo.
pause
