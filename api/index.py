from flask import Flask, request, jsonify, render_template, send_file, session
import json
import io
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime

app = Flask(__name__, template_folder='../templates', static_folder='../static')
app.secret_key = os.getenv('SECRET_KEY', 'ayurveda_secret_key_2024')

# ============= ROUTES =============

@app.route('/')
def home():
    return render_template('home_dynamic.html')

@app.route('/old')
def old_home():
    return render_template('index.html')

@app.route('/dynamic')
def dynamic_home():
    return render_template('index_dynamic.html')

@app.route('/about')
def about():
    return render_template('about_dynamic.html')

@app.route('/assessment')
def assessment():
    return render_template('assessment.html')

@app.route('/chatbot')
def chatbot():
    return render_template('chatbot_dynamic.html')

@app.route('/contact')
def contact():
    return render_template('contact_dynamic.html')

@app.route('/clinical-assessment')
def clinical_assessment():
    return render_template('clinical_assessment_dynamic.html')

@app.route('/comprehensive-assessment')
def comprehensive_assessment():
    return render_template('comprehensive_assessment.html')

@app.route('/feedback')
def feedback():
    return render_template('feedback_dynamic.html')

@app.route('/face-analysis')
def face_analysis():
    return render_template('face_analysis.html')

@app.route('/face-analysis-advanced')
def face_analysis_advanced():
    return render_template('face_analysis_advanced.html')

@app.route('/body-analysis')
def body_analysis():
    return render_template('body_face_fusion.html')

@app.route('/ml-face-analysis')
def ml_face_analysis():
    return render_template('ml_face_analysis.html')

@app.route('/analyze-face', methods=['POST'])
def analyze_face():
    """Analyze face from uploaded image or camera capture with automatic quality enhancement"""
    try:
        from face_analysis_engine import FaceAnalysisEngine
        from image_quality_enhancer import ImageQualityEnhancer
        import numpy as np
        
        data = request.json
        image_data = data.get('image')
        user_data = data.get('user_data', {})
        
        if not image_data:
            return jsonify({'success': False, 'error': 'No image provided'})
        
        # Step 1: Enhance image quality automatically
        print("🔍 Analyzing image quality...")
        enhancer = ImageQualityEnhancer()
        enhancement_result = enhancer.analyze_and_enhance(image_data, input_type='base64')
        
        if not enhancement_result['success']:
            return jsonify({'success': False, 'error': 'Failed to process image'})
        
        enhanced_image = enhancement_result['enhanced_image']
        quality_report = enhancer.create_quality_report(
            enhancement_result['original_metrics'],
            enhancement_result['enhanced_metrics']
        )
        
        print(f"✅ Image quality improved: {quality_report['original_quality']}% → {quality_report['enhanced_quality']}%")
        print(f"📋 Enhancements applied: {', '.join(quality_report['enhancements_applied']) if quality_report['enhancements_applied'] else 'None needed'}")
        
        # Step 2: Initialize face analysis engine
        engine = FaceAnalysisEngine()
        
        # Step 3: Analyze enhanced face
        result = engine.analyze_face(enhanced_image, input_type='array')
        
        if 'error' in result:
            # If face detection fails, try with original image as fallback
            print("⚠️ Face detection failed on enhanced image, trying original...")
            result = engine.analyze_face(image_data, input_type='base64')
            
            if 'error' in result:
                return jsonify({
                    'success': False, 
                    'error': result['error'],
                    'quality_report': quality_report,
                    'suggestion': 'Please ensure your face is clearly visible and well-lit in the image'
                })
        
        # Convert numpy types to Python native types for JSON serialization
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
        
        # Add quality enhancement info
        result['quality_enhancement'] = quality_report
        result['user_data'] = user_data
        
        # Get recommendations based on dominant dosha
        dominant_lower = result['dominant'].lower()
        result['recommendations'] = get_recommendations(dominant_lower)
        result['diet_suggestions'] = get_diet_suggestions(dominant_lower)
        result['lifestyle_tips'] = get_lifestyle_tips(dominant_lower)
        
        return jsonify(result)
        
    except Exception as e:
        print(f"Face analysis error: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({
            'success': False,
            'error': f'Analysis failed: {str(e)}',
            'suggestion': 'Please try with a different image or check image format'
        }), 500

@app.route('/analyze-face-structural', methods=['POST'])
def analyze_face_structural():
    """Analyze face using structural pattern analysis (geometry-based)"""
    try:
        from structural_face_analysis_simple import StructuralFaceAnalyzer
        import numpy as np
        
        data = request.json
        image_data = data.get('image')
        user_data = data.get('user_data', {})
        
        if not image_data:
            return jsonify({'success': False, 'error': 'No image provided'})
        
        # Initialize structural face analyzer
        analyzer = StructuralFaceAnalyzer()
        
        # Analyze face from base64 image
        result = analyzer.analyze_face(image_data, input_type='base64')
        
        if 'error' in result:
            return jsonify({'success': False, 'error': result['error']})
        
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
        
        # Add user data
        result['user_data'] = user_data
        result['analysis_type'] = 'Structural Pattern Analysis (OpenCV DNN)'
        
        # Get recommendations
        dominant_lower = result['dominant'].lower()
        result['recommendations'] = get_recommendations(dominant_lower)
        result['diet_suggestions'] = get_diet_suggestions(dominant_lower)
        result['lifestyle_tips'] = get_lifestyle_tips(dominant_lower)
        
        return jsonify(result)
        
    except Exception as e:
        print(f"Structural face analysis error: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({
            'success': False,
            'error': f'Structural analysis failed: {str(e)}'
        }), 500

@app.route('/extract-facial-regions', methods=['POST'])
def extract_facial_regions():
    """Extract facial regions using MediaPipe Face Mesh"""
    try:
        from facial_region_extraction import FacialRegionExtractor
        import numpy as np
        import cv2
        import base64
        
        data = request.json
        image_data = data.get('image')
        
        if not image_data:
            return jsonify({'success': False, 'error': 'No image provided'})
        
        # Initialize extractor
        extractor = FacialRegionExtractor()
        
        # Load image from base64
        image = extractor.load_image_from_base64(image_data)
        if image is None:
            return jsonify({'success': False, 'error': 'Failed to load image'})
        
        # Detect face
        face_landmarks = extractor.detect_face(image)
        if face_landmarks is None:
            return jsonify({'success': False, 'error': 'No face detected'})
        
        # Extract landmarks
        landmarks = extractor.extract_landmarks(face_landmarks, image.shape)
        
        # Segment regions
        regions = extractor.segment_regions(image, landmarks)
        
        # Convert regions to base64
        region_images = {}
        for region_name, region_img in regions.items():
            if region_img is not None and region_img.size > 0:
                # Encode to base64
                _, buffer = cv2.imencode('.jpg', region_img)
                region_base64 = base64.b64encode(buffer).decode('utf-8')
                region_images[region_name] = f"data:image/jpeg;base64,{region_base64}"
        
        return jsonify({
            'success': True,
            'regions': region_images,
            'total_regions': len(region_images),
            'landmark_count': len(landmarks)
        })
        
    except Exception as e:
        print(f"Facial region extraction error: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({
            'success': False,
            'error': f'Region extraction failed: {str(e)}'
        }), 500

@app.route('/analyze-face-enhanced', methods=['POST'])
def analyze_face_enhanced():
    """Enhanced face analysis with automatic image quality enhancement and texture detection"""
    try:
        # Handle both JSON and form data
        if request.is_json:
            data = request.json
        else:
            data = request.form.to_dict()
        
        image_data = data.get('image')
        user_data = data.get('user_data', {})
        
        if not image_data:
            return jsonify({'success': False, 'error': 'No image provided'}), 400
        
        import cv2
        import numpy as np
        import base64
        from io import BytesIO
        from PIL import Image
        from image_quality_enhancer import ImageQualityEnhancer
        
        # Step 1: Enhance image quality automatically
        print("🔍 Enhancing image quality...")
        enhancer = ImageQualityEnhancer()
        enhancement_result = enhancer.analyze_and_enhance(image_data, input_type='base64')
        
        if not enhancement_result['success']:
            return jsonify({'success': False, 'error': 'Failed to process image'})
        
        image = enhancement_result['enhanced_image']
        quality_report = enhancer.create_quality_report(
            enhancement_result['original_metrics'],
            enhancement_result['enhanced_metrics']
        )
        
        print(f"✅ Quality: {quality_report['original_quality']}% → {quality_report['enhanced_quality']}%")
        
        # Detect face using OpenCV
        face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)
        
        if len(faces) == 0:
            return jsonify({'success': False, 'error': 'No face detected'})
        
        # Get largest face
        face = max(faces, key=lambda f: f[2] * f[3])
        x, y, w, h = face
        
        # Extract face region with padding
        padding = 20
        x_min = max(0, x - padding)
        y_min = max(0, y - padding)
        x_max = min(image.shape[1], x + w + padding)
        y_max = min(image.shape[0], y + h + padding)
        
        face_region = image[y_min:y_max, x_min:x_max].copy()
        
        # Image enhancement pipeline
        processing_steps = {}
        
        # Step 1: Grayscale
        gray_face = cv2.cvtColor(face_region, cv2.COLOR_BGR2GRAY)
        _, buffer = cv2.imencode('.jpg', cv2.cvtColor(gray_face, cv2.COLOR_GRAY2BGR))
        processing_steps['grayscale'] = f"data:image/jpeg;base64,{base64.b64encode(buffer).decode('utf-8')}"
        
        # Step 2: Histogram equalization
        equalized = cv2.equalizeHist(gray_face)
        _, buffer = cv2.imencode('.jpg', cv2.cvtColor(equalized, cv2.COLOR_GRAY2BGR))
        processing_steps['equalized'] = f"data:image/jpeg;base64,{base64.b64encode(buffer).decode('utf-8')}"
        
        # Step 3: Sharpening
        kernel_sharpen = np.array([[0, -1, 0], [-1, 5, -1], [0, -1, 0]])
        sharpened = cv2.filter2D(equalized, -1, kernel_sharpen)
        _, buffer = cv2.imencode('.jpg', cv2.cvtColor(sharpened, cv2.COLOR_GRAY2BGR))
        processing_steps['sharpened'] = f"data:image/jpeg;base64,{base64.b64encode(buffer).decode('utf-8')}"
        
        # Step 4: Gaussian blur
        blurred = cv2.GaussianBlur(sharpened, (3, 3), 0)
        _, buffer = cv2.imencode('.jpg', cv2.cvtColor(blurred, cv2.COLOR_GRAY2BGR))
        processing_steps['blurred'] = f"data:image/jpeg;base64,{base64.b64encode(buffer).decode('utf-8')}"
        
        # Texture extraction
        laplacian = cv2.Laplacian(blurred, cv2.CV_64F)
        texture_variance = float(laplacian.var())
        texture_mean = float(np.abs(laplacian).mean())
        
        # Create texture map
        texture_map = np.abs(laplacian)
        texture_map = cv2.normalize(texture_map, None, 0, 255, cv2.NORM_MINMAX)
        texture_map = texture_map.astype(np.uint8)
        texture_map_colored = cv2.applyColorMap(texture_map, cv2.COLORMAP_JET)
        _, buffer = cv2.imencode('.jpg', texture_map_colored)
        processing_steps['texture'] = f"data:image/jpeg;base64,{base64.b64encode(buffer).decode('utf-8')}"
        
        # Face structure
        face_width = x_max - x_min
        face_height = y_max - y_min
        face_ratio = face_width / face_height if face_height > 0 else 0
        
        # Dosha scoring
        vata = pitta = kapha = 0
        
        # Texture-based scoring
        if texture_variance > 120:
            vata += 2
        elif texture_variance >= 60:
            pitta += 2
        else:
            kapha += 2
        
        # Structure-based scoring
        if face_ratio < 0.75:
            vata += 2
        elif face_ratio > 0.9:
            kapha += 2
        else:
            pitta += 2
        
        # Additional texture metrics
        if texture_mean > 15:
            vata += 1
        elif texture_mean < 8:
            kapha += 1
        else:
            pitta += 1
        
        # Normalization
        total = vata + pitta + kapha
        if total > 0:
            vata_percent = round((vata / total) * 100, 1)
            pitta_percent = round((pitta / total) * 100, 1)
            kapha_percent = round((kapha / total) * 100, 1)
        else:
            vata_percent = pitta_percent = kapha_percent = 33.3
        
        # Determine dominant
        doshas = {'Vata': vata_percent, 'Pitta': pitta_percent, 'Kapha': kapha_percent}
        dominant = max(doshas, key=doshas.get)
        
        # Risk level
        max_score = max(vata_percent, pitta_percent, kapha_percent)
        if max_score >= 50:
            risk = 'High'
        elif max_score >= 40:
            risk = 'Moderate'
        else:
            risk = 'Low'
        
        # Generate explanation
        explanation = f"{dominant} dominance detected based on "
        if dominant == 'Vata':
            explanation += f"high skin texture variance ({texture_variance:.2f}) indicating rough, dry skin"
            if face_ratio < 0.75:
                explanation += f" and narrow facial structure (ratio: {face_ratio:.3f})"
        elif dominant == 'Pitta':
            explanation += f"moderate skin texture variance ({texture_variance:.2f})"
            if 0.75 <= face_ratio <= 0.9:
                explanation += f" and balanced facial structure (ratio: {face_ratio:.3f})"
        elif dominant == 'Kapha':
            explanation += f"low skin texture variance ({texture_variance:.2f}) indicating smooth, oily skin"
            if face_ratio > 0.9:
                explanation += f" and wide facial structure (ratio: {face_ratio:.3f})"
        
        # Compile result
        result = {
            'success': True,
            'analysis_type': 'Enhanced Texture Analysis with Auto Quality Enhancement',
            'dominant': dominant,
            'scores': {
                'vata': vata_percent,
                'pitta': pitta_percent,
                'kapha': kapha_percent
            },
            'risk': risk,
            'texture': {
                'variance': round(texture_variance, 2),
                'mean': round(texture_mean, 2)
            },
            'structure': {
                'width': int(face_width),
                'height': int(face_height),
                'ratio': round(face_ratio, 3)
            },
            'processing_steps': processing_steps,
            'explanation': explanation,
            'quality_enhancement': quality_report,
            'user_data': user_data
        }
        
        # Add recommendations
        dominant_lower = dominant.lower()
        result['recommendations'] = get_recommendations(dominant_lower)
        result['diet_suggestions'] = get_diet_suggestions(dominant_lower)
        result['lifestyle_tips'] = get_lifestyle_tips(dominant_lower)
        
        return jsonify(result)
        
    except Exception as e:
        print(f"Enhanced face analysis error: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({
            'success': False,
            'error': f'Enhanced analysis failed: {str(e)}'
        }), 500

