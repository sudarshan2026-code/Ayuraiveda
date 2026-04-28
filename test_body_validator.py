"""
Test Body Structure Validator
Verifies that structural misclassifications are corrected before dosha calculation
"""

from body_validator import BodyStructureValidator

def test_validator():
    validator = BodyStructureValidator()
    
    print("=" * 60)
    print("BODY STRUCTURE VALIDATOR TEST")
    print("=" * 60)
    
    # Test Case 1: Lean misclassification with medium limbs
    print("\n[TEST 1] Lean body with medium limbs (should correct to medium)")
    test1 = {
        'body_ratio': 0.30,
        'body_frame': 0.35,
        'limb_thickness': 0.45,  # Medium thickness
        'shoulder_width': 0.52,  # Medium width
        'oiliness': 0.3
    }
    result1 = validator.validate_and_correct(test1)
    print(f"Input: body_ratio={test1['body_ratio']}, limb_thickness={test1['limb_thickness']}")
    print(f"Output: {result1['body_build']}")
    print(f"Vata Eligible: {result1['vata_eligible']}")
    print(f"Base Dosha: {result1['base_dosha']}")
    assert result1['body_build'] == 'medium', "Should correct to medium"
    print("[PASSED]")
    
    # Test Case 2: Lean with high oiliness (should correct to medium-heavy)
    print("\n[TEST 2] Lean body with high oiliness (should correct to medium-heavy)")
    test2 = {
        'body_ratio': 0.32,
        'body_frame': 0.38,
        'limb_thickness': 0.35,
        'shoulder_width': 0.35,
        'oiliness': 0.65  # High oiliness indicates fat
    }
    result2 = validator.validate_and_correct(test2)
    print(f"Input: body_ratio={test2['body_ratio']}, oiliness={test2['oiliness']}")
    print(f"Output: {result2['body_build']}")
    print(f"Vata Eligible: {result2['vata_eligible']}")
    print(f"Base Dosha: {result2['base_dosha']}")
    assert result2['body_build'] == 'medium-heavy', "Should correct to medium-heavy"
    print("[PASSED]")
    
    # Test Case 3: True Vata (lean body)
    print("\n[TEST 3] True Vata - lean body with thin limbs")
    test3 = {
        'body_ratio': 0.30,
        'body_frame': 0.35,
        'limb_thickness': 0.35,
        'shoulder_width': 0.35,
        'oiliness': 0.3
    }
    result3 = validator.validate_and_correct(test3)
    print(f"Body Build: {result3['body_build']}")
    print(f"Vata Eligible: {result3['vata_eligible']}")
    print(f"Base Dosha: {result3['base_dosha']}")
    assert result3['vata_eligible'] == True, "Should be Vata eligible"
    assert result3['base_dosha'] == 'vata', "Should have Vata base"
    print("[PASSED]")
    
    # Test Case 4: Heavy build (Kapha-Pitta base)
    print("\n[TEST 4] Heavy build - should lock to Kapha-Pitta")
    test4 = {
        'body_ratio': 0.55,
        'body_frame': 0.65,
        'limb_thickness': 0.65,
        'shoulder_width': 0.60
    }
    result4 = validator.validate_and_correct(test4)
    print(f"Body Build: {result4['body_build']}")
    print(f"Vata Eligible: {result4['vata_eligible']}")
    print(f"Base Dosha: {result4['base_dosha']}")
    assert result4['vata_eligible'] == False, "Should not be Vata eligible"
    assert result4['base_dosha'] == 'kapha-pitta', "Should have Kapha-Pitta base"
    print("[PASSED]")
    
    # Test Case 5: Medium build
    print("\n[TEST 5] Medium build - should lock to Kapha-Pitta")
    test5 = {
        'body_ratio': 0.42,
        'body_frame': 0.50,
        'limb_thickness': 0.50,
        'shoulder_width': 0.48
    }
    result5 = validator.validate_and_correct(test5)
    print(f"Body Build: {result5['body_build']}")
    print(f"Vata Eligible: {result5['vata_eligible']}")
    print(f"Base Dosha: {result5['base_dosha']}")
    assert result5['vata_eligible'] == False, "Should not be Vata eligible"
    assert result5['base_dosha'] == 'kapha-pitta', "Should have Kapha-Pitta base"
    print("[PASSED]")
    
    print("\n" + "=" * 60)
    print("ALL TESTS PASSED")
    print("Body Structure Validator is working correctly!")
    print("=" * 60)

if __name__ == '__main__':
    test_validator()
