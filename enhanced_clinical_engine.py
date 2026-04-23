import pickle
import numpy as np
import os
from datetime import datetime

class EnhancedClinicalEngine:
    def __init__(self):
        self.model_path = "C:/Users/jayde/Documents/Ayurveda/dosha_assessment_model.pkl"
        self.model = None
        self.load_model()
        
    def load_model(self):
        """Load the trained ML model"""
        try:
            if os.path.exists(self.model_path):
                with open(self.model_path, 'rb') as f:
                    loaded_data = pickle.load(f)
                    # Handle different model formats
                    if hasattr(loaded_data, 'predict_proba'):
                        self.model = loaded_data
                    elif isinstance(loaded_data, dict) and 'model' in loaded_data:
                        self.model = loaded_data['model']
                    else:
                        print("⚠ Invalid model format, using rule-based system")
                        return False
                print("✓ ML model loaded successfully")
                return True
            else:
                print("⚠ ML model not found, using rule-based system")
                return False
        except Exception as e:
            print(f"⚠ Error loading ML model: {e}")
            return False
    
    def analyze(self, data):
        """Enhanced analysis with ML model, diet suggestions, and disease predictions"""
        try:
            # Use ML model if available
            if self.model:
                ml_result = self.ml_analyze(data)
                if ml_result:
                    return ml_result
            
            # Fallback to rule-based analysis
            return self.rule_based_analyze(data)
            
        except Exception as e:
            print(f"Analysis error: {e}")
            return self.rule_based_analyze(data)
    
    def ml_analyze(self, data):
        """ML-based analysis using the trained model"""
        try:
            # Verify model has predict_proba method
            if not hasattr(self.model, 'predict_proba'):
                print("⚠ Model doesn't support probability prediction, using rule-based")
                return None
            
            # Prepare features for ML model
            features = self.prepare_features(data)
            
            # Get ML predictions
            dosha_scores = self.model.predict_proba([features])[0]
            
            # Map to dosha names (assuming order: vata, pitta, kapha)
            vata_score = int(dosha_scores[0] * 100)
            pitta_score = int(dosha_scores[1] * 100)
            kapha_score = int(dosha_scores[2] * 100)
            
            # Determine dominant dosha
            scores = {'vata': vata_score, 'pitta': pitta_score, 'kapha': kapha_score}
            dominant = max(scores, key=scores.get)
            
            # Determine risk level
            max_score = max(scores.values())
            if max_score >= 60:
                risk = 'High'
            elif max_score >= 40:
                risk = 'Moderate'
            else:
                risk = 'Low'
            
            # Generate comprehensive result
            result = {
                'dominant': dominant.capitalize(),
                'scores': scores,
                'risk': risk,
                'dosha_state': self.get_dosha_state(scores),
                'agni_state': self.get_agni_state(data),
                'ama_status': self.get_ama_status(data),
                'justification': self.get_ml_justification(dominant, scores, data),
                'recommendations': self.get_enhanced_recommendations(dominant, data),
                'diet_suggestions': self.get_detailed_diet_suggestions(dominant, data),
                'disease_predictions': self.get_disease_predictions(dominant, scores, data),
                'lifestyle_tips': self.get_lifestyle_tips(dominant, data)
            }
            
            return result
            
        except Exception as e:
            print(f"ML analysis error: {e}")
            print(f"Model type: {type(self.model)}")
            print(f"Model attributes: {dir(self.model) if self.model else 'None'}")
            return None
    
    def prepare_features(self, data):
        """Convert form data to ML model features"""
        # Map form responses to numerical features
        feature_map = {
            'body_structure': {'lean': 0, 'moderate': 1, 'heavy': 2},
            'vikriti': {'balanced': 0, 'mild': 1, 'moderate': 2, 'severe': 3},
            'appetite': {'regular': 0, 'irregular': 1, 'excessive': 2, 'low': 3},
            'digestion': {'normal': 0, 'gas': 1, 'acidity': 2, 'constipation': 3, 'slow': 4},
            'skin': {'normal': 0, 'dry': 1, 'oily': 2, 'sensitive': 3},
            'temperature': {'normal': 0, 'cold': 1, 'hot': 2},
            'sweat': {'normal': 0, 'minimal': 1, 'excessive': 2},
            'energy': {'stable': 0, 'fluctuating': 1, 'heavy': 2, 'hyperactive': 3},
            'stress': {'low': 0, 'moderate': 1, 'high': 2},
            'anxiety': {'none': 0, 'moderate': 1, 'high': 2},
            'sleep': {'excellent': 0, 'good': 1, 'poor': 2, 'very_poor': 3, 'excessive': 4},
            'mental_clarity': {'clear': 0, 'foggy': 1, 'sharp': 2, 'dull': 3},
            'exercise_tolerance': {'high': 0, 'moderate': 1, 'low': 2},
            'climate': {'good': 0, 'cold_sensitive': 1, 'heat_sensitive': 2, 'humidity_sensitive': 3},
            'food_tolerance': {'good': 0, 'sensitive': 1, 'specific': 2},
            'immunity': {'strong': 0, 'moderate': 1, 'weak': 2}
        }
        
        features = []
        for key, mapping in feature_map.items():
            value = data.get(key, 'normal')
            features.append(mapping.get(value, 0))
        
        # Add numerical features
        features.extend([
            int(data.get('mala', 0)),
            int(data.get('mutra_frequency', 0)),
            int(data.get('tongue_coating', 0)),
            int(data.get('bloating', 0))
        ])
        
        return features
    
    def rule_based_analyze(self, data):
        """Fallback rule-based analysis"""
        vata_score = pitta_score = kapha_score = 0
        
        # Body structure
        if data.get('body_structure') == 'lean':
            vata_score += 3
        elif data.get('body_structure') == 'moderate':
            pitta_score += 3
        elif data.get('body_structure') == 'heavy':
            kapha_score += 3
        
        # Digestion patterns
        if data.get('appetite') == 'irregular':
            vata_score += 2
        elif data.get('appetite') == 'excessive':
            pitta_score += 2
        elif data.get('appetite') == 'low':
            kapha_score += 2
        
        if data.get('digestion') == 'gas':
            vata_score += 2
        elif data.get('digestion') == 'acidity':
            pitta_score += 3
        elif data.get('digestion') == 'slow':
            kapha_score += 2
        
        # Physical characteristics
        if data.get('skin') == 'dry':
            vata_score += 2
        elif data.get('skin') == 'oily':
            kapha_score += 2
        elif data.get('skin') == 'sensitive':
            pitta_score += 2
        
        if data.get('temperature') == 'cold':
            vata_score += 2
        elif data.get('temperature') == 'hot':
            pitta_score += 2
        
        # Mental characteristics
        if data.get('stress') == 'high':
            vata_score += 2
        if data.get('anxiety') == 'high':
            vata_score += 3
        
        if data.get('sleep') in ['poor', 'very_poor']:
            vata_score += 2
        elif data.get('sleep') == 'excessive':
            kapha_score += 2
        
        # Normalize scores
        total = max(vata_score + pitta_score + kapha_score, 1)
        scores = {
            'vata': int((vata_score / total) * 100),
            'pitta': int((pitta_score / total) * 100),
            'kapha': int((kapha_score / total) * 100)
        }
        
        dominant = max(scores, key=scores.get)
        max_score = max(scores.values())
        
        if max_score >= 50:
            risk = 'High'
        elif max_score >= 35:
            risk = 'Moderate'
        else:
            risk = 'Low'
        
        return {
            'dominant': dominant.capitalize(),
            'scores': scores,
            'risk': risk,
            'dosha_state': self.get_dosha_state(scores),
            'agni_state': self.get_agni_state(data),
            'ama_status': self.get_ama_status(data),
            'justification': self.get_rule_justification(dominant, scores, data),
            'recommendations': self.get_enhanced_recommendations(dominant, data),
            'diet_suggestions': self.get_detailed_diet_suggestions(dominant, data),
            'disease_predictions': self.get_disease_predictions(dominant, scores, data),
            'lifestyle_tips': self.get_lifestyle_tips(dominant, data)
        }
    
    def get_dosha_state(self, scores):
        """Determine overall dosha state"""
        max_score = max(scores.values())
        if max_score >= 60:
            return "Significantly Imbalanced"
        elif max_score >= 45:
            return "Moderately Imbalanced"
        elif max_score >= 35:
            return "Mildly Imbalanced"
        else:
            return "Relatively Balanced"
    
    def get_agni_state(self, data):
        """Determine digestive fire state"""
        if data.get('digestion') == 'normal' and data.get('appetite') == 'regular':
            return "Balanced Agni (Sama Agni)"
        elif data.get('digestion') in ['gas', 'constipation'] or data.get('appetite') == 'irregular':
            return "Variable Agni (Vishama Agni)"
        elif data.get('digestion') == 'acidity' or data.get('appetite') == 'excessive':
            return "Sharp Agni (Tikshna Agni)"
        elif data.get('digestion') == 'slow' or data.get('appetite') == 'low':
            return "Weak Agni (Manda Agni)"
        else:
            return "Moderate Agni"
    
    def get_ama_status(self, data):
        """Determine toxin accumulation status"""
        ama_indicators = 0
        
        if data.get('tongue_coating', 0) >= 2:
            ama_indicators += 1
        if data.get('bloating', 0) >= 2:
            ama_indicators += 1
        if data.get('energy') in ['heavy', 'fluctuating']:
            ama_indicators += 1
        if data.get('mental_clarity') in ['foggy', 'dull']:
            ama_indicators += 1
        
        if ama_indicators >= 3:
            return "High Ama (Significant Toxin Accumulation)"
        elif ama_indicators >= 2:
            return "Moderate Ama (Some Toxin Buildup)"
        elif ama_indicators >= 1:
            return "Mild Ama (Minor Toxin Presence)"
        else:
            return "Low Ama (Minimal Toxins)"
    
    def get_ml_justification(self, dominant, scores, data):
        """Generate ML-based justification"""
        return f"Based on machine learning analysis of your 20 clinical parameters, your constitution shows {dominant} dominance ({scores[dominant.lower()]}%). Key indicators include your {data.get('body_structure', 'moderate')} body structure, {data.get('digestion', 'normal')} digestion pattern, and {data.get('energy', 'stable')} energy levels."
    
    def get_rule_justification(self, dominant, scores, data):
        """Generate rule-based justification"""
        return f"Classical Ayurvedic analysis indicates {dominant} predominance ({scores[dominant.lower()]}%) based on your constitutional markers, digestive patterns, and mental-physical characteristics."
    
    def get_enhanced_recommendations(self, dominant, data):
        """Get comprehensive recommendations"""
        base_recs = {
            'vata': [
                "Follow regular daily routine (Dinacharya) - wake up and sleep at same time",
                "Practice daily oil massage (Abhyanga) with warm sesame oil",
                "Eat warm, cooked, moist foods - avoid cold, dry, raw foods",
                "Practice gentle yoga and meditation - avoid excessive exercise",
                "Stay warm and avoid cold, windy environments",
                "Use calming essential oils like lavender and sandalwood"
            ],
            'pitta': [
                "Maintain cool environment and avoid excessive heat",
                "Practice cooling pranayama (Sheetali, Sheetkari)",
                "Eat cooling, sweet, bitter foods - avoid spicy, sour, salty",
                "Practice moderate exercise during cooler parts of day",
                "Cultivate patience and avoid competitive activities",
                "Use cooling oils like coconut or sunflower for massage"
            ],
            'kapha': [
                "Wake up early (before 6 AM) and avoid daytime napping",
                "Practice vigorous exercise and active lifestyle",
                "Eat light, warm, spicy foods - avoid heavy, oily, sweet",
                "Use dry brushing and stimulating massage",
                "Stay active and avoid sedentary lifestyle",
                "Use warming spices like ginger, black pepper, cinnamon"
            ]
        }
        
        recommendations = base_recs.get(dominant.lower(), base_recs['vata'])
        
        # Add specific recommendations based on symptoms
        if data.get('stress') == 'high':
            recommendations.append("Practice stress-reduction techniques: meditation, deep breathing")
        
        if data.get('sleep') in ['poor', 'very_poor']:
            recommendations.append("Establish sleep hygiene: no screens 1 hour before bed, chamomile tea")
        
        if data.get('digestion') != 'normal':
            recommendations.append("Take digestive spices before meals: ginger, cumin, fennel")
        
        return recommendations
    
    def get_detailed_diet_suggestions(self, dominant, data):
        """Get detailed diet recommendations"""
        diet_plans = {
            'vata': {
                'foods_to_favor': [
                    "Warm, cooked grains: rice, oats, quinoa",
                    "Sweet fruits: bananas, mangoes, dates, figs",
                    "Cooked vegetables: sweet potato, carrots, beets",
                    "Healthy fats: ghee, sesame oil, avocado",
                    "Warm spices: ginger, cinnamon, cardamom, fennel",
                    "Dairy: warm milk, fresh cheese, yogurt",
                    "Nuts and seeds: almonds, walnuts, sesame seeds"
                ],
                'foods_to_avoid': [
                    "Cold, frozen foods and ice-cold drinks",
                    "Raw vegetables and salads",
                    "Dry, light foods: crackers, popcorn",
                    "Bitter vegetables: broccoli, cabbage, cauliflower",
                    "Stimulants: coffee, black tea, alcohol",
                    "Processed and packaged foods"
                ],
                'meal_timing': [
                    "Eat at regular times - breakfast 7-8 AM",
                    "Lunch 12-1 PM (largest meal)",
                    "Dinner 6-7 PM (lighter meal)",
                    "Avoid skipping meals",
                    "Eat in calm, peaceful environment"
                ]
            },
            'pitta': {
                'foods_to_favor': [
                    "Cooling grains: basmati rice, barley, oats",
                    "Sweet, astringent fruits: grapes, pears, melons",
                    "Leafy greens and cooling vegetables",
                    "Cooling oils: coconut, olive, sunflower",
                    "Cooling spices: coriander, fennel, mint",
                    "Fresh dairy: milk, butter, fresh cheese",
                    "Sweet nuts: almonds, coconut"
                ],
                'foods_to_avoid': [
                    "Spicy, hot foods: chili, garlic, onions",
                    "Sour foods: citrus, tomatoes, vinegar",
                    "Salty foods: pickles, processed foods",
                    "Red meat and fried foods",
                    "Alcohol and caffeine",
                    "Fermented foods in excess"
                ],
                'meal_timing': [
                    "Never skip meals - eat regularly",
                    "Largest meal at midday when digestion is strongest",
                    "Avoid eating when angry or stressed",
                    "Eat in cool, pleasant environment",
                    "Drink cool (not ice-cold) water"
                ]
            },
            'kapha': {
                'foods_to_favor': [
                    "Light grains: millet, buckwheat, quinoa",
                    "Astringent fruits: apples, pears, pomegranates",
                    "Pungent vegetables: radish, onions, garlic",
                    "Warming spices: ginger, black pepper, turmeric",
                    "Light proteins: legumes, white fish",
                    "Honey (in moderation)",
                    "Herbal teas: ginger, cinnamon, clove"
                ],
                'foods_to_avoid': [
                    "Heavy, oily foods: fried foods, nuts",
                    "Sweet foods: sugar, desserts, sweet fruits",
                    "Dairy products: milk, cheese, yogurt",
                    "Cold foods and drinks",
                    "Excessive salt",
                    "Wheat and heavy grains"
                ],
                'meal_timing': [
                    "Light breakfast or skip if not hungry",
                    "Substantial lunch around noon",
                    "Light, early dinner (before 7 PM)",
                    "Avoid snacking between meals",
                    "Fast occasionally to reset digestion"
                ]
            }
        }
        
        return diet_plans.get(dominant.lower(), diet_plans['vata'])
    
    def get_disease_predictions(self, dominant, scores, data):
        """Predict potential health risks based on dosha imbalance"""
        disease_risks = {
            'vata': {
                'primary_risks': [
                    "Anxiety and nervous system disorders",
                    "Insomnia and sleep disturbances",
                    "Digestive issues (gas, bloating, constipation)",
                    "Joint pain and arthritis",
                    "Dry skin conditions and eczema",
                    "Irregular menstruation",
                    "Chronic fatigue syndrome"
                ],
                'secondary_risks': [
                    "Osteoporosis",
                    "Irritable bowel syndrome",
                    "Chronic pain conditions",
                    "Depression and mood swings"
                ]
            },
            'pitta': {
                'primary_risks': [
                    "Acid reflux and peptic ulcers",
                    "Inflammatory skin conditions (acne, rashes)",
                    "Liver and gallbladder disorders",
                    "Hypertension and heart disease",
                    "Inflammatory bowel disease",
                    "Migraines and headaches",
                    "Anger management issues"
                ],
                'secondary_risks': [
                    "Diabetes mellitus",
                    "Autoimmune disorders",
                    "Eye problems",
                    "Premature graying and hair loss"
                ]
            },
            'kapha': {
                'primary_risks': [
                    "Obesity and weight gain",
                    "Type 2 diabetes",
                    "Respiratory congestion and asthma",
                    "High cholesterol",
                    "Sluggish metabolism",
                    "Depression and lethargy",
                    "Sinus congestion and allergies"
                ],
                'secondary_risks': [
                    "Hypothyroidism",
                    "Sleep apnea",
                    "Lymphatic congestion",
                    "Kidney stones"
                ]
            }
        }
        
        risks = disease_risks.get(dominant.lower(), disease_risks['vata'])
        
        # Add specific risks based on symptoms
        additional_risks = []
        if data.get('stress') == 'high':
            additional_risks.append("Stress-related cardiovascular issues")
        if data.get('sleep') in ['poor', 'very_poor']:
            additional_risks.append("Immune system weakness due to poor sleep")
        if data.get('digestion') == 'acidity':
            additional_risks.append("Gastroesophageal reflux disease (GERD)")
        
        return {
            'primary_risks': risks['primary_risks'][:5],
            'secondary_risks': risks['secondary_risks'][:3],
            'additional_risks': additional_risks,
            'prevention_note': "These are potential risks based on Ayurvedic principles. Early intervention through lifestyle changes can prevent most conditions."
        }
    
    def get_lifestyle_tips(self, dominant, data):
        """Get specific lifestyle recommendations"""
        lifestyle_tips = {
            'vata': {
                'daily_routine': [
                    "Wake up at 6 AM consistently",
                    "Practice 10 minutes of meditation",
                    "Gentle yoga or stretching",
                    "Regular meal times",
                    "Oil massage before bath",
                    "Sleep by 10 PM"
                ],
                'seasonal_care': [
                    "Extra care during autumn and winter",
                    "Stay warm and avoid cold winds",
                    "Increase oil consumption",
                    "Practice grounding activities"
                ],
                'exercise': [
                    "Gentle yoga and tai chi",
                    "Walking in nature",
                    "Swimming in warm water",
                    "Avoid excessive cardio"
                ]
            },
            'pitta': {
                'daily_routine': [
                    "Wake up at 5:30 AM",
                    "Cool shower or bath",
                    "Moderate exercise in morning",
                    "Avoid midday sun",
                    "Practice cooling pranayama",
                    "Sleep by 10:30 PM"
                ],
                'seasonal_care': [
                    "Extra care during summer",
                    "Stay cool and hydrated",
                    "Avoid excessive heat",
                    "Practice patience and tolerance"
                ],
                'exercise': [
                    "Swimming and water sports",
                    "Yoga in cool environment",
                    "Moderate cardio",
                    "Avoid competitive sports"
                ]
            },
            'kapha': {
                'daily_routine': [
                    "Wake up at 5 AM",
                    "Vigorous exercise",
                    "Dry brushing before bath",
                    "Light breakfast",
                    "Stay active throughout day",
                    "Sleep by 10 PM"
                ],
                'seasonal_care': [
                    "Extra care during spring",
                    "Increase activity levels",
                    "Reduce heavy foods",
                    "Practice energizing activities"
                ],
                'exercise': [
                    "High-intensity cardio",
                    "Weight training",
                    "Running and cycling",
                    "Dynamic yoga styles"
                ]
            }
        }
        
        return lifestyle_tips.get(dominant.lower(), lifestyle_tips['vata'])