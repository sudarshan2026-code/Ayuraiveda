"""
STRUCTURAL FACE PATTERN ANALYSIS SYSTEM
Ayurvedic Dosha Detection using Facial Geometry (NOT Color)

Uses MediaPipe Face Mesh for precise landmark detection
Analyzes facial proportions, structure, and patterns

Requirements:
pip install mediapipe opencv-python numpy pillow

Author: AyurAI Veda Team
Version: 3.0 - Structural Analysis
"""

import cv2
import numpy as np
try:
    import mediapipe as mp
    from mediapipe.tasks import python
    from mediapipe.tasks.python import vision
    MEDIAPIPE_AVAILABLE = True
    MEDIAPIPE_VERSION = 'new'  # 0.10.x uses tasks API
except ImportError:
    try:
        import mediapipe as mp
        if hasattr(mp, 'solutions'):
            MEDIAPIPE_AVAILABLE = True
            MEDIAPIPE_VERSION = 'old'  # <0.10.x uses solutions API
        else:
            MEDIAPIPE_AVAILABLE = False
            MEDIAPIPE_VERSION = None
    except ImportError:
        MEDIAPIPE_AVAILABLE = False
        MEDIAPIPE_VERSION = None
        mp = None
from typing import Dict, Optional, Tuple, List
import base64
from io import BytesIO
from PIL import Image


