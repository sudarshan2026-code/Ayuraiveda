"""
FACIAL REGION EXTRACTION USING MEDIAPIPE FACE MESH
Complete script for detecting face and extracting 4 facial regions

Requirements:
pip install opencv-python mediapipe numpy

Author: Computer Vision Engineer
Version: 1.0 - Complete Implementation
"""

import cv2
import numpy as np
import mediapipe as mp
from typing import List, Tuple, Dict, Optional
import sys


class FacialRegionExtractor:
    """
    Extract facial regions using MediaPipe Face Mesh
    Divides face into: Forehead, Eyes, Cheeks, Lips+Chin
    """
    
    def __init__(self):
        """Initialize MediaPipe Face Mesh"""
        self.mp_face_mesh = mp.solutions.face_mesh
        self.face_mesh = self.mp_face_mesh.FaceMesh(
            static_image_mode=True,
            max_num_faces=1,
            refine_landmarks=True,
            min_detection_confidence=0.5
        )
        
        # Define landmark indices for each region
        self.region_landmarks = {
            'forehead': [10, 338, 297, 332, 284, 251, 389, 356, 454, 323, 361, 288,
                        397, 365, 379, 378, 400, 377, 152, 148, 176, 149, 150, 136,
                        172, 58, 132, 93, 234, 127, 162, 21, 54, 103, 67, 109],
            
            'left_eye': [33, 7, 163, 144, 145, 153, 154, 155, 133, 173, 157, 158,
                        159, 160, 161, 246, 33, 130, 25, 110, 24, 23, 22, 26, 112,
                        243, 190, 56, 28, 27, 29, 30, 247, 130, 226, 113, 225, 224,
                        223, 222, 221, 189],
            
            'right_eye': [362, 382, 381, 380, 374, 373, 390, 249, 263, 466, 388,
                         387, 386, 385, 384, 398, 362, 359, 255, 339, 254, 253, 252,
                         256, 341, 463, 414, 286, 258, 257, 259, 260, 467, 359, 446,
                         342, 445, 444, 443, 442, 441, 413],
            
            'cheeks': [205, 50, 118, 119, 101, 36, 203, 206, 216, 207, 187, 123,
                      50, 205, 187, 207, 216, 206, 203, 36, 101, 119, 118, 50,
                      425, 280, 347, 348, 330, 266, 423, 426, 436, 427, 411, 352,
                      280, 425, 411, 427, 436, 426, 423, 266, 330, 348, 347, 280,
                      2, 97, 98, 129, 49, 131, 134, 51, 5, 281, 363, 360, 279,
                      420, 429, 358, 327, 326, 2],
            
            'lips_chin': [61, 185, 40, 39, 37, 0, 267, 269, 270, 409, 291, 375,
                         321, 405, 314, 17, 84, 181, 91, 146, 61, 185, 40, 39, 37,
                         0, 267, 269, 270, 409, 291, 78, 95, 88, 178, 87, 14, 317,
                         402, 318, 324, 308, 415, 310, 311, 312, 13, 82, 81, 80,
                         191, 78, 95, 88, 178, 87, 14, 317, 402, 318, 324, 308,
                         415, 310, 311, 312, 13, 82, 81, 80, 191, 78, 152, 148,
                         176, 149, 150, 136, 172, 58, 132, 93, 234, 127, 162]
        }
        
        print("✅ Facial Region Extractor initialized")
        print("📊 Regions: Forehead, Eyes, Cheeks, Lips+Chin")
    
    def load_image(self, image_path: str) -> Optional[np.ndarray]:
        """
        Load image from file path
        
        Args:
            image_path: Path to image file
            
        Returns:
            Image as numpy array or None if failed
        """
        try:
            image = cv2.imread(image_path)
            if image is None:
                print(f"❌ Error: Could not load image from {image_path}")
                return None
            
            print(f"✅ Image loaded: {image.shape[1]}x{image.shape[0]} pixels")
            return image
        except Exception as e:
            print(f"❌ Error loading image: {str(e)}")
            return None
    
    def detect_face(self, image: np.ndarray) -> Optional[Dict]:
        """
        Detect face using MediaPipe Face Mesh
        
        Args:
            image: Input image as numpy array
            
        Returns:
            Dictionary with landmarks or None if no face detected
        """
        try:
            # Convert BGR to RGB
            rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            
            # Process image
            results = self.face_mesh.process(rgb_image)
            
            if not results.multi_face_landmarks:
                print("❌ No face detected in the image")
                return None
            
            print("✅ Face detected successfully")
            return results.multi_face_landmarks[0]
            
        except Exception as e:
            print(f"❌ Error detecting face: {str(e)}")
            return None
    
    def extract_landmarks(self, face_landmarks, image_shape: Tuple[int, int, int]) -> List[Tuple[int, int]]:
        """
        Extract landmark coordinates from MediaPipe results
        
        Args:
            face_landmarks: MediaPipe face landmarks
            image_shape: Shape of the image (height, width, channels)
            
        Returns:
            List of (x, y) coordinates for all 468 landmarks
        """
        h, w, _ = image_shape
        landmarks = []
        
        for landmark in face_landmarks.landmark:
            x = int(landmark.x * w)
            y = int(landmark.y * h)
            landmarks.append((x, y))
        
        print(f"✅ Extracted {len(landmarks)} facial landmarks")
        return landmarks
    
    def get_region_bounds(self, landmarks: List[Tuple[int, int]], 
                         region_indices: List[int]) -> Tuple[int, int, int, int]:
        """
        Get bounding box for a region based on landmark indices
        
        Args:
            landmarks: List of all landmark coordinates
            region_indices: Indices of landmarks for this region
            
        Returns:
            Tuple of (x_min, y_min, x_max, y_max)
        """
        region_points = [landmarks[i] for i in region_indices if i < len(landmarks)]
        
        if not region_points:
            return (0, 0, 0, 0)
        
        x_coords = [p[0] for p in region_points]
        y_coords = [p[1] for p in region_points]
        
        x_min = max(0, min(x_coords) - 10)  # Add padding
        y_min = max(0, min(y_coords) - 10)
        x_max = max(x_coords) + 10
        y_max = max(y_coords) + 10
        
        return (x_min, y_min, x_max, y_max)
    
    def create_region_mask(self, image_shape: Tuple[int, int, int],
                          landmarks: List[Tuple[int, int]],
                          region_indices: List[int]) -> np.ndarray:
        """
        Create a mask for a specific facial region
        
        Args:
            image_shape: Shape of the image
            landmarks: List of all landmark coordinates
            region_indices: Indices of landmarks for this region
            
        Returns:
            Binary mask for the region
        """
        h, w, _ = image_shape
        mask = np.zeros((h, w), dtype=np.uint8)
        
        # Get region points
        region_points = np.array([landmarks[i] for i in region_indices 
                                 if i < len(landmarks)], dtype=np.int32)
        
        if len(region_points) > 0:
            # Create convex hull for the region
            hull = cv2.convexHull(region_points)
            cv2.fillConvexPoly(mask, hull, 255)
        
        return mask
    
    def segment_regions(self, image: np.ndarray, 
                       landmarks: List[Tuple[int, int]]) -> Dict[str, np.ndarray]:
        """
        Segment face into 4 regions
        
        Args:
            image: Input image
            landmarks: List of facial landmarks
            
        Returns:
            Dictionary with region names and cropped images
        """
        regions = {}
        h, w, _ = image.shape
        
        print("\n📐 Segmenting facial regions...")
        
        # Process each region
        for region_name, indices in self.region_landmarks.items():
            # Get bounding box
            x_min, y_min, x_max, y_max = self.get_region_bounds(landmarks, indices)
            
            # Ensure bounds are within image
            x_min = max(0, x_min)
            y_min = max(0, y_min)
            x_max = min(w, x_max)
            y_max = min(h, y_max)
            
            # Crop region
            if x_max > x_min and y_max > y_min:
                cropped = image[y_min:y_max, x_min:x_max].copy()
                regions[region_name] = cropped
                print(f"  ✅ {region_name.upper()}: {cropped.shape[1]}x{cropped.shape[0]} pixels")
            else:
                print(f"  ⚠️ {region_name.upper()}: Invalid bounds, skipping")
        
        return regions
    
    def crop_region(self, image: np.ndarray, 
                   landmarks: List[Tuple[int, int]],
                   region_name: str) -> Optional[np.ndarray]:
        """
        Crop a specific region from the image
        
        Args:
            image: Input image
            landmarks: List of facial landmarks
            region_name: Name of the region to crop
            
        Returns:
            Cropped region image or None
        """
        if region_name not in self.region_landmarks:
            print(f"❌ Unknown region: {region_name}")
            return None
        
        indices = self.region_landmarks[region_name]
        x_min, y_min, x_max, y_max = self.get_region_bounds(landmarks, indices)
        
        h, w, _ = image.shape
        x_min = max(0, x_min)
        y_min = max(0, y_min)
        x_max = min(w, x_max)
        y_max = min(h, y_max)
        
        if x_max > x_min and y_max > y_min:
            return image[y_min:y_max, x_min:x_max].copy()
        
        return None
    
    def display_regions(self, regions: Dict[str, np.ndarray], 
                       save_output: bool = False,
                       output_prefix: str = "region"):
        """
        Display all facial regions
        
        Args:
            regions: Dictionary of region names and images
            save_output: Whether to save images to disk
            output_prefix: Prefix for saved image files
        """
        print("\n🖼️ Displaying facial regions...")
        
        # Create a window for each region
        for region_name, region_image in regions.items():
            if region_image is not None and region_image.size > 0:
                # Create window title
                window_name = f"{region_name.upper().replace('_', ' ')}"
                
                # Display
                cv2.imshow(window_name, region_image)
                print(f"  ✅ Displaying: {window_name}")
                
                # Save if requested
                if save_output:
                    filename = f"{output_prefix}_{region_name}.jpg"
                    cv2.imwrite(filename, region_image)
                    print(f"  💾 Saved: {filename}")
        
        print("\n⌨️ Press any key to close all windows...")
        cv2.waitKey(0)
        cv2.destroyAllWindows()
    
    def draw_landmarks_on_image(self, image: np.ndarray,
                               landmarks: List[Tuple[int, int]],
                               region_name: Optional[str] = None) -> np.ndarray:
        """
        Draw landmarks on image for visualization
        
        Args:
            image: Input image
            landmarks: List of facial landmarks
            region_name: If specified, only draw landmarks for this region
            
        Returns:
            Image with landmarks drawn
        """
        output = image.copy()
        
        if region_name and region_name in self.region_landmarks:
            # Draw only specific region landmarks
            indices = self.region_landmarks[region_name]
            for idx in indices:
                if idx < len(landmarks):
                    x, y = landmarks[idx]
                    cv2.circle(output, (x, y), 2, (0, 255, 0), -1)
        else:
            # Draw all landmarks
            for x, y in landmarks:
                cv2.circle(output, (x, y), 1, (0, 255, 0), -1)
        
        return output
    
    def process_image(self, image_path: str, 
                     display: bool = True,
                     save_output: bool = False,
                     output_prefix: str = "region") -> Optional[Dict[str, np.ndarray]]:
        """
        Complete pipeline: Load, detect, extract, segment, display
        
        Args:
            image_path: Path to input image
            display: Whether to display regions
            save_output: Whether to save region images
            output_prefix: Prefix for saved files
            
        Returns:
            Dictionary of regions or None if failed
        """
        print("=" * 70)
        print("🔍 FACIAL REGION EXTRACTION PIPELINE")
        print("=" * 70)
        
        # Step 1: Load image
        print("\n[1/5] Loading image...")
        image = self.load_image(image_path)
        if image is None:
            return None
        
        # Step 2: Detect face
        print("\n[2/5] Detecting face...")
        face_landmarks = self.detect_face(image)
        if face_landmarks is None:
            return None
        
        # Step 3: Extract landmarks
        print("\n[3/5] Extracting landmarks...")
        landmarks = self.extract_landmarks(face_landmarks, image.shape)
        
        # Step 4: Segment regions
        print("\n[4/5] Segmenting regions...")
        regions = self.segment_regions(image, landmarks)
        
        # Step 5: Display regions
        if display and regions:
            print("\n[5/5] Displaying regions...")
            self.display_regions(regions, save_output, output_prefix)
        
        print("\n" + "=" * 70)
        print("✅ PIPELINE COMPLETE")
        print("=" * 70)
        
        return regions
    
    def create_combined_view(self, image: np.ndarray,
                            regions: Dict[str, np.ndarray]) -> np.ndarray:
        """
        Create a combined view showing all regions
        
        Args:
            image: Original image
            regions: Dictionary of region images
            
        Returns:
            Combined visualization image
        """
        # Calculate layout
        num_regions = len(regions)
        cols = 2
        rows = (num_regions + 1) // 2
        
        # Resize original image
        display_height = 300
        aspect = image.shape[1] / image.shape[0]
        display_width = int(display_height * aspect)
        original_resized = cv2.resize(image, (display_width, display_height))
        
        # Create canvas
        canvas_width = display_width * cols + 20
        canvas_height = display_height * (rows + 1) + 20
        canvas = np.ones((canvas_height, canvas_width, 3), dtype=np.uint8) * 255
        
        # Place original image
        y_offset = 10
        x_offset = (canvas_width - display_width) // 2
        canvas[y_offset:y_offset+display_height, 
               x_offset:x_offset+display_width] = original_resized
        
        # Add label
        cv2.putText(canvas, "ORIGINAL", (x_offset, y_offset - 5),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 0), 2)
        
        # Place regions
        y_offset = display_height + 20
        x_offset = 10
        col = 0
        
        for region_name, region_img in regions.items():
            if region_img is not None and region_img.size > 0:
                # Resize region
                region_resized = cv2.resize(region_img, (display_width, display_height))
                
                # Place on canvas
                canvas[y_offset:y_offset+display_height,
                       x_offset:x_offset+display_width] = region_resized
                
                # Add label
                label = region_name.upper().replace('_', ' ')
                cv2.putText(canvas, label, (x_offset, y_offset - 5),
                           cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 0), 2)
                
                # Update position
                col += 1
                if col >= cols:
                    col = 0
                    y_offset += display_height + 10
                    x_offset = 10
                else:
                    x_offset += display_width + 10
        
        return canvas
    
    def __del__(self):
        """Cleanup"""
        if hasattr(self, 'face_mesh'):
            self.face_mesh.close()


