@echo off
color 0B
title Configure Gmail App Password

echo.
echo ========================================
echo   Gmail App Password Configuration
echo ========================================
echo.

echo This script will help you configure your Gmail App Password
echo for the AyurAI Veda email system.
echo.

REM Check if app password was already provided
if exist ".env" (
    echo [!] .env file already exists
    set /p overwrite="Do you want to overwrite it? (Y/N): "
    if /i not "%overwrite%"=="Y" (
        echo Configuration cancelled.
        pause
        exit /b 0
    )
)

echo.
echo ========================================
echo   Step 1: Get Your Gmail App Password
echo ========================================
echo.

echo If you don't have a Gmail App Password yet:
echo.
echo 1. Go to: https://myaccount.google.com/apppasswords
echo 2. Enable 2-Step Verification (if not already enabled)
echo 3. Generate App Password:
echo    - Select: Mail
echo    - Device: Other (Custom name)
echo    - Name: AyurAI Veda
echo    - Click Generate
echo 4. Copy the 16-character password
echo.

set /p open_browser="Open Gmail App Password page now? (Y/N): "
if /i "%open_browser%"=="Y" (
    start https://myaccount.google.com/apppasswords
    echo.
    echo Browser opened. Generate your App Password and come back here.
    echo.
    pause
)

echo.
echo ========================================
echo   Step 2: Enter Your App Password
echo ========================================
echo.

echo IMPORTANT: Remove all spaces from the password!
echo Example: "abcd efgh ijkl mnop" should be entered as "abcdefghijklmnop"
echo.

set /p app_password="Enter your Gmail App Password (16 characters): "

REM Remove spaces
set app_password=%app_password: =%

REM Validate length
set password_length=0
set temp_password=%app_password%
:count_loop
if defined temp_password (
    set temp_password=%temp_password:~1%
    set /a password_length+=1
    goto count_loop
)

if %password_length% NEQ 16 (
    echo.
    echo [ERROR] App Password must be exactly 16 characters!
    echo You entered %password_length% characters.
    echo.
    echo Please try again with the correct password.
    pause
    exit /b 1
)

echo.
echo [OK] Password length verified: 16 characters
echo.

REM Create .env file
echo # AyurAI Veda - Environment Configuration > .env
echo # Generated on %date% %time% >> .env
echo. >> .env
echo SENDER_EMAIL=zjay5398@gmail.com >> .env
echo GMAIL_APP_PASSWORD=%app_password% >> .env
echo ADMIN_EMAIL=zjay5398@gmail.com >> .env
echo SECRET_KEY=ayurveda_secret_key_2024 >> .env

echo [OK] .env file created successfully!
echo.

echo ========================================
echo   Step 3: Add to Vercel
echo ========================================
echo.

echo Your .env file has been created for local testing.
echo.
echo Now you need to add these to Vercel:
echo.
echo 1. Go to: https://vercel.com/dashboard
echo 2. Select your project
echo 3. Settings -^> Environment Variables
echo 4. Add these 3 variables:
echo.
echo    Variable Name          Value
echo    ─────────────────────  ──────────────────
echo    SENDER_EMAIL           zjay5398@gmail.com
echo    GMAIL_APP_PASSWORD     %app_password%
echo    ADMIN_EMAIL            zjay5398@gmail.com
echo.
echo 5. Click Save for each variable
echo 6. Redeploy your application
echo.

set /p open_vercel="Open Vercel Dashboard now? (Y/N): "
if /i "%open_vercel%"=="Y" (
    start https://vercel.com/dashboard
)

echo.
echo ========================================
echo   Configuration Complete!
echo ========================================
echo.

echo What was done:
echo [OK] .env file created for local testing
echo [OK] App Password validated (16 characters)
echo [OK] Configuration ready
echo.

echo Next steps:
echo 1. Add environment variables to Vercel (see above)
echo 2. Redeploy your application
echo 3. Test the feedback form
echo.

echo ========================================
echo   Test Locally (Optional)
echo ========================================
echo.

echo To test email locally before deploying:
echo.
echo 1. Install dependencies:
echo    pip install Flask
echo.
echo 2. Run the application:
echo    python api/index.py
echo.
echo 3. Open: http://localhost:5000/feedback
echo.
echo 4. Submit a test feedback
echo.
echo 5. Check your email: zjay5398@gmail.com
echo.

echo ========================================
echo   Security Note
echo ========================================
echo.

echo [!] IMPORTANT: Never commit .env file to Git!
echo.
echo The .env file is already in .gitignore
echo Your App Password is safe and won't be uploaded to GitHub
echo.

echo ========================================
echo   Summary
echo ========================================
echo.

echo Email: zjay5398@gmail.com
echo App Password: %app_password%
echo Status: Configured
echo.

echo Remember to:
echo - Add to Vercel Environment Variables
echo - Redeploy your application
echo - Test the feedback form
echo.

pause
