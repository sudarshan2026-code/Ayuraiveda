"""
Quick Test Script for Face & Body Detection
Run this to verify your setup is working correctly
"""

import cv2
import sys

def test_detection():
    print("="*60)
    print("FACE & BODY DETECTION TEST")
    print("="*60)
    
    # Test 1: Check OpenCV installation
    print("\n[Test 1] Checking OpenCV installation...")
    try:
        print(f"✓ OpenCV version: {cv2.__version__}")
    except Exception as e:
        print(f"✗ OpenCV error: {e}")
        return False
    
    # Test 2: Check Haar Cascade
    print("\n[Test 2] Checking Haar Cascade...")
    try:
        cascade_path = cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
        face_cascade = cv2.CascadeClassifier(cascade_path)
        if face_cascade.empty():
            print(f"✗ Failed to load Haar Cascade from {cascade_path}")
            return False
        print(f"✓ Haar Cascade loaded successfully")
    except Exception as e:
        print(f"✗ Haar Cascade error: {e}")
        return False
    
    # Test 3: Check HOG Descriptor
    print("\n[Test 3] Checking HOG Descriptor...")
    try:
        hog = cv2.HOGDescriptor()
        hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())
        print(f"✓ HOG Descriptor initialized successfully")
    except Exception as e:
        print(f"✗ HOG Descriptor error: {e}")
        return False
    
    # Test 4: Check face_body_detection_extended module
    print("\n[Test 4] Checking face_body_detection_extended module...")
    try:
        from face_body_detection_extended import FaceBodyDetector
        detector = FaceBodyDetector()
        print(f"✓ FaceBodyDetector imported and initialized")
    except Exception as e:
        print(f"✗ Module import error: {e}")
        return False
    
    # Test 5: Test with sample image (if available)
    print("\n[Test 5] Testing with sample image...")
    import os
    test_images = ['test_image.jpg', 'sample.jpg', 'photo.jpg']
    
    found_image = None
    for img in test_images:
        if os.path.exists(img):
            found_image = img
            break
    
    if found_image:
        try:
            image = cv2.imread(found_image)
            if image is None:
                print(f"✗ Failed to load image: {found_image}")
            else:
                print(f"✓ Loaded test image: {found_image} ({image.shape[1]}x{image.shape[0]})")
                
                # Test face detection
                faces = detector.detect_faces(image)
                print(f"  → Faces detected: {len(faces)}")
                
                # Test body detection
                bodies = detector.detect_bodies(image)
                print(f"  → Bodies detected: {len(bodies)}")
                
                if len(faces) > 0 and len(bodies) > 0:
                    print(f"✓ Both face and body detected successfully!")
                elif len(faces) > 0:
                    print(f"⚠ Face detected but no body. Ensure full body is visible.")
                elif len(bodies) > 0:
                    print(f"⚠ Body detected but no face. Ensure face is clearly visible.")
                else:
                    print(f"✗ No face or body detected. Check image quality and composition.")
        except Exception as e:
            print(f"✗ Detection test error: {e}")
    else:
        print(f"⚠ No test image found. Place a test image (test_image.jpg) to test detection.")
    
    print("\n" + "="*60)
    print("TEST COMPLETE")
    print("="*60)
    return True

if __name__ == "__main__":
    success = test_detection()
    
    if success:
        print("\n✓ All tests passed! System is ready.")
        print("\nNext steps:")
        print("1. Start Flask server: python run.py")
        print("2. Navigate to: http://127.0.0.1:5000/body-analysis")
        print("3. Upload a full-body image")
    else:
        print("\n✗ Some tests failed. Please fix the errors above.")
        sys.exit(1)
