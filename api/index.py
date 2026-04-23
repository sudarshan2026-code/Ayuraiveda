from flask import Flask, request, jsonify, render_template_string
import json
from datetime import datetime
import random

app = Flask(__name__)

# CSS Styles
STYLES = """
<style>
* { margin: 0; padding: 0; box-sizing: border-box; }
body { 
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    background: linear-gradient(135deg, #0a0a0a, #1a1a2e, #16213e);
    color: #ffffff;
    min-height: 100vh;
    line-height: 1.6;
}
.container { max-width: 1200px; margin: 0 auto; padding: 2rem; }
.header { text-align: center; margin-bottom: 3rem; }
.logo { 
    font-size: 3rem; font-weight: bold; margin-bottom: 1rem; 
    background: linear-gradient(45deg, #00D9FF, #7B2FFF, #FF2E97);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent; 
}
.subtitle { font-size: 1.2rem; opacity: 0.8; margin-bottom: 2rem; }
.nav { display: flex; justify-content: center; gap: 2rem; margin: 2rem 0; flex-wrap: wrap; }
.nav a { 
    color: #00D9FF; text-decoration: none; padding: 0.5rem 1rem;
    border: 1px solid rgba(0,217,255,0.3); border-radius: 8px;
    transition: all 0.3s;
}
.nav a:hover { background: rgba(0,217,255,0.1); transform: translateY(-2px); }
.features { display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 2rem; margin: 3rem 0; }
.feature { 
    background: rgba(255,255,255,0.1); padding: 2rem; border-radius: 12px; 
    border: 1px solid rgba(0,217,255,0.3); transition: transform 0.3s;
}
.feature:hover { transform: translateY(-5px); }
.feature h3 { color: #00D9FF; margin-bottom: 1rem; }
.btn { 
    display: inline-block; padding: 1rem 2rem; margin: 1rem;
    background: linear-gradient(45deg, #00D9FF, #7B2FFF);
    color: white; text-decoration: none; border-radius: 8px;
    font-weight: bold; transition: transform 0.3s; border: none; cursor: pointer;
}
.btn:hover { transform: translateY(-2px); }
.status { background: rgba(0,255,0,0.1); padding: 1rem; border-radius: 8px; margin: 2rem 0; }
.form-group { margin: 1rem 0; }
.form-group label { display: block; margin-bottom: 0.5rem; color: #00D9FF; }
.form-group select, .form-group input { 
    width: 100%; padding: 0.8rem; border-radius: 8px; border: 1px solid rgba(0,217,255,0.3);
    background: rgba(255,255,255,0.1); color: #fff;
}
.results { background: rgba(123,47,255,0.1); padding: 2rem; border-radius: 12px; margin: 2rem 0; }
.dosha-meter { background: rgba(0,0,0,0.3); height: 30px; border-radius: 15px; margin: 1rem 0; overflow: hidden; }
.dosha-fill { height: 100%; border-radius: 15px; transition: width 0.5s; }
.vata { background: linear-gradient(45deg, #00D9FF, #0099CC); }
.pitta { background: linear-gradient(45deg, #FF2E97, #CC2577); }
.kapha { background: linear-gradient(45deg, #7B2FFF, #5522CC); }
.chat-container { max-width: 800px; margin: 0 auto; }
.chat-messages { 
    height: 400px; overflow-y: auto; background: rgba(0,0,0,0.3); 
    padding: 1rem; border-radius: 12px; margin-bottom: 1rem;
}
.message { margin: 1rem 0; padding: 1rem; border-radius: 8px; }
.user-message { background: rgba(0,217,255,0.2); text-align: right; }
.bot-message { background: rgba(123,47,255,0.2); }
.chat-input { display: flex; gap: 1rem; }
.chat-input input { flex: 1; padding: 1rem; border-radius: 8px; border: 1px solid rgba(0,217,255,0.3); background: rgba(255,255,255,0.1); color: #fff; }
.footer { text-align: center; margin-top: 3rem; opacity: 0.7; border-top: 1px solid rgba(0,217,255,0.3); padding-top: 2rem; }
</style>
"""

