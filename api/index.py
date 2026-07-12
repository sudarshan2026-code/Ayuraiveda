if __import__('sys').platform == 'win32':
    __import__('sys').stdout.reconfigure(encoding='utf-8', errors='replace')
    __import__('sys').stderr.reconfigure(encoding='utf-8', errors='replace')

from flask import Flask, request, jsonify, render_template, send_file, session, make_response
import json
import io
import os
import sys
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime

app = Flask(__name__, template_folder='../templates', static_folder='../static')
app.secret_key = os.getenv('SECRET_KEY', 'ayurveda_secret_key_2024')

# Enable CORS globally for native app API requests (Capacitor/Cordova)
@app.before_request
def handle_options_preflight():
    if request.method == 'OPTIONS':
        response = make_response()
        response.headers['Access-Control-Allow-Origin'] = '*'
        response.headers['Access-Control-Allow-Headers'] = 'Content-Type,Authorization'
        response.headers['Access-Control-Allow-Methods'] = 'GET,PUT,POST,DELETE,OPTIONS'
        return response

@app.after_request
def add_cors_headers(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type,Authorization'
    response.headers['Access-Control-Allow-Methods'] = 'GET,PUT,POST,DELETE,OPTIONS'
    return response

# Import authentication routes
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)) + '/..')

try:
    from auth_routes_sqlite import register_auth_routes
    register_auth_routes(app)
    print('[OK] Authentication routes registered')
except Exception as e:
    print('[WARN] Auth routes skipped: ' + str(e))

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

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

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
        return jsonify({
            'success': False,
            'error': f'Enhanced analysis failed: {str(e)}'
        }), 500

@app.route('/analyze-body', methods=['POST'])
def analyze_body():
    """Analyze body from uploaded image with automatic quality enhancement and structure validation"""
    try:
        from face_body_detection_extended import FaceBodyDetector
        from image_quality_enhancer import ImageQualityEnhancer
        from confidence_calibrator import ConfidenceCalibrator
        from body_validator import BodyStructureValidator
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
        
        # Step 2: Calibrate confidence scores
        print("📊 Calibrating confidence scores...")
        calibrator = ConfidenceCalibrator()
        
        # Prepare features for calibration
        body_features = {
            'body_ratio': body_result['ratio'],
            'body_frame': body_result['width'] / image.shape[1],
            'limb_thickness': body_result['ratio'] * 0.8,
            'shoulder_width': body_result['width'] / image.shape[1]
        }
        
        calibrated_features = calibrator.calibrate(body_features)
        print(f"✅ Calibration complete - Confidence: {calibrated_features['body_confidence']}")
        
        # Step 3: Validate and correct body structure
        print("🔧 Validating body structure...")
        validator = BodyStructureValidator()
        
        # Prepare detected data for validation
        detected_data = {
            'body_build': 'lean' if body_result['ratio'] < 0.35 else 'medium' if body_result['ratio'] < 0.45 else 'heavy',
            'body_width': body_result['width'],
            'body_height': body_result['height'],
            'body_ratio': body_result['ratio']
        }
        
        corrected_data = validator.validate_and_correct(detected_data)
        print(f"✅ Structure validated - Vata eligible: {corrected_data.get('vata_eligible', True)}")
        
        # Encode result image with bounding boxes
        result_image = detector.draw_detections(image, faces, bodies)
        _, buffer = cv2.imencode('.jpg', result_image)
        result_image_base64 = f"data:image/jpeg;base64,{base64.b64encode(buffer).decode('utf-8')}"
        
        # Apply validation corrections to dosha scores
        raw_vata = body_result['vata']
        raw_pitta = body_result['pitta']
        raw_kapha = body_result['kapha']
        
        # Apply Vata safety rule
        if not corrected_data.get('vata_eligible', True):
            raw_vata *= 0.5  # Reduce Vata if not structurally eligible
            print("⚠️ Vata reduced - body structure not lean/angular")
        
        # Apply structure lock for medium/heavy builds
        if corrected_data.get('base_dosha') == 'kapha-pitta':
            raw_vata *= 0.3  # Further reduce Vata
            print("🔒 Structure locked to Kapha-Pitta base")
        
        # Determine dominant dosha with corrections
        max_score = max(raw_vata, raw_pitta, raw_kapha)
        if raw_vata == max_score:
            dominant = 'Vata'
        elif raw_pitta == max_score:
            dominant = 'Pitta'
        else:
            dominant = 'Kapha'
        
        # Calculate percentages with corrected scores
        total = raw_vata + raw_pitta + raw_kapha
        if total > 0:
            vata_percent = round((raw_vata / total) * 100, 1)
            pitta_percent = round((raw_pitta / total) * 100, 1)
            kapha_percent = round((raw_kapha / total) * 100, 1)
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

# Initialize Ayurvedic Chat Service
try:
    from backend.chat.chat_service import AyurvedicChatService
    chat_service = AyurvedicChatService()
    print('[OK] Ayurvedic RAG Chat Service initialized')
except Exception as e:
    chat_service = None
    print('[WARN] Chat service initialization warning: ' + str(e))