@app.route('/analyze-body', methods=['POST'])
def analyze_body():
    """Analyze body from uploaded image with automatic quality enhancement"""
    try:
        from face_body_detection_extended import FaceBodyDetector
        from image_quality_enhancer import ImageQualityEnhancer
        import numpy as np
        import base64
        from io import BytesIO
        from PIL import Image
        import cv2
        
        data = request.json
        image_data = data.get('image')
        user_data = data.get('user_data', {})
        
        if not image_data:
            return jsonify({'success': False, 'error': 'No image provided'})
        
        # Step 1: Enhance image quality automatically
        print("🔍 Enhancing image quality for body analysis...")
        enhancer = ImageQualityEnhancer()
        enhancement_result = enhancer.analyze_and_enhance(image_data, input_type='base64')
        
        if not enhancement_result['success']:
            return jsonify({'success': False, 'error': 'Failed to process image'})
        
        image = enhancement_result['enhanced_image']
        quality_report = enhancer.create_quality_report(
            enhancement_result['original_metrics'],
            enhancement_result['enhanced_metrics']
        )
        
        print(f"✅ Quality improved: {quality_report['original_quality']}% → {quality_report['enhanced_quality']}%")
        
        # Initialize detector
        detector = FaceBodyDetector()
        
        # Detect faces and bodies
        faces = detector.detect_faces(image)
        bodies = detector.detect_bodies(image)
        
        if len(bodies) == 0:
            return jsonify({'success': False, 'error': 'No body detected. Please ensure full body is visible in the image.'})
        
        # Analyze body
        body_analyses = []
        for body_bbox in bodies:
            analysis = detector.analyze_body(body_bbox)
            body_analyses.append(analysis)
        
        # Get first body analysis
        body_result = body_analyses[0]
        
        # Encode result image with bounding boxes
        result_image = detector.draw_detections(image, faces, bodies)
        _, buffer = cv2.imencode('.jpg', result_image)
        result_image_base64 = f"data:image/jpeg;base64,{base64.b64encode(buffer).decode('utf-8')}"
        
        # Determine dominant dosha
        max_score = max(body_result['vata'], body_result['pitta'], body_result['kapha'])
        if body_result['vata'] == max_score:
            dominant = 'Vata'
        elif body_result['pitta'] == max_score:
            dominant = 'Pitta'
        else:
            dominant = 'Kapha'
        
        # Calculate percentages
        total = body_result['vata'] + body_result['pitta'] + body_result['kapha']
        if total > 0:
            vata_percent = round((body_result['vata'] / total) * 100, 1)
            pitta_percent = round((body_result['pitta'] / total) * 100, 1)
            kapha_percent = round((body_result['kapha'] / total) * 100, 1)
        else:
            vata_percent = pitta_percent = kapha_percent = 33.3
        
        result = {
            'success': True,
            'analysis_type': 'Body Structure Analysis with Auto Quality Enhancement',
            'dominant': dominant,
            'scores': {
                'vata': vata_percent,
                'pitta': pitta_percent,
                'kapha': kapha_percent
            },
            'body_measurements': {
                'width': body_result['width'],
                'height': body_result['height'],
                'ratio': body_result['ratio']
            },
            'result_image': result_image_base64,
            'faces_detected': len(faces),
            'bodies_detected': len(bodies),
            'quality_enhancement': quality_report,
            'user_data': user_data
        }
        
        # Add recommendations
        dominant_lower = dominant.lower()
        result['recommendations'] = get_recommendations(dominant_lower)
        result['diet_suggestions'] = get_diet_suggestions(dominant_lower)
        result['lifestyle_tips'] = get_lifestyle_tips(dominant_lower)
        
        return jsonify(result)
        
    except Exception as e:
        print(f"Body analysis error: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({
            'success': False,
            'error': f'Body analysis failed: {str(e)}'
        }), 500

@app.route('/analyze-face-body-fusion', methods=['POST'])
def analyze_face_body_fusion():
    """Perform face-body fusion analysis with automatic quality enhancement"""
    try:
        # Handle both JSON and form data
        if request.is_json:
            data = request.json
        else:
            data = request.form.to_dict()
        
        image_data = data.get('image')
        face_scores = data.get('face_scores')  # {'vata': x, 'pitta': y, 'kapha': z}
        user_data = data.get('user_data', {})
        
        if not image_data:
            return jsonify({'success': False, 'error': 'No image provided'}), 400
        
        if not face_scores:
            return jsonify({'success': False, 'error': 'Face scores required for fusion'}), 400
        
        from face_body_detection_extended import FaceBodyDetector
        from image_quality_enhancer import ImageQualityEnhancer
        import numpy as np
        import base64
        from io import BytesIO
        from PIL import Image
        import cv2
        
        # Step 1: Enhance image quality automatically
        print("🔍 Enhancing image quality for fusion analysis...")
        enhancer = ImageQualityEnhancer()
        enhancement_result = enhancer.analyze_and_enhance(image_data, input_type='base64')
        
        if not enhancement_result['success']:
            return jsonify({'success': False, 'error': 'Failed to process image'})
        
        image = enhancement_result['enhanced_image']
        quality_report = enhancer.create_quality_report(
            enhancement_result['original_metrics'],
            enhancement_result['enhanced_metrics']
        )
        
        print(f"✅ Quality improved: {quality_report['original_quality']}% → {quality_report['enhanced_quality']}%")
        
        # Initialize detector
        detector = FaceBodyDetector()
        
        # Detect and analyze body
        bodies = detector.detect_bodies(image)
        
        if len(bodies) == 0:
            return jsonify({'success': False, 'error': 'No body detected. Please ensure full body is visible in the image with good lighting.'})
        
        # Get largest body
        body_bbox = max(bodies, key=lambda b: b[2] * b[3])
        
        # Analyze body
        body_analysis = detector.analyze_body(body_bbox)
        
        # Perform fusion
        fusion_result = detector.fuse_results(face_scores, body_analysis)
        
        # Draw detections on image
        faces = detector.detect_faces(image)
        result_image = detector.draw_detections(image, faces, bodies)
        _, buffer = cv2.imencode('.jpg', result_image)
        result_image_base64 = f"data:image/jpeg;base64,{base64.b64encode(buffer).decode('utf-8')}"
        
        result = {
            'success': True,
            'analysis_type': 'Face-Body Fusion Analysis with Auto Quality Enhancement',
            'dominant': fusion_result['dominant_dosha'],
            'scores': {
                'vata': fusion_result['vata_percent'],
                'pitta': fusion_result['pitta_percent'],
                'kapha': fusion_result['kapha_percent']
            },
            'fusion_details': {
                'face_weight': '60%',
                'body_weight': '40%',
                'face_scores': face_scores,
                'body_scores': {
                    'vata': body_analysis['vata'],
                    'pitta': body_analysis['pitta'],
                    'kapha': body_analysis['kapha']
                },
                'body_measurements': {
                    'width': body_analysis['width'],
                    'height': body_analysis['height'],
                    'ratio': body_analysis['ratio']
                }
            },
            'result_image': result_image_base64,
            'faces_detected': len(faces),
            'bodies_detected': len(bodies),
            'quality_enhancement': quality_report,
            'user_data': user_data
        }
        
        # Add recommendations
        dominant_lower = fusion_result['dominant_dosha'].lower()
        result['recommendations'] = get_recommendations(dominant_lower)
        result['diet_suggestions'] = get_diet_suggestions(dominant_lower)
        result['lifestyle_tips'] = get_lifestyle_tips(dominant_lower)
        
        return jsonify(result)
        
    except Exception as e:
        print(f"Fusion analysis error: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({
            'success': False,
            'error': f'Fusion analysis failed: {str(e)}'
        }), 500

# ============= API ENDPOINTS =============

@app.route('/health')
def health_check():
    return jsonify({
        'status': 'healthy',
        'service': 'AyurAI Veda',
        'version': '2.0.0',
        'timestamp': datetime.now().isoformat(),
        'environment': 'vercel' if os.getenv('VERCEL') else 'local'
    })

