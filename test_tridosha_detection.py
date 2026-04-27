"""
Test Script for Tridosha Detection Logic
Verifies that balanced constitutions are properly detected
"""

import sys
import os

# Set UTF-8 encoding for Windows console
if sys.platform == 'win32':
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
    sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')

print("="*60)
print("TESTING TRIDOSHA DETECTION LOGIC")
print("="*60)

# Import the engine
from face_analysis_engine import FaceAnalysisEngine

# Initialize engine
engine = FaceAnalysisEngine()
print("\nOK - FaceAnalysisEngine initialized")

print("\n" + "="*60)
print("TRIDOSHA DETECTION FORMULA")
print("="*60)
print()
print("Formula:")
print("  scores = [vata, pitta, kapha]")
print("  if max(scores) - min(scores) < 10:")
print("      result = 'Tridoshic (Balanced)'")
print("  else:")
print("      result = dominant dosha")
print()
print("Threshold: 10% difference")
print()

# Test cases with different score distributions
test_cases = [
    # (vata, pitta, kapha, expected_result, description)
    (33.3, 33.3, 33.4, "Tridoshic (Balanced)", "Perfect balance"),
    (32.0, 34.0, 34.0, "Tridoshic (Balanced)", "Very close (2% diff)"),
    (30.0, 35.0, 35.0, "Tridoshic (Balanced)", "Close (5% diff)"),
    (28.0, 36.0, 36.0, "Tridoshic (Balanced)", "Borderline (8% diff)"),
    (27.0, 36.5, 36.5, "Tridoshic (Balanced)", "Just balanced (9.5% diff)"),
    (26.0, 37.0, 37.0, "Pitta", "Just unbalanced (11% diff)"),
    (25.0, 40.0, 35.0, "Pitta", "Pitta dominant (15% diff)"),
    (50.0, 30.0, 20.0, "Vata", "Clear Vata (30% diff)"),
    (20.0, 55.0, 25.0, "Pitta", "Clear Pitta (35% diff)"),
    (15.0, 25.0, 60.0, "Kapha", "Clear Kapha (45% diff)"),
    (31.0, 33.0, 36.0, "Tridoshic (Balanced)", "Slight Kapha tendency (5% diff)"),
    (35.0, 33.0, 32.0, "Tridoshic (Balanced)", "Slight Vata tendency (3% diff)"),
]

print("Testing tridosha detection with various score distributions:")
print()

for vata, pitta, kapha, expected, description in test_cases:
    # Create scores dict
    scores = {'vata': vata, 'pitta': pitta, 'kapha': kapha}
    
    # Get dominant dosha
    result = engine.get_dominant_dosha(scores)
    
    # Calculate difference
    score_list = [vata, pitta, kapha]
    diff = max(score_list) - min(score_list)
    
    # Check if result matches expectation
    status = "OK" if result == expected else "FAIL"
    
    print(f"{status} - {description}")
    print(f"     Scores: V={vata:.1f}%, P={pitta:.1f}%, K={kapha:.1f}%")
    print(f"     Difference: {diff:.1f}%")
    print(f"     Expected: {expected}")
    print(f"     Got: {result}")
    print()

# Test with full feature analysis
print("="*60)
print("FULL FEATURE ANALYSIS TEST")
print("="*60)
print()

# Test 1: Balanced features (should be tridoshic)
print("Test 1: Balanced features (Tridoshic expected)")
balanced_features = {
    'brightness': 140,   # Medium
    'shine': 45.0,       # Medium
    'redness': 0.5,      # Medium
    'hsv': {'hue': 15.0, 'saturation': 75.0, 'value': 140.0},  # Medium
    'face_ratio': 0.82,  # Medium
    'texture': 75.0      # Medium
}

scores_balanced = engine.calculate_dosha_scores(balanced_features)
dominant_balanced = engine.get_dominant_dosha(scores_balanced)
explanation_balanced = engine.generate_explanation(balanced_features, scores_balanced, dominant_balanced)

print(f"  Scores: V={scores_balanced['vata']:.1f}%, P={scores_balanced['pitta']:.1f}%, K={scores_balanced['kapha']:.1f}%")
print(f"  Difference: {max([scores_balanced['vata'], scores_balanced['pitta'], scores_balanced['kapha']]) - min([scores_balanced['vata'], scores_balanced['pitta'], scores_balanced['kapha']]):.1f}%")
print(f"  Result: {dominant_balanced}")
print(f"  Explanation: {explanation_balanced}")
print()

# Test 2: Vata-dominant features
print("Test 2: Vata-dominant features")
vata_features = {
    'brightness': 80,
    'shine': 20.0,
    'redness': 0.4,
    'hsv': {'hue': 15.0, 'saturation': 40.0, 'value': 80.0},
    'face_ratio': 0.65,
    'texture': 150.0
}

scores_vata = engine.calculate_dosha_scores(vata_features)
dominant_vata = engine.get_dominant_dosha(scores_vata)
explanation_vata = engine.generate_explanation(vata_features, scores_vata, dominant_vata)

