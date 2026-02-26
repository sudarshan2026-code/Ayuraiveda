"""
Advanced Tridosha Intelligence Engine™
Based on classical Ayurvedic principles with improved accuracy
"""

class AdvancedTridoshaEngine:
    def __init__(self):
        self.prakriti_scores = {'vata': 0, 'pitta': 0, 'kapha': 0}
        self.vikriti_scores = {'vata': 0, 'pitta': 0, 'kapha': 0}
        
    def analyze(self, user_data):
        """Main analysis with Prakriti-Vikriti separation"""
        self._reset_scores()
        
        # Calculate scores with Ayurvedic priority
        self._assess_mental_state(user_data)  # Highest priority
        self._assess_sleep_patterns(user_data)  # High priority
        self._assess_digestion(user_data)  # Medium-high priority
        self._assess_physical_signs(user_data)  # Medium priority
        self._assess_lifestyle(user_data)  # Lower priority
        self._assess_prakriti(user_data)  # Constitutional baseline
        
        # Calculate percentages
        vikriti_total = sum(self.vikriti_scores.values()) or 1
        prakriti_total = sum(self.prakriti_scores.values()) or 1
        
        vikriti_percent = {
            'vata': round((self.vikriti_scores['vata'] / vikriti_total) * 100, 1),
            'pitta': round((self.vikriti_scores['pitta'] / vikriti_total) * 100, 1),
            'kapha': round((self.vikriti_scores['kapha'] / vikriti_total) * 100, 1)
        }
        
        prakriti_percent = {
            'vata': round((self.prakriti_scores['vata'] / prakriti_total) * 100, 1),
            'pitta': round((self.prakriti_scores['pitta'] / prakriti_total) * 100, 1),
            'kapha': round((self.prakriti_scores['kapha'] / prakriti_total) * 100, 1)
        }
        
        # Determine dominant and secondary doshas
        dominant, secondary = self._identify_doshas(vikriti_percent)
        
        # Calculate imbalance severity (Dosha Vriddhi)
        imbalance_level = self._calculate_imbalance(vikriti_percent, prakriti_percent, dominant)
        
        # Risk assessment using Samprapti (disease progression)
        risk_level = self._assess_disease_risk(vikriti_percent, imbalance_level, user_data)
        
        # Generate recommendations
        recommendations = self._get_recommendations(dominant, secondary, imbalance_level, user_data)
        
        return {
            'scores': vikriti_percent,
            'prakriti': prakriti_percent,
            'dominant': dominant.capitalize(),
            'secondary': secondary.capitalize() if secondary else None,
            'risk': risk_level,
            'imbalance_level': imbalance_level,
            'recommendations': recommendations,
            'description': self._get_description(dominant, imbalance_level)
        }
    
    def _reset_scores(self):
        self.prakriti_scores = {'vata': 0, 'pitta': 0, 'kapha': 0}
        self.vikriti_scores = {'vata': 0, 'pitta': 0, 'kapha': 0}
    
    def _assess_mental_state(self, data):
        """Priority 1: Mental state (Manas) - Most important in Ayurveda"""
        stress = data.get('stress', 'low')
        
        if stress == 'high':
            self.vikriti_scores['vata'] += 6  # Vata governs mind
            self.vikriti_scores['pitta'] += 3  # Pitta secondary
        elif stress == 'moderate':
            self.vikriti_scores['vata'] += 3
            self.vikriti_scores['pitta'] += 1
    
    def _assess_sleep_patterns(self, data):
        """Priority 2: Sleep (Nidra) - Critical for dosha balance"""
        sleep = data.get('sleep')
        
        if sleep == 'very_poor':
            self.vikriti_scores['vata'] += 5  # Severe Vata aggravation
        elif sleep == 'poor':
            self.vikriti_scores['vata'] += 3
        elif sleep == 'excessive':
            self.vikriti_scores['kapha'] += 4  # Kapha excess
            self.prakriti_scores['kapha'] += 2
    
    def _assess_digestion(self, data):
        """Priority 3: Digestion (Agni) - Foundation of health"""
        digestion = data.get('digestion')
        appetite = data.get('appetite')
        
        # Digestion patterns
        if digestion == 'constipation':
            self.vikriti_scores['vata'] += 5  # Classic Vata sign
        elif digestion == 'acidity':
            self.vikriti_scores['pitta'] += 5  # Classic Pitta sign
        elif digestion == 'slow':
            self.vikriti_scores['kapha'] += 4  # Kapha sluggishness
        elif digestion == 'gas':
            self.vikriti_scores['vata'] += 3
        
        # Appetite patterns
        if appetite == 'irregular':
            self.vikriti_scores['vata'] += 4
            self.prakriti_scores['vata'] += 2
        elif appetite == 'excessive':
            self.vikriti_scores['pitta'] += 3
            self.vikriti_scores['kapha'] += 2
        elif appetite == 'low':
            self.vikriti_scores['kapha'] += 3
    
    def _assess_physical_signs(self, data):
        """Priority 4: Physical manifestations"""
        skin = data.get('skin')
        temperature = data.get('temperature')
        
        # Skin type (reflects both Prakriti and Vikriti)
        if skin == 'dry':
            self.vikriti_scores['vata'] += 3
            self.prakriti_scores['vata'] += 3
        elif skin == 'oily':
            self.vikriti_scores['kapha'] += 2
            self.prakriti_scores['kapha'] += 3
        elif skin == 'sensitive':
            self.vikriti_scores['pitta'] += 3
            self.prakriti_scores['pitta'] += 2
        
        # Body temperature
        if temperature == 'cold':
            self.vikriti_scores['vata'] += 2
            self.vikriti_scores['kapha'] += 1
        elif temperature == 'hot':
            self.vikriti_scores['pitta'] += 3
    
    def _assess_lifestyle(self, data):
        """Priority 5: Lifestyle factors"""
        food = data.get('food')
        
        if food == 'spicy':
            self.vikriti_scores['pitta'] += 2
        elif food == 'sweet':
            self.vikriti_scores['kapha'] += 2
        elif food == 'bitter':
            self.vikriti_scores['vata'] += 1
    
    def _assess_prakriti(self, data):
        """Determine natural constitution from age and stable traits"""
        age = int(data.get('age', 25))
        
        # Age-based Prakriti tendency
        if age < 18:
            self.prakriti_scores['kapha'] += 2  # Kapha phase of life
        elif 18 <= age <= 50:
            self.prakriti_scores['pitta'] += 2  # Pitta phase
        elif age > 50:
            self.prakriti_scores['vata'] += 2  # Vata phase
    
    def _identify_doshas(self, scores):
        """Identify dominant and secondary (Anubandha) doshas"""
        sorted_doshas = sorted(scores.items(), key=lambda x: x[1], reverse=True)
        
        dominant = sorted_doshas[0][0]
        dominant_score = sorted_doshas[0][1]
        secondary_score = sorted_doshas[1][1]
        
        # Secondary dosha only if within 15% of dominant
        secondary = sorted_doshas[1][0] if (dominant_score - secondary_score) < 15 else None
        
        return dominant, secondary
    
    def _calculate_imbalance(self, vikriti, prakriti, dominant):
        """Calculate imbalance severity (Sama/Vishama Dosha)"""
        deviation = abs(vikriti[dominant] - prakriti[dominant])
        
        if deviation < 10:
            return 'balanced'  # Sama Dosha
        elif deviation < 25:
            return 'mild'  # Mild Vriddhi
        elif deviation < 40:
            return 'moderate'  # Moderate Vriddhi
        else:
            return 'severe'  # Severe Vriddhi (Prakopa stage)
    
    def _assess_disease_risk(self, vikriti, imbalance_level, data):
        """Risk assessment using Samprapti (disease pathogenesis)"""
        dominant_score = max(vikriti.values())
        
        # Check for multiple severe symptoms (Samprapti progression)
        severe_symptoms = 0
        if data.get('stress') == 'high': severe_symptoms += 1
        if data.get('sleep') in ['very_poor', 'poor']: severe_symptoms += 1
        if data.get('digestion') in ['constipation', 'acidity']: severe_symptoms += 1
        
        # Risk calculation
        if imbalance_level == 'balanced' and severe_symptoms == 0:
            return 'Low'  # Healthy state
        elif imbalance_level == 'mild' or severe_symptoms == 1:
            return 'Low'  # Early stage (Sanchaya)
        elif imbalance_level == 'moderate' or severe_symptoms == 2:
            return 'Moderate'  # Accumulation stage (Prakopa)
        elif imbalance_level == 'severe' or severe_symptoms >= 3:
            return 'High'  # Spread stage (Prasara) - needs attention
        else:
            return 'Low'
    
    def _get_description(self, dosha, imbalance_level):
        """Get description based on dosha and imbalance"""
        base_desc = {
            'vata': 'Vata governs movement, creativity, and nervous system.',
            'pitta': 'Pitta governs metabolism, digestion, and transformation.',
            'kapha': 'Kapha governs structure, stability, and immunity.'
        }
        
        imbalance_desc = {
            'balanced': 'Your doshas are in good balance (Sama Dosha). Continue your healthy lifestyle.',
            'mild': 'Mild imbalance detected (early Vriddhi stage). Simple lifestyle adjustments recommended.',
            'moderate': 'Moderate imbalance (Prakopa stage). Follow recommendations to restore balance.',
            'severe': 'Significant imbalance (Prasara stage). Prioritize Ayurvedic lifestyle changes and consider consulting a practitioner.'
        }
        
        return f"{base_desc[dosha]} {imbalance_desc[imbalance_level]}"
    
    def _get_recommendations(self, dominant, secondary, imbalance_level, data):
        """Generate targeted recommendations"""
        base_recs = {
            'vata': [
                'Diet: Warm, cooked, oily foods; ghee, nuts, sweet fruits; regular meal times',
                'Yoga: Gentle, grounding poses - Child pose, Cat-Cow, Legs-up-the-wall',
                'Pranayama: Nadi Shodhana (alternate nostril) 10 min daily for nervous system',
                'Lifestyle: Regular sleep 10 PM-6 AM, daily oil massage (Abhyanga), warm baths',
                'Herbs: Ashwagandha for stress, Brahmi for mental clarity',
                'Avoid: Cold foods, irregular routines, excessive travel, raw vegetables'
            ],
            'pitta': [
                'Diet: Cool, fresh foods; cucumber, coconut water, sweet fruits; avoid spicy/fried',
                'Yoga: Cooling poses - Moon salutation, Forward bends, Shavasana',
                'Pranayama: Sheetali (cooling breath) and Sheetkari 10 min daily',
                'Lifestyle: Avoid midday sun, meditation, work-life balance, cool environment',
                'Herbs: Amla for cooling, Neem for blood purification, Aloe vera',
                'Avoid: Competitive activities, anger triggers, excessive heat, alcohol'
            ],
            'kapha': [
                'Diet: Light, warm, spicy foods; ginger, turmeric, leafy greens; avoid dairy/sweets',
                'Yoga: Energizing poses - Sun salutation, Warrior poses, Backbends',
                'Pranayama: Kapalabhati (skull shining) and Bhastrika for energy',
                'Lifestyle: Wake early 6 AM, vigorous exercise, avoid daytime sleep',
                'Herbs: Trikatu for metabolism, Guggulu for weight management',
                'Avoid: Sedentary lifestyle, oversleeping, cold/damp environments, heavy foods'
            ]
        }
        
        recs = base_recs[dominant][:6]
        
        # Add secondary dosha recommendations if present
        if secondary and imbalance_level in ['moderate', 'severe']:
            recs.append(f"Also balance {secondary.capitalize()}: {base_recs[secondary][0]}")
        
        # Add severity-specific advice
        if imbalance_level == 'severe':
            recs.insert(0, f"⚠️ Priority: Address {dominant.capitalize()} imbalance immediately with strict dietary and lifestyle changes")
        
        return recs