@app.route('/api/status')
def api_status():
    return jsonify({
        'api': 'AyurAI Veda API',
        'status': 'operational',
        'features': {
            'clinical_assessment': True,
            'comprehensive_assessment': True,
            'chatbot': True,
            'feedback': True
        }
    })

@app.route('/analyze', methods=['POST'])
def analyze():
    try:
        data = request.json
        result = analyze_tridosha(data)
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/clinical-analyze', methods=['POST'])
def clinical_analyze():
    try:
        data = request.json
        
        # Get user details
        user_data = {
            'name': data.get('name', 'User'),
            'age': data.get('age', 'N/A'),
            'gender': data.get('gender', 'N/A'),
            'location': data.get('location', 'N/A')
        }
        
        # Perform clinical analysis
        result = analyze_clinical(data)
        result['raw_answers'] = data  # Store for report generation
        
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/comprehensive-analyze', methods=['POST'])
def comprehensive_analyze():
    try:
        data = request.json
        result = analyze_comprehensive(data)
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/chat', methods=['POST'])
def chat():
    try:
        data = request.json
        message = data.get('message', '').lower()
        response = get_chatbot_response(message)
        return jsonify({'response': response})
    except Exception as e:
        return jsonify({'response': 'Sorry, I encountered an error. Please try again.'}), 500

@app.route('/submit-feedback', methods=['POST'])
def submit_feedback():
    try:
        data = request.json
        # Validate required fields
        required = ['name', 'mobile', 'institute', 'designation', 'feedback']
        for field in required:
            if not data.get(field):
                return jsonify({'success': False, 'message': f'{field.title()} is required'})
        
        # Validate mobile number
        mobile = data['mobile']
        if not mobile.isdigit() or len(mobile) != 10:
            return jsonify({'success': False, 'message': 'Please enter a valid 10-digit mobile number'})
        
        # Validate feedback length
        if len(data['feedback']) > 2000:
            return jsonify({'success': False, 'message': 'Feedback must be less than 2000 characters'})
        
        # Try to send email
        email_sent = send_feedback_email(data)
        
        # Always log feedback
        log_feedback(data)
        
        if email_sent:
            return jsonify({'success': True, 'message': 'Feedback submitted successfully! We will contact you soon.'})
        else:
            # Return success even if email fails (feedback is logged)
            return jsonify({'success': True, 'message': 'Feedback received successfully! Thank you for your input.'})
    except Exception as e:
        print(f"Feedback error: {str(e)}")
        # Still log the feedback
        try:
            log_feedback(data)
        except:
            pass
        return jsonify({'success': True, 'message': 'Feedback received successfully!'})

@app.route('/send-report-email', methods=['POST'])
def send_report_email():
    try:
        data = request.json
        email = data.get('email')
        report_data = data.get('report_data')
        
        if not email or not report_data:
            return jsonify({'success': False, 'message': 'Email and report data required'})
        
        # Validate email format
        import re
        if not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email):
            return jsonify({'success': False, 'message': 'Invalid email address'})
        
        # Send report via email
        email_sent = send_assessment_report_email(email, report_data)
        
        if email_sent:
            return jsonify({'success': True, 'message': f'Report sent successfully to {email}'})
        else:
            return jsonify({'success': False, 'message': 'Failed to send email. Please try again.'})
    except Exception as e:
        print(f"Email error: {str(e)}")
        return jsonify({'success': False, 'message': 'An error occurred'}), 500

