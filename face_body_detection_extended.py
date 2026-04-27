"""
COMPLETE FACE AND BODY DETECTION WITH TRIDOSHA FUSION
Using OpenCV Only (No MediaPipe)

Features:
- Face detection using Haar Cascade
- Full body detection using HOG descriptor
- Body Tridosha analysis (Vata/Pitta/Kapha)
- Face-Body weighted fusion (60%/40%)
- Normalized percentage scores
- Dominant dosha determination
- Bounding box visualization
- Crop detected regions
- Display regions separately
- Error handling

Author: Computer Vision Engineer
Version: 3.0 - Extended with Tridosha Fusion
"""

import cv2
import numpy as np
import sys
import os

# Fix Windows console encoding
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')


class FaceBodyDetector:
    """
    Face and Body Detection using OpenCV with Region Cropping
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
        
        print("[OK] Face cascade loaded successfully")
        print("[OK] HOG descriptor initialized successfully")
    
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
        
        print(f"[OK] Image loaded: {image.shape[1]}x{image.shape[0]} pixels")
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
        
        print(f"[OK] Detected {len(faces)} face(s)")
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
        
        print(f"[OK] Detected {len(bodies)} body/bodies")
        return bodies
    
    def crop_region(self, image, x, y, w, h, padding=10):
        """
        Crop region from image with bounds checking
        
        Args:
            image: Input image
            x, y, w, h: Bounding box coordinates
            padding: Extra padding around region (default: 10)
            
        Returns:
            cropped: Cropped region or None if invalid
        """
        img_height, img_width = image.shape[:2]
        
        # Add padding
        x_start = max(0, x - padding)
        y_start = max(0, y - padding)
        x_end = min(img_width, x + w + padding)
        y_end = min(img_height, y + h + padding)
        
        # Validate bounds
        if x_start >= x_end or y_start >= y_end:
            print(f"WARNING: Invalid crop region: ({x_start}, {y_start}) to ({x_end}, {y_end})")
            return None
        
        # Crop region
        cropped = image[y_start:y_end, x_start:x_end].copy()
        
        return cropped
    
    def crop_all_faces(self, image, faces, padding=10):
        """
        Crop all detected face regions
        
        Args:
            image: Input image
            faces: List of face bounding boxes
            padding: Extra padding around faces
            
        Returns:
            face_crops: List of cropped face images
        """
        face_crops = []
        
        for i, (x, y, w, h) in enumerate(faces):
            cropped = self.crop_region(image, x, y, w, h, padding)
            
            if cropped is not None:
                face_crops.append({
                    'index': i,
                    'bbox': (x, y, w, h),
                    'image': cropped
                })
                print(f"  ✓ Cropped face {i+1}: {cropped.shape[1]}x{cropped.shape[0]} pixels")
        
        return face_crops
    
    def crop_all_bodies(self, image, bodies, padding=10):
        """
        Crop all detected body regions
        
        Args:
            image: Input image
            bodies: List of body bounding boxes
            padding: Extra padding around bodies
            
        Returns:
            body_crops: List of cropped body images
        """
        body_crops = []
        
        for i, (x, y, w, h) in enumerate(bodies):
            cropped = self.crop_region(image, x, y, w, h, padding)
            
            if cropped is not None:
                body_crops.append({
                    'index': i,
                    'bbox': (x, y, w, h),
                    'image': cropped
                })
                print(f"  ✓ Cropped body {i+1}: {cropped.shape[1]}x{cropped.shape[0]} pixels")
        
        return body_crops
    
    def analyze_body(self, body_bbox):
        """
        Analyze body region for Tridosha classification
        
        Args:
            body_bbox: Body bounding box (x, y, w, h)
            
        Returns:
            analysis: Dictionary with body measurements and dosha scores
        """
        x, y, w, h = body_bbox
        
        # Compute body dimensions
        body_width = w
        body_height = h
        body_ratio = body_width / body_height if body_height > 0 else 0
        
        # Initialize dosha scores
        body_vata = 0
        body_pitta = 0
        body_kapha = 0
        
        # Body Dosha Classification Logic
        if body_ratio < 0.35:
            body_vata += 2
        elif 0.35 <= body_ratio <= 0.5:
            body_pitta += 2
        elif body_ratio > 0.5:
            body_kapha += 2
        
        # Print analysis
        print(f"\n  Body Width: {body_width}px")
        print(f"  Body Height: {body_height}px")
        print(f"  Body Ratio: {body_ratio:.3f}")
        print(f"  Body Vata Score: {body_vata}")
        print(f"  Body Pitta Score: {body_pitta}")
        print(f"  Body Kapha Score: {body_kapha}")
        
        return {
            'width': body_width,
            'height': body_height,
            'ratio': body_ratio,
            'vata': body_vata,
            'pitta': body_pitta,
            'kapha': body_kapha
        }
    
    def fuse_results(self, face_scores, body_scores):
        """
        Fuse face and body dosha scores with weighted fusion
        
        Args:
            face_scores: Dictionary with face dosha scores {'vata': x, 'pitta': y, 'kapha': z}
            body_scores: Dictionary with body dosha scores {'vata': x, 'pitta': y, 'kapha': z}
            
        Returns:
            fusion: Dictionary with final fused results
        """
        # Extract scores
        face_vata = face_scores.get('vata', 0)
        face_pitta = face_scores.get('pitta', 0)
        face_kapha = face_scores.get('kapha', 0)
        
        body_vata = body_scores.get('vata', 0)
        body_pitta = body_scores.get('pitta', 0)
        body_kapha = body_scores.get('kapha', 0)
        
        # Weighted fusion (Face: 60%, Body: 40%)
        final_vata = (face_vata * 0.6) + (body_vata * 0.4)
        final_pitta = (face_pitta * 0.6) + (body_pitta * 0.4)
        final_kapha = (face_kapha * 0.6) + (body_kapha * 0.4)
        
        # Normalize to percentages
        total = final_vata + final_pitta + final_kapha
        
        if total > 0:
            final_vata_percent = (final_vata / total) * 100
            final_pitta_percent = (final_pitta / total) * 100
            final_kapha_percent = (final_kapha / total) * 100
        else:
            final_vata_percent = 33.33
            final_pitta_percent = 33.33
            final_kapha_percent = 33.34
        
        # Determine dominant dosha
        max_percent = max(final_vata_percent, final_pitta_percent, final_kapha_percent)
        
        if final_vata_percent == max_percent:
            dominant_dosha = "Vata"
        elif final_pitta_percent == max_percent:
            dominant_dosha = "Pitta"
        else:
            dominant_dosha = "Kapha"
        
        # Print fusion results
        print("\n" + "="*60)
        print("FINAL DOSHA FUSION RESULTS")
        print("="*60)
        print(f"\nWeighted Fusion (Face: 60%, Body: 40%):")
        print(f"  Vata:  {final_vata:.2f} → {final_vata_percent:.2f}%")
        print(f"  Pitta: {final_pitta:.2f} → {final_pitta_percent:.2f}%")
        print(f"  Kapha: {final_kapha:.2f} → {final_kapha_percent:.2f}%")
        print(f"\nDominant Dosha: {dominant_dosha}")
        print("="*60)
        
        return {
            'vata_raw': final_vata,
            'pitta_raw': final_pitta,
            'kapha_raw': final_kapha,
            'vata_percent': final_vata_percent,
            'pitta_percent': final_pitta_percent,
            'kapha_percent': final_kapha_percent,
            'dominant_dosha': dominant_dosha,
            'total': total
        }
    
    def show_pipeline(self, image, faces, bodies, face_crops, body_crops, delay=800):
        """
        Display step-by-step visual processing pipeline
        
        Args:
            image: Original image
            faces: List of face bounding boxes
            bodies: List of body bounding boxes
            face_crops: List of face crop dictionaries
            body_crops: List of body crop dictionaries
            delay: Delay between steps in milliseconds (default: 800)
        """
        print("\n" + "="*60)
        print("VISUAL PROCESSING PIPELINE")
        print("="*60)
        print(f"Delay: {delay}ms between steps")
        print("="*60)
        
        # Step 1: Original Image
        print("\n[Step 1/5] Displaying Original Image...")
        original_display = image.copy()
        cv2.imshow('Original', original_display)
        cv2.waitKey(delay)
        
        # Step 2: Face Detection
        print("[Step 2/5] Displaying Face Detection...")
        face_detection = image.copy()
        for (x, y, w, h) in faces:
            cv2.rectangle(face_detection, (x, y), (x+w, y+h), (0, 255, 0), 3)
            cv2.putText(face_detection, 'FACE', (x, y-10),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)
        cv2.imshow('Face Detection', face_detection)
        cv2.waitKey(delay)
        
        # Step 3: Body Detection
        print("[Step 3/5] Displaying Body Detection...")
        body_detection = image.copy()
        for (x, y, w, h) in bodies:
            cv2.rectangle(body_detection, (x, y), (x+w, y+h), (255, 0, 0), 3)
            cv2.putText(body_detection, 'BODY', (x, y-10),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 0, 0), 2)
        cv2.imshow('Body Detection', body_detection)
        cv2.waitKey(delay)
        
        # Step 4: Face Region
        if len(face_crops) > 0:
            print("[Step 4/5] Displaying Face Region...")
            face_region = face_crops[0]['image'].copy()
            # Resize if too small
            if face_region.shape[0] < 200 or face_region.shape[1] < 200:
                scale = max(200.0 / face_region.shape[0], 200.0 / face_region.shape[1])
                new_width = int(face_region.shape[1] * scale)
                new_height = int(face_region.shape[0] * scale)
                face_region = cv2.resize(face_region, (new_width, new_height), interpolation=cv2.INTER_CUBIC)
            cv2.imshow('Face Region', face_region)
            cv2.waitKey(delay)
        else:
            print("[Step 4/5] No face region to display")
        
        # Step 5: Body Region
        if len(body_crops) > 0:
            print("[Step 5/5] Displaying Body Region...")
            body_region = body_crops[0]['image'].copy()
            # Resize if too large
            if body_region.shape[0] > 600:
                scale = 600.0 / body_region.shape[0]
                new_width = int(body_region.shape[1] * scale)
                new_height = 600
                body_region = cv2.resize(body_region, (new_width, new_height))
            cv2.imshow('Body Region', body_region)
            cv2.waitKey(delay)
        else:
            print("[Step 5/5] No body region to display")
        
        # Final wait and cleanup
        print("\n" + "="*60)
        print("Pipeline complete. Press any key to close all windows...")
        print("="*60)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        print("✓ All windows closed")
    
    def display_cropped_regions(self, face_crops, body_crops, wait_time=0):
        """
        Display all cropped regions in separate windows
        
        Args:
            face_crops: List of face crop dictionaries
            body_crops: List of body crop dictionaries
            wait_time: Time to wait (0 = wait for key press)
        """
        print("\n" + "="*60)
        print("DISPLAYING CROPPED REGIONS")
        print("="*60)
        
        # Display face regions
        if len(face_crops) > 0:
            print(f"\nDisplaying {len(face_crops)} face region(s)...")
            for crop_data in face_crops:
                idx = crop_data['index']
                img = crop_data['image']
                
                # Resize if too small for visibility
                if img.shape[0] < 100 or img.shape[1] < 100:
                    scale = max(100.0 / img.shape[0], 100.0 / img.shape[1])
                    new_width = int(img.shape[1] * scale)
                    new_height = int(img.shape[0] * scale)
                    img = cv2.resize(img, (new_width, new_height), interpolation=cv2.INTER_CUBIC)
                
                window_name = f"Face Region {idx+1}"
                cv2.imshow(window_name, img)
                print(f"  ✓ Window opened: {window_name}")
        else:
            print("\n⚠ No face regions to display")
        
        # Display body regions
        if len(body_crops) > 0:
            print(f"\nDisplaying {len(body_crops)} body region(s)...")
            for crop_data in body_crops:
                idx = crop_data['index']
                img = crop_data['image']
                
                # Resize if too large for display
                if img.shape[0] > 800:
                    scale = 800.0 / img.shape[0]
                    new_width = int(img.shape[1] * scale)
                    new_height = 800
                    img = cv2.resize(img, (new_width, new_height))
                
                window_name = f"Body Region {idx+1}"
                cv2.imshow(window_name, img)
                print(f"  ✓ Window opened: {window_name}")
        else:
            print("\n⚠ No body regions to display")
        
        # Wait for key press
        if len(face_crops) > 0 or len(body_crops) > 0:
            print("\n" + "="*60)
            print("Press any key to close all windows...")
            print("="*60)
            cv2.waitKey(wait_time)
            cv2.destroyAllWindows()
    
    def save_cropped_regions(self, face_crops, body_crops, output_dir="cropped_regions"):
        """
        Save all cropped regions to files
        
        Args:
            face_crops: List of face crop dictionaries
            body_crops: List of body crop dictionaries
            output_dir: Directory to save crops
        """
        # Create output directory
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
            print(f"✓ Created directory: {output_dir}")
        
        saved_files = []
        
        # Save face regions
        for crop_data in face_crops:
            idx = crop_data['index']
            img = crop_data['image']
            filename = os.path.join(output_dir, f"face_{idx+1}.jpg")
            cv2.imwrite(filename, img)
            saved_files.append(filename)
            print(f"  ✓ Saved: {filename}")
        
        # Save body regions
        for crop_data in body_crops:
            idx = crop_data['index']
            img = crop_data['image']
            filename = os.path.join(output_dir, f"body_{idx+1}.jpg")
            cv2.imwrite(filename, img)
            saved_files.append(filename)
            print(f"  ✓ Saved: {filename}")
        
        return saved_files
    
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
    
    def process_image(self, image_path, display=True, save_path=None, 
                     crop_regions=True, display_crops=True, save_crops=False, show_pipeline_steps=False):
        """
        Complete processing pipeline with cropping
        
        Args:
            image_path: Path to input image
            display: Whether to display result with bounding boxes
            save_path: Path to save result (optional)
            crop_regions: Whether to crop detected regions
            display_crops: Whether to display cropped regions
            save_crops: Whether to save cropped regions
            show_pipeline_steps: Whether to show step-by-step pipeline visualization
            
        Returns:
            result: Dictionary with all results
        """
        print("\n" + "="*60)
        print("FACE AND BODY DETECTION WITH CROPPING")
        print("="*60)
        
        # Step 1: Load image
        print("\n[1/6] Loading image...")
        image = self.load_image(image_path)
        
        if image is None:
            return None
        
        # Step 2: Detect faces
        print("\n[2/6] Detecting faces...")
        faces = self.detect_faces(image)
        
        # Step 3: Detect bodies
        print("\n[3/6] Detecting bodies...")
        bodies = self.detect_bodies(image)
        
        # Step 4: Draw results
        print("\n[4/6] Drawing detections...")
        result_image = self.draw_detections(image, faces, bodies)
        
        # Step 5: Crop regions and analyze bodies
        face_crops = []
        body_crops = []
        body_analyses = []
        
        if crop_regions and (len(faces) > 0 or len(bodies) > 0):
            print("\n[5/6] Cropping detected regions and analyzing bodies...")
            
            if len(faces) > 0:
                print(f"\nCropping {len(faces)} face(s)...")
                face_crops = self.crop_all_faces(image, faces, padding=20)
            
            if len(bodies) > 0:
                print(f"\nCropping {len(bodies)} body/bodies...")
                body_crops = self.crop_all_bodies(image, bodies, padding=20)
                
                # Analyze each body for Tridosha
                print(f"\nAnalyzing {len(bodies)} body/bodies for Tridosha...")
                for i, body_bbox in enumerate(bodies):
                    print(f"\nBody {i+1} Analysis:")
                    analysis = self.analyze_body(body_bbox)
                    body_analyses.append(analysis)
        else:
            print("\n[5/6] Skipping cropping (no detections or disabled)")
        
        # Show pipeline visualization if requested
        if show_pipeline_steps and (len(faces) > 0 or len(bodies) > 0):
            self.show_pipeline(image, faces, bodies, face_crops, body_crops)
        
        # Step 6: Display/Save
        print("\n[6/6] Displaying and saving results...")
        
        # Display main result
        if display and not show_pipeline_steps:
            print("\n" + "="*60)
            print("MAIN DETECTION RESULTS")
            print("="*60)
            print(f"Faces detected: {len(faces)}")
            print(f"Bodies detected: {len(bodies)}")
            print("\nPress any key to continue...")
            print("="*60)
            
            # Resize for display if too large
            display_img = result_image.copy()
            height, width = display_img.shape[:2]
            if width > 1200:
                scale = 1200.0 / width
                new_width = 1200
                new_height = int(height * scale)
                display_img = cv2.resize(display_img, (new_width, new_height))
            
            cv2.imshow('Face and Body Detection', display_img)
            cv2.waitKey(0)
            cv2.destroyAllWindows()
        
        # Save main result
        if save_path:
            cv2.imwrite(save_path, result_image)
            print(f"\n✓ Main result saved to: {save_path}")
        
        # Display cropped regions
        if display_crops and (len(face_crops) > 0 or len(body_crops) > 0) and not show_pipeline_steps:
            self.display_cropped_regions(face_crops, body_crops)
        
        # Save cropped regions
        saved_crops = []
        if save_crops and (len(face_crops) > 0 or len(body_crops) > 0):
            print("\n" + "="*60)
            print("SAVING CROPPED REGIONS")
            print("="*60)
            saved_crops = self.save_cropped_regions(face_crops, body_crops)
        
        # Return all results
        return {
            'original_image': image,
            'result_image': result_image,
            'faces': faces,
            'bodies': bodies,
            'face_crops': face_crops,
            'body_crops': body_crops,
            'body_analyses': body_analyses,
            'saved_crops': saved_crops
        }
    
    def process_with_fusion(self, image_path, face_scores=None, display=True, save_path=None,
                           crop_regions=True, display_crops=True, save_crops=False, show_pipeline_steps=False):
        """
        Complete processing pipeline with face-body fusion
        
        Args:
            image_path: Path to input image
            face_scores: Dictionary with face dosha scores (optional)
            display: Whether to display result with bounding boxes
            save_path: Path to save result (optional)
            crop_regions: Whether to crop detected regions
            display_crops: Whether to display cropped regions
            save_crops: Whether to save cropped regions
            show_pipeline_steps: Whether to show step-by-step pipeline visualization
            
        Returns:
            result: Dictionary with all results including fusion
        """
        # First, run standard processing
        result = self.process_image(
            image_path=image_path,
            display=display,
            save_path=save_path,
            crop_regions=crop_regions,
            display_crops=display_crops,
            save_crops=save_crops,
            show_pipeline_steps=show_pipeline_steps
        )
        
        if result is None:
            return None
        
        # Perform fusion if both face and body scores available
        fusion_result = None
        
        if face_scores is not None and len(result['body_analyses']) > 0:
            # Use first body analysis for fusion
            body_scores = result['body_analyses'][0]
            
            print("\n" + "="*60)
            print("PERFORMING FACE-BODY FUSION")
            print("="*60)
            print(f"\nFace Scores: Vata={face_scores.get('vata', 0)}, Pitta={face_scores.get('pitta', 0)}, Kapha={face_scores.get('kapha', 0)}")
            print(f"Body Scores: Vata={body_scores['vata']}, Pitta={body_scores['pitta']}, Kapha={body_scores['kapha']}")
            
            fusion_result = self.fuse_results(face_scores, body_scores)
            result['fusion'] = fusion_result
        elif face_scores is None and len(result['body_analyses']) > 0:
            print("\n⚠ WARNING: Face scores not provided. Fusion skipped.")
            print("  Tip: Provide face_scores parameter for complete fusion.")
        elif len(result['body_analyses']) == 0:
            print("\n⚠ WARNING: No body detected. Fusion skipped.")
        
        return result


def main():
    """
    Main function with example usage
    """
    print("\n" + "="*60)
    print("OPENCV FACE AND BODY DETECTION WITH CROPPING")
    print("="*60)
    print("\nFeatures:")
    print("  • Face detection using Haar Cascade (GREEN boxes)")
    print("  • Body detection using HOG descriptor (BLUE boxes)")
    print("  • Crop detected regions")
    print("  • Display regions separately")
    print("  • Save cropped regions")
    print("  • Visual processing pipeline")
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
    
    # Process image with pipeline visualization
    result = detector.process_image(
        image_path=image_path,
        display=True,
        save_path="result_detection.jpg",
        crop_regions=True,
        display_crops=False,
        save_crops=True,
        show_pipeline_steps=True  # Enable pipeline visualization
    )
    
    if result is not None:
        print("\n" + "="*60)
        print("PROCESSING SUMMARY")
        print("="*60)
        print(f"✓ Faces detected: {len(result['faces'])}")
        print(f"✓ Bodies detected: {len(result['bodies'])}")
        print(f"✓ Face crops: {len(result['face_crops'])}")
        print(f"✓ Body crops: {len(result['body_crops'])}")
        print(f"✓ Body analyses: {len(result['body_analyses'])}")
        print(f"✓ Files saved: {len(result['saved_crops']) + 1}")
        
        # Display Tridosha summary
        if len(result['body_analyses']) > 0:
            print("\n" + "="*60)
            print("TRIDOSHA BODY ANALYSIS SUMMARY")
            print("="*60)
            for i, analysis in enumerate(result['body_analyses']):
                print(f"\nBody {i+1}:")
                print(f"  Ratio: {analysis['ratio']:.3f}")
                print(f"  Vata: {analysis['vata']} | Pitta: {analysis['pitta']} | Kapha: {analysis['kapha']}")
                
                # Determine dominant dosha
                max_score = max(analysis['vata'], analysis['pitta'], analysis['kapha'])
                if analysis['vata'] == max_score:
                    dominant = "Vata (Thin body)"
                elif analysis['pitta'] == max_score:
                    dominant = "Pitta (Medium body)"
                else:
                    dominant = "Kapha (Broad body)"
                print(f"  Dominant: {dominant}")
        
        print("="*60)
        print("\n✓ Processing completed successfully!")
    else:
        print("\n✗ Processing failed!")


def main_with_fusion():
    """
    Main function demonstrating face-body fusion
    """
    print("\n" + "="*60)
    print("FACE-BODY TRIDOSHA FUSION DEMO")
    print("="*60)
    print("\nFeatures:")
    print("  • Face detection and analysis")
    print("  • Body detection and analysis")
    print("  • Weighted fusion (Face: 60%, Body: 40%)")
    print("  • Normalized percentage scores")
    print("  • Dominant dosha determination")
    print("  • Visual processing pipeline")
    print("="*60)
    
    # Initialize detector
    try:
        detector = FaceBodyDetector()
    except Exception as e:
        print(f"\nERROR: Failed to initialize detector: {e}")
        return
    
    # Example image path
    image_path = "test_image.jpg"
    
    # Check if example image exists
    if not os.path.exists(image_path):
        print(f"\n⚠ WARNING: Example image '{image_path}' not found")
        print("\nUsage:")
        print("  1. Place an image file in the same directory")
        print("  2. Update 'image_path' variable with your image filename")
        print("  3. Run the script again")
        return
    
    # Example face scores (replace with actual face analysis results)
    # These would come from your face analysis module
    face_scores = {
        'vata': 3,
        'pitta': 5,
        'kapha': 2
    }
    
    print("\n" + "="*60)
    print("USING EXAMPLE FACE SCORES")
    print("="*60)
    print(f"Face Vata: {face_scores['vata']}")
    print(f"Face Pitta: {face_scores['pitta']}")
    print(f"Face Kapha: {face_scores['kapha']}")
    print("\nNote: Replace with actual face analysis results")
    print("="*60)
    
    # Process with fusion and pipeline visualization
    result = detector.process_with_fusion(
        image_path=image_path,
        face_scores=face_scores,
        display=False,
        save_path="result_fusion.jpg",
        crop_regions=True,
        display_crops=False,
        save_crops=True,
        show_pipeline_steps=True  # Enable pipeline visualization
    )
    
    if result is not None and 'fusion' in result:
        fusion = result['fusion']
        
        print("\n" + "="*60)
        print("✓ FUSION COMPLETED SUCCESSFULLY")
        print("="*60)
        print(f"\nFinal Results:")
        print(f"  Vata:  {fusion['vata_percent']:.2f}%")
        print(f"  Pitta: {fusion['pitta_percent']:.2f}%")
        print(f"  Kapha: {fusion['kapha_percent']:.2f}%")
        print(f"\n  Dominant Dosha: {fusion['dominant_dosha']}")
        print("="*60)
    elif result is not None:
        print("\n⚠ Fusion not performed (missing face or body data)")
    else:
        print("\n✗ Processing failed!")


def test_with_webcam():
    """
    BONUS: Real-time detection using webcam with cropping
    """
    print("\n" + "="*60)
    print("REAL-TIME WEBCAM DETECTION WITH CROPPING")
    print("="*60)
    print("\nControls:")
    print("  • Press 'q' to quit")
    print("  • Press 'c' to capture and crop current frame")
    print("="*60)
    
    # Initialize detector
    detector = FaceBodyDetector()
    
    # Open webcam
    cap = cv2.VideoCapture(0)
    
    if not cap.isOpened():
        print("ERROR: Cannot open webcam")
        return
    
    print("\n✓ Webcam opened successfully")
    print("Processing frames... (Press 'q' to quit, 'c' to capture)")
    
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
            bodies = []
            
            # Draw detections
            frame = detector.draw_detections(frame, faces, bodies)
        
        # Display FPS
        cv2.putText(frame, f'Frame: {frame_count} | Press C to capture', (10, 30),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)
        
        # Show frame
        cv2.imshow('Webcam Detection (Q=Quit, C=Capture)', frame)
        
        # Check for key press
        key = cv2.waitKey(1) & 0xFF
        
        if key == ord('q'):
            break
        elif key == ord('c'):
            # Capture and crop current frame
            print(f"\n📸 Capturing frame {frame_count}...")
            
            # Detect on current frame
            faces = detector.detect_faces(frame)
            bodies = detector.detect_bodies(frame)
            
            if len(faces) > 0 or len(bodies) > 0:
                # Crop regions
                face_crops = detector.crop_all_faces(frame, faces)
                body_crops = detector.crop_all_bodies(frame, bodies)
                
                # Display crops
                detector.display_cropped_regions(face_crops, body_crops, wait_time=1)
                
                # Save crops
                detector.save_cropped_regions(face_crops, body_crops, 
                                            output_dir=f"webcam_capture_{frame_count}")
                print(f"✓ Saved to: webcam_capture_{frame_count}/")
            else:
                print("⚠ No faces or bodies detected in current frame")
    
    # Cleanup
    cap.release()
    cv2.destroyAllWindows()
    print("\n✓ Webcam closed")


# ============================================================================
# EXAMPLE USAGE PATTERNS
# ============================================================================

def example_1_basic_with_crops():
    """Example 1: Basic detection with cropping"""
    detector = FaceBodyDetector()
    result = detector.process_image(
        "photo.jpg",
        crop_regions=True,
        display_crops=True
    )


def example_2_save_all():
    """Example 2: Save everything"""
    detector = FaceBodyDetector()
    result = detector.process_image(
        "photo.jpg",
        display=True,
        save_path="result.jpg",
        crop_regions=True,
        display_crops=True,
        save_crops=True
    )


def example_3_crop_only():
    """Example 3: Only crop and save, no display"""
    detector = FaceBodyDetector()
    result = detector.process_image(
        "photo.jpg",
        display=False,
        crop_regions=True,
        display_crops=False,
        save_crops=True
    )


def example_4_manual_cropping():
    """Example 4: Manual cropping with custom parameters"""
    detector = FaceBodyDetector()
    
    # Load and detect
    image = detector.load_image("photo.jpg")
    faces = detector.detect_faces(image)
    bodies = detector.detect_bodies(image)
    
    # Crop with custom padding
    face_crops = detector.crop_all_faces(image, faces, padding=50)
    body_crops = detector.crop_all_bodies(image, bodies, padding=30)
    
    # Display
    detector.display_cropped_regions(face_crops, body_crops)
    
    # Save to custom directory
    detector.save_cropped_regions(face_crops, body_crops, 
                                 output_dir="my_custom_crops")


def example_5_batch_processing_with_crops():
    """Example 5: Process multiple images and save crops"""
    detector = FaceBodyDetector()
    
    image_files = ["image1.jpg", "image2.jpg", "image3.jpg"]
    
    for img_file in image_files:
        if os.path.exists(img_file):
            print(f"\n{'='*60}")
            print(f"Processing: {img_file}")
            print('='*60)
            
            result = detector.process_image(
                img_file,
                display=False,
                save_path=f"result_{img_file}",
                crop_regions=True,
                display_crops=False,
                save_crops=True
            )
            
            if result:
                # Rename crop directory
                old_dir = "cropped_regions"
                new_dir = f"crops_{img_file.replace('.jpg', '')}"
                if os.path.exists(old_dir):
                    os.rename(old_dir, new_dir)
                    print(f"✓ Crops saved to: {new_dir}/")


def example_6_get_crop_data():
    """Example 6: Access crop data programmatically"""
    detector = FaceBodyDetector()
    
    result = detector.process_image(
        "photo.jpg",
        display=False,
        crop_regions=True,
        display_crops=False
    )
    
    if result:
        # Access face crops
        for crop_data in result['face_crops']:
            idx = crop_data['index']
            bbox = crop_data['bbox']
            img = crop_data['image']
            
            print(f"\nFace {idx+1}:")
            print(f"  Bounding box: {bbox}")
            print(f"  Crop size: {img.shape[1]}x{img.shape[0]}")
            
            # Do something with the crop
            # e.g., face recognition, analysis, etc.
        
        # Access body crops
        for crop_data in result['body_crops']:
            idx = crop_data['index']
            bbox = crop_data['bbox']
            img = crop_data['image']
            
            print(f"\nBody {idx+1}:")
            print(f"  Bounding box: {bbox}")
            print(f"  Crop size: {img.shape[1]}x{img.shape[0]}")


def example_7_fusion_demo():
    """Example 7: Face-Body Fusion"""
    detector = FaceBodyDetector()
    
    # Example face scores from face analysis
    face_scores = {
        'vata': 4,
        'pitta': 6,
        'kapha': 3
    }
    
    # Process with fusion
    result = detector.process_with_fusion(
        image_path="photo.jpg",
        face_scores=face_scores,
        display=True,
        crop_regions=True
    )
    
    if result and 'fusion' in result:
        fusion = result['fusion']
        print(f"\nFinal Dosha: {fusion['dominant_dosha']}")
        print(f"Vata: {fusion['vata_percent']:.2f}%")
        print(f"Pitta: {fusion['pitta_percent']:.2f}%")
        print(f"Kapha: {fusion['kapha_percent']:.2f}%")


def example_8_manual_fusion():
    """Example 8: Manual Fusion Calculation"""
    detector = FaceBodyDetector()
    
    # Face scores
    face_scores = {'vata': 5, 'pitta': 3, 'kapha': 4}
    
    # Body scores
    body_scores = {'vata': 2, 'pitta': 6, 'kapha': 1}
    
    # Perform fusion
    fusion = detector.fuse_results(face_scores, body_scores)
    
    print(f"\nDominant: {fusion['dominant_dosha']}")
    print(f"Percentages: V={fusion['vata_percent']:.1f}% P={fusion['pitta_percent']:.1f}% K={fusion['kapha_percent']:.1f}%")


def example_9_pipeline_visualization():
    """Example 9: Visual Processing Pipeline"""
    detector = FaceBodyDetector()
    
    # Process with step-by-step visualization
    result = detector.process_image(
        image_path="photo.jpg",
        show_pipeline_steps=True,
        display=False,
        display_crops=False
    )
    
    print("\nPipeline visualization complete!")


def example_10_custom_pipeline_delay():
    """Example 10: Custom Pipeline Delay"""
    detector = FaceBodyDetector()
    
    # Load and detect
    image = detector.load_image("photo.jpg")
    faces = detector.detect_faces(image)
    bodies = detector.detect_bodies(image)
    face_crops = detector.crop_all_faces(image, faces)
    body_crops = detector.crop_all_bodies(image, bodies)
    
    # Show pipeline with custom delay (1500ms)
    detector.show_pipeline(image, faces, bodies, face_crops, body_crops, delay=1500)


# ============================================================================
# RUN SCRIPT
# ============================================================================

if __name__ == "__main__":
    # Run main detection with pipeline visualization
    # main()
    
    # Run fusion demo with pipeline
    main_with_fusion()
    
    # Uncomment to test webcam with cropping
    # test_with_webcam()
    
    # Uncomment to run examples
    # example_1_basic_with_crops()
    # example_2_save_all()
    # example_3_crop_only()
    # example_4_manual_cropping()
    # example_5_batch_processing_with_crops()
    # example_6_get_crop_data()
    # example_7_fusion_demo()
    # example_8_manual_fusion()
    # example_9_pipeline_visualization()
    # example_10_custom_pipeline_delay()


# ============================================================================
# INSTALLATION INSTRUCTIONS
# ============================================================================
"""
INSTALLATION:

