"""
Test script for verifying Prakriti Image Model predictions
"""

import os
import pickle
import numpy as np

def main():
    print("=" * 60)
    print("Testing Prakriti Image Classifier Model")
    print("=" * 60)
    
    model_path = os.path.join(os.path.dirname(__file__), 'prakriti_image_model.pkl')
    
    if not os.path.exists(model_path):
        print(f"Error: Model file not found at {model_path}")
        return
        
    with open(model_path, 'rb') as f:
        model = pickle.load(f)
        
    print("Model successfully loaded!")
    
    # Test cases mapping:
    # 0: Vata, 1: Pitta, 2: Kapha
    # Feature vector: [skin_texture, oiliness, pigmentation, redness, brightness, body_frame, body_width, body_height, body_ratio, shoulder_width, hip_width, torso_length, limb_thickness, posture]
    
    test_cases = {
        "Vata Profile": np.array([[0.8, 0.1, 0.4, 0.2, 0.3, 0.2, 0.2, 0.7, 0.25, 0.25, 0.25, 0.7, 0.2, 0.35]]),
        "Pitta Profile": np.array([[0.4, 0.5, 0.6, 0.8, 0.8, 0.5, 0.5, 0.55, 0.5, 0.5, 0.5, 0.5, 0.5, 0.6]]),
        "Kapha Profile": np.array([[0.15, 0.85, 0.25, 0.25, 0.7, 0.8, 0.8, 0.5, 0.85, 0.8, 0.8, 0.55, 0.85, 0.8]])
    }
    
    print("\nRunning predictions:")
    for name, features in test_cases.items():
        # Get probability distributions
        probs = model.predict_proba(features)[0]
        
        # Convert class indices to names
        vata_pct = probs[0] * 100
        pitta_pct = probs[1] * 100
        kapha_pct = probs[2] * 100
        
        # Determine predicted dominant
        classes = ["Vata", "Pitta", "Kapha"]
        predicted = classes[np.argmax(probs)]
        
        print(f"\n{name}:")
        print(f"  Predicted Dominant: {predicted}")
        print(f"  Vata Probability:   {vata_pct:.2f}%")
        print(f"  Pitta Probability:  {pitta_pct:.2f}%")
        print(f"  Kapha Probability:  {kapha_pct:.2f}%")
        
    print("\n" + "=" * 60)

if __name__ == "__main__":
    main()
