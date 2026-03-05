class ClinicalTridoshaEngine:
    """20-Parameter Clinical Diagnostic Engine - Classical Ayurveda"""
    
    def __init__(self):
        # Try to initialize ML model API client
        try:
            from model_api_client import ModelAPIClient
            self.ml_client = ModelAPIClient()
            print("✓ ML Model API client initialized")
        except:
            self.ml_client = None
            print("⚠ ML Model API not available, using rule-based only")
    
    def analyze(self, data):
        # Initialize scores
        vata = pitta = kapha = 0
        
        # Convert numeric strings to integers
        for key in ['mala', 'mutra_frequency', 'tongue_coating', 'bloating']:
            if key in data and isinstance(data[key], str):
                data[key] = int(data[key]) if data[key].isdigit() else 0
        
        # Map text values to numeric scores
        stress_map = {'low': 0, 'moderate': 1, 'high': 2}
        anxiety_map = {'none': 0, 'moderate': 1, 'high': 2}
        
        stress_score = stress_map.get(data.get('stress', 'low'), 0)
        anxiety_score = anxiety_map.get(data.get('anxiety', 'none'), 0)
        
        # FOUNDATION LAYER
        agni_state = self._assess_agni(data)
        ama_status = self._assess_ama(data)
        
        # 1-10: Personal Info
        age = int(data.get('age', 25))
        if age < 18: kapha += 2
        elif age > 50: vata += 3
        elif 18 <= age <= 50: pitta += 2
        if data.get('gender') == 'male': pitta += 1
        elif data.get('gender') == 'female': kapha += 1
        
        # 11-12: Body Measurements
        bmi = float(data.get('bmi', 22))
        if bmi < 18.5: vata += 4
        elif 18.5 <= bmi < 25: pitta += 2
        elif bmi >= 25: kapha += 4
        
        # 13-15: Body Structure
        if data.get('body_frame') == 'thin': vata += 4
        elif data.get('body_frame') == 'medium': pitta += 3
        elif data.get('body_frame') == 'heavy': kapha += 4
        if data.get('body_build') == 'lean': vata += 3
        elif data.get('body_build') == 'muscular': pitta += 3
        elif data.get('body_build') == 'stocky': kapha += 3
        if data.get('muscle_tone') == 'low': vata += 2
        elif data.get('muscle_tone') == 'medium': pitta += 2
        elif data.get('muscle_tone') == 'high': kapha += 2
        
        # 16-19: Physical Characteristics
        if data.get('weight_tendency') == 'hard_to_gain': vata += 4
        elif data.get('weight_tendency') == 'stable': pitta += 2
        elif data.get('weight_tendency') == 'easy_to_gain': kapha += 4
        if data.get('joints') == 'prominent': vata += 3
        elif data.get('joints') == 'normal': pitta += 1
        elif data.get('joints') == 'well_covered': kapha += 2
        if data.get('veins') == 'prominent': vata += 2
        elif data.get('veins') == 'visible': pitta += 1
        elif data.get('veins') == 'hidden': kapha += 2
        if data.get('bone_structure') == 'light': vata += 3
        elif data.get('bone_structure') == 'medium': pitta += 2
        elif data.get('bone_structure') == 'heavy': kapha += 3
        
        # 20-24: Skin
        if data.get('skin_type') == 'dry': vata += 4
        elif data.get('skin_type') == 'sensitive': pitta += 4
        elif data.get('skin_type') == 'oily': kapha += 4
        if data.get('skin_texture') == 'rough': vata += 3
        elif data.get('skin_texture') == 'soft': pitta += 2
        elif data.get('skin_texture') == 'smooth': kapha += 3
        if data.get('skin_temperature') == 'cold': vata += 3; kapha += 1
        elif data.get('skin_temperature') == 'warm': pitta += 4
        if data.get('complexion') == 'dark': vata += 2
        elif data.get('complexion') == 'fair': pitta += 2
        elif data.get('complexion') == 'pale': kapha += 2
        if data.get('skin_luster') == 'dull': vata += 2
        elif data.get('skin_luster') == 'radiant': pitta += 2
        elif data.get('skin_luster') == 'glowing': kapha += 2
        
        # 25-27: Hair & Nails
        if data.get('hair_type') == 'dry': vata += 3
        elif data.get('hair_type') == 'thin': pitta += 3
        elif data.get('hair_type') == 'thick': kapha += 3
        if data.get('hair_texture') == 'rough': vata += 2
        elif data.get('hair_texture') == 'fine': pitta += 2
        elif data.get('hair_texture') == 'smooth': kapha += 2
        if data.get('nails') == 'brittle': vata += 2
        elif data.get('nails') == 'soft': pitta += 2
        elif data.get('nails') == 'strong': kapha += 2
        
        # 28-33: Appetite & Digestion
        if data.get('appetite') == 'irregular': vata += 4
        elif data.get('appetite') == 'strong': pitta += 4
        elif data.get('appetite') == 'low': kapha += 3
        if data.get('hunger') == 'variable': vata += 3
        elif data.get('hunger') == 'intense': pitta += 3
        elif data.get('hunger') == 'mild': kapha += 2
        if data.get('thirst') == 'variable': vata += 2
        elif data.get('thirst') == 'high': pitta += 3
        elif data.get('thirst') == 'low': kapha += 2
        if data.get('digestion') == 'irregular': vata += 4
        elif data.get('digestion') == 'fast': pitta += 4
        elif data.get('digestion') == 'slow': kapha += 4
        if data.get('bowel') == 'constipation': vata += 5
        elif data.get('bowel') == 'loose': pitta += 4
        elif data.get('bowel') == 'heavy': kapha += 3
        if data.get('gas') == 'frequent': vata += 3
        
        # 34-35: Food & Metabolism
        if data.get('food_preference') == 'warm': vata += 2
        elif data.get('food_preference') == 'cold': pitta += 2
        elif data.get('food_preference') == 'spicy': kapha += 2
        if data.get('metabolism') == 'fast': vata += 2; pitta += 2
        elif data.get('metabolism') == 'slow': kapha += 3
        
        # 36-42: Lifestyle & Physiology
        if data.get('sleep_pattern') == 'light': vata += 4
        elif data.get('sleep_pattern') == 'moderate': pitta += 2
        elif data.get('sleep_pattern') == 'deep': kapha += 4
        if data.get('sleep_duration') == 'less_6': vata += 3; pitta += 2
        elif data.get('sleep_duration') == 'more_8': kapha += 3
        if data.get('dreams') == 'active': vata += 3
        elif data.get('dreams') == 'colorful': pitta += 2
        elif data.get('dreams') == 'few': kapha += 2
        if data.get('energy_level') == 'variable': vata += 3
        elif data.get('energy_level') == 'moderate': pitta += 2
        elif data.get('energy_level') == 'steady': kapha += 3
        if data.get('stamina') == 'low': vata += 3
        elif data.get('stamina') == 'medium': pitta += 2
        elif data.get('stamina') == 'high': kapha += 3
        if data.get('physical_activity') == 'restless': vata += 4
        elif data.get('physical_activity') == 'moderate': pitta += 2
        elif data.get('physical_activity') == 'slow': kapha += 3
        if data.get('exercise_tolerance') == 'low': vata += 2
        elif data.get('exercise_tolerance') == 'high': pitta += 3
        
        # 43-44: Body Response
        if data.get('sweat') == 'minimal': vata += 3
        elif data.get('sweat') == 'profuse': pitta += 4
        elif data.get('sweat') == 'moderate': kapha += 2
        if data.get('body_odor') == 'strong': pitta += 2
        
        # 45-46: Climate
        if data.get('weather_preference') == 'warm': vata += 3; kapha += 2
        elif data.get('weather_preference') == 'cool': pitta += 3
        if data.get('season_discomfort') == 'winter': vata += 2
        elif data.get('season_discomfort') == 'summer': pitta += 3
        elif data.get('season_discomfort') == 'spring': kapha += 2
        
        # 47-48: General Health
        if data.get('immunity') == 'weak': vata += 3
        elif data.get('immunity') == 'moderate': pitta += 2
        elif data.get('immunity') == 'strong': kapha += 3
        if data.get('disease_tendency') == 'nervous': vata += 4
        elif data.get('disease_tendency') == 'inflammatory': pitta += 4
        elif data.get('disease_tendency') == 'congestion': kapha += 4
        
        # 49-51: Speech
        if data.get('speech_pace') == 'fast': vata += 3
        elif data.get('speech_pace') == 'moderate': pitta += 2
        elif data.get('speech_pace') == 'slow': kapha += 3
        if data.get('voice_quality') == 'weak': vata += 2
        elif data.get('voice_quality') == 'sharp': pitta += 2
        elif data.get('voice_quality') == 'deep': kapha += 2
        if data.get('communication') == 'talkative': vata += 2
        elif data.get('communication') == 'precise': pitta += 2
        elif data.get('communication') == 'reserved': kapha += 2
        
        # 52: Movements
        if data.get('movements') == 'quick': vata += 3
        elif data.get('movements') == 'purposeful': pitta += 2
        elif data.get('movements') == 'slow': kapha += 3
        
        # 53: Mental State
        if data.get('mental_state') == 'anxious': vata += 5
        elif data.get('mental_state') == 'focused': pitta += 3
        elif data.get('mental_state') == 'calm': kapha += 3
        
        # 54-57: Memory & Mind
        if data.get('memory') == 'quick_forget': vata += 3
        elif data.get('memory') == 'sharp': pitta += 3
        elif data.get('memory') == 'slow_retain': kapha += 3
        if data.get('learning') == 'quick': vata += 2; pitta += 2
        elif data.get('learning') == 'slow': kapha += 2
        if data.get('concentration') == 'poor': vata += 3
        elif data.get('concentration') == 'good': pitta += 3
        elif data.get('concentration') == 'excellent': kapha += 2
        if data.get('decision_making') == 'quick': vata += 2
        elif data.get('decision_making') == 'analytical': pitta += 3
        elif data.get('decision_making') == 'slow': kapha += 2
        
        # 58-59: Behavior
        if data.get('emotional_response') == 'fearful': vata += 4
        elif data.get('emotional_response') == 'angry': pitta += 4
        elif data.get('emotional_response') == 'attached': kapha += 3
        if data.get('stress_response') == 'anxious': vata += 4
        elif data.get('stress_response') == 'irritable': pitta += 3
        elif data.get('stress_response') == 'withdrawn': kapha += 3
        
        # 54-59: Additional Characteristics
        if data.get('teeth_gums') == 'weak': vata += 2
        elif data.get('teeth_gums') == 'strong': kapha += 2
        
        if data.get('eyes_appearance') == 'small': vata += 2
        elif data.get('eyes_appearance') == 'medium': pitta += 2
        elif data.get('eyes_appearance') == 'large': kapha += 2
        
        if data.get('lips_condition') == 'dry': vata += 2
        elif data.get('lips_condition') == 'moist': kapha += 2
        
        if data.get('temp_regulation') == 'poor': vata += 2
        elif data.get('temp_regulation') == 'good': pitta += 1
        
        if data.get('pain_tolerance') == 'low': vata += 2
        elif data.get('pain_tolerance') == 'high': kapha += 2
        
        if data.get('healing_speed') == 'slow': vata += 2; kapha += 1
        elif data.get('healing_speed') == 'fast': pitta += 2
        
        # Agni modifier (±10%)
        agni_modifier = {'sama': 1.0, 'vishama': 1.1, 'tikshna': 0.95, 'manda': 1.15}
        vata *= agni_modifier.get(agni_state, 1.0)
        
        # Calculate percentages
        total = vata + pitta + kapha
        if total == 0:
            return self._sama_dosha_output()
        
        vata_pct = round((vata / total) * 100)
        pitta_pct = round((pitta / total) * 100)
        kapha_pct = round((kapha / total) * 100)
        
        # Determine dominant dosha
        scores = {'Vata': vata_pct, 'Pitta': pitta_pct, 'Kapha': kapha_pct}
        dominant = max(scores, key=scores.get)
        dominant_score = scores[dominant]
        
        # STRICT DIAGNOSTIC RULES
        
        # Rule 1: Sama Dosha Check
        has_symptoms = self._check_symptoms(data)
        is_balanced = abs(vata_pct - pitta_pct) <= 10 and abs(pitta_pct - kapha_pct) <= 10
        
        if not has_symptoms and agni_state == 'sama' and ama_status == 'absent' and is_balanced:
            return self._sama_dosha_output()
        
        # Rule 2: Dosha State Classification
        if dominant_score >= 65:
            dosha_state = "Severe Prakopa"
        elif dominant_score >= 45:
            dosha_state = "Prakopa"
        else:
            dosha_state = "Mild Imbalance"
        
        # Rule 3: Risk Level Calculation
        risk_level, primary_risk = self._calculate_risk(data, dominant, dominant_score, agni_state, ama_status)
        
        # Rule 4: Contradiction Prevention
        if risk_level == 'Low' and primary_risk:
            risk_level = 'Moderate'
        
        # Generate recommendations
        recommendations = self._generate_recommendations(dominant, agni_state, ama_status, data)
        
        # Clinical justification
        justification = self._generate_justification(dominant, dosha_state, agni_state, ama_status, primary_risk)
        
        return {
            'dominant': dominant,
            'dosha_state': dosha_state,
            'agni_state': agni_state.title(),
            'ama_status': ama_status.title(),
            'risk': risk_level,
            'primary_risk': primary_risk,
            'scores': {'vata': vata_pct, 'pitta': pitta_pct, 'kapha': kapha_pct},
            'recommendations': recommendations,
            'justification': justification
        }
    
    def _assess_agni(self, data):
        """Assess digestive fire type"""
        appetite = data.get('appetite', 'regular')
        digestion = data.get('digestion', 'normal')
        
        if appetite == 'irregular' or digestion == 'gas':
            return 'vishama'  # Vata-type
        elif appetite == 'excessive' or digestion == 'acidity':
            return 'tikshna'  # Pitta-type
        elif appetite == 'low' or digestion == 'slow':
            return 'manda'  # Kapha-type
        return 'sama'  # Balanced
    
    def _assess_ama(self, data):
        """Assess toxin presence"""
        tongue_coating = data.get('tongue_coating', 0)
        bloating = data.get('bloating', 0)
        fatigue = data.get('energy') == 'heavy'
        
        if tongue_coating > 2 or bloating > 2 or fatigue:
            return 'present'
        return 'absent'
    
    def _assess_prakriti(self, data):
        """Assess constitutional baseline"""
        body = data.get('body_structure', 'moderate')
        return {'lean': 'Vata', 'moderate': 'Pitta', 'heavy': 'Kapha'}.get(body, 'Balanced')
    
    def _check_symptoms(self, data):
        """Check if any active symptoms present"""
        symptom_keys = ['stress', 'anxiety', 'acidity', 'bloating', 'mala', 'sleep']
        return any(data.get(key) in ['high', 'poor', 'very_poor', 'constipation', 'acidity'] for key in symptom_keys)
    
    def _calculate_risk(self, data, dominant, score, agni, ama):
        """Calculate risk level and primary risk"""
        symptom_count = sum([
            data.get('stress') == 'high',
            data.get('anxiety') == 'high',
            data.get('sleep') in ['poor', 'very_poor'],
            data.get('digestion') in ['acidity', 'constipation', 'gas'],
            ama == 'present',
            agni in ['vishama', 'manda']
        ])
        
        # Disease mapping
        primary_risk = None
        if score >= 45:
            if dominant == 'Vata':
                if data.get('anxiety') == 'high':
                    primary_risk = "Anxiety Disorders"
                elif data.get('sleep') in ['poor', 'very_poor']:
                    primary_risk = "Insomnia"
                elif data.get('digestion') == 'constipation':
                    primary_risk = "Chronic Constipation"
                else:
                    primary_risk = "Nervous System Imbalance"
            
            elif dominant == 'Pitta':
                if data.get('digestion') == 'acidity':
                    primary_risk = "Acid Reflux / GERD"
                elif data.get('skin') == 'sensitive':
                    primary_risk = "Inflammatory Skin Conditions"
                elif data.get('stress') == 'high':
                    primary_risk = "Stress-Induced Inflammation"
                else:
                    primary_risk = "Metabolic Imbalance"
            
            elif dominant == 'Kapha':
                if data.get('body_structure') == 'heavy':
                    primary_risk = "Obesity / Weight Gain"
                elif data.get('energy') == 'heavy':
                    primary_risk = "Chronic Fatigue"
                elif data.get('digestion') == 'slow':
                    primary_risk = "Slow Metabolism"
                else:
                    primary_risk = "Congestion Disorders"
        
        # Risk level
        if symptom_count == 0 and ama == 'absent' and agni == 'sama':
            return 'Low', None
        elif symptom_count >= 3 or (ama == 'present' and agni in ['vishama', 'manda']):
            return 'High', primary_risk
        else:
            return 'Moderate', primary_risk
    
    def _sama_dosha_output(self):
        """Output for balanced state"""
        return {
            'dominant': 'Balanced (Sama Dosha)',
            'dosha_state': 'Sama',
            'agni_state': 'Sama',
            'ama_status': 'Absent',
            'risk': 'Low',
            'primary_risk': None,
            'scores': {'vata': 33, 'pitta': 33, 'kapha': 34},
            'recommendations': [
                'Maintain current healthy lifestyle',
                'Continue balanced diet and regular routine',
                'Practice preventive yoga and pranayama',
                'Follow seasonal routines (Ritucharya)'
            ],
            'justification': 'All parameters indicate balanced Tridosha state with no active symptoms, balanced Agni, and absence of Ama. Continue preventive practices.'
        }
    
    def _generate_recommendations(self, dominant, agni, ama, data):
        """Generate clinical recommendations"""
        recs = []
        
        if ama == 'present':
            recs.append('Detoxification: Warm water with ginger, avoid heavy foods')
        
        if agni == 'manda':
            recs.append('Strengthen Agni: Ginger tea, digestive spices (cumin, fennel)')
        elif agni == 'tikshna':
            recs.append('Cool Agni: Avoid spicy foods, eat cooling herbs (coriander, fennel)')
        
        if dominant == 'Vata':
            recs.extend([
                'Warm, cooked, oily foods (ghee, sesame oil)',
                'Regular routine and adequate rest',
                'Grounding yoga poses and oil massage (Abhyanga)'
            ])
        elif dominant == 'Pitta':
            recs.extend([
                'Cooling foods (cucumber, coconut, mint)',
                'Avoid spicy, fried, acidic foods',
                'Meditation and cooling pranayama (Sheetali)'
            ])
        elif dominant == 'Kapha':
            recs.extend([
                'Light, warm, spicy foods',
                'Regular vigorous exercise',
                'Avoid dairy, sweets, and heavy foods'
            ])
        
        return recs[:5]
    
    def _generate_justification(self, dominant, state, agni, ama, risk):
        """Generate clinical justification"""
        return f"Clinical Assessment: {dominant} {state} detected with {agni} Agni and {ama} Ama. " + \
               (f"Primary risk identified: {risk}. " if risk else "No immediate disease risk. ") + \
               "Recommendations follow classical Ayurvedic protocols for dosha pacification and Agni restoration."