# ============================================================================
# UTILITY FUNCTIONS
# ============================================================================

def print_usage():
    """Print usage instructions"""
    print("""
╔═══════════════════════════════════════════════════════════════════════╗
║                FACIAL REGION EXTRACTION TOOL                          ║
╚═══════════════════════════════════════════════════════════════════════╝

USAGE:
    python facial_region_extraction.py <image_path>

EXAMPLE:
    python facial_region_extraction.py face.jpg

REQUIREMENTS:
    pip install opencv-python mediapipe numpy

REGIONS EXTRACTED:
    1. Forehead
    2. Eyes (left and right)
    3. Cheeks (mid-face)
    4. Lips + Chin

OUTPUT:
    - Displays each region in separate window
    - Press any key to close windows
    - Optional: Save regions to disk
    """)


def main():
    """Main function for command-line usage"""
    print("\n" + "=" * 70)
    print("🌿 FACIAL REGION EXTRACTION USING MEDIAPIPE")
    print("=" * 70)
    
    # Check command line arguments
    if len(sys.argv) < 2:
        print("\n❌ Error: No image path provided")
        print_usage()
        sys.exit(1)
    
    image_path = sys.argv[1]
    
    # Check if save option is provided
    save_output = '--save' in sys.argv
    
    # Initialize extractor
    print("\n🔧 Initializing facial region extractor...")
    extractor = FacialRegionExtractor()
    
    # Process image
    regions = extractor.process_image(
        image_path=image_path,
        display=True,
        save_output=save_output,
        output_prefix="facial_region"
    )
    
    if regions:
        print(f"\n✅ Successfully extracted {len(regions)} facial regions")
        print("\nRegions extracted:")
        for region_name in regions.keys():
            print(f"  • {region_name.upper().replace('_', ' ')}")
    else:
        print("\n❌ Failed to extract facial regions")
        sys.exit(1)


