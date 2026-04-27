"""
VISUAL FACE ANALYSIS SYSTEM WITH IMAGE ENHANCEMENT
Complete standalone application with step-by-step processing visualization

Requirements:
pip install opencv-python mediapipe numpy

Author: Senior Computer Vision Engineer
Version: 1.0 - Complete Implementation
"""

import cv2
import numpy as np
import mediapipe as mp
from typing import Dict, Tuple, Optional
import sys


class VisualFaceAnalyzer:
    """
    Enhanced Face Analysis with Visual Processing Pipeline
    Shows each step of image enhancement and texture extraction
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
        
        print("=" * 70)
        print("🌿 VISUAL FACE ANALYSIS SYSTEM")
        print("=" * 70)
        print("✅ MediaPipe Face Mesh initialized")
        print("📊 Features: Image Enhancement + Texture Analysis")
        print("=" * 70)
    
    def load_image(self, image_path: str) -> Optional[np.ndarray]:
        """Load image from file path"""
        try:
            image = cv2.imread(image_path)
            if image is None:
                print(f"❌ Error: Could not load image from {image_path}")
                return None
            
            print(f"\n✅ Image loaded: {image.shape[1]}x{image.shape[0]} pixels")
            return image
        except Exception as e:
            print(f"❌ Error loading image: {str(e)}")
            return None
    
    def display_step(self, image: np.ndarray, title: str, wait_time: int = 1500):
        """
        Display processing step with title
        
        Args:
            image: Image to display
            title: Window title
            wait_time: Time to display in milliseconds (1500ms = 1.5s)
        """
        # Resize for display if too large
        display_image = image.copy()
        max_width = 800
        max_height = 600
        
        h, w = display_image.shape[:2]
        if w > max_width or h > max_height:
            scale = min(max_width / w, max_height / h)
            new_w = int(w * scale)
            new_h = int(h * scale)
            display_image = cv2.resize(display_image, (new_w, new_h))
        
        # Add title text to image
        title_image = display_image.copy()
        cv2.putText(title_image, title, (10, 30), 
                   cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        
        cv2.imshow("Face Analysis Pipeline", title_image)
        cv2.waitKey(wait_time)
        
        print(f"   📸 Displaying: {title}")
    
    def detect_face(self, image: np.ndarray) -> Optional[Dict]:
        """
        Detect face using MediaPipe Face Mesh
        
        Returns:
            Dictionary with face region and landmarks
        """
        try:
            # Convert BGR to RGB
            rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            
            # Process image
            results = self.face_mesh.process(rgb_image)
            
            if not results.multi_face_landmarks:
                print("❌ No face detected in the image")
                return None
            
            # Get landmarks
            face_landmarks = results.multi_face_landmarks[0]
            
            # Get image dimensions
            h, w, _ = image.shape
            
            # Extract landmark coordinates
            landmarks = []
            for landmark in face_landmarks.landmark:
                x = int(landmark.x * w)
                y = int(landmark.y * h)
                landmarks.append((x, y))
            
            # Get bounding box
            x_coords = [lm[0] for lm in landmarks]
            y_coords = [lm[1] for lm in landmarks]
            
            x_min = max(0, min(x_coords) - 20)
            y_min = max(0, min(y_coords) - 20)
            x_max = min(w, max(x_coords) + 20)
            y_max = min(h, max(y_coords) + 20)
            
            # Crop face region
            face_region = image[y_min:y_max, x_min:x_max].copy()
            
            print(f"✅ Face detected: {len(landmarks)} landmarks")
            print(f"   Face region: {face_region.shape[1]}x{face_region.shape[0]} pixels")
            
            return {
                'face_region': face_region,
                'landmarks': landmarks,
                'bbox': (x_min, y_min, x_max, y_max),
                'width': x_max - x_min,
                'height': y_max - y_min
            }
            
        except Exception as e:
            print(f"❌ Error detecting face: {str(e)}")
            return None
    
    def enhance_image(self, image: np.ndarray) -> Dict[str, np.ndarray]:
        """
        Apply image enhancement filters
        
        Returns:
            Dictionary with enhanced images at each step
        """
        enhanced_images = {}
        
        print("\n🔧 Applying image enhancement filters...")
        
        # Step 1: Convert to grayscale
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        enhanced_images['grayscale'] = gray
        print("   ✅ Grayscale conversion")
        
        # Step 2: Histogram equalization (improves contrast)
        equalized = cv2.equalizeHist(gray)
        enhanced_images['equalized'] = equalized
        print("   ✅ Histogram equalization")
        
        # Step 3: Sharpening filter
        kernel_sharpen = np.array([
            [0, -1, 0],
            [-1, 5, -1],
            [0, -1, 0]
        ])
        sharpened = cv2.filter2D(equalized, -1, kernel_sharpen)
        enhanced_images['sharpened'] = sharpened
        print("   ✅ Sharpening filter")
        
        # Step 4: Gaussian blur (slight smoothing to reduce noise)
        blurred = cv2.GaussianBlur(sharpened, (3, 3), 0)
        enhanced_images['blurred'] = blurred
        print("   ✅ Gaussian blur")
        
        # Final enhanced image
        enhanced_images['final'] = blurred
        
        return enhanced_images
    
    def extract_texture(self, image: np.ndarray) -> Dict:
        """
        Extract skin texture patterns using Laplacian
        
        Returns:
            Dictionary with texture metrics
        """
        print("\n🔬 Extracting skin texture patterns...")
        
        # Convert to grayscale if needed
        if len(image.shape) == 3:
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        else:
            gray = image
        
        # Apply Laplacian operator for texture detection
        laplacian = cv2.Laplacian(gray, cv2.CV_64F)
        
        # Compute texture variance
        texture_variance = float(laplacian.var())
        
        # Compute texture mean (average roughness)
        texture_mean = float(np.abs(laplacian).mean())
        
        # Compute texture standard deviation
        texture_std = float(laplacian.std())
        
        # Create texture map for visualization
        texture_map = np.abs(laplacian)
        texture_map = cv2.normalize(texture_map, None, 0, 255, cv2.NORM_MINMAX)
        texture_map = texture_map.astype(np.uint8)
        
        # Apply colormap for better visualization
        texture_map_colored = cv2.applyColorMap(texture_map, cv2.COLORMAP_JET)
        
        print(f"   ✅ Texture variance: {texture_variance:.2f}")
        print(f"   ✅ Texture mean: {texture_mean:.2f}")
        print(f"   ✅ Texture std: {texture_std:.2f}")
        
        return {
            'variance': texture_variance,
            'mean': texture_mean,
            'std': texture_std,
            'texture_map': texture_map,
            'texture_map_colored': texture_map_colored,
            'laplacian': laplacian
        }
    
    def calculate_face_structure(self, face_data: Dict) -> Dict:
        """
        Calculate face structural measurements
        
        Returns:
            Dictionary with structural metrics
        """
        print("\n📐 Calculating face structure...")
        
        width = face_data['width']
        height = face_data['height']
        
        # Calculate face ratio
        face_ratio = width / height if height > 0 else 0
        
        # Classify face shape
        if face_ratio < 0.75:
            face_shape = "Narrow (Elongated)"
        elif face_ratio > 0.9:
            face_shape = "Wide (Round)"
        else:
            face_shape = "Medium (Balanced)"
        
        print(f"   ✅ Face width: {width} pixels")
        print(f"   ✅ Face height: {height} pixels")
        print(f"   ✅ Face ratio: {face_ratio:.3f}")
        print(f"   ✅ Face shape: {face_shape}")
        
        return {
            'width': width,
            'height': height,
            'ratio': face_ratio,
            'shape': face_shape
        }
    
    def calculate_dosha_scores(self, texture_data: Dict, structure_data: Dict) -> Dict:
        """
        Calculate dosha scores based on texture and structure
        
        Scoring Logic:
        - Texture variance indicates skin roughness/smoothness
        - Face ratio indicates body constitution
        
        Returns:
            Dictionary with dosha scores
        """
        print("\n⚖️ Calculating dosha scores...")
        
        # Initialize scores
        vata = 0
        pitta = 0
        kapha = 0
        
        texture_variance = texture_data['variance']
        face_ratio = structure_data['ratio']
        
        # TEXTURE-BASED SCORING
        print("\n   📊 Texture Analysis:")
        if texture_variance > 120:
            vata += 2
            print(f"      High texture variance ({texture_variance:.2f}) → Vata +2")
            print("      (Rough, dry skin characteristic)")
        elif texture_variance >= 60:
            pitta += 2
            print(f"      Medium texture variance ({texture_variance:.2f}) → Pitta +2")
            print("      (Moderate skin texture)")
        else:
            kapha += 2
            print(f"      Low texture variance ({texture_variance:.2f}) → Kapha +2")
            print("      (Smooth, oily skin characteristic)")
        
        # STRUCTURE-BASED SCORING
        print("\n   📊 Structure Analysis:")
        if face_ratio < 0.75:
            vata += 2
            print(f"      Narrow face ratio ({face_ratio:.3f}) → Vata +2")
            print("      (Thin, elongated face structure)")
        elif face_ratio > 0.9:
            kapha += 2
            print(f"      Wide face ratio ({face_ratio:.3f}) → Kapha +2")
            print("      (Round, wide face structure)")
        else:
            pitta += 2
            print(f"      Medium face ratio ({face_ratio:.3f}) → Pitta +2")
            print("      (Balanced face structure)")
        
        # ADDITIONAL TEXTURE METRICS
        texture_mean = texture_data['mean']
        if texture_mean > 15:
            vata += 1
            print(f"      High texture roughness ({texture_mean:.2f}) → Vata +1")
        elif texture_mean < 8:
            kapha += 1
            print(f"      Low texture roughness ({texture_mean:.2f}) → Kapha +1")
        else:
            pitta += 1
            print(f"      Medium texture roughness ({texture_mean:.2f}) → Pitta +1")
        
        # NORMALIZATION
        total = vata + pitta + kapha
        
        if total > 0:
            vata_percent = (vata / total) * 100
            pitta_percent = (pitta / total) * 100
            kapha_percent = (kapha / total) * 100
        else:
            vata_percent = pitta_percent = kapha_percent = 33.33
        
        # Determine dominant dosha
        doshas = {
            'Vata': vata_percent,
            'Pitta': pitta_percent,
            'Kapha': kapha_percent
        }
        dominant = max(doshas, key=doshas.get)
        
        print(f"\n   ✅ Raw scores: Vata={vata}, Pitta={pitta}, Kapha={kapha}")
        print(f"   ✅ Normalized: Vata={vata_percent:.1f}%, Pitta={pitta_percent:.1f}%, Kapha={kapha_percent:.1f}%")
        print(f"   ✅ Dominant dosha: {dominant}")
        
        return {
            'vata': round(vata_percent, 1),
            'pitta': round(pitta_percent, 1),
            'kapha': round(kapha_percent, 1),
            'dominant': dominant,
            'raw_scores': {
                'vata': vata,
                'pitta': pitta,
                'kapha': kapha
            }
        }
    
    def generate_explanation(self, scores: Dict, texture_data: Dict, structure_data: Dict) -> str:
        """Generate explanation for dosha determination"""
        dominant = scores['dominant']
        texture_variance = texture_data['variance']
        face_ratio = structure_data['ratio']
        
        explanation = f"{dominant} dominance detected based on:\n"
        
        if dominant == 'Vata':
            explanation += f"   • High skin texture variance ({texture_variance:.2f}) indicating rough, dry skin\n"
            if face_ratio < 0.75:
                explanation += f"   • Narrow facial structure (ratio: {face_ratio:.3f})\n"
            explanation += "   • Characteristics: Dry, rough skin with angular features"
        
        elif dominant == 'Pitta':
            explanation += f"   • Moderate skin texture variance ({texture_variance:.2f})\n"
            if 0.75 <= face_ratio <= 0.9:
                explanation += f"   • Balanced facial structure (ratio: {face_ratio:.3f})\n"
            explanation += "   • Characteristics: Moderate texture with balanced features"
        
        elif dominant == 'Kapha':
            explanation += f"   • Low skin texture variance ({texture_variance:.2f}) indicating smooth, oily skin\n"
            if face_ratio > 0.9:
                explanation += f"   • Wide facial structure (ratio: {face_ratio:.3f})\n"
            explanation += "   • Characteristics: Smooth, oily skin with round features"
        
        return explanation
    
    def analyze(self, image_path: str, show_visuals: bool = True) -> Optional[Dict]:
        """
        Complete analysis pipeline with visual feedback
        
        Args:
            image_path: Path to image file
            show_visuals: Whether to show processing steps
        
        Returns:
            Dictionary with analysis results
        """
        print("\n" + "=" * 70)
        print("🔍 STARTING VISUAL FACE ANALYSIS PIPELINE")
        print("=" * 70)
        
        # STEP 1: Load image
        print("\n[STEP 1/7] Loading image...")
        image = self.load_image(image_path)
        if image is None:
            return None
        
        if show_visuals:
            self.display_step(image, "STEP 1: Original Image", 2000)
        
        # STEP 2: Detect face
        print("\n[STEP 2/7] Detecting face...")
        face_data = self.detect_face(image)
        if face_data is None:
            cv2.destroyAllWindows()
            return None
        
        face_region = face_data['face_region']
        
        if show_visuals:
            # Draw bounding box on original image
            bbox_image = image.copy()
            x_min, y_min, x_max, y_max = face_data['bbox']
            cv2.rectangle(bbox_image, (x_min, y_min), (x_max, y_max), (0, 255, 0), 2)
            self.display_step(bbox_image, "STEP 2: Face Detection", 2000)
            
            # Show cropped face
            self.display_step(face_region, "STEP 2b: Cropped Face Region", 2000)
        
        # STEP 3: Enhance image
        print("\n[STEP 3/7] Enhancing image...")
        enhanced_images = self.enhance_image(face_region)
        
        if show_visuals:
            # Show grayscale
            gray_bgr = cv2.cvtColor(enhanced_images['grayscale'], cv2.COLOR_GRAY2BGR)
            self.display_step(gray_bgr, "STEP 3a: Grayscale Conversion", 1500)
            
            # Show equalized
            eq_bgr = cv2.cvtColor(enhanced_images['equalized'], cv2.COLOR_GRAY2BGR)
            self.display_step(eq_bgr, "STEP 3b: Histogram Equalization", 1500)
            
            # Show sharpened
            sharp_bgr = cv2.cvtColor(enhanced_images['sharpened'], cv2.COLOR_GRAY2BGR)
            self.display_step(sharp_bgr, "STEP 3c: Sharpening Filter", 1500)
            
            # Show blurred
            blur_bgr = cv2.cvtColor(enhanced_images['blurred'], cv2.COLOR_GRAY2BGR)
            self.display_step(blur_bgr, "STEP 3d: Gaussian Blur", 1500)
        
        # STEP 4: Extract texture
        print("\n[STEP 4/7] Extracting texture patterns...")
        texture_data = self.extract_texture(enhanced_images['final'])
        
        if show_visuals:
            self.display_step(texture_data['texture_map_colored'], 
                            "STEP 4: Texture Map (Laplacian)", 2000)
        
        # STEP 5: Calculate face structure
        print("\n[STEP 5/7] Calculating face structure...")
        structure_data = self.calculate_face_structure(face_data)
        
        # STEP 6: Calculate dosha scores
        print("\n[STEP 6/7] Calculating dosha scores...")
        scores = self.calculate_dosha_scores(texture_data, structure_data)
        
        # STEP 7: Generate explanation
        print("\n[STEP 7/7] Generating explanation...")
        explanation = self.generate_explanation(scores, texture_data, structure_data)
        
        # Create final result visualization
        if show_visuals:
            result_image = self.create_result_visualization(
                face_region, texture_data, scores
            )
            self.display_step(result_image, "STEP 7: Final Analysis", 3000)
        
        # Compile results
        result = {
            'success': True,
            'scores': {
                'vata': scores['vata'],
                'pitta': scores['pitta'],
                'kapha': scores['kapha']
            },
            'dominant': scores['dominant'],
            'texture': {
                'variance': texture_data['variance'],
                'mean': texture_data['mean'],
                'std': texture_data['std']
            },
            'structure': {
                'width': structure_data['width'],
                'height': structure_data['height'],
                'ratio': structure_data['ratio'],
                'shape': structure_data['shape']
            },
            'explanation': explanation
        }
        
        return result
    
    def create_result_visualization(self, face_image: np.ndarray, 
                                   texture_data: Dict, scores: Dict) -> np.ndarray:
        """Create final result visualization"""
        # Create canvas
        h, w = face_image.shape[:2]
        canvas = np.ones((h, w + 300, 3), dtype=np.uint8) * 255
        
        # Place face image
        canvas[:h, :w] = face_image
        
        # Place texture map
        texture_resized = cv2.resize(texture_data['texture_map_colored'], (w, h))
        
        # Add text overlay with scores
        y_offset = 20
        cv2.putText(canvas, "DOSHA SCORES:", (w + 10, y_offset), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 0), 2)
        
        y_offset += 40
        cv2.putText(canvas, f"Vata: {scores['vata']:.1f}%", (w + 10, y_offset), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.5, (128, 0, 128), 2)
        
        y_offset += 30
        cv2.putText(canvas, f"Pitta: {scores['pitta']:.1f}%", (w + 10, y_offset), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 87, 34), 2)
        
        y_offset += 30
        cv2.putText(canvas, f"Kapha: {scores['kapha']:.1f}%", (w + 10, y_offset), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.5, (76, 175, 80), 2)
        
        y_offset += 50
        cv2.putText(canvas, f"Dominant:", (w + 10, y_offset), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 0), 2)
        
        y_offset += 30
        cv2.putText(canvas, scores['dominant'], (w + 10, y_offset), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 0), 2)
        
        return canvas
    
    def print_results(self, result: Dict):
        """Print formatted results to console"""
        print("\n" + "=" * 70)
        print("📋 ANALYSIS RESULTS")
        print("=" * 70)
        
        print("\n🔬 TEXTURE ANALYSIS:")
        print(f"   • Texture Variance: {result['texture']['variance']:.2f}")
        print(f"   • Texture Mean: {result['texture']['mean']:.2f}")
        print(f"   • Texture Std Dev: {result['texture']['std']:.2f}")
        
        print("\n📐 FACE STRUCTURE:")
        print(f"   • Face Width: {result['structure']['width']} pixels")
        print(f"   • Face Height: {result['structure']['height']} pixels")
        print(f"   • Face Ratio: {result['structure']['ratio']:.3f}")
        print(f"   • Face Shape: {result['structure']['shape']}")
        
        print("\n⚖️ DOSHA SCORES:")
        print(f"   • Vata:  {result['scores']['vata']:.1f}%")
        print(f"   • Pitta: {result['scores']['pitta']:.1f}%")
        print(f"   • Kapha: {result['scores']['kapha']:.1f}%")
        
        print(f"\n🎯 DOMINANT DOSHA: {result['dominant']}")
        
        print("\n💡 EXPLANATION:")
        print(result['explanation'])
        
        print("\n" + "=" * 70)
        print("✅ ANALYSIS COMPLETE")
        print("=" * 70)
    
    def __del__(self):
        """Cleanup"""
        if hasattr(self, 'face_mesh'):
            self.face_mesh.close()
        cv2.destroyAllWindows()


# ============================================================================
# MAIN EXECUTION
# ============================================================================

def main():
    """Main function"""
    print("\n" + "=" * 70)
    print("🕉️ AYURVEDA FACE ANALYSIS WITH IMAGE ENHANCEMENT")
    print("=" * 70)
    print("\nVersion: 1.0 - Visual Processing Pipeline")
    print("Features: Image Enhancement + Texture Analysis + Dosha Detection")
    print("\n" + "=" * 70)
    
    # Check command line arguments
    if len(sys.argv) < 2:
        print("\n❌ Error: No image path provided")
        print("\nUsage:")
        print("   python enhanced_face_analysis.py <image_path>")
        print("\nExample:")
        print("   python enhanced_face_analysis.py face.jpg")
        print("\n" + "=" * 70)
        sys.exit(1)
    
    image_path = sys.argv[1]
    
    # Initialize analyzer
    analyzer = VisualFaceAnalyzer()
    
    # Perform analysis with visual feedback
    result = analyzer.analyze(image_path, show_visuals=True)
    
    if result is None:
        print("\n❌ Analysis failed")
        cv2.destroyAllWindows()
        sys.exit(1)
    
    # Print results
    analyzer.print_results(result)
    
    # Wait for user to close windows
    print("\n⌨️ Press any key to close all windows and exit...")
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    
    print("\n✅ Program completed successfully")


if __name__ == "__main__":
    main()
