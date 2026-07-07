@echo off
echo ============================================================
echo AyurAI Veda - Database Authentication Setup
echo ============================================================
echo.

echo Step 1: Installing Python dependencies...
pip install -r requirements_auth.txt
if %errorlevel% neq 0 (
    echo Error: Failed to install dependencies
    pause
    exit /b 1
)
echo.

echo Step 2: Creating database...
createdb ananta_labs
if %errorlevel% neq 0 (
    echo Warning: Database might already exist or PostgreSQL not installed
)
echo.

echo Step 3: Running database schema...
psql -d ananta_labs -f database/schema.sql
if %errorlevel% neq 0 (
    echo Error: Failed to create database schema
    echo Make sure PostgreSQL is installed and running
    pause
    exit /b 1
)
echo.

echo Step 4: Creating admin user...
python -c "import bcrypt; import psycopg2; conn = psycopg2.connect('postgresql://postgres:postgres@localhost:5432/ananta_labs'); cur = conn.cursor(); password_hash = bcrypt.hashpw(b'A@L!2026#Secure', bcrypt.gensalt()).decode('utf-8'); cur.execute('INSERT INTO users (name, email, password_hash, role) VALUES (%s, %s, %s, %s) ON CONFLICT (email) DO NOTHING', ('Admin', 'anantalabsindia@gmail.com', password_hash, 'admin')); conn.commit(); cur.close(); conn.close(); print('Admin user created successfully')"
if %errorlevel% neq 0 (
    echo Warning: Admin user might already exist
)
echo.

echo ============================================================
echo Setup Complete!
echo ============================================================
echo.
echo Admin Login:
echo   Email: anantalabsindia@gmail.com
echo   Password: A@L!2026#Secure
echo.
echo To start the application, run: python run.py
echo.
pause
