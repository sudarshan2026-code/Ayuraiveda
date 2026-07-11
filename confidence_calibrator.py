"""
Confidence Calibration System
Interprets model scores correctly before assigning body types
"""

class ConfidenceCalibrator:
    """Calibrates confidence scores to prevent over-confident misclassifications"""
    
    def __init__(self):
        self.thresholds = {
            'uncertain': 0.3,
            'moderate': 0.6
        }
    
    def calibrate(self, features):
        """
        Calibrate feature scores and assign confidence levels
        
        Args:
            features: Dictionary of normalized features (0-1)
            
        Returns:
            Dictionary with calibrated classifications and confidence levels
        """
        calibrated = features.copy()
        
        # RULE 1: Score Interpretation
        body_confidence = self._interpret_score(features.get('body_frame', 0.5))
        face_confidence = self._interpret_score(features.get('face_ratio', 0.5)) if 'face_ratio' in features else None
        
        # RULE 2: Body Type Decision
        body_type = self._decide_body_type(
            features.get('body_ratio', 0.5),
            features.get('body_frame', 0.5),
            features.get('limb_thickness', 0.5),
            body_confidence
        )
        
        # RULE 3: Face Shape Decision
        face_shape = None
        if 'face_ratio' in features or 'face_shape' in features:
            face_shape = self._decide_face_shape(
                features.get('face_ratio', 0.5),
                face_confidence
            )
        
        # RULE 4: Safety Override
        if body_confidence == 'uncertain' and (face_confidence == 'uncertain' or face_confidence is None):
            vata_eligible = False
            base_dosha = 'kapha-pitta'
        else:
            vata_eligible = (body_type == 'lean' and (face_shape == 'angular' if face_shape else True))
            base_dosha = 'vata' if vata_eligible else 'kapha-pitta'
        
        # Add calibrated results
        calibrated['body_type'] = body_type
        calibrated['body_confidence'] = body_confidence
        calibrated['face_shape'] = face_shape
        calibrated['face_confidence'] = face_confidence
        calibrated['vata_eligible'] = vata_eligible
        calibrated['base_dosha'] = base_dosha
        
        return calibrated
    
    def _interpret_score(self, score):
        """
        Interpret a score as uncertain, moderate, or strong
        
        RULE 1: SCORE INTERPRETATION
        - score < 0.3: uncertain
        - score 0.3-0.6: moderate
        - score > 0.6: strong
        """
        if score < self.thresholds['uncertain']:
            return 'uncertain'
        elif score < self.thresholds['moderate']:
            return 'moderate'
        else:
            return 'strong'
    
    def _decide_body_type(self, body_ratio, body_frame, limb_thickness, confidence):
        """
        Decide body type based on features and confidence
        
        RULE 2: BODY TYPE DECISION
        - uncertain: default to "medium"
        - moderate: classify as "medium"
        - strong: decide lean/heavy based on scores
        """
        if confidence == 'uncertain':
            return 'medium'
        
        if confidence == 'moderate':
            return 'medium'
        
        # Strong confidence - make actual classification
        avg_score = (body_ratio + body_frame + limb_thickness) / 3
        
        if avg_score < 0.35:
            return 'lean'
        elif avg_score > 0.55:
            return 'heavy'
        else:
            return 'medium'
    
    def _decide_face_shape(self, face_ratio, confidence):
        """
        Decide face shape based on ratio and confidence
        
        RULE 3: FACE SHAPE
        - angular_score < 0.3: classify as "oval"
        - otherwise: use actual classification
        """
        if confidence == 'uncertain' or face_ratio < self.thresholds['uncertain']:
            return 'oval'
        
        # Angular faces have lower width/height ratio
        if face_ratio < 0.75:
            return 'angular'
        elif face_ratio > 0.9:
            return 'round'
        else:
            return 'oval'
    
    def get_calibration_report(self, features, calibrated):
        """Generate a human-readable calibration report"""
        report = []
        
        report.append("=== CONFIDENCE CALIBRATION REPORT ===")
        report.append("")
        
        # Body analysis
        body_frame = features.get('body_frame', 0.5)
        report.append(f"Body Frame Score: {body_frame:.3f}")
        report.append(f"Body Confidence: {calibrated['body_confidence']}")
        report.append(f"Body Type: {calibrated['body_type']}")
        
        if calibrated['body_confidence'] == 'uncertain':
            report.append("  -> Score < 0.3: Defaulted to 'medium' (RULE 2)")
        elif calibrated['body_confidence'] == 'moderate':
            report.append("  -> Score 0.3-0.6: Classified as 'medium' (RULE 2)")
        
        report.append("")
        
        # Face analysis (if present)
        if calibrated['face_shape']:
            face_ratio = features.get('face_ratio', 0.5)
            report.append(f"Face Ratio Score: {face_ratio:.3f}")
            report.append(f"Face Confidence: {calibrated['face_confidence']}")
            report.append(f"Face Shape: {calibrated['face_shape']}")
            
            if calibrated['face_confidence'] == 'uncertain':
                report.append("  -> Score < 0.3: Defaulted to 'oval' (RULE 3)")
        
        report.append("")
        
        # Safety override
        if calibrated['body_confidence'] == 'uncertain' and (
            calibrated['face_confidence'] == 'uncertain' or calibrated['face_confidence'] is None
        ):
            report.append("SAFETY OVERRIDE APPLIED (RULE 4):")
            report.append("  -> Both body AND face uncertain")
            report.append("  -> Base Dosha: Kapha-Pitta (NOT Vata)")
        
        report.append("")
        report.append(f"Vata Eligible: {calibrated['vata_eligible']}")
        report.append(f"Base Dosha: {calibrated['base_dosha']}")
        report.append("")
        report.append("=" * 40)
        
        return "\n".join(report)


