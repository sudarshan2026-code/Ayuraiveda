"""
Ayurvedic Clinical Intelligence Engine for Body Analysis
Implements 10-step hierarchical framework for Prakriti estimation
"""

import cv2
import numpy as np
import base64
from io import BytesIO
from PIL import Image


class AyurvedicBodyAnalyzer:
    """
    Ayurvedic Clinical Intelligence Engine
    Analyzes body images using structured 10-step framework
    """
    
    def __init__(self):
        self.confidence_threshold = 0.5
        
    def analyze_image(self, image_data, input_type='base64'):
        """Main analysis pipeline following 10-step framework"""
        
        # Load image
        image = self._load_image(image_data, input_type)
        if image is None:
            return {'success': False, 'error': 'Failed to load image'}
        
        # STEP 0: Input Validation
        validation = self._validate_input(image)
        if not validation['valid']:
            return {
                'success': False,
                'error': validation['message'],
                'confidence': 'Low'
            }
        
        # STEP 1: Structural Analysis (PRIMARY - 50%)
        structural = self._structural_analysis(image)
        
        # STEP 2: Surface Analysis (SECONDARY - 30%)
        surface = self._surface_analysis(image)
        
        # STEP 3: Dynamic Features (TERTIARY - 20%)
        dynamic = self._dynamic_analysis(image)
        
        # STEP 4: Initial Scoring Template
        base_dosha = self._determine_base_dosha(structural)
        scores = self._initialize_scores(base_dosha)
        
        # STEP 5: Controlled Adjustments
        scores = self._apply_adjustments(scores, surface, dynamic)
        
        # STEP 6: Safety Constraints
        scores = self._apply_safety_constraints(scores, structural)
        
        # STEP 7: Normalization
        percentages = self._normalize_scores(scores)
        
        # STEP 8: Final Classification
        classification = self._classify_prakriti(percentages)
        
        # STEP 9: Generate Output
        result = self._generate_output(
            structural, surface, dynamic, base_dosha,
            percentages, classification, validation
        )
        
        return result
    
    def _load_image(self, image_data, input_type):
        """Load image from base64 or array"""
        try:
            if input_type == 'base64':
                if ',' in image_data:
                    image_data = image_data.split(',')[1]
                img_bytes = base64.b64decode(image_data)
                img = Image.open(BytesIO(img_bytes))
                return cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
            return image_data
        except:
            return None
    
    def _validate_input(self, image):
        """STEP 0: Input Validation"""
        h, w = image.shape[:2]
        
        # Check image size
        if h < 200 or w < 150:
            return {'valid': False, 'message': 'Image too small. Please use higher resolution.'}
        
        # Check lighting
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        brightness = np.mean(gray)
        
        if brightness < 50:
            return {
                'valid': True,
                'message': 'Low lighting detected. Confidence reduced.',
                'confidence': 0.4
            }
        elif brightness > 200:
            return {
                'valid': True,
                'message': 'Overexposed image. Confidence reduced.',
                'confidence': 0.5
            }
        
        return {'valid': True, 'message': 'Input validated', 'confidence': 0.8}
    
    def _structural_analysis(self, image):
        """STEP 1: Structural Analysis (PRIMARY - 50%)"""
        h, w = image.shape[:2]
        
        # Detect body contours
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        blur = cv2.GaussianBlur(gray, (5, 5), 0)
        edges = cv2.Canny(blur, 50, 150)
        contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        # Find largest contour (body)
        if contours:
            body_contour = max(contours, key=cv2.contourArea)
            x, y, bw, bh = cv2.boundingRect(body_contour)
        else:
            # Fallback: use center region
            bw, bh = int(w * 0.4), int(h * 0.8)
        
        # Calculate body metrics
        body_ratio = bw / bh if bh > 0 else 0.5
        frame_width = bw / w
        
        # Body Build Classification
        if body_ratio < 0.35:
            body_build = 'lean'
        elif body_ratio < 0.45:
            body_build = 'medium'
        elif body_ratio < 0.55:
            body_build = 'medium-heavy'
        else:
            body_build = 'heavy'
        
        # Frame Width Classification
        if frame_width < 0.35:
            frame = 'narrow'
        elif frame_width < 0.5:
            frame = 'balanced'
        else:
            frame = 'broad'
        
        # Fat Distribution (estimated from body ratio)
        if body_ratio < 0.4:
            fat_dist = 'low'
        elif body_ratio < 0.5:
            fat_dist = 'moderate'
        else:
            fat_dist = 'high'
        
        # Face Shape (upper body region)
        face_region = gray[:int(h*0.3), :]
        face_ratio = face_region.shape[1] / face_region.shape[0] if face_region.shape[0] > 0 else 1.0
        
        if face_ratio < 0.75:
            face_shape = 'angular'
        elif face_ratio < 0.9:
            face_shape = 'oval'
        else:
            face_shape = 'round'
        
        return {
            'body_build': body_build,
            'frame_width': frame,
            'fat_distribution': fat_dist,
            'face_shape': face_shape,
            'body_ratio': body_ratio,
            'frame_ratio': frame_width,
            'confidence': 0.7
        }
    
    def _surface_analysis(self, image):
        """STEP 2: Surface Analysis (SECONDARY - 30%)"""
        # Extract skin region (upper body)
        h, w = image.shape[:2]
        skin_region = image[int(h*0.2):int(h*0.5), int(w*0.3):int(w*0.7)]
        
        if skin_region.size == 0:
            return {'texture': 'normal', 'tone': 'normal', 'confidence': 0.3}
        
        # Convert to LAB color space
        lab = cv2.cvtColor(skin_region, cv2.COLOR_BGR2LAB)
        l_channel = lab[:, :, 0]
        
        # Texture analysis
        laplacian = cv2.Laplacian(l_channel, cv2.CV_64F)
        texture_var = np.var(laplacian)
        
        if texture_var > 100:
            texture = 'dry'
        elif texture_var < 50:
            texture = 'oily'
        else:
            texture = 'normal'
        
        # Tone analysis
        avg_brightness = np.mean(l_channel)
        if avg_brightness < 100:
            tone = 'dull'
        elif avg_brightness > 150:
            tone = 'clear'
        else:
            tone = 'normal'
        
        # Redness detection (a channel in LAB)
        a_channel = lab[:, :, 1]
        redness = np.mean(a_channel)
        
        return {
            'texture': texture,
            'tone': tone,
            'redness': redness,
            'texture_variance': texture_var,
            'confidence': 0.6
        }
    
    def _dynamic_analysis(self, image):
        """STEP 3: Dynamic Features (TERTIARY - 20%)"""
        # Note: Static image has limited dynamic info
        # We infer from structural cues
        
        h, w = image.shape[:2]
        upper_body = image[:int(h*0.4), :]
        
        # Posture inference from body alignment
        gray = cv2.cvtColor(upper_body, cv2.COLOR_BGR2GRAY)
        edges = cv2.Canny(gray, 50, 150)
        lines = cv2.HoughLinesP(edges, 1, np.pi/180, 50, minLineLength=30, maxLineGap=10)
        
        if lines is not None and len(lines) > 10:
            posture = 'restless'
        elif lines is not None and len(lines) > 5:
            posture = 'firm'
        else:
            posture = 'grounded'
        
        return {
            'posture': posture,
            'expression': 'neutral',  # Cannot determine from body
            'confidence': 0.4
        }
    
    def _determine_base_dosha(self, structural):
        """STEP 1: Structure Decision Rule"""
        body = structural['body_build']
        face = structural['face_shape']
        
        # Primary rule: Structure defines base
        if body in ['medium', 'medium-heavy', 'heavy']:
            # NOT Vata
            if face == 'round':
                return 'Kapha'
            else:
                return 'Kapha-Pitta'
        
        if body == 'lean' and face == 'angular':
            return 'Vata'
        
        if body == 'medium' and structural['frame_width'] == 'balanced':
            return 'Pitta-Kapha'
        
        # Default fallback
        if structural.get('confidence', 0) < 0.5:
            return 'Kapha-Pitta'  # NOT Vata by default
        
        return 'Kapha'
    
    def _initialize_scores(self, base_dosha):
        """STEP 4: Initial Scoring Template"""
        templates = {
            'Kapha': {'vata': 20, 'pitta': 30, 'kapha': 50},
            'Pitta': {'vata': 25, 'pitta': 45, 'kapha': 30},
            'Vata': {'vata': 50, 'pitta': 30, 'kapha': 20},
            'Kapha-Pitta': {'vata': 20, 'pitta': 40, 'kapha': 40},
            'Pitta-Vata': {'vata': 35, 'pitta': 40, 'kapha': 25}
        }
        return templates.get(base_dosha, templates['Kapha-Pitta']).copy()
    
    def _apply_adjustments(self, scores, surface, dynamic):
        """STEP 5: Controlled Adjustments (max ±10%)"""
        adjustments = 0
        
        # Surface adjustments
        if surface['texture'] == 'dry':
            scores['vata'] += 5
            adjustments += 5
        elif surface['texture'] == 'oily':
            scores['kapha'] += 5
            adjustments += 5
        
        if surface.get('redness', 0) > 130:
            scores['pitta'] += 3
            adjustments += 3
        
        # Dynamic adjustments
        if dynamic['posture'] == 'restless':
            scores['vata'] += 2
            adjustments += 2
        elif dynamic['posture'] == 'grounded':
            scores['kapha'] += 2
            adjustments += 2
        
        # Cap total adjustments at 10
        if adjustments > 10:
            scale = 10 / adjustments
            # Scale back proportionally (simplified)
            pass
        
        return scores
    
    def _apply_safety_constraints(self, scores, structural):
        """STEP 6: Safety Constraints (MANDATORY)"""
        body = structural['body_build']
        face = structural['face_shape']
        
        # Rule 1: If body ≠ lean → Vata ≤ 35%
        if body != 'lean':
            max_vata = 35
            total = sum(scores.values())
            vata_percent = (scores['vata'] / total) * 100
            if vata_percent > max_vata:
                # Reduce Vata to 35%
                scores['vata'] = int((max_vata / 100) * total)
        
        # Rule 2: If face ≠ angular → reduce Vata
        if face != 'angular':
            scores['vata'] = int(scores['vata'] * 0.8)
        
        # Rule 3: If face is round → Kapha must be highest
        if face == 'round':
            if scores['kapha'] < max(scores['vata'], scores['pitta']):
                max_other = max(scores['vata'], scores['pitta'])
                scores['kapha'] = max_other + 5
        
        # Rule 4: Vata cannot dominate unless lean AND angular
        if not (body == 'lean' and face == 'angular'):
            if scores['vata'] > max(scores['pitta'], scores['kapha']):
                # Swap with highest
                max_dosha = 'pitta' if scores['pitta'] > scores['kapha'] else 'kapha'
                scores['vata'], scores[max_dosha] = scores[max_dosha], scores['vata']
        
        return scores
    
    def _normalize_scores(self, scores):
        """STEP 7: Normalization"""
        total = sum(scores.values())
        if total == 0:
            return {'vata': 33.3, 'pitta': 33.3, 'kapha': 33.3}
        
        return {
            'vata': round((scores['vata'] / total) * 100, 1),
            'pitta': round((scores['pitta'] / total) * 100, 1),
            'kapha': round((scores['kapha'] / total) * 100, 1)
        }
    
    def _classify_prakriti(self, percentages):
        """STEP 8: Final Classification"""
        sorted_doshas = sorted(percentages.items(), key=lambda x: x[1], reverse=True)
        
        # Check if balanced (all within 5%)
        max_diff = sorted_doshas[0][1] - sorted_doshas[2][1]
        if max_diff < 5:
            return 'Balanced (Sama Prakriti)'
        
        # Dominant classification
        dominant = sorted_doshas[0][0].capitalize()
        second = sorted_doshas[1][0].capitalize()
        
        # If second dosha is close (within 10%), it's dual
        if sorted_doshas[0][1] - sorted_doshas[1][1] < 10:
            return f"{dominant}-{second}"
        
        return dominant
    
    def _generate_output(self, structural, surface, dynamic, base_dosha, 
                        percentages, classification, validation):
        """STEP 9: Output Format"""
        
        # Build reasoning
        reasoning = []
        reasoning.append(f"Body build: {structural['body_build']}")
        reasoning.append(f"Frame: {structural['frame_width']}")
        reasoning.append(f"Face shape: {structural['face_shape']}")
        reasoning.append(f"Base dosha determined: {base_dosha}")
        
        if structural['body_build'] != 'lean':
            reasoning.append("Vata reduced due to non-lean body structure")
        
        if surface['texture'] == 'dry':
            reasoning.append("Dry skin texture increases Vata")
        elif surface['texture'] == 'oily':
            reasoning.append("Oily skin texture increases Kapha")
        
        # Confidence calculation
        conf_scores = [
            validation.get('confidence', 0.5),
            structural.get('confidence', 0.5),
            surface.get('confidence', 0.5)
        ]
        avg_confidence = sum(conf_scores) / len(conf_scores)
        
        if avg_confidence > 0.7:
            confidence_level = 'High'
        elif avg_confidence > 0.5:
            confidence_level = 'Medium'
        else:
            confidence_level = 'Low'
        
        return {
            'success': True,
            'structural_analysis': structural,
            'surface_observations': surface,
            'dynamic_observations': dynamic,
            'base_dosha': base_dosha,
            'base_dosha_justification': f"Determined from body build ({structural['body_build']}) and face shape ({structural['face_shape']})",
            'adjustments_applied': reasoning,
            'final_scores': percentages,
            'final_prakriti': classification,
            'confidence_level': confidence_level,
            'confidence_score': round(avg_confidence, 2),
            'disclaimer': 'This is an AI-based Ayurvedic estimation for wellness purposes and not a medical diagnosis.'
        }


def analyze_body_image(image_data, input_type='base64'):
    """Convenience function for body analysis"""
    analyzer = AyurvedicBodyAnalyzer()
    return analyzer.analyze_image(image_data, input_type)
