"""
Refined Tridosha Intelligence Engine™
Enhanced logic for dual-dosha dominance and accurate risk assessment
"""

class RefinedTridoshaEngine:
    def __init__(self):
        self.vikriti_scores = {'vata': 0, 'pitta': 0, 'kapha': 0}
        self.pathology_indicators = {'vata': 0, 'pitta': 0, 'kapha': 0}
        
    def analyze(self, user_data):
        """Main analysis with refined logic"""
        self._reset_scores()
        
        # Weighted assessment (Ayurvedic priority)
        self._assess_mental_sleep(user_data)  # Weight: 6-7 (highest)
        self._assess_digestion(user_data)  # Weight: 4-5
        self._assess_physical_signs(user_data)  # Weight: 3-4 (strong indicators)
        self._assess_lifestyle(user_data)  # Weight: 1-2 (lowest)
        
        # Calculate percentages
        total = sum(self.vikriti_scores.values()) or 1
        scores = {
            'vata': round((self.vikriti_scores['vata'] / total) * 100, 1),
            'pitta': round((self.vikriti_scores['pitta'] / total) * 100, 1),
            'kapha': round((self.vikriti_scores['kapha'] / total) * 100, 1)
        }
        
        # Identify dominant dosha(s) with dual-dosha handling
        dominant_info = self._identify_dominance(scores)
        
        # Calculate imbalance level
        imbalance_level = self._calculate_imbalance_level(scores, dominant_info)
        
        # Risk assessment with pathology-based logic
        risk_level = self._assess_risk(scores, imbalance_level, dominant_info, user_data)
        
        # Generate recommendations
        recommendations = self._get_recommendations(dominant_info, imbalance_level, user_data)
        
        return {
            'scores': scores,
            'dominant': dominant_info['display_name'],
            'is_dual': dominant_info['is_dual'],
            'risk': risk_level,
            'imbalance_level': imbalance_level,
            'recommendations': recommendations,
            'description': self._get_description(dominant_info, imbalance_level)
        }
    
    def _reset_scores(self):
        self.vikriti_scores = {'vata': 0, 'pitta': 0, 'kapha': 0}
        self.pathology_indicators = {'vata': 0, 'pitta': 0, 'kapha': 0}
    
    def _assess_mental_sleep(self, data):
        """Priority 1: Mental state + Sleep (Weight: 6-7)"""
        stress = data.get('stress', 'low')
        sleep = data.get('sleep')
        
        # Mental state (highest priority)
        if stress == 'high':
            self.vikriti_scores['vata'] += 7
            self.vikriti_scores['pitta'] += 3
            self.pathology_indicators['vata'] += 1
        elif stress == 'moderate':
            self.vikriti_scores['vata'] += 3
        
        # Sleep patterns (critical indicator)
        if sleep == 'very_poor':
            self.vikriti_scores['vata'] += 6
            self.pathology_indicators['vata'] += 1
        elif sleep == 'poor':
            self.vikriti_scores['vata'] += 4
        elif sleep == 'excessive':
            self.vikriti_scores['kapha'] += 5
            self.pathology_indicators['kapha'] += 1
    
    def _assess_digestion(self, data):
        """Priority 2: Digestion + Appetite (Weight: 4-5)"""
        digestion = data.get('digestion')
        appetite = data.get('appetite')
        
        # Digestion (strong pathology indicator)
        if digestion == 'constipation':
            self.vikriti_scores['vata'] += 5
            self.pathology_indicators['vata'] += 1
        elif digestion == 'acidity':
            self.vikriti_scores['pitta'] += 5
            self.pathology_indicators['pitta'] += 1
        elif digestion == 'slow':
            self.vikriti_scores['kapha'] += 4
            self.pathology_indicators['kapha'] += 1
        elif digestion == 'gas':
            self.vikriti_scores['vata'] += 3
        
        # Appetite (medium priority)
        if appetite == 'irregular':
            self.vikriti_scores['vata'] += 4
        elif appetite == 'excessive':
            self.vikriti_scores['pitta'] += 2
            self.vikriti_scores['kapha'] += 2
        elif appetite == 'low':
            self.vikriti_scores['kapha'] += 3
    
    def _assess_physical_signs(self, data):
        """Priority 3: Skin + Temperature (Weight: 3-4, strong indicators)"""
        skin = data.get('skin')
        temperature = data.get('temperature')
        
        # Skin type (strong constitutional indicator)
        if skin == 'dry':
            self.vikriti_scores['vata'] += 4
        elif skin == 'oily':
            self.vikriti_scores['kapha'] += 3
        elif skin == 'sensitive':
            self.vikriti_scores['pitta'] += 4
        
        # Body temperature (strong indicator)
        if temperature == 'cold':
            self.vikriti_scores['vata'] += 3
            self.vikriti_scores['kapha'] += 2
        elif temperature == 'hot':
            self.vikriti_scores['pitta'] += 4
    
    def _assess_lifestyle(self, data):
        """Priority 4: Food preference (Weight: 1-2, lowest)"""
        food = data.get('food')
        
        if food == 'spicy':
            self.vikriti_scores['pitta'] += 2
        elif food == 'sweet':
            self.vikriti_scores['kapha'] += 2
        elif food == 'bitter':
            self.vikriti_scores['vata'] += 1
    
    def _identify_dominance(self, scores):
        """Identify dominant dosha(s) with dual-dosha handling"""
        sorted_doshas = sorted(scores.items(), key=lambda x: x[1], reverse=True)
        
        first_dosha, first_score = sorted_doshas[0]
        second_dosha, second_score = sorted_doshas[1]
        
        score_diff = first_score - second_score
        
        # Dual-dosha dominance if difference ≤ 5%
        if score_diff <= 5:
            return {
                'primary': first_dosha,
                'secondary': second_dosha,
                'is_dual': True,
                'display_name': f"{first_dosha.capitalize()}-{second_dosha.capitalize()}",
                'scores': [first_score, second_score]
            }
        else:
            return {
                'primary': first_dosha,
                'secondary': None,
                'is_dual': False,
                'display_name': first_dosha.capitalize(),
                'scores': [first_score]
            }
    
    def _calculate_imbalance_level(self, scores, dominant_info):
        """Calculate imbalance severity"""
        if dominant_info['is_dual']:
            avg_score = sum(dominant_info['scores']) / 2
            max_score = avg_score
        else:
            max_score = dominant_info['scores'][0]
        
        # Balanced state: all doshas within 10% of each other
        score_range = max(scores.values()) - min(scores.values())
        
        if score_range <= 10:
            return 'balanced'  # Sama Dosha
        elif max_score < 40:
            return 'mild'  # Functional state
        elif max_score < 55:
            return 'moderate'  # Prakopa
        else:
            return 'severe'  # Vriddhi
    
    def _assess_risk(self, scores, imbalance_level, dominant_info, data):
        """Refined risk assessment with pathology-based logic"""
        primary = dominant_info['primary']
        pathology_count = self.pathology_indicators[primary]
        
        # Special Kapha risk logic: require 2+ pathology signs
        if primary == 'kapha':
            kapha_pathology_signs = 0
            if data.get('sleep') == 'excessive': kapha_pathology_signs += 1
            if data.get('digestion') == 'slow': kapha_pathology_signs += 1
            if data.get('appetite') == 'low': kapha_pathology_signs += 1
            
            if kapha_pathology_signs < 2:
                # Insufficient pathology for high Kapha risk
                if imbalance_level == 'balanced':
                    return 'Low'
                else:
                    return 'Preventive'
        
        # Risk logic based on imbalance + pathology
        if imbalance_level == 'balanced':
            return 'Low'  # Healthy state
        
        elif imbalance_level == 'mild':
            if pathology_count == 0:
                return 'Preventive'  # No pathology, just tendency
            else:
                return 'Low'  # Mild with some indicators
        
        elif imbalance_level == 'moderate':
            if pathology_count >= 2:
                return 'Moderate'  # Clear pathology
            else:
                return 'Low'  # Moderate score but low pathology
        
        elif imbalance_level == 'severe':
            if pathology_count >= 2:
                return 'High'  # Clear pathological state
            else:
                return 'Moderate'  # High score but fewer pathology signs
        
        return 'Low'
    
    def _get_description(self, dominant_info, imbalance_level):
        """Generate description"""
        base_desc = {
            'vata': 'Vata governs movement, creativity, and nervous system.',
            'pitta': 'Pitta governs metabolism, digestion, and transformation.',
            'kapha': 'Kapha governs structure, stability, and immunity.'
        }
        
        imbalance_desc = {
            'balanced': 'Your doshas are in good balance (Sama Dosha). Maintain your healthy lifestyle.',
            'mild': 'Mild imbalance detected. Simple lifestyle adjustments recommended for prevention.',
            'moderate': 'Moderate imbalance (Prakopa stage). Follow recommendations to restore balance.',
            'severe': 'Significant imbalance (Vriddhi stage). Prioritize Ayurvedic lifestyle changes.'
        }
        
        if dominant_info['is_dual']:
            desc = f"{base_desc[dominant_info['primary']]} {base_desc[dominant_info['secondary']]} "
        else:
            desc = base_desc[dominant_info['primary']]
        
        return f"{desc} {imbalance_desc[imbalance_level]}"
    
    def _get_recommendations(self, dominant_info, imbalance_level, data):
        """Generate recommendations"""
        base_recs = {
            'vata': [
                'Diet: Warm, cooked, oily foods; ghee, nuts, sweet fruits; regular meal times',
                'Yoga: Gentle, grounding poses - Child pose, Cat-Cow, Legs-up-the-wall',
                'Pranayama: Nadi Shodhana (alternate nostril) 10 min daily',
                'Lifestyle: Regular sleep 10 PM-6 AM, daily oil massage, warm baths',
                'Herbs: Ashwagandha for stress, Brahmi for mental clarity',
                'Avoid: Cold foods, irregular routines, excessive travel'
            ],
            'pitta': [
                'Diet: Cool, fresh foods; cucumber, coconut water, sweet fruits',
                'Yoga: Cooling poses - Moon salutation, Forward bends, Shavasana',
                'Pranayama: Sheetali (cooling breath) 10 min daily',
                'Lifestyle: Avoid midday sun, meditation, work-life balance',
                'Herbs: Amla for cooling, Neem for blood purification',
                'Avoid: Spicy/fried foods, competitive activities, anger triggers'
            ],
            'kapha': [
                'Diet: Light, warm, spicy foods; ginger, turmeric, leafy greens',
                'Yoga: Energizing poses - Sun salutation, Warrior poses, Backbends',
                'Pranayama: Kapalabhati (skull shining) and Bhastrika for energy',
                'Lifestyle: Wake early 6 AM, vigorous exercise, avoid daytime sleep',
                'Herbs: Trikatu for metabolism, Guggulu for weight management',
                'Avoid: Dairy/sweets, sedentary lifestyle, oversleeping'
            ]
        }
        
        recs = base_recs[dominant_info['primary']][:6]
        
        # Add dual-dosha recommendations
        if dominant_info['is_dual']:
            recs.append(f"Balance both {dominant_info['display_name']}: {base_recs[dominant_info['secondary']][0]}")
        
        # Add severity-specific advice
        if imbalance_level == 'severe':
            recs.insert(0, f"⚠️ Priority: Address {dominant_info['display_name']} imbalance with strict lifestyle changes")
        
        return recs
