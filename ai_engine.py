class TridoshaIntelligenceEngine:
    """
    Tridosha Intelligence Engine™ (TIE)
    AI-powered Ayurvedic health assessment system
    """
    
    def __init__(self):
        self.dosha_weights = {
            'vata': 0,
            'pitta': 0,
            'kapha': 0
        }
    
    def analyze(self, user_data):
        self._reset_scores()
        self._calculate_dosha_scores(user_data)
        
        total = sum(self.dosha_weights.values())
        if total == 0:
            total = 1
        
        scores = {
            'vata': round((self.dosha_weights['vata'] / total) * 100, 1),
            'pitta': round((self.dosha_weights['pitta'] / total) * 100, 1),
            'kapha': round((self.dosha_weights['kapha'] / total) * 100, 1)
        }
        
        dominant = max(scores, key=scores.get)
        risk_level = self._calculate_risk(scores[dominant])
        recommendations = self._get_recommendations(dominant, user_data)
        
        return {
            'scores': scores,
            'dominant': dominant.capitalize(),
            'risk': risk_level,
            'recommendations': recommendations,
            'description': self._get_dosha_description(dominant)
        }
    
    def _reset_scores(self):
        self.dosha_weights = {'vata': 0, 'pitta': 0, 'kapha': 0}
    
    def _calculate_dosha_scores(self, data):
        # Sleep quality analysis
        if data.get('sleep') in ['poor', 'very_poor']:
            self.dosha_weights['vata'] += 3
        elif data.get('sleep') == 'excessive':
            self.dosha_weights['kapha'] += 2
        
        # Appetite analysis
        if data.get('appetite') == 'irregular':
            self.dosha_weights['vata'] += 3
        elif data.get('appetite') == 'excessive':
            self.dosha_weights['pitta'] += 2
            self.dosha_weights['kapha'] += 2
        elif data.get('appetite') == 'low':
            self.dosha_weights['kapha'] += 2
        
        # Stress level
        stress = data.get('stress', 'low')
        if stress == 'high':
            self.dosha_weights['vata'] += 4
            self.dosha_weights['pitta'] += 2
        elif stress == 'moderate':
            self.dosha_weights['vata'] += 2
        
        # Digestion
        if data.get('digestion') == 'constipation':
            self.dosha_weights['vata'] += 4
        elif data.get('digestion') == 'acidity':
            self.dosha_weights['pitta'] += 4
        elif data.get('digestion') == 'slow':
            self.dosha_weights['kapha'] += 3
        elif data.get('digestion') == 'gas':
            self.dosha_weights['vata'] += 3
        
        # Skin type
        if data.get('skin') == 'dry':
            self.dosha_weights['vata'] += 3
        elif data.get('skin') == 'oily':
            self.dosha_weights['kapha'] += 3
        elif data.get('skin') == 'sensitive':
            self.dosha_weights['pitta'] += 3
        
        # Body temperature
        if data.get('temperature') == 'cold':
            self.dosha_weights['vata'] += 2
            self.dosha_weights['kapha'] += 1
        elif data.get('temperature') == 'hot':
            self.dosha_weights['pitta'] += 3
        
        # Food preferences
        if data.get('food') == 'spicy':
            self.dosha_weights['pitta'] += 2
        elif data.get('food') == 'sweet':
            self.dosha_weights['kapha'] += 2
        elif data.get('food') == 'bitter':
            self.dosha_weights['vata'] += 1
        
        # Age factor
        age = int(data.get('age', 25))
        if age < 18:
            self.dosha_weights['kapha'] += 1
        elif age > 50:
            self.dosha_weights['vata'] += 2
        elif 18 <= age <= 50:
            self.dosha_weights['pitta'] += 1
    
    def _calculate_risk(self, score):
        if score >= 50:
            return 'High'
        elif score >= 35:
            return 'Moderate'
        else:
            return 'Low'
    
    def _get_dosha_description(self, dosha):
        descriptions = {
            'vata': 'Vata governs movement, creativity, and nervous system. Imbalance causes anxiety, dryness, and irregular patterns.',
            'pitta': 'Pitta governs metabolism, digestion, and transformation. Imbalance causes heat, inflammation, and anger.',
            'kapha': 'Kapha governs structure, stability, and lubrication. Imbalance causes weight gain, lethargy, and congestion.'
        }
        return descriptions.get(dosha, '')
    
    def _get_recommendations(self, dosha, data):
        # Try to get classical recommendations from Ashtanga Hridaya
        try:
            from ashtanga_knowledge import AshtangaKnowledge
            ak = AshtangaKnowledge()
            
            # Get symptoms for context
            symptoms = {
                'sleep': data.get('sleep'),
                'digestion': data.get('digestion'),
                'stress': data.get('stress'),
                'skin': data.get('skin')
            }
            
            classical_recs = ak.get_recommendations(dosha, symptoms)
            
            # Parse into bullet points
            lines = classical_recs.split('\n')
            recommendations = []
            for line in lines:
                line = line.strip()
                if line.startswith('•') or line.startswith('-'):
                    recommendations.append(line.strip('•- '))
                elif ':' in line and len(line) > 20 and len(line) < 150:
                    recommendations.append(line)
            
            if len(recommendations) >= 4:
                return recommendations[:8]  # Return top 8 recommendations
        except Exception as e:
            print(f"Ashtanga knowledge error: {str(e)}")
        
        # Fallback to basic recommendations
        recommendations = {
            'vata': [
                'Diet: Warm, cooked foods; ghee, nuts, sweet fruits; avoid cold, raw foods',
                'Yoga: Gentle poses - Child pose, Cat-Cow, Legs-up-the-wall',
                'Pranayama: Nadi Shodhana (alternate nostril breathing) for 10 minutes daily',
                'Lifestyle: Regular sleep schedule (10 PM - 6 AM), oil massage, warm baths',
                'Herbs: Ashwagandha, Brahmi for stress relief',
                'Avoid: Excessive travel, irregular routines, cold weather exposure'
            ],
            'pitta': [
                'Diet: Cool, fresh foods; cucumber, coconut, sweet fruits; avoid spicy, fried foods',
                'Yoga: Cooling poses - Moon salutation, Forward bends, Shavasana',
                'Pranayama: Sheetali (cooling breath) and Sheetkari for 10 minutes',
                'Lifestyle: Avoid midday sun, practice meditation, maintain work-life balance',
                'Herbs: Amla, Neem, Aloe vera for cooling effect',
                'Avoid: Competitive activities, anger triggers, excessive heat'
            ],
            'kapha': [
                'Diet: Light, warm, spicy foods; ginger, turmeric, leafy greens; avoid dairy, sweets',
                'Yoga: Energizing poses - Sun salutation, Warrior poses, Backbends',
                'Pranayama: Kapalabhati (skull shining breath) and Bhastrika for energy',
                'Lifestyle: Wake early (6 AM), regular exercise, avoid daytime sleep',
                'Herbs: Trikatu, Guggulu for metabolism boost',
                'Avoid: Sedentary lifestyle, oversleeping, cold/damp environments'
            ]
        }
        return recommendations.get(dosha, [])
