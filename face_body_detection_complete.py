"""
COMPLETE FACE AND BODY DETECTION SCRIPT
Using OpenCV Only (No MediaPipe)

Features:
- Face detection using Haar Cascade
- Full body detection using HOG descriptor
- Bounding box visualization
- Error handling

Author: Computer Vision Engineer
"""

import cv2
import numpy as np
import sys
import os


class FaceBodyDetector:
    """
    Face and Body Detection using OpenCV
    """
    
    def __init__(self):
        """Initialize Haar Cascade and HOG Descriptor"""
        
        # Load Haar Cascade for face detection
        cascade_path = cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
        self.face_cascade = cv2.CascadeClassifier(cascade_path)
        
        if self.face_cascade.empty():
            raise Exception(f"Failed to load face cascade from {cascade_path}")
        
        # Initialize HOG descriptor for body detection
        self.hog = cv2.HOGDescriptor()
        self.hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())
        
        print("✓ Face cascade loaded successfully")
        print("✓ HOG descriptor initialized successfully")
    
    def load_image(self, image_path):
        """
        Load image from file path
        
        Args:
            image_path: Path to image file
            
        Returns:
            image: Loaded image or None if failed
        """
        if not os.path.exists(image_path):
            print(f"ERROR: Image file not found: {image_path}")
            return None
        
        image = cv2.imread(image_path)
        
        if image is None:
            print(f"ERROR: Failed to load image: {image_path}")
            return None
        
        print(f"✓ Image loaded: {image.shape[1]}x{image.shape[0]} pixels")
        return image
    
    def detect_faces(self, image):
        """
        Detect faces using Haar Cascade
        
        Args:
            image: Input image (BGR)
            
        Returns:
            faces: List of face bounding boxes [(x, y, w, h), ...]
        """
        # Convert to grayscale for face detection
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
        # Detect faces
        # Parameters: scaleFactor, minNeighbors, minSize
        faces = self.face_cascade.detectMultiScale(
            gray,
            scaleFactor=1.1,
            minNeighbors=5,
            minSize=(30, 30),
            flags=cv2.CASCADE_SCALE_IMAGE
        )
        
        print(f"✓ Detected {len(faces)} face(s)")
        return faces
    
    def detect_bodies(self, image):
        """
        Detect full bodies using HOG descriptor
        
        Args:
            image: Input image (BGR)
            
        Returns:
            bodies: List of body bounding boxes [(x, y, w, h), ...]
        """
        # Resize image for better detection (HOG works better on smaller images)
        height, width = image.shape[:2]
        scale = 1.0
        
        if width > 640:
            scale = 640.0 / width
            new_width = 640
            new_height = int(height * scale)
            resized = cv2.resize(image, (new_width, new_height))
        else:
            resized = image.copy()
        
        # Detect people using HOG
        # Returns: (bounding_boxes, weights)
        # winStride: step size for sliding window
        # padding: padding around detection window
        # scale: detection scale
        bodies, weights = self.hog.detectMultiScale(
            resized,
            winStride=(8, 8),
            padding=(8, 8),
            scale=1.05,
            useMeanshiftGrouping=False
        )
        
        # Scale back to original image size
        if scale != 1.0:
            bodies = [(int(x/scale), int(y/scale), int(w/scale), int(h/scale)) 
                     for (x, y, w, h) in bodies]
        
        print(f"✓ Detected {len(bodies)} body/bodies")
        return bodies
    
    def draw_detections(self, image, faces, bodies):
        """
        Draw bounding boxes on image
        
        Args:
            image: Input image
            faces: List of face bounding boxes
            bodies: List of body bounding boxes
            
        Returns:
            result: Image with drawn bounding boxes
        """
        result = image.copy()
        
        # Draw face bounding boxes (GREEN)
        for (x, y, w, h) in faces:
            cv2.rectangle(result, (x, y), (x+w, y+h), (0, 255, 0), 3)
            cv2.putText(result, 'FACE', (x, y-10), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)
        
        # Draw body bounding boxes (BLUE)
        for (x, y, w, h) in bodies:
            cv2.rectangle(result, (x, y), (x+w, y+h), (255, 0, 0), 3)
            cv2.putText(result, 'BODY', (x, y-10), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 0, 0), 2)
        
        return result
    
    def process_image(self, image_path, display=True, save_path=None):
        """
        Complete processing pipeline
        
        Args:
            image_path: Path to input image
            display: Whether to display result
            save_path: Path to save result (optional)
            
        Returns:
            result: Processed image with detections
        """
        print("\n" + "="*60)
        print("FACE AND BODY DETECTION")
        print("="*60)
        
        # Step 1: Load image
        print("\n[1/4] Loading image...")
        image = self.load_image(image_path)
        
        if image is None:
            return None
        
        # Step 2: Detect faces
        print("\n[2/4] Detecting faces...")
        faces = self.detect_faces(image)
        
        # Step 3: Detect bodies
        print("\n[3/4] Detecting bodies...")
        bodies = self.detect_bodies(image)
        
        # Step 4: Draw results
        print("\n[4/4] Drawing detections...")
        result = self.draw_detections(image, faces, bodies)
        
        # Display results
        if display:
            print("\n" + "="*60)
            print("RESULTS")
            print("="*60)
            print(f"Faces detected: {len(faces)}")
            print(f"Bodies detected: {len(bodies)}")
            print("\nPress any key to close the window...")
            print("="*60)
            
            # Resize for display if too large
            display_img = result.copy()
            height, width = display_img.shape[:2]
            if width > 1200:
                scale = 1200.0 / width
                new_width = 1200
                new_height = int(height * scale)
                display_img = cv2.resize(display_img, (new_width, new_height))
            
            cv2.imshow('Face and Body Detection', display_img)
            cv2.waitKey(0)
            cv2.destroyAllWindows()
        
        # Save result if requested
        if save_path:
            cv2.imwrite(save_path, result)
            print(f"\n✓ Result saved to: {save_path}")
        
        return result


