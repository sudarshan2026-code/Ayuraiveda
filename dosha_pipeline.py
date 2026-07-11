"""
Integrated ML Pipeline for Image-Based Dosha Analysis
Combines feature extraction and ML prediction
"""

from feature_extractor import ImageFeatureExtractor
from ml_predictor import DoshaPredictor
from typing import Dict
import time


class DoshaAnalysisPipeline:
    """Complete pipeline: Image → Features → ML Prediction"""
    
    def __init__(self, model_path: str = None):
        """
        Initialize pipeline
        
        Args:
            model_path: Path to trained ML model
        """
        self.feature_extractor = ImageFeatureExtractor()
        self.predictor = DoshaPredictor(model_path)
        
        print("✓ Dosha Analysis Pipeline initialized")
    
    def analyze_image(self, image_input, input_type='base64', include_metadata=True) -> Dict[str, any]:
        """
        Complete analysis pipeline
        
        Args:
            image_input: Image data (base64, path, or array)
            input_type: Type of input ('base64', 'path', 'array')
            include_metadata: Whether to include detailed metadata
            
        Returns:
            Complete analysis results
        """
        start_time = time.time()
        
        # Step 1: Extract features
        print("Step 1/3: Extracting features...")
        feature_result = self.feature_extractor.extract_all_features(image_input, input_type)
        
        if not feature_result['success']:
            return {
                'success': False,
                'error': feature_result['error'],
                'stage': 'feature_extraction'
            }
        
        features = feature_result['features']
        metadata = feature_result['metadata']
        
        # Step 2: Convert to feature vector
        print("Step 2/3: Preparing feature vector...")
        feature_vector = self.feature_extractor.get_feature_vector_array(features)
        
        # Step 3: Predict doshas
        print("Step 3/3: Predicting doshas...")
        prediction = self.predictor.predict(features, feature_vector)
        
        # Step 4: Generate explanation
        explanation = self.predictor.generate_explanation(features, prediction['doshas'])
        
        # Step 5: Get recommendations
        recommendations = self.predictor.get_recommendations(prediction['dominant'])
        
        # Calculate processing time
        processing_time = time.time() - start_time
        
        # Build result
        result = {
            'success': True,
            'dominant_dosha': prediction['dominant'],
            'dosha_percentages': prediction['doshas'],
            'explanation': explanation,
            'recommendations': recommendations,
            'processing_time': round(processing_time, 2)
        }
        
        if include_metadata:
            result['features'] = features
            result['metadata'] = metadata
            result['prediction_method'] = prediction['method']
        
        return result
    
    def analyze_with_progress(self, image_input, input_type='base64', progress_callback=None):
        """
        Analysis with progress updates
        
        Args:
            image_input: Image data
            input_type: Type of input
            progress_callback: Function to call with progress updates
            
        Returns:
            Complete analysis results
        """
        def update_progress(stage, message, percent):
            if progress_callback:
                progress_callback({'stage': stage, 'message': message, 'percent': percent})
        
        start_time = time.time()
        
        # Stage 1: Image validation
        update_progress('validation', 'Validating image...', 10)
        image = self.feature_extractor.load_image(image_input, input_type)
        if image is None:
            return {'success': False, 'error': 'Failed to load image'}
        
        validation = self.feature_extractor.validate_image(image)
        if not validation['valid']:
            return {'success': False, 'error': validation['reason']}
        
        # Stage 2: Preprocessing
        update_progress('preprocessing', 'Enhancing image quality...', 25)
        processed = self.feature_extractor.preprocess_image(image)
        
        # Stage 3: Face detection
        update_progress('detection', 'Detecting facial features...', 40)
        face_region = self.feature_extractor.detect_face_region(processed)
        if face_region is None:
            return {'success': False, 'error': 'No face detected'}
        
        # Stage 4: Feature extraction
        update_progress('extraction', 'Extracting features...', 60)
        skin_features = self.feature_extractor.extract_skin_features(processed, face_region)
        facial_features = self.feature_extractor.extract_facial_structure(processed, face_region)
        color_features = self.feature_extractor.extract_color_features(processed, face_region)
        body_features = self.feature_extractor.extract_body_features(processed)
        
        features = {**skin_features, **facial_features, **color_features, **body_features}
        
        # Stage 5: ML prediction
        update_progress('prediction', 'Analyzing dosha composition...', 80)
        feature_vector = self.feature_extractor.get_feature_vector_array(features)
        prediction = self.predictor.predict(features, feature_vector)
        
        # Stage 6: Generate insights
        update_progress('insights', 'Generating insights...', 95)
        explanation = self.predictor.generate_explanation(features, prediction['doshas'])
        recommendations = self.predictor.get_recommendations(prediction['dominant'])
        
        # Complete
        update_progress('complete', 'Analysis complete!', 100)
        
        processing_time = time.time() - start_time
        
        return {
            'success': True,
            'dominant_dosha': prediction['dominant'],
            'dosha_percentages': prediction['doshas'],
            'explanation': explanation,
            'recommendations': recommendations,
            'features': features,
            'metadata': {
                'image_resolution': validation['resolution'],
                'blur_score': validation['blur_score'],
                'brightness': validation['brightness'],
                'face_detected': True
            },
            'prediction_method': prediction['method'],
            'processing_time': round(processing_time, 2)
        }
    
    def batch_analyze(self, image_list, input_type='base64'):
        """
        Analyze multiple images
        
        Args:
            image_list: List of images
            input_type: Type of input
            
        Returns:
            List of analysis results
        """
        results = []
        
        for i, image_input in enumerate(image_list):
            print(f"\nAnalyzing image {i+1}/{len(image_list)}...")
            result = self.analyze_image(image_input, input_type, include_metadata=False)
            results.append(result)
        
        return results
    
    def get_feature_importance(self, features: Dict[str, float]) -> Dict[str, float]:
        """
        Calculate feature importance for current prediction
        
        Returns:
            Dictionary with feature importance scores
        """
        # Normalize features to importance scores
        importance = {}
        
        for feature_name, value in features.items():
            # Features closer to extremes (0 or 1) are more important
            deviation = abs(value - 0.5)
            importance[feature_name] = deviation * 2  # Scale to 0-1
        
        # Sort by importance
        sorted_importance = dict(sorted(importance.items(), key=lambda x: x[1], reverse=True))
        
        return sorted_importance


