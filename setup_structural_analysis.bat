@echo off
REM STRUCTURAL FACE ANALYSIS - QUICK SETUP
REM Run this script to install all dependencies

echo ============================================================
echo STRUCTURAL FACE ANALYSIS SYSTEM - SETUP
echo ============================================================
echo.

echo [1/3] Installing dependencies...
pip install mediapipe opencv-python numpy pillow
echo.

echo [2/3] Verifying installation...
python -c "import mediapipe; import cv2; import numpy; from PIL import Image; print('✓ All dependencies installed successfully!')"
echo.

echo [3/3] Running test suite...
python test_structural_analysis.py
echo.

echo ============================================================
echo SETUP COMPLETE!
echo ============================================================
echo.
echo Next steps:
echo 1. Place a test image named 'test_face.jpg' in this folder
echo 2. Run: python structural_face_analysis.py
echo 3. Or use in your code:
echo    from structural_face_analysis import StructuralFaceAnalyzer
echo.
echo ============================================================

pause