# HTML Templates
HOME_TEMPLATE = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AyurAI Veda - Ancient Wisdom. Intelligent Health.</title>
    {STYLES}
</head>
<body>
    <div class="container">
        <div class="header">
            <div class="logo">🕉️ AyurAI Veda</div>
            <div class="subtitle">Ancient Wisdom. Intelligent Health.</div>
            <nav class="nav">
                <a href="/">Home</a>
                <a href="/about">About</a>
                <a href="/assessment">Clinical Assessment</a>
                <a href="/chat">AyurVaani Chat</a>
                <a href="/contact">Contact</a>
            </nav>
        </div>
        
        <div class="status">
            <h3>✅ Vercel Deployment: WORKING PERFECTLY!</h3>
            <p>Serverless AyurAI Veda is running successfully with all features!</p>
        </div>
        
        <div class="features">
            <div class="feature">
                <h3>🧠 Tridosha Intelligence Engine</h3>
                <p>AI-powered analysis of Vata, Pitta, and Kapha doshas for personalized health insights based on ancient Ayurvedic principles.</p>
                <a href="/assessment" class="btn">Start Assessment</a>
            </div>
            <div class="feature">
                <h3>💬 AyurVaani AI Chatbot</h3>
                <p>Conversational AI assistant with comprehensive Ayurvedic knowledge base for instant health guidance.</p>
                <a href="/chat" class="btn">Chat Now</a>
            </div>
            <div class="feature">
                <h3>📊 Comprehensive Analysis</h3>
                <p>Detailed constitutional analysis with personalized diet, yoga, and lifestyle recommendations.</p>
                <a href="/about" class="btn">Learn More</a>
            </div>
        </div>
        
        <div class="footer">
            <p>© 2026 AyurAI Veda. All rights reserved.</p>
            <p>A Sudarshan Technologies Production</p>
        </div>
    </div>
</body>
</html>
"""

ABOUT_TEMPLATE = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>About - AyurAI Veda</title>
    {STYLES}
</head>
<body>
    <div class="container">
        <div class="header">
            <div class="logo">🕉️ AyurAI Veda</div>
            <div class="subtitle">Ancient Wisdom. Intelligent Health.</div>
            <nav class="nav">
                <a href="/">Home</a>
                <a href="/about">About</a>
                <a href="/assessment">Clinical Assessment</a>
                <a href="/chat">AyurVaani Chat</a>
                <a href="/contact">Contact</a>
            </nav>
        </div>
        
        <div class="features">
            <div class="feature">
                <h3>🌿 What is Ayurveda?</h3>
                <p>Ayurveda is a 5,000-year-old system of natural healing from India. It emphasizes prevention and treatment through lifestyle practices, diet, herbal remedies, and spiritual practices.</p>
            </div>
            <div class="feature">
                <h3>⚖️ The Three Doshas</h3>
                <p><strong>Vata (Air + Space):</strong> Governs movement, creativity, nervous system<br>
                <strong>Pitta (Fire + Water):</strong> Governs metabolism, digestion, transformation<br>
                <strong>Kapha (Water + Earth):</strong> Governs structure, stability, immunity</p>
            </div>
            <div class="feature">
                <h3>🤖 AI Enhancement</h3>
                <p>Our Tridosha Intelligence Engine combines traditional Ayurvedic wisdom with modern AI to provide personalized health insights and recommendations.</p>
            </div>
        </div>
        
        <div class="footer">
            <p>© 2026 AyurAI Veda. All rights reserved.</p>
            <p>A Sudarshan Technologies Production</p>
        </div>
    </div>
</body>
</html>
"""

ASSESSMENT_TEMPLATE = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Clinical Assessment - AyurAI Veda</title>
    {STYLES}