@app.route('/generate-clinical-report', methods=['POST'])
def generate_clinical_report_endpoint():
    """Generate comprehensive clinical report with LLM"""
    try:
        from clinical_report_generator import generate_clinical_report
        
        data = request.json
        user_data = data.get('user_data', {})
        assessment_results = data.get('assessment_results', {})
        
        # Generate comprehensive report
        report = generate_clinical_report(user_data, assessment_results)
        
        return jsonify({
            'success': True,
            'report': report
        })
    except Exception as e:
        print(f"Report generation error: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/download-clinical-report', methods=['POST'])
def download_clinical_report():
    """Download clinical report as PDF"""
    try:
        from reportlab.lib.pagesizes import letter
        from reportlab.lib import colors
        from reportlab.lib.units import inch
        from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
        from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
        from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
        
        data = request.json
        report = data.get('report', {})
        
        # Create PDF in memory
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(
            buffer,
            pagesize=letter,
            rightMargin=60,
            leftMargin=60,
            topMargin=60,
            bottomMargin=40
        )
        
        elements = []
        styles = getSampleStyleSheet()
        
        # Custom styles
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=22,
            textColor=colors.HexColor('#FF9933'),
            spaceAfter=8,
            alignment=TA_CENTER,
            fontName='Helvetica-Bold'
        )
        
        subtitle_style = ParagraphStyle(
            'Subtitle',
            parent=styles['Normal'],
            fontSize=12,
            textColor=colors.HexColor('#138808'),
            spaceAfter=20,
            alignment=TA_CENTER,
            fontName='Helvetica-Bold'
        )
        
        section_heading = ParagraphStyle(
            'SectionHeading',
            parent=styles['Heading2'],
            fontSize=14,
            textColor=colors.HexColor('#1a237e'),
            spaceAfter=10,
            spaceBefore=15,
            fontName='Helvetica-Bold',
            borderPadding=5,
            backColor=colors.HexColor('#f5f5f5')
        )
        
        body_style = ParagraphStyle(
            'CustomBody',
            parent=styles['Normal'],
            fontSize=10,
            spaceAfter=6,
            fontName='Helvetica',
            alignment=TA_JUSTIFY
        )
        
        bullet_style = ParagraphStyle(
            'Bullet',
            parent=styles['Normal'],
            fontSize=10,
            spaceAfter=4,
            leftIndent=20,
            fontName='Helvetica'
        )
        
        # Header
        elements.append(Paragraph("🕉️ AyurAI Veda", title_style))
        elements.append(Paragraph("Ayurvedic Clinical Assessment Report", subtitle_style))
        elements.append(Spacer(1, 0.2*inch))
        
        # Personal Details
        personal = report.get('personal_details', {})
        elements.append(Paragraph("👤 Personal Details", section_heading))
        
        personal_data = [
            ['Name:', str(personal.get('name', 'N/A'))],
            ['Age:', str(personal.get('age', 'N/A'))],
            ['Gender:', str(personal.get('gender', 'N/A'))],
            ['Location:', str(personal.get('location', 'N/A'))],
            ['Assessment Date:', report.get('timestamp', datetime.now().strftime('%d %B %Y at %I:%M %p'))]
        ]
        
        personal_table = Table(personal_data, colWidths=[1.5*inch, 4.5*inch])
        personal_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#f5f5f5')),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
            ('TOPPADDING', (0, 0), (-1, -1), 8),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey)
        ]))
        elements.append(personal_table)
        elements.append(Spacer(1, 0.2*inch))
        
        # Dosha Analysis
        dosha_analysis = report.get('dosha_analysis', {})
        elements.append(Paragraph("🧠 Dosha Analysis", section_heading))
        
        dosha_data = [
            ['Dominant Dosha:', str(dosha_analysis.get('dominant_dosha', 'N/A'))],
            ['Secondary Dosha:', str(dosha_analysis.get('secondary_dosha', 'N/A'))],
            ['Current Imbalance:', str(dosha_analysis.get('vikriti', 'N/A'))]
        ]
        
        dosha_table = Table(dosha_data, colWidths=[2*inch, 4*inch])
        dosha_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#fff3e0')),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
            ('TOPPADDING', (0, 0), (-1, -1), 8),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey)
        ]))
        elements.append(dosha_table)
        elements.append(Spacer(1, 0.1*inch))
        
        explanation = dosha_analysis.get('explanation', '')
        if explanation:
            elements.append(Paragraph(explanation, body_style))
        elements.append(Spacer(1, 0.2*inch))
        
        # Diet Recommendations
        diet = report.get('diet_recommendations', {})
        elements.append(Paragraph("🥗 Diet Recommendations", section_heading))
        
        elements.append(Paragraph("<b>✅ Foods to Take:</b>", body_style))
        for food in diet.get('foods_to_take', []):
            elements.append(Paragraph(f"• {food}", bullet_style))
        elements.append(Spacer(1, 0.1*inch))
        
        elements.append(Paragraph("<b>❌ Foods to Avoid:</b>", body_style))
        for food in diet.get('foods_to_avoid', []):
            elements.append(Paragraph(f"• {food}", bullet_style))
        elements.append(Spacer(1, 0.1*inch))
        
        elements.append(Paragraph("<b>💡 Eating Guidelines:</b>", body_style))
        for guideline in diet.get('eating_guidelines', []):
            elements.append(Paragraph(f"• {guideline}", bullet_style))
        elements.append(Spacer(1, 0.2*inch))
        
        # Lifestyle Recommendations
        lifestyle = report.get('lifestyle_recommendations', {})
        elements.append(Paragraph("🧘 Lifestyle Recommendations", section_heading))
        
        elements.append(Paragraph("<b>🌿 Daily Routine (Dinacharya):</b>", body_style))
        for routine in lifestyle.get('daily_routine', []):
            elements.append(Paragraph(f"• {routine}", bullet_style))
        elements.append(Spacer(1, 0.1*inch))
        
        practices = lifestyle.get('practices', {})
        if practices.get('yoga'):
            elements.append(Paragraph("<b>🧘♂️ Yoga Practices:</b>", body_style))
            for yoga in practices['yoga']:
                elements.append(Paragraph(f"• {yoga}", bullet_style))
            elements.append(Spacer(1, 0.1*inch))
        
        if practices.get('pranayama'):
            elements.append(Paragraph("<b>🌬️ Pranayama:</b>", body_style))
            for prana in practices['pranayama']:
                elements.append(Paragraph(f"• {prana}", bullet_style))
            elements.append(Spacer(1, 0.1*inch))
        
        if practices.get('meditation'):
            elements.append(Paragraph("<b>🧘 Meditation:</b>", body_style))
            for med in practices['meditation']:
                elements.append(Paragraph(f"• {med}", bullet_style))
        elements.append(Spacer(1, 0.2*inch))
        
        # Herbal Support
        herbal = report.get('herbal_support', {})
        elements.append(Paragraph("🌱 Herbal Support", section_heading))
        
        elements.append(Paragraph("<b>🌿 Recommended Herbs:</b>", body_style))
        for herb in herbal.get('recommended_herbs', []):
            elements.append(Paragraph(f"• {herb}", bullet_style))
        elements.append(Spacer(1, 0.1*inch))
        
        elements.append(Paragraph("<b>💊 Usage Guidance:</b>", body_style))
        for usage in herbal.get('usage_guidance', []):
            elements.append(Paragraph(f"• {usage}", bullet_style))
        elements.append(Spacer(1, 0.2*inch))
        
        # Wellness Advice
        wellness = report.get('wellness_advice', {})
        elements.append(Paragraph("🧭 Additional Wellness Advice", section_heading))
        
        if wellness.get('seasonal_tips'):
            elements.append(Paragraph("<b>Seasonal Care (Ritucharya):</b>", body_style))
            for tip in wellness['seasonal_tips']:
                elements.append(Paragraph(f"• {tip}", bullet_style))
            elements.append(Spacer(1, 0.1*inch))
        
        if wellness.get('stress_management'):
            elements.append(Paragraph("<b>Stress Management:</b>", body_style))
            for tip in wellness['stress_management']:
                elements.append(Paragraph(f"• {tip}", bullet_style))
            elements.append(Spacer(1, 0.1*inch))
        
        if wellness.get('digestive_care'):
            elements.append(Paragraph("<b>Digestive Care:</b>", body_style))
            for tip in wellness['digestive_care']:
                elements.append(Paragraph(f"• {tip}", bullet_style))
        elements.append(Spacer(1, 0.3*inch))
        
        # Disclaimer
        disclaimer_style = ParagraphStyle(
            'Disclaimer',
            parent=styles['Normal'],
            fontSize=8,
            textColor=colors.HexColor('#d32f2f'),
            leftIndent=10,
            rightIndent=10,
            fontName='Helvetica',
            alignment=TA_JUSTIFY
        )
        elements.append(Paragraph(
            "<b>⚠️ Important Disclaimer:</b> " + report.get('disclaimer', ''),
            disclaimer_style
        ))
        
        elements.append(Spacer(1, 0.2*inch))
        
        # Footer
        footer_style = ParagraphStyle(
            'Footer',
            parent=styles['Normal'],
            fontSize=9,
            alignment=TA_CENTER,
            textColor=colors.HexColor('#666666'),
            fontName='Helvetica'
        )
        elements.append(Paragraph("🌿 AyurAI Veda | Ancient Wisdom. Intelligent Health.", footer_style))
        elements.append(Paragraph("Powered by Tridosha Intelligence Engine™", footer_style))
        
        # Build PDF
        doc.build(elements)
        
        # Get PDF data
        pdf_data = buffer.getvalue()
        buffer.close()
        
        # Create new buffer with PDF data
        output = io.BytesIO(pdf_data)
        output.seek(0)
        
        return send_file(
            output,
            mimetype='application/pdf',
            as_attachment=True,
            download_name=f'AyurAI_Clinical_Report_{datetime.now().strftime("%Y%m%d_%H%M%S")}.pdf'
        )
        
    except Exception as e:
        print(f"PDF generation error: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': f'Failed to generate PDF: {str(e)}'}), 500
@app.route('/download-report', methods=['POST'])
def download_report():
    try:
        from reportlab.lib.pagesizes import letter, A4
        from reportlab.lib import colors
        from reportlab.lib.units import inch
        from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, Image
        from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
        from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
        from reportlab.graphics.shapes import Drawing, Rect, String
        from reportlab.graphics.charts.barcharts import VerticalBarChart
        from reportlab.graphics import renderPDF
        
        data = request.json
        
        # Create PDF in memory
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(
            buffer,
            pagesize=letter,
            rightMargin=50,
            leftMargin=50,
            topMargin=50,
            bottomMargin=30
        )
        
        elements = []
        styles = getSampleStyleSheet()
        
        # Custom styles
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=24,
            textColor=colors.HexColor('#FF9933'),
            spaceAfter=8,
            alignment=TA_CENTER,
            fontName='Helvetica-Bold'
        )
        
        subtitle_style = ParagraphStyle(
            'Subtitle',
            parent=styles['Normal'],
            fontSize=14,
            textColor=colors.HexColor('#138808'),
            spaceAfter=20,
            alignment=TA_CENTER,
            fontName='Helvetica-Bold'
        )
        
        section_heading = ParagraphStyle(
            'SectionHeading',
            parent=styles['Heading2'],
            fontSize=13,
            textColor=colors.white,
            spaceAfter=10,
            spaceBefore=15,
            fontName='Helvetica-Bold',
            backColor=colors.HexColor('#1a237e'),
            borderPadding=8
        )
        
        body_style = ParagraphStyle(
            'CustomBody',
            parent=styles['Normal'],
            fontSize=10,
            spaceAfter=6,
            fontName='Helvetica',
            alignment=TA_JUSTIFY
        )
        
        bullet_style = ParagraphStyle(
            'Bullet',
            parent=styles['Normal'],
            fontSize=10,
            spaceAfter=4,
            leftIndent=20,
            fontName='Helvetica'
        )
        
        # Header
        elements.append(Paragraph("🕉️ AyurAI Veda™", title_style))
        elements.append(Paragraph("Tridosha Intelligence Engine™ Report", subtitle_style))
        elements.append(Spacer(1, 0.3*inch))
        
        # Assessment Summary Box
        summary_data = [
            ['Assessment Date:', datetime.now().strftime('%d %B %Y at %I:%M %p')],
            ['Dominant Dosha:', str(data.get('dominant', 'N/A'))],
            ['Risk Level:', str(data.get('risk', 'N/A'))]
        ]
        
        if data.get('dosha_state'):
            summary_data.append(['Dosha State:', str(data.get('dosha_state'))])
        if data.get('agni_state'):
            summary_data.append(['Agni State:', str(data.get('agni_state'))])
        if data.get('ama_status'):
            summary_data.append(['Ama Status:', str(data.get('ama_status'))])
        
        summary_table = Table(summary_data, colWidths=[2*inch, 4.5*inch])
        summary_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#f5f5f5')),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
            ('TOPPADDING', (0, 0), (-1, -1), 10),
            ('GRID', (0, 0), (-1, -1), 1, colors.grey),
            ('BOX', (0, 0), (-1, -1), 2, colors.HexColor('#1a237e'))
        ]))
        elements.append(summary_table)
        elements.append(Spacer(1, 0.3*inch))
        
        # Dosha Distribution with Visual Meters
        elements.append(Paragraph("⚖️ DOSHA DISTRIBUTION ANALYSIS", section_heading))
        elements.append(Spacer(1, 0.15*inch))
        
        scores = data.get('scores', {})
        vata_score = scores.get('vata', 0)
        pitta_score = scores.get('pitta', 0)
        kapha_score = scores.get('kapha', 0)
        
        # Create visual bar chart
        drawing = Drawing(400, 200)
        chart = VerticalBarChart()
        chart.x = 50
        chart.y = 50
        chart.height = 120
        chart.width = 300
        chart.data = [[vata_score, pitta_score, kapha_score]]
        chart.categoryAxis.categoryNames = ['Vata', 'Pitta', 'Kapha']
        chart.bars[0].fillColor = colors.HexColor('#9C27B0')
        chart.bars[1].fillColor = colors.HexColor('#FF5722')
        chart.bars[2].fillColor = colors.HexColor('#4CAF50')
        chart.valueAxis.valueMin = 0
        chart.valueAxis.valueMax = 100
        chart.valueAxis.valueStep = 20
        chart.categoryAxis.labels.fontSize = 10
        chart.valueAxis.labels.fontSize = 8
        drawing.add(chart)
        elements.append(drawing)
        elements.append(Spacer(1, 0.15*inch))
        
        # Dosha percentage table
        dosha_data = [
            ['Dosha', 'Percentage', 'Status'],
            ['🌬️ Vata (Air + Space)', f"{vata_score}%", '✓ Dominant' if data.get('dominant', '').lower().startswith('vata') else ''],
            ['🔥 Pitta (Fire + Water)', f"{pitta_score}%", '✓ Dominant' if data.get('dominant', '').lower().startswith('pitta') else ''],
            ['🌊 Kapha (Water + Earth)', f"{kapha_score}%", '✓ Dominant' if data.get('dominant', '').lower().startswith('kapha') else '']
        ]
        
        dosha_table = Table(dosha_data, colWidths=[2.5*inch, 1.5*inch, 2.5*inch])
        dosha_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1a237e')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
            ('TOPPADDING', (0, 0), (-1, -1), 10),
            ('GRID', (0, 0), (-1, -1), 1, colors.grey),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f9f9f9')])
        ]))
        elements.append(dosha_table)
        elements.append(Spacer(1, 0.2*inch))
        
        # Clinical Justification
        if data.get('justification'):
            elements.append(Paragraph("🔬 CLINICAL ASSESSMENT", section_heading))
            elements.append(Spacer(1, 0.1*inch))
            justification_text = str(data['justification']).replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
            elements.append(Paragraph(justification_text, body_style))
            elements.append(Spacer(1, 0.2*inch))
        
        # Recommendations Section
        recommendations = data.get('recommendations', [])
        if recommendations:
            elements.append(Paragraph("📋 PERSONALIZED RECOMMENDATIONS", section_heading))
            elements.append(Spacer(1, 0.1*inch))
            
            current_category = None
            for rec in recommendations:
                rec_text = str(rec).strip()
                
                # Check if it's a category header
                if rec_text.endswith(':') and rec_text.isupper():
                    if current_category:
                        elements.append(Spacer(1, 0.1*inch))
                    category_style = ParagraphStyle(
                        'Category',
                        parent=body_style,
                        fontSize=11,
                        textColor=colors.HexColor('#1a237e'),
                        fontName='Helvetica-Bold',
                        spaceAfter=6,
                        spaceBefore=8
                    )
                    elements.append(Paragraph(rec_text, category_style))
                    current_category = rec_text
                else:
                    # Regular recommendation
                    rec_clean = rec_text.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
                    elements.append(Paragraph(f"• {rec_clean}", bullet_style))
            
            elements.append(Spacer(1, 0.2*inch))
        
        # Diet Suggestions
        diet_suggestions = data.get('diet_suggestions', {})
        if diet_suggestions:
            elements.append(Paragraph("🥗 DIETARY GUIDELINES", section_heading))
            elements.append(Spacer(1, 0.1*inch))
            
            if diet_suggestions.get('foods_to_favor'):
                elements.append(Paragraph("<b>✅ Foods to Favor:</b>", body_style))
                for food in diet_suggestions['foods_to_favor']:
                    elements.append(Paragraph(f"• {food}", bullet_style))
                elements.append(Spacer(1, 0.1*inch))
            
            if diet_suggestions.get('foods_to_avoid'):
                elements.append(Paragraph("<b>❌ Foods to Avoid:</b>", body_style))
                for food in diet_suggestions['foods_to_avoid']:
                    elements.append(Paragraph(f"• {food}", bullet_style))
                elements.append(Spacer(1, 0.1*inch))
            
            if diet_suggestions.get('meal_timing'):
                elements.append(Paragraph("<b>⏰ Meal Timing:</b>", body_style))
                for timing in diet_suggestions['meal_timing']:
                    elements.append(Paragraph(f"• {timing}", bullet_style))
            
            elements.append(Spacer(1, 0.2*inch))
        
        # Lifestyle Tips
        lifestyle_tips = data.get('lifestyle_tips', {})
        if lifestyle_tips:
            elements.append(Paragraph("🧘 LIFESTYLE MODIFICATIONS", section_heading))
            elements.append(Spacer(1, 0.1*inch))
            
            if lifestyle_tips.get('daily_routine'):
                elements.append(Paragraph("<b>📅 Daily Routine (Dinacharya):</b>", body_style))
                for routine in lifestyle_tips['daily_routine']:
                    elements.append(Paragraph(f"• {routine}", bullet_style))
                elements.append(Spacer(1, 0.1*inch))
            
            if lifestyle_tips.get('exercise'):
                elements.append(Paragraph("<b>💪 Exercise Recommendations:</b>", body_style))
                for exercise in lifestyle_tips['exercise']:
                    elements.append(Paragraph(f"• {exercise}", bullet_style))
                elements.append(Spacer(1, 0.1*inch))
            
            if lifestyle_tips.get('seasonal_care'):
                elements.append(Paragraph("<b>🌦️ Seasonal Care (Ritucharya):</b>", body_style))
                for care in lifestyle_tips['seasonal_care']:
                    elements.append(Paragraph(f"• {care}", bullet_style))
            
            elements.append(Spacer(1, 0.3*inch))
        
        # Disclaimer Box
        disclaimer_style = ParagraphStyle(
            'Disclaimer',
            parent=styles['Normal'],
            fontSize=8,
            textColor=colors.HexColor('#d32f2f'),
            leftIndent=10,
            rightIndent=10,
            fontName='Helvetica',
            alignment=TA_JUSTIFY,
            backColor=colors.HexColor('#ffebee'),
            borderPadding=10
        )
        elements.append(Paragraph(
            "<b>⚠️ IMPORTANT MEDICAL DISCLAIMER:</b> This report provides educational and preventive health insights based on Ayurvedic principles only. "
            "It is NOT a medical diagnosis and should not replace professional medical advice, diagnosis, or treatment. "
            "Always consult qualified healthcare professionals for medical concerns. The Tridosha Intelligence Engine™ is designed for wellness education purposes.",
            disclaimer_style
        ))
        
        elements.append(Spacer(1, 0.3*inch))
        
        # Footer
        footer_style = ParagraphStyle(
            'Footer',
            parent=styles['Normal'],
            fontSize=9,
            alignment=TA_CENTER,
            textColor=colors.HexColor('#666666'),
            fontName='Helvetica'
        )
        elements.append(Paragraph("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━", footer_style))
        elements.append(Paragraph("🌿 AyurAI Veda™ | Ancient Wisdom. Intelligent Health.", footer_style))
        elements.append(Paragraph("Powered by Tridosha Intelligence Engine™ | NEP 2020 Aligned", footer_style))
        timestamp = datetime.now().strftime('%d %B %Y at %I:%M %p')
        elements.append(Paragraph(f"Report Generated: {timestamp}", footer_style))
        
        # Build PDF
        doc.build(elements)
        
        # Get PDF data
        pdf_data = buffer.getvalue()
        buffer.close()
        
        # Create new buffer with PDF data
        output = io.BytesIO(pdf_data)
        output.seek(0)
        
        return send_file(
            output,
            mimetype='application/pdf',
            as_attachment=True,
            download_name=f'AyurAI_Report_{datetime.now().strftime("%Y%m%d_%H%M%S")}.pdf'
        )
        
    except Exception as e:
        print(f"PDF generation error: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': f'Failed to generate PDF: {str(e)}'}), 500

# ============= ANALYSIS FUNCTIONS =============

def analyze_tridosha(data):
    """Basic Tridosha analysis"""
    vata_score = pitta_score = kapha_score = 0
    
    # Body build
    if data.get('body_build') == 'thin': vata_score += 25
    elif data.get('body_build') == 'medium': pitta_score += 25
    elif data.get('body_build') == 'heavy': kapha_score += 25
    
    # Skin
    if data.get('skin') == 'dry': vata_score += 20
    elif data.get('skin') == 'oily': pitta_score += 20
    elif data.get('skin') == 'smooth': kapha_score += 20
    
    # Appetite
    if data.get('appetite') == 'variable': vata_score += 15
    elif data.get('appetite') == 'strong': pitta_score += 15
    elif data.get('appetite') == 'steady': kapha_score += 15
    
    # Digestion
    if data.get('digestion') == 'irregular': vata_score += 20
    elif data.get('digestion') == 'quick': pitta_score += 20
    elif data.get('digestion') == 'slow': kapha_score += 20
    
    # Sleep
    if data.get('sleep') == 'light': vata_score += 10
    elif data.get('sleep') == 'moderate': pitta_score += 10
    elif data.get('sleep') == 'deep': kapha_score += 10
    
    # Energy
    if data.get('energy') == 'variable': vata_score += 10
    elif data.get('energy') == 'moderate': pitta_score += 10
    elif data.get('energy') == 'steady': kapha_score += 10
    
    # Calculate percentages
    total = vata_score + pitta_score + kapha_score
    if total > 0:
        vata_percent = round((vata_score / total) * 100)
        pitta_percent = round((pitta_score / total) * 100)
        kapha_percent = round((kapha_score / total) * 100)
    else:
        vata_percent = pitta_percent = kapha_percent = 33
    
    scores = {'vata': vata_percent, 'pitta': pitta_percent, 'kapha': kapha_percent}
    dominant = max(scores, key=scores.get)
    
    # Risk level
    max_score = max(vata_percent, pitta_percent, kapha_percent)
    if max_score >= 50: risk = 'High'
    elif max_score >= 40: risk = 'Moderate'
    else: risk = 'Low'
    
    return {
        'dominant': dominant.capitalize(),
        'scores': scores,
        'risk': risk,
        'recommendations': get_recommendations(dominant),
        'timestamp': datetime.now().isoformat()
    }

def analyze_clinical(data):
    """Advanced Clinical Assessment with ML-Ready Logic Framework"""
    vata_score = pitta_score = kapha_score = 0
    reasoning = []
    ama_indicators = []
    
    # STEP 1: FEATURE CLASSIFICATION WITH WEIGHTED SCORING
    
    # Body Frame (Strong match = +3)
    if data.get('body_frame') == 'thin': 
        vata_score += 3
        reasoning.append("Thin body frame indicates Vata dominance (light, mobile qualities)")
    elif data.get('body_frame') == 'medium': 
        pitta_score += 3
        reasoning.append("Medium body frame indicates Pitta constitution (balanced structure)")
    elif data.get('body_frame') == 'heavy': 
        kapha_score += 3
        reasoning.append("Heavy body frame indicates Kapha dominance (stable, heavy qualities)")
    
    # Body Build
    if data.get('body_build') == 'lean': vata_score += 3
    elif data.get('body_build') == 'muscular': pitta_score += 3
    elif data.get('body_build') == 'stocky': kapha_score += 3
    
    # Muscle Tone
    if data.get('muscle_tone') == 'low': vata_score += 2
    elif data.get('muscle_tone') == 'medium': pitta_score += 2
    elif data.get('muscle_tone') == 'high': kapha_score += 2
    
    # Weight Tendency
    if data.get('weight_tendency') == 'hard_to_gain': 
        vata_score += 3
        reasoning.append("Difficulty gaining weight suggests high Vata metabolism")
    elif data.get('weight_tendency') == 'stable': pitta_score += 2
    elif data.get('weight_tendency') == 'easy_to_gain': 
        kapha_score += 3
        reasoning.append("Easy weight gain indicates Kapha tendency")
    
    # Joints
    if data.get('joints') == 'prominent': vata_score += 2
    elif data.get('joints') == 'normal': pitta_score += 2
    elif data.get('joints') == 'well_covered': kapha_score += 2
    
    # Veins
    if data.get('veins') == 'prominent': vata_score += 2
    elif data.get('veins') == 'visible': pitta_score += 2
    elif data.get('veins') == 'hidden': kapha_score += 2
    
    # Bone Structure
    if data.get('bone_structure') == 'light': vata_score += 3
    elif data.get('bone_structure') == 'medium': pitta_score += 3
    elif data.get('bone_structure') == 'heavy': kapha_score += 3
    
    # Skin Type (Critical indicator)
    if data.get('skin_type') == 'dry': 
        vata_score += 3
        reasoning.append("Dry skin is a primary Vata characteristic (dry, rough qualities)")
    elif data.get('skin_type') == 'sensitive': 
        pitta_score += 3
        reasoning.append("Sensitive skin indicates Pitta imbalance (hot, sharp qualities)")
    elif data.get('skin_type') == 'oily': 
        kapha_score += 3
        reasoning.append("Oily skin indicates Kapha dominance (oily, smooth qualities)")
    
    # Skin Texture
    if data.get('skin_texture') == 'rough': vata_score += 2
    elif data.get('skin_texture') == 'soft': pitta_score += 2
    elif data.get('skin_texture') == 'smooth': kapha_score += 2
    
    # Skin Temperature
    if data.get('skin_temperature') == 'cold': vata_score += 2
    elif data.get('skin_temperature') == 'warm': pitta_score += 2
    
    # Complexion
    if data.get('complexion') == 'dark': pitta_score += 1
    elif data.get('complexion') == 'fair': pitta_score += 1
    elif data.get('complexion') == 'pale': vata_score += 1
    
    # Skin Luster
    if data.get('skin_luster') == 'dull': vata_score += 2
    elif data.get('skin_luster') == 'radiant': pitta_score += 2
    elif data.get('skin_luster') == 'glowing': kapha_score += 2
    
    # Hair Type
    if data.get('hair_type') == 'dry': vata_score += 2
    elif data.get('hair_type') == 'thin': vata_score += 2
    elif data.get('hair_type') == 'thick': kapha_score += 2
    
    # Hair Texture
    if data.get('hair_texture') == 'rough': vata_score += 2
    elif data.get('hair_texture') == 'fine': pitta_score += 2
    elif data.get('hair_texture') == 'smooth': kapha_score += 2
    
    # Nails
    if data.get('nails') == 'brittle': vata_score += 2
    elif data.get('nails') == 'soft': pitta_score += 2
    elif data.get('nails') == 'strong': kapha_score += 2
    
    # STEP 4: AGNI ANALYSIS (Critical for diagnosis)
    agni_type = 'Sama Agni'
    
    # Appetite
    if data.get('appetite') == 'irregular': 
        vata_score += 3
        agni_type = 'Vishama Agni (Irregular)'
        ama_indicators.append('irregular appetite')
        reasoning.append("Irregular appetite indicates Vishama Agni - Vata imbalance in digestion")
    elif data.get('appetite') == 'strong': 
        pitta_score += 3
        agni_type = 'Tikshna Agni (Sharp)'
        reasoning.append("Strong appetite indicates Tikshna Agni - Pitta-dominant digestion")
    elif data.get('appetite') == 'low': 
        kapha_score += 3
        agni_type = 'Manda Agni (Slow)'
        ama_indicators.append('low appetite')
        reasoning.append("Low appetite indicates Manda Agni - Kapha-type sluggish digestion")
    
    # Hunger
    if data.get('hunger') == 'variable': vata_score += 2
    elif data.get('hunger') == 'intense': pitta_score += 2
    elif data.get('hunger') == 'mild': kapha_score += 2
    
    # Thirst
    if data.get('thirst') == 'variable': vata_score += 2
    elif data.get('thirst') == 'high': pitta_score += 2
    elif data.get('thirst') == 'low': kapha_score += 2
    
    # Digestion
    if data.get('digestion') == 'irregular': 
        vata_score += 3
        ama_indicators.append('irregular digestion')
    elif data.get('digestion') == 'fast': pitta_score += 3
    elif data.get('digestion') == 'slow': 
        kapha_score += 3
        ama_indicators.append('slow digestion')
    
    # Bowel
    if data.get('bowel') == 'constipation': 
        vata_score += 3
        ama_indicators.append('constipation')
    elif data.get('bowel') == 'loose': pitta_score += 3
    elif data.get('bowel') in ['regular', 'heavy']: kapha_score += 2
    
    # Gas (AMA indicator)
    if data.get('gas') == 'frequent': 
        vata_score += 2
        ama_indicators.append('frequent gas/bloating')
    elif data.get('gas') == 'occasional': vata_score += 1
    
    # Food Preference
    if data.get('food_preference') == 'warm': vata_score += 2
    elif data.get('food_preference') == 'cold': pitta_score += 2
    elif data.get('food_preference') == 'spicy': kapha_score += 2
    
    # Metabolism
    if data.get('metabolism') == 'fast': vata_score += 2
    elif data.get('metabolism') == 'moderate': pitta_score += 2
    elif data.get('metabolism') == 'slow': kapha_score += 2
    
    # Sleep Pattern
    if data.get('sleep_pattern') == 'light': vata_score += 3
    elif data.get('sleep_pattern') == 'moderate': pitta_score += 3
    elif data.get('sleep_pattern') == 'deep': kapha_score += 3
    
    # Sleep Duration
    if data.get('sleep_duration') == 'less_6': vata_score += 2
    elif data.get('sleep_duration') == '6_8': pitta_score += 2
    elif data.get('sleep_duration') == 'more_8': kapha_score += 2
    
    # Dreams
    if data.get('dreams') == 'active': vata_score += 2
    elif data.get('dreams') == 'colorful': pitta_score += 2
    elif data.get('dreams') == 'few': kapha_score += 2
    
    # Energy Level
    if data.get('energy_level') == 'variable': vata_score += 3
    elif data.get('energy_level') == 'moderate': pitta_score += 3
    elif data.get('energy_level') == 'steady': kapha_score += 3
    
    # Stamina
    if data.get('stamina') == 'low': vata_score += 2
    elif data.get('stamina') == 'medium': pitta_score += 2
    elif data.get('stamina') == 'high': kapha_score += 2
    
    # Physical Activity
    if data.get('physical_activity') == 'restless': vata_score += 2
    elif data.get('physical_activity') == 'moderate': pitta_score += 2
    elif data.get('physical_activity') == 'slow': kapha_score += 2
    
    # Exercise Tolerance
    if data.get('exercise_tolerance') == 'low': vata_score += 2
    elif data.get('exercise_tolerance') == 'high': pitta_score += 2
    elif data.get('exercise_tolerance') == 'moderate': kapha_score += 2
    
    # Sweat
    if data.get('sweat') == 'minimal': vata_score += 2
    elif data.get('sweat') == 'profuse': pitta_score += 2
    elif data.get('sweat') == 'moderate': kapha_score += 2
    
    # Body Odor
    if data.get('body_odor') == 'minimal': vata_score += 1
    elif data.get('body_odor') == 'strong': pitta_score += 2
    elif data.get('body_odor') == 'mild': kapha_score += 1
    
    # Weather Preference
    if data.get('weather_preference') == 'warm': vata_score += 2
    elif data.get('weather_preference') == 'cool': pitta_score += 2
    
    # Season Discomfort
    if data.get('season_discomfort') == 'winter': vata_score += 2
    elif data.get('season_discomfort') == 'summer': pitta_score += 2
    elif data.get('season_discomfort') == 'spring': kapha_score += 2
    
    # Immunity
    if data.get('immunity') == 'weak': vata_score += 2
    elif data.get('immunity') == 'moderate': pitta_score += 2
    elif data.get('immunity') == 'strong': kapha_score += 2
    
    # Disease Tendency
    if data.get('disease_tendency') == 'nervous': vata_score += 3
    elif data.get('disease_tendency') == 'inflammatory': pitta_score += 3
    elif data.get('disease_tendency') == 'congestion': kapha_score += 3
    
    # Speech Pace
    if data.get('speech_pace') == 'fast': vata_score += 2
    elif data.get('speech_pace') == 'moderate': pitta_score += 2
    elif data.get('speech_pace') == 'slow': kapha_score += 2
    
    # Voice Quality
    if data.get('voice_quality') == 'weak': vata_score += 2
    elif data.get('voice_quality') == 'sharp': pitta_score += 2
    elif data.get('voice_quality') == 'deep': kapha_score += 2
    
    # Communication
    if data.get('communication') == 'talkative': vata_score += 2
    elif data.get('communication') == 'precise': pitta_score += 2
    elif data.get('communication') == 'reserved': kapha_score += 2
    
    # Movements
    if data.get('movements') == 'quick': vata_score += 2
    elif data.get('movements') == 'purposeful': pitta_score += 2
    elif data.get('movements') == 'slow': kapha_score += 2
    
    # Mental State
    if data.get('mental_state') == 'anxious': vata_score += 3
    elif data.get('mental_state') == 'focused': pitta_score += 3
    elif data.get('mental_state') == 'calm': kapha_score += 3
    
    # Memory
    if data.get('memory') == 'quick_forget': vata_score += 2
    elif data.get('memory') == 'sharp': pitta_score += 2
    elif data.get('memory') == 'slow_retain': kapha_score += 2
    
    # Learning
    if data.get('learning') == 'quick': vata_score += 2
    elif data.get('learning') == 'moderate': pitta_score += 2
    elif data.get('learning') == 'slow': kapha_score += 2
    
    # Concentration
    if data.get('concentration') == 'poor': vata_score += 2
    elif data.get('concentration') == 'good': pitta_score += 2
    elif data.get('concentration') == 'excellent': kapha_score += 2
    
    # Decision Making
    if data.get('decision_making') == 'quick': vata_score += 2
    elif data.get('decision_making') == 'analytical': pitta_score += 2
    elif data.get('decision_making') == 'slow': kapha_score += 2
    
    # Emotional Response
    if data.get('emotional_response') == 'fearful': vata_score += 3
    elif data.get('emotional_response') == 'angry': pitta_score += 3
    elif data.get('emotional_response') == 'attached': kapha_score += 3
    
    # Stress Response
    if data.get('stress_response') == 'anxious': vata_score += 3
    elif data.get('stress_response') == 'irritable': pitta_score += 3
    elif data.get('stress_response') == 'withdrawn': kapha_score += 3
    
    # Additional characteristics
    if data.get('teeth_gums') == 'weak': vata_score += 2
    elif data.get('teeth_gums') == 'normal': pitta_score += 2
    elif data.get('teeth_gums') == 'strong': kapha_score += 2
    
    if data.get('eyes_appearance') == 'small': vata_score += 2
    elif data.get('eyes_appearance') == 'medium': pitta_score += 2
    elif data.get('eyes_appearance') == 'large': kapha_score += 2
    
    if data.get('lips_condition') == 'dry': vata_score += 2
    elif data.get('lips_condition') == 'normal': pitta_score += 2
    elif data.get('lips_condition') == 'moist': kapha_score += 2
    
    if data.get('temp_regulation') == 'poor': vata_score += 2
    elif data.get('temp_regulation') == 'moderate': pitta_score += 2
    elif data.get('temp_regulation') == 'good': kapha_score += 2
    
    if data.get('pain_tolerance') == 'low': vata_score += 2
    elif data.get('pain_tolerance') == 'medium': pitta_score += 2
    elif data.get('pain_tolerance') == 'high': kapha_score += 2
    
    if data.get('healing_speed') == 'slow': vata_score += 2
    elif data.get('healing_speed') == 'moderate': pitta_score += 2
    elif data.get('healing_speed') == 'fast': kapha_score += 2
    
    # STEP 2: DOSHA SCORING & NORMALIZATION
    total = vata_score + pitta_score + kapha_score
    if total > 0:
        vata_percent = round((vata_score / total) * 100)
        pitta_percent = round((pitta_score / total) * 100)
        kapha_percent = round((kapha_score / total) * 100)
    else:
        vata_percent = pitta_percent = kapha_percent = 33
    
    scores = {'vata': vata_percent, 'pitta': pitta_percent, 'kapha': kapha_percent}
    
    # STEP 3: DOSHA CLASSIFICATION
    sorted_doshas = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    dominant_dosha = sorted_doshas[0][0]
    second_dosha = sorted_doshas[1][0]
    
    if sorted_doshas[0][1] > 50:
        prakriti = dominant_dosha.capitalize()
    elif sorted_doshas[1][1] >= 25:
        prakriti = f"{dominant_dosha.capitalize()}-{second_dosha.capitalize()}"
    else:
        prakriti = dominant_dosha.capitalize()
    
    # STEP 5: AMA DETECTION
    if len(ama_indicators) == 0:
        ama_status = 'None'
    elif len(ama_indicators) <= 2:
        ama_status = 'Mild'
    elif len(ama_indicators) <= 4:
        ama_status = 'Moderate'
    else:
        ama_status = 'High'
    
    if ama_status != 'None':
        reasoning.append(f"Ama (toxins) detected: {', '.join(ama_indicators)}")
    
    # STEP 6: VIKRITI (IMBALANCE)
    vikriti = dominant_dosha.capitalize()
    max_score = sorted_doshas[0][1]
    
    if max_score >= 50:
        reasoning.append(f"{vikriti} is significantly aggravated (>{max_score}%)")
    
    # STEP 7: RISK LEVEL (Conservative approach)
    if max_score >= 55 and len(ama_indicators) >= 3:
        risk = 'High'
    elif max_score >= 45 or len(ama_indicators) >= 2:
        risk = 'Moderate'
    else:
        risk = 'Low'
    
    # Generate clinical justification
    justification = f"Based on 59-point clinical assessment: {prakriti} constitution identified. " + " ".join(reasoning[:3])
    
    return {
        'dominant': prakriti,
        'scores': scores,
        'risk': risk,
        'dosha_state': 'Balanced' if max_score < 45 else 'Imbalanced',
        'agni_state': agni_type,
        'ama_status': ama_status,
        'vikriti': vikriti,
        'justification': justification,
        'reasoning': reasoning[:5],
        'recommendations': get_clinical_recommendations(dominant_dosha, ama_status),
        'diet_suggestions': get_diet_suggestions(dominant_dosha),
        'lifestyle_tips': get_lifestyle_tips(dominant_dosha),
        'timestamp': datetime.now().isoformat()
    }

def analyze_comprehensive(data):
    """Comprehensive 59-question analysis"""
    vata_count = pitta_count = kapha_count = 0
    total_questions = 0
    
    for key, value in data.items():
        if key.startswith('q') and value:
            total_questions += 1
            if value == 'A': vata_count += 1
            elif value == 'B': pitta_count += 1
            elif value == 'C': kapha_count += 1
    
    if total_questions == 0:
        return {'error': 'No valid responses found'}
    
    vata_percent = int((vata_count / total_questions) * 100)
    pitta_percent = int((pitta_count / total_questions) * 100)
    kapha_percent = int((kapha_count / total_questions) * 100)
    
    scores = {'vata': vata_percent, 'pitta': pitta_percent, 'kapha': kapha_percent}
    dominant = max(scores, key=scores.get)
    
    max_score = max(vata_percent, pitta_percent, kapha_percent)
    if max_score >= 50: risk = 'High'
    elif max_score >= 40: risk = 'Moderate'
    else: risk = 'Low'
    
    return {
        'dominant': dominant.capitalize(),
        'scores': scores,
        'risk': risk,
        'assessment_type': 'Comprehensive Prakriti Assessment',
        'total_questions': total_questions,
        'dosha_state': 'Balanced' if max_score < 45 else 'Imbalanced',
        'recommendations': get_recommendations(dominant),
        'diet_suggestions': get_diet_suggestions(dominant),
        'lifestyle_tips': get_lifestyle_tips(dominant),
        'timestamp': datetime.now().isoformat()
    }

# ============= RECOMMENDATION FUNCTIONS =============

def get_clinical_recommendations(dominant, ama_status):
    """Clinical recommendations based on dosha and ama status"""
    base_recommendations = {
        'vata': [
            'Establish regular daily routine (Dinacharya) - wake, eat, sleep at fixed times',
            'Consume warm, cooked, moist foods with healthy fats (ghee, sesame oil)',
            'Practice daily oil massage (Abhyanga) with warm sesame oil',
            'Ensure 7-8 hours of quality sleep in warm, quiet environment',
            'Avoid cold, dry, raw foods and excessive stimulants',
            'Practice gentle, grounding yoga and meditation (avoid excessive cardio)'
        ],
        'pitta': [
            'Avoid spicy, hot, acidic, and fermented foods',
            'Stay cool - avoid excessive heat, sun exposure, and hot environments',
            'Practice moderation in all activities - avoid overwork and competition',
            'Consume cooling foods: cucumber, coconut, sweet fruits, leafy greens',
            'Practice cooling pranayama (Sheetali, Sheetkari) and calming meditation',
            'Maintain work-life balance and avoid perfectionism'
        ],
        'kapha': [
            'Engage in regular vigorous exercise (minimum 45 min daily)',
            'Eat light, warm, spicy foods with pungent and bitter tastes',
            'Avoid heavy, oily, sweet, and dairy-rich foods',
            'Wake up early before 6 AM and avoid daytime sleeping',
            'Stay mentally and physically active - avoid sedentary lifestyle',
            'Practice energizing pranayama (Bhastrika, Kapalabhati)'
        ]
    }
    
    recommendations = base_recommendations.get(dominant, base_recommendations['vata']).copy()
    
    # Add ama-specific recommendations
    if ama_status == 'High':
        recommendations.insert(0, 'URGENT: Undergo Panchakarma detoxification under Ayurvedic supervision')
        recommendations.insert(1, 'Fast or eat very light meals (kitchari) until digestion improves')
    elif ama_status == 'Moderate':
        recommendations.insert(0, 'Focus on improving Agni - use digestive spices (ginger, cumin, fennel)')
        recommendations.insert(1, 'Avoid heavy meals and eat only when truly hungry')
    elif ama_status == 'Mild':
        recommendations.insert(0, 'Drink warm water with ginger throughout the day')
    
    return recommendations

def get_recommendations(dominant):
    recommendations = {
        'vata': [
            'Follow regular daily routine',
            'Eat warm, cooked foods',
            'Practice oil massage (abhyanga)',
            'Get adequate sleep (7-8 hours)',
            'Avoid cold, dry foods',
            'Practice gentle yoga and meditation'
        ],
        'pitta': [
            'Avoid spicy, hot foods',
            'Stay cool and avoid overheating',
            'Practice moderation in activities',
            'Eat cooling foods like cucumber, coconut',
            'Avoid excessive sun exposure',
            'Practice calming pranayama'
        ],
        'kapha': [
            'Engage in regular vigorous exercise',
            'Eat light, warm, spicy foods',
            'Avoid heavy, oily foods',
            'Wake up early (before 6 AM)',
            'Stay active and avoid sedentary lifestyle',
            'Practice energizing breathing exercises'
        ]
    }
    return recommendations.get(dominant, recommendations['vata'])

def get_diet_suggestions(dominant):
    diet_plans = {
        'vata': {
            'foods_to_favor': ['Warm cooked grains', 'Sweet fruits', 'Healthy fats', 'Warm spices'],
            'foods_to_avoid': ['Cold foods', 'Raw vegetables', 'Dry foods', 'Stimulants'],
            'meal_timing': ['Regular meal times', 'Largest meal at lunch', 'Warm environment']
        },
        'pitta': {
            'foods_to_favor': ['Cooling foods', 'Sweet fruits', 'Leafy greens', 'Cooling spices'],
            'foods_to_avoid': ['Spicy foods', 'Sour foods', 'Salty foods', 'Alcohol'],
            'meal_timing': ['Never skip meals', 'Cool environment', 'Avoid eating when stressed']
        },
        'kapha': {
            'foods_to_favor': ['Light foods', 'Warming spices', 'Astringent fruits', 'Light proteins'],
            'foods_to_avoid': ['Heavy foods', 'Sweet foods', 'Dairy products', 'Cold foods'],
            'meal_timing': ['Light breakfast', 'Main meal at lunch', 'Early light dinner']
        }
    }
    return diet_plans.get(dominant, diet_plans['vata'])

def get_lifestyle_tips(dominant):
    tips = {
        'vata': {
            'daily_routine': ['Wake at 6 AM', 'Oil massage', 'Regular meals', 'Sleep by 10 PM'],
            'seasonal_care': ['Extra care in autumn', 'Stay warm', 'Avoid cold winds'],
            'exercise': ['Gentle yoga', 'Walking', 'Swimming', 'Avoid excessive cardio']
        },
        'pitta': {
            'daily_routine': ['Wake at 5:30 AM', 'Cool shower', 'Moderate exercise', 'Sleep by 10:30 PM'],
            'seasonal_care': ['Extra care in summer', 'Stay cool', 'Avoid midday sun'],
            'exercise': ['Swimming', 'Yoga in cool place', 'Moderate cardio', 'Avoid competition']
        },
        'kapha': {
            'daily_routine': ['Wake at 5 AM', 'Vigorous exercise', 'Light meals', 'Stay active'],
            'seasonal_care': ['Extra care in spring', 'Increase activity', 'Reduce heavy foods'],
            'exercise': ['High-intensity cardio', 'Weight training', 'Running', 'Dynamic yoga']
        }
    }
    return tips.get(dominant, tips['vata'])

# ============= CHATBOT FUNCTION =============

def get_chatbot_response(message):
    """Enhanced chatbot with comprehensive responses"""
    
    if 'tridosha' in message or 'tri dosha' in message or 'three dosha' in message:
        return """<strong>Tridosha - The Three Fundamental Energies</strong><br><br>
Tridosha is the foundation of Ayurveda, consisting of three biological energies (doshas) that govern all physical and mental processes:<br><br>
<strong>🌬️ Vata (Air + Space)</strong><br>
• Governs: Movement, breathing, circulation, nervous system<br>
• Qualities: Dry, light, cold, mobile, irregular<br>
• Imbalance: Anxiety, insomnia, constipation, dry skin<br>
• Balance: Warm foods, routine, oil massage<br><br>
<strong>🔥 Pitta (Fire + Water)</strong><br>
• Governs: Metabolism, digestion, body temperature, intelligence<br>
• Qualities: Hot, sharp, intense, oily, penetrating<br>
• Imbalance: Acidity, inflammation, anger, skin rashes<br>
• Balance: Cooling foods, meditation, avoid spicy items<br><br>
<strong>🌊 Kapha (Water + Earth)</strong><br>
• Governs: Structure, stability, lubrication, immunity<br>
• Qualities: Heavy, slow, cool, oily, stable<br>
• Imbalance: Weight gain, lethargy, congestion<br>
• Balance: Light foods, exercise, avoid dairy<br><br>
Everyone has a unique combination of these three doshas, called their <strong>Prakriti</strong> (constitution). Take our AI Health Assessment to discover your dominant dosha! 🌿"""
    
    elif 'vata' in message:
        return "Vata dosha (Air + Space) governs movement, creativity, and the nervous system. When balanced, it promotes creativity and flexibility. When imbalanced, it can cause anxiety, dry skin, and digestive issues. Balance vata with warm foods, regular routines, and oil massage."
    
    elif 'pitta' in message:
        return "Pitta dosha (Fire + Water) governs metabolism and is associated with fire and water elements. When balanced, it promotes good digestion and sharp intellect. When imbalanced, it can cause acidity, anger, and skin inflammation. Balance pitta with cooling foods and avoiding excessive heat."
    
    elif 'kapha' in message:
        return "Kapha dosha (Water + Earth) governs structure and is associated with water and earth elements. When balanced, it provides strength and immunity. When imbalanced, it can cause weight gain, congestion, and lethargy. Balance kapha with light foods, regular exercise, and staying active."
    
    elif 'diet' in message or 'food' in message:
        return "Ayurvedic diet is based on your dosha constitution. Vata types need warm, moist foods. Pitta types need cooling, less spicy foods. Kapha types need light, warm, spicy foods. Eat fresh, seasonal foods and avoid processed items."
    
    elif 'yoga' in message or 'exercise' in message:
        return "Yoga is an integral part of Ayurveda. Vata types benefit from gentle, grounding poses. Pitta types need cooling, moderate practices. Kapha types need energizing, vigorous sequences. Practice regularly for best results."
    
    elif 'sleep' in message or 'insomnia' in message:
        return "Good sleep is crucial for health. Vata types need 7-8 hours with regular bedtime. Pitta types need 6-7 hours in cool environment. Kapha types need 6-7 hours and should wake early. Avoid screens before bed."
    
    elif 'stress' in message or 'anxiety' in message:
        return "Ayurvedic stress management: Regular routine, adequate sleep, meditation, pranayama (breathing exercises), Abhyanga (oil massage), and adaptogenic herbs like Ashwagandha. Stress is seen as Vata imbalance affecting the mind."
    
    elif 'digestion' in message or 'agni' in message:
        return "To improve digestion (Agni): Eat at regular times, use digestive spices (ginger, cumin, fennel), avoid overeating, drink warm water, and walk after meals. Strong Agni is key to health in Ayurveda."
    
    elif 'meditation' in message:
        return "Meditation balances all doshas. Vata types benefit from grounding meditations. Pitta types need cooling, calming practices. Kapha types benefit from energizing techniques. Start with 10-15 minutes daily."
    
    elif 'herb' in message or 'ashwagandha' in message or 'turmeric' in message:
        return "Key Ayurvedic herbs: Ashwagandha (stress relief, strength), Turmeric (anti-inflammatory), Tulsi (immunity, stress), Amla (Vitamin C, rejuvenation), Brahmi (memory, clarity), and Neem (blood purification)."
    
    else:
        return """Hello! I'm AyurVaani, your Ayurvedic wellness assistant. I can help you with:<br><br>
🌬️ Understanding Vata, Pitta, and Kapha doshas<br>
🍽️ Personalized diet recommendations<br>
🌿 Herbal remedies and natural treatments<br>
🧘 Yoga and pranayama practices<br>
😌 Stress management and sleep improvement<br>
🔥 Digestive health and Agni strengthening<br><br>
What would you like to know about Ayurveda today?"""

# ============= EMAIL FUNCTIONS =============

def send_feedback_email(data):
    """Send feedback email to admin"""
    try:
        smtp_server = "smtp.gmail.com"
        smtp_port = 587
        sender_email = os.getenv('SENDER_EMAIL', 'zjay5398@gmail.com')
        sender_password = os.getenv('GMAIL_APP_PASSWORD', '')
        recipient_email = os.getenv('ADMIN_EMAIL', 'zjay5398@gmail.com')
        
        if not sender_password:
            print("⚠ Gmail App Password not configured")
            return False
        
        msg = MIMEMultipart('alternative')
        msg['From'] = sender_email
        msg['To'] = recipient_email
        msg['Subject'] = f"🌿 AyurAI Veda Feedback from {data['name']} - {data['designation']}"
        
        html_body = f"""
        <html>
        <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
            <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
                <div style="background: linear-gradient(135deg, #FF9933, #138808); padding: 20px; border-radius: 8px; margin-bottom: 20px;">
                    <h2 style="color: white; margin: 0; text-align: center;">🕉️ AyurAI Veda Feedback</h2>
                    <p style="color: white; margin: 5px 0 0 0; text-align: center; opacity: 0.9;">New feedback received</p>
                </div>
                
                <div style="background: #f8f9fa; padding: 15px; border-radius: 6px; margin-bottom: 20px;">
                    <h3 style="color: #1a237e; margin-top: 0;">📋 Contact Information</h3>
                    <table style="width: 100%; border-collapse: collapse;">
                        <tr>
                            <td style="padding: 8px 0; font-weight: bold; width: 30%;">👤 Name:</td>
                            <td style="padding: 8px 0;">{data['name']}</td>
                        </tr>
                        <tr>
                            <td style="padding: 8px 0; font-weight: bold;">📱 Mobile:</td>
                            <td style="padding: 8px 0;">{data['mobile']}</td>
                        </tr>
                        <tr>
                            <td style="padding: 8px 0; font-weight: bold;">🏢 Institute:</td>
                            <td style="padding: 8px 0;">{data['institute']}</td>
                        </tr>
                        <tr>
                            <td style="padding: 8px 0; font-weight: bold;">💼 Designation:</td>
                            <td style="padding: 8px 0;">{data['designation']}</td>
                        </tr>
                        <tr>
                            <td style="padding: 8px 0; font-weight: bold;">📅 Submitted:</td>
                            <td style="padding: 8px 0;">{datetime.now().strftime('%d %B %Y at %I:%M %p')}</td>
                        </tr>
                    </table>
                </div>
                
                <div style="background: #fff; padding: 20px; border: 1px solid #ddd; border-radius: 6px; margin-bottom: 20px;">
                    <h3 style="color: #1a237e; margin-top: 0;">💬 Feedback Message</h3>
                    <div style="background: #f1f3f4; padding: 15px; border-radius: 4px; border-left: 4px solid #FF9933;">
                        <p style="margin: 0; white-space: pre-wrap;">{data['feedback']}</p>
                    </div>
                    <p style="font-size: 12px; color: #666; margin-top: 10px;">Character count: {len(data['feedback'])}/2000</p>
                </div>
                
                <div style="text-align: center; margin-top: 30px; padding: 20px; background: #1a237e; border-radius: 6px;">
                    <p style="color: white; margin: 0; font-size: 14px;">🌿 <strong>AyurAI Veda</strong> | Ancient Wisdom. Intelligent Health.</p>
                    <p style="color: #ccc; margin: 5px 0 0 0; font-size: 12px;">Powered by Tridosha Intelligence Engine™</p>
                </div>
            </div>
        </body>
        </html>
        """
        
        msg.attach(MIMEText(html_body, 'html'))
        
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, recipient_email, msg.as_string())
        server.quit()
        
        print(f"✅ Feedback email sent to {recipient_email}")
        return True
        
    except Exception as e:
        print(f"❌ Email error: {str(e)}")
        return False

