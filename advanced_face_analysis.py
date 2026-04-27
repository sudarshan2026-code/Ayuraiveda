"""
ADVANCED AYURVEDIC FACE ANALYSIS SYSTEM
Multi-Image Aggregation with Weighted Feature Analysis

Requirements:
pip install opencv-python numpy pillow

Author: AyurAI Veda Team
Version: 2.0 - Production Ready
"""

import cv2
import numpy as np
from typing import List, Dict, Optional, Tuple
import base64
from io import BytesIO
from PIL import Image
import os

# ============================================================================
# PART 1: CORE FACE DETECTION AND FEATURE EXTRACTION
# ============================================================================

class AdvancedFaceAnalyzer:
    """
    High-Accuracy Ayurvedic Face Analysis Engine
    Supports multi-image aggregation with weighted scoring
    """
    
    def __init__(self):
        """Initialize face detection cascades"""
        self.face_cascade = cv2.CascadeClassifier(
            cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
        )
        self.eye_cascade = cv2.CascadeClassifier(
            cv2.data.haarcascades + 'haarcascade_eye.xml'
        )
        
        # Weighted feature importance
        self.weights = {
            'skin_analysis': 0.40,      # 40%
            'facial_geometry': 0.30,    # 30%
            'color_analysis': 0.20,     # 20%
            'texture_analysis': 0.10    # 10%
        }
        
        # Confidence threshold
        self.confidence_threshold = 0.5
        
        print("✅ Advanced Face Analyzer initialized")
        print(f"📊 Feature Weights: Skin={self.weights['skin_analysis']*100}%, "
              f"Geometry={self.weights['facial_geometry']*100}%, "
              f"Color={self.weights['color_analysis']*100}%, "
              f"Texture={self.weights['texture_analysis']*100}%")
    
    # ------------------------------------------------------------------------
    # IMAGE LOADING FUNCTIONS
    # ------------------------------------------------------------------------
    
    def load_image_from_path(self, image_path: str) -> Optional[np.ndarray]:
        """Load image from file path"""
        try:
            if not os.path.exists(image_path):
                print(f"❌ File not found: {image_path}")
                return None
            
            image = cv2.imread(image_path)
            if image is None:
                print(f"❌ Could not read image: {image_path}")
                return None
            
            return image
        except Exception as e:
            print(f"❌ Error loading {image_path}: {str(e)}")
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
            print(f"❌ Error loading base64 image: {str(e)}")
            return None
    
    # ------------------------------------------------------------------------
    # FACE DETECTION
    # ------------------------------------------------------------------------
    
    def detect_face(self, image: np.ndarray) -> Optional[Dict]:
        """
        Detect face using OpenCV Haar Cascade
        Returns face region and bounding box
        """
        try:
            # Convert to grayscale
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            
            # Detect faces
            faces = self.face_cascade.detectMultiScale(
                gray,
                scaleFactor=1.1,
                minNeighbors=5,
                minSize=(50, 50)
            )
            
            if len(faces) == 0:
                return None
            
            # Get largest face
            face = max(faces, key=lambda f: f[2] * f[3])
            x, y, w, h = face
            
            # Get image dimensions
            img_h, img_w = image.shape[:2]
            
            # Ensure coordinates are within bounds
            x_min = max(0, x)
            y_min = max(0, y)
            x_max = min(img_w, x + w)
            y_max = min(img_h, y + h)
            
            # Extract face region
            face_region = image[y_min:y_max, x_min:x_max]
            
            # Detect eyes for additional landmarks
            face_gray = gray[y_min:y_max, x_min:x_max]
            eyes = self.eye_cascade.detectMultiScale(
                face_gray,
                scaleFactor=1.1,
                minNeighbors=5
            )
            
            bbox = {
                'x': x_min,
                'y': y_min,
                'width': x_max - x_min,
                'height': y_max - y_min
            }
            
            return {
                'face_region': face_region,
                'bbox': bbox,
                'eyes_detected': len(eyes),
                'gray_face': face_gray
            }
            
        except Exception as e:
            print(f"❌ Face detection error: {str(e)}")
            return None
    
    # ------------------------------------------------------------------------
    # FEATURE EXTRACTION - SKIN ANALYSIS (40%)
    # ------------------------------------------------------------------------
    
    def extract_skin_brightness(self, face_region: np.ndarray) -> float:
        """
        Extract skin brightness (grayscale mean)
        Range: 0-255
        """
        try:
            gray = cv2.cvtColor(face_region, cv2.COLOR_BGR2GRAY)
            brightness = float(np.mean(gray))
            return round(brightness, 2)
        except Exception as e:
            print(f"❌ Brightness extraction error: {str(e)}")
            return 0.0
    
    def extract_skin_shine(self, face_region: np.ndarray) -> float:
        """
        Extract skin shine using variance/highlights
        Higher variance = more shine (Kapha)
        """
        try:
            gray = cv2.cvtColor(face_region, cv2.COLOR_BGR2GRAY)
            
            # Calculate variance (measure of shine/highlights)
            variance = float(np.var(gray))
            
            # Normalize to 0-100 scale
            shine_score = min(100, variance / 10)
            
            return round(shine_score, 2)
        except Exception as e:
            print(f"❌ Shine extraction error: {str(e)}")
            return 0.0
    
    def analyze_skin(self, face_region: np.ndarray) -> Dict:
        """
        Complete skin analysis
        Returns brightness, shine, and dosha scores
        """
        brightness = self.extract_skin_brightness(face_region)
        shine = self.extract_skin_shine(face_region)
        
        # Scoring logic
        vata_skin = 0
        pitta_skin = 0
        kapha_skin = 0
        
        # Brightness rules
        if brightness < 100:
            vata_skin += 40  # Low brightness → Vata
        elif brightness > 160:
            kapha_skin += 40  # High brightness → Kapha
        else:
            pitta_skin += 20  # Medium brightness → Pitta
        
        # Shine rules
        if shine < 30:
            vata_skin += 30  # Low shine → Vata (dry)
        elif shine > 60:
            kapha_skin += 30  # High shine → Kapha (oily)
        else:
            pitta_skin += 15  # Medium shine → Pitta
        
        return {
            'brightness': brightness,
            'shine': shine,
            'vata_score': vata_skin,
            'pitta_score': pitta_skin,
            'kapha_score': kapha_skin
        }
    
    # ------------------------------------------------------------------------
    # FEATURE EXTRACTION - FACIAL GEOMETRY (30%)
    # ------------------------------------------------------------------------
    
    def extract_face_ratio(self, bbox: Dict) -> float:
        """
        Calculate face width/height ratio
        """
        try:
            width = bbox['width']
            height = bbox['height']
            
            if height == 0:
                return 0.0
            
            ratio = width / height
            return round(ratio, 3)
        except Exception as e:
            print(f"❌ Ratio calculation error: {str(e)}")
            return 0.0
    
    def analyze_facial_geometry(self, bbox: Dict, eyes_detected: int) -> Dict:
        """
        Analyze facial proportions and geometry
        """
        ratio = self.extract_face_ratio(bbox)
        
        # Scoring logic
        vata_geo = 0
        pitta_geo = 0
        kapha_geo = 0
        
        # Face ratio rules
        if ratio < 0.75:
            vata_geo += 40  # Narrow, elongated → Vata
        elif 0.75 <= ratio <= 0.90:
            pitta_geo += 40  # Medium, angular → Pitta
        else:
            kapha_geo += 40  # Wide, round → Kapha
        
        # Eye detection bonus (structural indicator)
        if eyes_detected >= 2:
            # Well-defined features
            pitta_geo += 10
        elif eyes_detected == 1:
            vata_geo += 5
        
        return {
            'face_ratio': ratio,
            'eyes_detected': eyes_detected,
            'vata_score': vata_geo,
            'pitta_score': pitta_geo,
            'kapha_score': kapha_geo
        }
    
    # ------------------------------------------------------------------------
    # FEATURE EXTRACTION - COLOR ANALYSIS (20%)
    # ------------------------------------------------------------------------
    
    def extract_redness(self, face_region: np.ndarray) -> float:
        """
        Extract red channel intensity
        Range: 0-255
        """
        try:
            # Extract BGR channels
            b, g, r = cv2.split(face_region)
            
            # Calculate mean red intensity
            red_intensity = float(np.mean(r))
            
            return round(red_intensity, 2)
        except Exception as e:
            print(f"❌ Redness extraction error: {str(e)}")
            return 0.0
    
    def extract_hsv_tone(self, face_region: np.ndarray) -> Dict:
        """
        Extract HSV color tone
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
            print(f"❌ HSV extraction error: {str(e)}")
            return {'hue': 0, 'saturation': 0, 'value': 0}
    
    def analyze_color(self, face_region: np.ndarray) -> Dict:
        """
        Complete color analysis
        """
        redness = self.extract_redness(face_region)
        hsv = self.extract_hsv_tone(face_region)
        
        # Scoring logic
        vata_color = 0
        pitta_color = 0
        kapha_color = 0
        
        # Redness rules
        if redness > 140:
            pitta_color += 40  # High red → Pitta (warm)
        elif redness < 100:
            vata_color += 30  # Low red → Vata (pale)
        else:
            kapha_color += 20  # Medium red → Kapha
        
        # Saturation rules
        if hsv['saturation'] < 50:
            vata_color += 20  # Dull → Vata
        elif hsv['saturation'] > 100:
            pitta_color += 20  # Vibrant → Pitta
        else:
            kapha_color += 15  # Even tone → Kapha
        
        return {
            'redness': redness,
            'hue': hsv['hue'],
            'saturation': hsv['saturation'],
            'value': hsv['value'],
            'vata_score': vata_color,
            'pitta_score': pitta_color,
            'kapha_score': kapha_color
        }
    
    # ------------------------------------------------------------------------
    # FEATURE EXTRACTION - TEXTURE ANALYSIS (10%)
    # ------------------------------------------------------------------------
    
    def extract_texture(self, face_region: np.ndarray) -> float:
        """
        Extract skin texture using Laplacian variance
        Higher value = rougher texture (Vata)
        Lower value = smoother texture (Kapha)
        """
        try:
            gray = cv2.cvtColor(face_region, cv2.COLOR_BGR2GRAY)
            
            # Apply Laplacian operator
            laplacian = cv2.Laplacian(gray, cv2.CV_64F)
            
            # Calculate variance
            texture_score = float(laplacian.var())
            
            return round(texture_score, 2)
        except Exception as e:
            print(f"❌ Texture extraction error: {str(e)}")
            return 0.0
    
    def analyze_texture(self, face_region: np.ndarray) -> Dict:
        """
        Complete texture analysis
        """
        texture = self.extract_texture(face_region)
        
        # Scoring logic
        vata_texture = 0
        pitta_texture = 0
        kapha_texture = 0
        
        # Texture rules
        if texture > 500:
            vata_texture += 50  # High roughness → Vata
        elif texture < 200:
            kapha_texture += 50  # Smooth → Kapha
        else:
            pitta_texture += 30  # Medium → Pitta
        
        return {
            'texture_variance': texture,
            'vata_score': vata_texture,
            'pitta_score': pitta_texture,
            'kapha_score': kapha_texture
        }

# >>> CONTINUE

    # ========================================================================
    # PART 2: SCORING ENGINE AND CONFIDENCE CALCULATION
    # ========================================================================
    
    def compute_image_score(self, features: Dict) -> Dict:
        """
        Compute weighted dosha scores for a single image
        
        FINAL_SCORE = (Skin * 40%) + (Geometry * 30%) + (Color * 20%) + (Texture * 10%)
        """
        try:
            # Extract component scores
            skin = features['skin_analysis']
            geometry = features['facial_geometry']
            color = features['color_analysis']
            texture = features['texture_analysis']
            
            # Calculate weighted scores
            vata_total = (
                skin['vata_score'] * self.weights['skin_analysis'] +
                geometry['vata_score'] * self.weights['facial_geometry'] +
                color['vata_score'] * self.weights['color_analysis'] +
                texture['vata_score'] * self.weights['texture_analysis']
            )
            
            pitta_total = (
                skin['pitta_score'] * self.weights['skin_analysis'] +
                geometry['pitta_score'] * self.weights['facial_geometry'] +
                color['pitta_score'] * self.weights['color_analysis'] +
                texture['pitta_score'] * self.weights['texture_analysis']
            )
            
            kapha_total = (
                skin['kapha_score'] * self.weights['skin_analysis'] +
                geometry['kapha_score'] * self.weights['facial_geometry'] +
                color['kapha_score'] * self.weights['color_analysis'] +
                texture['kapha_score'] * self.weights['texture_analysis']
            )
            
            # Normalize to percentages
            total = vata_total + pitta_total + kapha_total
            
            if total > 0:
                vata_percent = (vata_total / total) * 100
                pitta_percent = (pitta_total / total) * 100
                kapha_percent = (kapha_total / total) * 100
            else:
                vata_percent = pitta_percent = kapha_percent = 33.33
            
            return {
                'vata': round(vata_percent, 2),
                'pitta': round(pitta_percent, 2),
                'kapha': round(kapha_percent, 2),
                'raw_scores': {
                    'vata': round(vata_total, 2),
                    'pitta': round(pitta_total, 2),
                    'kapha': round(kapha_total, 2)
                }
            }
            
        except Exception as e:
            print(f"❌ Score computation error: {str(e)}")
            return {
                'vata': 33.33,
                'pitta': 33.33,
                'kapha': 33.33,
                'raw_scores': {'vata': 0, 'pitta': 0, 'kapha': 0}
            }
    
    def calculate_confidence(self, scores: Dict) -> float:
        """
        Calculate confidence score
        confidence = max(score) / total_score
        """
        try:
            vata = scores['vata']
            pitta = scores['pitta']
            kapha = scores['kapha']
            
            max_score = max(vata, pitta, kapha)
            total = vata + pitta + kapha
            
            if total > 0:
                confidence = max_score / total
            else:
                confidence = 0.0
            
            return round(confidence, 3)
            
        except Exception as e:
            print(f"❌ Confidence calculation error: {str(e)}")
            return 0.0
    
    # ========================================================================
    # PART 3: SINGLE IMAGE ANALYSIS
    # ========================================================================
    
    def analyze_single_image(self, image_path: str) -> Optional[Dict]:
        """
        Analyze a single image and return complete results
        """
        print(f"\n📸 Processing: {os.path.basename(image_path)}")
        
        # Load image
        image = self.load_image_from_path(image_path)
        if image is None:
            return None
        
        # Detect face
        face_data = self.detect_face(image)
        if face_data is None:
            print(f"   ❌ No face detected")
            return None
        
        face_region = face_data['face_region']
        bbox = face_data['bbox']
        eyes_detected = face_data['eyes_detected']
        
        print(f"   ✅ Face detected ({bbox['width']}x{bbox['height']})")
        
        # Extract all features
        skin_analysis = self.analyze_skin(face_region)
        geometry_analysis = self.analyze_facial_geometry(bbox, eyes_detected)
        color_analysis = self.analyze_color(face_region)
        texture_analysis = self.analyze_texture(face_region)
        
        # Compile features
        features = {
            'skin_analysis': skin_analysis,
            'facial_geometry': geometry_analysis,
            'color_analysis': color_analysis,
            'texture_analysis': texture_analysis
        }
        
        # Compute scores
        scores = self.compute_image_score(features)
        
        # Calculate confidence
        confidence = self.calculate_confidence(scores)
        
        print(f"   📊 Scores: V={scores['vata']:.1f}% P={scores['pitta']:.1f}% K={scores['kapha']:.1f}%")
        print(f"   🎯 Confidence: {confidence:.2%}")
        
        return {
            'image_path': image_path,
            'features': features,
            'scores': scores,
            'confidence': confidence,
            'valid': confidence >= self.confidence_threshold
        }
    
    # ========================================================================
    # PART 4: MULTI-IMAGE AGGREGATION
    # ========================================================================
    
    def aggregate_scores(self, all_results: List[Dict]) -> Dict:
        """
        Aggregate scores from multiple images using weighted average
        
        final_score += image_score * confidence
        """
        print("\n" + "="*60)
        print("🔄 AGGREGATING RESULTS FROM MULTIPLE IMAGES")
        print("="*60)
        
        # Filter valid images
        valid_results = [r for r in all_results if r and r.get('valid', False)]
        
        total_images = len(all_results)
        valid_images = len(valid_results)
        
        print(f"\n📊 Total images processed: {total_images}")
        print(f"✅ Valid images used: {valid_images}")
        
        if valid_images == 0:
            print("❌ No valid images for aggregation")
            return {
                'vata': 33.33,
                'pitta': 33.33,
                'kapha': 33.33,
                'confidence': 0.0,
                'valid_images': 0,
                'total_images': total_images
            }
        
        # Weighted aggregation
        vata_weighted = 0
        pitta_weighted = 0
        kapha_weighted = 0
        total_confidence = 0
        
        for result in valid_results:
            scores = result['scores']
            confidence = result['confidence']
            
            vata_weighted += scores['vata'] * confidence
            pitta_weighted += scores['pitta'] * confidence
            kapha_weighted += scores['kapha'] * confidence
            total_confidence += confidence
        
        # Normalize
        if total_confidence > 0:
            vata_final = vata_weighted / total_confidence
            pitta_final = pitta_weighted / total_confidence
            kapha_final = kapha_weighted / total_confidence
        else:
            vata_final = pitta_final = kapha_final = 33.33
        
        # Overall confidence (average of all confidences)
        overall_confidence = total_confidence / valid_images if valid_images > 0 else 0.0
        
        return {
            'vata': round(vata_final, 2),
            'pitta': round(pitta_final, 2),
            'kapha': round(kapha_final, 2),
            'confidence': round(overall_confidence, 3),
            'valid_images': valid_images,
            'total_images': total_images
        }
    
    # ========================================================================
    # PART 5: EXPLANATION GENERATION
    # ========================================================================
    
    def generate_explanation(self, final_scores: Dict, all_results: List[Dict]) -> str:
        """
        Generate clinical explanation for final dosha determination
        """
        vata = final_scores['vata']
        pitta = final_scores['pitta']
        kapha = final_scores['kapha']
        
        # Determine dominant dosha
        doshas = {'Vata': vata, 'Pitta': pitta, 'Kapha': kapha}
        dominant = max(doshas, key=doshas.get)
        dominant_score = doshas[dominant]
        
        # Analyze patterns across images
        valid_results = [r for r in all_results if r and r.get('valid', False)]
        
        if len(valid_results) == 0:
            return "Insufficient data for clinical explanation."
        
        # Aggregate feature patterns
        avg_brightness = np.mean([
            r['features']['skin_analysis']['brightness'] 
            for r in valid_results
        ])
        avg_redness = np.mean([
            r['features']['color_analysis']['redness'] 
            for r in valid_results
        ])
        avg_ratio = np.mean([
            r['features']['facial_geometry']['face_ratio'] 
            for r in valid_results
        ])
        avg_texture = np.mean([
            r['features']['texture_analysis']['texture_variance'] 
            for r in valid_results
        ])
        
        # Build explanation
        explanation_parts = []
        
        explanation_parts.append(
            f"Final analysis based on {final_scores['valid_images']} images "
            f"indicates {dominant} dominance ({dominant_score:.1f}%)"
        )
        
        # Add specific observations
        observations = []
        
        if dominant == 'Vata':
            if avg_brightness < 120:
                observations.append("lower skin brightness (dry, thin skin characteristic)")
            if avg_ratio < 0.8:
                observations.append("angular facial proportions (thin face structure)")
            if avg_texture > 400:
                observations.append("rough skin texture")
        
        elif dominant == 'Pitta':
            if avg_redness > 130:
                observations.append("higher redness levels (warm, sensitive skin)")
            if 0.75 <= avg_ratio <= 0.9:
                observations.append("medium facial proportions (balanced structure)")
            if 200 <= avg_texture <= 500:
                observations.append("moderate skin texture")
        
        elif dominant == 'Kapha':
            if avg_brightness > 150:
                observations.append("higher skin brightness (oily, smooth skin)")
            if avg_ratio > 0.85:
                observations.append("wider facial proportions (round face structure)")
            if avg_texture < 250:
                observations.append("smooth skin texture")
        
        if observations:
            explanation_parts.append("due to consistent visual patterns including")
            explanation_parts.append(", ".join(observations))
        
        return " ".join(explanation_parts) + "."
    
    # ========================================================================
    # PART 6: MAIN ANALYSIS PIPELINE
    # ========================================================================
    
    def analyze_multiple_images(self, image_paths: List[str]) -> Dict:
        """
        Main pipeline: Analyze multiple images and return aggregated result
        
        Args:
            image_paths: List of image file paths
        
        Returns:
            Dictionary with final aggregated dosha scores
        """
        print("\n" + "="*60)
        print("🌿 AYURVEDIC FACE ANALYSIS - MULTI-IMAGE AGGREGATION")
        print("="*60)
        print(f"\n📂 Total images to process: {len(image_paths)}")
        
        # Analyze each image
        all_results = []
        for image_path in image_paths:
            result = self.analyze_single_image(image_path)
            all_results.append(result)
        
        # Aggregate scores
        final_scores = self.aggregate_scores(all_results)
        
        # Generate explanation
        explanation = self.generate_explanation(final_scores, all_results)
        
        # Determine dominant dosha
        doshas = {
            'Vata': final_scores['vata'],
            'Pitta': final_scores['pitta'],
            'Kapha': final_scores['kapha']
        }
        dominant = max(doshas, key=doshas.get)
        
        # Compile final result
        final_result = {
            'total_images': final_scores['total_images'],
            'valid_images': final_scores['valid_images'],
            'scores': {
                'vata': final_scores['vata'],
                'pitta': final_scores['pitta'],
                'kapha': final_scores['kapha']
            },
            'dominant_dosha': dominant,
            'confidence': final_scores['confidence'],
            'explanation': explanation,
            'individual_results': all_results
        }
        
        return final_result
    
    def print_final_report(self, result: Dict):
        """
        Print formatted final report
        """
        print("\n" + "="*60)
        print("📋 FINAL AYURVEDIC DOSHA ANALYSIS REPORT")
        print("="*60)
        
        print(f"\n📊 Images Processed:")
        print(f"   • Total images: {result['total_images']}")
        print(f"   • Valid images used: {result['valid_images']}")
        print(f"   • Skipped (low confidence): {result['total_images'] - result['valid_images']}")
        
        print(f"\n⚖️ Final Dosha Scores:")
        print(f"   • Vata:  {result['scores']['vata']:.2f}%")
        print(f"   • Pitta: {result['scores']['pitta']:.2f}%")
        print(f"   • Kapha: {result['scores']['kapha']:.2f}%")
        
        print(f"\n🎯 Dominant Dosha: {result['dominant_dosha']}")
        print(f"🔍 Overall Confidence: {result['confidence']:.2%}")
        
        print(f"\n💡 Clinical Explanation:")
        print(f"   {result['explanation']}")
        
        print("\n" + "="*60)
        print("✅ ANALYSIS COMPLETE")
        print("="*60)

# >>> CONTINUE


# ============================================================================
# PART 7: EXAMPLE USAGE AND TESTING
# ============================================================================

def main():
    """
    Example usage of the Advanced Face Analysis System
    """
    print("\n" + "="*60)
    print("🕉️ AYURAI VEDA - ADVANCED FACE ANALYSIS SYSTEM")
    print("="*60)
    print("\nVersion: 2.0 - Production Ready")
    print("Features: Multi-image aggregation with weighted scoring")
    print("\n" + "="*60)
    
    # Initialize analyzer
    analyzer = AdvancedFaceAnalyzer()
    
    # Example 1: Single image analysis
    print("\n\n📌 EXAMPLE 1: SINGLE IMAGE ANALYSIS")
    print("-" * 60)
    
    single_image = ["test_face.jpg"]  # Replace with actual image path
    
    if os.path.exists(single_image[0]):
        result = analyzer.analyze_multiple_images(single_image)
        analyzer.print_final_report(result)
    else:
        print(f"⚠️ Image not found: {single_image[0]}")
        print("   Please provide a valid image path")
    
    # Example 2: Multiple images analysis
    print("\n\n📌 EXAMPLE 2: MULTIPLE IMAGES ANALYSIS")
    print("-" * 60)
    
    multiple_images = [
        "face1.jpg",
        "face2.jpg",
        "face3.jpg"
    ]
    
    # Check if any images exist
    existing_images = [img for img in multiple_images if os.path.exists(img)]
    
    if existing_images:
        result = analyzer.analyze_multiple_images(existing_images)
        analyzer.print_final_report(result)
    else:
        print("⚠️ No valid images found")
        print("   Please provide valid image paths in the multiple_images list")
    
    # Example 3: Programmatic usage
    print("\n\n📌 EXAMPLE 3: PROGRAMMATIC USAGE")
    print("-" * 60)
    print("\nCode example:")
    print("""
    from advanced_face_analysis import AdvancedFaceAnalyzer
    
    # Initialize
    analyzer = AdvancedFaceAnalyzer()
    
    # Analyze images
    images = ["face1.jpg", "face2.jpg", "face3.jpg"]
    result = analyzer.analyze_multiple_images(images)
    
    # Access results
    print(f"Dominant Dosha: {result['dominant_dosha']}")
    print(f"Vata: {result['scores']['vata']}%")
    print(f"Pitta: {result['scores']['pitta']}%")
    print(f"Kapha: {result['scores']['kapha']}%")
    print(f"Confidence: {result['confidence']:.2%}")
    """)
    
    print("\n" + "="*60)
    print("📚 USAGE INSTRUCTIONS")
    print("="*60)
    print("""
