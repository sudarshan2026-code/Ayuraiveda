from flask import Flask, jsonify, render_template_string
import json
from datetime import datetime

app = Flask(__name__)

# Inline HTML templates to avoid file path issues
HOME_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AyurAI Veda - Ancient Wisdom. Intelligent Health.</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { 
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #0a0a0a, #1a1a2e, #16213e);
            color: #ffffff;
            min-height: 100vh;
        }
        .container { max-width: 1200px; margin: 0 auto; padding: 2rem; }
        .header { text-align: center; margin-bottom: 3rem; }
        .logo { font-size: 3rem; font-weight: bold; margin-bottom: 1rem; 
                background: linear-gradient(45deg, #00D9FF, #7B2FFF, #FF2E97);
                -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
        .subtitle { font-size: 1.2rem; opacity: 0.8; }
        .features { display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 2rem; margin: 3rem 0; }
        .feature { background: rgba(255,255,255,0.1); padding: 2rem; border-radius: 12px; border: 1px solid rgba(0,217,255,0.3); }
        .feature h3 { color: #00D9FF; margin-bottom: 1rem; }
        .btn { 
            display: inline-block; padding: 1rem 2rem; margin: 1rem;
            background: linear-gradient(45deg, #00D9FF, #7B2FFF);
            color: white; text-decoration: none; border-radius: 8px;
            font-weight: bold; transition: transform 0.3s;
        }
        .btn:hover { transform: translateY(-2px); }
        .status { background: rgba(0,255,0,0.1); padding: 1rem; border-radius: 8px; margin: 2rem 0; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <div class="logo">🕉️ AyurAI Veda</div>
            <div class="subtitle">Ancient Wisdom. Intelligent Health.</div>
        </div>
        
        <div class="status">
            <h3>✅ Vercel Deployment Status: WORKING</h3>
            <p>Serverless function is running successfully!</p>
        </div>
        
        <div class="features">
            <div class="feature">
                <h3>🧠 Tridosha Intelligence</h3>
                <p>AI-powered analysis of Vata, Pitta, and Kapha doshas for personalized health insights.</p>
            </div>
            <div class="feature">
                <h3>💬 AyurVaani Chat</h3>
                <p>Conversational AI assistant with comprehensive Ayurvedic knowledge base.</p>
            </div>
            <div class="feature">
                <h3>📊 Health Assessment</h3>
                <p>Comprehensive constitutional analysis with personalized recommendations.</p>
            </div>
        </div>
        
        <div style="text-align: center;">
            <a href="/api/health" class="btn">🔍 Health Check</a>
            <a href="/api/test" class="btn">🧪 Test Analysis</a>
        </div>
        
        <div style="text-align: center; margin-top: 3rem; opacity: 0.7;">
            <p>© 2026 AyurAI Veda. All rights reserved.</p>
            <p>A Sudarshan Technologies Production</p>
        </div>
    </div>
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(HOME_TEMPLATE)

@app.route('/api/health')
def health_check():
    return jsonify({
        'status': 'healthy',
        'service': 'AyurAI Veda',
        'version': '2.0.0',
        'timestamp': datetime.now().isoformat(),
        'environment': 'vercel',
        'message': 'Serverless function working perfectly!'
    })

@app.route('/api/test')
def test_analysis():
    # Simple test analysis
    sample_result = {
        'dominant': 'Vata',
        'scores': {'vata': 45, 'pitta': 30, 'kapha': 25},
        'risk': 'Moderate',
        'message': 'Test analysis successful!',
        'recommendations': [
            'Follow regular daily routine',
            'Eat warm, cooked foods',
            'Practice oil massage',
            'Get adequate sleep'
        ]
    }
    return jsonify(sample_result)

@app.route('/api/analyze', methods=['POST'])
def analyze():
    try:
        # Simple analysis without external dependencies
        return jsonify({
            'status': 'success',
            'dominant': 'Pitta',
            'scores': {'vata': 25, 'pitta': 50, 'kapha': 25},
            'risk': 'Low',
            'message': 'Basic analysis complete',
            'timestamp': datetime.now().isoformat()
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Vercel handler
def handler(request):
    return app(request.environ, lambda *args: None)

if __name__ == '__main__':
    app.run(debug=True)