from flask import Flask, render_template, request, jsonify
import os
from datetime import datetime

# Create Flask app
app = Flask(__name__, template_folder='../templates', static_folder='../static')
app.secret_key = os.getenv('FLASK_SECRET_KEY', 'ayurveda_secret_key_2024')

# Health check endpoint
@app.route('/api/health')
def health_check():
    return jsonify({
        'status': 'healthy',
        'service': 'AyurAI Veda',
        'version': '1.0.0',
        'timestamp': datetime.now().isoformat(),
        'environment': 'vercel'
    })

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/feedback')
def feedback():
    return render_template('feedback.html')

@app.route('/chatbot')
def chatbot():
    return render_template('chatbot.html')

@app.route('/clinical-assessment')
def clinical_assessment():
    return render_template('assessment.html')

# Basic assessment endpoint
@app.route('/clinical-analyze', methods=['POST'])
def clinical_analyze():
    try:
        data = request.json
        if not data:
            return jsonify({'error': 'No data provided'}), 400
            
        # Simple rule-based analysis for Vercel
        result = perform_basic_analysis(data)
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e), 'message': 'Analysis failed'}), 500

# Feedback submission
@app.route('/submit-feedback', methods=['POST'])
def submit_feedback():
    try:
        data = request.json
        
        # Validate required fields
        required_fields = ['name', 'mobile', 'institute', 'designation', 'feedback']
        for field in required_fields:
            if not data.get(field):
                return jsonify({'success': False, 'message': f'{field.title()} is required'})
        
        # Log feedback (since email might not work in serverless)
        print(f"=== FEEDBACK RECEIVED ===")
        print(f"Name: {data['name']}")
        print(f"Mobile: {data['mobile']}")
        print(f"Institute: {data['institute']}")
        print(f"Designation: {data['designation']}")
        print(f"Feedback: {data['feedback']}")
        print(f"Timestamp: {datetime.now().isoformat()}")
        print("========================")
        
        return jsonify({'success': True, 'message': 'Feedback submitted successfully'})
        
    except Exception as e:
        print(f"Feedback error: {e}")
        return jsonify({'success': False, 'message': 'An error occurred. Please try again.'})

def perform_basic_analysis(data):
    """Basic dosha analysis without heavy dependencies"""
    vata_score = pitta_score = kapha_score = 0
    
    # Simple scoring based on common parameters
    if data.get('body_structure') == 'lean':
        vata_score += 30
    elif data.get('body_structure') == 'moderate':
        pitta_score += 30
    elif data.get('body_structure') == 'heavy':
        kapha_score += 30
    
    if data.get('digestion') == 'gas':
        vata_score += 20
    elif data.get('digestion') == 'acidity':
        pitta_score += 20
    elif data.get('digestion') == 'slow':
        kapha_score += 20
    
    if data.get('skin') == 'dry':
        vata_score += 15
    elif data.get('skin') == 'sensitive':
        pitta_score += 15
    elif data.get('skin') == 'oily':
        kapha_score += 15
    
    if data.get('sleep') == 'poor':
        vata_score += 10
    elif data.get('sleep') == 'excessive':
        kapha_score += 10
    
    # Ensure minimum scores
    if vata_score == 0: vata_score = 10
    if pitta_score == 0: pitta_score = 10
    if kapha_score == 0: kapha_score = 10
    
    # Normalize scores
    total = vata_score + pitta_score + kapha_score
    scores = {
        'vata': int((vata_score / total) * 100),
        'pitta': int((pitta_score / total) * 100),
        'kapha': int((kapha_score / total) * 100)
    }
    
    dominant = max(scores, key=scores.get)
    
    return {
        'dominant': dominant.capitalize(),
        'scores': scores,
        'risk': 'Moderate' if max(scores.values()) >= 40 else 'Low',
        'dosha_state': f'{dominant.capitalize()} predominant constitution',
        'agni_state': 'Balanced digestive fire',
        'ama_status': 'Normal toxin levels',
        'justification': f'Based on your responses, {dominant} dosha is predominant with {scores[dominant]}% dominance.',
        'recommendations': get_basic_recommendations(dominant)
    }

def get_basic_recommendations(dominant):
    recommendations = {
        'vata': [
            "Follow regular daily routine (Dinacharya)",
            "Eat warm, cooked, moist foods",
            "Practice daily oil massage (Abhyanga)",
            "Avoid cold, dry environments",
            "Practice calming yoga and meditation",
            "Get adequate sleep (7-8 hours)"
        ],
        'pitta': [
            "Stay cool and avoid excessive heat",
            "Eat cooling, sweet, bitter foods",
            "Practice moderation in all activities",
            "Avoid spicy, sour, salty foods",
            "Practice patience and tolerance",
            "Exercise during cooler parts of day"
        ],
        'kapha': [
            "Wake up early and stay active",
            "Eat light, warm, spicy foods",
            "Practice vigorous exercise regularly",
            "Avoid heavy, oily, sweet foods",
            "Stay mentally stimulated",
            "Use warming spices in cooking"
        ]
    }
    return recommendations.get(dominant, recommendations['vata'])

# Export for Vercel
def handler(request):
    return app(request.environ, lambda *args: None)

if __name__ == '__main__':
    app.run(debug=True)