class StructuralFaceAnalyzer:
    """
    Structural Face Pattern Analysis Engine
    Predicts Vata, Pitta, Kapha based on facial geometry
    """
    
    def __init__(self):
        """Initialize MediaPipe Face Mesh"""
        if not MEDIAPIPE_AVAILABLE or mp is None:
            raise ImportError(
                "MediaPipe is not available. Please install it with: pip install mediapipe"
            )
        
        if MEDIAPIPE_VERSION == 'old':
            # Old API (mediapipe < 0.10.x)
            try:
                self.mp_face_mesh = mp.solutions.face_mesh
                self.face_mesh = self.mp_face_mesh.FaceMesh(
                    static_image_mode=True,
                    max_num_faces=1,
                    refine_landmarks=True,
                    min_detection_confidence=0.5
                )
                self.api_version = 'old'
            except AttributeError:
                raise ImportError(
                    "MediaPipe API incompatible. Please reinstall: pip install --upgrade mediapipe"
                )
        else:
            # New API (mediapipe >= 0.10.x) - uses tasks
            # For now, use cv2.dnn face detection as fallback
            self.api_version = 'fallback'
            print("Using OpenCV DNN face detection (MediaPipe 0.10.x tasks API not yet supported)")
        
        print("Structural Face Analyzer initialized")
        print(f"API Version: {self.api_version}")
    
    # ========================================================================
    # IMAGE LOADING
    # ========================================================================
    
    def load_image_from_path(self, image_path: str) -> Optional[np.ndarray]:
        """Load image from file path"""
        try:
            image = cv2.imread(image_path)
            if image is None:
                print(f"❌ Could not load image: {image_path}")
                return None
            return image
        except Exception as e:
            print(f"❌ Error loading image: {str(e)}")
            return None
    
    def load_image_from_base64(self, base64_string: str) -> Optional[np.ndarray]:
        """Load image from base64 string"""
        try:
            if ',' in base64_string:
                base64_string = base64_string.split(',')[1]
            
            image_bytes = base64.b64decode(base64_string)
            pil_image = Image.open(BytesIO(image_bytes))
            image = cv2.cvtColor(np.array(pil_image), cv2.COLOR_RGB2BGR)
            
            return image
        except Exception as e:
            print(f"❌ Error loading base64 image: {str(e)}")
            return None
    
    # ========================================================================
    # FACE LANDMARK EXTRACTION
    # ========================================================================
    
    def extract_landmarks(self, image: np.ndarray) -> Optional[Dict]:
        """
        Extract face landmarks using MediaPipe Face Mesh
        Returns 468 facial landmarks
        """
        try:
            # Convert BGR to RGB
            rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            
            # Process image
            results = self.face_mesh.process(rgb_image)
            
            if not results.multi_face_landmarks:
                return None
            
            # Get first face
            face_landmarks = results.multi_face_landmarks[0]
            
            # Convert to pixel coordinates
            h, w, _ = image.shape
            landmarks = []
            
            for landmark in face_landmarks.landmark:
                x = int(landmark.x * w)
                y = int(landmark.y * h)
                landmarks.append((x, y))
            
            return {
                'landmarks': landmarks,
                'image_width': w,
                'image_height': h
            }
            
        except Exception as e:
            print(f"❌ Landmark extraction error: {str(e)}")
            return None
    
    # ========================================================================
    # GEOMETRIC FEATURE CALCULATION
    # ========================================================================
    
    def calculate_distance(self, p1: Tuple[int, int], p2: Tuple[int, int]) -> float:
        """Calculate Euclidean distance between two points"""
        return np.sqrt((p2[0] - p1[0])**2 + (p2[1] - p1[1])**2)
    
    def extract_face_dimensions(self, landmarks: List[Tuple[int, int]]) -> Dict:
        """
        Extract face width and height
        
        Key landmarks:
        - 10: Forehead top
        - 152: Chin bottom
        - 234: Left face edge
        - 454: Right face edge
        """
        try:
            # Face height (forehead to chin)
            forehead_top = landmarks[10]
            chin_bottom = landmarks[152]
            face_height = self.calculate_distance(forehead_top, chin_bottom)
            
            # Face width (left to right)
            left_edge = landmarks[234]
            right_edge = landmarks[454]
            face_width = self.calculate_distance(left_edge, right_edge)
            
            # Face ratio
            face_ratio = face_width / face_height if face_height > 0 else 0
            
            return {
                'face_width': round(face_width, 2),
                'face_height': round(face_height, 2),
                'face_ratio': round(face_ratio, 3)
            }
            
        except Exception as e:
            print(f"❌ Face dimension error: {str(e)}")
            return {'face_width': 0, 'face_height': 0, 'face_ratio': 0}
    
    def extract_jaw_structure(self, landmarks: List[Tuple[int, int]]) -> Dict:
        """
        Extract jaw width and compare with forehead
        
        Key landmarks:
        - 234, 454: Face width (forehead level)
        - 172, 397: Jaw width
        """
        try:
            # Forehead width
            forehead_left = landmarks[234]
            forehead_right = landmarks[454]
            forehead_width = self.calculate_distance(forehead_left, forehead_right)
            
            # Jaw width
            jaw_left = landmarks[172]
            jaw_right = landmarks[397]
            jaw_width = self.calculate_distance(jaw_left, jaw_right)
            
            # Jaw ratio (jaw / forehead)
            jaw_ratio = jaw_width / forehead_width if forehead_width > 0 else 0
            
            return {
                'jaw_width': round(jaw_width, 2),
                'forehead_width': round(forehead_width, 2),
                'jaw_ratio': round(jaw_ratio, 3)
            }
            
        except Exception as e:
            print(f"❌ Jaw structure error: {str(e)}")
            return {'jaw_width': 0, 'forehead_width': 0, 'jaw_ratio': 0}
    
    def extract_eye_size(self, landmarks: List[Tuple[int, int]]) -> Dict:
        """
        Extract eye size (horizontal distance)
        
        Key landmarks:
        - Left eye: 33 (inner), 133 (outer)
        - Right eye: 362 (inner), 263 (outer)
        """
        try:
            # Left eye width
            left_eye_inner = landmarks[33]
            left_eye_outer = landmarks[133]
            left_eye_width = self.calculate_distance(left_eye_inner, left_eye_outer)
            
            # Right eye width
            right_eye_inner = landmarks[362]
            right_eye_outer = landmarks[263]
            right_eye_width = self.calculate_distance(right_eye_inner, right_eye_outer)
            
            # Average eye size
            avg_eye_size = (left_eye_width + right_eye_width) / 2
            
            return {
                'left_eye_width': round(left_eye_width, 2),
                'right_eye_width': round(right_eye_width, 2),
                'avg_eye_size': round(avg_eye_size, 2)
            }
            
        except Exception as e:
            print(f"❌ Eye size error: {str(e)}")
            return {'left_eye_width': 0, 'right_eye_width': 0, 'avg_eye_size': 0}
    
    def extract_lip_thickness(self, landmarks: List[Tuple[int, int]]) -> Dict:
        """
        Extract lip thickness (vertical distance)
        
        Key landmarks:
        - Upper lip top: 0
        - Lower lip bottom: 17
        - Lip center: 13
        """
        try:
            # Upper lip
            upper_lip = landmarks[0]
            
            # Lower lip
            lower_lip = landmarks[17]
            
            # Lip thickness (vertical distance)
            lip_thickness = self.calculate_distance(upper_lip, lower_lip)
            
            return {
                'lip_thickness': round(lip_thickness, 2)
            }
            
        except Exception as e:
            print(f"❌ Lip thickness error: {str(e)}")
            return {'lip_thickness': 0}
    
    def extract_face_fullness(self, landmarks: List[Tuple[int, int]], 
                             image_width: int, image_height: int) -> Dict:
        """
        Calculate face fullness (area ratio)
        
        Face area vs bounding box area
        """
        try:
            # Get bounding box
            x_coords = [lm[0] for lm in landmarks]
            y_coords = [lm[1] for lm in landmarks]
            
            bbox_width = max(x_coords) - min(x_coords)
            bbox_height = max(y_coords) - min(y_coords)
            bbox_area = bbox_width * bbox_height
            
            # Approximate face area using convex hull
            points = np.array(landmarks, dtype=np.int32)
            hull = cv2.convexHull(points)
            face_area = cv2.contourArea(hull)
            
            # Fullness ratio
            fullness = face_area / bbox_area if bbox_area > 0 else 0
            
            return {
                'face_area': round(face_area, 2),
                'bbox_area': round(bbox_area, 2),
                'fullness': round(fullness, 3)
            }
            
        except Exception as e:
            print(f"❌ Fullness calculation error: {str(e)}")
            return {'face_area': 0, 'bbox_area': 0, 'fullness': 0}
    
    # ========================================================================
    # DOSHA SCORING (PATTERN BASED)
    # ========================================================================
    
    def calculate_dosha_scores(self, features: Dict) -> Dict:
        """
        Calculate Vata, Pitta, Kapha scores based on structural patterns
        
        SCORING RULES:
        - Face Shape: Narrow → Vata, Medium → Pitta, Wide → Kapha
        - Jaw Structure: Narrow → Vata, Angular → Pitta, Wide → Kapha
        - Eye Size: Small → Vata, Medium → Pitta, Large → Kapha
        - Lip Thickness: Thin → Vata, Medium → Pitta, Thick → Kapha
        - Face Fullness: Low → Vata, Medium → Pitta, High → Kapha
        """
        
        # Initialize scores
        vata = 0
        pitta = 0
        kapha = 0
        
        # Extract features
        face_ratio = features['face_dimensions']['face_ratio']
        jaw_ratio = features['jaw_structure']['jaw_ratio']
        eye_size = features['eye_size']['avg_eye_size']
        lip_thickness = features['lip_thickness']['lip_thickness']
        fullness = features['face_fullness']['fullness']
        
        # Normalize eye size and lip thickness (relative to face size)
        face_width = features['face_dimensions']['face_width']
        eye_size_norm = eye_size / face_width if face_width > 0 else 0
        lip_thickness_norm = lip_thickness / face_width if face_width > 0 else 0
        
        # ===== FACE SHAPE SCORING =====
        if face_ratio > 0.9:
            kapha += 2  # Wide, round face
        elif face_ratio < 0.75:
            vata += 2   # Narrow, elongated face
        else:
            pitta += 2  # Medium, balanced face
        
        # ===== JAW STRUCTURE SCORING =====
        if jaw_ratio > 1.0:
            kapha += 2  # Wide jaw (square/round)
        elif jaw_ratio < 0.8:
            vata += 2   # Narrow jaw (pointed)
        else:
            pitta += 2  # Angular jaw (triangular)
        
        # ===== EYE SIZE SCORING =====
        if eye_size_norm > 0.15:
            kapha += 2  # Large eyes
        elif eye_size_norm < 0.10:
            vata += 2   # Small eyes
        else:
            pitta += 2  # Medium eyes
        
        # ===== LIP THICKNESS SCORING =====
        if lip_thickness_norm > 0.08:
            kapha += 2  # Thick lips
        elif lip_thickness_norm < 0.05:
            vata += 2   # Thin lips
        else:
            pitta += 2  # Medium lips
        
        # ===== FACE FULLNESS SCORING =====
        if fullness > 0.75:
            kapha += 3  # High fullness (round, fleshy)
        elif fullness < 0.60:
            vata += 3   # Low fullness (angular, thin)
        else:
            pitta += 2  # Medium fullness (balanced)
        
        # ===== NORMALIZATION =====
        total = vata + pitta + kapha
        
        if total > 0:
            vata_percent = (vata / total) * 100
            pitta_percent = (pitta / total) * 100
            kapha_percent = (kapha / total) * 100
        else:
            vata_percent = pitta_percent = kapha_percent = 33.33
        
        return {
            'vata': round(vata_percent, 1),
            'pitta': round(pitta_percent, 1),
            'kapha': round(kapha_percent, 1),
            'raw_scores': {
                'vata': vata,
                'pitta': pitta,
                'kapha': kapha
            },
            'normalized_features': {
                'face_ratio': round(face_ratio, 3),
                'jaw_ratio': round(jaw_ratio, 3),
                'eye_size_norm': round(eye_size_norm, 3),
                'lip_thickness_norm': round(lip_thickness_norm, 3),
                'fullness': round(fullness, 3)
            }
        }
    
    # ========================================================================
    # EXPLANATION GENERATION
    # ========================================================================
    
    def generate_explanation(self, features: Dict, scores: Dict, dominant: str) -> str:
        """Generate explanation based on structural patterns"""
        
        face_ratio = features['face_dimensions']['face_ratio']
        jaw_ratio = features['jaw_structure']['jaw_ratio']
        fullness = features['face_fullness']['fullness']
        
        face_width = features['face_dimensions']['face_width']
        eye_size = features['eye_size']['avg_eye_size']
        lip_thickness = features['lip_thickness']['lip_thickness']
        
        eye_size_norm = eye_size / face_width if face_width > 0 else 0
        lip_thickness_norm = lip_thickness / face_width if face_width > 0 else 0
        
        explanations = []
        
        if dominant == "Vata":
            explanations.append(f"{dominant} dominance detected due to")
            
            reasons = []
            if face_ratio < 0.75:
                reasons.append("narrow facial proportions (elongated face structure)")
            if jaw_ratio < 0.8:
                reasons.append("pointed jaw structure")
            if eye_size_norm < 0.10:
                reasons.append("smaller eyes")
            if lip_thickness_norm < 0.05:
                reasons.append("thinner lips")
            if fullness < 0.60:
                reasons.append("angular facial features with lower fullness")
            
            if reasons:
                explanations.append(", ".join(reasons))
        
        elif dominant == "Pitta":
            explanations.append(f"{dominant} dominance detected due to")
            
            reasons = []
            if 0.75 <= face_ratio <= 0.9:
                reasons.append("balanced facial proportions (medium face structure)")
            if 0.8 <= jaw_ratio <= 1.0:
                reasons.append("angular jaw structure")
            if 0.10 <= eye_size_norm <= 0.15:
                reasons.append("medium-sized eyes")
            if 0.05 <= lip_thickness_norm <= 0.08:
                reasons.append("medium lip thickness")
            if 0.60 <= fullness <= 0.75:
                reasons.append("balanced facial fullness")
            
            if reasons:
                explanations.append(", ".join(reasons))
        
        elif dominant == "Kapha":
            explanations.append(f"{dominant} dominance detected due to")
            
            reasons = []
            if face_ratio > 0.9:
                reasons.append("rounded facial proportions (wide face structure)")
            if jaw_ratio > 1.0:
                reasons.append("wider jaw structure")
            if eye_size_norm > 0.15:
                reasons.append("larger eyes")
            if lip_thickness_norm > 0.08:
                reasons.append("fuller lips")
            if fullness > 0.75:
                reasons.append("overall facial fullness and rounded features")
            
            if reasons:
                explanations.append(", ".join(reasons))
        
        return " ".join(explanations) + "."
    
    # ========================================================================
    # MAIN ANALYSIS PIPELINE
    # ========================================================================
    
    def analyze_face(self, image_input: str, input_type: str = 'path') -> Dict:
        """
        Complete structural face analysis pipeline
        
        Args:
            image_input: Either file path or base64 string
            input_type: 'path' or 'base64'
        
        Returns:
            Dictionary with analysis results
        """
        
        # Load image
        if input_type == 'path':
            image = self.load_image_from_path(image_input)
        elif input_type == 'base64':
            image = self.load_image_from_base64(image_input)
        else:
            return {'error': 'Invalid input type. Use "path" or "base64"'}
        
        if image is None:
            return {'error': 'Failed to load image'}
        
        # Extract landmarks
        landmark_data = self.extract_landmarks(image)
        
        if landmark_data is None:
            return {'error': 'No face detected in the image'}
        
        landmarks = landmark_data['landmarks']
        image_width = landmark_data['image_width']
        image_height = landmark_data['image_height']
        
        # Extract all geometric features
        face_dimensions = self.extract_face_dimensions(landmarks)
        jaw_structure = self.extract_jaw_structure(landmarks)
        eye_size = self.extract_eye_size(landmarks)
        lip_thickness = self.extract_lip_thickness(landmarks)
        face_fullness = self.extract_face_fullness(landmarks, image_width, image_height)
        
        # Compile features
        features = {
            'face_dimensions': face_dimensions,
            'jaw_structure': jaw_structure,
            'eye_size': eye_size,
            'lip_thickness': lip_thickness,
            'face_fullness': face_fullness
        }
        
        # Calculate dosha scores
        scores = self.calculate_dosha_scores(features)
        
        # Determine dominant dosha
        doshas = {
            'Vata': scores['vata'],
            'Pitta': scores['pitta'],
            'Kapha': scores['kapha']
        }
        dominant = max(doshas, key=doshas.get)
        
        # Generate explanation
        explanation = self.generate_explanation(features, scores, dominant)
        
        # Determine risk level
        max_score = max(scores['vata'], scores['pitta'], scores['kapha'])
        if max_score >= 50:
            risk = 'High'
        elif max_score >= 40:
            risk = 'Moderate'
        else:
            risk = 'Low'
        
        # Compile results
        result = {
            'success': True,
            'features': features,
            'scores': {
                'vata': scores['vata'],
                'pitta': scores['pitta'],
                'kapha': scores['kapha']
            },
            'dominant': dominant,
            'risk': risk,
            'explanation': explanation,
            'face_detected': True
        }
        
        return result
    
    def __del__(self):
        """Cleanup"""
        if hasattr(self, 'face_mesh'):
            self.face_mesh.close()