</head>
<body>
    <div class="container">
        <div class="header">
            <div class="logo">🕉️ AyurAI Veda</div>
            <div class="subtitle">Tridosha Intelligence Engine Assessment</div>
            <nav class="nav">
                <a href="/">Home</a>
                <a href="/about">About</a>
                <a href="/assessment">Clinical Assessment</a>
                <a href="/chat">AyurVaani Chat</a>
                <a href="/contact">Contact</a>
            </nav>
        </div>
        
        <form id="assessmentForm" onsubmit="analyzeHealth(event)">
            <div class="features">
                <div class="feature">
                    <h3>🏃‍♂️ Physical Constitution</h3>
                    <div class="form-group">
                        <label>Body Build:</label>
                        <select name="body_build" required>
                            <option value="">Select...</option>
                            <option value="thin">Thin/Lean (Vata)</option>
                            <option value="medium">Medium/Athletic (Pitta)</option>
                            <option value="heavy">Heavy/Stocky (Kapha)</option>
                        </select>
                    </div>
                    <div class="form-group">
                        <label>Skin Type:</label>
                        <select name="skin" required>
                            <option value="">Select...</option>
                            <option value="dry">Dry/Rough (Vata)</option>
                            <option value="oily">Oily/Sensitive (Pitta)</option>
                            <option value="smooth">Smooth/Thick (Kapha)</option>
                        </select>
                    </div>
                </div>
                
                <div class="feature">
                    <h3>🍽️ Digestion & Appetite</h3>
                    <div class="form-group">
                        <label>Appetite:</label>
                        <select name="appetite" required>
                            <option value="">Select...</option>
                            <option value="variable">Variable/Irregular (Vata)</option>
                            <option value="strong">Strong/Sharp (Pitta)</option>
                            <option value="steady">Steady/Slow (Kapha)</option>
                        </select>
                    </div>
                    <div class="form-group">
                        <label>Digestion:</label>
                        <select name="digestion" required>
                            <option value="">Select...</option>
                            <option value="irregular">Irregular/Gas (Vata)</option>
                            <option value="quick">Quick/Acidic (Pitta)</option>
                            <option value="slow">Slow/Heavy (Kapha)</option>
                        </select>
                    </div>
                </div>
                
                <div class="feature">
                    <h3>😴 Sleep & Energy</h3>
                    <div class="form-group">
                        <label>Sleep Pattern:</label>
                        <select name="sleep" required>
                            <option value="">Select...</option>
                            <option value="light">Light/Restless (Vata)</option>
                            <option value="moderate">Moderate/Sound (Pitta)</option>
                            <option value="deep">Deep/Heavy (Kapha)</option>
                        </select>
                    </div>
                    <div class="form-group">
                        <label>Energy Level:</label>
                        <select name="energy" required>
                            <option value="">Select...</option>
                            <option value="variable">Variable/Bursts (Vata)</option>
                            <option value="moderate">Moderate/Steady (Pitta)</option>
                            <option value="steady">Steady/Enduring (Kapha)</option>
                        </select>
                    </div>
                </div>
            </div>
            
            <div style="text-align: center;">
                <button type="submit" class="btn">🔍 Analyze with Tridosha Intelligence Engine</button>
            </div>
        </form>
        
        <div id="results" style="display: none;"></div>
        
        <div class="footer">
            <p>© 2026 AyurAI Veda. All rights reserved.</p>
            <p>A Sudarshan Technologies Production</p>
        </div>
    </div>
    
    <script>
    async function analyzeHealth(event) {{
        event.preventDefault();
        const formData = new FormData(event.target);
        const data = Object.fromEntries(formData);
        
        try {{
            const response = await fetch('/api/analyze', {{
                method: 'POST',
                headers: {{ 'Content-Type': 'application/json' }},
                body: JSON.stringify(data)
            }});
            const result = await response.json();
            displayResults(result);
        }} catch (error) {{
            console.error('Error:', error);
        }}
    }}
    
    function displayResults(result) {{
        const resultsDiv = document.getElementById('results');
        resultsDiv.innerHTML = `
            <div class="results">
                <h2>🎯 Your Tridosha Analysis Results</h2>
                <div class="feature">
                    <h3>Dominant Dosha: ${{result.dominant}}</h3>
                    <p>Risk Level: <strong>${{result.risk}}</strong></p>
                    
                    <h4>Dosha Distribution:</h4>
                    <div>
                        <label>Vata: ${{result.scores.vata}}%</label>
                        <div class="dosha-meter">
                            <div class="dosha-fill vata" style="width: ${{result.scores.vata}}%"></div>
                        </div>
                    </div>
                    <div>
                        <label>Pitta: ${{result.scores.pitta}}%</label>
                        <div class="dosha-meter">
                            <div class="dosha-fill pitta" style="width: ${{result.scores.pitta}}%"></div>
                        </div>
                    </div>
                    <div>
                        <label>Kapha: ${{result.scores.kapha}}%</label>
                        <div class="dosha-meter">
                            <div class="dosha-fill kapha" style="width: ${{result.scores.kapha}}%"></div>
                        </div>
                    </div>
                    
                    <h4>🍎 Personalized Recommendations:</h4>
                    <ul>
                        ${{result.recommendations.map(rec => `<li>${{rec}}</li>`).join('')}}
                    </ul>
                </div>
            </div>
        `;
        resultsDiv.style.display = 'block';
        resultsDiv.scrollIntoView({{ behavior: 'smooth' }});
    }}
    </script>