1. Install OpenCV:
   pip install opencv-python

2. Run script:
   python face_body_detection_extended.py

3. Place test image in same directory as script

4. Update image_path variable with your image filename

NEW FEATURES IN VERSION 3.0:

✓ Body region analysis with Tridosha classification
✓ Face-Body dosha fusion with weighted scoring
✓ Normalized percentage outputs
✓ Dominant dosha determination
✓ Complete Ayurvedic analysis pipeline
✓ Visual processing pipeline with step-by-step display
✓ Configurable delay between pipeline steps
✓ Automatic window management

PREVIOUS FEATURES (VERSION 2.0):

✓ Crop detected face regions
✓ Crop detected body regions
✓ Display cropped regions in separate windows
✓ Save cropped regions to files
✓ Automatic bounds checking
✓ Configurable padding around crops
✓ Batch processing with crops
✓ Webcam capture with cropping

BODY ANALYSIS:

1. analyze_body(body_bbox)
   - Computes body width, height, ratio
   - Classifies body type:
     * ratio < 0.35 → Vata (thin)
     * 0.35 ≤ ratio ≤ 0.5 → Pitta (medium)
     * ratio > 0.5 → Kapha (broad)
   - Returns dosha scores

FUSION ANALYSIS:

1. fuse_results(face_scores, body_scores)
   - Weighted fusion: Face 60%, Body 40%
   - Normalizes to percentages
   - Determines dominant dosha
   - Returns complete fusion results

