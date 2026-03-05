"""
FastAPI Service for Dosha Assessment Model
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import pickle
import numpy as np
from typing import Optional
import os

app = FastAPI(title="Tridosha Assessment API", version="1.0.0")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load model
MODEL_PATH = "dosha_assessment_model.pkl"
model_data = None

try:
    if os.path.exists(MODEL_PATH):
        with open(MODEL_PATH, 'rb') as f:
            model_data = pickle.load(f)
        print("✓ Model loaded successfully")
except Exception as e:
    print(f"⚠ Model loading failed: {e}")

class AssessmentInput(BaseModel):
    age: int
    gender: str
    sleep: str
    appetite: str
    stress: str
    digestion: str
    skin: str
    temperature: str
    food: str

class AssessmentOutput(BaseModel):
    vata_confidence: float
    pitta_confidence: float
    kapha_confidence: float
    dominant_dosha: str
    predicted_severity: str
    recommendations: list

@app.get("/")
def root():
    return {
        "service": "Tridosha Assessment API",
        "status": "running",
        "model_loaded": model_data is not None
    }

@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "model_status": "loaded" if model_data else "not_loaded"
    }

@app.post("/predict", response_model=AssessmentOutput)
def predict_dosha(input_data: AssessmentInput):
    """Predict dosha using ML model"""
    
    if not model_data:
        raise HTTPException(status_code=503, detail="Model not loaded")
    
    try:
        # Prepare features
        features = prepare_features(input_data.dict())
        
        # Get predictions from model
        if isinstance(model_data, dict):
            # Simulated prediction (replace with actual model)
            predictions = simulate_prediction(features)
        else:
            # Actual model prediction
            predictions = model_data.predict_proba(features)[0]
        
        # Process results
        vata_conf = float(predictions[0])
        pitta_conf = float(predictions[1])
        kapha_conf = float(predictions[2])
        
        # Determine dominant
        doshas = {'vata': vata_conf, 'pitta': pitta_conf, 'kapha': kapha_conf}
        dominant = max(doshas, key=doshas.get)
        
        # Determine severity
        max_conf = max(vata_conf, pitta_conf, kapha_conf)
        if max_conf < 0.40:
            severity = 'balanced'
        elif max_conf < 0.55:
            severity = 'mild'
        elif max_conf < 0.70:
            severity = 'moderate'
        else:
            severity = 'severe'
        
        # Get recommendations
        recommendations = get_recommendations(dominant, severity)
        
        return AssessmentOutput(
            vata_confidence=round(vata_conf, 3),
            pitta_confidence=round(pitta_conf, 3),
            kapha_confidence=round(kapha_conf, 3),
            dominant_dosha=dominant.capitalize(),
            predicted_severity=severity,
            recommendations=recommendations
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction error: {str(e)}")

def prepare_features(data):
    """Convert input data to model features"""
    feature_map = {
        'sleep': {'excellent': 0, 'good': 1, 'poor': 2, 'very_poor': 3, 'excessive': 4},
        'appetite': {'regular': 0, 'irregular': 1, 'excessive': 2, 'low': 3},
        'stress': {'low': 0, 'moderate': 1, 'high': 2},
        'digestion': {'normal': 0, 'constipation': 1, 'acidity': 2, 'gas': 3, 'slow': 4},
        'skin': {'normal': 0, 'dry': 1, 'oily': 2, 'sensitive': 3},
        'temperature': {'normal': 0, 'cold': 1, 'hot': 2},
        'food': {'balanced': 0, 'spicy': 1, 'sweet': 2, 'bitter': 3}
    }
    
    features = [
        feature_map['sleep'].get(data.get('sleep'), 0),
        feature_map['appetite'].get(data.get('appetite'), 0),
        feature_map['stress'].get(data.get('stress'), 0),
        feature_map['digestion'].get(data.get('digestion'), 0),
        feature_map['skin'].get(data.get('skin'), 0),
        feature_map['temperature'].get(data.get('temperature'), 0),
        feature_map['food'].get(data.get('food'), 0),
        int(data.get('age', 25)),
        1 if data.get('gender') == 'male' else 0
    ]
    
    return np.array(features).reshape(1, -1)

def simulate_prediction(features):
    """Simulate model prediction (fallback)"""
    sleep, appetite, stress, digestion, skin, temp, food, age, gender = features[0]
    
    vata = 0.33
    pitta = 0.33
    kapha = 0.33
    
    # Stress + Sleep
    if stress >= 1:
        vata += 0.15 * (stress / 2)
    if sleep >= 2:
        vata += 0.18
    elif sleep == 4:
        kapha += 0.15
    
    # Digestion
    if digestion == 1:
        vata += 0.14
    elif digestion == 2:
        pitta += 0.14
    elif digestion == 4:
        kapha += 0.12
    
    # Physical signs
    if skin == 1:
        vata += 0.12
    elif skin == 2:
        kapha += 0.10
    elif skin == 3:
        pitta += 0.12
    
    if temp == 1:
        vata += 0.10
    elif temp == 2:
        pitta += 0.12
    
    # Normalize
    total = vata + pitta + kapha
    return [vata/total, pitta/total, kapha/total]

def get_recommendations(dosha, severity):
    """Get recommendations based on dosha"""
    recs = {
        'vata': [
            'Warm, cooked foods; ghee, nuts',
            'Gentle yoga poses',
            'Nadi Shodhana pranayama',
            'Regular sleep schedule'
        ],
        'pitta': [
            'Cool, fresh foods; cucumber',
            'Cooling yoga poses',
            'Sheetali pranayama',
            'Avoid midday sun'
        ],
        'kapha': [
            'Light, warm, spicy foods',
            'Energizing yoga poses',
            'Kapalabhati pranayama',
            'Wake early, exercise'
        ]
    }
    
    return recs.get(dosha, recs['vata'])

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
