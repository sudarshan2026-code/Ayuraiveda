import pickle
import os
import numpy as np

class DiseasePredictor:
    def __init__(self):
        self.model = None
        self.label_encoder = None
        self.scaler = None
        self.model_path = r'C:\Users\acer\OneDrive\Desktop\Ayurveda\dosha_assessment_model.pkl'
        self.load_model()
        
        # Disease mapping from model predictions
        self.disease_map = {
            0: 'Anxiety Disorder',
            1: 'Insomnia', 
            2: 'Constipation',
            3: 'Arthritis',
            4: 'Acidity/GERD',
            5: 'Hypertension',
            6: 'Skin Inflammation',
            7: 'Obesity',
            8: 'Diabetes Type 2',
            9: 'Respiratory Issues',
            10: 'Migraine',
            11: 'IBS',
            12: 'Metabolic Syndrome',
            13: 'Chronic Fatigue',
            14: 'Good Health'
        }
    
    def load_model(self):
        """Load trained ML model"""
        try:
            if os.path.exists(self.model_path):
                with open(self.model_path, 'rb') as f:
                    data = pickle.load(f)
                    self.model = data.get('model')
                    self.label_encoder = data.get('label_encoder')
                    self.scaler = data.get('scaler')
                print("Disease prediction model loaded successfully")
                return True
        except Exception as e:
            print(f"Error loading model: {e}")
        return False
    
    def predict(self, user_data):
        """Predict diseases using trained ML model"""
        if not self.model:
            return self._fallback_prediction(user_data)
        
        try:
            # Prepare features for model
            features = self._prepare_features(user_data)
            
            # Scale features if scaler exists
            if self.scaler:
                features = self.scaler.transform([features])
            else:
                features = [features]
            
            # Get predictions with probabilities
            predictions = self.model.predict(features)
            probabilities = self.model.predict_proba(features)[0]
            
            # Get top 3 disease predictions
            top_indices = np.argsort(probabilities)[-3:][::-1]
            predicted_diseases = []
            
            for idx in top_indices:
                if probabilities[idx] > 0.15:  # Only include if probability > 15%
                    disease_name = self.disease_map.get(idx, 'Unknown')
                    predicted_diseases.append(f"{disease_name} ({int(probabilities[idx]*100)}% risk)")
            
            if not predicted_diseases:
                predicted_diseases = ['Good Health - Preventive Care Recommended']
            
            # Get risk factors
            vata = user_data.get('vata_score', 33)
            pitta = user_data.get('pitta_score', 33)
            kapha = user_data.get('kapha_score', 33)
            risk_factors = self._calculate_risk_factors(user_data, vata, pitta, kapha)
            
            return {
                'diseases': predicted_diseases,
                'risk_factors': risk_factors,
                'primary_risk': predicted_diseases[0] if predicted_diseases[0] != 'Good Health - Preventive Care Recommended' else None
            }
        except Exception as e:
            print(f"Prediction error: {e}")
            return self._fallback_prediction(user_data)
    
    def _prepare_features(self, data):
        """Prepare feature vector for model"""
        return [
            int(data.get('age', 30)),
            1 if data.get('gender') == 'male' else 0,
            self._encode_sleep(data.get('sleep', 'good')),
            self._encode_appetite(data.get('appetite', 'regular')),
            self._encode_stress(data.get('stress', 'low')),
            self._encode_digestion(data.get('digestion', 'normal')),
            self._encode_skin(data.get('skin', 'normal')),
            self._encode_temp(data.get('temperature', 'normal')),
            self._encode_food(data.get('food', 'balanced')),
            data.get('vata_score', 33),
            data.get('pitta_score', 33),
            data.get('kapha_score', 33)
        ]
    
    def _fallback_prediction(self, user_data):
        """Fallback when model unavailable"""
        vata = user_data.get('vata_score', 33)
        pitta = user_data.get('pitta_score', 33)
        kapha = user_data.get('kapha_score', 33)
        
        diseases = []
        if vata > 40:
            diseases.extend(['Anxiety Disorder', 'Insomnia', 'Constipation'])
        if pitta > 40:
            diseases.extend(['Acidity/GERD', 'Hypertension', 'Skin Inflammation'])
        if kapha > 40:
            diseases.extend(['Obesity', 'Diabetes Type 2', 'Respiratory Issues'])
        
        if not diseases:
            diseases = ['Good Health - Preventive Care Recommended']
        
        return {
            'diseases': diseases[:3],
            'risk_factors': self._calculate_risk_factors(user_data, vata, pitta, kapha),
            'primary_risk': diseases[0] if diseases[0] != 'Good Health - Preventive Care Recommended' else None
        }
    
    def _calculate_risk_factors(self, data, vata, pitta, kapha):
        """Calculate specific risk factors"""
        risks = []
        
        if data.get('sleep') == 'poor' and vata > 35:
            risks.append('High risk for anxiety and nervous system disorders')
        
        if data.get('digestion') in ['acidity', 'burning'] and pitta > 35:
            risks.append('High risk for GERD and digestive inflammation')
        
        if data.get('appetite') == 'excessive' and kapha > 35:
            risks.append('High risk for metabolic disorders and weight gain')
        
        if data.get('stress') == 'high':
            risks.append('Elevated stress increases all dosha imbalances')
        
        if data.get('skin') == 'oily' and kapha > 40:
            risks.append('Risk for skin congestion and acne')
        
        if data.get('temperature') == 'always_hot' and pitta > 40:
            risks.append('Risk for inflammatory conditions')
        
        if not risks:
            risks.append('Low risk - maintain current lifestyle')
        
        return risks
    
    def _encode_sleep(self, val):
        return {'excellent': 0, 'good': 1, 'poor': 2, 'very_poor': 3, 'excessive': 4}.get(val, 1)
    
    def _encode_appetite(self, val):
        return {'regular': 0, 'irregular': 1, 'excessive': 2, 'low': 3}.get(val, 0)
    
    def _encode_stress(self, val):
        return {'low': 0, 'moderate': 1, 'high': 2}.get(val, 0)
    
    def _encode_digestion(self, val):
        return {'normal': 0, 'constipation': 1, 'acidity': 2, 'gas': 3, 'slow': 4}.get(val, 0)
    
    def _encode_skin(self, val):
        return {'normal': 0, 'dry': 1, 'oily': 2, 'sensitive': 3}.get(val, 0)
    
    def _encode_temp(self, val):
        return {'normal': 0, 'cold': 1, 'hot': 2}.get(val, 0)
    
    def _encode_food(self, val):
        return {'balanced': 0, 'spicy': 1, 'sweet': 2, 'bitter': 3}.get(val, 0)
