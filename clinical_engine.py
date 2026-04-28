"""
Clinical Assessment Engine for AyurAI Veda™
Implements: Lakshana (Features) → Guna (Qualities) → Dosha (Assessment)
"""

import math

class ClinicalAssessmentEngine:
    
    def __init__(self):
        self.guna_weights = {
            'vata': {'ruksha': 0.3, 'laghu': 0.3, 'chala': 0.2, 'sukshma': 0.2},
            'pitta': {'ushna': 0.4, 'tikshna': 0.3, 'drava': 0.2, 'sara': 0.1},
            'kapha': {'guru': 0.4, 'snigdha': 0.3, 'mridu': 0.2, 'sthira': 0.1}
        }
        
        # Body-focused weights (no face required)
        self.region_weights = {
            'body': 0.50,        # Body structure is primary
            'skin': 0.30,        # Skin characteristics
            'proportions': 0.15, # Body proportions
            'overall': 0.05      # Overall appearance
        }
    
    def assess(self, features):
        """Main assessment pipeline"""
        gunas = self._extract_gunas(features)
        dosha_scores = self._compute_dosha_scores(gunas)
        regional_scores = self._compute_regional_scores(features)
        final_scores = self._combine_regional_scores(regional_scores)
        
        contradictions = self._detect_contradictions(gunas)
        confidence = self._calculate_confidence(gunas, contradictions)
        dosha_type = self._classify_type(final_scores)
        explanation = self._generate_explanation(gunas, final_scores, features)
        
        return {
            'dosha': final_scores,
            'type': dosha_type,
            'confidence': round(confidence, 2),
            'guna_analysis': gunas,
            'explanation': explanation
        }
    
    def _extract_gunas(self, f):
        """Layer 1: Feature → Guna mapping (Body-focused)"""
        
        # Get features with defaults
        skin_texture = f.get('skin_texture', 0.5)
        oiliness = f.get('oiliness', 0.5)
        pigmentation = f.get('pigmentation', 0.5)
        redness = f.get('redness', 0.5)
        brightness = f.get('brightness', 0.5)
        body_frame = f.get('body_frame', 0.5)
        body_width = f.get('body_width', body_frame)
        body_height = f.get('body_height', 0.5)
        body_ratio = f.get('body_ratio', 0.5)
        shoulder_width = f.get('shoulder_width', 0.5)
        hip_width = f.get('hip_width', 0.5)
        torso_length = f.get('torso_length', 0.5)
        limb_thickness = f.get('limb_thickness', 0.5)
        posture = f.get('posture', 0.5)
        
        # Ruksha (Dry/Rough) - from skin and body leanness
        ruksha = (1 - oiliness) * 0.4 + skin_texture * 0.3 + (1 - body_frame) * 0.3
        
        # Snigdha (Unctuous/Oily) - from skin and body fullness
        snigdha = oiliness * 0.5 + body_frame * 0.3 + brightness * 0.2
        
        # Ushna (Heat) - from skin tone and pigmentation
        ushna = redness * 0.5 + pigmentation * 0.3 + (1 - brightness) * 0.2
        
        # Tikshna (Sharp) - from angular body structure
        tikshna = (1 - body_frame) * 0.4 + (1 - limb_thickness) * 0.3 + body_ratio * 0.3
        
        # Mridu (Soft) - from rounded body structure
        mridu = body_frame * 0.4 + (1 - skin_texture) * 0.3 + limb_thickness * 0.3
        
        # Guru (Heavy) - from body mass and structure
        guru = body_frame * 0.5 + body_width * 0.3 + limb_thickness * 0.2
        
        # Laghu (Light) - opposite of heavy
        laghu = (1 - body_frame) * 0.5 + (1 - body_width) * 0.3 + body_height * 0.2
        
        # Sthira (Stable) - from body stability and structure
        sthira = body_frame * 0.4 + posture * 0.3 + shoulder_width * 0.3
        
        # Chala (Mobile/Variable) - from body lightness
        chala = (1 - body_frame) * 0.5 + (1 - posture) * 0.3 + (1 - limb_thickness) * 0.2
        
        # Sukshma (Subtle) - from delicate structure
        sukshma = (1 - body_frame) * 0.4 + (1 - limb_thickness) * 0.3 + skin_texture * 0.3
        
        # Drava (Liquid/Flowing) - from skin and body softness
        drava = oiliness * 0.5 + (1 - body_ratio) * 0.3 + brightness * 0.2
        
        # Sara (Flowing/Mobile) - from body fluidity
        sara = oiliness * 0.4 + (1 - skin_texture) * 0.3 + (1 - body_frame) * 0.3
        
        return {
            'ruksha': ruksha,
            'snigdha': snigdha,
            'ushna': ushna,
            'tikshna': tikshna,
            'mridu': mridu,
            'guru': guru,
            'laghu': laghu,
            'sthira': sthira,
            'chala': chala,
            'sukshma': sukshma,
            'drava': drava,
            'sara': sara
        }
    
    def _compute_dosha_scores(self, gunas):
        """Layer 2: Guna → Dosha scoring"""
        vata = (gunas['ruksha'] * 0.3 + gunas['laghu'] * 0.3 + 
                gunas['chala'] * 0.2 + gunas['sukshma'] * 0.2)
        
        pitta = (gunas['ushna'] * 0.4 + gunas['tikshna'] * 0.3 + 
                 gunas['drava'] * 0.2 + gunas['sara'] * 0.1)
        
        kapha = (gunas['guru'] * 0.4 + gunas['snigdha'] * 0.3 + 
                 gunas['mridu'] * 0.2 + gunas['sthira'] * 0.1)
        
        total = vata + pitta + kapha
        
        return {
            'vata': round((vata / total) * 100, 2),
            'pitta': round((pitta / total) * 100, 2),
            'kapha': round((kapha / total) * 100, 2)
        }
    
    def _compute_regional_scores(self, f):
        """Layer 4: Region-based analysis (Body-focused)"""
        
        # Get features with defaults
        skin_texture = f.get('skin_texture', 0.5)
        oiliness = f.get('oiliness', 0.5)
        redness = f.get('redness', 0.5)
        pigmentation = f.get('pigmentation', 0.5)
        brightness = f.get('brightness', 0.5)
        body_frame = f.get('body_frame', 0.5)
        body_width = f.get('body_width', body_frame)
        shoulder_width = f.get('shoulder_width', 0.5)
        hip_width = f.get('hip_width', 0.5)
        limb_thickness = f.get('limb_thickness', 0.5)
        
        # Skin region (30%)
        skin_gunas = {
            'ruksha': (1 - oiliness) * 0.5 + skin_texture * 0.5,
            'snigdha': oiliness,
            'ushna': redness * 0.7 + pigmentation * 0.3,
            'mridu': (1 - skin_texture)
        }
        skin_vata = skin_gunas['ruksha'] * 0.6 + (1 - skin_gunas['snigdha']) * 0.4
        skin_pitta = skin_gunas['ushna']
        skin_kapha = skin_gunas['snigdha'] * 0.6 + skin_gunas['mridu'] * 0.4
        
        # Body structure (50%) - PRIMARY INDICATOR
        body_vata = (1 - body_frame) * 0.4 + (1 - limb_thickness) * 0.3 + (1 - body_width) * 0.3
        body_pitta = 0.5  # Neutral for body structure
        body_kapha = body_frame * 0.4 + limb_thickness * 0.3 + body_width * 0.3
        
        # Proportions (15%)
        prop_vata = (1 - shoulder_width) * 0.5 + (1 - hip_width) * 0.5
        prop_pitta = (shoulder_width + hip_width) / 2
        prop_kapha = shoulder_width * 0.5 + hip_width * 0.5
        
        # Overall appearance (5%)
        overall_vata = skin_texture * 0.5 + (1 - body_frame) * 0.5
        overall_pitta = pigmentation * 0.5 + redness * 0.5
        overall_kapha = brightness * 0.5 + body_frame * 0.5
        
        return {
            'skin': {'vata': skin_vata, 'pitta': skin_pitta, 'kapha': skin_kapha},
            'body': {'vata': body_vata, 'pitta': body_pitta, 'kapha': body_kapha},
            'proportions': {'vata': prop_vata, 'pitta': prop_pitta, 'kapha': prop_kapha},
            'overall': {'vata': overall_vata, 'pitta': overall_pitta, 'kapha': overall_kapha}
        }
    
    def _combine_regional_scores(self, regional):
        """Combine regional scores with weights (Body-focused)"""
        # Updated weights: Body is primary indicator
        weights = {
            'body': 0.50,        # Body structure is most important
            'skin': 0.30,        # Skin characteristics
            'proportions': 0.15, # Body proportions
            'overall': 0.05      # Overall appearance
        }
        
        vata = (regional['body']['vata'] * weights['body'] +
                regional['skin']['vata'] * weights['skin'] +
                regional['proportions']['vata'] * weights['proportions'] +
                regional['overall']['vata'] * weights['overall'])
        
        pitta = (regional['body']['pitta'] * weights['body'] +
                 regional['skin']['pitta'] * weights['skin'] +
                 regional['proportions']['pitta'] * weights['proportions'] +
                 regional['overall']['pitta'] * weights['overall'])
        
        kapha = (regional['body']['kapha'] * weights['body'] +
                 regional['skin']['kapha'] * weights['skin'] +
                 regional['proportions']['kapha'] * weights['proportions'] +
                 regional['overall']['kapha'] * weights['overall'])
        
        total = vata + pitta + kapha
        
        return {
            'vata': round((vata / total) * 100, 2),
            'pitta': round((pitta / total) * 100, 2),
            'kapha': round((kapha / total) * 100, 2)
        }
    
    def _detect_contradictions(self, gunas):
        """Layer 3: Detect opposing Gunas"""
        contradictions = []
        
        if abs(gunas['ruksha'] - gunas['snigdha']) < 0.2:
            contradictions.append(('ruksha', 'snigdha'))
        
        if abs(gunas['laghu'] - gunas['guru']) < 0.2:
            contradictions.append(('laghu', 'guru'))
        
        if abs(gunas['chala'] - gunas['sthira']) < 0.2:
            contradictions.append(('chala', 'sthira'))
        
        return contradictions
    
    def _calculate_confidence(self, gunas, contradictions):
        """Calculate confidence based on clarity and contradictions"""
        base_confidence = 85
        
        # Reduce for contradictions
        contradiction_penalty = len(contradictions) * 10
        
        # Check feature clarity (variance in gunas)
        guna_values = list(gunas.values())
        variance = sum((x - 0.5) ** 2 for x in guna_values) / len(guna_values)
        clarity_bonus = variance * 20
        
        confidence = base_confidence - contradiction_penalty + clarity_bonus
        return max(50, min(95, confidence))
    
    def _classify_type(self, scores):
        """Layer 3: Classify dosha type"""
        doshas = sorted(scores.items(), key=lambda x: x[1], reverse=True)
        
        dominant = doshas[0]
        second = doshas[1]
        
        # Balanced
        if max(scores.values()) - min(scores.values()) < 15:
            return "Balanced (Sama Prakriti)"
        
        # Single dominant
        if dominant[1] > 60:
            return f"{dominant[0].capitalize()} Dominant"
        
        # Dual type
        if dominant[1] - second[1] < 10:
            return f"{dominant[0].capitalize()}-{second[0].capitalize()} Type"
        
        return f"{dominant[0].capitalize()} Predominant"
    
    def _generate_explanation(self, gunas, scores, features):
        """Layer 5: Generate clinical explanation"""
        dominant = max(scores.items(), key=lambda x: x[1])
        dosha_name = dominant[0].capitalize()
        
        explanations = []
        
        # Vata explanation
        if dominant[0] == 'vata':
            if gunas['ruksha'] > 0.6:
                explanations.append(f"pronounced dryness (Ruksha: {gunas['ruksha']:.2f})")
            if gunas['laghu'] > 0.6:
                explanations.append(f"light body structure (Laghu: {gunas['laghu']:.2f})")
            if gunas['chala'] > 0.6:
                explanations.append(f"mobile body type (Chala: {gunas['chala']:.2f})")
            if features.get('body_frame', 0.5) < 0.4:
                explanations.append(f"thin body frame")
        
        # Pitta explanation
        elif dominant[0] == 'pitta':
            if gunas['ushna'] > 0.6:
                explanations.append(f"heat indicators (Ushna: {gunas['ushna']:.2f})")
            if gunas['tikshna'] > 0.6:
                explanations.append(f"angular body structure (Tikshna: {gunas['tikshna']:.2f})")
            if features.get('redness', 0.5) > 0.5:
                explanations.append(f"increased redness")
            if features.get('pigmentation', 0.5) > 0.5:
                explanations.append(f"prominent pigmentation")
        
        # Kapha explanation
        elif dominant[0] == 'kapha':
            if gunas['guru'] > 0.6:
                explanations.append(f"heavy build (Guru: {gunas['guru']:.2f})")
            if gunas['snigdha'] > 0.6:
                explanations.append(f"oily skin (Snigdha: {gunas['snigdha']:.2f})")
            if gunas['mridu'] > 0.6:
                explanations.append(f"soft, rounded body (Mridu: {gunas['mridu']:.2f})")
            if features.get('body_frame', 0.5) > 0.6:
                explanations.append(f"robust body frame")
        
        if not explanations:
            explanations.append("balanced guna distribution")
        
        return f"{dosha_name} constitution observed due to {', '.join(explanations)}."