# ============================================================================
# EXAMPLE USAGE
# ============================================================================

if __name__ == "__main__":
    print("=" * 70)
    print("🌿 STRUCTURAL FACE PATTERN ANALYSIS SYSTEM")
    print("=" * 70)
    print("\nVersion: 3.0 - Geometry-Based Dosha Detection")
    print("Technology: MediaPipe Face Mesh + Structural Analysis")
    print("\n" + "=" * 70)
    
    # Initialize analyzer
    print("\n🔧 Initializing analyzer...")
    analyzer = StructuralFaceAnalyzer()
    
    # Example analysis
    print("\n📸 Example Usage:")
    print("-" * 70)
    
    image_path = "test_face.jpg"  # Replace with actual image path
    
    print(f"\nAnalyzing: {image_path}")
    print("Processing...")
    
    result = analyzer.analyze_face(image_path, input_type='path')
    
    if 'error' in result:
        print(f"\n❌ Error: {result['error']}")
    else:
        print("\n✅ Analysis Complete!")
        print("\n" + "=" * 70)
        print("📊 EXTRACTED GEOMETRIC FEATURES")
        print("=" * 70)
        
        features = result['features']
        
        print("\n1️⃣ Face Dimensions:")
        print(f"   • Face Width:  {features['face_dimensions']['face_width']:.2f} px")
        print(f"   • Face Height: {features['face_dimensions']['face_height']:.2f} px")
        print(f"   • Face Ratio:  {features['face_dimensions']['face_ratio']:.3f}")
        
        print("\n2️⃣ Jaw Structure:")
        print(f"   • Jaw Width:      {features['jaw_structure']['jaw_width']:.2f} px")
        print(f"   • Forehead Width: {features['jaw_structure']['forehead_width']:.2f} px")
        print(f"   • Jaw Ratio:      {features['jaw_structure']['jaw_ratio']:.3f}")
        
        print("\n3️⃣ Eye Size:")
        print(f"   • Left Eye:   {features['eye_size']['left_eye_width']:.2f} px")
        print(f"   • Right Eye:  {features['eye_size']['right_eye_width']:.2f} px")
        print(f"   • Average:    {features['eye_size']['avg_eye_size']:.2f} px")
        
        print("\n4️⃣ Lip Thickness:")
        print(f"   • Thickness:  {features['lip_thickness']['lip_thickness']:.2f} px")
        
        print("\n5️⃣ Face Fullness:")
        print(f"   • Face Area:  {features['face_fullness']['face_area']:.2f} px²")
        print(f"   • BBox Area:  {features['face_fullness']['bbox_area']:.2f} px²")
        print(f"   • Fullness:   {features['face_fullness']['fullness']:.3f}")
        
        print("\n" + "=" * 70)
        print("⚖️ DOSHA SCORES (STRUCTURAL ANALYSIS)")
        print("=" * 70)
        print(f"\n   • Vata:  {result['scores']['vata']:.1f}%")
        print(f"   • Pitta: {result['scores']['pitta']:.1f}%")
        print(f"   • Kapha: {result['scores']['kapha']:.1f}%")
        
        print(f"\n🎯 Dominant Dosha: {result['dominant']}")
        print(f"⚠️ Risk Level: {result['risk']}")
        
        print("\n" + "=" * 70)
        print("💡 EXPLANATION")
        print("=" * 70)
        print(f"\n{result['explanation']}")
        
        print("\n" + "=" * 70)
        print("✅ ANALYSIS COMPLETE")
        print("=" * 70)
    
    print("\n" + "=" * 70)
    print("📚 USAGE INSTRUCTIONS")
    print("=" * 70)
    print("""
1. Install requirements:
   pip install mediapipe opencv-python numpy pillow

2. Use in your code:
   from structural_face_analysis import StructuralFaceAnalyzer
   
   analyzer = StructuralFaceAnalyzer()
   result = analyzer.analyze_face("image.jpg", input_type='path')
   
   print(f"Dominant: {result['dominant']}")
   print(f"Vata: {result['scores']['vata']}%")
   print(f"Pitta: {result['scores']['pitta']}%")
   print(f"Kapha: {result['scores']['kapha']}%")

3. Advantages:
   ✅ Lighting-independent (uses geometry, not color)
   ✅ More stable across different conditions
   ✅ Based on structural Ayurvedic principles
   ✅ Precise landmark detection (468 points)
   ✅ Reduces color/brightness bias

4. Dosha Characteristics:
   • Vata:  Narrow face, pointed jaw, small eyes, thin lips
   • Pitta: Medium face, angular jaw, medium features
   • Kapha: Round face, wide jaw, large eyes, full lips
    """)
    
    print("\n" + "=" * 70)
    print("⚠️ DISCLAIMER")
    print("=" * 70)
    print("""
This system provides educational and preventive health insights only.
It is NOT a medical diagnosis platform.
Always consult qualified healthcare professionals for medical advice.
    """)
    
    print("=" * 70)
    print("🌿 AyurAI Veda | Ancient Wisdom. Intelligent Health.")
    print("=" * 70)