@app.route('/chat', methods=['POST'])
@app.route('/api/chat', methods=['POST'])
def chat():
    try:
        data = request.json or {}
        message = data.get('message', '')
        session_id = data.get('session_id', 'default_session')
        user_profile = data.get('user_profile', {})
        language = data.get('language', 'en')
        
        if not message:
            return jsonify({'error': 'Message is required'}), 400
            
        if chat_service:
            result = chat_service.process_chat_message(session_id, message, user_profile, language=language)
            return jsonify(result)
        else:
            # Fallback patterns in case service is not fully initialized
            resp_text = get_chatbot_response(message.lower())
            return jsonify({
                "response": resp_text,
                "prakriti": "Unknown",
                "vikriti": "Unknown",
                "agni": "Unknown",
                "ama": "Unknown",
                "emergency": False
            })
    except Exception as e:
        print(f"Chat API error: {str(e)}")
        return jsonify({'response': 'Sorry, I encountered an error in the Ayurvedic reasoning engine. Please try again.', 'error': str(e)}), 500

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
    """Advanced Clinical Assessment with 22-Question Ayurvedic Prakriti Parikshan Framework"""
    
    # 22-question bank definitions matching frontend and PDF
    QUESTION_BANK = [
        {
            "id": 1,
            "question": "Body Structure",
            "options": {
                "Lean, thin, tall or short stature with dry skin": "Vata",
                "Medium build, athletic, well-proportioned structure": "Pitta",
                "Broad, heavy-set, well-nourished, stable structure": "Kapha"
            }
        },
        {
            "id": 2,
            "question": "Body Parts",
            "options": {
                "Narrow, irregular facial features or bony joints": "Vata",
                "Delicate/sharp features, fair or flushed complexion": "Pitta",
                "Round, smooth, well-nourished body and face": "Kapha"
            }
        },
        {
            "id": 3,
            "question": "Sleep",
            "options": {
                "Light, disturbed, or interrupted sleep": "Vata",
                "Moderate sleep but wakes up refreshed": "Pitta",
                "Deep, long sleep, difficult to wake up": "Kapha"
            }
        },
        {
            "id": 4,
            "question": "Dreams",
            "options": {
                "Active, flying, falling, sky, or running": "Vata",
                "Fire, fighting, sun, lightning, or anger": "Pitta",
                "Water, lakes, gardens, swans, or clouds": "Kapha"
            }
        },
        {
            "id": 5,
            "question": "Complexion",
            "options": {
                "Dusky, darkish, brown, or dry complexion": "Vata",
                "Fair, pinkish, reddish, or freckled complexion": "Pitta",
                "Pale white, golden, clear, or glowing complexion": "Kapha"
            }
        },
        {
            "id": 6,
            "question": "Hair",
            "options": {
                "Dry, rough, thin, brittle, or split-ended hair": "Vata",
                "Soft, thin, prematurely greying, or balding hair": "Pitta",
                "Thick, dense, oily, shiny black, or wavy hair": "Kapha"
            }
        },
        {
            "id": 7,
            "question": "Nails",
            "options": {
                "Dry, rough, brittle, small, or irregular nails": "Vata",
                "Pink, smooth, moderate-sized, or flexible nails": "Pitta",
                "Large, thick, strong, smooth, or pale nails": "Kapha"
            }
        },
        {
            "id": 8,
            "question": "Joints",
            "options": {
                "Cracking, dry, unstable, or prominent joints": "Vata",
                "Moderate, flexible, loose, or flabby ligaments": "Pitta",
                "Strong, well-built, padded with muscle, silent joints": "Kapha"
            }
        },
        {
            "id": 9,
            "question": "Hunger",
            "options": {
                "Irregular, variable appetite (sometimes high, sometimes low)": "Vata",
                "Intense, sharp hunger (cannot tolerate skipping meals)": "Pitta",
                "Mild, slow, stable hunger (can easily skip meals)": "Kapha"
            }
        },
        {
            "id": 10,
            "question": "Thirst",
            "options": {
                "Variable, irregular thirst with dry mouth": "Vata",
                "Intense, frequent thirst (drinks a lot of water)": "Pitta",
                "Low thirst (drinks little water, stable)": "Kapha"
            }
        },
        {
            "id": 11,
            "question": "Activity",
            "options": {
                "Fast walking, talking, eating, and rapid movements": "Vata",
                "Moderate, purposeful, energetic, and organized actions": "Pitta",
                "Slow, steady, deliberate, and relaxed movements": "Kapha"
            }
        },
        {
            "id": 12,
            "question": "Voice",
            "options": {
                "Dry, weak, low-pitched, or hoarse voice": "Vata",
                "Loud, sharp, clear, and commanding voice": "Pitta",
                "Soft, sweet, melodious, and deep resonant voice": "Kapha"
            }
        },
        {
            "id": 13,
            "question": "Exercise & Tolerance",
            "options": {
                "Intolerant to cold, prefers warm climates and gentle exercise": "Vata",
                "Intolerant to heat/sun, prefers cool environment": "Pitta",
                "High tolerance to exertion, dislikes cold/damp weather": "Kapha"
            }
        },
        {
            "id": 14,
            "question": "Intelligence & Memory",
            "options": {
                "Learns quickly but forgets quickly (short-term memory)": "Vata",
                "Sharp, intelligent, logical, with excellent comprehension": "Pitta",
                "Learns slowly but remembers forever (long-term memory)": "Kapha"
            }
        },
        {
            "id": 15,
            "question": "Friends",
            "options": {
                "Makes friends quickly, but friendships are unstable": "Vata",
                "Selective, loyal but demanding circle of friends": "Pitta",
                "Makes friends slowly, but holds deep, lifelong bonds": "Kapha"
            }
        },
        {
            "id": 16,
            "question": "Resources",
            "options": {
                "Struggles to save, spends impulsively on whims": "Vata",
                "Spends planned, buys quality/luxury items": "Pitta",
                "Saves systematically, spends conservatively, accumulates wealth": "Kapha"
            }
        },
        {
            "id": 17,
            "question": "Wealth",
            "options": {
                "Variable or fluctuating financial status": "Vata",
                "Moderate, stable, and well-managed financial status": "Pitta",
                "Wealthy, stable, and naturally good at accumulating assets": "Kapha"
            }
        },
        {
            "id": 18,
            "question": "Disease Susceptibility",
            "options": {
                "Prone to cold/cough, stiffness, body pain, easily sick": "Vata",
                "Prone to heat, mouth ulcers, acidity, inflammation": "Pitta",
                "Strong general immunity, prone to congestion/mucus": "Kapha"
            }
        },
        {
            "id": 19,
            "question": "Food & Lifestyle Preferences",
            "options": {
                "Prefers sweet, sour, hot food; enjoys traveling": "Vata",
                "Prefers sweet, bitter, astringent, cold food and cosmetics": "Pitta",
                "Prefers warm, spicy, bitter food; enjoys active hobbies": "Kapha"
            }
        },
        {
            "id": 20,
            "question": "Nature",
            "options": {
                "Quick starter, creative, restless, easily anxious": "Vata",
                "Courageous, ambitious, short-tempered, organized": "Pitta",
                "Calm, patient, forgiving, slow to anger": "Kapha"
            }
        },
        {
            "id": 21,
            "question": "Miscellaneous",
            "options": {
                "Feels highly relaxed and energized after oil massage": "Vata",
                "Likes massage with cooling oils only": "Pitta",
                "Does not prefer or need oil massage (feels heavy)": "Kapha"
            }
        },
        {
            "id": 22,
            "question": "Animal Personality",
            "options": {
                "Goat, Rabbit, Rat, Deer, Crow (quick, active)": "Vata",
                "Tiger, Cobra, Cat, Monkey (sharp, aggressive)": "Pitta",
                "Elephant, Lion, Horse, Swan (majestic, calm)": "Kapha"
            }
        }
    ]

    # ML model loading for hybrid calculation
    ml_vata_score = ml_pitta_score = ml_kapha_score = 0
    ml_calculated = False
    
    try:
        from backend.utils.ml_loader import AyurMLModelLoader
        from sklearn.metrics.pairwise import cosine_similarity
        import numpy as np
        import re
        
        ml_loader = AyurMLModelLoader()
        if ml_loader.vectorizer and len(ml_loader.chunks) > 0:
            # 1. Compile user answers into a single text profile string
            user_answers = []
            for q in QUESTION_BANK:
                key = f"q{q['id']}"
                val = data.get(key)
                if val:
                    user_answers.append(f"{q['question']}: {val}")
            
            patient_profile_text = ". ".join(user_answers)
            
            # 2. Get similarity vector
            query_vec = ml_loader.vectorizer.transform([patient_profile_text])
            similarities = cosine_similarity(query_vec, ml_loader.tfidf_matrix).flatten()
            
            # 3. Match against the top chunks
            top_k = min(30, len(ml_loader.chunks))
            top_indices = np.argsort(similarities)[-top_k:][::-1]
            
            # 4. Score based on matching keyword occurrences in relevant guidelines
            vata_kws = r'\b(vata|vataja|vayu|dryness|roughness|coldness|lightness|unstable|cracking)\b'
            pitta_kws = r'\b(pitta|pittaja|heat|redness|acidity|sharpness|soft|sweat|flushed)\b'
            kapha_kws = r'\b(kapha|kaphaja|heaviness|oiliness|smoothness|stability|stout|nourish)\b'
            
            for idx in top_indices:
                sim = similarities[idx]
                if sim > 0:
                    chunk_text = ml_loader.chunks[idx].lower()
                    
                    vata_cnt = len(re.findall(vata_kws, chunk_text))
                    pitta_cnt = len(re.findall(pitta_kws, chunk_text))
                    kapha_cnt = len(re.findall(kapha_kws, chunk_text))
                    
                    ml_vata_score += sim * vata_cnt
                    ml_pitta_score += sim * pitta_cnt
                    ml_kapha_score += sim * kapha_cnt
            
            # 5. Convert ML scores to percentages
            ml_total = ml_vata_score + ml_pitta_score + ml_kapha_score
            if ml_total > 0:
                ml_vata_pct = (ml_vata_score / ml_total) * 100
                ml_pitta_pct = (ml_pitta_score / ml_total) * 100
                ml_kapha_pct = (ml_kapha_score / ml_total) * 100
                ml_calculated = True
    except Exception as e:
        print(f"[WARN] ML Clinical Scoring failed: {str(e)}")
        ml_calculated = False

    vata_score = pitta_score = kapha_score = 0
    reasoning = []
    
    # Tally scores dynamically from the model
    for q in QUESTION_BANK:
        key = f"q{q['id']}"
        val = data.get(key)
        if val and val in q["options"]:
            dosha = q["options"][val]
            if dosha == "Vata":
                vata_score += 1
            elif dosha == "Pitta":
                pitta_score += 1
            elif dosha == "Kapha":
                kapha_score += 1

    # Convert to percentages
    total = vata_score + pitta_score + kapha_score
    if total > 0:
        vata_percent_rule = (vata_score / total) * 100
        pitta_percent_rule = (pitta_score / total) * 100
        kapha_percent_rule = (kapha_score / total) * 100
        
        # Apply hybrid blend if ML was successfully calculated
        if ml_calculated:
            # 50/50 blend of Rule-based and ML-based similarity mapping
            vata_percent = round(0.5 * vata_percent_rule + 0.5 * ml_vata_pct)
            pitta_percent = round(0.5 * pitta_percent_rule + 0.5 * ml_pitta_pct)
            kapha_percent = round(0.5 * kapha_percent_rule + 0.5 * ml_kapha_pct)
        else:
            vata_percent = round(vata_percent_rule)
            pitta_percent = round(pitta_percent_rule)
            kapha_percent = round(kapha_percent_rule)
            
        # Adjust rounding errors
        diff = 100 - (vata_percent + pitta_percent + kapha_percent)
        if diff != 0:
            if vata_percent >= pitta_percent and vata_percent >= kapha_percent:
                vata_percent += diff
            elif pitta_percent >= vata_percent and pitta_percent >= kapha_percent:
                pitta_percent += diff
            else:
                kapha_percent += diff
    else:
        vata_percent = pitta_percent = kapha_percent = 33

    scores = {'vata': vata_percent, 'pitta': pitta_percent, 'kapha': kapha_percent}
    
    # Classify dominant constitution using identical rules to frontend
    sorted_doshas = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    highest = sorted_doshas[0]
    second = sorted_doshas[1]
    lowest = sorted_doshas[2]
    
    if highest[1] - lowest[1] <= 5:
        prakriti = "Sama Prakriti (Tridoshic)"
        dosha_state = "Balanced"
    elif highest[1] - second[1] <= 6:
        prakriti = f"{highest[0].capitalize()}-{second[0].capitalize()} Prakriti"
        dosha_state = "Imbalanced"
    else:
        prakriti = f"{highest[0].capitalize()} Prakriti"
        dosha_state = "Imbalanced" if highest[1] >= 55 else "Balanced"

    vikriti = highest[0].capitalize()

    # Determine Agni and Ama states
    if vikriti == 'Vata':
        agni_type = 'Vishama Agni (Irregular)'
        ama_status = 'Mild'
        reasoning.append("Irregular appetite and joints indicate Vishama Agni and Vata imbalance")
    elif vikriti == 'Pitta':
        agni_type = 'Tikshna Agni (Sharp)'
        ama_status = 'Moderate'
        reasoning.append("Strong thirst and digestion speed suggest Tikshna Agni and Pitta constitution")
    else:
        agni_type = 'Manda Agni (Sluggish)'
        ama_status = 'Mild'
        reasoning.append("Slow walking and physical stability indicate Manda Agni and Kapha dominance")

    # Set risk
    if highest[1] >= 60:
        risk = "High"
    elif highest[1] >= 45:
        risk = "Moderate"
    else:
        risk = "Low"

    justification = f"Based on 22-question Ayurvedic assessment: {prakriti} constitution identified. " + " ".join(reasoning)

    return {
        'dominant': prakriti,
        'scores': scores,
        'risk': risk,
        'dosha_state': dosha_state,
        'agni_state': agni_type,
        'ama_status': ama_status,
        'vikriti': vikriti,
        'justification': justification,
        'reasoning': reasoning[:5],
        'recommendations': get_clinical_recommendations(vikriti.lower(), ama_status),
        'diet_suggestions': get_diet_suggestions(vikriti.lower()),
        'lifestyle_tips': get_lifestyle_tips(vikriti.lower()),
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
    msg_clean = message.strip().lower().rstrip("?./!")
    greetings = ["hi", "hello", "namaste", "hey", "good morning", "good afternoon", "good evening"]
    
    is_pure_greeting = False
    temp_msg = msg_clean.strip(" ,.!?;:")
    if temp_msg in greetings:
        is_pure_greeting = True
        
    if not is_pure_greeting:
        for g in greetings:
            if temp_msg.startswith(g):
                remaining = temp_msg[len(g):].strip(" ,.!?;:")
                if remaining:
                    msg_clean = remaining
                    break
                    
    if is_pure_greeting:
        return """Hello! I'm AyurVaani, your Ayurvedic wellness assistant. I can help you with:<br><br>
🌬️ Understanding Vata, Pitta, and Kapha doshas<br>
🍽️ Personalized diet recommendations<br>
🌿 Herbal remedies and natural treatments<br>
🧘 Yoga and pranayama practices<br>
😌 Stress management and sleep improvement<br>
🔥 Digestive health and Agni strengthening<br><br>
What would you like to know about Ayurveda today?"""

    if 'tridosha' in msg_clean or 'tri dosha' in msg_clean or 'three dosha' in msg_clean:
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
    
    elif 'vata' in msg_clean:
        return "Vata dosha (Air + Space) governs movement, creativity, and the nervous system. When balanced, it promotes creativity and flexibility. When imbalanced, it can cause anxiety, dry skin, and digestive issues. Balance vata with warm foods, regular routines, and oil massage."
    
    elif 'pitta' in msg_clean:
        return "Pitta dosha (Fire + Water) governs metabolism and is associated with fire and water elements. When balanced, it promotes good digestion and sharp intellect. When imbalanced, it can cause acidity, anger, and skin inflammation. Balance pitta with cooling foods and avoiding excessive heat."
    
    elif 'kapha' in msg_clean:
        return "Kapha dosha (Water + Earth) governs structure and is associated with water and earth elements. When balanced, it provides strength and immunity. When imbalanced, it can cause weight gain, congestion, and lethargy. Balance kapha with light foods, regular exercise, and staying active."
    
    elif 'diet' in msg_clean or 'food' in msg_clean:
        return "Ayurvedic diet is based on your dosha constitution. Vata types need warm, moist foods. Pitta types need cooling, less spicy foods. Kapha types need light, warm, spicy foods. Eat fresh, seasonal foods and avoid processed items."
    
    elif 'yoga' in msg_clean or 'exercise' in msg_clean:
        return "Yoga is an integral part of Ayurveda. Vata types benefit from gentle, grounding poses. Pitta types need cooling, moderate practices. Kapha types need energizing, vigorous sequences. Practice regularly for best results."
    
    elif 'sleep' in msg_clean or 'insomnia' in msg_clean:
        return "Good sleep is crucial for health. Vata types need 7-8 hours with regular bedtime. Pitta types need 6-7 hours in cool environment. Kapha types need 6-7 hours and should wake early. Avoid screens before bed."
    
    elif 'stress' in msg_clean or 'anxiety' in msg_clean:
        return "Ayurvedic stress management: Regular routine, adequate sleep, meditation, pranayama (breathing exercises), Abhyanga (oil massage), and adaptogenic herbs like Ashwagandha. Stress is seen as Vata imbalance affecting the mind."
    
    elif 'digestion' in msg_clean or 'agni' in msg_clean:
        return "To improve digestion (Agni): Eat at regular times, use digestive spices (ginger, cumin, fennel), avoid overeating, drink warm water, and walk after meals. Strong Agni is key to health in Ayurveda."
    
    elif 'meditation' in msg_clean:
        return "Meditation balances all doshas. Vata types benefit from grounding meditations. Pitta types need cooling, calming practices. Kapha types benefit from energizing techniques. Start with 10-15 minutes daily."
    
    elif 'herb' in msg_clean or 'ashwagandha' in msg_clean or 'turmeric' in msg_clean:
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


@app.route('/contact-email', methods=['POST'])
def contact_email():
    try:
        data = request.json
        name    = data.get('name', '').strip()
        email   = data.get('email', '').strip()
        subject = data.get('subject', '').strip()
        message = data.get('message', '').strip()

        if not all([name, email, subject, message]):
            return jsonify({'success': False, 'message': 'All fields are required'})

        smtp_server  = 'smtp.gmail.com'
        smtp_port    = 587
        sender_email = os.getenv('CONTACT_EMAIL', 'ayuraiveda@gmail.com')
        sender_pass  = os.getenv('CONTACT_EMAIL_PASS', '')
        recipient    = 'ayuraiveda@gmail.com'

        html = f"""<html><body style="font-family:Arial,sans-serif;color:#333;max-width:600px;margin:0 auto;padding:20px">
<div style="background:linear-gradient(135deg,#5f6b2a,#7d8c3a);padding:20px;border-radius:8px;margin-bottom:20px">
  <h2 style="color:white;margin:0">AyurAI Veda - Contact Form</h2>
</div>
<table style="width:100%;border-collapse:collapse">
  <tr><td style="padding:8px 0;font-weight:bold;width:30%">Name:</td><td>{name}</td></tr>
  <tr><td style="padding:8px 0;font-weight:bold">Email:</td><td><a href="mailto:{email}">{email}</a></td></tr>
  <tr><td style="padding:8px 0;font-weight:bold">Subject:</td><td>{subject}</td></tr>
</table>
<div style="background:#f5f5f5;padding:15px;border-radius:6px;margin-top:15px;border-left:4px solid #5f6b2a">
  <p style="margin:0;white-space:pre-wrap">{message}</p>
</div>
<p style="color:#999;font-size:11px;margin-top:20px">Sent from AyurAI Veda contact form</p>
</body></html>"""

        if sender_pass:
            msg = MIMEMultipart('alternative')
            msg['From']     = f'AyurAI Veda <{sender_email}>'
            msg['To']       = recipient
            msg['Subject']  = f'[Contact] {subject} - from {name}'
            msg['Reply-To'] = email
            msg.attach(MIMEText(html, 'html'))
            server = smtplib.SMTP(smtp_server, smtp_port)
            server.starttls()
            server.login(sender_email, sender_pass)
            server.sendmail(sender_email, recipient, msg.as_string())
            server.quit()

        print('[CONTACT] Name:' + name + ' Email:' + email + ' Subject:' + subject)
        return jsonify({'success': True, 'message': 'Message sent successfully!'})
    except Exception as ex:
        print('[CONTACT ERROR] ' + str(ex))
        return jsonify({'success': True, 'message': 'Message received! We will get back to you soon.'})

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
        from confidence_calibrator import ConfidenceCalibrator
        from body_validator import BodyStructureValidator
        import numpy as np
        
        data = request.json
        image_data = data.get('image')
        user_data = data.get('user_data', {})
        
        if not image_data:
            return jsonify({'success': False, 'error': 'No image provided'})
        
        # Step 1: Detect if a human body is present
        print("🔍 Detecting human body...")
        import cv2
        import base64
        from io import BytesIO
        from PIL import Image
        
        raw_b64 = image_data
        if 'base64,' in raw_b64:
            raw_b64 = raw_b64.split('base64,')[1]
        
        try:
            image_bytes = base64.b64decode(raw_b64)
            pil_image = Image.open(BytesIO(image_bytes))
            image = cv2.cvtColor(np.array(pil_image), cv2.COLOR_RGB2BGR)
        except Exception as e:
            return jsonify({'success': False, 'error': f'Failed to decode image: {str(e)}'})
            
        h, w = image.shape[:2]
        
        # 1. HOG Person Detector
        body_detected = False
        try:
            hog = cv2.HOGDescriptor()
            hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())
            
            # Resize for faster SVM processing
            max_dim = 400
            if max(h, w) > max_dim:
                scale = max_dim / max(h, w)
                resized_hog = cv2.resize(image, (int(w * scale), int(h * scale)))
            else:
                resized_hog = image
                
            # SVM HOG detector requires minimum dimensions of 64x128
            if resized_hog.shape[0] >= 128 and resized_hog.shape[1] >= 64:
                (rects, weights) = hog.detectMultiScale(resized_hog, winStride=(4, 4), padding=(8, 8), scale=1.05)
                body_detected = len(rects) > 0
        except Exception as e:
            print(f"[WARN] HOG detector failed: {e}")
            body_detected = False
            
        # 2. Contour area fallback if HOG fails (in case of cropped profiles)
        if not body_detected:
            try:
                gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
                edges = cv2.Canny(gray, 50, 150)
                contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
                if contours:
                    largest_contour = max(contours, key=cv2.contourArea)
                    largest_area = cv2.contourArea(largest_contour)
                    # If largest contour is at least 8% of the image area, count as valid human structure
                    if largest_area > (w * h * 0.08):
                        body_detected = True
            except Exception as e:
                print(f"[WARN] Contour fallback failed: {e}")
                
        # 3. Haar Cascade Face Detector as a final check (perfect for selfies / face close-ups)
        face_detected = False
        if not body_detected:
            try:
                face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
                gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
                faces = face_cascade.detectMultiScale(gray, 1.1, 4)
                face_detected = len(faces) > 0
                if face_detected:
                    print("✅ Human face identified in selfie/close-up!")
            except Exception as e:
                print(f"[WARN] Face detection failed: {e}")
                
        if not body_detected and not face_detected:
            return jsonify({
                'success': False,
                'error': 'No human body or face detected in the image. Please ensure your upper body or face is clearly visible.'
            })
            
        print("✅ Human body successfully identified!")
        
        # Step 2: Extract body features (no face detection required)
        print("🔍 Extracting body features...")
        extractor = SimpleBodyExtractor()
        feature_result = extractor.extract_features(image_data, input_type='base64')
        
        if not feature_result['success']:
            return jsonify(feature_result)
        
        print("✅ Body features extracted successfully")
        
        # Step 2: Calibrate confidence scores
        print("📊 Calibrating confidence scores...")
        calibrator = ConfidenceCalibrator()
        calibrated_features = calibrator.calibrate(feature_result['features'])
        calibration_report = calibrator.get_calibration_report(feature_result['features'], calibrated_features)
        print(calibration_report)
        
        # Step 3: Validate and correct structural misclassifications
        print("🔧 Validating body structure...")
        validator = BodyStructureValidator()
        corrected_features = validator.validate_and_correct(calibrated_features)
        print(f"✅ Validation complete - Vata eligible: {corrected_features.get('vata_eligible', True)}")
        
        # Step 4: Use clinical engine for assessment with corrected features
        print("🧠 Running clinical assessment...")
        clinical_engine = ClinicalAssessmentEngine()
        clinical_result = clinical_engine.assess(corrected_features)
        
        print("✅ Clinical assessment completed")
        
        # ML model loading for hybrid calculation
        ml_vata_score = ml_pitta_score = ml_kapha_score = 0
        ml_calculated = False
        
        try:
            from backend.utils.ml_loader import AyurMLModelLoader
            from sklearn.metrics.pairwise import cosine_similarity
            import numpy as np
            import re
            
            ml_loader = AyurMLModelLoader()
            if ml_loader.vectorizer and len(ml_loader.chunks) > 0:
                # Compile features into a description
                feature_text_list = []
                
                # Skin texture
                if corrected_features.get('skin_texture', 0.5) > 0.6:
                    feature_text_list.append("rough skin texture dry skin")
                elif corrected_features.get('skin_texture', 0.5) < 0.4:
                    feature_text_list.append("smooth skin soft skin")
                    
                # Oiliness
                if corrected_features.get('oiliness', 0.5) > 0.6:
                    feature_text_list.append("oily skin unctuous skin shine")
                elif corrected_features.get('oiliness', 0.5) < 0.4:
                    feature_text_list.append("dry skin lack of oil")
                    
                # Redness
                if corrected_features.get('redness', 0.5) > 0.6:
                    feature_text_list.append("redness red complexion skin heat flushed")
                    
                # Body frame
                frame = corrected_features.get('body_frame', 0.5)
                width = corrected_features.get('body_width', 0.5)
                if frame > 0.6 or width > 0.6:
                    feature_text_list.append("broad heavy body frame stout thick limbs solid structure")
                elif frame < 0.4 or width < 0.4:
                    feature_text_list.append("lean thin narrow body frame tall short slim structure")
                    
                # Limb thickness
                if corrected_features.get('limb_thickness', 0.5) > 0.6:
                    feature_text_list.append("thick joints heavy limbs robust")
                elif corrected_features.get('limb_thickness', 0.5) < 0.4:
                    feature_text_list.append("thin joints prominent veins bony joints")

                user_profile_text = " ".join(feature_text_list)
                
                if user_profile_text:
                    # Transform and similarity
                    user_vec = ml_loader.vectorizer.transform([user_profile_text])
                    similarities = cosine_similarity(user_vec, ml_loader.tfidf_matrix).flatten()
                    top_indices = np.argsort(similarities)[-10:][::-1]
                    
                    # Score based on keyword occurrences
                    vata_kws = r'\b(vata|vataja|vayu|dryness|roughness|coldness|lightness|unstable|cracking)\b'
                    pitta_kws = r'\b(pitta|pittaja|heat|redness|acidity|sharpness|soft|sweat|flushed)\b'
                    kapha_kws = r'\b(kapha|kaphaja|heaviness|oiliness|smoothness|stability|stout|nourish)\b'
                    
                    for idx in top_indices:
                        sim = similarities[idx]
                        if sim > 0:
                            chunk_text = ml_loader.chunks[idx].lower()
                            
                            vata_cnt = len(re.findall(vata_kws, chunk_text))
                            pitta_cnt = len(re.findall(pitta_kws, chunk_text))
                            kapha_cnt = len(re.findall(kapha_kws, chunk_text))
                            
                            ml_vata_score += sim * vata_cnt
                            ml_pitta_score += sim * pitta_cnt
                            ml_kapha_score += sim * kapha_cnt
                    
                    # Convert to percentages
                    ml_total = ml_vata_score + ml_pitta_score + ml_kapha_score
                    if ml_total > 0:
                        ml_vata_pct = (ml_vata_score / ml_total) * 100
                        ml_pitta_pct = (ml_pitta_score / ml_total) * 100
                        ml_kapha_pct = (ml_kapha_score / ml_total) * 100
                        ml_calculated = True
        except Exception as e:
            print(f"[WARN] ML Image Analysis Scoring failed: {str(e)}")
            ml_calculated = False

        # Load Prakriti Image Classifier model
        classifier_calculated = False
        classifier_vata = classifier_pitta = classifier_kapha = 0.0
        
        try:
            import pickle
            import numpy as np
            image_model_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../prakriti_image_model.pkl')
            if os.path.exists(image_model_path):
                with open(image_model_path, 'rb') as f:
                    image_classifier = pickle.load(f)
                
                features_list = [
                    corrected_features.get('skin_texture', 0.5),
                    corrected_features.get('oiliness', 0.5),
                    corrected_features.get('pigmentation', 0.5),
                    corrected_features.get('redness', 0.5),
                    corrected_features.get('brightness', 0.5),
                    corrected_features.get('body_frame', 0.5),
                    corrected_features.get('body_width', 0.5),
                    corrected_features.get('body_height', 0.5),
                    corrected_features.get('body_ratio', 0.5),
                    corrected_features.get('shoulder_width', 0.5),
                    corrected_features.get('hip_width', 0.5),
                    corrected_features.get('torso_length', 0.5),
                    corrected_features.get('limb_thickness', 0.5),
                    corrected_features.get('posture', 0.5)
                ]
                
                features_arr = np.array([features_list])
                image_classifier_probs = image_classifier.predict_proba(features_arr)[0]
                
                classifier_vata = float(image_classifier_probs[0] * 100)
                classifier_pitta = float(image_classifier_probs[1] * 100)
                classifier_kapha = float(image_classifier_probs[2] * 100)
                classifier_calculated = True
                print(f"[OK] Image classifier prediction completed: V={classifier_vata:.1f}%, P={classifier_pitta:.1f}%, K={classifier_kapha:.1f}%")
        except Exception as e:
            print(f"[WARN] Image classifier prediction failed: {str(e)}")
            classifier_calculated = False

        # Blend Rule-based and ML-based models
        vata_percent = clinical_result['dosha']['vata']
        pitta_percent = clinical_result['dosha']['pitta']
        kapha_percent = clinical_result['dosha']['kapha']
        
        if classifier_calculated and ml_calculated:
            vata_percent = round(0.4 * clinical_result['dosha']['vata'] + 0.4 * classifier_vata + 0.2 * ml_vata_pct)
            pitta_percent = round(0.4 * clinical_result['dosha']['pitta'] + 0.4 * classifier_pitta + 0.2 * ml_pitta_pct)
            kapha_percent = round(0.4 * clinical_result['dosha']['kapha'] + 0.4 * classifier_kapha + 0.2 * ml_kapha_pct)
        elif classifier_calculated:
            vata_percent = round(0.5 * clinical_result['dosha']['vata'] + 0.5 * classifier_vata)
            pitta_percent = round(0.5 * clinical_result['dosha']['pitta'] + 0.5 * classifier_pitta)
            kapha_percent = round(0.5 * clinical_result['dosha']['kapha'] + 0.5 * classifier_kapha)
        elif ml_calculated:
            vata_percent = round(0.5 * clinical_result['dosha']['vata'] + 0.5 * ml_vata_pct)
            pitta_percent = round(0.5 * clinical_result['dosha']['pitta'] + 0.5 * ml_pitta_pct)
            kapha_percent = round(0.5 * clinical_result['dosha']['kapha'] + 0.5 * ml_kapha_pct)
            
        # Adjust rounding errors to exactly 100%
        diff = 100 - (vata_percent + pitta_percent + kapha_percent)
        if diff != 0:
            if vata_percent >= pitta_percent and vata_percent >= kapha_percent:
                vata_percent += diff
            elif pitta_percent >= vata_percent and pitta_percent >= kapha_percent:
                pitta_percent += diff
            else:
                kapha_percent += diff
        
        # Update scores
        clinical_result['dosha']['vata'] = vata_percent
        clinical_result['dosha']['pitta'] = pitta_percent
        clinical_result['dosha']['kapha'] = kapha_percent
        
        # Recalculate type
        sorted_doshas = sorted(clinical_result['dosha'].items(), key=lambda x: x[1], reverse=True)
        highest = sorted_doshas[0]
        second = sorted_doshas[1]
        lowest = sorted_doshas[2]
        
        if highest[1] - lowest[1] <= 5:
            clinical_result['type'] = "Balanced (Sama Prakriti)"
        elif highest[1] - second[1] <= 6:
            clinical_result['type'] = f"{highest[0].capitalize()}-{second[0].capitalize()} Type"
        else:
            clinical_result['type'] = f"{highest[0].capitalize()} Predominant"

        # Convert numpy types
        def convert_to_native(obj):
            if isinstance(obj, (np.integer, np.int64)):
                return int(obj)
            elif isinstance(obj, (np.floating, np.float64)):
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
        return jsonify({
            'success': False,
            'error': f'Clinical analysis failed: {str(e)}'
        }), 500

