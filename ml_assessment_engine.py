import PyPDF2
import pickle
import os
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

class MLTridoshaEngine:
    def __init__(self):
        self.dosha_weights = {'vata': 0, 'pitta': 0, 'kapha': 0}
        self.vectorizer = None
        self.dosha_knowledge = {'vata': [], 'pitta': [], 'kapha': []}
        self.model_path = 'dosha_assessment_model.pkl'
    
    def train_from_pdfs(self, pdf_paths):
        """Train model on PDF knowledge"""
        print("Training assessment model on PDFs...")
        
        all_text = ""
        for pdf_path in pdf_paths:
            if os.path.exists(pdf_path):
                print(f"Processing: {pdf_path}")
                with open(pdf_path, 'rb') as file:
                    reader = PyPDF2.PdfReader(file)
                    for page in reader.pages:
                        all_text += page.extract_text() + "\n"
        
        # Extract dosha-specific knowledge
        self._extract_dosha_knowledge(all_text)
        
        # Save model
        with open(self.model_path, 'wb') as f:
            pickle.dump(self.dosha_knowledge, f)
        
        print("Assessment model trained!")
    
    def _extract_dosha_knowledge(self, text):
        """Extract dosha-specific recommendations"""
        lines = text.split('\n')
        current_dosha = None
        
        for line in lines:
            line_lower = line.lower()
            
            if 'vata' in line_lower and len(line) < 200:
                current_dosha = 'vata'
            elif 'pitta' in line_lower and len(line) < 200:
                current_dosha = 'pitta'
            elif 'kapha' in line_lower and len(line) < 200:
                current_dosha = 'kapha'
            
            if current_dosha and len(line) > 30 and len(line) < 200:
                if any(word in line_lower for word in ['diet', 'food', 'eat', 'avoid', 'yoga', 'exercise', 'herb', 'treatment', 'remedy']):
                    self.dosha_knowledge[current_dosha].append(line.strip())
    
    def load_model(self):
        """Load trained model"""
        if os.path.exists(self.model_path):
            with open(self.model_path, 'rb') as f:
                self.dosha_knowledge = pickle.load(f)
            return True
        return False
    
    def analyze(self, user_data):
        """Analyze with ML enhancement"""
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
        
        # Get ML-enhanced recommendations
        recommendations = self._get_ml_recommendations(dominant, user_data)
        
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
        """Calculate dosha scores from user data"""
        if data.get('sleep') in ['poor', 'very_poor']:
            self.dosha_weights['vata'] += 3
        elif data.get('sleep') == 'excessive':
            self.dosha_weights['kapha'] += 2
        
        if data.get('appetite') == 'irregular':
            self.dosha_weights['vata'] += 3
        elif data.get('appetite') == 'excessive':
            self.dosha_weights['pitta'] += 2
            self.dosha_weights['kapha'] += 2
        elif data.get('appetite') == 'low':
            self.dosha_weights['kapha'] += 2
        
        stress = data.get('stress', 'low')
        if stress == 'high':
            self.dosha_weights['vata'] += 4
            self.dosha_weights['pitta'] += 2
        elif stress == 'moderate':
            self.dosha_weights['vata'] += 2
        
        if data.get('digestion') == 'constipation':
            self.dosha_weights['vata'] += 4
        elif data.get('digestion') == 'acidity':
            self.dosha_weights['pitta'] += 4
        elif data.get('digestion') == 'slow':
            self.dosha_weights['kapha'] += 3
        elif data.get('digestion') == 'gas':
            self.dosha_weights['vata'] += 3
        
        if data.get('skin') == 'dry':
            self.dosha_weights['vata'] += 3
        elif data.get('skin') == 'oily':
            self.dosha_weights['kapha'] += 3
        elif data.get('skin') == 'sensitive':
            self.dosha_weights['pitta'] += 3
        
        if data.get('temperature') == 'cold':
            self.dosha_weights['vata'] += 2
            self.dosha_weights['kapha'] += 1
        elif data.get('temperature') == 'hot':
            self.dosha_weights['pitta'] += 3
        
        if data.get('food') == 'spicy':
            self.dosha_weights['pitta'] += 2
        elif data.get('food') == 'sweet':
            self.dosha_weights['kapha'] += 2
        elif data.get('food') == 'bitter':
            self.dosha_weights['vata'] += 1
        
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
    
    def _get_ml_recommendations(self, dosha, data):
        """Get ML-enhanced recommendations from PDF knowledge"""
        if not self.load_model():
            return self._get_fallback_recommendations(dosha)
        
        knowledge = self.dosha_knowledge.get(dosha, [])
        
        if len(knowledge) >= 6:
            # Filter relevant recommendations based on symptoms
            symptoms = [data.get('sleep'), data.get('digestion'), data.get('stress'), data.get('skin')]
            
            relevant_recs = []
            for rec in knowledge[:15]:
                rec_lower = rec.lower()
                if any(str(s).lower() in rec_lower for s in symptoms if s):
                    relevant_recs.append(rec)
            
            # Combine with general recommendations
            all_recs = relevant_recs + knowledge[:10]
            unique_recs = list(dict.fromkeys(all_recs))[:8]
            
            if len(unique_recs) >= 4:
                return unique_recs
        
        return self._get_fallback_recommendations(dosha)
    
    def _get_fallback_recommendations(self, dosha):
        """Fallback recommendations"""
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

if __name__ == "__main__":
    engine = MLTridoshaEngine()
    
    pdf_files = [
        'astang hrdaya.pdf',
        'Ayurvedic Medicine Encyclopedia.pdf'
    ]
    
    engine.train_from_pdfs(pdf_files)
    print("Assessment model ready!")
