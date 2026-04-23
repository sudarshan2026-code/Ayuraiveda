@echo off
color 0A
title AyurAI Veda - Vercel Deployment Setup

echo.
echo ========================================
echo   AyurAI Veda - Vercel Deployment
echo   Complete Setup Assistant
echo ========================================
echo.

:CHECK_NODE
echo [STEP 1] Checking Node.js installation...
where node >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo [X] Node.js not found!
    echo.
    echo Node.js is required to install Vercel CLI.
    echo.
    echo Please follow these steps:
    echo 1. Open browser and go to: https://nodejs.org/
    echo 2. Download the LTS version (recommended)
    echo 3. Run the installer (use default settings)
    echo 4. Restart this script after installation
    echo.
    set /p open="Open Node.js website now? (Y/N): "
    if /i "%open%"=="Y" (
        start https://nodejs.org/
    )
    echo.
    pause
    exit /b 1
)

echo [OK] Node.js found!
node --version
echo.

:CHECK_NPM
echo [STEP 2] Checking npm installation...
where npm >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo [X] npm not found!
    echo Please reinstall Node.js from https://nodejs.org/
    pause
    exit /b 1
)

echo [OK] npm found!
npm --version
echo.

:CHECK_VERCEL
echo [STEP 3] Checking Vercel CLI installation...
where vercel >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo [X] Vercel CLI not found!
    echo.
    echo Installing Vercel CLI globally...
    echo This may take 1-2 minutes...
    echo.
    npm install -g vercel
    
    if %ERRORLEVEL% NEQ 0 (
        echo.
        echo [ERROR] Failed to install Vercel CLI!
        echo.
        echo Try running Command Prompt as Administrator:
        echo 1. Right-click Command Prompt
        echo 2. Select "Run as administrator"
        echo 3. Run this script again
        echo.
        pause
        exit /b 1
    )
    
    echo.
    echo [SUCCESS] Vercel CLI installed successfully!
    echo.
)

echo [OK] Vercel CLI found!
vercel --version
echo.

:CHECK_LOGIN
echo [STEP 4] Checking Vercel login status...
echo.
echo Please login to Vercel (browser will open)...
echo.
vercel whoami >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo You need to login to Vercel first.
    echo.
    set /p login="Login now? (Y/N): "
    if /i "%login%"=="Y" (
        vercel login
    ) else (
        echo.
        echo Please run 'vercel login' manually before deploying.
        pause
        exit /b 1
    )
)

echo [OK] Logged in to Vercel!
echo.

:DEPLOYMENT_MENU
echo ========================================
echo   Deployment Options
echo ========================================
echo.
echo 1. Deploy to Preview (test first)
echo 2. Deploy to Production (go live!)
echo 3. View existing deployments
echo 4. Open Vercel Dashboard
echo 5. View deployment logs
echo 6. Exit
echo.

set /p choice="Enter your choice (1-6): "

if "%choice%"=="1" goto DEPLOY_PREVIEW
if "%choice%"=="2" goto DEPLOY_PRODUCTION
if "%choice%"=="3" goto VIEW_DEPLOYMENTS
if "%choice%"=="4" goto OPEN_DASHBOARD
if "%choice%"=="5" goto VIEW_LOGS
if "%choice%"=="6" goto EXIT
goto INVALID_CHOICE

:DEPLOY_PREVIEW
echo.
echo ========================================
echo   Deploying to Preview...
echo ========================================
echo.
echo This will create a test deployment.
echo You can test all features before going live.
echo.
pause
echo.
vercel
echo.
if %ERRORLEVEL% EQU 0 (
    echo [SUCCESS] Preview deployment complete!
    echo.
    echo Test your app using the URL above.
    echo If everything works, deploy to production!
) else (
    echo [ERROR] Deployment failed!
    echo Check the error messages above.
)
echo.
pause
goto DEPLOYMENT_MENU

:DEPLOY_PRODUCTION
echo.
echo ========================================
echo   Deploying to Production...
echo ========================================
echo.
echo This will make your app LIVE and accessible worldwide!
echo.
set /p confirm="Are you sure? (Y/N): "
if /i not "%confirm%"=="Y" (
    echo Deployment cancelled.
    echo.
    pause
    goto DEPLOYMENT_MENU
)
echo.
echo Deploying to production...
echo.
vercel --prod
echo.
if %ERRORLEVEL% EQU 0 (
    echo.
    echo ========================================
    echo   SUCCESS! Your app is LIVE!
    echo ========================================
    echo.
    echo Your AyurAI Veda app is now accessible worldwide!
    echo.
    echo Features deployed:
    echo [OK] Homepage
    echo [OK] About Ayurveda
    echo [OK] Basic Assessment
    echo [OK] Clinical Assessment
    echo [OK] Comprehensive Assessment
    echo [OK] AyurVaani Chatbot
    echo [OK] Feedback System
    echo [OK] Dashboard
    echo [OK] All API Endpoints
    echo.
    echo Share your app URL with the world!
    echo.
) else (
    echo [ERROR] Production deployment failed!
    echo Check the error messages above.
)
echo.
pause
goto DEPLOYMENT_MENU

:VIEW_DEPLOYMENTS
echo.
echo ========================================
echo   Your Deployments
echo ========================================
echo.
vercel ls
echo.
pause
goto DEPLOYMENT_MENU

:OPEN_DASHBOARD
echo.
echo Opening Vercel Dashboard in browser...
start https://vercel.com/dashboard
echo.
pause
goto DEPLOYMENT_MENU

:VIEW_LOGS
echo.
echo ========================================
echo   Deployment Logs
echo ========================================
echo.
vercel logs
echo.
pause
goto DEPLOYMENT_MENU

:INVALID_CHOICE
echo.
echo [ERROR] Invalid choice! Please enter 1-6.
echo.
pause
goto DEPLOYMENT_MENU

:EXIT
echo.
echo Thank you for using AyurAI Veda Deployment Assistant!
echo.
echo Need help? Check SETUP_GUIDE.md
echo.
pause
exit /b 0