def send_assessment_report_email(recipient_email, report_data):
    """Send assessment report to user's email"""
    try:
        smtp_server = "smtp.gmail.com"
        smtp_port = 587
        sender_email = os.getenv('SENDER_EMAIL', 'zjay5398@gmail.com')
        sender_password = os.getenv('GMAIL_APP_PASSWORD', '')
        
        if not sender_password:
            print("⚠ Gmail App Password not configured")
            return False
        
        msg = MIMEMultipart('alternative')
        msg['From'] = f"AyurAI Veda <{sender_email}>"
        msg['To'] = recipient_email
        msg['Subject'] = f"🌿 Your AyurAI Veda Health Assessment Report - {report_data['dominant']} Dosha"
        
        html_body = f"""
        <html>
        <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
            <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
                <div style="background: linear-gradient(135deg, #FF9933, #138808); padding: 30px; border-radius: 8px; margin-bottom: 20px; text-align: center;">
                    <h1 style="color: white; margin: 0; font-size: 28px;">🕉️ AyurAI Veda</h1>
                    <p style="color: white; margin: 10px 0 0 0; font-size: 16px;">Your Personalized Health Assessment Report</p>
                </div>
                
                <div style="background: #f8f9fa; padding: 20px; border-radius: 6px; margin-bottom: 20px;">
                    <h2 style="color: #1a237e; margin-top: 0;">📊 Your Results</h2>
                    <div style="background: white; padding: 15px; border-radius: 4px; margin-bottom: 15px;">
                        <p style="margin: 0; font-size: 14px; color: #666;">Dominant Dosha</p>
                        <p style="margin: 5px 0 0 0; font-size: 24px; font-weight: bold; color: #FF9933;">{report_data['dominant']}</p>
                    </div>
                    <div style="background: white; padding: 15px; border-radius: 4px;">
                        <p style="margin: 0; font-size: 14px; color: #666;">Risk Level</p>
                        <p style="margin: 5px 0 0 0; font-size: 20px; font-weight: bold; color: {'#d32f2f' if report_data['risk'] == 'High' else '#f57c00' if report_data['risk'] == 'Moderate' else '#388e3c'};">{report_data['risk']}</p>
                    </div>
                </div>
                
                <div style="background: white; padding: 20px; border: 1px solid #ddd; border-radius: 6px; margin-bottom: 20px;">
                    <h3 style="color: #1a237e; margin-top: 0;">⚖️ Dosha Distribution</h3>
                    <div style="margin-bottom: 15px;">
                        <div style="display: flex; justify-content: space-between; margin-bottom: 5px;">
                            <span style="font-weight: bold; color: #333;">🌬️ Vata</span>
                            <span style="color: #333;">{report_data['scores']['vata']}%</span>
                        </div>
                        <div style="background: #e0e0e0; height: 20px; border-radius: 10px; overflow: hidden;">
                            <div style="background: #9C27B0; height: 100%; width: {report_data['scores']['vata']}%;"></div>
                        </div>
                    </div>
                    <div style="margin-bottom: 15px;">
                        <div style="display: flex; justify-content: space-between; margin-bottom: 5px;">
                            <span style="font-weight: bold; color: #333;">🔥 Pitta</span>
                            <span style="color: #333;">{report_data['scores']['pitta']}%</span>
                        </div>
                        <div style="background: #e0e0e0; height: 20px; border-radius: 10px; overflow: hidden;">
                            <div style="background: #FF5722; height: 100%; width: {report_data['scores']['pitta']}%;"></div>
                        </div>
                    </div>
                    <div>
                        <div style="display: flex; justify-content: space-between; margin-bottom: 5px;">
                            <span style="font-weight: bold; color: #333;">🌊 Kapha</span>
                            <span style="color: #333;">{report_data['scores']['kapha']}%</span>
                        </div>
                        <div style="background: #e0e0e0; height: 20px; border-radius: 10px; overflow: hidden;">
                            <div style="background: #4CAF50; height: 100%; width: {report_data['scores']['kapha']}%;"></div>
                        </div>
                    </div>
                </div>
                
                <div style="background: #e8f5e9; padding: 20px; border-radius: 6px; border-left: 4px solid #138808; margin-bottom: 20px;">
                    <h3 style="color: #2e7d32; margin-top: 0;">✨ Personalized Recommendations</h3>
                    <ul style="margin: 0; padding-left: 20px; color: #333;">
                        {''.join([f'<li style="margin-bottom: 8px; color: #333;">{rec}</li>' for rec in report_data['recommendations']])}
                    </ul>
                </div>
                
                <div style="background: #fff3e0; padding: 15px; border-radius: 6px; border-left: 4px solid #FF9933; margin-bottom: 20px;">
                    <p style="margin: 0; font-size: 12px; color: #e65100;"><strong>⚠️ Important Disclaimer:</strong> This report provides educational and preventive health insights only. It is NOT a medical diagnosis. Always consult qualified healthcare professionals for medical advice.</p>
                </div>
                
                <div style="text-align: center; padding: 20px; background: #1a237e; border-radius: 6px;">
                    <p style="color: white; margin: 0; font-size: 14px;">🌿 <strong>AyurAI Veda</strong></p>
                    <p style="color: #ccc; margin: 5px 0; font-size: 12px;">Ancient Wisdom. Intelligent Health.</p>
                    <p style="color: #ccc; margin: 5px 0; font-size: 11px;">Powered by Tridosha Intelligence Engine™</p>
                    <p style="color: #999; margin: 10px 0 0 0; font-size: 10px;">Report generated on {datetime.now().strftime('%d %B %Y at %I:%M %p')}</p>
                </div>
            </div>
        </body>
        </html>
        """
        
        msg.attach(MIMEText(html_body, 'html'))
        
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, recipient_email, msg.as_string())
        server.quit()
        
        print(f"✅ Assessment report sent to {recipient_email}")
        return True
        
    except Exception as e:
        print(f"❌ Email error: {str(e)}")
        return False

