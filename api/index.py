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
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/assessment')
def assessment():
    return render_template('assessment.html')

@app.route('/chatbot')
def chatbot():
    return render_template('chatbot.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/clinical-assessment')
def clinical_assessment():
    return render_template('clinical_assessment.html')

@app.route('/comprehensive-assessment')
def comprehensive_assessment():
    return render_template('comprehensive_assessment.html')

@app.route('/feedback')
def feedback():
    return render_template('feedback.html')

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

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
        result = analyze_clinical(data)
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
        
        # Send email
        email_sent = send_feedback_email(data)
        
        if email_sent:
            return jsonify({'success': True, 'message': 'Feedback submitted successfully! We will contact you soon.'})
        else:
            # Log feedback even if email fails
            log_feedback(data)
            return jsonify({'success': True, 'message': 'Feedback received and logged successfully'})
    except Exception as e:
        print(f"Feedback error: {str(e)}")
        return jsonify({'success': False, 'message': 'An error occurred. Please try again.'}), 500

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
    """Clinical assessment analysis"""
    vata_score = pitta_score = kapha_score = 0
    
    # Body structure
    if data.get('body_structure') == 'lean': vata_score += 20
    elif data.get('body_structure') == 'moderate': pitta_score += 20
    elif data.get('body_structure') == 'heavy': kapha_score += 20
    
    # Skin
    if data.get('skin') == 'dry': vata_score += 15
    elif data.get('skin') == 'normal': pitta_score += 15
    elif data.get('skin') == 'oily': kapha_score += 15
    
    # Appetite
    if data.get('appetite') == 'irregular': vata_score += 15
    elif data.get('appetite') == 'excessive': pitta_score += 15
    elif data.get('appetite') == 'low': kapha_score += 15
    
    # Digestion
    if data.get('digestion') == 'gas': vata_score += 15
    elif data.get('digestion') == 'normal': pitta_score += 15
    elif data.get('digestion') == 'slow': kapha_score += 15
    
    # Sleep
    if data.get('sleep') == 'poor': vata_score += 10
    elif data.get('sleep') == 'good': pitta_score += 10
    elif data.get('sleep') == 'excellent': kapha_score += 10
    
    # Energy
    if data.get('energy') == 'fluctuating': vata_score += 10
    elif data.get('energy') == 'hyperactive': pitta_score += 10
    elif data.get('energy') == 'stable': kapha_score += 10
    
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
    
    max_score = max(vata_percent, pitta_percent, kapha_percent)
    if max_score >= 50: risk = 'High'
    elif max_score >= 40: risk = 'Moderate'
    else: risk = 'Low'
    
    return {
        'dominant': dominant.capitalize(),
        'scores': scores,
        'risk': risk,
        'dosha_state': 'Balanced' if max_score < 45 else 'Imbalanced',
        'agni_state': 'Strong' if data.get('digestion') == 'normal' else 'Weak',
        'recommendations': get_recommendations(dominant),
        'diet_suggestions': get_diet_suggestions(dominant),
        'lifestyle_tips': get_lifestyle_tips(dominant),
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
        return """Hello! I'm AyurVaani™, your Ayurvedic wellness assistant. I can help you with:<br><br>
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
