"""
Add this route to api/index.py to integrate ML pipeline
"""

@app.route('/analyze-ml-face', methods=['POST'])
def analyze_ml_face():
    """ML-based face analysis using feature extraction pipeline"""
    try:
        import sys
        import os
        sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)) + '/..')
        
        from dosha_pipeline import DoshaAnalysisPipeline
        import numpy as np
        
        data = request.json
        image_data = data.get('image')
        user_data = data.get('user_data', {})
        
        if not image_data:
            return jsonify({'success': False, 'error': 'No image provided'})
        
        # Initialize pipeline
        pipeline = DoshaAnalysisPipeline()
        
        # Analyze image
        result = pipeline.analyze_image(image_data, input_type='base64', include_metadata=True)
        
        if not result['success']:
            return jsonify(result)
        
        # Convert numpy types to Python native types
        def convert_to_native(obj):
            if isinstance(obj, np.integer):
                return int(obj)
            elif isinstance(obj, np.floating):
                return float(obj)
            elif isinstance(obj, np.ndarray):
                return obj.tolist()
            elif isinstance(obj, dict):
                return {key: convert_to_native(value) for key, value in obj.items()}
            elif isinstance(obj, list):
                return [convert_to_native(item) for item in obj]
            return obj
        
        result = convert_to_native(result)
        result['user_data'] = user_data
        result['analysis_type'] = 'ML-Based Feature Extraction Pipeline'
        
        # Format for compatibility with existing UI
        formatted_result = {
            'success': True,
            'dominant': result['dominant_dosha'],
            'scores': {
                'vata': result['dosha_percentages']['vata'],
                'pitta': result['dosha_percentages']['pitta'],
                'kapha': result['dosha_percentages']['kapha']
            },
            'explanation': result['explanation']['summary'],
            'features': result.get('features', {}),
            'metadata': result.get('metadata', {}),
            'recommendations': result['recommendations']['diet'][:3] + result['recommendations']['lifestyle'][:2],
            'diet_suggestions': {
                'foods_to_favor': result['recommendations']['diet'][:4],
                'foods_to_avoid': [],
                'meal_timing': []
            },
            'lifestyle_tips': {
                'daily_routine': result['recommendations']['lifestyle'][:3],
                'exercise': result['recommendations']['exercise'][:3],
                'seasonal_care': []
            },
            'processing_time': result.get('processing_time', 0),
            'prediction_method': result.get('prediction_method', 'ml_model')
        }
        
        return jsonify(formatted_result)
        
    except Exception as e:
        print(f"ML face analysis error: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({
            'success': False,
            'error': f'ML analysis failed: {str(e)}'
        }), 500