</body>
</html>
"""

CHAT_TEMPLATE = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AyurVaani Chat - AyurAI Veda</title>
    {STYLES}
</head>
<body>
    <div class="container">
        <div class="header">
            <div class="logo">🕉️ AyurAI Veda</div>
            <div class="subtitle">AyurVaani AI Chatbot</div>
            <nav class="nav">
                <a href="/">Home</a>
                <a href="/about">About</a>
                <a href="/assessment">Clinical Assessment</a>
                <a href="/chat">AyurVaani Chat</a>
                <a href="/contact">Contact</a>
            </nav>
        </div>
        
        <div class="chat-container">
            <div class="feature">
                <h3>💬 Chat with AyurVaani</h3>
                <p>Ask questions about Ayurveda, doshas, health tips, and lifestyle recommendations.</p>
            </div>
            
            <div class="chat-messages" id="chatMessages">
                <div class="message bot-message">
                    <strong>AyurVaani:</strong> Namaste! I'm AyurVaani, your Ayurvedic AI assistant. How can I help you with your health and wellness journey today?
                </div>
            </div>
            
            <div class="chat-input">
                <input type="text" id="userInput" placeholder="Ask about Ayurveda, doshas, diet, yoga..." onkeypress="handleKeyPress(event)">
                <button onclick="sendMessage()" class="btn">Send</button>
            </div>
        </div>
        
        <div class="footer">
            <p>© 2026 AyurAI Veda. All rights reserved.</p>
            <p>A Sudarshan Technologies Production</p>
        </div>
    </div>
    
    <script>
    function handleKeyPress(event) {{
        if (event.key === 'Enter') {{
            sendMessage();
        }}
    }}
    
    async function sendMessage() {{
        const input = document.getElementById('userInput');
        const message = input.value.trim();
        if (!message) return;
        
        // Add user message
        addMessage(message, 'user');
        input.value = '';
        
        try {{
            const response = await fetch('/api/chat', {{
                method: 'POST',
                headers: {{ 'Content-Type': 'application/json' }},
                body: JSON.stringify({{ message: message }})
            }});
            const result = await response.json();
            addMessage(result.response, 'bot');
        }} catch (error) {{
            addMessage('Sorry, I encountered an error. Please try again.', 'bot');
        }}
    }}
    
    function addMessage(message, sender) {{
        const messagesDiv = document.getElementById('chatMessages');
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${{sender}}-message`;
        messageDiv.innerHTML = `<strong>${{sender === 'user' ? 'You' : 'AyurVaani'}}:</strong> ${{message}}`;
        messagesDiv.appendChild(messageDiv);
        messagesDiv.scrollTop = messagesDiv.scrollHeight;
    }}
    </script>
</body>
</html>
"""

