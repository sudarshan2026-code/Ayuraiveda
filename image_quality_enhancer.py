"""
Image Quality Enhancement Module
Automatically preprocesses and enhances images for optimal analysis
"""

import cv2
import numpy as np
from PIL import Image, ImageEnhance, ImageFilter
import io
import base64


class ImageQualityEnhancer:
    """
    Intelligent image preprocessing system that automatically:
    - Detects image quality issues
    - Applies appropriate enhancements
    - Ensures optimal input for AI analysis
    """
    
    def __init__(self):
        self.min_resolution = (200, 200)
        self.target_resolution = (800, 800)
        self.max_resolution = (2000, 2000)
    
    def analyze_and_enhance(self, image_data, input_type='base64'):
        """
        Main method: Analyzes image quality and applies enhancements
        
        Args:
            image_data: Image data (base64 string, file path, or numpy array)
            input_type: 'base64', 'path', or 'array'
        
        Returns:
            dict: Enhanced image and quality metrics
        """
        # Load image
        image = self._load_image(image_data, input_type)
        
        if image is None:
            return {'success': False, 'error': 'Failed to load image'}
        
        # Analyze quality
        quality_metrics = self._analyze_quality(image)
        
        # Apply enhancements based on quality analysis
        enhanced_image = self._apply_enhancements(image, quality_metrics)
        
        # Final validation
        final_metrics = self._analyze_quality(enhanced_image)
        
        return {
            'success': True,
            'original_metrics': quality_metrics,
            'enhanced_metrics': final_metrics,
            'enhanced_image': enhanced_image,
            'enhancements_applied': quality_metrics['enhancements_needed']
        }
    
    def _load_image(self, image_data, input_type):
        """Load image from various input formats"""
        try:
            if input_type == 'base64':
                # Remove data URL prefix if present
                if ',' in image_data:
                    image_data = image_data.split(',')[1]
                
                # Decode base64
                image_bytes = base64.b64decode(image_data)
                pil_image = Image.open(io.BytesIO(image_bytes))
                
                # Convert to RGB if needed
                if pil_image.mode != 'RGB':
                    pil_image = pil_image.convert('RGB')
                
                # Convert to numpy array
                image = cv2.cvtColor(np.array(pil_image), cv2.COLOR_RGB2BGR)
                
            elif input_type == 'path':
                image = cv2.imread(image_data)
                
            elif input_type == 'array':
                image = image_data
            
            else:
                return None
            
            return image
            
        except Exception as e:
            print(f"Error loading image: {str(e)}")
            return None
    
    def _analyze_quality(self, image):
        """
        Comprehensive image quality analysis
        
        Checks:
        - Resolution
        - Brightness
        - Contrast
        - Sharpness
        - Noise level
        - Color balance
        """
        metrics = {}
        enhancements_needed = []
        
        # 1. Resolution check
        height, width = image.shape[:2]
        metrics['resolution'] = (width, height)
        metrics['total_pixels'] = width * height
        
        if width < self.min_resolution[0] or height < self.min_resolution[1]:
            enhancements_needed.append('upscale')
            metrics['resolution_status'] = 'too_low'
        elif width > self.max_resolution[0] or height > self.max_resolution[1]:
            enhancements_needed.append('downscale')
            metrics['resolution_status'] = 'too_high'
        else:
            metrics['resolution_status'] = 'acceptable'
        
        # 2. Brightness analysis
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        brightness = np.mean(gray)
        metrics['brightness'] = float(brightness)
        
        if brightness < 80:
            enhancements_needed.append('brighten')
            metrics['brightness_status'] = 'too_dark'
        elif brightness > 200:
            enhancements_needed.append('darken')
            metrics['brightness_status'] = 'too_bright'
        else:
            metrics['brightness_status'] = 'good'
        
        # 3. Contrast analysis
        contrast = gray.std()
        metrics['contrast'] = float(contrast)
        
        if contrast < 30:
            enhancements_needed.append('increase_contrast')
            metrics['contrast_status'] = 'low'
        elif contrast > 80:
            metrics['contrast_status'] = 'high'
        else:
            metrics['contrast_status'] = 'good'
        
        # 4. Sharpness analysis (Laplacian variance)
        laplacian = cv2.Laplacian(gray, cv2.CV_64F)
        sharpness = laplacian.var()
        metrics['sharpness'] = float(sharpness)
        
        if sharpness < 100:
            enhancements_needed.append('sharpen')
            metrics['sharpness_status'] = 'blurry'
        else:
            metrics['sharpness_status'] = 'sharp'
        
        # 5. Noise analysis
        noise_level = self._estimate_noise(gray)
        metrics['noise_level'] = float(noise_level)
        
        if noise_level > 15:
            enhancements_needed.append('denoise')
            metrics['noise_status'] = 'noisy'
        else:
            metrics['noise_status'] = 'clean'
        
        # 6. Color balance
        b, g, r = cv2.split(image)
        color_balance = {
            'red': float(np.mean(r)),
            'green': float(np.mean(g)),
            'blue': float(np.mean(b))
        }
        metrics['color_balance'] = color_balance
        
        # Check if color cast exists
        color_diff = max(color_balance.values()) - min(color_balance.values())
        if color_diff > 30:
            enhancements_needed.append('color_correction')
            metrics['color_status'] = 'color_cast'
        else:
            metrics['color_status'] = 'balanced'
        
        metrics['enhancements_needed'] = enhancements_needed
        metrics['overall_quality'] = self._calculate_overall_quality(metrics)
        
        return metrics
    
    def _estimate_noise(self, gray_image):
        """Estimate noise level using median absolute deviation"""
        h, w = gray_image.shape
        
        # Use central region for noise estimation
        center_h, center_w = h // 2, w // 2
        region = gray_image[center_h-50:center_h+50, center_w-50:center_w+50]
        
        # Calculate noise using high-pass filter
        kernel = np.array([[-1, -1, -1],
                          [-1,  8, -1],
                          [-1, -1, -1]])
        
        filtered = cv2.filter2D(region, -1, kernel)
        noise = np.median(np.abs(filtered))
        
        return noise
    
    def _calculate_overall_quality(self, metrics):
        """Calculate overall quality score (0-100)"""
        score = 100
        
        # Deduct points for issues
        if metrics['resolution_status'] != 'acceptable':
            score -= 20
        if metrics['brightness_status'] != 'good':
            score -= 15
        if metrics['contrast_status'] == 'low':
            score -= 15
        if metrics['sharpness_status'] == 'blurry':
            score -= 20
        if metrics['noise_status'] == 'noisy':
            score -= 15
        if metrics['color_status'] == 'color_cast':
            score -= 10
        
        return max(0, score)
    
    def _apply_enhancements(self, image, quality_metrics):
        """Apply necessary enhancements based on quality analysis"""
        enhanced = image.copy()
        enhancements = quality_metrics['enhancements_needed']
        
        # 1. Resolution adjustment
        if 'upscale' in enhancements:
            enhanced = self._upscale_image(enhanced)
        elif 'downscale' in enhancements:
            enhanced = self._downscale_image(enhanced)
        
        # 2. Denoising (do this early)
        if 'denoise' in enhancements:
            enhanced = self._denoise_image(enhanced)
        
        # 3. Brightness adjustment
        if 'brighten' in enhancements:
            enhanced = self._adjust_brightness(enhanced, increase=True)
        elif 'darken' in enhancements:
            enhanced = self._adjust_brightness(enhanced, increase=False)
        
        # 4. Contrast enhancement
        if 'increase_contrast' in enhancements:
            enhanced = self._enhance_contrast(enhanced)
        
        # 5. Sharpening
        if 'sharpen' in enhancements:
            enhanced = self._sharpen_image(enhanced)
        
        # 6. Color correction
        if 'color_correction' in enhancements:
            enhanced = self._correct_color_balance(enhanced)
        
        # 7. Final normalization
        enhanced = self._normalize_image(enhanced)
        
        return enhanced
    
    def _upscale_image(self, image):
        """Upscale low-resolution images using intelligent interpolation"""
        h, w = image.shape[:2]
        
        # Calculate scale factor
        scale_factor = max(
            self.target_resolution[0] / w,
            self.target_resolution[1] / h
        )
        
        new_w = int(w * scale_factor)
        new_h = int(h * scale_factor)
        
        # Use LANCZOS for high-quality upscaling
        upscaled = cv2.resize(image, (new_w, new_h), interpolation=cv2.INTER_LANCZOS4)
        
        return upscaled
    
    def _downscale_image(self, image):
        """Downscale high-resolution images"""
        h, w = image.shape[:2]
        
        # Calculate scale factor
        scale_factor = min(
            self.max_resolution[0] / w,
            self.max_resolution[1] / h
        )
        
        new_w = int(w * scale_factor)
        new_h = int(h * scale_factor)
        
        # Use AREA for high-quality downscaling
        downscaled = cv2.resize(image, (new_w, new_h), interpolation=cv2.INTER_AREA)
        
        return downscaled
    
    def _denoise_image(self, image):
        """Remove noise while preserving edges"""
        # Use Non-local Means Denoising
        denoised = cv2.fastNlMeansDenoisingColored(image, None, 10, 10, 7, 21)
        return denoised
    
    def _adjust_brightness(self, image, increase=True):
        """Adjust image brightness intelligently"""
        # Convert to HSV for better brightness control
        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        h, s, v = cv2.split(hsv)
        
        if increase:
            # Increase brightness
            v = cv2.add(v, 30)
        else:
            # Decrease brightness
            v = cv2.subtract(v, 30)
        
        # Merge and convert back
        hsv = cv2.merge([h, s, v])
        adjusted = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)
        
        return adjusted
    
    def _enhance_contrast(self, image):
        """Enhance image contrast using CLAHE"""
        # Convert to LAB color space
        lab = cv2.cvtColor(image, cv2.COLOR_BGR2LAB)
        l, a, b = cv2.split(lab)
        
        # Apply CLAHE to L channel
        clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8, 8))
        l = clahe.apply(l)
        
        # Merge and convert back
        lab = cv2.merge([l, a, b])
        enhanced = cv2.cvtColor(lab, cv2.COLOR_LAB2BGR)
        
        return enhanced
    
    def _sharpen_image(self, image):
        """Sharpen blurry images"""
        # Create sharpening kernel
        kernel = np.array([[-1, -1, -1],
                          [-1,  9, -1],
                          [-1, -1, -1]])
        
        sharpened = cv2.filter2D(image, -1, kernel)
        
        # Blend with original to avoid over-sharpening
        alpha = 0.7
        result = cv2.addWeighted(sharpened, alpha, image, 1 - alpha, 0)
        
        return result
    
    def _correct_color_balance(self, image):
        """Correct color cast using gray world assumption"""
        result = image.copy()
        
        # Calculate average color values
        avg_b = np.mean(result[:, :, 0])
        avg_g = np.mean(result[:, :, 1])
        avg_r = np.mean(result[:, :, 2])
        
        # Calculate gray value
        gray_avg = (avg_b + avg_g + avg_r) / 3
        
        # Calculate scaling factors
        scale_b = gray_avg / avg_b if avg_b > 0 else 1
        scale_g = gray_avg / avg_g if avg_g > 0 else 1
        scale_r = gray_avg / avg_r if avg_r > 0 else 1
        
        # Apply correction
        result[:, :, 0] = np.clip(result[:, :, 0] * scale_b, 0, 255)
        result[:, :, 1] = np.clip(result[:, :, 1] * scale_g, 0, 255)
        result[:, :, 2] = np.clip(result[:, :, 2] * scale_r, 0, 255)
        
        return result.astype(np.uint8)
    
    def _normalize_image(self, image):
        """Final normalization to ensure optimal range"""
        # Normalize to 0-255 range
        normalized = cv2.normalize(image, None, 0, 255, cv2.NORM_MINMAX)
        return normalized.astype(np.uint8)
    
    def get_enhanced_base64(self, enhanced_image):
        """Convert enhanced image back to base64"""
        # Convert BGR to RGB
        rgb_image = cv2.cvtColor(enhanced_image, cv2.COLOR_BGR2RGB)
        
        # Convert to PIL Image
        pil_image = Image.fromarray(rgb_image)
        
        # Save to bytes
        buffer = io.BytesIO()
        pil_image.save(buffer, format='JPEG', quality=95)
        buffer.seek(0)
        
        # Encode to base64
        base64_str = base64.b64encode(buffer.getvalue()).decode('utf-8')
        
        return f"data:image/jpeg;base64,{base64_str}"
    
    def create_quality_report(self, original_metrics, enhanced_metrics):
        """Create a detailed quality improvement report"""
        report = {
            'original_quality': original_metrics['overall_quality'],
            'enhanced_quality': enhanced_metrics['overall_quality'],
            'improvement': enhanced_metrics['overall_quality'] - original_metrics['overall_quality'],
            'enhancements_applied': original_metrics['enhancements_needed'],
            'details': {
                'resolution': {
                    'before': original_metrics['resolution'],
                    'after': enhanced_metrics['resolution']
                },
                'brightness': {
                    'before': round(original_metrics['brightness'], 2),
                    'after': round(enhanced_metrics['brightness'], 2)
                },
                'contrast': {
                    'before': round(original_metrics['contrast'], 2),
                    'after': round(enhanced_metrics['contrast'], 2)
                },
                'sharpness': {
                    'before': round(original_metrics['sharpness'], 2),
                    'after': round(enhanced_metrics['sharpness'], 2)
                }
            }
        }
        
        return report


# Convenience function for quick enhancement
def enhance_image_for_analysis(image_data, input_type='base64'):
    """
    Quick function to enhance any image for analysis
    
    Usage:
        result = enhance_image_for_analysis(base64_image)
        enhanced_image = result['enhanced_image']
    """
    enhancer = ImageQualityEnhancer()
    return enhancer.analyze_and_enhance(image_data, input_type)
