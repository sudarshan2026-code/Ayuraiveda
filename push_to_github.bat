@echo off
color 0B
title AyurAI Veda - Push to GitHub

echo.
echo ========================================
echo   AyurAI Veda - GitHub Push Assistant
echo ========================================
echo.

:CHECK_GIT
echo [STEP 1] Checking Git installation...
where git >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo [X] Git not found!
    echo.
    echo Git is required to push to GitHub.
    echo.
    echo Please follow these steps:
    echo 1. Download Git from: https://git-scm.com/download/win
    echo 2. Run the installer (use default settings)
    echo 3. Restart this script after installation
    echo.
    set /p open="Open Git download page now? (Y/N): "
    if /i "%open%"=="Y" (
        start https://git-scm.com/download/win
    )
    echo.
    pause
    exit /b 1
)

echo [OK] Git found!
git --version
echo.

:GET_REPO_URL
echo [STEP 2] GitHub Repository Setup
echo.
echo Do you already have a GitHub repository created?
echo.
set /p has_repo="(Y/N): "

if /i "%has_repo%"=="N" (
    echo.
    echo Please create a GitHub repository first:
    echo 1. Go to: https://github.com/new
    echo 2. Repository name: ayurveda (or your choice)
    echo 3. Description: AyurAI Veda - AI-Powered Ayurvedic Health System
    echo 4. Select: Public or Private
    echo 5. DO NOT initialize with README
    echo 6. Click "Create repository"
    echo 7. Copy the repository URL
    echo.
    set /p open_github="Open GitHub to create repository? (Y/N): "
    if /i "%open_github%"=="Y" (
        start https://github.com/new
    )
    echo.
    echo After creating the repository, run this script again.
    pause
    exit /b 0
)

echo.
echo Enter your GitHub repository URL:
echo Example: https://github.com/username/ayurveda.git
echo.
set /p repo_url="Repository URL: "

if "%repo_url%"=="" (
    echo [ERROR] Repository URL cannot be empty!
    pause
    exit /b 1
)

echo.
echo [STEP 3] Configuring Git...
echo.

:GIT_CONFIG
echo Setting up Git configuration...
echo.
set /p git_name="Enter your name: "
set /p git_email="Enter your email: "

git config --global user.name "%git_name%"
git config --global user.email "%git_email%"

echo [OK] Git configured!
echo.

:INIT_REPO
echo [STEP 4] Initializing Git repository...
echo.

if exist .git (
    echo [!] Git repository already initialized.
    set /p reinit="Reinitialize? This will reset git history (Y/N): "
    if /i "%reinit%"=="Y" (
        rmdir /s /q .git
        git init
        echo [OK] Repository reinitialized!
    )
) else (
    git init
    echo [OK] Repository initialized!
)
echo.

:CREATE_GITIGNORE
echo [STEP 5] Creating .gitignore file...
echo.

(
echo # Python
echo __pycache__/
echo *.py[cod]
echo *$py.class
echo *.so
echo .Python
echo.
echo # Virtual Environment
echo venv/
echo env/
echo ENV/
echo.
echo # IDE
echo .vscode/
echo .idea/
echo *.swp
echo *.swo
echo.
echo # OS
echo .DS_Store
echo Thumbs.db
echo.
echo # Database
echo *.db
echo *.sqlite
echo *.sqlite3
echo.
echo # Large files
echo *.pkl
echo *.h5
echo *.pdf
echo.
echo # Logs
echo *.log
echo.
echo # Environment variables
echo .env
echo.
echo # Batch files ^(optional^)
echo # *.bat
) > .gitignore

echo [OK] .gitignore created!
echo.

:ADD_FILES
echo [STEP 6] Adding files to Git...
echo.

git add .

if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Failed to add files!
    pause
    exit /b 1
)

echo [OK] Files added!
echo.

:COMMIT
echo [STEP 7] Creating commit...
echo.

set commit_msg="Initial commit - AyurAI Veda with all features"

git commit -m %commit_msg%

if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Failed to commit!
    echo.
    echo This might happen if there are no changes to commit.
    pause
    exit /b 1
)

echo [OK] Commit created!
echo.

:ADD_REMOTE
echo [STEP 8] Adding remote repository...
echo.

git remote remove origin >nul 2>&1
git remote add origin %repo_url%

if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Failed to add remote!
    pause
    exit /b 1
)

echo [OK] Remote added!
echo.

:PUSH
echo [STEP 9] Pushing to GitHub...
echo.
echo This will upload all your files to GitHub.
echo You may be asked to login to GitHub.
echo.
pause

git branch -M main
git push -u origin main

if %ERRORLEVEL% NEQ 0 (
    echo.
    echo [ERROR] Push failed!
    echo.
    echo Common issues:
    echo 1. Authentication failed - Check your GitHub credentials
    echo 2. Repository doesn't exist - Create it on GitHub first
    echo 3. Permission denied - Check repository access
    echo.
    echo Try these solutions:
    echo - Use GitHub Desktop: https://desktop.github.com/
    echo - Use Personal Access Token instead of password
    echo - Check repository URL is correct
    echo.
    pause
    exit /b 1
)

echo.
echo ========================================
echo   SUCCESS! Pushed to GitHub!
echo ========================================
echo.
echo Your AyurAI Veda project is now on GitHub!
echo.
echo Repository URL: %repo_url%
echo.
echo Next steps:
echo 1. View your repository on GitHub
echo 2. Deploy to Vercel from GitHub
echo 3. Share your project!
echo.
echo Files pushed:
echo [OK] api/index.py - Main application
echo [OK] templates/ - All HTML pages
echo [OK] static/ - CSS, JS, images
echo [OK] vercel.json - Vercel configuration
echo [OK] requirements.txt - Dependencies
echo [OK] README.md - Documentation
echo [OK] All other project files
echo.

set /p open_repo="Open repository in browser? (Y/N): "
if /i "%open_repo%"=="Y" (
    start %repo_url:~0,-4%
)

echo.
echo ========================================
echo   Deploy to Vercel Now?
echo ========================================
echo.
echo You can now deploy to Vercel:
echo 1. Go to: https://vercel.com/new
echo 2. Import your GitHub repository
echo 3. Click Deploy
echo 4. Your app will be live in 60 seconds!
echo.

set /p deploy="Open Vercel to deploy? (Y/N): "
if /i "%deploy%"=="Y" (
    start https://vercel.com/new
)

echo.
echo Thank you for using AyurAI Veda GitHub Assistant!
echo.
pause
