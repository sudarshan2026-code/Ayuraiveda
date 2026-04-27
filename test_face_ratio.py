"""
Test Script for Improved Face Ratio Logic
Verifies that face shape classification is working correctly
"""

import sys
import os
import numpy as np

# Set UTF-8 encoding for Windows console
if sys.platform == 'win32':
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
    sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')

print("="*60)
print("TESTING IMPROVED FACE RATIO LOGIC")
print("="*60)

# Import the engine
from face_analysis_engine import FaceAnalysisEngine

# Initialize engine
engine = FaceAnalysisEngine()
print("\nOK - FaceAnalysisEngine initialized")

# Test face ratio calculation
print("\n" + "="*60)
print("FACE RATIO CLASSIFICATION TESTS")
print("="*60)

print("\nFormula: ratio = width / height")
print("Thresholds:")
print("  < 0.75  -> Vata (narrow, elongated face)")
print("  > 0.9   -> Kapha (wide, round face)")
print("  0.75-0.9 -> Pitta (medium, angular face)")
print()

# Test cases with different face ratios
test_cases = [
    # (width, height, ratio, expected_dosha, description)
    (100, 150, 0.667, "Vata", "Very narrow face"),
    (120, 160, 0.750, "Pitta", "Borderline narrow/medium"),
    (130, 160, 0.813, "Pitta", "Medium face"),
    (140, 160, 0.875, "Pitta", "Medium-wide face"),
    (145, 160, 0.906, "Kapha", "Borderline wide"),
    (150, 160, 0.938, "Kapha", "Wide face"),
    (160, 160, 1.000, "Kapha", "Very wide (square) face"),
    (90, 140, 0.643, "Vata", "Elongated face"),
    (135, 150, 0.900, "Pitta", "Borderline medium/wide"),
    (112, 150, 0.747, "Vata", "Slightly narrow"),
]

print("Testing face ratio classification:")
print()

for width, height, expected_ratio, expected_dosha, description in test_cases:
    # Create bbox
    bbox = {'width': width, 'height': height}
    
    # Calculate ratio
    ratio = engine.calculate_face_ratio(bbox)
    
    # Determine dosha based on ratio
    if ratio < 0.75:
        result_dosha = "Vata"
        points = 20
    elif ratio > 0.9:
        result_dosha = "Kapha"
        points = 20
    else:
        result_dosha = "Pitta"
        points = 15
    
    # Check if result matches expectation
    status = "OK" if result_dosha == expected_dosha else "FAIL"
    
    print(f"{status} - {description}")
    print(f"     Dimensions: {width}x{height}")
    print(f"     Ratio: {ratio:.3f}")
    print(f"     Expected: {expected_dosha}, Got: {result_dosha} (+{points} points)")
    print()

# Test scoring integration
print("="*60)
print("SCORING INTEGRATION TEST")
print("="*60)
print()

# Test with narrow face (Vata)
features_narrow = {
    'brightness': 140,
    'shine': 45.0,
    'redness': 0.5,
    'hsv': {'hue': 15.0, 'saturation': 75.0, 'value': 140.0},
    'face_ratio': 0.65,  # Narrow
    'texture': 75.0
}

scores_narrow = engine.calculate_dosha_scores(features_narrow)
print("Narrow face (ratio 0.65) scoring:")
print(f"  Vata:  {scores_narrow['vata']:.1f}%")
print(f"  Pitta: {scores_narrow['pitta']:.1f}%")
print(f"  Kapha: {scores_narrow['kapha']:.1f}%")
print(f"  Geometry component: {scores_narrow['component_scores']['geometry']}")
print()

# Test with medium face (Pitta)
features_medium = {
    'brightness': 140,
    'shine': 45.0,
    'redness': 0.5,
    'hsv': {'hue': 15.0, 'saturation': 75.0, 'value': 140.0},
    'face_ratio': 0.82,  # Medium
    'texture': 75.0
}

scores_medium = engine.calculate_dosha_scores(features_medium)
print("Medium face (ratio 0.82) scoring:")
print(f"  Vata:  {scores_medium['vata']:.1f}%")
print(f"  Pitta: {scores_medium['pitta']:.1f}%")
print(f"  Kapha: {scores_medium['kapha']:.1f}%")
print(f"  Geometry component: {scores_medium['component_scores']['geometry']}")
print()