def test_calibrator():
    """Test the confidence calibration system"""
    calibrator = ConfidenceCalibrator()
    
    print("=" * 60)
    print("CONFIDENCE CALIBRATION SYSTEM TEST")
    print("=" * 60)
    
    # Test Case 1: Uncertain body score
    print("\n[TEST 1] Uncertain body score (< 0.3)")
    test1 = {
        'body_ratio': 0.25,
        'body_frame': 0.28,
        'limb_thickness': 0.22,
        'shoulder_width': 0.25
    }
    result1 = calibrator.calibrate(test1)
    print(calibrator.get_calibration_report(test1, result1))
    assert result1['body_type'] == 'medium', "Should default to medium"
    assert result1['body_confidence'] == 'uncertain', "Should be uncertain"
    print("[PASSED]")
    
    # Test Case 2: Moderate body score
    print("\n[TEST 2] Moderate body score (0.3-0.6)")
    test2 = {
        'body_ratio': 0.45,
        'body_frame': 0.50,
        'limb_thickness': 0.48,
        'shoulder_width': 0.47
    }
    result2 = calibrator.calibrate(test2)
    print(calibrator.get_calibration_report(test2, result2))
    assert result2['body_type'] == 'medium', "Should classify as medium"
    assert result2['body_confidence'] == 'moderate', "Should be moderate"
    print("[PASSED]")
    
    # Test Case 3: Strong lean score
    print("\n[TEST 3] Strong lean score (> 0.6)")
    test3 = {
        'body_ratio': 0.30,
        'body_frame': 0.65,
        'limb_thickness': 0.32,
        'shoulder_width': 0.35
    }
    result3 = calibrator.calibrate(test3)
    print(calibrator.get_calibration_report(test3, result3))
    assert result3['body_confidence'] == 'strong', "Should be strong"
    print("[PASSED]")
    
    # Test Case 4: Uncertain face score
    print("\n[TEST 4] Uncertain face score (< 0.3)")
    test4 = {
        'body_ratio': 0.70,
        'body_frame': 0.75,
        'limb_thickness': 0.72,
        'face_ratio': 0.25
    }
    result4 = calibrator.calibrate(test4)
    print(calibrator.get_calibration_report(test4, result4))
    assert result4['face_shape'] == 'oval', "Should default to oval"
    print("[PASSED]")
    
    # Test Case 5: Safety override (both uncertain)
    print("\n[TEST 5] Safety override - both body and face uncertain")
    test5 = {
        'body_ratio': 0.25,
        'body_frame': 0.28,
        'limb_thickness': 0.22,
        'face_ratio': 0.25
    }
    result5 = calibrator.calibrate(test5)
    print(calibrator.get_calibration_report(test5, result5))
    assert result5['vata_eligible'] == False, "Should not be Vata eligible"
    assert result5['base_dosha'] == 'kapha-pitta', "Should default to Kapha-Pitta"
    print("[PASSED]")
    
    print("\n" + "=" * 60)
    print("ALL TESTS PASSED")
    print("Confidence Calibration System is working correctly!")
    print("=" * 60)


if __name__ == '__main__':
    test_calibrator()
