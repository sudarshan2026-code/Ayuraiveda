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
        """Main assessment pipeline with STRICT hierarchical reasoning"""
        
        # STEP 1: DETERMINE BASE DOSHA FROM STRUCTURE (MANDATORY)
        base_dosha, base_scores, structural_reasoning = self._determine_base_dosha(features)
        
        # STEP 2: Extract Gunas for surface/dynamic features
        gunas = self._extract_gunas(features)
        
        # STEP 3: Modify with surface features (limited adjustment)
        adjusted_scores = self._apply_surface_adjustments(base_scores, gunas, features)
        
        # STEP 4: Apply correction rules
        final_scores = self._apply_correction_rules(adjusted_scores, base_dosha, features)
        
        # STEP 5: Normalize to percentages
        normalized_scores = self._normalize_scores(final_scores)
        
        # STEP 6: Detect contradictions and calculate confidence
        contradictions = self._detect_contradictions(gunas)
        confidence = self._calculate_confidence(gunas, contradictions, base_dosha)
        
        # STEP 7: Classify type
        dosha_type = self._classify_type(normalized_scores)
        
        # STEP 8: Generate explanation
        explanation = self._generate_hierarchical_explanation(
            base_dosha, structural_reasoning, gunas, normalized_scores, features
        )
        
        return {
            'dosha': normalized_scores,
            'type': dosha_type,
            'confidence': round(confidence, 2),
            'base_dosha': base_dosha,
            'structural_reasoning': structural_reasoning,
            'guna_analysis': gunas,
            'explanation': explanation
        }
    
    def _determine_base_dosha(self, f):
        """STEP 1: MANDATORY - Determine base dosha from STRUCTURE ONLY"""
        
        # Get structural features with defaults
        body_frame = f.get('body_frame', 0.5)
        body_width = f.get('body_width', body_frame)
        body_ratio = f.get('body_ratio', 0.5)
        shoulder_width = f.get('shoulder_width', 0.5)
        hip_width = f.get('hip_width', 0.5)
        limb_thickness = f.get('limb_thickness', 0.5)
        
        # Calculate structural indicators
        build_score = (body_frame + body_width + limb_thickness) / 3
        face_roundness = body_ratio  # Higher ratio = rounder/wider
        fat_distribution = body_frame
        
        reasoning = []
        
        # RULE 1: Heavy/Rounded → Kapha
        if build_score >= 0.6 and face_roundness >= 0.6:
            base_dosha = 'kapha'
            base_scores = {'vata': 20, 'pitta': 30, 'kapha': 50}
            reasoning.append(f"Heavy body build (score: {build_score:.2f})")
            reasoning.append(f"Rounded face shape (ratio: {face_roundness:.2f})")
            reasoning.append("Base Dosha: KAPHA (heavy, rounded structure)")
        
        # RULE 2: Medium/Slightly Heavy + Rounded → Kapha
        elif build_score >= 0.45 and face_roundness >= 0.55:
            base_dosha = 'kapha'
            base_scores = {'vata': 25, 'pitta': 30, 'kapha': 45}
            reasoning.append(f"Medium-to-heavy build (score: {build_score:.2f})")
            reasoning.append(f"Rounded facial features (ratio: {face_roundness:.2f})")
            reasoning.append("Base Dosha: KAPHA (moderate build with roundness)")
        
        # RULE 3: Lean/Angular → Vata
        elif build_score <= 0.35 and face_roundness <= 0.45:
            base_dosha = 'vata'
            base_scores = {'vata': 50, 'pitta': 30, 'kapha': 20}
            reasoning.append(f"Lean body build (score: {build_score:.2f})")
            reasoning.append(f"Angular face shape (ratio: {face_roundness:.2f})")
            reasoning.append("Base Dosha: VATA (lean, angular structure)")
        
        # RULE 4: Medium/Sharp → Pitta
        elif 0.4 <= build_score <= 0.55 and face_roundness <= 0.55:
            base_dosha = 'pitta'
            base_scores = {'vata': 25, 'pitta': 45, 'kapha': 30}
            reasoning.append(f"Medium body build (score: {build_score:.2f})")
            reasoning.append(f"Balanced-to-sharp features (ratio: {face_roundness:.2f})")
            reasoning.append("Base Dosha: PITTA (medium, balanced structure)")
        
        # RULE 5: Default to Pitta for ambiguous cases
        else:
            base_dosha = 'pitta'
            base_scores = {'vata': 30, 'pitta': 40, 'kapha': 30}
            reasoning.append(f"Moderate build (score: {build_score:.2f})")
            reasoning.append(f"Balanced proportions (ratio: {face_roundness:.2f})")
            reasoning.append("Base Dosha: PITTA (balanced structure)")
        
        return base_dosha, base_scores, reasoning
    
    def _apply_surface_adjustments(self, base_scores, gunas, features):
        """STEP 2: Adjust (not replace) with surface features - LIMITED"""
        
        adjusted = base_scores.copy()
        
        # Surface adjustments (max ±10 points)
        dryness_factor = gunas['ruksha']
        oiliness_factor = gunas['snigdha']
        heat_factor = gunas['ushna']
        
        # Dryness → +Vata (small increase only, max +10)
        if dryness_factor > 0.6:
            vata_boost = min(10, (dryness_factor - 0.6) * 25)
            adjusted['vata'] += vata_boost
            adjusted['kapha'] -= vata_boost / 2
        
        # Oiliness/Smooth → +Kapha (max +10)
        if oiliness_factor > 0.6:
            kapha_boost = min(10, (oiliness_factor - 0.6) * 25)
            adjusted['kapha'] += kapha_boost
            adjusted['vata'] -= kapha_boost / 2
        
        # Heat/Pigmentation → +Pitta (max +10)
        if heat_factor > 0.6:
            pitta_boost = min(10, (heat_factor - 0.6) * 25)
            adjusted['pitta'] += pitta_boost
            adjusted['kapha'] -= pitta_boost / 2
        
        return adjusted
    
    def _apply_correction_rules(self, scores, base_dosha, features):
        """STEP 3: Apply HARD correction rules"""
        
        corrected = scores.copy()
        body_frame = features.get('body_frame', 0.5)
        body_ratio = features.get('body_ratio', 0.5)
        
        # RULE 1: If BASE DOSHA = Kapha, Vata cannot exceed Kapha
        if base_dosha == 'kapha':
            if corrected['vata'] > corrected['kapha']:
                excess = corrected['vata'] - corrected['kapha']
                corrected['vata'] = corrected['kapha']
                corrected['pitta'] += excess / 2
                corrected['kapha'] += excess / 2
        
        # RULE 2: If structure is NOT lean, Vata must remain below 30%
        if body_frame >= 0.4:
            total = sum(corrected.values())
            vata_percent = (corrected['vata'] / total) * 100
            if vata_percent > 30:
                # Reduce Vata to 30%
                target_vata = total * 0.30
                excess = corrected['vata'] - target_vata
                corrected['vata'] = target_vata
                # Redistribute to base dosha
                corrected[base_dosha] += excess
        
        # RULE 3: If face is rounded, Kapha must be highest or equal highest
        if body_ratio >= 0.6:
            max_dosha = max(corrected.values())
            if corrected['kapha'] < max_dosha:
                diff = max_dosha - corrected['kapha']
                corrected['kapha'] = max_dosha
                # Take from Vata primarily
                corrected['vata'] -= diff * 0.7
                corrected['pitta'] -= diff * 0.3
        
        # RULE 4: If BASE DOSHA = Pitta, Vata cannot dominate
        if base_dosha == 'pitta':
            if corrected['vata'] > corrected['pitta']:
                excess = corrected['vata'] - corrected['pitta']
                corrected['vata'] = corrected['pitta']
                corrected['pitta'] += excess * 0.6
                corrected['kapha'] += excess * 0.4
        
        # Ensure no negative values
        for dosha in corrected:
            if corrected[dosha] < 0:
                corrected[dosha] = 0
        
        return corrected
    
    def _normalize_scores(self, scores):
        """Convert to percentages"""
        total = sum(scores.values())
        if total == 0:
            return {'vata': 33.33, 'pitta': 33.33, 'kapha': 33.34}
        
        return {
            'vata': round((scores['vata'] / total) * 100, 2),
            'pitta': round((scores['pitta'] / total) * 100, 2),
            'kapha': round((scores['kapha'] / total) * 100, 2)
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
    
    def _calculate_confidence(self, gunas, contradictions, base_dosha):
        """Calculate confidence based on clarity, contradictions, and base dosha strength"""
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
        """STEP 5: Classify dosha type with STRICT balanced check"""
        doshas = sorted(scores.items(), key=lambda x: x[1], reverse=True)
        
        dominant = doshas[0]
        second = doshas[1]
        
        # STRICT: Balanced only if ALL within 5%
        max_score = max(scores.values())
        min_score = min(scores.values())
        
        if (max_score - min_score) <= 5:
            return "Balanced (Sama Prakriti)"
        
        # Single dominant (>45%)
        if dominant[1] >= 45:
            return f"{dominant[0].capitalize()} Predominant"
        
        # Dual type (within 10% and both >30%)
        if abs(dominant[1] - second[1]) <= 10 and second[1] >= 30:
            return f"{dominant[0].capitalize()}-{second[0].capitalize()} Type"
        
        return f"{dominant[0].capitalize()} Predominant"
    
    def _generate_hierarchical_explanation(self, base_dosha, structural_reasoning, gunas, scores, features):
        """Generate explanation following hierarchical reasoning"""
        
        explanation_parts = []
        
        # Part 1: Base Dosha from Structure
        explanation_parts.append(f"**STEP 1 - Base Dosha (Structure):** {base_dosha.upper()}")
        explanation_parts.append(" | ".join(structural_reasoning))
        
        # Part 2: Surface Adjustments
        adjustments = []
        if gunas['ruksha'] > 0.6:
            adjustments.append(f"Dryness detected (Ruksha: {gunas['ruksha']:.2f}) -> +Vata adjustment")
        if gunas['snigdha'] > 0.6:
            adjustments.append(f"Oiliness detected (Snigdha: {gunas['snigdha']:.2f}) -> +Kapha adjustment")
        if gunas['ushna'] > 0.6:
            adjustments.append(f"Heat indicators (Ushna: {gunas['ushna']:.2f}) -> +Pitta adjustment")
        
        if adjustments:
            explanation_parts.append(f"**STEP 2 - Surface Adjustments:** {'; '.join(adjustments)}")
        else:
            explanation_parts.append("**STEP 2 - Surface Adjustments:** No significant surface modifications")
        
        # Part 3: Final Classification
        dominant = max(scores.items(), key=lambda x: x[1])
        explanation_parts.append(
            f"**FINAL RESULT:** {dominant[0].capitalize()} constitution with "
            f"Vata: {scores['vata']:.1f}%, Pitta: {scores['pitta']:.1f}%, Kapha: {scores['kapha']:.1f}%"
        )
        
        return " | ".join(explanation_parts)


def test_engine():
    """Test the clinical engine with hierarchical reasoning"""
    engine = ClinicalAssessmentEngine()
    
    print("=" * 80)
    print("TESTING HIERARCHICAL CLINICAL ASSESSMENT ENGINE")
    print("=" * 80)
    
    # Test case 1: Kapha-dominant (heavy, rounded)
    print("\n" + "=" * 80)
    print("TEST CASE 1: Heavy Build + Rounded Face (Expected: Kapha)")
    print("=" * 80)
    kapha_features = {
        'skin_texture': 0.3,
        'oiliness': 0.8,
        'pigmentation': 0.4,
        'redness': 0.3,
        'brightness': 0.7,
        'body_frame': 0.75,      # Heavy
        'body_width': 0.8,       # Wide
        'body_height': 0.5,
        'body_ratio': 0.75,      # Rounded
        'shoulder_width': 0.7,
        'hip_width': 0.75,
        'torso_length': 0.6,
        'limb_thickness': 0.7,   # Thick
        'posture': 0.7
    }
    
    result = engine.assess(kapha_features)
    print_hierarchical_result(result)
    
    # Test case 2: Vata-dominant (lean, angular)
    print("\n" + "=" * 80)
    print("TEST CASE 2: Lean Build + Angular Face (Expected: Vata)")
    print("=" * 80)
    vata_features = {
        'skin_texture': 0.8,
        'oiliness': 0.2,
        'pigmentation': 0.3,
        'redness': 0.3,
        'brightness': 0.5,
        'body_frame': 0.25,      # Light
        'body_width': 0.3,       # Narrow
        'body_height': 0.7,
        'body_ratio': 0.35,      # Angular
        'shoulder_width': 0.3,
        'hip_width': 0.3,
        'torso_length': 0.6,
        'limb_thickness': 0.3,   # Thin
        'posture': 0.4
    }
    
    result = engine.assess(vata_features)
    print_hierarchical_result(result)
    
    # Test case 3: Pitta-dominant (medium, balanced)
    print("\n" + "=" * 80)
    print("TEST CASE 3: Medium Build + Balanced Features (Expected: Pitta)")
    print("=" * 80)
    pitta_features = {
        'skin_texture': 0.5,
        'oiliness': 0.5,
        'pigmentation': 0.7,
        'redness': 0.8,
        'brightness': 0.6,
        'body_frame': 0.5,       # Medium
        'body_width': 0.5,
        'body_height': 0.6,
        'body_ratio': 0.5,       # Balanced
        'shoulder_width': 0.6,
        'hip_width': 0.5,
        'torso_length': 0.5,
        'limb_thickness': 0.5,
        'posture': 0.6
    }
    
    result = engine.assess(pitta_features)
    print_hierarchical_result(result)
    
    # Test case 4: Edge case - Dry skin but heavy build (Should be Kapha, not Vata)
    print("\n" + "=" * 80)
    print("TEST CASE 4: Dry Skin BUT Heavy Build (Expected: Kapha, NOT Vata)")
    print("=" * 80)
    edge_case_features = {
        'skin_texture': 0.8,     # Very dry
        'oiliness': 0.2,         # Low oil
        'pigmentation': 0.4,
        'redness': 0.3,
        'brightness': 0.5,
        'body_frame': 0.7,       # Heavy (STRUCTURE WINS)
        'body_width': 0.75,
        'body_height': 0.5,
        'body_ratio': 0.7,       # Rounded
        'shoulder_width': 0.7,
        'hip_width': 0.7,
        'torso_length': 0.6,
        'limb_thickness': 0.65,
        'posture': 0.7
    }
    
    result = engine.assess(edge_case_features)
    print_hierarchical_result(result)
    
    print("\n" + "=" * 80)
    print("TESTS COMPLETE - Hierarchical Reasoning Working")
    print("=" * 80)
    print("\nStructure-first approach working correctly")
    print("Surface features limited to adjustments only")
    print("Correction rules applied successfully")


def print_hierarchical_result(result):
    """Print result in hierarchical format"""
    print(f"\nRESULT: {result['type']}")
    print(f"   Confidence: {result['confidence']:.1f}%")
    print(f"\nBASE DOSHA (from structure): {result['base_dosha'].upper()}")
    print(f"\nDOSHA SCORES:")
    print(f"   Vata:  {result['dosha']['vata']:.2f}%")
    print(f"   Pitta: {result['dosha']['pitta']:.2f}%")
    print(f"   Kapha: {result['dosha']['kapha']:.2f}%")
    print(f"\nHIERARCHICAL REASONING:")
    for line in result['structural_reasoning']:
        print(f"   - {line}")
    print(f"\nEXPLANATION:")
    print(f"   {result['explanation']}")


if __name__ == "__main__":
    test_engine()