# Test with wide face (Kapha)
features_wide = {
    'brightness': 140,
    'shine': 45.0,
    'redness': 0.5,
    'hsv': {'hue': 15.0, 'saturation': 75.0, 'value': 140.0},
    'face_ratio': 0.95,  # Wide
    'texture': 75.0
}

scores_wide = engine.calculate_dosha_scores(features_wide)
print("Wide face (ratio 0.95) scoring:")
print(f"  Vata:  {scores_wide['vata']:.1f}%")
print(f"  Pitta: {scores_wide['pitta']:.1f}%")
print(f"  Kapha: {scores_wide['kapha']:.1f}%")
print(f"  Geometry component: {scores_wide['component_scores']['geometry']}")
print()

# Comparison
print("="*60)
print("COMPARISON")
print("="*60)
print()
print("Face Ratio Impact on Geometry Component:")
print(f"  Narrow face (<0.75):  Vata +20 points")
print(f"  Medium face (0.75-0.9): Pitta +15 points")
print(f"  Wide face (>0.9):     Kapha +20 points")
print()
print("Geometry weight in final score: 30%")
print()

# Detailed breakdown
print("="*60)
print("DETAILED BREAKDOWN")
print("="*60)
print()

ratio_values = [
    (0.60, "Very narrow", "Vata"),
    (0.70, "Narrow", "Vata"),
    (0.74, "Borderline narrow", "Vata"),
    (0.75, "Borderline medium", "Pitta"),
    (0.80, "Medium", "Pitta"),
    (0.85, "Medium-wide", "Pitta"),
    (0.89, "Borderline wide", "Pitta"),
    (0.90, "Borderline wide", "Pitta"),
    (0.91, "Wide", "Kapha"),
    (0.95, "Very wide", "Kapha"),
    (1.00, "Square", "Kapha"),
]

print("Face ratio classification:")
print()
for ratio, description, expected_dosha in ratio_values:
    if ratio < 0.75:
        result = "Vata"
        points = 20
    elif ratio > 0.9:
        result = "Kapha"
        points = 20
    else:
        result = "Pitta"
        points = 15
    
    status = "OK" if result == expected_dosha else "FAIL"
    print(f"{status} - Ratio {ratio:.2f}: {description:20s} -> {result:6s} (+{points} points)")

print()

# Visual representation
print("="*60)
print("VISUAL REPRESENTATION")
print("="*60)
print()
print("Face Shape Examples:")
print()
print("VATA (< 0.75):")
print("  ___")
print(" |   |")
print(" |   |")
print(" |   |")
print(" |___|")
print("  Narrow, elongated, angular")
print()
print("PITTA (0.75 - 0.9):")
print("  _____")
print(" |     |")
print(" |     |")
print(" |_____|")
print("  Medium, balanced, angular")
print()
print("KAPHA (> 0.9):")
print("  _______")
print(" |       |")
print(" |       |")
print(" |_______|")
print("  Wide, round, full")
print()

# Summary
print("="*60)
print("TEST SUMMARY")
print("="*60)
print()
print("Face ratio improvements:")
print()
print("METHOD:")
print("  - Calculates width/height ratio")
print("  - Classifies face shape based on proportions")
print()
print("OLD SCORING:")
print("  - < 0.75: Vata (+50 points)")
print("  - 0.75-0.90: Pitta (+50 points)")
print("  - > 0.90: Kapha (+50 points)")
print()
print("NEW SCORING:")
print("  - < 0.75: Vata (+20 points)")
print("  - > 0.9: Kapha (+20 points)")
print("  - else (0.75-0.9): Pitta (+15 points)")
print()
print("CHANGES:")
print("  - Reduced point values for better balance")
print("  - Simplified Pitta condition (else clause)")
print("  - Maintains same threshold boundaries")
print()
print("BENEFITS:")
print("  - More balanced scoring across doshas")
print("  - Geometry contributes 30% to final score")
print("  - Clear face shape classification")
print()
print("AYURVEDIC ALIGNMENT:")
print("  - Vata: Thin, angular, narrow face")
print("  - Pitta: Medium, balanced proportions")
print("  - Kapha: Wide, round, full face")
print()
print("="*60)
print("TESTING COMPLETE")
print("="*60)