def main():
    """
    Main function with example usage
    """
    print("\n" + "="*60)
    print("OPENCV FACE AND BODY DETECTION")
    print("="*60)
    print("\nFeatures:")
    print("  • Face detection using Haar Cascade (GREEN boxes)")
    print("  • Body detection using HOG descriptor (BLUE boxes)")
    print("  • Real-time visualization")
    print("="*60)
    
    # Initialize detector
    try:
        detector = FaceBodyDetector()
    except Exception as e:
        print(f"\nERROR: Failed to initialize detector: {e}")
        return
    
    # Example usage
    # Replace with your image path
    image_path = "test_image.jpg"
    
    # Check if example image exists
    if not os.path.exists(image_path):
        print(f"\n⚠ WARNING: Example image '{image_path}' not found")
        print("\nUsage:")
        print("  1. Place an image file in the same directory")
        print("  2. Update 'image_path' variable with your image filename")
        print("  3. Run the script again")
        print("\nExample:")
        print("  image_path = 'my_photo.jpg'")
        print("  detector.process_image(image_path)")
        return
    
    # Process image
    result = detector.process_image(
        image_path=image_path,
        display=True,
        save_path="result_detection.jpg"
    )
    
    if result is not None:
        print("\n✓ Processing completed successfully!")
    else:
        print("\n✗ Processing failed!")


