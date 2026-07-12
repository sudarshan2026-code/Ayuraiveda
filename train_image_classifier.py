"""
Training Script for Prakriti Image Feature Classifier
Generates high-fidelity synthetic physiological vectors based on classical Ayurvedic guidelines
and trains a scikit-learn RandomForest classifier.
"""

import os
import pickle
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, accuracy_score

def generate_profile(dosha_class, num_samples):
    """
    Generate synthetic feature distributions corresponding to a specific dominant Dosha
    Features order:
    [
        'skin_texture', 'oiliness', 'pigmentation', 'redness', 'brightness',
        'body_frame', 'body_width', 'body_height', 'body_ratio',
        'shoulder_width', 'hip_width', 'torso_length', 'limb_thickness', 'posture'
    ]
    """
    np.random.seed(42 + dosha_class)
    
    # Pre-allocate feature matrix
    X = np.zeros((num_samples, 14))
    
    if dosha_class == 0:  # VATA (Lean, dry, rough, irregular)
        X[:, 0] = np.random.normal(0.75, 0.10, num_samples)  # high skin_texture (rough)
        X[:, 1] = np.random.normal(0.20, 0.08, num_samples)  # low oiliness (dry)
        X[:, 2] = np.random.normal(0.40, 0.12, num_samples)  # pigmentation
        X[:, 3] = np.random.normal(0.30, 0.08, num_samples)  # low redness
        X[:, 4] = np.random.normal(0.35, 0.10, num_samples)  # low brightness
        X[:, 5] = np.random.normal(0.25, 0.08, num_samples)  # low body_frame (lean)
        X[:, 6] = np.random.normal(0.25, 0.08, num_samples)  # low body_width (narrow)
        X[:, 7] = np.random.normal(0.65, 0.12, num_samples)  # height (often tall/slim)
        X[:, 8] = np.random.normal(0.30, 0.08, num_samples)  # body_ratio (angular)
        X[:, 9] = np.random.normal(0.30, 0.08, num_samples)  # shoulder_width
        X[:, 10] = np.random.normal(0.30, 0.08, num_samples) # hip_width
        X[:, 11] = np.random.normal(0.65, 0.10, num_samples) # torso_length
        X[:, 12] = np.random.normal(0.25, 0.08, num_samples) # low limb_thickness (thin joints)
        X[:, 13] = np.random.normal(0.40, 0.12, num_samples) # posture (unstable/mobile)
        
    elif dosha_class == 1:  # PITTA (Moderate, reddish, sharp, warm)
        X[:, 0] = np.random.normal(0.45, 0.10, num_samples)  # moderate skin_texture
        X[:, 1] = np.random.normal(0.50, 0.10, num_samples)  # moderate oiliness
        X[:, 2] = np.random.normal(0.60, 0.12, num_samples)  # pigmentation
        X[:, 3] = np.random.normal(0.78, 0.08, num_samples)  # high redness (flushed/warm)
        X[:, 4] = np.random.normal(0.75, 0.10, num_samples)  # high brightness (radiant)
        X[:, 5] = np.random.normal(0.50, 0.08, num_samples)  # moderate body_frame
        X[:, 6] = np.random.normal(0.50, 0.08, num_samples)  # moderate body_width
        X[:, 7] = np.random.normal(0.55, 0.10, num_samples)  # body_height
        X[:, 8] = np.random.normal(0.55, 0.08, num_samples)  # body_ratio (balanced)
        X[:, 9] = np.random.normal(0.50, 0.08, num_samples)  # shoulder_width
        X[:, 10] = np.random.normal(0.50, 0.08, num_samples) # hip_width
        X[:, 11] = np.random.normal(0.55, 0.10, num_samples) # torso_length
        X[:, 12] = np.random.normal(0.50, 0.08, num_samples) # moderate limb_thickness
        X[:, 13] = np.random.normal(0.65, 0.10, num_samples) # posture (active)
        
    else:  # KAPHA (Heavy, smooth, oily, stable, solid)
        X[:, 0] = np.random.normal(0.20, 0.08, num_samples)  # low skin_texture (smooth/soft)
        X[:, 1] = np.random.normal(0.80, 0.08, num_samples)  # high oiliness
        X[:, 2] = np.random.normal(0.30, 0.10, num_samples)  # even complexion
        X[:, 3] = np.random.normal(0.30, 0.08, num_samples)  # low redness
        X[:, 4] = np.random.normal(0.65, 0.10, num_samples)  # good brightness
        X[:, 5] = np.random.normal(0.78, 0.08, num_samples)  # high body_frame (robust)
        X[:, 6] = np.random.normal(0.78, 0.08, num_samples)  # high body_width (broad)
        X[:, 7] = np.random.normal(0.50, 0.10, num_samples)  # height
        X[:, 8] = np.random.normal(0.80, 0.08, num_samples)  # body_ratio (rounded)
        X[:, 9] = np.random.normal(0.75, 0.08, num_samples)  # shoulder_width
        X[:, 10] = np.random.normal(0.75, 0.08, num_samples) # hip_width
        X[:, 11] = np.random.normal(0.50, 0.10, num_samples) # torso_length
        X[:, 12] = np.random.normal(0.80, 0.08, num_samples) # high limb_thickness (thick joints)
        X[:, 13] = np.random.normal(0.80, 0.08, num_samples) # posture (stable/centered)

    # Bound all features strictly in the range [0.0, 1.0]
    return np.clip(X, 0.0, 1.0)

def main():
    print("=" * 60)
    print("Training Prakriti Image Feature Classifier")
    print("=" * 60)
    
    samples_per_class = 8000
    
    # Generate data
    print("Generating simulated clinical profiles...")
    X_vata = generate_profile(0, samples_per_class)
    X_pitta = generate_profile(1, samples_per_class)
    X_kapha = generate_profile(2, samples_per_class)
    
    X = np.vstack([X_vata, X_pitta, X_kapha])
    y = np.array([0] * samples_per_class + [1] * samples_per_class + [2] * samples_per_class)
    
    # Shuffle and split
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.20, random_state=42, stratify=y)
    
    print(f"Total dataset size: {X.shape[0]} profiles")
    print(f"Training set size: {X_train.shape[0]} profiles")
    print(f"Validation set size: {X_test.shape[0]} profiles")
    
    # Train classifier
    print("\nTraining Random Forest Classifier...")
    model = RandomForestClassifier(
        n_estimators=200,
        max_depth=12,
        min_samples_split=4,
        random_state=42,
        n_jobs=-1
    )
    model.fit(X_train, y_train)
    
    # Evaluate
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    print(f"\nValidation Accuracy: {accuracy * 100:.2f}%")
    
    print("\nClassification Report:")
    print(classification_report(y_test, y_pred, target_names=["Vata", "Pitta", "Kapha"]))
    
    # Save model
    model_path = os.path.join(os.path.dirname(__file__), 'prakriti_image_model.pkl')
    with open(model_path, 'wb') as f:
        pickle.dump(model, f)
        
    print(f"Model successfully saved to: {model_path}")
    print("=" * 60)

if __name__ == "__main__":
    main()
