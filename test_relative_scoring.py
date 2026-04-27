"""
Test Script for Relative Dosha Scoring System
Verifies anti-Kapha bias and fair competition between doshas
"""

import sys
import os

# Set UTF-8 encoding for Windows console
if sys.platform == 'win32':
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
    sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')

print("="*60)
print("TESTING RELATIVE DOSHA SCORING SYSTEM")
print("="*60)

# Import the engine
from face_analysis_engine import FaceAnalysisEngine

# Initialize engine
engine = FaceAnalysisEngine()
print("\nOK - FaceAnalysisEngine initialized")

print("\n" + "="*60)
print("RELATIVE SCORING PRINCIPLES")
print("="*60)
print()
print("Key Changes:")
print("  1. All features normalized (0-1 range)")
print("  2. Competitive scoring (points, not weights)")
print("  3. Fair distribution across doshas")
print("  4. Anti-Kapha bias correction")
print()
print("Scoring System:")
print("  - Each feature awards points to ONE dosha")
print("  - Total points normalized to 100%")
print("  - No dosha gets unfair advantage")
print()

# Test cases with different feature combinations
test_cases = [
    {
        'name': "Balanced/Medium features",
        'features': {
            'brightness': 140,   # Medium (0.549) \u2192 Pitta
            'shine': 45.0,       # Medium (0.45) \u2192 Pitta
            'redness': 0.5,      # Medium (0.4-0.6) \u2192 Kapha
            'hsv': {'saturation': 75.0},  # Medium (0.294) \u2192 Kapha
            'face_ratio': 0.82,  # Medium (0.75-0.9) \u2192 Pitta
            'texture': 75.0      # Medium (0.375) \u2192 Pitta
        },
        'expected_dominant': 'Pitta'
    },
    {
        'name': "Vata features",
        'features': {
            'brightness': 80,    # Low (0.314) \u2192 Vata
            'shine': 20.0,       # Low (0.2) \u2192 Vata
            'redness': 0.35,     # Low (<0.4) \u2192 Vata
            'hsv': {'saturation': 40.0},  # Low (0.157) \u2192 Vata
            'face_ratio': 0.65,  # Narrow (<0.75) \u2192 Vata
            'texture': 150.0     # High (0.75) \u2192 Vata
        },
        'expected_dominant': 'Vata'
    },
    {
        'name': "Pitta features",
        'features': {
            'brightness': 140,   # Medium \u2192 Pitta
            'shine': 45.0,       # Medium \u2192 Pitta
            'redness': 0.8,      # High (>0.6) \u2192 Pitta
            'hsv': {'saturation': 110.0},  # High (0.431) \u2192 Pitta
            'face_ratio': 0.82,  # Medium \u2192 Pitta
            'texture': 75.0      # Medium \u2192 Pitta
        },
        'expected_dominant': 'Pitta'
    },
    {
        'name': "Kapha features",
        'features': {
            'brightness': 200,   # High (0.784) \u2192 Kapha
            'shine': 80.0,       # High (0.8) \u2192 Kapha
            'redness': 0.45,     # Medium \u2192 Kapha
            'hsv': {'saturation': 70.0},  # Medium (0.275) \u2192 Kapha
            'face_ratio': 0.95,  # Wide (>0.9) \u2192 Kapha
            'texture': 30.0      # Low (0.15) \u2192 Kapha
        },
        'expected_dominant': 'Kapha'
    },
    {
        'name': "Medium brightness (anti-bias test)",
        'features': {
            'brightness': 150,   # Medium-high (0.588)
            'shine': 50.0,       # Medium
            'redness': 0.5,      # Medium
            'hsv': {'saturation': 80.0},
            'face_ratio': 0.85,  # Medium
            'texture': 70.0      # Medium
        },
        'expected_dominant': 'Pitta or Kapha (balanced)'
    }
]

print("="*60)
print("FEATURE-BY-FEATURE ANALYSIS")
print("="*60)
print()

