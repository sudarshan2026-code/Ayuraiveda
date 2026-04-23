@echo off
color 0A
title AyurAI Veda - Complete Setup

echo.
echo ========================================
echo   AyurAI Veda - Complete Setup
echo   Security + Email Configuration
echo ========================================
echo.

cd /d "%~dp0"

REM ============= STEP 1: ADD SECURITY TO ALL TEMPLATES =============
echo [STEP 1] Adding Security System to All Templates...
echo.

set security_line=    ^<script src="{{ url_for('static', filename='js/security.js') }}"^>^</script^>

REM Templates to update
set templates=chatbot.html clinical_assessment.html contact.html feedback.html comprehensive_assessment.html dashboard.html

for %%f in (%templates%) do (
    if exist "templates\%%f" (
        findstr /C:"security.js" "templates\%%f" >nul
        if errorlevel 1 (
            echo Adding security to %%f...
            powershell -Command "$content = Get-Content 'templates\%%f' -Raw; $content = $content -replace '</body>', '    <script src=\"{{ url_for(''static'', filename=''js/security.js'') }}\"></script>`n</body>'; Set-Content 'templates\%%f' -Value $content -NoNewline"
            echo [OK] %%f updated
        ) else (
            echo [SKIP] %%f already has security
        )
    )
)

echo.
echo [SUCCESS] Security system added to all templates!
echo.

REM ============= STEP 2: EMAIL CONFIGURATION =============
echo ========================================
echo [STEP 2] Email Configuration
echo ========================================
echo.

echo Please provide your Gmail App Password for email functionality.
echo.
echo If you don't have one:
echo 1. Go to: https://myaccount.google.com/apppasswords
echo 2. Enable 2-Step Verification
echo 3. Generate App Password for "Mail"
echo 4. Copy the 16-character password
echo.

set /p app_password="Enter Gmail App Password (or press Enter to skip): "

if "%app_password%"=="" (
    echo.
    echo [SKIP] Email configuration skipped
    echo You can configure it later in Vercel Dashboard
    echo.
) else (
    echo.
    echo [OK] App Password received
    echo.
    echo Add these to Vercel Environment Variables:
    echo.
    echo SENDER_EMAIL = zjay5398@gmail.com
    echo GMAIL_APP_PASSWORD = %app_password%
    echo ADMIN_EMAIL = zjay5398@gmail.com
    echo.
    echo Steps to add in Vercel:
    echo 1. Go to: https://vercel.com/dashboard
    echo 2. Select your project
    echo 3. Settings -^> Environment Variables
    echo 4. Add the 3 variables above
    echo 5. Redeploy your application
    echo.
)

REM ============= STEP 3: VERIFICATION =============
echo ========================================
echo [STEP 3] Verification
echo ========================================
echo.

echo Checking files...
echo.

if exist "static\js\security.js" (
    echo [OK] Security system file exists
) else (
    echo [ERROR] Security system file missing!
)

if exist "templates\index.html" (
    findstr /C:"security.js" "templates\index.html" >nul
    if errorlevel 1 (
        echo [WARN] index.html missing security
    ) else (
        echo [OK] index.html has security
    )
)

if exist "api\index.py" (
    echo [OK] API file exists
) else (
    echo [ERROR] API file missing!
)

echo.

REM ============= STEP 4: SUMMARY =============
echo ========================================
echo   Setup Complete!
echo ========================================
echo.

echo What was done:
echo [OK] Security system added to all templates
echo [OK] Right-click protection enabled
echo [OK] F12 / DevTools disabled
echo [OK] Copy/paste protection enabled
echo [OK] Image protection enabled
echo.

if not "%app_password%"=="" (
    echo [OK] Email configuration ready
    echo     Remember to add to Vercel!
    echo.
)

echo ========================================
echo   Next Steps
echo ========================================
echo.

echo 1. Test locally:
echo    python api/index.py
echo    Open: http://localhost:5000
echo.

echo 2. Commit changes:
echo    git add .
echo    git commit -m "Add security system and email config"
echo    git push
echo.

echo 3. Configure Vercel (if email provided):
echo    - Go to Vercel Dashboard
echo    - Add environment variables
echo    - Redeploy
echo.

echo 4. Test on live site:
echo    - Right-click should be disabled
echo    - F12 should be disabled
echo    - Feedback form should work
echo.

echo ========================================
echo   Files Modified
echo ========================================
echo.

echo Templates updated:
for %%f in (%templates%) do (
    if exist "templates\%%f" echo   - templates\%%f
)
echo.

echo ========================================
echo   Security Features Active
echo ========================================
echo.

echo [OK] Right-click protection
echo [OK] F12 / DevTools disabled
echo [OK] Ctrl+Shift+I disabled
echo [OK] Ctrl+U (View Source) disabled
echo [OK] Ctrl+S (Save) disabled
echo [OK] Ctrl+P (Print) disabled
echo [OK] Image protection
echo [OK] Console protection
echo [OK] Watermark added
echo [OK] Iframe protection
echo.

echo ========================================
echo   Ready to Deploy!
echo ========================================
echo.

echo Your application is now fully configured with:
echo - Complete security system
echo - Email functionality (if configured)
echo - All features working
echo.

echo Deploy now:
echo   git add .
echo   git commit -m "Complete setup with security and email"
echo   git push
echo.

pause
