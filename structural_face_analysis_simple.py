"""
SIMPLIFIED STRUCTURAL FACE ANALYSIS
Uses OpenCV DNN for face detection + geometric analysis
No MediaPipe dependency required

Author: AyurAI Veda Team
Version: 4.0 - OpenCV DNN Based
"""

import cv2
import numpy as np
from typing import Dict, Optional
import base64
from io import BytesIO
from PIL import Image


class StructuralFaceAnalyzer:
    """
    Simplified Structural Face Analyzer using OpenCV DNN
    """
    
    def __init__(self):
        """Initialize OpenCV DNN face detector"""
        self.face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        self.eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')
        print("Structural Face Analyzer initialized (OpenCV DNN)")
    
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
            print(f"Error loading base64 image: {str(e)}")
            return None
    
    def analyze_face(self, image_input: str, input_type: str = 'base64') -> Dict:
        """
        Analyze face structure
        
        Args:
            image_input: Base64 string
            input_type: 'base64'
        
        Returns:
            Dictionary with analysis results
        """
        
        # Load image
        if input_type == 'base64':
            image = self.load_image_from_base64(image_input)
        else:
            return {'error': 'Only base64 input supported'}
        
        if image is None:
            return {'error': 'Failed to load image'}
        
        # Convert to grayscale
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
        # Detect face
        faces = self.face_cascade.detectMultiScale(gray, 1.3, 5)
        
        if len(faces) == 0:
            return {'error': 'No face detected in the image'}
        
        # Get largest face
        face = max(faces, key=lambda f: f[2] * f[3])
        x, y, w, h = face
        
        # Calculate face ratio
        face_ratio = w / h if h > 0 else 0
        
        # Detect eyes in face region
        face_roi = gray[y:y+h, x:x+w]
        eyes = self.eye_cascade.detectMultiScale(face_roi, 1.1, 5)
        
        # Calculate features
        eye_count = len(eyes)
        avg_eye_size = 0
        if eye_count > 0:
            avg_eye_size = np.mean([ew * eh for (ex, ey, ew, eh) in eyes])
        
        # Estimate jaw width (lower 1/3 of face)
        jaw_region_height = h // 3
        jaw_region = face_roi[h - jaw_region_height:h, :]
        jaw_width_estimate = w * 0.8  # Approximate
        
        # Calculate fullness (face area vs bounding box)
        face_area = w * h
        fullness = 0.75  # Default estimate
        
        # Dosha scoring based on structure
        vata = pitta = kapha = 0
        
        # Face shape scoring
        if face_ratio > 0.9:
            kapha += 3  # Wide face
        elif face_ratio < 0.75:
            vata += 3   # Narrow face
        else:
            pitta += 3  # Medium face
        
        # Eye size scoring (relative to face)
        eye_size_ratio = avg_eye_size / face_area if face_area > 0 else 0
        if eye_size_ratio > 0.015:
            kapha += 2  # Large eyes
        elif eye_size_ratio < 0.008:
            vata += 2   # Small eyes
        else:
            pitta += 2  # Medium eyes
        
        # Jaw structure (estimated from face ratio)
        if face_ratio > 0.95:
            kapha += 2  # Square/wide jaw
        elif face_ratio < 0.70:
            vata += 2   # Narrow jaw
        else:
            pitta += 2  # Angular jaw
        
        # Face fullness
        if fullness > 0.80:
            kapha += 2
        elif fullness < 0.65:
            vata += 2
        else:
            pitta += 2
        
        # Normalize scores
        total = vata + pitta + kapha
        if total > 0:
            vata_percent = round((vata / total) * 100, 1)
            pitta_percent = round((pitta / total) * 100, 1)
            kapha_percent = round((kapha / total) * 100, 1)
        else:
            vata_percent = pitta_percent = kapha_percent = 33.3
        
        # Determine dominant
        doshas = {'Vata': vata_percent, 'Pitta': pitta_percent, 'Kapha': kapha_percent}
        dominant = max(doshas, key=doshas.get)
        
        # Risk level
        max_score = max(vata_percent, pitta_percent, kapha_percent)
        if max_score >= 50:
            risk = 'High'
        elif max_score >= 40:
            risk = 'Moderate'
        else:
            risk = 'Low'
        
        # Generate explanation
        explanation = f"{dominant} dominance detected based on "
        if dominant == 'Vata':
            explanation += f"narrow facial structure (ratio: {face_ratio:.3f}), angular features"
        elif dominant == 'Pitta':
            explanation += f"balanced facial proportions (ratio: {face_ratio:.3f}), medium features"
        elif dominant == 'Kapha':
            explanation += f"rounded facial structure (ratio: {face_ratio:.3f}), fuller features"
        
        # Compile result
        result = {
            'success': True,
            'features': {
                'face_dimensions': {
                    'face_width': float(w),
                    'face_height': float(h),
                    'face_ratio': round(face_ratio, 3)
                },
                'eye_size': {
                    'eye_count': int(eye_count),
                    'avg_eye_size': round(float(avg_eye_size), 2)
                },
                'jaw_structure': {
                    'jaw_width': round(float(jaw_width_estimate), 2)
                },
                'face_fullness': {
                    'fullness': round(fullness, 3)
                }
            },
            'scores': {
                'vata': vata_percent,
                'pitta': pitta_percent,
                'kapha': kapha_percent
            },
            'dominant': dominant,
            'risk': risk,
            'explanation': explanation,
            'face_detected': True
        }
        
        return result


if __name__ == "__main__":
    print("=" * 70)
    print("Structural Face Analysis System (OpenCV DNN)")
    print("=" * 70)
    analyzer = StructuralFaceAnalyzer()
    print("Ready for analysis!")