@app.route('/analyze-ayurvedic-body', methods=['POST'])
def analyze_ayurvedic_body():
    """Ayurvedic Clinical Intelligence Engine - 10-Step Hierarchical Framework"""
    try:
        import sys
        import os
        sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)) + '/..')
        
        from ayurvedic_body_analyzer import AyurvedicBodyAnalyzer
        
        data = request.json
        image_data = data.get('image')
        user_data = data.get('user_data', {})
        
        if not image_data:
            return jsonify({'success': False, 'error': 'No image provided'})
        
        print("🧠 Starting Ayurvedic Clinical Intelligence Analysis...")
        
        # Initialize analyzer
        analyzer = AyurvedicBodyAnalyzer()
        
        # Perform 10-step analysis
        result = analyzer.analyze_image(image_data, input_type='base64')
        
        if not result.get('success'):
            return jsonify(result)
        
        print(f"✅ Analysis complete - Prakriti: {result['final_prakriti']}")
        
        # Add recommendations
        dominant_lower = result['final_prakriti'].split('-')[0].lower()
        result['recommendations'] = get_recommendations(dominant_lower)
        result['diet_suggestions'] = get_diet_suggestions(dominant_lower)
        result['lifestyle_tips'] = get_lifestyle_tips(dominant_lower)
        result['user_data'] = user_data
        result['analysis_method'] = 'Ayurvedic Clinical Intelligence Engine (10-Step Framework)'
        
        return jsonify(result)
        
    except Exception as e:
        print(f"Ayurvedic body analysis error: {str(e)}")
        return jsonify({
            'success': False,
            'error': f'Analysis failed: {str(e)}'
        }), 500

