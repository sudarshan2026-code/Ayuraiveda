from flask import Flask, render_template, request, jsonify, session, redirect, url_for, flash
from functools import wraps
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

app = Flask(__name__, template_folder='../templates', static_folder='../static')
app.secret_key = 'ayurveda_secret_key_2024'

from auth_db import AuthDatabase
auth_db = AuthDatabase()

from ai_engine import TridoshaIntelligenceEngine
tie = TridoshaIntelligenceEngine()

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please login to access this page', 'error')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/signup')
def signup():
    return render_template('signup.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/assessment')
@login_required
def assessment():
    user = auth_db.get_user(session['user_id'])
    return render_template('assessment.html', user=user)

@app.route('/chatbot')
@login_required
def chatbot():
    return render_template('chatbot.html')

@app.route('/profile')
@login_required
def profile():
    user = auth_db.get_user(session['user_id'])
    assessments = auth_db.get_user_assessments(session['user_id'])
    return render_template('profile.html', user=user, assessments=assessments)

@app.route('/auth/login', methods=['POST'])
def auth_login():
    data = request.json
    success, user = auth_db.login_user(data['email'], data['password'])
    if success:
        session['user_id'] = user['id']
        session['user_type'] = user['user_type']
        session['user_name'] = user['name']
        return jsonify({'success': True, 'message': 'Login successful'})
    return jsonify({'success': False, 'message': 'Invalid credentials'})

@app.route('/auth/signup', methods=['POST'])
def auth_signup():
    data = request.json
    success, message = auth_db.register_user(
        data['email'], data['password'], data['user_type'],
        data['name'], data.get('phone'), data.get('specialization')
    )
    return jsonify({'success': success, 'message': message})

@app.route('/analyze', methods=['POST'])
@login_required
def analyze():
    data = request.json
    result = tie.analyze(data)
    auth_db.save_assessment(session['user_id'], data, result, data.get('patient_name'), data.get('patient_phone'))
    return jsonify(result)

@app.route('/chat', methods=['POST'])
def chat():
    from simple_pdf_reader import SimplePDFKnowledge
    data = request.json
    message = data.get('message', '')
    kb = SimplePDFKnowledge()
    response = kb.get_answer(message)
    return jsonify({'response': response})

# Vercel handler
def handler(request):
    return app(request.environ, lambda *args: None)
