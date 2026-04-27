@echo off
echo ========================================
echo AyurAI Veda - Face Analysis Setup
echo ========================================
echo.

echo Installing required packages...
echo.

pip install Flask==3.0.0
pip install reportlab==4.0.7
pip install groq==0.4.1
pip install opencv-python==4.8.1.78
pip install mediapipe==0.10.8
pip install numpy==1.24.3
pip install Pillow==10.1.0

echo.
echo ========================================
echo Installation Complete!
echo ========================================
echo.
echo You can now run the application:
echo   python run.py
echo.
echo Then access Face Analysis at:
echo   http://127.0.0.1:5000/face-analysis
echo.
pause
