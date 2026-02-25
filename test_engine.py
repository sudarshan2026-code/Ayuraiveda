"""
Test script for Tridosha Intelligence Engine™
Run this to verify the AI engine works correctly
"""

from ai_engine import TridoshaIntelligenceEngine

def test_vata_dominant():
    print("\n" + "="*60)
    print("TEST 1: High Vata Imbalance")
    print("="*60)
    
    tie = TridoshaIntelligenceEngine()
    data = {
        'age': '25',
        'gender': 'male',
        'sleep': 'poor',
        'appetite': 'irregular',
        'stress': 'high',
        'digestion': 'constipation',
        'skin': 'dry',
        'temperature': 'cold',
        'food': 'bitter'
    }
    
    result = tie.analyze(data)
    print(f"Dominant Dosha: {result['dominant']}")
    print(f"Risk Level: {result['risk']}")
    print(f"Scores: Vata={result['scores']['vata']}%, Pitta={result['scores']['pitta']}%, Kapha={result['scores']['kapha']}%")
    print(f"\nExpected: Vata dominant [PASS]" if result['dominant'] == 'Vata' else "\nUnexpected result [FAIL]")

def test_pitta_dominant():
    print("\n" + "="*60)
    print("TEST 2: High Pitta Imbalance")
    print("="*60)
    
    tie = TridoshaIntelligenceEngine()
    data = {
        'age': '35',
        'gender': 'female',
        'sleep': 'good',
        'appetite': 'excessive',
        'stress': 'moderate',
        'digestion': 'acidity',
        'skin': 'sensitive',
        'temperature': 'hot',
        'food': 'spicy'
    }
    
    result = tie.analyze(data)
    print(f"Dominant Dosha: {result['dominant']}")
    print(f"Risk Level: {result['risk']}")
    print(f"Scores: Vata={result['scores']['vata']}%, Pitta={result['scores']['pitta']}%, Kapha={result['scores']['kapha']}%")
    print(f"\nExpected: Pitta dominant [PASS]" if result['dominant'] == 'Pitta' else "\nUnexpected result [FAIL]")

def test_kapha_dominant():
    print("\n" + "="*60)
    print("TEST 3: High Kapha Imbalance")
    print("="*60)
    
    tie = TridoshaIntelligenceEngine()
    data = {
        'age': '45',
        'gender': 'male',
        'sleep': 'excessive',
        'appetite': 'low',
        'stress': 'low',
        'digestion': 'slow',
        'skin': 'oily',
        'temperature': 'cold',
        'food': 'sweet'
    }
    
    result = tie.analyze(data)
    print(f"Dominant Dosha: {result['dominant']}")
    print(f"Risk Level: {result['risk']}")
    print(f"Scores: Vata={result['scores']['vata']}%, Pitta={result['scores']['pitta']}%, Kapha={result['scores']['kapha']}%")
    print(f"\nExpected: Kapha dominant [PASS]" if result['dominant'] == 'Kapha' else "\nUnexpected result [FAIL]")
    print("\nRecommendations:")
    for i, rec in enumerate(result['recommendations'][:3], 1):
        print(f"{i}. {rec}")

if __name__ == "__main__":
    print("\nTRIDOSHA INTELLIGENCE ENGINE - TEST SUITE")
    print("Testing AI logic with sample cases...\n")
    
    test_vata_dominant()
    test_pitta_dominant()
    test_kapha_dominant()
    
    print("\n" + "="*60)
    print("All tests completed!")
    print("="*60)
    print("\nIf all tests show expected results, the AI engine is working correctly.")
    print("You can now run: python app.py")
    print("="*60 + "\n")
