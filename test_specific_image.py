"""
Simple Test Script for Face & Body Detection on Specific Image
"""

import cv2
import sys
import os

def test_image(image_path):
    print("="*60)
    print("TESTING IMAGE:", image_path)
    print("="*60)
    
    # Check if image exists
    if not os.path.exists(image_path):
        print("ERROR: Image not found!")
        return False
    
    # Load image
    print("\n[1] Loading image...")
    image = cv2.imread(image_path)
    if image is None:
        print("ERROR: Failed to load image!")
        return False
    
    print(f"OK - Image loaded: {image.shape[1]}x{image.shape[0]} pixels")
    
    # Initialize detector
    print("\n[2] Initializing detector...")
    try:
        from face_body_detection_extended import FaceBodyDetector
        detector = FaceBodyDetector()
        print("OK - Detector initialized")
    except Exception as e:
        print(f"ERROR: {e}")
        return False
    
    # Detect faces
    print("\n[3] Detecting faces...")
    try:
        faces = detector.detect_faces(image)
        print(f"OK - Detected {len(faces)} face(s)")
        for i, (x, y, w, h) in enumerate(faces):
            print(f"  Face {i+1}: x={x}, y={y}, w={w}, h={h}")
    except Exception as e:
        print(f"ERROR: {e}")
        return False
    
    # Detect bodies
    print("\n[4] Detecting bodies...")
    try:
        bodies = detector.detect_bodies(image)
        print(f"OK - Detected {len(bodies)} body/bodies")
        for i, (x, y, w, h) in enumerate(bodies):
            print(f"  Body {i+1}: x={x}, y={y}, w={w}, h={h}")
    except Exception as e:
        print(f"ERROR: {e}")
        return False
    
    # Analyze body if detected
    if len(bodies) > 0:
        print("\n[5] Analyzing body structure...")
        try:
            body_analysis = detector.analyze_body(bodies[0])
            print(f"OK - Body analysis complete")
            print(f"  Width: {body_analysis['width']}px")
            print(f"  Height: {body_analysis['height']}px")
            print(f"  Ratio: {body_analysis['ratio']:.3f}")
            print(f"  Vata: {body_analysis['vata']}")
            print(f"  Pitta: {body_analysis['pitta']}")
            print(f"  Kapha: {body_analysis['kapha']}")
        except Exception as e:
            print(f"ERROR: {e}")
            return False
    
    # Test fusion if both detected
    if len(faces) > 0 and len(bodies) > 0:
        print("\n[6] Testing fusion...")
        try:
            # Sample face scores
            face_scores = {'vata': 3, 'pitta': 5, 'kapha': 2}
            body_analysis = detector.analyze_body(bodies[0])
            
            fusion = detector.fuse_results(face_scores, body_analysis)
            print(f"OK - Fusion complete")
            print(f"  Dominant: {fusion['dominant_dosha']}")
            print(f"  Vata: {fusion['vata_percent']:.1f}%")
            print(f"  Pitta: {fusion['pitta_percent']:.1f}%")
            print(f"  Kapha: {fusion['kapha_percent']:.1f}%")
        except Exception as e:
            print(f"ERROR: {e}")
            return False
    
    # Save result image
    print("\n[7] Saving result image...")
    try:
        result_image = detector.draw_detections(image, faces, bodies)
        output_path = "test_result.jpg"
        cv2.imwrite(output_path, result_image)
        print(f"OK - Result saved to: {output_path}")
    except Exception as e:
        print(f"ERROR: {e}")
        return False
    
    print("\n" + "="*60)
    print("TEST COMPLETE - SUCCESS!")
    print("="*60)
    
    # Summary
    print("\nSUMMARY:")
    print(f"  Faces detected: {len(faces)}")
    print(f"  Bodies detected: {len(bodies)}")
    if len(faces) > 0 and len(bodies) > 0:
        print("  Status: READY FOR FUSION ANALYSIS")
    elif len(faces) > 0:
        print("  Status: Face detected, but no body")
        print("  TIP: Ensure full body is visible in image")
    elif len(bodies) > 0:
        print("  Status: Body detected, but no face")
        print("  TIP: Ensure face is clearly visible")
    else:
        print("  Status: No face or body detected")
        print("  TIP: Check image quality and composition")
    
    return True

if __name__ == "__main__":
    # Test on the specific image
    image_path = r"C:\Users\jayde\Documents\Ayurveda\WIN_20260427_12_47_30_Pro.jpg"
    
    try:
        success = test_image(image_path)
        if success:
            print("\nImage is suitable for face-body fusion analysis!")
        else:
            print("\nImage test failed. Check errors above.")
    except Exception as e:
        print(f"\nFATAL ERROR: {e}")
        import traceback
        traceback.print_exc()
