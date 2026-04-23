@echo off
echo Deploying comprehensive AyurAI Veda with all features...

cd /d "c:\Users\jayde\Documents\Ayurveda"

git add api/index.py
git commit -m "MAJOR UPDATE: Full AyurAI Veda with Assessment, Chat, Analysis & All Pages"
git push origin main

echo.
echo Comprehensive AyurAI Veda deployed!
echo Features included:
echo - Homepage with navigation
echo - About Ayurveda page
echo - Clinical Assessment with Tridosha analysis
echo - AyurVaani AI Chatbot
echo - Contact page
echo - API endpoints for analysis and chat
echo.
echo Check your Vercel deployment!
pause