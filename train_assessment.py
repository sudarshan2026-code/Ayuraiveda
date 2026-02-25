"""
Train the ML-Enhanced Health Assessment Engine
Run this script to train the assessment model on PDFs
"""

from ml_assessment_engine import MLTridoshaEngine

def main():
    print("=" * 60)
    print("AyurAI Veda™ - Training Assessment Engine")
    print("=" * 60)
    
    engine = MLTridoshaEngine()
    
    pdf_files = [
        'astang hrdaya.pdf',
    ]
    
    print("\nTraining assessment model on:")
    for pdf in pdf_files:
        print(f"  - {pdf}")
    
    engine.train_from_pdfs(pdf_files)
    
    print("\n" + "=" * 60)
    print("Assessment Model Training Complete!")
    print("=" * 60)
    
    # Test the model
    print("\n--- Testing Assessment Engine ---\n")
    
    test_data = {
        'age': 30,
        'gender': 'male',
        'sleep': 'poor',
        'appetite': 'irregular',
        'stress': 'high',
        'digestion': 'constipation',
        'skin': 'dry',
        'temperature': 'cold',
        'food': 'balanced'
    }
    
    result = engine.analyze(test_data)
    
    print(f"Dominant Dosha: {result['dominant']}")
    print(f"Risk Level: {result['risk']}")
    print(f"\nDosha Scores:")
    print(f"  Vata: {result['scores']['vata']}%")
    print(f"  Pitta: {result['scores']['pitta']}%")
    print(f"  Kapha: {result['scores']['kapha']}%")
    print(f"\nRecommendations:")
    for i, rec in enumerate(result['recommendations'][:5], 1):
        print(f"  {i}. {rec}")
    
    print("\n" + "=" * 60)
    print("Assessment engine is ready!")
    print("=" * 60)

if __name__ == "__main__":
    main()