CONTACT_TEMPLATE = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Contact - AyurAI Veda</title>
    {STYLES}
</head>
<body>
    <div class="container">
        <div class="header">
            <div class="logo">🕉️ AyurAI Veda</div>
            <div class="subtitle">Contact & Information</div>
            <nav class="nav">
                <a href="/">Home</a>
                <a href="/about">About</a>
                <a href="/assessment">Clinical Assessment</a>
                <a href="/chat">AyurVaani Chat</a>
                <a href="/contact">Contact</a>
            </nav>
        </div>
        
        <div class="features">
            <div class="feature">
                <h3>📧 Contact Information</h3>
                <p><strong>Email:</strong> zjay5398@gmail.com</p>
                <p><strong>Project:</strong> AyurAI Veda - AI-Powered Ayurvedic Health System</p>
                <p><strong>Technology:</strong> Flask, Python, Vercel Serverless</p>
            </div>
            <div class="feature">
                <h3>⚠️ Important Disclaimer</h3>
                <p><strong>This system provides educational and preventive insights only. It is NOT a medical diagnosis platform.</strong></p>
                <p>Always consult qualified healthcare professionals for medical advice.</p>
            </div>
            <div class="feature">
                <h3>🏆 About the Project</h3>
                <p>AyurAI Veda integrates ancient Ayurvedic wisdom with modern AI technology to provide personalized health insights based on the Tridosha system.</p>
                <p><strong>A Sudarshan Technologies Production</strong></p>
            </div>
        </div>
        
        <div class="footer">
            <p>© 2026 AyurAI Veda. All rights reserved.</p>
            <p>A Sudarshan Technologies Production</p>
        </div>
    </div>
