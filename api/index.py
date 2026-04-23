from flask import Flask, render_template, request, jsonify
import os
from datetime import datetime

# Create Flask app
app = Flask(__name__)
app.secret_key = os.getenv('FLASK_SECRET_KEY', 'ayurveda_secret_key_2024')

# Health check endpoint
@app.route('/health')
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
        # Simple rule-based analysis for Vercel
        result = perform_basic_analysis(data)
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e), 'message': 'Analysis failed'}), 500

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
    
    # Normalize scores
    total = max(vata_score + pitta_score + kapha_score, 1)
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
        'justification': f'Based on your responses, {dominant} dosha is predominant.',
        'recommendations': get_basic_recommendations(dominant)
    }

def get_basic_recommendations(dominant):
    recommendations = {
        'vata': [
            "Follow regular daily routine",
            "Eat warm, cooked foods",
            "Practice oil massage",
            "Avoid cold environments"
        ],
        'pitta': [
            "Stay cool and avoid heat",
            "Eat cooling foods",
            "Practice moderation",
            "Avoid spicy foods"
        ],
        'kapha': [
            "Wake up early",
            "Eat light foods",
            "Practice vigorous exercise",
            "Avoid heavy foods"
        ]
    }
    return recommendations.get(dominant, recommendations['vata'])

# Vercel handler
def handler(request):
    return app(request.environ, lambda *args: None)

if __name__ == '__main__':
    app.run(debug=True)