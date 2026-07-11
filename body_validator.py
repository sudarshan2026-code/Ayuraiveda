class BodyStructureValidator:
    """Pre-processing validation for structural misclassification correction"""
    
    def validate_and_correct(self, detected_data):
        """Correct structural misclassifications before dosha calculation"""
        corrected = detected_data.copy()
        
        # STEP 1: Body Build Validation
        # Map continuous features to categorical body build
        body_ratio = detected_data.get('body_ratio', 0.5)
        body_frame = detected_data.get('body_frame', 0.5)
        limb_thickness = detected_data.get('limb_thickness', 0.5)
        shoulder_width = detected_data.get('shoulder_width', 0.5)
        hip_width = detected_data.get('hip_width', 0.5)
        
        # Determine initial body build from features
        # Lean: low ratio, low frame, thin limbs
        # Medium: moderate values
        # Heavy: high ratio, high frame, thick limbs
        if body_ratio < 0.35 and body_frame < 0.4 and limb_thickness < 0.4:
            body_build = 'lean'
        elif body_ratio > 0.5 or body_frame > 0.6 or limb_thickness > 0.6:
            body_build = 'heavy'
        else:
            body_build = 'medium'
        
        # Check for misclassification
        if body_build == 'lean':
            # Check if arms/limbs are NOT thin AND torso is NOT narrow
            if limb_thickness >= 0.4 or shoulder_width >= 0.5:
                corrected['body_build'] = 'medium'
                body_build = 'medium'
            # Check if fat present (high oiliness or low texture)
            elif detected_data.get('oiliness', 0.5) > 0.6:
                corrected['body_build'] = 'medium-heavy'
                body_build = 'medium-heavy'
            else:
                corrected['body_build'] = 'lean'
        else:
            corrected['body_build'] = body_build
        
        # STEP 2: Face Shape Validation (if face data present)
        face_shape = detected_data.get('face_shape', None)
        if face_shape:
            jaw_sharpness = detected_data.get('jaw_sharpness', 'moderate')
            cheek_fullness = detected_data.get('cheek_fullness', 'moderate')
            
            if face_shape == 'angular':
                # Check if cheeks are filled OR jaw is not sharp
                if cheek_fullness in ['full', 'very_full'] or jaw_sharpness in ['soft', 'moderate']:
                    corrected['face_shape'] = 'oval'
                    face_shape = 'oval'
        
        # STEP 3 & 4: Apply Vata Safety Rule and Structure Lock
        corrected['vata_eligible'] = (
            body_build == 'lean' and 
            (face_shape == 'angular' if face_shape else True)
        )
        
        if body_build in ['medium', 'medium-heavy', 'heavy']:
            corrected['base_dosha'] = 'kapha-pitta'
        else:
            corrected['base_dosha'] = 'vata'
        
        return corrected
