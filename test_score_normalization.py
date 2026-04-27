"""
Verification Test for Score Normalization
Confirms that final scores are properly normalized to 100%
"""

import sys
import os

# Set UTF-8 encoding for Windows console
if sys.platform == 'win32':
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
    sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')

print("="*60)
print("SCORE NORMALIZATION VERIFICATION")
print("="*60)

# Import the engine
from face_analysis_engine import FaceAnalysisEngine

# Initialize engine
engine = FaceAnalysisEngine()
print("\nOK - FaceAnalysisEngine initialized")

print("\n" + "="*60)
print("NORMALIZATION FORMULA VERIFICATION")
print("="*60)
print()
print("Formula:")
print("  total = vata_total + pitta_total + kapha_total")
print("  vata_percent = (vata_total / total) * 100")
print("  pitta_percent = (pitta_total / total) * 100")
print("  kapha_percent = (kapha_total / total) * 100")
print()
print("Expected: vata% + pitta% + kapha% = 100%")
print()

# Test multiple feature combinations
test_cases = [
    {
        'name': "Balanced features",
        'features': {
            'brightness': 140,
            'shine': 45.0,
            'redness': 0.5,
            'hsv': {'hue': 15.0, 'saturation': 75.0, 'value': 140.0},
            'face_ratio': 0.82,
            'texture': 75.0
        }
    },
    {
        'name': "Vata-dominant features",
        'features': {
            'brightness': 80,   # Low (Vata)
            'shine': 20.0,      # Low (Vata)
            'redness': 0.4,     # Low (Kapha)
            'hsv': {'hue': 15.0, 'saturation': 40.0, 'value': 80.0},  # Dull (Vata)
            'face_ratio': 0.65, # Narrow (Vata)
            'texture': 150.0    # Rough (Vata)
        }
    },
    {
        'name': "Pitta-dominant features",
        'features': {
            'brightness': 140,  # Medium (Pitta)
            'shine': 45.0,      # Medium (Pitta)
            'redness': 0.8,     # High (Pitta)
            'hsv': {'hue': 15.0, 'saturation': 110.0, 'value': 140.0},  # Vibrant (Pitta)
            'face_ratio': 0.82, # Medium (Pitta)
            'texture': 75.0     # Medium (Pitta)
        }
    },
    {
        'name': "Kapha-dominant features",
        'features': {
            'brightness': 200,  # High (Kapha)
            'shine': 80.0,      # High (Kapha)
            'redness': 0.4,     # Low (Kapha)
            'hsv': {'hue': 15.0, 'saturation': 70.0, 'value': 200.0},  # Even (Kapha)
            'face_ratio': 0.95, # Wide (Kapha)
            'texture': 30.0     # Smooth (Kapha)
        }
    },
    {
        'name': "Extreme Vata",
        'features': {
            'brightness': 50,
            'shine': 10.0,
            'redness': 0.3,
            'hsv': {'hue': 15.0, 'saturation': 30.0, 'value': 50.0},
            'face_ratio': 0.60,
            'texture': 200.0
        }
    },
    {
        'name': "Extreme Kapha",
        'features': {
            'brightness': 220,
            'shine': 95.0,
            'redness': 0.35,
            'hsv': {'hue': 15.0, 'saturation': 60.0, 'value': 220.0},
            'face_ratio': 1.0,
            'texture': 20.0
        }
    }
]

print("Testing score normalization with various feature combinations:")
print()

all_passed = True

for i, test_case in enumerate(test_cases, 1):
    print(f"Test {i}: {test_case['name']}")
    
    # Calculate scores
    scores = engine.calculate_dosha_scores(test_case['features'])
    
    # Extract percentages
    vata = scores['vata']
    pitta = scores['pitta']
    kapha = scores['kapha']
    
    # Calculate total
    total = vata + pitta + kapha
    
    # Check if normalized (should be 100%)
    is_normalized = abs(total - 100.0) < 0.1  # Allow 0.1% tolerance for rounding
    
    status = "OK" if is_normalized else "FAIL"
    if not is_normalized:
        all_passed = False
    
    print(f"  {status} - Vata: {vata:.1f}%, Pitta: {pitta:.1f}%, Kapha: {kapha:.1f}%")
    print(f"       Total: {total:.1f}% (Expected: 100.0%)")
    print(f"       Raw scores: V={scores['raw_scores']['vata']:.2f}, "
          f"P={scores['raw_scores']['pitta']:.2f}, K={scores['raw_scores']['kapha']:.2f}")
    print()

# Summary
print("="*60)
print("NORMALIZATION VERIFICATION SUMMARY")
print("="*60)
print()

if all_passed:
    print("RESULT: ALL TESTS PASSED")
    print()
    print("Score normalization is working correctly!")
    print("All dosha percentages sum to 100%")
else:
    print("RESULT: SOME TESTS FAILED")
    print()
    print("Score normalization may have issues")

print()
print("="*60)
print("IMPLEMENTATION DETAILS")
print("="*60)
print()
print("Location: calculate_dosha_scores() function")
print("Lines: 336-343 in face_analysis_engine.py")
print()
print("Code:")
print("```python")
print("# Normalize to percentages")
print("total = vata_total + pitta_total + kapha_total")
print("if total > 0:")
print("    vata_percent = (vata_total / total) * 100")
print("    pitta_percent = (pitta_total / total) * 100")
print("    kapha_percent = (kapha_total / total) * 100")
print("else:")
print("    vata_percent = pitta_percent = kapha_percent = 33.33")
print("```")
print()
print("Benefits:")
print("  - Ensures balanced output (always sums to 100%)")
print("  - Allows fair comparison between doshas")
print("  - Handles edge cases (total = 0)")
print("  - Provides percentage-based interpretation")
print()
print("="*60)
print("VERIFICATION COMPLETE")
print("="*60)
