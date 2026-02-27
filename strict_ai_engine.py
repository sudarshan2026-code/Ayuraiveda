"""
Strictly Validated Tridosha Intelligence Engine™
Classical Ayurvedic principles with zero contradictions
"""

class StrictTridoshaEngine:
    def __init__(self):
        self.dosha_scores = {'vata': 0, 'pitta': 0, 'kapha': 0}
        
        # Classical symptom-dosha mapping
        self.SYMPTOM_MAP = {
            'vata': ['anxiety', 'insomnia', 'constipation', 'gas', 'dry_skin', 'irregular_appetite'],
            'pitta': ['acidity', 'inflammation', 'anger', 'sensitive_skin', 'excessive_heat'],
            'kapha': ['lethargy', 'weight_gain', 'congestion', 'slow_digestion', 'excessive_sleep']
        }
    
    def analyze(self, user_data):
        """Strict analysis following classical Ayurveda"""
        
        # Step 1: Detect symptoms
        symptoms = self._detect_symptoms(user_data)
        
        # Step 2: Calculate dosha scores
        self._calculate_scores(user_data)
        
        # Step 3: Determine if Sama Dosha (STRICT RULES)
        is_sama = self._check_sama_dosha(symptoms)
        
        # Step 4: Determine dominant dosha
        dominant_info = self._determine_dominant(is_sama)
        
        # Step 5: Determine dosha state (Sama/Prakopa)
        dosha_state = self._determine_state(is_sama, dominant_info)
        
        # Step 6: Assign risk level (STRICT CONSISTENCY)
        risk_level = self._assign_risk(is_sama, dominant_info, symptoms)
        
        # Step 7: Map disease risks
        disease_risks = self._map_disease_risks(dominant_info, symptoms, risk_level)
        
        # Step 8: Final strict validation
        result = self._strict_validation(dominant_info, dosha_state, risk_level, disease_risks, is_sama)
        
        return result
    
    def _detect_symptoms(self, data):
        """Detect present symptoms"""
        symptoms = []
        
        # Vata symptoms
        if data.get('stress') in ['moderate', 'high']:
            symptoms.append('anxiety')
        if data.get('sleep') in ['poor', 'very_poor']:
            symptoms.append('insomnia')
        if data.get('digestion') == 'constipation':
            symptoms.append('constipation')
        if data.get('digestion') == 'gas':
            symptoms.append('gas')
        if data.get('skin') == 'dry':
            symptoms.append('dry_skin')
        if data.get('appetite') == 'irregular':
            symptoms.append('irregular_appetite')
        
        # Pitta symptoms
        if data.get('digestion') == 'acidity':
            symptoms.append('acidity')
        if data.get('skin') == 'sensitive':
            symptoms.append('sensitive_skin')
        if data.get('temperature') == 'hot':
            symptoms.append('excessive_heat')
        
        # Kapha symptoms
        if data.get('sleep') == 'excessive':
            symptoms.append('excessive_sleep')
        if data.get('digestion') == 'slow':
            symptoms.append('slow_digestion')
        if data.get('appetite') == 'low':
            symptoms.append('lethargy')
        
        return symptoms
    
    def _calculate_scores(self, data):
        """Calculate dosha scores"""
        self.dosha_scores = {'vata': 0, 'pitta': 0, 'kapha': 0}
        
        # Stress + Sleep (weight: 8)
        if data.get('stress') == 'high':
            self.dosha_scores['vata'] += 8
        elif data.get('stress') == 'moderate':
            self.dosha_scores['vata'] += 4
        
        if data.get('sleep') in ['poor', 'very_poor']:
            self.dosha_scores['vata'] += 7
        elif data.get('sleep') == 'excessive':
            self.dosha_scores['kapha'] += 6
        
        # Digestion (weight: 6)
        if data.get('digestion') == 'constipation':
            self.dosha_scores['vata'] += 6
        elif data.get('digestion') == 'acidity':
            self.dosha_scores['pitta'] += 6
        elif data.get('digestion') == 'slow':
            self.dosha_scores['kapha'] += 5
        elif data.get('digestion') == 'gas':
            self.dosha_scores['vata'] += 4
        
        # Physical signs (weight: 4)
        if data.get('skin') == 'dry':
            self.dosha_scores['vata'] += 4
        elif data.get('skin') == 'oily':
            self.dosha_scores['kapha'] += 3
        elif data.get('skin') == 'sensitive':
            self.dosha_scores['pitta'] += 4
        
        if data.get('temperature') == 'cold':
            self.dosha_scores['vata'] += 3
        elif data.get('temperature') == 'hot':
            self.dosha_scores['pitta'] += 4
        
        # Appetite (weight: 3)
        if data.get('appetite') == 'irregular':
            self.dosha_scores['vata'] += 3
        elif data.get('appetite') == 'excessive':
            self.dosha_scores['pitta'] += 2
        elif data.get('appetite') == 'low':
            self.dosha_scores['kapha'] += 2
        
        # Food (weight: 2)
        if data.get('food') == 'spicy':
            self.dosha_scores['pitta'] += 2
        elif data.get('food') == 'sweet':
            self.dosha_scores['kapha'] += 2
    
    def _check_sama_dosha(self, symptoms):
        """STRICT: Sama Dosha only when NO symptoms"""
        if symptoms:
            return False  # Any symptom disables Sama
        
        # Check score range (must be within ±10%)
        total = sum(self.dosha_scores.values()) or 1
        percentages = {k: (v/total)*100 for k, v in self.dosha_scores.items()}
        score_range = max(percentages.values()) - min(percentages.values())
        
        return score_range <= 10
    
    def _determine_dominant(self, is_sama):
        """Determine dominant dosha"""
        total = sum(self.dosha_scores.values()) or 1
        percentages = {
            'vata': round((self.dosha_scores['vata'] / total) * 100, 1),
            'pitta': round((self.dosha_scores['pitta'] / total) * 100, 1),
            'kapha': round((self.dosha_scores['kapha'] / total) * 100, 1)
        }
        
        if is_sama:
            return {
                'type': 'sama',
                'primary': 'balanced',
                'display_name': 'Balanced (Sama Dosha)',
                'scores': percentages,
                'max_score': max(percentages.values())
            }
        
        max_dosha = max(percentages, key=percentages.get)
        max_score = percentages[max_dosha]
        
        # RULE: If score ≥ 45%, declare dominant
        if max_score >= 45:
            return {
                'type': 'dominant',
                'primary': max_dosha,
                'display_name': max_dosha.capitalize(),
                'scores': percentages,
                'max_score': max_score
            }
        
        # Dual dosha check
        sorted_doshas = sorted(percentages.items(), key=lambda x: x[1], reverse=True)
        if abs(sorted_doshas[0][1] - sorted_doshas[1][1]) <= 7:
            return {
                'type': 'dual',
                'primary': sorted_doshas[0][0],
                'secondary': sorted_doshas[1][0],
                'display_name': f"{sorted_doshas[0][0].capitalize()}-{sorted_doshas[1][0].capitalize()}",
                'scores': percentages,
                'max_score': sorted_doshas[0][1]
            }
        
        return {
            'type': 'dominant',
            'primary': max_dosha,
            'display_name': max_dosha.capitalize(),
            'scores': percentages,
            'max_score': max_score
        }
    
    def _determine_state(self, is_sama, dominant_info):
        """Determine dosha state (Sama/Prakopa)"""
        if is_sama:
            return 'Sama'  # Balanced
        
        max_score = dominant_info['max_score']
        
        if max_score >= 70:
            return 'Prakopa'  # Severe aggravation
        elif max_score >= 50:
            return 'Prakopa'  # Moderate aggravation
        else:
            return 'Sanchaya'  # Mild accumulation
    
    def _assign_risk(self, is_sama, dominant_info, symptoms):
        """STRICT: Assign risk level"""
        
        # RULE 1: Sama Dosha → LOW risk ONLY
        if is_sama:
            return 'Low'
        
        # RULE 2: Any symptom → at least MODERATE
        if symptoms:
            symptom_count = len(symptoms)
            max_score = dominant_info['max_score']
            
            # RULE 4: Dominant ≥ 70% → never LOW
            if max_score >= 70:
                return 'High' if symptom_count >= 3 else 'Moderate'
            elif max_score >= 50:
                return 'Moderate' if symptom_count >= 2 else 'Moderate'
            else:
                return 'Moderate'
        
        # No symptoms but imbalance detected
        return 'Preventive'
    
    def _map_disease_risks(self, dominant_info, symptoms, risk_level):
        """Map disease risks based on dosha-symptom alignment"""
        
        # RULE 6: Primary Risk only when MODERATE or HIGH
        if risk_level not in ['Moderate', 'High']:
            return []
        
        risks = []
        primary_dosha = dominant_info['primary']
        
        # RULE 5: Dosha-symptom mapping
        if primary_dosha == 'vata':
            if 'anxiety' in symptoms or 'insomnia' in symptoms:
                risks.append('Anxiety/Insomnia (Vata Vikruti)')
            if 'constipation' in symptoms:
                risks.append('Constipation (Vata Vikruti)')
            if 'gas' in symptoms:
                risks.append('Bloating/Gas (Vata Vikruti)')
        
        elif primary_dosha == 'pitta':
            if 'acidity' in symptoms:
                risks.append('Acidity/GERD (Pitta Vikruti)')
            if 'sensitive_skin' in symptoms:
                risks.append('Skin inflammation (Pitta Vikruti)')
            if 'excessive_heat' in symptoms:
                risks.append('Heat-related issues (Pitta Vikruti)')
        
        elif primary_dosha == 'kapha':
            if 'excessive_sleep' in symptoms and 'slow_digestion' in symptoms:
                risks.append('Metabolic sluggishness (Kapha Vikruti)')
            if 'lethargy' in symptoms:
                risks.append('Lethargy/Low energy (Kapha Vikruti)')
        
        return risks
    
    def _strict_validation(self, dominant_info, dosha_state, risk_level, disease_risks, is_sama):
        """Final strict validation - eliminate ALL contradictions"""
        
        # VALIDATION 1: Sama Dosha + Disease Risk (FORBIDDEN)
        if is_sama and disease_risks:
            is_sama = False
            dosha_state = 'Sanchaya'
            risk_level = 'Moderate'
        
        # VALIDATION 2: Sama Dosha + Risk != Low (FORBIDDEN)
        if is_sama and risk_level != 'Low':
            risk_level = 'Low'
            disease_risks = []
        
        # VALIDATION 3: Low Risk + Disease (FORBIDDEN)
        if risk_level == 'Low' and disease_risks:
            risk_level = 'Moderate'
        
        # VALIDATION 4: Dominant ≥ 70% + Low Risk (FORBIDDEN)
        if dominant_info['max_score'] >= 70 and risk_level == 'Low':
            risk_level = 'Moderate'
        
        return {
            'scores': dominant_info['scores'],
            'dominant': dominant_info['display_name'],
            'is_dual': dominant_info['type'] == 'dual',
            'dosha_state': dosha_state,
            'risk': risk_level,
            'disease_risks': disease_risks,
            'is_sama_dosha': is_sama,
            'imbalance_level': 'balanced' if is_sama else ('severe' if dominant_info['max_score'] >= 70 else ('moderate' if dominant_info['max_score'] >= 50 else 'mild')),
            'recommendations': self._get_recommendations(dominant_info, is_sama, disease_risks),
            'description': self._get_description(dominant_info, dosha_state, is_sama, disease_risks)
        }
    
    def _get_description(self, dominant_info, dosha_state, is_sama, disease_risks):
        """Generate description"""
        if is_sama:
            return "All three doshas are in harmony (Sama Dosha). No imbalance detected. Continue your healthy lifestyle with preventive care."
        
        base = {
            'vata': 'Vata dosha governs movement, creativity, and nervous system.',
            'pitta': 'Pitta dosha governs metabolism, digestion, and transformation.',
            'kapha': 'Kapha dosha governs structure, stability, and immunity.'
        }
        
        state_desc = {
            'Sanchaya': 'Mild accumulation stage detected. Early intervention recommended.',
            'Prakopa': 'Aggravation stage detected. Follow recommendations to restore balance.'
        }
        
        primary = dominant_info['primary']
        desc = base.get(primary, '')
        
        if disease_risks:
            desc += f" Detected imbalances: {', '.join(disease_risks)}. "
        
        desc += state_desc.get(dosha_state, '')
        
        return desc
    
    def _get_recommendations(self, dominant_info, is_sama, disease_risks):
        """Generate recommendations"""
        if is_sama:
            return [
                'Continue balanced lifestyle and regular routines',
                'Practice preventive care with seasonal adjustments',
                'Maintain healthy diet, sleep, and stress management',
                'Regular yoga and pranayama for wellness'
            ]
        
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
        
        primary = dominant_info['primary']
        recommendations = recs.get(primary, recs['vata'])[:6]
        
        # Add disease-specific priority recommendations
        if disease_risks:
            for risk in disease_risks:
                if 'Acidity' in risk:
                    recommendations.insert(0, '⚠️ PRIORITY: Avoid spicy, fried, acidic foods; eat small frequent meals')
                elif 'Anxiety' in risk or 'Insomnia' in risk:
                    recommendations.insert(0, '⚠️ PRIORITY: Establish regular sleep routine; practice relaxation')
                elif 'Constipation' in risk:
                    recommendations.insert(0, '⚠️ PRIORITY: Increase fiber, warm water; abdominal massage')
                elif 'Metabolic' in risk:
                    recommendations.insert(0, '⚠️ PRIORITY: Increase physical activity; reduce heavy foods')
        
        return recommendations[:8]