2. process_with_fusion(image_path, face_scores, ...)
   - Complete pipeline with fusion
   - Integrates face and body analysis
   - Automatic fusion calculation

FUSION FORMULA:

final_vata = (face_vata * 0.6) + (body_vata * 0.4)
final_pitta = (face_pitta * 0.6) + (body_pitta * 0.4)
final_kapha = (face_kapha * 0.6) + (body_kapha * 0.4)

total = final_vata + final_pitta + final_kapha

final_vata_percent = (final_vata / total) * 100
final_pitta_percent = (final_pitta / total) * 100
final_kapha_percent = (final_kapha / total) * 100

VISUAL PIPELINE:

1. show_pipeline(image, faces, bodies, face_crops, body_crops, delay=800)
   - Displays 5-step processing pipeline
   - Step 1: Original Image
   - Step 2: Face Detection (green boxes)
   - Step 3: Body Detection (blue boxes)
   - Step 4: Face Region (cropped)
   - Step 5: Body Region (cropped)
   - Configurable delay between steps
   - Automatic window cleanup

2. Enable in process_image():
   result = detector.process_image(
       image_path="photo.jpg",
       show_pipeline_steps=True
   )

3. Enable in process_with_fusion():
   result = detector.process_with_fusion(
       image_path="photo.jpg",
       face_scores=scores,
       show_pipeline_steps=True
   )

