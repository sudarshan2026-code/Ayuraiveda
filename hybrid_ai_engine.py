"""
Hybrid Tridosha Intelligence Engine™
ML Model + Ayurvedic Rule-Based Validation
"""

import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
import pickle
import os

class HybridTridoshaEngine:
    def __init__(self):
        self.dosha_model = None
        self.severity_model = None
        self.risk_model = None
        self.feature_encoders = {}
        self.model_path = 'hybrid_tridosha_model.pkl'
        
        # Ayurvedic priority weights (hard constraints)
        self.PRIORITY_WEIGHTS = {
            'mental_sleep': 1.0,      # Highest
            'physical_signs': 0.75,   # Second
            'digestion': 0.6,         # Third
            'lifestyle': 0.3          # Lowest
        }
        
        # Decision thresholds
        self.DUAL_DOSHA_THRESHOLD = 0.07  # 7% difference
        self.CONFIDENCE_THRESHOLD = 0.45  # 45% minimum
        self.MAX_DOMINANCE = 0.85         # Cap at 85%
        
    def analyze(self, user_data):
        """Main hybrid analysis pipeline"""
        
        # Step 1: Prepare features
        features = self._prepare_features(user_data)
        
        # Step 2: ML Model Prediction
        ml_prediction = self._ml_predict(features)
        
        # Step 3: Ayurvedic Rule Validation
        validated_prediction = self._validate_with_rules(ml_prediction, user_data)
        
        # Step 4: Dosha Decision (Dual vs Single)
        dosha_decision = self._decide_dosha_dominance(validated_prediction)
        
        # Step 5: Risk Assessment (Model + Rules)
        risk_assessment = self._assess_risk(validated_prediction, dosha_decision, user_data)
        
        # Step 6: Generate Output
        return self._generate_output(dosha_decision, risk_assessment, user_data)
    
    def _prepare_features(self, data):
        """Convert user data to ML features"""
        feature_map = {
            'sleep': {'excellent': 0, 'good': 1, 'poor': 2, 'very_poor': 3, 'excessive': 4},
            'appetite': {'regular': 0, 'irregular': 1, 'excessive': 2, 'low': 3},
            'stress': {'low': 0, 'moderate': 1, 'high': 2},
            'digestion': {'normal': 0, 'constipation': 1, 'acidity': 2, 'gas': 3, 'slow': 4},
            'skin': {'normal': 0, 'dry': 1, 'oily': 2, 'sensitive': 3},
            'temperature': {'normal': 0, 'cold': 1, 'hot': 2},
            'food': {'balanced': 0, 'spicy': 1, 'sweet': 2, 'bitter': 3}
        }
        
        features = [
            feature_map['sleep'].get(data.get('sleep'), 0),
            feature_map['appetite'].get(data.get('appetite'), 0),
            feature_map['stress'].get(data.get('stress'), 0),
            feature_map['digestion'].get(data.get('digestion'), 0),
            feature_map['skin'].get(data.get('skin'), 0),
            feature_map['temperature'].get(data.get('temperature'), 0),
            feature_map['food'].get(data.get('food'), 0),
            int(data.get('age', 25)),
            1 if data.get('gender') == 'male' else 0
        ]
        
        return np.array(features).reshape(1, -1)
    
    def _ml_predict(self, features):
        """ML Model Prediction (simulated with rule-based logic for now)"""
        # In production, load trained model: self.dosha_model.predict_proba(features)
        
        # Simulated ML prediction based on features
        sleep, appetite, stress, digestion, skin, temp, food, age, gender = features[0]
        
        # Initialize confidence scores
        vata_conf = 0.33
        pitta_conf = 0.33
        kapha_conf = 0.33
        
        # Mental + Sleep (highest priority)
        if stress >= 1:
            vata_conf += 0.15 * (stress / 2)
            pitta_conf += 0.08 * (stress / 2)
        
        if sleep >= 2:  # Poor/very poor
            vata_conf += 0.18
        elif sleep == 4:  # Excessive
            kapha_conf += 0.15
        
        # Physical signs (second priority)
        if skin == 1:  # Dry
            vata_conf += 0.12
        elif skin == 2:  # Oily
            kapha_conf += 0.10
        elif skin == 3:  # Sensitive
            pitta_conf += 0.12
        
        if temp == 1:  # Cold
            vata_conf += 0.10
        elif temp == 2:  # Hot
            pitta_conf += 0.12
        
        # Digestion (third priority)
        if digestion == 1:  # Constipation
            vata_conf += 0.14
        elif digestion == 2:  # Acidity
            pitta_conf += 0.14
        elif digestion == 4:  # Slow
            kapha_conf += 0.12
        
        if appetite == 1:  # Irregular
            vata_conf += 0.10
        elif appetite == 2:  # Excessive
            pitta_conf += 0.06
            kapha_conf += 0.06
        
        # Lifestyle (lowest priority)
        if food == 1:  # Spicy
            pitta_conf += 0.05
        elif food == 2:  # Sweet
            kapha_conf += 0.05
        
        # Normalize to sum to 1.0
        total = vata_conf + pitta_conf + kapha_conf
        vata_conf /= total
        pitta_conf /= total
        kapha_conf /= total
        
        # Cap at MAX_DOMINANCE
        vata_conf = min(vata_conf, self.MAX_DOMINANCE)
        pitta_conf = min(pitta_conf, self.MAX_DOMINANCE)
        kapha_conf = min(kapha_conf, self.MAX_DOMINANCE)
        
        # Severity prediction
        max_conf = max(vata_conf, pitta_conf, kapha_conf)
        if max_conf < 0.40:
            severity = 'balanced'
        elif max_conf < 0.55:
            severity = 'mild'
        elif max_conf < 0.70:
            severity = 'moderate'
        else:
            severity = 'severe'
        
        return {
            'vata_confidence': vata_conf,
            'pitta_confidence': pitta_conf,
            'kapha_confidence': kapha_conf,
            'predicted_severity': severity,
            'confidence_scores': {'vata': vata_conf, 'pitta': pitta_conf, 'kapha': kapha_conf}
        }
    
    def _validate_with_rules(self, ml_pred, user_data):
        """Ayurvedic rule-based validation and correction"""
        validated = ml_pred.copy()
        
        # Rule 1: Mental + Sleep must dominate if severe
        if user_data.get('stress') == 'high' and user_data.get('sleep') in ['poor', 'very_poor']:
            # Boost Vata if not already dominant
            if validated['vata_confidence'] < 0.50:
                validated['vata_confidence'] = min(0.55, validated['vata_confidence'] + 0.15)
        
        # Rule 2: Physical signs validation
        if user_data.get('skin') == 'dry' and user_data.get('temperature') == 'cold':
            # Strong Vata indicator
            if validated['vata_confidence'] < validated['pitta_confidence']:
                validated['vata_confidence'], validated['pitta_confidence'] = \
                    validated['pitta_confidence'], validated['vata_confidence']
        
        # Rule 3: Digestion priority check
        if user_data.get('digestion') in ['constipation', 'acidity', 'slow']:
            dosha_map = {'constipation': 'vata', 'acidity': 'pitta', 'slow': 'kapha'}
            target_dosha = dosha_map[user_data.get('digestion')]
            
            # Ensure digestion-related dosha has reasonable confidence
            if validated[f'{target_dosha}_confidence'] < 0.35:
                validated[f'{target_dosha}_confidence'] = 0.40
        
        # Renormalize
        total = sum([validated['vata_confidence'], validated['pitta_confidence'], validated['kapha_confidence']])
        validated['vata_confidence'] /= total
        validated['pitta_confidence'] /= total
        validated['kapha_confidence'] /= total
        
        return validated
    
    def _decide_dosha_dominance(self, prediction):
        """Decide single vs dual dosha dominance"""
        scores = [
            ('vata', prediction['vata_confidence']),
            ('pitta', prediction['pitta_confidence']),
            ('kapha', prediction['kapha_confidence'])
        ]
        scores.sort(key=lambda x: x[1], reverse=True)
        
        first_dosha, first_conf = scores[0]
        second_dosha, second_conf = scores[1]
        
        # Dual dosha if difference ≤ 7%
        if abs(first_conf - second_conf) <= self.DUAL_DOSHA_THRESHOLD:
            return {
                'type': 'dual',
                'primary': first_dosha,
                'secondary': second_dosha,
                'display_name': f"{first_dosha.capitalize()}-{second_dosha.capitalize()}",
                'confidence': (first_conf + second_conf) / 2,
                'scores': {'vata': prediction['vata_confidence'], 
                          'pitta': prediction['pitta_confidence'],
                          'kapha': prediction['kapha_confidence']}
            }
        
        # Single dominant if confidence ≥ 45%
        elif first_conf >= self.CONFIDENCE_THRESHOLD:
            return {
                'type': 'single',
                'primary': first_dosha,
                'secondary': None,
                'display_name': first_dosha.capitalize(),
                'confidence': first_conf,
                'scores': {'vata': prediction['vata_confidence'],
                          'pitta': prediction['pitta_confidence'],
                          'kapha': prediction['kapha_confidence']}
            }
        
        # Balanced state
        else:
            return {
                'type': 'balanced',
                'primary': 'balanced',
                'secondary': None,
                'display_name': 'Balanced (Sama Dosha)',
                'confidence': 1.0 - first_conf,
                'scores': {'vata': prediction['vata_confidence'],
                          'pitta': prediction['pitta_confidence'],
                          'kapha': prediction['kapha_confidence']}
            }
    
    def _assess_risk(self, prediction, dosha_decision, user_data):
        """Model-driven risk assessment with rule-based correction"""
        severity = prediction['predicted_severity']
        primary_dosha = dosha_decision['primary']
        
        # Count pathology indicators
        pathology_count = 0
        if user_data.get('stress') == 'high': pathology_count += 1
        if user_data.get('sleep') in ['poor', 'very_poor']: pathology_count += 1
        if user_data.get('digestion') in ['constipation', 'acidity', 'slow']: pathology_count += 1
        
        # Kapha-specific rule: require 2+ pathology signs
        if primary_dosha == 'kapha':
            kapha_signs = 0
            if user_data.get('sleep') == 'excessive': kapha_signs += 1
            if user_data.get('digestion') == 'slow': kapha_signs += 1
            if user_data.get('appetite') == 'low': kapha_signs += 1
            
            if kapha_signs < 2:
                # Downgrade risk
                if severity == 'severe':
                    severity = 'moderate'
                elif severity == 'moderate':
                    severity = 'mild'
        
        # Risk mapping
        if dosha_decision['type'] == 'balanced':
            return 'Low'
        
        if severity == 'balanced':
            return 'Low'
        elif severity == 'mild':
            return 'Preventive' if pathology_count == 0 else 'Low'
        elif severity == 'moderate':
            return 'Moderate' if pathology_count >= 2 else 'Low'
        elif severity == 'severe':
            return 'High' if pathology_count >= 2 else 'Moderate'
        
        return 'Low'
    
    def _generate_output(self, dosha_decision, risk_level, user_data):
        """Generate final output"""
        # Convert confidence scores to percentages
        scores = {
            'vata': round(dosha_decision['scores']['vata'] * 100, 1),
            'pitta': round(dosha_decision['scores']['pitta'] * 100, 1),
            'kapha': round(dosha_decision['scores']['kapha'] * 100, 1)
        }
        
        # Determine imbalance level
        max_score = max(scores.values())
        if dosha_decision['type'] == 'balanced':
            imbalance_level = 'balanced'
        elif max_score < 50:
            imbalance_level = 'mild'
        elif max_score < 65:
            imbalance_level = 'moderate'
        else:
            imbalance_level = 'severe'
        
        return {
            'scores': scores,
            'dominant': dosha_decision['display_name'],
            'is_dual': dosha_decision['type'] == 'dual',
            'risk': risk_level,
            'imbalance_level': imbalance_level,
            'confidence': round(dosha_decision['confidence'] * 100, 1),
            'recommendations': self._get_recommendations(dosha_decision, imbalance_level),
            'description': self._get_description(dosha_decision, imbalance_level)
        }
    
    def _get_description(self, dosha_decision, imbalance_level):
        """Generate description"""
        base = {
            'vata': 'Vata governs movement, creativity, and nervous system.',
            'pitta': 'Pitta governs metabolism, digestion, and transformation.',
            'kapha': 'Kapha governs structure, stability, and immunity.',
            'balanced': 'All three doshas are in harmony.'
        }
        
        level_desc = {
            'balanced': 'Maintain your healthy lifestyle (Sama Dosha).',
            'mild': 'Mild imbalance detected. Simple adjustments recommended.',
            'moderate': 'Moderate imbalance (Prakopa). Follow recommendations.',
            'severe': 'Significant imbalance (Vriddhi). Prioritize lifestyle changes.'
        }
        
        primary = dosha_decision['primary']
        return f"{base.get(primary, base['balanced'])} {level_desc[imbalance_level]}"
    
    def _get_recommendations(self, dosha_decision, imbalance_level):
        """Generate recommendations"""
        recs = {
            'vata': [
                'Diet: Warm, cooked foods; ghee, nuts, sweet fruits',
                'Yoga: Gentle poses - Child pose, Cat-Cow',
                'Pranayama: Nadi Shodhana 10 min daily',
                'Lifestyle: Regular sleep 10 PM-6 AM, oil massage',
                'Herbs: Ashwagandha, Brahmi',
                'Avoid: Cold foods, irregular routines'
            ],
            'pitta': [
                'Diet: Cool, fresh foods; cucumber, coconut water',
                'Yoga: Cooling poses - Forward bends, Shavasana',
                'Pranayama: Sheetali (cooling breath) 10 min',
                'Lifestyle: Avoid midday sun, meditation',
                'Herbs: Amla, Neem, Aloe vera',
                'Avoid: Spicy foods, competitive activities'
            ],
            'kapha': [
                'Diet: Light, warm, spicy foods; ginger, turmeric',
                'Yoga: Energizing poses - Sun salutation, Warrior',
                'Pranayama: Kapalabhati, Bhastrika',
                'Lifestyle: Wake early 6 AM, vigorous exercise',
                'Herbs: Trikatu, Guggulu',
                'Avoid: Dairy, sweets, oversleeping'
            ]
        }
        
        primary = dosha_decision['primary']
        if primary == 'balanced':
            return ['Continue balanced lifestyle', 'Maintain regular routines', 'Practice preventive care']
        
        result = recs.get(primary, recs['vata'])[:6]
        
        if dosha_decision['type'] == 'dual' and dosha_decision['secondary']:
            result.append(f"Also balance {dosha_decision['secondary'].capitalize()}: {recs[dosha_decision['secondary']][0]}")
        
        return result