print(f"  Scores: V={scores_vata['vata']:.1f}%, P={scores_vata['pitta']:.1f}%, K={scores_vata['kapha']:.1f}%")
print(f"  Difference: {max([scores_vata['vata'], scores_vata['pitta'], scores_vata['kapha']]) - min([scores_vata['vata'], scores_vata['pitta'], scores_vata['kapha']]):.1f}%")
print(f"  Result: {dominant_vata}")
print(f"  Explanation: {explanation_vata}")
print()

# Test 3: Pitta-dominant features
print("Test 3: Pitta-dominant features")
pitta_features = {
    'brightness': 140,
    'shine': 45.0,
    'redness': 0.8,
    'hsv': {'hue': 15.0, 'saturation': 110.0, 'value': 140.0},
    'face_ratio': 0.82,
    'texture': 75.0
}

scores_pitta = engine.calculate_dosha_scores(pitta_features)
dominant_pitta = engine.get_dominant_dosha(scores_pitta)
explanation_pitta = engine.generate_explanation(pitta_features, scores_pitta, dominant_pitta)

print(f"  Scores: V={scores_pitta['vata']:.1f}%, P={scores_pitta['pitta']:.1f}%, K={scores_pitta['kapha']:.1f}%")
print(f"  Difference: {max([scores_pitta['vata'], scores_pitta['pitta'], scores_pitta['kapha']]) - min([scores_pitta['vata'], scores_pitta['pitta'], scores_pitta['kapha']]):.1f}%")
print(f"  Result: {dominant_pitta}")
print(f"  Explanation: {explanation_pitta}")
print()

# Test 4: Kapha-dominant features
print("Test 4: Kapha-dominant features")
kapha_features = {
    'brightness': 200,
    'shine': 80.0,
    'redness': 0.4,
    'hsv': {'hue': 15.0, 'saturation': 70.0, 'value': 200.0},
    'face_ratio': 0.95,
    'texture': 30.0
}

scores_kapha = engine.calculate_dosha_scores(kapha_features)
dominant_kapha = engine.get_dominant_dosha(scores_kapha)
explanation_kapha = engine.generate_explanation(kapha_features, scores_kapha, dominant_kapha)

print(f"  Scores: V={scores_kapha['vata']:.1f}%, P={scores_kapha['pitta']:.1f}%, K={scores_kapha['kapha']:.1f}%")
print(f"  Difference: {max([scores_kapha['vata'], scores_kapha['pitta'], scores_kapha['kapha']]) - min([scores_kapha['vata'], scores_kapha['pitta'], scores_kapha['kapha']]):.1f}%")
print(f"  Result: {dominant_kapha}")
print(f"  Explanation: {explanation_kapha}")
print()

# Visual representation
print("="*60)
print("VISUAL REPRESENTATION")
print("="*60)
print()
print("Score Distribution Examples:")
print()
print("TRIDOSHIC (< 10% difference):")
print("  Vata:  33% ████████████")
print("  Pitta: 34% █████████████")
print("  Kapha: 33% ████████████")
print("  → Balanced constitution")
print()
print("VATA DOMINANT (> 10% difference):")
print("  Vata:  50% ████████████████████")
print("  Pitta: 30% ████████████")
print("  Kapha: 20% ████████")
print("  → Clear Vata dominance")
print()
print("PITTA DOMINANT (> 10% difference):")
print("  Vata:  20% ████████")
print("  Pitta: 55% ██████████████████████")
print("  Kapha: 25% ██████████")
print("  → Clear Pitta dominance")
print()
print("KAPHA DOMINANT (> 10% difference):")
print("  Vata:  15% ██████")
print("  Pitta: 25% ██████████")
print("  Kapha: 60% ████████████████████████")
print("  → Clear Kapha dominance")
print()

# Summary
print("="*60)
print("TEST SUMMARY")
print("="*60)
print()
print("Tridosha detection logic:")
print()
print("IMPLEMENTATION:")
print("  1. Create list: scores = [vata, pitta, kapha]")
print("  2. Calculate: difference = max(scores) - min(scores)")
print("  3. If difference < 10%: Return 'Tridoshic (Balanced)'")
print("  4. Else: Return dominant dosha")
print()
print("BENEFITS:")
print("  - Identifies balanced constitutions")
print("  - Prevents false dominance detection")
print("  - Provides accurate classification")
print("  - Aligns with Ayurvedic principles")
print()
print("AYURVEDIC CONTEXT:")
print("  - Tridoshic: Rare, ideal balanced constitution")
print("  - Most people: 1-2 dominant doshas")
print("  - Balance: Key to health and wellness")
print()
print("THRESHOLD RATIONALE:")
print("  - 10% difference allows for minor variations")
print("  - Strict enough to identify true balance")
print("  - Flexible enough to avoid over-classification")
print()
print("="*60)
print("TESTING COMPLETE")
print("="*60)