def test_with_webcam():
    """
    BONUS: Real-time detection using webcam
    """
    print("\n" + "="*60)
    print("REAL-TIME WEBCAM DETECTION")
    print("="*60)
    print("\nPress 'q' to quit")
    print("="*60)
    
    # Initialize detector
    detector = FaceBodyDetector()
    
    # Open webcam
    cap = cv2.VideoCapture(0)
    
    if not cap.isOpened():
        print("ERROR: Cannot open webcam")
        return
    
    print("\n✓ Webcam opened successfully")
    print("Processing frames... (Press 'q' to quit)")
    
    frame_count = 0
    
    while True:
        # Read frame
        ret, frame = cap.read()
        
        if not ret:
            print("ERROR: Cannot read frame")
            break
        
        frame_count += 1
        
        # Detect every 3 frames for performance
        if frame_count % 3 == 0:
            # Detect faces
            faces = detector.detect_faces(frame)
            
            # Detect bodies (skip for performance)
            # bodies = detector.detect_bodies(frame)
            bodies = []
            
            # Draw detections
            frame = detector.draw_detections(frame, faces, bodies)
        
        # Display FPS
        cv2.putText(frame, f'Frame: {frame_count}', (10, 30),
                   cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)
        
        # Show frame
        cv2.imshow('Webcam Detection (Press Q to quit)', frame)
        
        # Check for quit
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    # Cleanup
    cap.release()
    cv2.destroyAllWindows()
    print("\n✓ Webcam closed")


# ============================================================================
# EXAMPLE USAGE PATTERNS
# ============================================================================

def example_1_basic():
    """Example 1: Basic detection"""
    detector = FaceBodyDetector()
    detector.process_image("photo.jpg")


def example_2_save_result():
    """Example 2: Save result without display"""
    detector = FaceBodyDetector()
    detector.process_image("photo.jpg", display=False, save_path="output.jpg")


def example_3_batch_processing():
    """Example 3: Process multiple images"""
    detector = FaceBodyDetector()
    
    image_files = ["image1.jpg", "image2.jpg", "image3.jpg"]
    
    for img_file in image_files:
        if os.path.exists(img_file):
            print(f"\nProcessing: {img_file}")
            detector.process_image(img_file, display=False, 
                                 save_path=f"result_{img_file}")


def example_4_get_detection_data():
    """Example 4: Get detection coordinates"""
    detector = FaceBodyDetector()
    
    image = detector.load_image("photo.jpg")
    if image is not None:
        faces = detector.detect_faces(image)
        bodies = detector.detect_bodies(image)
        
        print("\nFace coordinates:")
        for i, (x, y, w, h) in enumerate(faces):
            print(f"  Face {i+1}: x={x}, y={y}, width={w}, height={h}")
        
        print("\nBody coordinates:")
        for i, (x, y, w, h) in enumerate(bodies):
            print(f"  Body {i+1}: x={x}, y={y}, width={w}, height={h}")


# ============================================================================
# RUN SCRIPT
# ============================================================================

if __name__ == "__main__":
    # Run main detection
    main()
    
    # Uncomment to test webcam
    # test_with_webcam()
    
    # Uncomment to run examples
    # example_1_basic()
    # example_2_save_result()
    # example_3_batch_processing()
    # example_4_get_detection_data()


# ============================================================================
# INSTALLATION INSTRUCTIONS
# ============================================================================
"""
INSTALLATION:

1. Install OpenCV:
   pip install opencv-python

2. Run script:
   python face_body_detection.py

3. Place test image in same directory as script

4. Update image_path variable with your image filename

TROUBLESHOOTING:

• If cascade not found:
  - OpenCV should include Haar cascades by default
  - Check: cv2.data.haarcascades path
  
• If HOG detection is slow:
  - Reduce image size before detection
  - Increase winStride parameter
  - Skip frames in video processing

• If no detections:
  - Try different scaleFactor (1.05 - 1.3)
  - Adjust minNeighbors (3 - 7)
  - Check image quality and lighting

PARAMETERS TUNING:

Face Detection (Haar Cascade):
  - scaleFactor: 1.1 (smaller = more detections, slower)
  - minNeighbors: 5 (higher = fewer false positives)
  - minSize: (30, 30) (minimum face size in pixels)

Body Detection (HOG):
  - winStride: (8, 8) (smaller = more accurate, slower)
  - padding: (8, 8) (detection window padding)
  - scale: 1.05 (detection scale step)

PERFORMANCE TIPS:

1. Resize large images before detection
2. Convert to grayscale for face detection
3. Process every N frames for video
4. Use threading for real-time applications
5. Adjust detection parameters for speed/accuracy tradeoff
"""
