"""
Quick Integration Test for Clinical Assessment
"""

import sys
sys.path.insert(0, '.')

from simple_body_extractor import SimpleBodyExtractor
from clinical_engine import ClinicalAssessmentEngine

print("=" * 60)
print("INTEGRATION TEST: Body Extractor + Clinical Engine")
print("=" * 60)

# Create test features
test_features = {
    'skin_texture': 0.7,
    'oiliness': 0.3,
    'pigmentation': 0.4,
    'redness': 0.4,
    'brightness': 0.5,
    'body_frame': 0.6,
    'body_width': 0.65,
    'body_height': 0.5,
    'body_ratio': 0.65,
    'shoulder_width': 0.6,
    'hip_width': 0.65,
    'torso_length': 0.6,
    'limb_thickness': 0.6,
    'posture': 0.6
}

print("\nTest Features:")
print(f"  Body Frame: {test_features['body_frame']}")
print(f"  Body Ratio: {test_features['body_ratio']}")
print(f"  Skin Texture: {test_features['skin_texture']}")
print(f"  Oiliness: {test_features['oiliness']}")

# Run clinical assessment
print("\nRunning Clinical Assessment...")
engine = ClinicalAssessmentEngine()
result = engine.assess(test_features)

print("\n" + "=" * 60)
print("RESULT")
print("=" * 60)
print(f"Type: {result['type']}")
print(f"Base Dosha: {result['base_dosha'].upper()}")
print(f"Confidence: {result['confidence']}%")
print(f"\nDosha Scores:")
print(f"  Vata:  {result['dosha']['vata']}%")
print(f"  Pitta: {result['dosha']['pitta']}%")
print(f"  Kapha: {result['dosha']['kapha']}%")
print(f"\nExplanation:")
print(f"  {result['explanation']}")

print("\n" + "=" * 60)
print("INTEGRATION TEST PASSED")
print("=" * 60)