def test_pipeline():
    """Test the complete pipeline"""
    pipeline = DoshaAnalysisPipeline()
    
    # Test with sample image
    test_image = "test_image.jpg"
    
    print("\n" + "="*60)
    print("TESTING DOSHA ANALYSIS PIPELINE")
    print("="*60)
    
    result = pipeline.analyze_image(test_image, input_type='path')
    
    if result['success']:
        print("\n✓ Analysis successful!")
        print(f"\nProcessing time: {result['processing_time']}s")
        print(f"\nDominant Dosha: {result['dominant_dosha']}")
        print("\nDosha Percentages:")
        for dosha, percent in result['dosha_percentages'].items():
            print(f"  {dosha.capitalize()}: {percent:.2f}%")
        
        print(f"\nExplanation:")
        print(f"  {result['explanation']['summary']}")
        print(f"  Confidence: {result['explanation']['confidence']}")
        
        print(f"\nKey Factors:")
        for factor in result['explanation']['key_factors'][:3]:
            print(f"  • {factor}")
        
        print(f"\nTop Recommendations:")
        recs = result['recommendations']
        print(f"  Diet: {recs['diet'][0]}")
        print(f"  Lifestyle: {recs['lifestyle'][0]}")
        print(f"  Exercise: {recs['exercise'][0]}")
        
        if 'features' in result:
            print(f"\nExtracted Features:")
            for feature, value in list(result['features'].items())[:5]:
                print(f"  {feature}: {value:.4f}")
    else:
        print(f"\n✗ Analysis failed: {result['error']}")


if __name__ == "__main__":
    test_pipeline()
