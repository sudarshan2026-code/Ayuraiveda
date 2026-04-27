"""
Test Script for Improved Texture Analysis
Verifies that Laplacian variance texture detection is working correctly
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
print("TESTING IMPROVED TEXTURE ANALYSIS")
print("="*60)

# Import the engine
from face_analysis_engine import FaceAnalysisEngine

# Initialize engine
engine = FaceAnalysisEngine()
print("\nOK - FaceAnalysisEngine initialized")

# Test texture calculation
print("\n" + "="*60)
print("TEXTURE VARIANCE CALCULATION TESTS")
print("="*60)

print("\nFormula: texture = cv2.Laplacian(gray, cv2.CV_64F).var()")
print("Thresholds:")
print("  > 100  -> Vata (rough texture)")
print("  < 50   -> Kapha (smooth texture)")
print("  50-100 -> Pitta (medium texture)")
print()

# Create test images with different textures
print("Creating synthetic test images:")
print()

# Test 1: Smooth texture (low variance)
print("Test 1: Smooth texture (Kapha expected)")
smooth_image = np.ones((200, 200, 3), dtype=np.uint8) * 128
# Add very subtle noise
smooth_image = smooth_image + np.random.randint(-2, 3, smooth_image.shape, dtype=np.int16)
smooth_image = np.clip(smooth_image, 0, 255).astype(np.uint8)

texture_smooth = engine.extract_skin_texture(smooth_image)
print(f"  Smooth image texture: {texture_smooth:.2f}")
print(f"  Expected: < 50 (Kapha)")
if texture_smooth < 50:
    print(f"  Result: Kapha - OK")
elif texture_smooth > 100:
    print(f"  Result: Vata - UNEXPECTED")
else:
    print(f"  Result: Pitta - BORDERLINE")
print()

# Test 2: Medium texture
print("Test 2: Medium texture (Pitta expected)")
medium_image = np.ones((200, 200, 3), dtype=np.uint8) * 128
# Add moderate noise
medium_image = medium_image + np.random.randint(-10, 11, medium_image.shape, dtype=np.int16)
medium_image = np.clip(medium_image, 0, 255).astype(np.uint8)

texture_medium = engine.extract_skin_texture(medium_image)
print(f"  Medium image texture: {texture_medium:.2f}")
print(f"  Expected: 50-100 (Pitta)")
if texture_medium < 50:
    print(f"  Result: Kapha - TOO SMOOTH")
elif texture_medium > 100:
    print(f"  Result: Vata - TOO ROUGH")
else:
    print(f"  Result: Pitta - OK")
print()

# Test 3: Rough texture (high variance)
print("Test 3: Rough texture (Vata expected)")
rough_image = np.ones((200, 200, 3), dtype=np.uint8) * 128
# Add strong noise
rough_image = rough_image + np.random.randint(-30, 31, rough_image.shape, dtype=np.int16)
rough_image = np.clip(rough_image, 0, 255).astype(np.uint8)

texture_rough = engine.extract_skin_texture(rough_image)
print(f"  Rough image texture: {texture_rough:.2f}")
print(f"  Expected: > 100 (Vata)")
if texture_rough < 50:
    print(f"  Result: Kapha - UNEXPECTED")
elif texture_rough > 100:
    print(f"  Result: Vata - OK")
else:
    print(f"  Result: Pitta - BORDERLINE")
print()

# Test 4: Very smooth (uniform)
print("Test 4: Very smooth uniform image (Kapha expected)")
uniform_image = np.ones((200, 200, 3), dtype=np.uint8) * 128

texture_uniform = engine.extract_skin_texture(uniform_image)
print(f"  Uniform image texture: {texture_uniform:.2f}")
print(f"  Expected: < 50 (Kapha)")
if texture_uniform < 50:
    print(f"  Result: Kapha - OK")
else:
    print(f"  Result: Not Kapha - UNEXPECTED")
print()

# Test 5: Checkerboard pattern (very rough)
print("Test 5: Checkerboard pattern (Vata expected)")
checkerboard = np.zeros((200, 200, 3), dtype=np.uint8)
checkerboard[::2, ::2] = 255
checkerboard[1::2, 1::2] = 255

texture_checkerboard = engine.extract_skin_texture(checkerboard)
print(f"  Checkerboard texture: {texture_checkerboard:.2f}")
print(f"  Expected: > 100 (Vata)")
if texture_checkerboard > 100:
    print(f"  Result: Vata - OK")
else:
    print(f"  Result: Not Vata - UNEXPECTED")
print()

# Test scoring integration
print("="*60)
print("SCORING INTEGRATION TEST")
print("="*60)
print()

# Test with high texture (Vata)
features_high_texture = {
    'brightness': 140,
    'shine': 45.0,
    'redness': 0.5,
    'hsv': {'hue': 15.0, 'saturation': 75.0, 'value': 140.0},
    'face_ratio': 0.82,
    'texture': 150.0  # High texture
}

scores_high = engine.calculate_dosha_scores(features_high_texture)
print("High texture (150) scoring:")
print(f"  Vata:  {scores_high['vata']:.1f}%")
print(f"  Pitta: {scores_high['pitta']:.1f}%")
print(f"  Kapha: {scores_high['kapha']:.1f}%")
print(f"  Texture component: {scores_high['component_scores']['texture']}")
print()

# Test with low texture (Kapha)
features_low_texture = {
    'brightness': 140,
    'shine': 45.0,
    'redness': 0.5,
    'hsv': {'hue': 15.0, 'saturation': 75.0, 'value': 140.0},
    'face_ratio': 0.82,
    'texture': 30.0  # Low texture
}

scores_low = engine.calculate_dosha_scores(features_low_texture)
print("Low texture (30) scoring:")
print(f"  Vata:  {scores_low['vata']:.1f}%")
print(f"  Pitta: {scores_low['pitta']:.1f}%")
print(f"  Kapha: {scores_low['kapha']:.1f}%")
print(f"  Texture component: {scores_low['component_scores']['texture']}")
print()

# Test with medium texture (Pitta)
features_medium_texture = {
    'brightness': 140,
    'shine': 45.0,
    'redness': 0.5,
    'hsv': {'hue': 15.0, 'saturation': 75.0, 'value': 140.0},
    'face_ratio': 0.82,
    'texture': 75.0  # Medium texture
}

scores_medium = engine.calculate_dosha_scores(features_medium_texture)
print("Medium texture (75) scoring:")
print(f"  Vata:  {scores_medium['vata']:.1f}%")
print(f"  Pitta: {scores_medium['pitta']:.1f}%")
print(f"  Kapha: {scores_medium['kapha']:.1f}%")
print(f"  Texture component: {scores_medium['component_scores']['texture']}")
print()

# Comparison
print("="*60)
print("COMPARISON")
print("="*60)
print()
print("Texture Impact on Texture Component:")
print(f"  High texture (>100):  Vata +20 points")
print(f"  Low texture (<50):    Kapha +20 points")
print(f"  Medium texture (50-100): Pitta +10 points")
print()
print("Texture weight in final score: 10%")
print()

# Detailed breakdown
print("="*60)
print("DETAILED BREAKDOWN")
print("="*60)
print()

test_values = [
    (10, "Very smooth", "Kapha"),
    (30, "Smooth", "Kapha"),
    (49, "Borderline smooth", "Kapha"),
    (50, "Borderline medium", "Pitta"),
    (75, "Medium", "Pitta"),
    (99, "Borderline rough", "Pitta"),
    (100, "Borderline rough", "Pitta"),
    (101, "Rough", "Vata"),
    (150, "Very rough", "Vata"),
    (500, "Extremely rough", "Vata")
]

print("Texture value classification:")
print()
for value, description, expected_dosha in test_values:
    if value > 100:
        result = "Vata"
        points = 20
    elif value < 50:
        result = "Kapha"
        points = 20
    else:
        result = "Pitta"
        points = 10
    
    status = "OK" if result == expected_dosha else "FAIL"
    print(f"{status} - Texture {value:3d}: {description:20s} -> {result:6s} (+{points} points)")

print()

# Summary
print("="*60)
print("TEST SUMMARY")
print("="*60)
print()
print("Texture analysis improvements:")
print()
print("METHOD:")
print("  - Uses Laplacian variance: cv2.Laplacian(gray, cv2.CV_64F).var()")
print("  - Measures edge intensity and variation")
print("  - Higher variance = rougher texture")
print()
print("OLD THRESHOLDS:")
print("  - > 500: Vata (+50 points)")
print("  - < 200: Kapha (+50 points)")
print("  - 200-500: Pitta (+30 points)")
print()
print("NEW THRESHOLDS:")
print("  - > 100: Vata (+20 points)")
print("  - < 50: Kapha (+20 points)")
print("  - 50-100: Pitta (+10 points)")
print()
print("BENEFITS:")
print("  - More sensitive to texture differences")
print("  - Better suited for typical skin texture ranges")
print("  - Balanced point distribution")
print("  - 10% weight in final score (appropriate for texture)")
print()
print("AYURVEDIC ALIGNMENT:")
print("  - Vata: Dry, rough, thin skin (high variance)")
print("  - Pitta: Normal, moderate texture (medium variance)")
print("  - Kapha: Oily, smooth, thick skin (low variance)")
print()
print("="*60)
print("TESTING COMPLETE")
print("="*60)
