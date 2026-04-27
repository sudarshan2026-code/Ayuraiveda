"""
Test Script for Improved Redness Detection
Verifies that redness ratio calculation is working correctly
"""

import sys
import os
import numpy as np
import cv2

# Set UTF-8 encoding for Windows console
if sys.platform == 'win32':
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
    sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')

print("="*60)
print("TESTING IMPROVED REDNESS DETECTION")
print("="*60)

# Import the engine
from face_analysis_engine import FaceAnalysisEngine

# Initialize engine
engine = FaceAnalysisEngine()
print("\nOK - FaceAnalysisEngine initialized")

# Test redness ratio calculation
print("\n" + "="*60)
print("REDNESS RATIO CALCULATION TESTS")
print("="*60)

print("\nFormula: redness_ratio = R / (G + B + 1)")
print("Threshold: > 0.6 -> Pitta, else -> Kapha")
print()

# Test cases with different RGB combinations
test_cases = [
    # (R, G, B, expected_ratio, expected_dosha, description)
    (200, 100, 100, 200/(100+100+1), "Pitta", "High red, low green/blue"),
    (150, 120, 120, 150/(120+120+1), "Kapha", "Balanced colors"),
    (180, 80, 80, 180/(80+80+1), "Pitta", "Red dominant"),
    (100, 100, 100, 100/(100+100+1), "Kapha", "Equal RGB (gray)"),
    (255, 150, 150, 255/(150+150+1), "Pitta", "Maximum red"),
    (120, 140, 140, 120/(140+140+1), "Kapha", "Green/blue dominant"),
    (160, 100, 120, 160/(100+120+1), "Kapha", "Slightly red"),
    (200, 80, 100, 200/(80+100+1), "Pitta", "Strong red tone"),
]

print("Testing redness ratio with different RGB values:")
print()

for r, g, b, expected_ratio, expected_dosha, description in test_cases:
    # Create test image with specific RGB values
    test_image = np.zeros((100, 100, 3), dtype=np.uint8)
    test_image[:, :] = [b, g, r]  # OpenCV uses BGR
    
    # Extract redness ratio
    redness_ratio = engine.extract_redness(test_image)
    
    # Determine dosha based on ratio
    if redness_ratio > 0.6:
        result_dosha = "Pitta"
    else:
        result_dosha = "Kapha"
    
    # Check if result matches expectation
    status = "OK" if result_dosha == expected_dosha else "FAIL"
    
    print(f"{status} - {description}")
    print(f"     RGB: ({r}, {g}, {b})")
    print(f"     Expected ratio: {expected_ratio:.3f}")
    print(f"     Calculated ratio: {redness_ratio:.3f}")
    print(f"     Expected dosha: {expected_dosha}, Got: {result_dosha}")
    print()

# Test with full feature analysis
print("="*60)
print("FULL FEATURE ANALYSIS TEST")
print("="*60)
print()

# Test case 1: High redness (Pitta expected)
print("Test 1: High redness image (Pitta expected)")
high_red_image = np.zeros((200, 200, 3), dtype=np.uint8)
high_red_image[:, :] = [80, 100, 200]  # BGR: Low blue, medium green, high red

redness_high = engine.extract_redness(high_red_image)
print(f"  RGB: (200, 100, 80)")
print(f"  Redness ratio: {redness_high:.3f}")
print(f"  Expected: > 0.6 (Pitta)")
print(f"  Result: {'Pitta' if redness_high > 0.6 else 'Kapha'}")
print()

# Test case 2: Low redness (Kapha expected)
print("Test 2: Low redness image (Kapha expected)")
low_red_image = np.zeros((200, 200, 3), dtype=np.uint8)
low_red_image[:, :] = [140, 140, 120]  # BGR: High blue/green, lower red

redness_low = engine.extract_redness(low_red_image)
print(f"  RGB: (120, 140, 140)")
print(f"  Redness ratio: {redness_low:.3f}")
print(f"  Expected: <= 0.6 (Kapha)")
print(f"  Result: {'Pitta' if redness_low > 0.6 else 'Kapha'}")
print()

# Test case 3: Neutral (Kapha expected)
print("Test 3: Neutral gray image (Kapha expected)")
neutral_image = np.zeros((200, 200, 3), dtype=np.uint8)
neutral_image[:, :] = [128, 128, 128]  # Equal RGB

redness_neutral = engine.extract_redness(neutral_image)
print(f"  RGB: (128, 128, 128)")
print(f"  Redness ratio: {redness_neutral:.3f}")
print(f"  Expected: <= 0.6 (Kapha)")
print(f"  Result: {'Pitta' if redness_neutral > 0.6 else 'Kapha'}")
print()

# Test scoring integration
print("="*60)
print("SCORING INTEGRATION TEST")
print("="*60)
print()

# Create features with high redness
features_high_red = {
    'brightness': 140,
    'shine': 45.0,
    'redness': 0.8,  # High ratio
    'hsv': {'hue': 15.0, 'saturation': 75.0, 'value': 140.0},
    'face_ratio': 0.82,
    'texture': 350.0
}

scores_high = engine.calculate_dosha_scores(features_high_red)
print("High redness (0.8) scoring:")
print(f"  Vata:  {scores_high['vata']:.1f}%")
print(f"  Pitta: {scores_high['pitta']:.1f}%")
print(f"  Kapha: {scores_high['kapha']:.1f}%")
print(f"  Color component: {scores_high['component_scores']['color']}")
print()

# Create features with low redness
features_low_red = {
    'brightness': 140,
    'shine': 45.0,
    'redness': 0.4,  # Low ratio
    'hsv': {'hue': 15.0, 'saturation': 75.0, 'value': 140.0},
    'face_ratio': 0.82,
    'texture': 350.0
}

scores_low = engine.calculate_dosha_scores(features_low_red)
print("Low redness (0.4) scoring:")
print(f"  Vata:  {scores_low['vata']:.1f}%")
print(f"  Pitta: {scores_low['pitta']:.1f}%")
print(f"  Kapha: {scores_low['kapha']:.1f}%")
print(f"  Color component: {scores_low['component_scores']['color']}")
print()

# Comparison
print("="*60)
print("COMPARISON")
print("="*60)
print()
print("Redness Ratio Impact on Color Component:")
print(f"  High redness (0.8): Pitta +25 points")
print(f"  Low redness (0.4):  Kapha +5 points")
print()
print("This creates a clear distinction between:")
print("  - Warm, inflamed skin (high red ratio) -> Pitta")
print("  - Cool, balanced skin (low red ratio) -> Kapha")
print()

# Summary
print("="*60)
print("TEST SUMMARY")
print("="*60)
print()
print("Redness detection improvements:")
print()
print("OLD METHOD:")
print("  - Used absolute red channel intensity (0-255)")
print("  - Threshold: > 140 for Pitta")
print("  - Problem: Lighting dependent")
print()
print("NEW METHOD:")
print("  - Uses redness ratio: R / (G + B + 1)")
print("  - Threshold: > 0.6 for Pitta")
print("  - Benefit: Lighting independent, relative measure")
print()
print("Scoring:")
print("  - If redness > 0.6: Pitta += 25 points")
print("  - Else: Kapha += 5 points")
print()
print("This provides more accurate detection of warm/red tones")
print("regardless of overall image brightness.")
print()
print("="*60)
print("TESTING COMPLETE")
print("="*60)