USAGE EXAMPLES:

# Example 1: Basic body analysis
detector = FaceBodyDetector()
result = detector.process_image("photo.jpg")
if result['body_analyses']:
    body = result['body_analyses'][0]
    print(f"Body ratio: {body['ratio']:.3f}")
    print(f"Vata: {body['vata']}, Pitta: {body['pitta']}, Kapha: {body['kapha']}")

# Example 2: Face-Body fusion
face_scores = {'vata': 5, 'pitta': 3, 'kapha': 4}
result = detector.process_with_fusion("photo.jpg", face_scores=face_scores)
if 'fusion' in result:
    fusion = result['fusion']
    print(f"Dominant: {fusion['dominant_dosha']}")
    print(f"Vata: {fusion['vata_percent']:.2f}%")
    print(f"Pitta: {fusion['pitta_percent']:.2f}%")
    print(f"Kapha: {fusion['kapha_percent']:.2f}%")

# Example 3: Manual fusion
face_scores = {'vata': 4, 'pitta': 6, 'kapha': 2}
body_scores = {'vata': 2, 'pitta': 2, 'kapha': 0}
fusion = detector.fuse_results(face_scores, body_scores)

OUTPUT FORMAT:

FINAL DOSHA FUSION RESULTS
============================================================
Weighted Fusion (Face: 60%, Body: 40%):
  Vata:  3.20 → 31.37%
  Pitta: 4.40 → 43.14%
  Kapha: 2.60 → 25.49%