</body>
</html>
"""

# Routes
@app.route('/')
def home():
    return HOME_TEMPLATE

@app.route('/about')
def about():
    return ABOUT_TEMPLATE

@app.route('/assessment')
def assessment():
    return ASSESSMENT_TEMPLATE

@app.route('/chat')
def chat():
    return CHAT_TEMPLATE

@app.route('/contact')
def contact():
    return CONTACT_TEMPLATE

@app.route('/api/analyze', methods=['POST'])
def analyze():
    try:
        data = request.get_json()
        
        # Simple scoring logic
        vata_score = 0
        pitta_score = 0
        kapha_score = 0
        
        # Body build scoring
        if data.get('body_build') == 'thin': vata_score += 25
        elif data.get('body_build') == 'medium': pitta_score += 25
        elif data.get('body_build') == 'heavy': kapha_score += 25
        
        # Skin scoring
        if data.get('skin') == 'dry': vata_score += 20
        elif data.get('skin') == 'oily': pitta_score += 20
        elif data.get('skin') == 'smooth': kapha_score += 20
        
        # Appetite scoring
        if data.get('appetite') == 'variable': vata_score += 15
        elif data.get('appetite') == 'strong': pitta_score += 15
        elif data.get('appetite') == 'steady': kapha_score += 15
        
        # Digestion scoring
        if data.get('digestion') == 'irregular': vata_score += 20
        elif data.get('digestion') == 'quick': pitta_score += 20
        elif data.get('digestion') == 'slow': kapha_score += 20
        
        # Sleep scoring
        if data.get('sleep') == 'light': vata_score += 10
        elif data.get('sleep') == 'moderate': pitta_score += 10
        elif data.get('sleep') == 'deep': kapha_score += 10
        
        # Energy scoring
        if data.get('energy') == 'variable': vata_score += 10
        elif data.get('energy') == 'moderate': pitta_score += 10
        elif data.get('energy') == 'steady': kapha_score += 10
        
        # Normalize scores
        total = vata_score + pitta_score + kapha_score
        if total > 0:
            vata_percent = round((vata_score / total) * 100)
            pitta_percent = round((pitta_score / total) * 100)
            kapha_percent = round((kapha_score / total) * 100)
        else:
            vata_percent = pitta_percent = kapha_percent = 33
        
        # Determine dominant dosha
        scores = {'vata': vata_percent, 'pitta': pitta_percent, 'kapha': kapha_percent}
        dominant = max(scores, key=scores.get)
        
        # Risk level
        max_score = max(vata_percent, pitta_percent, kapha_percent)
        if max_score >= 50: risk = 'High'
        elif max_score >= 40: risk = 'Moderate'
        else: risk = 'Low'
        
        # Recommendations based on dominant dosha
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
        
        return jsonify({
            'status': 'success',
            'dominant': dominant.capitalize(),
            'scores': scores,
            'risk': risk,
            'recommendations': recommendations[dominant],
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/chat', methods=['POST'])
def chat_api():
    try:
        data = request.get_json()
        message = data.get('message', '').lower()
        
        # Simple chatbot responses
        responses = {
            'vata': 'Vata dosha governs movement and is associated with air and space elements. When balanced, it promotes creativity and flexibility. When imbalanced, it can cause anxiety, dry skin, and digestive issues. Balance vata with warm foods, regular routines, and oil massage.',
            'pitta': 'Pitta dosha governs metabolism and is associated with fire and water elements. When balanced, it promotes good digestion and sharp intellect. When imbalanced, it can cause acidity, anger, and skin inflammation. Balance pitta with cooling foods and avoiding excessive heat.',
            'kapha': 'Kapha dosha governs structure and is associated with water and earth elements. When balanced, it provides strength and immunity. When imbalanced, it can cause weight gain, congestion, and lethargy. Balance kapha with light foods, regular exercise, and staying active.',
            'diet': 'Ayurvedic diet is based on your dosha constitution. Vata types need warm, moist foods. Pitta types need cooling, less spicy foods. Kapha types need light, warm, spicy foods. Eat fresh, seasonal foods and avoid processed items.',
            'yoga': 'Yoga is an integral part of Ayurveda. Vata types benefit from gentle, grounding poses. Pitta types need cooling, moderate practices. Kapha types need energizing, vigorous sequences. Practice regularly for best results.',
            'sleep': 'Good sleep is crucial for health. Vata types need 7-8 hours with regular bedtime. Pitta types need 6-7 hours in cool environment. Kapha types need 6-7 hours and should wake early. Avoid screens before bed.',
            'meditation': 'Meditation balances all doshas. Vata types benefit from grounding meditations. Pitta types need cooling, calming practices. Kapha types benefit from energizing techniques. Start with 10-15 minutes daily.'
        }
        
        # Find matching response
        response = "I'm AyurVaani, your Ayurvedic AI assistant. I can help you with questions about doshas (vata, pitta, kapha), diet, yoga, sleep, meditation, and general Ayurvedic principles. What would you like to know?"
        
        for keyword, resp in responses.items():
            if keyword in message:
                response = resp
                break
        
        # Add some variety
        greetings = ['Namaste!', 'Great question!', 'According to Ayurveda,', 'Here\'s what I can tell you:']
        response = f"{random.choice(greetings)} {response}"
        
        return jsonify({
            'response': response,
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/health')
def health():
    return jsonify({
        'status': 'healthy',
        'service': 'AyurAI Veda',
        'version': '2.0.0',
        'features': ['Assessment', 'Chat', 'Analysis'],
        'timestamp': datetime.now().isoformat()
    })

if __name__ == '__main__':
    app.run(debug=True)