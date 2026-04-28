"""
Feature Extraction Module for Ayurvedic Dosha Analysis
Converts images into structured numerical features for ML prediction
"""

import cv2
import numpy as np
from typing import Dict, Tuple, Optional
import base64
from io import BytesIO
from PIL import Image


class ImageFeatureExtractor:
    """Extract structured features from face/body images"""
    
    def __init__(self):
        # Load Haar Cascades
        self.face_cascade = cv2.CascadeClassifier(
            cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
        )
        self.eye_cascade = cv2.CascadeClassifier(
            cv2.data.haarcascades + 'haarcascade_eye.xml'
        )
        
        # Standard image size for processing
        self.standard_size = (256, 256)
        
    def load_image(self, image_input, input_type='base64') -> Optional[np.ndarray]:
        """
        Load image from various sources
        
        Args:
            image_input: Image data (base64 string, file path, or numpy array)
            input_type: 'base64', 'path', or 'array'
            
        Returns:
            Loaded image as numpy array (BGR format)
        """
        try:
            if input_type == 'base64':
                if 'base64,' in image_input:
                    image_input = image_input.split('base64,')[1]
                image_bytes = base64.b64decode(image_input)
                image_pil = Image.open(BytesIO(image_bytes))
                image = cv2.cvtColor(np.array(image_pil), cv2.COLOR_RGB2BGR)
            elif input_type == 'path':
                image = cv2.imread(image_input)
            elif input_type == 'array':
                image = image_input
            else:
                return None
                
            return image
        except Exception as e:
            print(f"Error loading image: {e}")
            return None
    
    def validate_image(self, image: np.ndarray) -> Dict[str, any]:
        """
        Validate image quality
        
        Returns:
            Dictionary with validation results
        """
        if image is None:
            return {'valid': False, 'reason': 'Image is None'}
        
        height, width = image.shape[:2]
        
        # Check resolution
        if width < 100 or height < 100:
            return {'valid': False, 'reason': 'Resolution too low (min 100x100)'}
        
        # Check if image is too blurry
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        laplacian_var = cv2.Laplacian(gray, cv2.CV_64F).var()
        
        if laplacian_var < 50:
            return {'valid': False, 'reason': 'Image too blurry', 'blur_score': laplacian_var}
        
        # Check brightness
        brightness = np.mean(gray)
        if brightness < 30:
            return {'valid': False, 'reason': 'Image too dark'}
        if brightness > 225:
            return {'valid': False, 'reason': 'Image too bright'}
        
        return {
            'valid': True,
            'resolution': (width, height),
            'blur_score': laplacian_var,
            'brightness': brightness
        }
    
    def preprocess_image(self, image: np.ndarray) -> np.ndarray:
        """
        Preprocess image: resize, enhance, normalize
        
        Returns:
            Preprocessed image
        """
        # Resize to standard size
        resized = cv2.resize(image, self.standard_size, interpolation=cv2.INTER_AREA)
        
        # Convert to LAB for better processing
        lab = cv2.cvtColor(resized, cv2.COLOR_BGR2LAB)
        l, a, b = cv2.split(lab)
        
        # Apply CLAHE (Contrast Limited Adaptive Histogram Equalization)
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
        l = clahe.apply(l)
        
        # Merge back
        enhanced = cv2.merge([l, a, b])
        enhanced = cv2.cvtColor(enhanced, cv2.COLOR_LAB2BGR)
        
        # Denoise
        denoised = cv2.fastNlMeansDenoisingColored(enhanced, None, 10, 10, 7, 21)
        
        return denoised
    
    def detect_face_region(self, image: np.ndarray) -> Optional[Tuple[int, int, int, int]]:
        """
        Detect face region
        
        Returns:
            (x, y, w, h) or None
        """
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        faces = self.face_cascade.detectMultiScale(gray, 1.3, 5)
        
        if len(faces) == 0:
            return None
        
        # Return largest face
        return max(faces, key=lambda f: f[2] * f[3])
    
    def extract_skin_features(self, image: np.ndarray, face_region: Tuple[int, int, int, int]) -> Dict[str, float]:
        """
        Extract skin-related features
        
        Returns:
            Dictionary with normalized skin features (0-1 scale)
        """
        x, y, w, h = face_region
        
        # Extract face region with padding
        padding = 10
        x1 = max(0, x - padding)
        y1 = max(0, y - padding)
        x2 = min(image.shape[1], x + w + padding)
        y2 = min(image.shape[0], y + h + padding)
        
        face_img = image[y1:y2, x1:x2]
        
        # Convert to different color spaces
        gray_face = cv2.cvtColor(face_img, cv2.COLOR_BGR2GRAY)
        hsv_face = cv2.cvtColor(face_img, cv2.COLOR_BGR2HSV)
        lab_face = cv2.cvtColor(face_img, cv2.COLOR_BGR2LAB)
        
        # 1. TEXTURE SCORE (smooth ↔ rough)
        # Use Laplacian variance
        laplacian = cv2.Laplacian(gray_face, cv2.CV_64F)
        texture_variance = laplacian.var()
        texture_score = min(texture_variance / 200.0, 1.0)  # Normalize to 0-1
        
        # 2. OILINESS (shine detection)
        # Detect bright spots (highlights)
        _, bright_mask = cv2.threshold(gray_face, 200, 255, cv2.THRESH_BINARY)
        oiliness = np.sum(bright_mask > 0) / bright_mask.size
        
        # 3. PIGMENTATION VARIANCE
        # Standard deviation of skin tone
        l_channel = lab_face[:, :, 0]
        pigmentation = np.std(l_channel) / 50.0  # Normalize
        pigmentation = min(pigmentation, 1.0)
        
        # 4. WRINKLE DETECTION
        # Use Canny edge detection
        edges = cv2.Canny(gray_face, 50, 150)
        wrinkle_score = np.sum(edges > 0) / edges.size
        
        return {
            'skin_texture': float(texture_score),
            'oiliness': float(oiliness),
            'pigmentation': float(pigmentation),
            'wrinkles': float(wrinkle_score)
        }
    
    def extract_facial_structure(self, image: np.ndarray, face_region: Tuple[int, int, int, int]) -> Dict[str, float]:
        """
        Extract facial structure features
        
        Returns:
            Dictionary with normalized facial ratios
        """
        x, y, w, h = face_region
        
        # 1. FACE WIDTH/HEIGHT RATIO
        face_ratio = w / h if h > 0 else 0.75
        # Normalize: typical range 0.6-1.0, map to 0-1
        face_ratio_norm = (face_ratio - 0.6) / 0.4
        face_ratio_norm = max(0, min(1, face_ratio_norm))
        
        # Extract face region for detailed analysis
        face_img = image[y:y+h, x:x+w]
        gray_face = cv2.cvtColor(face_img, cv2.COLOR_BGR2GRAY)
        
        # 2. JAW WIDTH RATIO
        # Approximate jaw as lower 1/3 of face
        jaw_region = gray_face[int(h*0.66):h, :]
        jaw_width = np.sum(np.std(jaw_region, axis=0) > 10)
        jaw_ratio = jaw_width / w if w > 0 else 0.5
        
        # 3. EYE SPACING RATIO
        eyes = self.eye_cascade.detectMultiScale(gray_face, 1.1, 5)
        if len(eyes) >= 2:
            # Sort eyes by x-coordinate
            eyes_sorted = sorted(eyes, key=lambda e: e[0])
            eye1_center = eyes_sorted[0][0] + eyes_sorted[0][2] // 2
            eye2_center = eyes_sorted[1][0] + eyes_sorted[1][2] // 2
            eye_spacing = abs(eye2_center - eye1_center) / w
        else:
            eye_spacing = 0.4  # Default
        
        # 4. NOSE RATIO (approximate using center region)
        nose_region = gray_face[int(h*0.3):int(h*0.7), int(w*0.35):int(w*0.65)]
        nose_prominence = np.std(nose_region) / 50.0
        nose_ratio = min(nose_prominence, 1.0)
        
        return {
            'face_ratio': float(face_ratio_norm),
            'jaw_width': float(jaw_ratio),
            'eye_spacing': float(eye_spacing),
            'nose_ratio': float(nose_ratio)
        }
    
    def extract_color_features(self, image: np.ndarray, face_region: Tuple[int, int, int, int]) -> Dict[str, float]:
        """
        Extract color-based features
        
        Returns:
            Dictionary with normalized color features
        """
        x, y, w, h = face_region
        face_img = image[y:y+h, x:x+w]
        
        # Convert to HSV and LAB
        hsv_face = cv2.cvtColor(face_img, cv2.COLOR_BGR2HSV)
        lab_face = cv2.cvtColor(face_img, cv2.COLOR_BGR2LAB)
        
        # 1. SKIN TONE HUE
        # Extract dominant hue (skin tone)
        hue_channel = hsv_face[:, :, 0]
        skin_tone_hue = np.median(hue_channel) / 180.0  # Normalize to 0-1
        
        # 2. REDNESS INDEX
        # Use 'a' channel from LAB (green-red axis)
        a_channel = lab_face[:, :, 1]
        redness = (np.mean(a_channel) - 128) / 128.0  # Normalize around 0
        redness = (redness + 1) / 2  # Map to 0-1
        
        # 3. BRIGHTNESS
        # Use 'L' channel from LAB
        l_channel = lab_face[:, :, 0]
        brightness = np.mean(l_channel) / 255.0
        
        return {
            'skin_tone_hue': float(skin_tone_hue),
            'redness': float(redness),
            'brightness': float(brightness)
        }
    
    def extract_body_features(self, image: np.ndarray) -> Dict[str, float]:
        """
        Extract body structure features (if full body visible)
        
        Returns:
            Dictionary with body features
        """
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        height, width = gray.shape
        
        # 1. BODY FRAME CLASSIFICATION
        # Use edge detection to estimate body width
        edges = cv2.Canny(gray, 50, 150)
        
        # Analyze middle section (torso)
        torso_region = edges[int(height*0.3):int(height*0.7), :]
        body_width_pixels = np.sum(np.any(torso_region > 0, axis=0))
        body_frame = body_width_pixels / width
        
        # 2. SHOULDER WIDTH RATIO
        shoulder_region = edges[int(height*0.2):int(height*0.4), :]
        shoulder_width = np.sum(np.any(shoulder_region > 0, axis=0))
        shoulder_ratio = shoulder_width / width
        
        # 3. POSTURE ALIGNMENT
        # Check vertical symmetry
        left_half = edges[:, :width//2]
        right_half = cv2.flip(edges[:, width//2:], 1)
        
        # Resize to match if needed
        min_width = min(left_half.shape[1], right_half.shape[1])
        left_half = left_half[:, :min_width]
        right_half = right_half[:, :min_width]
        
        symmetry = 1 - (np.sum(np.abs(left_half - right_half)) / (left_half.size * 255))
        posture = max(0, min(1, symmetry))
        
        return {
            'body_frame': float(body_frame),
            'shoulder_ratio': float(shoulder_ratio),
            'posture': float(posture)
        }
    
    def extract_all_features(self, image_input, input_type='base64') -> Dict[str, any]:
        """
        Main pipeline: Extract all features from image
        
        Returns:
            Complete feature dictionary with metadata
        """
        # Load image
        image = self.load_image(image_input, input_type)
        if image is None:
            return {'success': False, 'error': 'Failed to load image'}
        
        # Validate image
        validation = self.validate_image(image)
        if not validation['valid']:
            return {'success': False, 'error': validation['reason']}
        
        # Preprocess
        processed = self.preprocess_image(image)
        
        # Detect face
        face_region = self.detect_face_region(processed)
        if face_region is None:
            return {'success': False, 'error': 'No face detected. Please ensure face is clearly visible.'}
        
        # Extract features
        skin_features = self.extract_skin_features(processed, face_region)
        facial_features = self.extract_facial_structure(processed, face_region)
        color_features = self.extract_color_features(processed, face_region)
        body_features = self.extract_body_features(processed)
        
        # Combine all features
        feature_vector = {
            **skin_features,
            **facial_features,
            **color_features,
            **body_features
        }
        
        return {
            'success': True,
            'features': feature_vector,
            'metadata': {
                'image_resolution': validation['resolution'],
                'blur_score': validation['blur_score'],
                'brightness': validation['brightness'],
                'face_detected': True,
                'face_region': face_region
            }
        }
    
    def get_feature_vector_array(self, features: Dict[str, float]) -> np.ndarray:
        """
        Convert feature dictionary to ordered numpy array for ML model
        
        Returns:
            1D numpy array of features
        """
        feature_order = [
            'skin_texture', 'oiliness', 'pigmentation', 'wrinkles',
            'face_ratio', 'jaw_width', 'eye_spacing', 'nose_ratio',
            'skin_tone_hue', 'redness', 'brightness',
            'body_frame', 'shoulder_ratio', 'posture'
        ]
        
        return np.array([features.get(key, 0.0) for key in feature_order])


def test_feature_extraction():
    """Test the feature extractor"""
    extractor = ImageFeatureExtractor()
    
    # Test with sample image
    test_image_path = "test_image.jpg"
    
    result = extractor.extract_all_features(test_image_path, input_type='path')
    
    if result['success']:
        print("✓ Feature extraction successful!")
        print("\nExtracted Features:")
        for key, value in result['features'].items():
            print(f"  {key}: {value:.4f}")
        
        print("\nMetadata:")
        for key, value in result['metadata'].items():
            print(f"  {key}: {value}")
    else:
        print(f"✗ Feature extraction failed: {result['error']}")


if __name__ == "__main__":
    test_feature_extraction()
