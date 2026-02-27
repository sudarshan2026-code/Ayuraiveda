class ClinicalTridoshaEngine:
    """20-Parameter Clinical Diagnostic Engine - Classical Ayurveda"""
    
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
        prakriti = self._assess_prakriti(data)
        agni_state = self._assess_agni(data)
        ama_status = self._assess_ama(data)
        
        # DIGESTIVE & ELIMINATION (Weight: 2x)
        vata += data.get('mala', 0) * 2
        vata += data.get('mutra_frequency', 0) * 1.5
        vata += data.get('tongue_coating', 0) if data.get('tongue_coating', 0) == 2 else 0
        pitta += 2 if data.get('appetite') == 'excessive' else 0
        pitta += 3 if data.get('digestion') == 'acidity' else 0
        kapha += data.get('tongue_coating', 0) if data.get('tongue_coating', 0) >= 1 else 0
        kapha += data.get('bloating', 0) * 1.5
        
        # PHYSICAL OBSERVATION (Weight: 1x)
        vata += 4 if data.get('body_structure') == 'lean' else 0
        pitta += 4 if data.get('body_structure') == 'moderate' else 0
        kapha += 4 if data.get('body_structure') == 'heavy' else 0
        
        vata += 3 if data.get('skin') == 'dry' else 0
        pitta += 3 if data.get('skin') == 'sensitive' else 0
        kapha += 3 if data.get('skin') == 'oily' else 0
        
        vata += 3 if data.get('temperature') == 'cold' else 0
        pitta += 3 if data.get('temperature') == 'hot' else 0
        
        kapha += 2 if data.get('sweat') == 'minimal' else 0
        pitta += 2 if data.get('sweat') == 'excessive' else 0
        
        # MENTAL & NERVOUS (Weight: 1.5x)
        vata += stress_score * 1.5
        vata += anxiety_score * 2
        vata += 3 if data.get('sleep') in ['poor', 'very_poor'] else 0
        pitta += 2 if data.get('sleep') == 'disturbed' else 0
        kapha += 2 if data.get('sleep') == 'excessive' else 0
        
        # STRENGTH & ADAPTABILITY
        vata += 2 if data.get('energy') == 'fluctuating' else 0
        kapha += 2 if data.get('energy') == 'heavy' else 0
        vata += 2 if data.get('exercise_tolerance') == 'low' else 0
        kapha += 2 if data.get('exercise_tolerance') == 'low' else 0
        
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
