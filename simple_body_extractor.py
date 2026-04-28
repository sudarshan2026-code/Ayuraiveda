"""
Simple Body Feature Extractor
Extracts body shape patterns without face detection
"""

import cv2
import numpy as np
import base64
from io import BytesIO
from PIL import Image


class SimpleBodyExtractor:
    """Extract body features from full image without face detection"""
    
    def __init__(self):
        self.feature_names = [
            'skin_texture', 'oiliness', 'pigmentation', 'redness', 'brightness',
            'body_frame', 'body_width', 'body_height', 'body_ratio',
            'shoulder_width', 'hip_width', 'torso_length', 'limb_thickness', 'posture'
        ]
    
    def extract_features(self, image_input, input_type='base64'):
        """
        Extract body features from image
        
        Args:
            image_input: Image data (base64, path, or array)
            input_type: 'base64', 'path', or 'array'
            
        Returns:
            Dictionary of normalized features (0-1)
        """
        try:
            # Load image
            image = self._load_image(image_input, input_type)
            if image is None:
                return {'success': False, 'error': 'Failed to load image'}
            
            # Extract features
            features = {}
            
            # Skin features
            skin_features = self._extract_skin_features(image)
            features.update(skin_features)
            
            # Body structure features
            body_features = self._extract_body_structure(image)
            features.update(body_features)
            
            # Ensure all features are present
            for feature_name in self.feature_names:
                if feature_name not in features:
                    features[feature_name] = 0.5  # Default neutral value
            
            return {
                'success': True,
                'features': features,
                'image_shape': image.shape
            }
            
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def _load_image(self, image_input, input_type):
        """Load image from various input types"""
        try:
            if input_type == 'base64':
                # Remove data URL prefix if present
                if isinstance(image_input, str) and 'base64,' in image_input:
                    image_input = image_input.split('base64,')[1]
                
                # Decode base64
                image_data = base64.b64decode(image_input)
                image = Image.open(BytesIO(image_data))
                image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
                
            elif input_type == 'path':
                image = cv2.imread(image_input)
                
            elif input_type == 'array':
                image = image_input
                
            else:
                return None
            
            return image
            
        except Exception as e:
            print(f"Error loading image: {str(e)}")
            return None
    
    def _extract_skin_features(self, image):
        """Extract skin-related features"""
        # Convert to different color spaces
        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        lab = cv2.cvtColor(image, cv2.COLOR_BGR2LAB)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
        # Get center region (likely to contain body)
        h, w = image.shape[:2]
        center_y1, center_y2 = int(h * 0.3), int(h * 0.7)
        center_x1, center_x2 = int(w * 0.3), int(w * 0.7)
        center_region = image[center_y1:center_y2, center_x1:center_x2]
        center_gray = gray[center_y1:center_y2, center_x1:center_x2]
        center_hsv = hsv[center_y1:center_y2, center_x1:center_x2]
        
        # Skin texture (using Laplacian variance)
        laplacian = cv2.Laplacian(center_gray, cv2.CV_64F)
        texture_variance = laplacian.var()
        skin_texture = min(texture_variance / 500.0, 1.0)  # Normalize
        
        # Oiliness (using saturation and brightness)
        saturation = center_hsv[:, :, 1].mean()
        value = center_hsv[:, :, 2].mean()
        oiliness = (saturation / 255.0) * 0.6 + (value / 255.0) * 0.4
        
        # Pigmentation (using L channel from LAB)
        center_lab = lab[center_y1:center_y2, center_x1:center_x2]
        l_channel = center_lab[:, :, 0].mean()
        pigmentation = 1.0 - (l_channel / 255.0)  # Darker = more pigmentation
        
        # Redness (using red channel and hue)
        red_channel = center_region[:, :, 2].mean()
        hue = center_hsv[:, :, 0].mean()
        # Red hue is around 0-10 or 170-180
        red_hue_score = 1.0 if (hue < 10 or hue > 170) else 0.5
        redness = (red_channel / 255.0) * 0.7 + red_hue_score * 0.3
        
        # Brightness (using V channel)
        brightness = value / 255.0
        
        return {
            'skin_texture': float(skin_texture),
            'oiliness': float(oiliness),
            'pigmentation': float(pigmentation),
            'redness': float(redness),
            'brightness': float(brightness)
        }
    
    def _extract_body_structure(self, image):
        """Extract body structure features"""
        h, w = image.shape[:2]
        
        # Convert to grayscale
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
        # Apply edge detection
        edges = cv2.Canny(gray, 50, 150)
        
        # Find contours
        contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        if len(contours) == 0:
            # No contours found, use image dimensions
            return self._estimate_from_dimensions(image)
        
        # Get largest contour (likely the body)
        largest_contour = max(contours, key=cv2.contourArea)
        
        # Get bounding rectangle
        x, y, bw, bh = cv2.boundingRect(largest_contour)
        
        # Body frame (width relative to image)
        body_frame = min(bw / w, 1.0)
        
        # Body width (normalized)
        body_width = min(bw / w, 1.0)
        
        # Body height (normalized)
        body_height = min(bh / h, 1.0)
        
        # Body ratio (width/height)
        body_ratio = (bw / bh) if bh > 0 else 0.5
        body_ratio = min(body_ratio, 1.0)
        
        # Shoulder width (top 1/3 of body)
        shoulder_region = largest_contour[largest_contour[:, 0, 1] < (y + bh // 3)]
        if len(shoulder_region) > 0:
            shoulder_width = (shoulder_region[:, 0, 0].max() - shoulder_region[:, 0, 0].min()) / w
        else:
            shoulder_width = body_width * 0.8
        
        # Hip width (bottom 1/3 of body)
        hip_region = largest_contour[largest_contour[:, 0, 1] > (y + 2 * bh // 3)]
        if len(hip_region) > 0:
            hip_width = (hip_region[:, 0, 0].max() - hip_region[:, 0, 0].min()) / w
        else:
            hip_width = body_width * 0.7
        
        # Torso length (middle section)
        torso_length = min(bh / h, 1.0)
        
        # Limb thickness (estimated from contour area vs bounding box)
        contour_area = cv2.contourArea(largest_contour)
        bbox_area = bw * bh
        limb_thickness = (contour_area / bbox_area) if bbox_area > 0 else 0.5
        
        # Posture (vertical alignment - how centered the body is)
        center_x = x + bw // 2
        image_center_x = w // 2
        posture = 1.0 - min(abs(center_x - image_center_x) / (w // 2), 1.0)
        
        return {
            'body_frame': float(body_frame),
            'body_width': float(body_width),
            'body_height': float(body_height),
            'body_ratio': float(body_ratio),
            'shoulder_width': float(shoulder_width),
            'hip_width': float(hip_width),
            'torso_length': float(torso_length),
            'limb_thickness': float(limb_thickness),
            'posture': float(posture)
        }
    
    def _estimate_from_dimensions(self, image):
        """Estimate body features from image dimensions when no contours found"""
        h, w = image.shape[:2]
        
        # Use image aspect ratio as proxy
        aspect_ratio = w / h if h > 0 else 1.0
        
        # Estimate features based on aspect ratio
        # Wider images suggest heavier build
        body_frame = min(aspect_ratio * 0.6, 1.0)
        
        return {
            'body_frame': float(body_frame),
            'body_width': float(body_frame),
            'body_height': 0.7,
            'body_ratio': float(min(aspect_ratio, 1.0)),
            'shoulder_width': float(body_frame * 0.8),
            'hip_width': float(body_frame * 0.7),
            'torso_length': 0.6,
            'limb_thickness': float(body_frame * 0.7),
            'posture': 0.6
        }


def test_extractor():
    """Test the body feature extractor"""
    extractor = SimpleBodyExtractor()
    
    # Test with sample image
    test_images = [
        'test_image.jpg',
        'test_result.jpg',
        'WhatsApp Image 2026-04-27 at 13.15.57.jpeg'
    ]
    
    test_image = None
    for img in test_images:
        import os
        if os.path.exists(img):
            test_image = img
            break
    
    if not test_image:
        print("⚠️  No test image found")
        return
    
    print(f"Testing with: {test_image}")
    result = extractor.extract_features(test_image, input_type='path')
    
    if result['success']:
        print("\n✅ Feature extraction successful!")
        print(f"\nImage shape: {result['image_shape']}")
        print("\nExtracted features:")
        for feature, value in result['features'].items():
            print(f"  {feature}: {value:.4f}")
    else:
        print(f"\n❌ Extraction failed: {result['error']}")


if __name__ == "__main__":
    test_extractor()
