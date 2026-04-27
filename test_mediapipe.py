"""
Test MediaPipe Installation
"""

print("Testing MediaPipe installation...")
print("=" * 60)

try:
    import mediapipe
    print(f"OK MediaPipe imported successfully")
    print(f"   Version: {mediapipe.__version__}")
    
    # Test solutions attribute
    if hasattr(mediapipe, 'solutions'):
        print(f"OK mediapipe.solutions available")
        
        # Test face_mesh
        if hasattr(mediapipe.solutions, 'face_mesh'):
            print(f"OK mediapipe.solutions.face_mesh available")
            
            # Try to initialize
            mp_face_mesh = mediapipe.solutions.face_mesh
            face_mesh = mp_face_mesh.FaceMesh(
                static_image_mode=True,
                max_num_faces=1,
                min_detection_confidence=0.5
            )
            print(f"OK FaceMesh initialized successfully")
            face_mesh.close()
        else:
            print(f"ERROR mediapipe.solutions.face_mesh NOT available")
    else:
        print(f"ERROR mediapipe.solutions NOT available")
        print(f"   Available attributes: {dir(mediapipe)}")
        
except ImportError as e:
    print(f"ERROR MediaPipe NOT installed: {e}")
    print(f"\nInstall with: pip install mediapipe>=0.10.0")

print("=" * 60)

# Test other dependencies
print("\nTesting other dependencies...")
print("-" * 60)

try:
    import cv2
    print(f"OK OpenCV: {cv2.__version__}")
except ImportError:
    print(f"ERROR OpenCV not installed")

try:
    import numpy
    print(f"OK NumPy: {numpy.__version__}")
except ImportError:
    print(f"ERROR NumPy not installed")

try:
    import PIL
    print(f"OK Pillow: {PIL.__version__}")
except ImportError:
    print(f"ERROR Pillow not installed")

print("=" * 60)
print("\nIf MediaPipe is not working, run:")
print("pip uninstall mediapipe")
print("pip install mediapipe>=0.10.0")
print("=" * 60)