def log_feedback(data):
    """Log feedback to console when email fails"""
    print("=== FEEDBACK RECEIVED ===")
    print(f"Name: {data['name']}")
    print(f"Mobile: {data['mobile']}")
    print(f"Institute: {data['institute']}")
    print(f"Designation: {data['designation']}")
    print(f"Feedback: {data['feedback']}")
    print(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=========================")

# Vercel serverless handler
handler = app


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

@app.route('/analyze-clinical-image', methods=['POST'])
def analyze_clinical_image():
    """Clinical assessment using Lakshana → Guna → Dosha pipeline (Body-based, no face detection)"""
    try:
        import sys
        import os
        sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)) + '/..')
        
        from clinical_engine import ClinicalAssessmentEngine
        from simple_body_extractor import SimpleBodyExtractor
        import numpy as np
        
        data = request.json
        image_data = data.get('image')
        user_data = data.get('user_data', {})
        
        if not image_data:
            return jsonify({'success': False, 'error': 'No image provided'})
        
        # Step 1: Extract body features (no face detection required)
        print("🔍 Extracting body features...")
        extractor = SimpleBodyExtractor()
        feature_result = extractor.extract_features(image_data, input_type='base64')
        
        if not feature_result['success']:
            return jsonify(feature_result)
        
        print("✅ Body features extracted successfully")
        
        # Step 2: Use clinical engine for assessment
        print("🧠 Running clinical assessment...")
        clinical_engine = ClinicalAssessmentEngine()
        clinical_result = clinical_engine.assess(feature_result['features'])
        
        print("✅ Clinical assessment completed")
        
        # Convert numpy types
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
        
        clinical_result = convert_to_native(clinical_result)
        
        # Format response
        dominant_lower = clinical_result['type'].split()[0].lower()
        
        formatted_result = {
            'success': True,
            'analysis_type': 'Clinical Assessment (Lakshana → Guna → Dosha) - Body-Based',
            'dominant': clinical_result['type'],
            'scores': clinical_result['dosha'],
            'confidence': clinical_result['confidence'],
            'explanation': clinical_result['explanation'],
            'guna_analysis': clinical_result['guna_analysis'],
            'features': feature_result.get('features', {}),
            'recommendations': get_recommendations(dominant_lower),
            'diet_suggestions': get_diet_suggestions(dominant_lower),
            'lifestyle_tips': get_lifestyle_tips(dominant_lower),
            'user_data': user_data,
            'note': 'No face detection required - Full body analysis'
        }
        
        return jsonify(formatted_result)
        
    except Exception as e:
        print(f"Clinical image analysis error: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({
            'success': False,
            'error': f'Clinical analysis failed: {str(e)}'
        }), 500