Dominant Dosha: Pitta
============================================================

TROUBLESHOOTING:

• If body not detected:
  - Ensure full body visible in image
  - Try different image resolution
  - Check lighting conditions

• If fusion not performed:
  - Provide face_scores parameter
  - Ensure body detected
  - Check score format: {'vata': x, 'pitta': y, 'kapha': z}

• If ratios seem incorrect:
  - Body ratio depends on bounding box
  - HOG detector may not be perfect
  - Consider manual adjustment

INTEGRATION WITH FACE ANALYSIS:

# Step 1: Get face scores from your face analysis module
from your_face_module import analyze_face
face_scores = analyze_face("photo.jpg")

# Step 2: Run fusion
detector = FaceBodyDetector()
result = detector.process_with_fusion(
    image_path="photo.jpg",
    face_scores=face_scores
)

# Step 3: Get final results
if 'fusion' in result:
    final_dosha = result['fusion']['dominant_dosha']
    percentages = {
        'vata': result['fusion']['vata_percent'],
        'pitta': result['fusion']['pitta_percent'],
        'kapha': result['fusion']['kapha_percent']
    }

PERFORMANCE NOTES:

1. Body detection is slower than face detection
2. Fusion calculation is very fast
3. Use display=False for batch processing
4. Body analysis adds minimal overhead
5. Fusion works with any score range

VERSION HISTORY:

v3.0 - Added body analysis and face-body fusion
v2.0 - Added cropping functionality
v1.0 - Basic face and body detection
"""