# ============================================================================
# EXAMPLE USAGE
# ============================================================================

if __name__ == "__main__":
    # Check if running from command line
    if len(sys.argv) > 1:
        main()
    else:
        # Example usage in code
        print("\n" + "=" * 70)
        print("📚 EXAMPLE USAGE")
        print("=" * 70)
        
        print("""
# Example 1: Basic usage
from facial_region_extraction import FacialRegionExtractor

extractor = FacialRegionExtractor()
regions = extractor.process_image("face.jpg")

# Example 2: Save regions to disk
extractor = FacialRegionExtractor()
regions = extractor.process_image(
    image_path="face.jpg",
    save_output=True,
    output_prefix="my_face"
)

# Example 3: Process without display
extractor = FacialRegionExtractor()
regions = extractor.process_image(
    image_path="face.jpg",
    display=False
)

# Access individual regions
forehead = regions['forehead']
eyes = regions['left_eye']
cheeks = regions['cheeks']
lips_chin = regions['lips_chin']

# Example 4: Create combined view
extractor = FacialRegionExtractor()
image = extractor.load_image("face.jpg")
face_landmarks = extractor.detect_face(image)
landmarks = extractor.extract_landmarks(face_landmarks, image.shape)
regions = extractor.segment_regions(image, landmarks)
combined = extractor.create_combined_view(image, regions)
cv2.imshow("Combined View", combined)
cv2.waitKey(0)

# Example 5: Draw landmarks
extractor = FacialRegionExtractor()
image = extractor.load_image("face.jpg")
face_landmarks = extractor.detect_face(image)
landmarks = extractor.extract_landmarks(face_landmarks, image.shape)
annotated = extractor.draw_landmarks_on_image(image, landmarks)
cv2.imshow("Landmarks", annotated)
cv2.waitKey(0)
        """)
        
        print("\n" + "=" * 70)
        print("💡 TO RUN FROM COMMAND LINE:")
        print("=" * 70)
        print("\npython facial_region_extraction.py <image_path>")
        print("python facial_region_extraction.py face.jpg --save")
        print("\n" + "=" * 70)
