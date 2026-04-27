"""
FACIAL REGION ANALYSIS WITH TRIDOSHA SCORING
Extended from facial_region_extraction.py

NEW FEATURES:
- Grayscale conversion
- Texture variance using Laplacian
- Face ratio (width/height) analysis
- Tridosha scoring based on texture and face shape

Requirements:
pip install opencv-python mediapipe numpy

Author: Computer Vision Engineer
Version: 2.0 - Extended with Tridosha Analysis
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
        """Load image from file path"""
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
        """Detect face using MediaPipe Face Mesh"""
        try:
            rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
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
        """Extract landmark coordinates from MediaPipe results"""
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
        """Get bounding box for a region based on landmark indices"""
        region_points = [landmarks[i] for i in region_indices if i < len(landmarks)]
        
        if not region_points:
            return (0, 0, 0, 0)
        
        x_coords = [p[0] for p in region_points]
        y_coords = [p[1] for p in region_points]
        
        x_min = max(0, min(x_coords) - 10)
        y_min = max(0, min(y_coords) - 10)
        x_max = max(x_coords) + 10
        y_max = max(y_coords) + 10
        
        return (x_min, y_min, x_max, y_max)
    
    def segment_regions(self, image: np.ndarray, 
                       landmarks: List[Tuple[int, int]]) -> Dict[str, np.ndarray]:
        """Segment face into 4 regions"""
        regions = {}
        h, w, _ = image.shape
        
        print("\n📐 Segmenting facial regions...")
        
        for region_name, indices in self.region_landmarks.items():
            x_min, y_min, x_max, y_max = self.get_region_bounds(landmarks, indices)
            
            x_min = max(0, x_min)
            y_min = max(0, y_min)
            x_max = min(w, x_max)
            y_max = min(h, y_max)
            
            if x_max > x_min and y_max > y_min:
                cropped = image[y_min:y_max, x_min:x_max].copy()
                regions[region_name] = cropped
                print(f"  ✅ {region_name.upper()}: {cropped.shape[1]}x{cropped.shape[0]} pixels")
            else:
                print(f"  ⚠️ {region_name.upper()}: Invalid bounds, skipping")
        
        return regions
    
    def get_face_bounds(self, landmarks: List[Tuple[int, int]]) -> Tuple[int, int, int, int]:
        """Get full face bounding box"""
        x_coords = [p[0] for p in landmarks]
        y_coords = [p[1] for p in landmarks]
        
        x_min = min(x_coords)
        y_min = min(y_coords)
        x_max = max(x_coords)
        y_max = max(y_coords)
        
        return (x_min, y_min, x_max, y_max)
    
    def process_image(self, image_path: str) -> Optional[Tuple[np.ndarray, List[Tuple[int, int]], Dict[str, np.ndarray]]]:
        """Complete pipeline: Load, detect, extract, segment"""
        print("=" * 70)
        print("🔍 FACIAL REGION EXTRACTION PIPELINE")
        print("=" * 70)
        
        print("\n[1/5] Loading image...")
        image = self.load_image(image_path)
        if image is None:
            return None
        
        print("\n[2/5] Detecting face...")
        face_landmarks = self.detect_face(image)
        if face_landmarks is None:
            return None
        
        print("\n[3/5] Extracting landmarks...")
        landmarks = self.extract_landmarks(face_landmarks, image.shape)
        
        print("\n[4/5] Segmenting regions...")
        regions = self.segment_regions(image, landmarks)
        
        print("\n[5/5] Pipeline complete")
        
        return image, landmarks, regions
    
    def __del__(self):
        """Cleanup"""
        if hasattr(self, 'face_mesh'):
            self.face_mesh.close()


# ============================================================================
# NEW: TRIDOSHA ANALYSIS ENGINE
# ============================================================================

class TridoshaFaceAnalyzer:
    """
    Analyze facial features for Tridosha scoring
    
    Analysis includes:
    1. Texture variance (Laplacian) - High=Vata, Medium=Pitta, Smooth=Kapha
    2. Face ratio (width/height) - Thin=Vata, Medium=Pitta, Wide=Kapha
    """
    
    def __init__(self):
        """Initialize analyzer"""
        print("\n✅ Tridosha Face Analyzer initialized")
    
    def convert_to_grayscale(self, image: np.ndarray) -> np.ndarray:
        """Convert image to grayscale"""
        if len(image.shape) == 3:
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            print(f"  ✅ Converted to grayscale: {gray.shape}")
            return gray
        return image
    
    def compute_texture_variance(self, gray_image: np.ndarray) -> float:
        """
        Compute texture variance using Laplacian operator
        
        Higher variance = more texture/roughness = Vata
        Lower variance = smoother skin = Kapha
        """
        laplacian = cv2.Laplacian(gray_image, cv2.CV_64F)
        variance = laplacian.var()
        print(f"  📊 Texture variance (Laplacian): {variance:.2f}")
        return variance
    
    def compute_face_ratio(self, landmarks: List[Tuple[int, int]]) -> float:
        """
        Compute face ratio = width / height
        
        Low ratio (< 0.7) = Thin face = Vata
        Medium ratio (0.7-0.85) = Balanced = Pitta
        High ratio (> 0.85) = Wide face = Kapha
        """
        x_coords = [p[0] for p in landmarks]
        y_coords = [p[1] for p in landmarks]
        
        width = max(x_coords) - min(x_coords)
        height = max(y_coords) - min(y_coords)
        
        ratio = width / height if height > 0 else 0
        print(f"  📊 Face ratio (W/H): {ratio:.3f} (W={width}px, H={height}px)")
        return ratio
    
    def score_texture(self, variance: float) -> Dict[str, float]:
        """
        Score doshas based on texture variance
        
        High texture (>100) → Vata dominant
        Medium texture (30-100) → Pitta dominant
        Smooth texture (<30) → Kapha dominant
        """
        scores = {'vata': 0, 'pitta': 0, 'kapha': 0}
        
        if variance > 100:
            scores['vata'] = 5
            scores['pitta'] = 2
            scores['kapha'] = 1
        elif variance > 30:
            scores['vata'] = 2
            scores['pitta'] = 5
            scores['kapha'] = 2
        else:
            scores['vata'] = 1
            scores['pitta'] = 2
            scores['kapha'] = 5
        
        print(f"  🎯 Texture scores → Vata:{scores['vata']} Pitta:{scores['pitta']} Kapha:{scores['kapha']}")
        return scores
    
    def score_face_ratio(self, ratio: float) -> Dict[str, float]:
        """
        Score doshas based on face ratio
        
        Thin face (<0.7) → Vata dominant
        Medium face (0.7-0.85) → Pitta dominant
        Wide face (>0.85) → Kapha dominant
        """
        scores = {'vata': 0, 'pitta': 0, 'kapha': 0}
        
        if ratio < 0.7:
            scores['vata'] = 5
            scores['pitta'] = 2
            scores['kapha'] = 1
        elif ratio < 0.85:
            scores['vata'] = 2
            scores['pitta'] = 5
            scores['kapha'] = 2
        else:
            scores['vata'] = 1
            scores['pitta'] = 2
            scores['kapha'] = 5
        
        print(f"  🎯 Face ratio scores → Vata:{scores['vata']} Pitta:{scores['pitta']} Kapha:{scores['kapha']}")
        return scores
    
    def analyze_face(self, image: np.ndarray, landmarks: List[Tuple[int, int]]) -> Dict[str, any]:
        """
        Complete face analysis for Tridosha scoring
        
        Returns:
            Dictionary with texture variance, face ratio, and dosha scores
        """
        print("\n" + "=" * 70)
        print("🧠 TRIDOSHA FACE ANALYSIS")
        print("=" * 70)
        
        # Step 1: Convert to grayscale
        print("\n[1/4] Converting to grayscale...")
        gray = self.convert_to_grayscale(image)
        
        # Step 2: Compute texture variance
        print("\n[2/4] Computing texture variance (Laplacian)...")
        texture_variance = self.compute_texture_variance(gray)
        
        # Step 3: Compute face ratio
        print("\n[3/4] Computing face ratio (width/height)...")
        face_ratio = self.compute_face_ratio(landmarks)
        
        # Step 4: Score doshas
        print("\n[4/4] Scoring Tridosha...")
        texture_scores = self.score_texture(texture_variance)
        ratio_scores = self.score_face_ratio(face_ratio)
        
        # Combine scores
        total_scores = {
            'vata': texture_scores['vata'] + ratio_scores['vata'],
            'pitta': texture_scores['pitta'] + ratio_scores['pitta'],
            'kapha': texture_scores['kapha'] + ratio_scores['kapha']
        }
        
        # Calculate percentages
        total = sum(total_scores.values())
        percentages = {
            'vata': (total_scores['vata'] / total * 100) if total > 0 else 0,
            'pitta': (total_scores['pitta'] / total * 100) if total > 0 else 0,
            'kapha': (total_scores['kapha'] / total * 100) if total > 0 else 0
        }
        
        # Determine dominant dosha
        dominant = max(total_scores, key=total_scores.get)
        
        print("\n" + "=" * 70)
        print("📊 FINAL TRIDOSHA SCORES")
        print("=" * 70)
        print(f"\n🔴 VATA:  {total_scores['vata']}/10 ({percentages['vata']:.1f}%)")
        print(f"🟡 PITTA: {total_scores['pitta']}/10 ({percentages['pitta']:.1f}%)")
        print(f"🟢 KAPHA: {total_scores['kapha']}/10 ({percentages['kapha']:.1f}%)")
        print(f"\n🎯 DOMINANT DOSHA: {dominant.upper()}")
        print("=" * 70)
        
        return {
            'texture_variance': texture_variance,
            'face_ratio': face_ratio,
            'texture_scores': texture_scores,
            'ratio_scores': ratio_scores,
            'total_scores': total_scores,
            'percentages': percentages,
            'dominant_dosha': dominant
        }


# ============================================================================
# MAIN EXECUTION
# ============================================================================

def main():
    """Main function for complete face analysis"""
    print("\n" + "=" * 70)
    print("🌿 FACIAL REGION ANALYSIS WITH TRIDOSHA SCORING")
    print("=" * 70)
    
    if len(sys.argv) < 2:
        print("\n❌ Error: No image path provided")
        print("\nUSAGE: python facial_region_analysis.py <image_path>")
        print("EXAMPLE: python facial_region_analysis.py face.jpg")
        sys.exit(1)
    
    image_path = sys.argv[1]
    
    # Step 1: Extract facial regions
    extractor = FacialRegionExtractor()
    result = extractor.process_image(image_path)
    
    if result is None:
        print("\n❌ Failed to process image")
        sys.exit(1)
    
    image, landmarks, regions = result
    
    # Step 2: Analyze face for Tridosha
    analyzer = TridoshaFaceAnalyzer()
    analysis = analyzer.analyze_face(image, landmarks)
    
    print("\n✅ Analysis complete!")
    print("\n💡 TIP: Use these scores in your Ayurvedic assessment system")


if __name__ == "__main__":
    main()
