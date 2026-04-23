@echo off
echo ========================================
echo   AyurAI Veda - Vercel Deployment
echo   All Features Included
echo ========================================
echo.

echo Checking Vercel CLI installation...
where vercel >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Vercel CLI not found!
    echo.
    echo Please install Vercel CLI first:
    echo npm install -g vercel
    echo.
    pause
    exit /b 1
)

echo [OK] Vercel CLI found
echo.

echo ========================================
echo   Deployment Options
echo ========================================
echo.
echo 1. Deploy to Preview (test deployment)
echo 2. Deploy to Production (live deployment)
echo 3. Check deployment status
echo 4. Exit
echo.

set /p choice="Enter your choice (1-4): "

if "%choice%"=="1" (
    echo.
    echo Deploying to Preview...
    echo.
    vercel
    echo.
    echo [SUCCESS] Preview deployment complete!
    echo Check the URL above to test your app.
    echo.
) else if "%choice%"=="2" (
    echo.
    echo Deploying to Production...
    echo.
    vercel --prod
    echo.
    echo [SUCCESS] Production deployment complete!
    echo Your app is now LIVE!
    echo.
) else if "%choice%"=="3" (
    echo.
    echo Checking deployment status...
    echo.
    vercel ls
    echo.
) else if "%choice%"=="4" (
    echo.
    echo Exiting...
    exit /b 0
) else (
    echo.
    echo [ERROR] Invalid choice!
    echo.
)

echo.
echo ========================================
echo   Features Deployed:
echo ========================================
echo [OK] Homepage
echo [OK] About Ayurveda
echo [OK] Basic Assessment
echo [OK] Clinical Assessment
echo [OK] Comprehensive Assessment
echo [OK] AyurVaani Chatbot
echo [OK] Feedback System
echo [OK] Dashboard
echo [OK] All API Endpoints
echo ========================================
echo.

pause
