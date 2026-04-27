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
        
        # Voting logic: max raw score determines dominant dosha
        raw_scores = self.dosha_weights.copy()
        dominant = max(raw_scores, key=raw_scores.get)
        
        # Calculate percentages for display
        total = sum(raw_scores.values())
        if total == 0:
            total = 1
        
        scores = {
            'vata': round((raw_scores['vata'] / total) * 100, 1),
            'pitta': round((raw_scores['pitta'] / total) * 100, 1),
            'kapha': round((raw_scores['kapha'] / total) * 100, 1)
        }
        
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
        """Clinical assessment pattern recommendations"""
        recommendations = {
            'vata': {
                'diet': [
                    'Favor: Warm, cooked, moist foods with healthy fats (ghee, sesame oil)',
                    'Include: Sweet fruits (bananas, dates), cooked grains (rice, oats), root vegetables',
                    'Avoid: Cold, dry, raw foods; excessive caffeine and stimulants',
                    'Timing: Regular meal times, largest meal at lunch (12-1 PM)'
                ],
                'lifestyle': [
                    'Daily Routine: Wake 6 AM, sleep 10 PM; maintain consistent schedule',
                    'Abhyanga: Daily warm sesame oil massage before bath',
                    'Environment: Keep warm, avoid cold winds and air conditioning',
                    'Rest: 7-8 hours quality sleep in quiet, warm room'
                ],
                'yoga_pranayama': [
                    'Yoga: Gentle, grounding poses - Child pose, Cat-Cow, Legs-up-wall',
                    'Pranayama: Nadi Shodhana (alternate nostril) 10 min daily',
                    'Meditation: Grounding practices, body scan meditation',
                    'Exercise: Gentle walking, swimming, avoid excessive cardio'
                ],
                'herbs': [
                    'Ashwagandha: 500mg twice daily for stress and anxiety',
                    'Brahmi: For mental clarity and nervous system support',
                    'Triphala: At bedtime for gentle detox and regularity',
                    'Dashamula: For Vata pacification and grounding'
                ]
            },
            'pitta': {
                'diet': [
                    'Favor: Cool, fresh foods; cucumber, coconut, sweet fruits, leafy greens',
                    'Include: Cooling spices (coriander, fennel, cardamom), ghee in moderation',
                    'Avoid: Spicy, fried, acidic, fermented foods; alcohol and red meat',
                    'Timing: Never skip meals, eat in cool environment, avoid eating when angry'
                ],
                'lifestyle': [
                    'Daily Routine: Wake 5:30 AM, sleep 10:30 PM; avoid midday sun',
                    'Cooling Practices: Cool showers, moonlight walks, time in nature',
                    'Work-Life Balance: Avoid overwork, competition, and perfectionism',
                    'Environment: Stay cool, use cooling colors (blue, green, white)'
                ],
                'yoga_pranayama': [
                    'Yoga: Cooling poses - Moon salutation, Forward bends, Shavasana',
                    'Pranayama: Sheetali and Sheetkari (cooling breaths) 10 min daily',
                    'Meditation: Loving-kindness meditation, visualization of cool places',
                    'Exercise: Swimming, yoga in cool place, moderate intensity'
                ],
                'herbs': [
                    'Amla: Rich in Vitamin C, cooling and rejuvenating',
                    'Neem: Blood purifier, cooling effect on body',
                    'Aloe Vera: Cooling, anti-inflammatory, digestive support',
                    'Shatavari: Cooling tonic, especially for women'
                ]
            },
            'kapha': {
                'diet': [
                    'Favor: Light, warm, spicy foods; ginger, turmeric, black pepper, leafy greens',
                    'Include: Astringent fruits (apples, pomegranate), light proteins, warming spices',
                    'Avoid: Heavy, oily, sweet foods; dairy products, cold foods, excessive salt',
                    'Timing: Light breakfast or skip, main meal at lunch, early light dinner'
                ],
                'lifestyle': [
                    'Daily Routine: Wake 5 AM (before sunrise), avoid daytime sleep',
                    'Activity: Stay physically and mentally active throughout day',
                    'Dry Brushing: Before shower to stimulate circulation',
                    'Environment: Bright, warm, stimulating; avoid damp, cold places'
                ],
                'yoga_pranayama': [
                    'Yoga: Energizing poses - Sun salutation, Warrior poses, Backbends',
                    'Pranayama: Kapalabhati and Bhastrika (energizing breaths) 10 min daily',
                    'Meditation: Active meditation, walking meditation',
                    'Exercise: High-intensity cardio, running, weight training, dynamic yoga'
                ],
                'herbs': [
                    'Trikatu: Ginger, black pepper, long pepper for metabolism',
                    'Guggulu: For weight management and cholesterol',
                    'Punarnava: Diuretic, reduces water retention',
                    'Tulsi: Energizing, immune-boosting, respiratory support'
                ]
            }
        }
        
        dosha_recs = recommendations.get(dosha, recommendations['vata'])
        
        # Flatten into clinical format
        clinical_recs = []
        clinical_recs.append('DIETARY RECOMMENDATIONS:')
        clinical_recs.extend(dosha_recs['diet'])
        clinical_recs.append('\nLIFESTYLE MODIFICATIONS:')
        clinical_recs.extend(dosha_recs['lifestyle'])
        clinical_recs.append('\nYOGA & PRANAYAMA:')
        clinical_recs.extend(dosha_recs['yoga_pranayama'])
        clinical_recs.append('\nHERBAL SUPPORT:')
        clinical_recs.extend(dosha_recs['herbs'])
        
        return clinical_recs
