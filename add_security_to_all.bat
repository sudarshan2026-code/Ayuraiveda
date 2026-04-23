@echo off
echo ========================================
echo   Adding Security System to All Pages
echo ========================================
echo.

cd /d "%~dp0"

echo Adding security script to templates...
echo.

REM List of template files to update
set templates=about.html assessment.html chatbot.html clinical_assessment.html comprehensive_assessment.html contact.html dashboard.html feedback.html

for %%f in (%templates%) do (
    echo Processing: %%f
    
    REM Check if file exists
    if exist "templates\%%f" (
        REM Check if security script already exists
        findstr /C:"security.js" "templates\%%f" >nul
        if errorlevel 1 (
            REM Security script not found, add it before </body>
            powershell -Command "(Get-Content 'templates\%%f') -replace '</body>', '    <script src=\"{{ url_for(''static'', filename=''js/security.js'') }}\"></script>^</body>' | Set-Content 'templates\%%f'"
            echo [OK] Added security to %%f
        ) else (
            echo [SKIP] Security already exists in %%f
        )
    ) else (
        echo [WARN] File not found: %%f
    )
    echo.
)

echo.
echo ========================================
echo   Security System Added Successfully!
echo ========================================
echo.
echo Next steps:
echo 1. Review the changes
echo 2. Test locally
echo 3. Commit and push to GitHub
echo.
echo Commands:
echo   git add templates/
echo   git commit -m "Add security system to all pages"
echo   git push
echo.
pause
