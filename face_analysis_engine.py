"""
Face Analysis Engine for Ayurvedic Dosha Detection
Advanced Multi-Feature Weighted Analysis System
Rule-based Dosha prediction (NO ML training required)
"""

import cv2
import numpy as np
from typing import Dict, Tuple, Optional, List
import base64
from io import BytesIO
from PIL import Image

class FaceAnalysisEngine:
    """
    Ayurvedic Face Analysis Engine
    Detects face features and predicts Vata, Pitta, Kapha dominance
    """
    
    def __init__(self):
        """Initialize OpenCV Face Detector with weighted feature analysis"""
        # Load Haar Cascade for face detection
        self.face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        self.eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')
        
        # Weighted feature importance (ADVANCED SCORING)
        self.weights = {
            'skin_analysis': 0.40,      # 40% - Brightness + Shine
            'facial_geometry': 0.30,    # 30% - Face ratio + Structure
            'color_analysis': 0.20,     # 20% - Redness + HSV tone
            'texture_analysis': 0.10    # 10% - Laplacian variance
        }
    
    def load_image_from_path(self, image_path: str) -> Optional[np.ndarray]:
        """Load image from file path"""
        try:
            image = cv2.imread(image_path)
            if image is None:
                print(f"Error: Could not load image from {image_path}")
                return None
            return image
        except Exception as e:
            print(f"Error loading image: {str(e)}")
            return None
    
    def load_image_from_base64(self, base64_string: str) -> Optional[np.ndarray]:
        """Load image from base64 string"""
        try:
            # Remove data URL prefix if present
            if ',' in base64_string:
                base64_string = base64_string.split(',')[1]
            
            # Decode base64 to bytes
            image_bytes = base64.b64decode(base64_string)
            
            # Convert to PIL Image
            pil_image = Image.open(BytesIO(image_bytes))
            
            # Convert to OpenCV format (BGR)
            image = cv2.cvtColor(np.array(pil_image), cv2.COLOR_RGB2BGR)
            
            return image
        except Exception as e:
            print(f"Error loading image from base64: {str(e)}")
            return None
    
    def detect_face(self, image: np.ndarray) -> Optional[Dict]:
        """
        Detect face using OpenCV Haar Cascade
        Returns face landmarks and bounding box
        """
        try:
            # Convert to grayscale for detection
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            
            # Detect faces
            faces = self.face_cascade.detectMultiScale(
                gray, 
                scaleFactor=1.1, 
                minNeighbors=5, 
                minSize=(30, 30)
            )
            
            if len(faces) == 0:
                return None
            
            # Get the largest face
            face = max(faces, key=lambda f: f[2] * f[3])
            x, y, w, h = face
            
            # Get image dimensions
            img_h, img_w, _ = image.shape
            
            # Ensure coordinates are within image bounds
            x_min = max(0, x)
            y_min = max(0, y)
            x_max = min(img_w, x + w)
            y_max = min(img_h, y + h)
            
            bbox = {
                'x_min': x_min,
                'y_min': y_min,
                'x_max': x_max,
                'y_max': y_max,
                'width': x_max - x_min,
                'height': y_max - y_min
            }
            
            # Extract face region
            face_region = image[y_min:y_max, x_min:x_max]
            
            # Detect eyes for additional landmarks
            face_gray = gray[y_min:y_max, x_min:x_max]
            eyes = self.eye_cascade.detectMultiScale(face_gray, scaleFactor=1.1, minNeighbors=5)
            
            landmarks = []
            # Add face corners as landmarks
            landmarks.append((x_min, y_min))  # Top-left
            landmarks.append((x_max, y_min))  # Top-right
            landmarks.append((x_min, y_max))  # Bottom-left
            landmarks.append((x_max, y_max))  # Bottom-right
            
            # Add eye positions if detected
            for (ex, ey, ew, eh) in eyes:
                landmarks.append((x_min + ex + ew//2, y_min + ey + eh//2))
            
            return {
                'landmarks': landmarks,
                'bbox': bbox,
                'face_region': face_region
            }
            
        except Exception as e:
            print(f"Error detecting face: {str(e)}")
            return None
    
    def extract_skin_brightness(self, face_region: np.ndarray) -> float:
        """
        Extract skin brightness from face region
        Returns mean brightness value (0-255)
        Part of SKIN ANALYSIS (40% weight)
        """
        try:
            # Convert to grayscale
            gray = cv2.cvtColor(face_region, cv2.COLOR_BGR2GRAY)
            
            # Calculate mean brightness
            brightness = np.mean(gray)
            
            return round(float(brightness), 2)
        except Exception as e:
            print(f"Error extracting brightness: {str(e)}")
            return 0.0
    
    def extract_skin_shine(self, face_region: np.ndarray) -> float:
        """
        Extract skin shine using variance/highlights
        Higher variance = more shine (Kapha characteristic)
        Part of SKIN ANALYSIS (40% weight)
        """
        try:
            gray = cv2.cvtColor(face_region, cv2.COLOR_BGR2GRAY)
            
            # Calculate variance (measure of shine/highlights)
            variance = float(np.var(gray))
            
            # Normalize to 0-100 scale
            shine_score = min(100, variance / 10)
            
            return round(shine_score, 2)
        except Exception as e:
            print(f"Error extracting shine: {str(e)}")
            return 0.0
    
    def extract_redness(self, face_region: np.ndarray) -> float:
        """
        Extract redness ratio from face region
        Returns redness ratio: r / (g + b + 1)
        Part of COLOR ANALYSIS (20% weight)
        """
        try:
            # Extract BGR channels
            b, g, r = cv2.split(face_region)
            
            # Calculate mean values for each channel
            b_mean = float(np.mean(b))
            g_mean = float(np.mean(g))
            r_mean = float(np.mean(r))
            
            # Compute redness ratio: r / (g + b + 1)
            # Adding 1 to denominator to avoid division by zero
            redness_ratio = r_mean / (g_mean + b_mean + 1)
            
            return round(redness_ratio, 3)
        except Exception as e:
            print(f"Error extracting redness: {str(e)}")
            return 0.0
    
    def extract_hsv_tone(self, face_region: np.ndarray) -> Dict:
        """
        Extract HSV color tone for advanced color analysis
        Part of COLOR ANALYSIS (20% weight)
        """
        try:
            # Convert to HSV
            hsv = cv2.cvtColor(face_region, cv2.COLOR_BGR2HSV)
            
            # Extract channels
            h, s, v = cv2.split(hsv)
            
            hue_mean = float(np.mean(h))
            saturation_mean = float(np.mean(s))
            value_mean = float(np.mean(v))
            
            return {
                'hue': round(hue_mean, 2),
                'saturation': round(saturation_mean, 2),
                'value': round(value_mean, 2)
            }
        except Exception as e:
            print(f"Error extracting HSV: {str(e)}")
            return {'hue': 0, 'saturation': 0, 'value': 0}
    
    def calculate_face_ratio(self, bbox: Dict) -> float:
        """
        Calculate face width/height ratio
        Returns ratio value
        """
        try:
            width = bbox['width']
            height = bbox['height']
            
            if height == 0:
                return 0.0
            
            ratio = width / height
            return round(ratio, 3)
        except Exception as e:
            print(f"Error calculating face ratio: {str(e)}")
            return 0.0
    
    def extract_skin_texture(self, face_region: np.ndarray) -> float:
        """
        Extract skin texture using Laplacian variance
        Higher value = rougher texture (Vata)
        Lower value = smoother texture (Kapha)
        Part of TEXTURE ANALYSIS (10% weight)
        """
        try:
            gray = cv2.cvtColor(face_region, cv2.COLOR_BGR2GRAY)
            laplacian = cv2.Laplacian(gray, cv2.CV_64F)
            texture_score = laplacian.var()
            return round(float(texture_score), 2)
        except Exception as e:
            print(f"Error extracting texture: {str(e)}")
            return 0.0
    
    def calculate_dosha_scores(self, features: Dict) -> Dict:
        """
        RELATIVE DOSHA SCORING SYSTEM
        Fair competition between Vata, Pitta, and Kapha
        Removes Kapha bias through normalized relative scoring
        """
        # Extract features
        brightness = features['brightness']
        shine = features.get('shine', 0)
        redness = features['redness']  # Already a ratio
        face_ratio = features['face_ratio']
        texture = features.get('texture', 0)
        hsv = features.get('hsv', {'saturation': 0})
        saturation = hsv.get('saturation', 0)
        
        # ===== STEP 1: NORMALIZE ALL FEATURES =====
        brightness_norm = brightness / 255.0
        texture_norm = min(texture / 200.0, 1.0)  # Cap at 1.0
        shine_norm = shine / 100.0  # Already 0-100 scale
        saturation_norm = saturation / 255.0
        
        # ===== STEP 2: RELATIVE SCORING (COMPETITIVE) =====
        vata_score = 0
        pitta_score = 0
        kapha_score = 0
        
        # BRIGHTNESS SCORING (normalized)
        if brightness_norm < 0.4:
            vata_score += 1  # Low brightness → Vata
        elif brightness_norm > 0.65:
            kapha_score += 1  # High brightness → Kapha
        else:
            pitta_score += 1  # Medium brightness → Pitta
        
        # SHINE SCORING
        if shine_norm < 0.3:
            vata_score += 1  # Low shine → Vata (dry)
        elif shine_norm > 0.6:
            kapha_score += 1  # High shine → Kapha (oily)
        else:
            pitta_score += 1  # Medium shine → Pitta
        
        # REDNESS SCORING (ratio-based, weighted)
        if redness > 0.6:
            pitta_score += 2  # High redness → Pitta (warm)
        elif redness < 0.4:
            vata_score += 1  # Low redness → Vata (pale)
        else:
            kapha_score += 1  # Medium redness → Kapha (balanced)
        
        # TEXTURE SCORING (normalized, weighted)
        if texture_norm > 0.5:
            vata_score += 2  # High roughness → Vata
        elif texture_norm < 0.25:
            kapha_score += 2  # Smooth → Kapha
        else:
            pitta_score += 1  # Medium → Pitta
        
        # FACE RATIO SCORING (weighted)
        if face_ratio < 0.75:
            vata_score += 2  # Narrow → Vata
        elif face_ratio > 0.9:
            kapha_score += 2  # Wide → Kapha
        else:
            pitta_score += 2  # Medium → Pitta
        
        # SATURATION SCORING
        if saturation_norm < 0.2:
            vata_score += 1  # Dull → Vata
        elif saturation_norm > 0.4:
            pitta_score += 1  # Vibrant → Pitta
        else:
            kapha_score += 1  # Even → Kapha
        
        # ===== STEP 3: COMPETITIVE NORMALIZATION =====
        total = vata_score + pitta_score + kapha_score
        
        if total > 0:
            vata_percent = (vata_score / total) * 100
            pitta_percent = (pitta_score / total) * 100
            kapha_percent = (kapha_score / total) * 100
        else:
            # Fallback if no scores (shouldn't happen)
            vata_percent = pitta_percent = kapha_percent = 33.33
        
        # ===== STEP 5: ANTI-BIAS SAFETY =====
        # Reduce Kapha bias in medium brightness range
        if kapha_percent > 60 and 0.5 <= brightness_norm <= 0.7:
            # Reduce Kapha by 10%
            reduction = kapha_percent * 0.10
            kapha_percent -= reduction
            # Distribute to Pitta (most likely in this range)
            pitta_percent += reduction
            
            # Re-normalize to ensure 100%
            total_adjusted = vata_percent + pitta_percent + kapha_percent
            vata_percent = (vata_percent / total_adjusted) * 100
            pitta_percent = (pitta_percent / total_adjusted) * 100
            kapha_percent = (kapha_percent / total_adjusted) * 100
        
        # ===== FINAL OUTPUT =====
        return {
            'vata': round(float(vata_percent), 1),
            'pitta': round(float(pitta_percent), 1),
            'kapha': round(float(kapha_percent), 1),
            'raw_scores': {
                'vata': vata_score,
                'pitta': pitta_score,
                'kapha': kapha_score
            },
            'normalized_features': {
                'brightness_norm': round(brightness_norm, 3),
                'redness': round(redness, 3),
                'texture_norm': round(texture_norm, 3),
                'face_ratio': round(face_ratio, 3),
                'shine_norm': round(shine_norm, 3),
                'saturation_norm': round(saturation_norm, 3)
            },
            'component_scores': {
                'brightness': {'vata': 1 if brightness_norm < 0.4 else 0, 
                              'pitta': 1 if 0.4 <= brightness_norm <= 0.65 else 0,
                              'kapha': 1 if brightness_norm > 0.65 else 0},
                'redness': {'vata': 1 if redness < 0.4 else 0,
                           'pitta': 2 if redness > 0.6 else 0,
                           'kapha': 1 if 0.4 <= redness <= 0.6 else 0},
                'texture': {'vata': 2 if texture_norm > 0.5 else 0,
                           'pitta': 1 if 0.25 <= texture_norm <= 0.5 else 0,
                           'kapha': 2 if texture_norm < 0.25 else 0},
                'face_ratio': {'vata': 2 if face_ratio < 0.75 else 0,
                              'pitta': 2 if 0.75 <= face_ratio <= 0.9 else 0,
                              'kapha': 2 if face_ratio > 0.9 else 0}
            }
        }
    
    def get_dominant_dosha(self, scores: Dict) -> str:
        """Determine dominant dosha or detect tridoshic balance"""
        vata = scores['vata']
        pitta = scores['pitta']
        kapha = scores['kapha']
        
        # Create list of scores
        score_list = [vata, pitta, kapha]
        
        # Check if all doshas are similar (tridoshic balance)
        if max(score_list) - min(score_list) < 10:
            return "Tridoshic (Balanced)"
        
        # Otherwise return dominant dosha
        doshas = {
            'Vata': vata,
            'Pitta': pitta,
            'Kapha': kapha
        }
        return max(doshas, key=doshas.get)
    
    def generate_explanation(self, features: Dict, scores: Dict, dominant: str) -> str:
        """Generate explanation for dosha prediction"""
        brightness = features['brightness']
        brightness_norm = brightness / 255.0  # Normalize brightness
        redness = features['redness']  # Now a ratio value
        face_ratio = features['face_ratio']
        
        explanations = []
        
        # Check if tridoshic (balanced)
        if dominant == "Tridoshic (Balanced)":
            explanations.append("Tridoshic constitution detected")
            explanations.append("with balanced Vata, Pitta, and Kapha doshas")
            explanations.append("indicating a harmonious and stable constitution")
            return " ".join(explanations) + "."
        
        if dominant == 'Vata':
            explanations.append(f"{dominant} dominance detected")
            if brightness_norm < 0.4:
                explanations.append("due to lower skin brightness (dry, thin skin characteristic)")
            if face_ratio < 0.75:
                explanations.append("and angular facial proportions (thin face structure)")
            if features.get('texture', 0) > 100:
                explanations.append("with rough skin texture")
        
        elif dominant == 'Pitta':
            explanations.append(f"{dominant} dominance detected")
            if redness > 0.6:
                explanations.append("due to higher redness ratio (warm, sensitive skin)")
            if 0.75 <= face_ratio <= 0.9:
                explanations.append("and medium facial proportions (balanced structure)")
        
        elif dominant == 'Kapha':
            explanations.append(f"{dominant} dominance detected")
            if brightness_norm > 0.65:
                explanations.append("due to higher skin brightness (oily, smooth skin)")
            if face_ratio > 0.9:
                explanations.append("and wider facial proportions (round face structure)")
            if features.get('texture', 0) < 50:
                explanations.append("with smooth skin texture")
        
        return " ".join(explanations) + "."
    
    def analyze_face(self, image_input: str, input_type: str = 'path') -> Dict:
        """
        Complete face analysis pipeline
        
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
        
        # Detect face
        face_data = self.detect_face(image)
        
        if face_data is None:
            return {'error': 'No face detected in the image'}
        
        # Extract features
        face_region = face_data['face_region']
        bbox = face_data['bbox']
        
        brightness = self.extract_skin_brightness(face_region)
        shine = self.extract_skin_shine(face_region)
        redness = self.extract_redness(face_region)
        hsv = self.extract_hsv_tone(face_region)
        face_ratio = self.calculate_face_ratio(bbox)
        texture = self.extract_skin_texture(face_region)
        
        features = {
            'brightness': brightness,
            'shine': shine,
            'redness': redness,
            'hsv': hsv,
            'face_ratio': face_ratio,
            'texture': texture
        }
        
        # Calculate dosha scores
        scores = self.calculate_dosha_scores(features)
        
        # Get dominant dosha
        dominant = self.get_dominant_dosha(scores)
        
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
            'face_detected': True,
            'bbox': bbox
        }
        
        return result
    
    def __del__(self):
        """Cleanup"""
        pass


# Example usage
if __name__ == "__main__":
    print("=" * 60)
    print("🌿 AyurAI Veda - Face Analysis Engine")
    print("=" * 60)
    print()
    
    # Initialize engine
    engine = FaceAnalysisEngine()
    
    # Example with image path
    image_path = "test_face.jpg"  # Replace with actual image path
    
    print(f"Analyzing face from: {image_path}")
    print()
    
    # Perform analysis
    result = engine.analyze_face(image_path, input_type='path')
    
    if 'error' in result:
        print(f"❌ Error: {result['error']}")
    else:
        print("✅ Face Analysis Complete!")
        print()
        print("📊 Extracted Features:")
        print(f"  • Skin Brightness: {result['features']['brightness']}")
        print(f"  • Redness Level: {result['features']['redness']}")
        print(f"  • Face Ratio (W/H): {result['features']['face_ratio']}")
        print(f"  • Skin Texture: {result['features']['texture']}")
        print()
        print("⚖️ Dosha Scores:")
        print(f"  • Vata: {result['scores']['vata']}%")
        print(f"  • Pitta: {result['scores']['pitta']}%")
        print(f"  • Kapha: {result['scores']['kapha']}%")
        print()
        print(f"🎯 Dominant Dosha: {result['dominant']}")
        print(f"⚠️ Risk Level: {result['risk']}")
        print()
        print(f"💡 Explanation: {result['explanation']}")
    
    print()
    print("=" * 60)
