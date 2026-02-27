"""
Corrected Tridosha Intelligence Engine™
Eliminates contradictions between dosha state and disease risk
"""

class CorrectedTridoshaEngine:
    def __init__(self):
        self.dosha_scores = {'vata': 0, 'pitta': 0, 'kapha': 0}
        self.disease_risks = []
        
    def analyze(self, user_data):
        """Main analysis with strict consistency logic"""
        
        # Step 1: Detect disease risks (HIGHEST PRIORITY)
        disease_risks = self._detect_disease_risks(user_data)
        
        # Step 2: Calculate dosha scores
        self._calculate_dosha_scores(user_data)
        
        # Step 3: Determine dominant dosha (disease-aligned)
        dominant_dosha = self._determine_dominant_dosha(disease_risks)
        
        # Step 4: Determine dosha state (Sama vs Imbalanced)
        dosha_state = self._determine_dosha_state(disease_risks)
        
        # Step 5: Assign risk level (consistent with state)
        risk_level = self._assign_risk_level(dosha_state, disease_risks)
        
        # Step 6: Final validation check
        result = self._validate_consistency(dominant_dosha, dosha_state, risk_level, disease_risks)
        
        # Step 7: Generate recommendations
        result['recommendations'] = self._get_recommendations(result)
        result['description'] = self._get_description(result)
        
        return result
    
    def _detect_disease_risks(self, data):
        """Detect primary disease risks (highest priority)"""
        risks = []
        
        # Pitta-related diseases
        if data.get('digestion') == 'acidity':
            risks.append({'dosha': 'pitta', 'condition': 'Acidity/GERD', 'severity': 'moderate'})
        
        # Vata-related diseases
        if data.get('stress') == 'high' or data.get('sleep') in ['poor', 'very_poor']:
            risks.append({'dosha': 'vata', 'condition': 'Anxiety/Insomnia', 'severity': 'moderate'})
        
        if data.get('digestion') == 'constipation':
            risks.append({'dosha': 'vata', 'condition': 'Constipation', 'severity': 'mild'})
        
        # Kapha-related diseases (requires 2+ indicators)
        kapha_indicators = 0
        if data.get('sleep') == 'excessive': kapha_indicators += 1
        if data.get('digestion') == 'slow': kapha_indicators += 1
        if data.get('appetite') == 'low': kapha_indicators += 1
        
        if kapha_indicators >= 2:
            risks.append({'dosha': 'kapha', 'condition': 'Metabolic sluggishness', 'severity': 'moderate'})
        
        return risks
    
    def _calculate_dosha_scores(self, data):
        """Calculate dosha scores"""
        self.dosha_scores = {'vata': 0, 'pitta': 0, 'kapha': 0}
        
        # Mental + Sleep (weight: 7)
        if data.get('stress') == 'high':
            self.dosha_scores['vata'] += 7
            self.dosha_scores['pitta'] += 3
        elif data.get('stress') == 'moderate':
            self.dosha_scores['vata'] += 3
        
        if data.get('sleep') in ['poor', 'very_poor']:
            self.dosha_scores['vata'] += 6
        elif data.get('sleep') == 'excessive':
            self.dosha_scores['kapha'] += 5
        
        # Digestion (weight: 5)
        if data.get('digestion') == 'constipation':
            self.dosha_scores['vata'] += 5
        elif data.get('digestion') == 'acidity':
            self.dosha_scores['pitta'] += 5
        elif data.get('digestion') == 'slow':
            self.dosha_scores['kapha'] += 4
        elif data.get('digestion') == 'gas':
            self.dosha_scores['vata'] += 3
        
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
        
        # Food preference (weight: 2)
        if data.get('food') == 'spicy':
            self.dosha_scores['pitta'] += 2
        elif data.get('food') == 'sweet':
            self.dosha_scores['kapha'] += 2
    
    def _determine_dominant_dosha(self, disease_risks):
        """Determine dominant dosha (disease-aligned)"""
        
        # RULE: If disease risk exists, dominant dosha MUST align with disease
        if disease_risks:
            # Get dosha from highest severity disease
            primary_risk = max(disease_risks, key=lambda x: 1 if x['severity'] == 'moderate' else 0)
            disease_dosha = primary_risk['dosha']
            
            # Calculate percentages
            total = sum(self.dosha_scores.values()) or 1
            percentages = {
                'vata': round((self.dosha_scores['vata'] / total) * 100, 1),
                'pitta': round((self.dosha_scores['pitta'] / total) * 100, 1),
                'kapha': round((self.dosha_scores['kapha'] / total) * 100, 1)
            }
            
            # Override: Ensure disease dosha is dominant
            if percentages[disease_dosha] < 40:
                # Boost disease dosha to minimum 45%
                percentages[disease_dosha] = 45
                remaining = 55
                other_doshas = [d for d in ['vata', 'pitta', 'kapha'] if d != disease_dosha]
                for d in other_doshas:
                    percentages[d] = remaining / 2
            
            return {
                'primary': disease_dosha,
                'display_name': disease_dosha.capitalize(),
                'scores': percentages,
                'is_disease_aligned': True
            }
        
        # No disease risk: calculate normally
        total = sum(self.dosha_scores.values()) or 1
        percentages = {
            'vata': round((self.dosha_scores['vata'] / total) * 100, 1),
            'pitta': round((self.dosha_scores['pitta'] / total) * 100, 1),
            'kapha': round((self.dosha_scores['kapha'] / total) * 100, 1)
        }
        
        max_dosha = max(percentages, key=percentages.get)
        max_score = percentages[max_dosha]
        
        # Check for dual dosha (≤7% difference)
        sorted_doshas = sorted(percentages.items(), key=lambda x: x[1], reverse=True)
        if abs(sorted_doshas[0][1] - sorted_doshas[1][1]) <= 7:
            return {
                'primary': sorted_doshas[0][0],
                'secondary': sorted_doshas[1][0],
                'display_name': f"{sorted_doshas[0][0].capitalize()}-{sorted_doshas[1][0].capitalize()}",
                'scores': percentages,
                'is_disease_aligned': False
            }
        
        return {
            'primary': max_dosha,
            'display_name': max_dosha.capitalize(),
            'scores': percentages,
            'is_disease_aligned': False
        }
    
    def _determine_dosha_state(self, disease_risks):
        """Determine dosha state (Sama vs Imbalanced)"""
        
        # MANDATORY RULE: Sama Dosha ONLY when NO disease risk
        if disease_risks:
            return 'imbalanced'  # Cannot be Sama if disease risk exists
        
        # Check balance
        scores = list(self.dosha_scores.values())
        score_range = max(scores) - min(scores)
        
        if score_range <= 5:
            return 'sama'  # Balanced
        else:
            return 'mild_imbalance'  # Mild tendency without disease
    
    def _assign_risk_level(self, dosha_state, disease_risks):
        """Assign risk level (consistent with state)"""
        
        # MANDATORY RULE: LOW risk ONLY when Sama Dosha
        if dosha_state == 'sama':
            return 'Low'
        
        # MANDATORY RULE: MODERATE/HIGH risk when disease present
        if disease_risks:
            severity_count = sum(1 for r in disease_risks if r['severity'] == 'moderate')
            if severity_count >= 2:
                return 'High'
            elif severity_count == 1:
                return 'Moderate'
            else:
                return 'Moderate'  # At least moderate if any disease risk
        
        # Mild imbalance without disease
        return 'Preventive'
    
    def _validate_consistency(self, dominant_dosha, dosha_state, risk_level, disease_risks):
        """Final validation to eliminate contradictions"""
        
        # Validation 1: Sama Dosha + Primary Risk (FORBIDDEN)
        if dosha_state == 'sama' and disease_risks:
            dosha_state = 'imbalanced'
            risk_level = 'Moderate'
        
        # Validation 2: Low Risk + Disease Prediction (FORBIDDEN)
        if risk_level == 'Low' and disease_risks:
            risk_level = 'Moderate'
        
        # Validation 3: Balanced State + Dosha-specific pathology (FORBIDDEN)
        if dosha_state == 'sama' and risk_level != 'Low':
            dosha_state = 'mild_imbalance'
        
        # Determine imbalance level
        if dosha_state == 'sama':
            imbalance_level = 'balanced'
        elif dosha_state == 'mild_imbalance':
            imbalance_level = 'mild'
        else:
            max_score = max(dominant_dosha['scores'].values())
            if max_score >= 60:
                imbalance_level = 'severe'
            elif max_score >= 50:
                imbalance_level = 'moderate'
            else:
                imbalance_level = 'mild'
        
        return {
            'scores': dominant_dosha['scores'],
            'dominant': dominant_dosha['display_name'],
            'is_dual': 'secondary' in dominant_dosha,
            'dosha_state': dosha_state,
            'imbalance_level': imbalance_level,
            'risk': risk_level,
            'disease_risks': disease_risks,
            'is_sama_dosha': dosha_state == 'sama'
        }
    
    def _get_description(self, result):
        """Generate description"""
        if result['is_sama_dosha']:
            return "All three doshas are in harmony (Sama Dosha). Continue your healthy lifestyle with preventive care."
        
        base_desc = {
            'vata': 'Vata governs movement, creativity, and nervous system.',
            'pitta': 'Pitta governs metabolism, digestion, and transformation.',
            'kapha': 'Kapha governs structure, stability, and immunity.'
        }
        
        level_desc = {
            'mild': 'Mild imbalance detected. Simple lifestyle adjustments recommended.',
            'moderate': 'Moderate imbalance (Prakopa stage). Follow recommendations to restore balance.',
            'severe': 'Significant imbalance (Vriddhi stage). Prioritize Ayurvedic lifestyle changes.'
        }
        
        primary = result['dominant'].lower().split('-')[0]
        desc = base_desc.get(primary, '')
        
        if result['disease_risks']:
            conditions = ', '.join([r['condition'] for r in result['disease_risks']])
            desc += f" Detected: {conditions}. "
        
        desc += level_desc.get(result['imbalance_level'], '')
        
        return desc
    
    def _get_recommendations(self, result):
        """Generate recommendations"""
        if result['is_sama_dosha']:
            return [
                'Continue balanced lifestyle and regular routines',
                'Practice preventive care with seasonal adjustments',
                'Maintain healthy diet, sleep, and stress management',
                'Regular yoga and pranayama for wellness',
                'Stay hydrated and eat fresh, seasonal foods'
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
        
        primary = result['dominant'].lower().split('-')[0]
        recommendations = recs.get(primary, recs['vata'])[:6]
        
        # Add disease-specific recommendations
        if result['disease_risks']:
            for risk in result['disease_risks']:
                if risk['condition'] == 'Acidity/GERD':
                    recommendations.insert(0, '⚠️ Priority: Avoid spicy, fried, acidic foods; eat small frequent meals')
                elif risk['condition'] == 'Anxiety/Insomnia':
                    recommendations.insert(0, '⚠️ Priority: Establish regular sleep routine; practice relaxation techniques')
                elif risk['condition'] == 'Constipation':
                    recommendations.insert(0, '⚠️ Priority: Increase fiber, warm water; practice abdominal massage')
                elif risk['condition'] == 'Metabolic sluggishness':
                    recommendations.insert(0, '⚠️ Priority: Increase physical activity; reduce heavy, oily foods')
        
        return recommendations[:8]