def test_engine():
    """Test the clinical engine"""
    engine = ClinicalAssessmentEngine()
    
    # Test case: Vata-dominant (thin, light body)
    test_features = {
        'skin_texture': 0.7,
        'oiliness': 0.2,
        'pigmentation': 0.3,
        'redness': 0.3,
        'brightness': 0.5,
        'body_frame': 0.25,      # Light build
        'body_width': 0.3,       # Narrow
        'body_height': 0.7,      # Tall
        'body_ratio': 0.4,       # Thin ratio
        'shoulder_width': 0.3,   # Narrow shoulders
        'hip_width': 0.3,        # Narrow hips
        'torso_length': 0.6,
        'limb_thickness': 0.3,   # Thin limbs
        'posture': 0.4
    }
    
    result = engine.assess(test_features)
    
    print("=== Clinical Assessment Result (Body-Based) ===")
    print(f"Type: {result['type']}")
    print(f"Confidence: {result['confidence']}%")
    print(f"\nDosha Scores:")
    print(f"  Vata: {result['dosha']['vata']}%")
    print(f"  Pitta: {result['dosha']['pitta']}%")
    print(f"  Kapha: {result['dosha']['kapha']}%")
    print(f"\nExplanation: {result['explanation']}")
    print(f"\nKey Gunas:")
    for guna, value in sorted(result['guna_analysis'].items(), key=lambda x: x[1], reverse=True)[:5]:
        print(f"  {guna}: {value:.2f}")
    print(f"\n✅ No face detection required - Full body analysis only")


if __name__ == "__main__":
    test_engine()