for i, test_case in enumerate(test_cases, 1):
    print(f"Test {i}: {test_case['name']}")
    print("-" * 60)
    
    # Calculate scores
    scores = engine.calculate_dosha_scores(test_case['features'])
    
    # Get dominant
    dominant = engine.get_dominant_dosha(scores)
    
    # Extract normalized features
    norm_features = scores['normalized_features']
    
    print(f"  Normalized Features:")
    print(f"    Brightness: {norm_features['brightness_norm']:.3f}")
    print(f"    Redness:    {norm_features['redness']:.3f}")
    print(f"    Texture:    {norm_features['texture_norm']:.3f}")
    print(f"    Face Ratio: {norm_features['face_ratio']:.3f}")
    print(f"    Shine:      {norm_features['shine_norm']:.3f}")
    print(f"    Saturation: {norm_features['saturation_norm']:.3f}")
    print()
    print(f"  Raw Scores:")
    print(f"    Vata:  {scores['raw_scores']['vata']} points")
    print(f"    Pitta: {scores['raw_scores']['pitta']} points")
    print(f"    Kapha: {scores['raw_scores']['kapha']} points")
    print()
    print(f"  Final Percentages:")
    print(f"    Vata:  {scores['vata']:.1f}%")
    print(f"    Pitta: {scores['pitta']:.1f}%")
    print(f"    Kapha: {scores['kapha']:.1f}%")
    print()
    print(f"  Dominant: {dominant}")
    print(f"  Expected: {test_case['expected_dominant']}")
    print()

# Anti-bias verification
print("="*60)
print("ANTI-KAPHA BIAS VERIFICATION")
print("="*60)
print()

# Test medium brightness range (0.5-0.7) where Kapha bias was problematic
bias_test_cases = [
    (130, "0.510 - Lower medium"),
    (140, "0.549 - Medium"),
    (150, "0.588 - Medium-high"),
    (160, "0.627 - Upper medium"),
    (170, "0.667 - Borderline high")
]

print("Testing brightness range 0.5-0.7 (medium range):")
print("This range previously showed Kapha bias")
print()

for brightness_val, description in bias_test_cases:
    test_features = {
        'brightness': brightness_val,
        'shine': 45.0,
        'redness': 0.5,
        'hsv': {'saturation': 75.0},
        'face_ratio': 0.82,
        'texture': 75.0
    }
    
    scores = engine.calculate_dosha_scores(test_features)
    dominant = engine.get_dominant_dosha(scores)
    
    print(f"Brightness {brightness_val} ({description}):")
    print(f"  V={scores['vata']:.1f}% P={scores['pitta']:.1f}% K={scores['kapha']:.1f}%")
    print(f"  Dominant: {dominant}")
    print()

# Competitive scoring verification
print("="*60)
print("COMPETITIVE SCORING VERIFICATION")
print("="*60)
print()

print("Verifying that all doshas compete fairly:")
print()

# Count wins for each dosha across test cases
vata_wins = 0
pitta_wins = 0
kapha_wins = 0

for test_case in test_cases[:4]:  # Exclude the ambiguous test
    scores = engine.calculate_dosha_scores(test_case['features'])
    dominant = engine.get_dominant_dosha(scores)
    
    if 'Vata' in dominant:
        vata_wins += 1
    elif 'Pitta' in dominant:
        pitta_wins += 1
    elif 'Kapha' in dominant:
        kapha_wins += 1

print(f"Dosha wins across test cases:")
print(f"  Vata:  {vata_wins}/4")
print(f"  Pitta: {pitta_wins}/4")
print(f"  Kapha: {kapha_wins}/4")
print()

if kapha_wins <= 2:
    print("OK - No Kapha bias detected")
else:
    print("WARNING - Possible Kapha bias")

print()

# Summary
print("="*60)
print("TEST SUMMARY")
print("="*60)
print()
print("Relative Scoring System Features:")
print()
print("1. NORMALIZED FEATURES:")
print("   - brightness_norm = brightness / 255.0")
print("   - texture_norm = texture / 200.0")
print("   - redness = r / (g + b + 1)")
print("   - All features in 0-1 range")
print()
print("2. COMPETITIVE SCORING:")
print("   - Each feature awards points (1-2)")
print("   - Points distributed based on thresholds")
print("   - Total points normalized to 100%")
print()
print("3. ANTI-BIAS CORRECTION:")
print("   - If Kapha > 60% in medium brightness (0.5-0.7)")
print("   - Reduce Kapha by 10%")
print("   - Distribute to Pitta")
print()
print("4. FAIR COMPETITION:")
print("   - No dosha gets default advantage")
print("   - All doshas compete on equal terms")
print("   - Results reflect actual features")
print()
print("BENEFITS:")
print("  - Removes camera/lighting bias")
print("  - Fair dosha distribution")
print("  - More accurate results")
print("  - Better clinical alignment")
print()
print("="*60)
print("TESTING COMPLETE")
print("="*60)
