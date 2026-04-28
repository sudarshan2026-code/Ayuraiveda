"""
ML Prediction Module for Dosha Analysis
Uses extracted features to predict Vata, Pitta, Kapha percentages
"""

import pickle
import numpy as np
from typing import Dict, List
import os


class DoshaPredictor:
    """ML-based Dosha prediction using feature vectors"""
    
    def __init__(self, model_path: str = None):
        """
        Initialize predictor with trained model
        
        Args:
            model_path: Path to trained model (.pkl file)
        """
        if model_path is None:
            model_path = os.path.join(os.path.dirname(__file__), 'dosha_assessment_model.pkl')
        
        self.model_path = model_path
        self.model = None
        self.load_model()
        
        # Feature importance mapping (for explainability)
        self.feature_names = [
            'skin_texture', 'oiliness', 'pigmentation', 'wrinkles',
            'face_ratio', 'jaw_width', 'eye_spacing', 'nose_ratio',
            'skin_tone_hue', 'redness', 'brightness',
            'body_frame', 'shoulder_ratio', 'posture'
        ]
        
        # Dosha characteristic mappings
        self.dosha_characteristics = {
            'vata': {
                'skin_texture': 'high',  # Rough, dry skin
                'oiliness': 'low',       # Dry skin
                'face_ratio': 'low',     # Narrow face
                'body_frame': 'low',     # Thin body
                'brightness': 'low'      # Dull complexion
            },
            'pitta': {
                'skin_texture': 'medium',
                'oiliness': 'medium',
                'redness': 'high',       # Reddish skin
                'face_ratio': 'medium',  # Balanced face
                'brightness': 'high'     # Radiant complexion
            },
            'kapha': {
                'oiliness': 'high',      # Oily skin
                'pigmentation': 'low',   # Even skin tone
                'face_ratio': 'high',    # Broad face
                'body_frame': 'high',    # Heavy body
                'brightness': 'medium'   # Glowing skin
            }
        }
    
    def load_model(self):
        """Load trained ML model"""
        try:
            with open(self.model_path, 'rb') as f:
                self.model = pickle.load(f)
            print(f"✓ Model loaded from {self.model_path}")
        except FileNotFoundError:
            print(f"⚠ Model file not found: {self.model_path}")
            print("  Using rule-based fallback prediction")
            self.model = None
        except Exception as e:
            print(f"⚠ Error loading model: {e}")
            print("  Using rule-based fallback prediction")
            self.model = None
    
    def predict_with_model(self, feature_vector: np.ndarray) -> Dict[str, float]:
        """
        Predict using trained ML model
        
        Args:
            feature_vector: 1D numpy array of features
            
        Returns:
            Dictionary with dosha percentages
        """
        try:
            # Reshape for single prediction
            features = feature_vector.reshape(1, -1)
            
            # Get prediction
            prediction = self.model.predict_proba(features)[0]
            
            # Assuming model outputs [vata, pitta, kapha] probabilities
            return {
                'vata': float(prediction[0] * 100),
                'pitta': float(prediction[1] * 100),
                'kapha': float(prediction[2] * 100)
            }
        except Exception as e:
            print(f"Model prediction error: {e}")
            return None
    
    def predict_rule_based(self, features: Dict[str, float]) -> Dict[str, float]:
        """
        Rule-based prediction (fallback if model not available)
        
        Args:
            features: Dictionary of extracted features
            
        Returns:
            Dictionary with dosha percentages
        """
        vata_score = 0
        pitta_score = 0
        kapha_score = 0
        
        # VATA SCORING (Dry, rough, thin, irregular)
        vata_score += features.get('skin_texture', 0) * 3  # High texture = rough = Vata
        vata_score += (1 - features.get('oiliness', 0.5)) * 3  # Low oil = dry = Vata
        vata_score += (1 - features.get('face_ratio', 0.5)) * 2  # Narrow face = Vata
        vata_score += (1 - features.get('body_frame', 0.5)) * 3  # Thin body = Vata
        vata_score += features.get('wrinkles', 0) * 2  # More wrinkles = Vata
        
        # PITTA SCORING (Hot, sharp, oily, reddish)
        pitta_score += features.get('redness', 0) * 4  # Redness = Pitta
        pitta_score += features.get('oiliness', 0) * 2  # Moderate oil = Pitta
        pitta_score += features.get('brightness', 0) * 2  # Radiant = Pitta
        pitta_score += abs(features.get('face_ratio', 0.5) - 0.5) * -2 + 2  # Balanced face
        pitta_score += features.get('pigmentation', 0) * 2  # Uneven tone = Pitta
        
        # KAPHA SCORING (Heavy, oily, smooth, stable)
        kapha_score += features.get('oiliness', 0) * 4  # High oil = Kapha
        kapha_score += (1 - features.get('skin_texture', 0.5)) * 3  # Smooth = Kapha
        kapha_score += features.get('face_ratio', 0) * 2  # Broad face = Kapha
        kapha_score += features.get('body_frame', 0) * 3  # Heavy body = Kapha
        kapha_score += (1 - features.get('wrinkles', 0.5)) * 2  # Fewer wrinkles = Kapha
        
        # Normalize to percentages
        total = vata_score + pitta_score + kapha_score
        if total > 0:
            vata_percent = (vata_score / total) * 100
            pitta_percent = (pitta_score / total) * 100
            kapha_percent = (kapha_score / total) * 100
        else:
            vata_percent = pitta_percent = kapha_percent = 33.33
        
        return {
            'vata': round(vata_percent, 2),
            'pitta': round(pitta_percent, 2),
            'kapha': round(kapha_percent, 2)
        }
    
    def predict(self, features: Dict[str, float], feature_vector: np.ndarray = None) -> Dict[str, any]:
        """
        Main prediction function
        
        Args:
            features: Dictionary of extracted features
            feature_vector: Optional pre-computed feature vector
            
        Returns:
            Complete prediction with dosha percentages
        """
        # Try ML model first
        if self.model is not None and feature_vector is not None:
            ml_prediction = self.predict_with_model(feature_vector)
            if ml_prediction is not None:
                return {
                    'method': 'ml_model',
                    'doshas': ml_prediction,
                    'dominant': self._get_dominant_dosha(ml_prediction)
                }
        
        # Fallback to rule-based
        rule_prediction = self.predict_rule_based(features)
        return {
            'method': 'rule_based',
            'doshas': rule_prediction,
            'dominant': self._get_dominant_dosha(rule_prediction)
        }
    
    def _get_dominant_dosha(self, doshas: Dict[str, float]) -> str:
        """Get dominant dosha from percentages"""
        return max(doshas, key=doshas.get).capitalize()
    
    def generate_explanation(self, features: Dict[str, float], doshas: Dict[str, float]) -> Dict[str, any]:
        """
        Generate explainability for prediction
        
        Returns:
            Dictionary with reasoning and key factors
        """
        dominant = self._get_dominant_dosha(doshas)
        dominant_lower = dominant.lower()
        
        # Identify key contributing features
        key_factors = []
        
        if dominant_lower == 'vata':
            if features.get('skin_texture', 0) > 0.6:
                key_factors.append("Rough, dry skin texture")
            if features.get('oiliness', 1) < 0.3:
                key_factors.append("Low skin oiliness (dry skin)")
            if features.get('face_ratio', 0.5) < 0.4:
                key_factors.append("Narrow facial structure")
            if features.get('body_frame', 0.5) < 0.4:
                key_factors.append("Lean body frame")
            if features.get('wrinkles', 0) > 0.4:
                key_factors.append("Visible fine lines")
        
        elif dominant_lower == 'pitta':
            if features.get('redness', 0) > 0.6:
                key_factors.append("Reddish skin tone")
            if 0.3 < features.get('oiliness', 0) < 0.7:
                key_factors.append("Moderate skin oiliness")
            if features.get('brightness', 0) > 0.6:
                key_factors.append("Radiant, bright complexion")
            if 0.4 < features.get('face_ratio', 0) < 0.6:
                key_factors.append("Balanced facial proportions")
            if features.get('pigmentation', 0) > 0.5:
                key_factors.append("Uneven skin pigmentation")
        
        elif dominant_lower == 'kapha':
            if features.get('oiliness', 0) > 0.7:
                key_factors.append("High skin oiliness")
            if features.get('skin_texture', 1) < 0.3:
                key_factors.append("Smooth skin texture")
            if features.get('face_ratio', 0) > 0.6:
                key_factors.append("Broad facial structure")
            if features.get('body_frame', 0) > 0.6:
                key_factors.append("Heavy, solid body frame")
            if features.get('pigmentation', 1) < 0.3:
                key_factors.append("Even skin tone")
        
        # Generate summary text
        if len(key_factors) == 0:
            key_factors.append("Balanced characteristics")
        
        summary = f"High {dominant} dominance ({doshas[dominant_lower]:.1f}%) detected based on: " + ", ".join(key_factors[:3])
        
        return {
            'summary': summary,
            'key_factors': key_factors,
            'dominant_dosha': dominant,
            'confidence': 'High' if doshas[dominant_lower] > 50 else 'Moderate' if doshas[dominant_lower] > 40 else 'Low'
        }
    
    def get_recommendations(self, dominant_dosha: str) -> Dict[str, List[str]]:
        """
        Get Ayurvedic recommendations based on dominant dosha
        
        Returns:
            Dictionary with recommendations
        """
        recommendations = {
            'vata': {
                'diet': [
                    'Warm, cooked, moist foods',
                    'Sweet, sour, and salty tastes',
                    'Healthy fats (ghee, sesame oil)',
                    'Avoid cold, dry, raw foods'
                ],
                'lifestyle': [
                    'Maintain regular daily routine',
                    'Get 7-8 hours of sleep',
                    'Practice oil massage (Abhyanga)',
                    'Stay warm and avoid cold environments'
                ],
                'exercise': [
                    'Gentle yoga and stretching',
                    'Walking in nature',
                    'Avoid excessive cardio',
                    'Focus on grounding practices'
                ]
            },
            'pitta': {
                'diet': [
                    'Cooling foods (cucumber, coconut)',
                    'Sweet, bitter, and astringent tastes',
                    'Avoid spicy, hot, acidic foods',
                    'Moderate portions'
                ],
                'lifestyle': [
                    'Stay cool, avoid excessive heat',
                    'Practice moderation in all activities',
                    'Avoid overwork and competition',
                    'Spend time in nature'
                ],
                'exercise': [
                    'Swimming and water activities',
                    'Moderate intensity workouts',
                    'Cooling pranayama',
                    'Avoid competitive sports'
                ]
            },
            'kapha': {
                'diet': [
                    'Light, warm, spicy foods',
                    'Pungent, bitter, and astringent tastes',
                    'Avoid heavy, oily, sweet foods',
                    'Reduce dairy intake'
                ],
                'lifestyle': [
                    'Wake up early (before 6 AM)',
                    'Stay active throughout the day',
                    'Avoid daytime sleeping',
                    'Engage in stimulating activities'
                ],
                'exercise': [
                    'Vigorous cardio (45+ min daily)',
                    'High-intensity workouts',
                    'Energizing pranayama',
                    'Dynamic yoga styles'
                ]
            }
        }
        
        return recommendations.get(dominant_dosha.lower(), recommendations['vata'])


def test_predictor():
    """Test the predictor"""
    predictor = DoshaPredictor()
    
    # Sample features
    sample_features = {
        'skin_texture': 0.7,
        'oiliness': 0.2,
        'pigmentation': 0.4,
        'wrinkles': 0.5,
        'face_ratio': 0.3,
        'jaw_width': 0.4,
        'eye_spacing': 0.4,
        'nose_ratio': 0.5,
        'skin_tone_hue': 0.3,
        'redness': 0.3,
        'brightness': 0.4,
        'body_frame': 0.3,
        'shoulder_ratio': 0.4,
        'posture': 0.8
    }
    
    # Predict
    result = predictor.predict(sample_features)
    
    print("✓ Prediction successful!")
    print(f"\nMethod: {result['method']}")
    print(f"Dominant Dosha: {result['dominant']}")
    print("\nDosha Percentages:")
    for dosha, percent in result['doshas'].items():
        print(f"  {dosha.capitalize()}: {percent:.2f}%")
    
    # Get explanation
    explanation = predictor.generate_explanation(sample_features, result['doshas'])
    print(f"\nExplanation: {explanation['summary']}")
    print(f"Confidence: {explanation['confidence']}")


if __name__ == "__main__":
    test_predictor()