1. Install requirements:
   pip install opencv-python numpy pillow

2. Prepare images:
   - Use clear, front-facing photos
   - Good lighting conditions
   - Face should be clearly visible
   - Multiple angles recommended for better accuracy

3. Run analysis:
   python advanced_face_analysis.py

4. Interpret results:
   - Vata: Dry, thin, angular features
   - Pitta: Warm, reddish, medium features
   - Kapha: Oily, round, smooth features
   - Confidence > 0.5 indicates reliable result

5. Clinical recommendations:
   - High Vata: Warm foods, oil massage, routine
   - High Pitta: Cooling foods, avoid heat, moderation
   - High Kapha: Light foods, exercise, stay active
    """)
    
    print("\n" + "="*60)
    print("⚠️ IMPORTANT DISCLAIMER")
    print("="*60)
    print("""
This system provides educational and preventive health insights only.
It is NOT a medical diagnosis platform.
Always consult qualified healthcare professionals for medical advice.

Based on traditional Ayurvedic principles of Darshana Pariksha
(visual examination) combined with modern computer vision techniques.
    """)
    
    print("\n" + "="*60)
    print("🌿 AyurAI Veda | Ancient Wisdom. Intelligent Health.")
    print("="*60)


# ============================================================================
# PART 8: UTILITY FUNCTIONS
# ============================================================================

def batch_analyze_directory(directory_path: str, output_file: str = "analysis_results.txt"):
    """
    Analyze all images in a directory and save results
    """
    import glob
    
    print(f"\n📂 Scanning directory: {directory_path}")
    
    # Get all image files
    image_extensions = ['*.jpg', '*.jpeg', '*.png', '*.bmp']
    image_paths = []
    
    for ext in image_extensions:
        image_paths.extend(glob.glob(os.path.join(directory_path, ext)))
        image_paths.extend(glob.glob(os.path.join(directory_path, ext.upper())))
    
    if not image_paths:
        print("❌ No images found in directory")
        return
    
    print(f"✅ Found {len(image_paths)} images")
    
    # Initialize analyzer
    analyzer = AdvancedFaceAnalyzer()
    
    # Analyze all images
    result = analyzer.analyze_multiple_images(image_paths)
    
    # Print report
    analyzer.print_final_report(result)
    
    # Save to file
    with open(output_file, 'w') as f:
        f.write("="*60 + "\n")
        f.write("AYURVEDIC FACE ANALYSIS REPORT\n")
        f.write("="*60 + "\n\n")
        f.write(f"Total images: {result['total_images']}\n")
        f.write(f"Valid images: {result['valid_images']}\n\n")
        f.write(f"Final Scores:\n")
        f.write(f"  Vata:  {result['scores']['vata']:.2f}%\n")
        f.write(f"  Pitta: {result['scores']['pitta']:.2f}%\n")
        f.write(f"  Kapha: {result['scores']['kapha']:.2f}%\n\n")
        f.write(f"Dominant Dosha: {result['dominant_dosha']}\n")
        f.write(f"Confidence: {result['confidence']:.2%}\n\n")
        f.write(f"Explanation:\n{result['explanation']}\n")
    
    print(f"\n💾 Results saved to: {output_file}")


def analyze_from_webcam(num_captures: int = 3, delay_seconds: int = 2):
    """
    Capture images from webcam and analyze
    """
    import time
    
    print("\n📷 Starting webcam capture...")
    print(f"   Will capture {num_captures} images with {delay_seconds}s delay")
    
    cap = cv2.VideoCapture(0)
    
    if not cap.isOpened():
        print("❌ Could not open webcam")
        return
    
    captured_images = []
    temp_dir = "temp_captures"
    os.makedirs(temp_dir, exist_ok=True)
    
    for i in range(num_captures):
        print(f"\n📸 Capture {i+1}/{num_captures} in {delay_seconds} seconds...")
        time.sleep(delay_seconds)
        
        ret, frame = cap.read()
        if ret:
            filename = os.path.join(temp_dir, f"capture_{i+1}.jpg")
            cv2.imwrite(filename, frame)
            captured_images.append(filename)
            print(f"   ✅ Saved: {filename}")
        else:
            print(f"   ❌ Failed to capture image {i+1}")
    
    cap.release()
    
    if captured_images:
        print(f"\n✅ Captured {len(captured_images)} images")
        print("🔄 Starting analysis...")
        
        analyzer = AdvancedFaceAnalyzer()
        result = analyzer.analyze_multiple_images(captured_images)
        analyzer.print_final_report(result)
        
        # Cleanup
        print(f"\n🗑️ Cleaning up temporary files...")
        for img in captured_images:
            os.remove(img)
        os.rmdir(temp_dir)
    else:
        print("❌ No images captured")


# ============================================================================
# PART 9: API INTEGRATION HELPER
# ============================================================================

class FaceAnalysisAPI:
    """
    API-ready wrapper for face analysis
    Returns JSON-serializable results
    """
    
    def __init__(self):
        self.analyzer = AdvancedFaceAnalyzer()
    
    def analyze_base64_images(self, base64_images: List[str]) -> Dict:
        """
        Analyze images from base64 strings
        """
        temp_dir = "temp_api"
        os.makedirs(temp_dir, exist_ok=True)
        
        image_paths = []
        
        for i, b64_img in enumerate(base64_images):
            try:
                image = self.analyzer.load_image_from_base64(b64_img)
                if image is not None:
                    filename = os.path.join(temp_dir, f"api_image_{i}.jpg")
                    cv2.imwrite(filename, image)
                    image_paths.append(filename)
            except Exception as e:
                print(f"❌ Error processing base64 image {i}: {str(e)}")
        
        if not image_paths:
            return {
                'success': False,
                'error': 'No valid images provided'
            }
        
        # Analyze
        result = self.analyzer.analyze_multiple_images(image_paths)
        
        # Cleanup
        for img in image_paths:
            try:
                os.remove(img)
            except:
                pass
        try:
            os.rmdir(temp_dir)
        except:
            pass
        
        # Return API-friendly result
        return {
            'success': True,
            'total_images': result['total_images'],
            'valid_images': result['valid_images'],
            'scores': {
                'vata': float(result['scores']['vata']),
                'pitta': float(result['scores']['pitta']),
                'kapha': float(result['scores']['kapha'])
            },
            'dominant': result['dominant_dosha'],
            'confidence': float(result['confidence']),
            'explanation': result['explanation']
        }


# ============================================================================
# MAIN EXECUTION
# ============================================================================

if __name__ == "__main__":
    import sys
    
    # Check command line arguments
    if len(sys.argv) > 1:
        if sys.argv[1] == "--directory" and len(sys.argv) > 2:
            # Batch analyze directory
            batch_analyze_directory(sys.argv[2])
        elif sys.argv[1] == "--webcam":
            # Webcam capture mode
            num_captures = int(sys.argv[2]) if len(sys.argv) > 2 else 3
            analyze_from_webcam(num_captures)
        elif sys.argv[1] == "--help":
            print("""
Usage:
  python advanced_face_analysis.py                    # Run examples
  python advanced_face_analysis.py --directory PATH   # Analyze directory
  python advanced_face_analysis.py --webcam [N]       # Capture N images from webcam
  python advanced_face_analysis.py --help             # Show this help
            """)
        else:
            # Analyze provided image paths
            image_paths = sys.argv[1:]
            analyzer = AdvancedFaceAnalyzer()
            result = analyzer.analyze_multiple_images(image_paths)
            analyzer.print_final_report(result)
    else:
        # Run main examples
        main()

# >>> COMPLETE
