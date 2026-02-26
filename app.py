from flask import Flask, render_template, request, jsonify, send_file, session, redirect, url_for, flash
from functools import wraps
from translations import get_translation
from chat_db import ChatDatabase
import io
import re
from reportlab.lib.pagesizes import letter, A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib.colors import HexColor
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import Paragraph, Frame
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
import os

app = Flask(__name__)
app.secret_key = 'ayurveda_secret_key_2024'
db = ChatDatabase()

# Initialize auth database
from auth_db import AuthDatabase
auth_db = AuthDatabase()

# Login required decorator
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please login to access this page', 'error')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

# Try to use advanced engine, fallback to ML, then basic
try:
    from advanced_ai_engine import AdvancedTridoshaEngine
    tie = AdvancedTridoshaEngine()
    print("✓ Using Advanced Tridosha Engine (Ayurvedic Logic)")
except:
    try:
        from ml_assessment_engine import MLTridoshaEngine
        tie = MLTridoshaEngine()
        tie.load_model()
        print("✓ Using ML-enhanced assessment engine")
    except:
        from ai_engine import TridoshaIntelligenceEngine
        tie = TridoshaIntelligenceEngine()
        print("✓ Using basic assessment engine")

# Load disease predictor
from disease_predictor import DiseasePredictor
disease_predictor = DiseasePredictor()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/assessment')
@login_required
def assessment():
    user = auth_db.get_user(session['user_id'])
    return render_template('assessment.html', user=user)

@app.route('/chatbot')
@login_required
def chatbot():
    return render_template('chatbot.html')

@app.route('/login')
def login():
    if 'user_id' in session:
        return redirect(url_for('home'))
    return render_template('login.html')

@app.route('/signup')
def signup():
    if 'user_id' in session:
        return redirect(url_for('home'))
    return render_template('signup.html')

@app.route('/logout')
def logout():
    session.clear()
    flash('Logged out successfully', 'success')
    return redirect(url_for('home'))

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

@app.route('/profile')
@login_required
def profile():
    user = auth_db.get_user(session['user_id'])
    assessments = auth_db.get_user_assessments(session['user_id'])
    return render_template('profile.html', user=user, assessments=assessments)

@app.route('/view-report/<int:assessment_id>')
@login_required
def view_report(assessment_id):
    assessment = auth_db.get_assessment(assessment_id)
    if not assessment or assessment['user_id'] != session['user_id']:
        flash('Assessment not found', 'error')
        return redirect(url_for('profile'))
    return render_template('view_report.html', assessment=assessment)

@app.route('/download-assessment-report/<int:assessment_id>')
@login_required
def download_assessment_report(assessment_id):
    assessment = auth_db.get_assessment(assessment_id)
    if not assessment or assessment['user_id'] != session['user_id']:
        flash('Assessment not found', 'error')
        return redirect(url_for('profile'))
    
    data = assessment['result_data']
    data['language'] = 'en'
    
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4
    
    font_regular = 'Helvetica'
    font_bold = 'Helvetica-Bold'
    
    orange = HexColor('#FF9933')
    green = HexColor('#138808')
    dark_blue = HexColor('#1a237e')
    dark_gray = HexColor('#333333')
    light_gray = HexColor('#666666')
    bg_gray = HexColor('#f5f5f5')
    
    c.setFillColor(dark_blue)
    c.rect(0, height - 120, width, 120, fill=True, stroke=False)
    c.setFillColor(HexColor('#FFFFFF'))
    c.setFont(font_bold, 22)
    c.drawCentredString(width/2, height - 45, "AyurAI Veda™ Health Report")
    c.setFont(font_regular, 9)
    c.drawCentredString(width/2, height - 65, "Powered by Tridosha Intelligence Engine™")
    
    from datetime import datetime
    c.setFont('Helvetica', 9)
    c.drawCentredString(width/2, height - 85, f"Report Date: {assessment['created_at']}")
    c.drawCentredString(width/2, height - 100, f"Report ID: AV-{assessment['id']:06d}")
    
    y = height - 150
    
    if assessment.get('patient_name'):
        draw_section_header(c, "PATIENT INFORMATION", 50, y, width - 100, dark_blue, font_bold)
        y -= 35
        c.setFillColor(dark_gray)
        c.setFont(font_regular, 10)
        c.drawString(70, y, f"Name: {assessment['patient_name']}")
        y -= 15
        if assessment.get('patient_phone'):
            c.drawString(70, y, f"Phone: {assessment['patient_phone']}")
            y -= 15
        y -= 15
    
    draw_section_header(c, "CLINICAL SUMMARY", 50, y, width - 100, dark_blue, font_bold)
    y -= 40
    
    c.setFillColor(bg_gray)
    c.roundRect(50, y - 45, width - 100, 50, 5, fill=True, stroke=False)
    c.setFillColor(dark_gray)
    c.setFont(font_bold, 13)
    c.drawString(70, y - 18, "Dominant Dosha:")
    c.setFillColor(orange)
    c.setFont(font_bold, 17)
    c.drawString(250, y - 18, data['dominant'])
    y -= 55
    
    risk = data['risk']
    risk_color = HexColor('#d32f2f') if risk == 'High' else HexColor('#f57c00') if risk == 'Moderate' else HexColor('#388e3c')
    c.setFillColor(dark_gray)
    c.setFont(font_bold, 11)
    c.drawString(70, y, "Risk Level:")
    c.setFillColor(risk_color)
    c.setFont(font_bold, 13)
    c.drawString(250, y, risk.upper())
    y -= 40
    
    draw_section_header(c, "DOSHA ANALYSIS", 50, y, width - 100, dark_blue, font_bold)
    y -= 40
    
    c.setFillColor(dark_blue)
    c.rect(50, y - 25, width - 100, 25, fill=True, stroke=False)
    c.setFillColor(HexColor('#FFFFFF'))
    c.setFont(font_bold, 10)
    c.drawString(70, y - 15, "Dosha Type")
    c.drawString(200, y - 15, "Score")
    c.drawString(320, y - 15, "Visual")
    y -= 30
    
    doshas = [
        ('vata', HexColor('#9C27B0'), 'Vata'),
        ('pitta', HexColor('#FF5722'), 'Pitta'),
        ('kapha', HexColor('#4CAF50'), 'Kapha')
    ]
    
    for i, (dosha, color, label) in enumerate(doshas):
        score = data['scores'][dosha]
        if i % 2 == 0:
            c.setFillColor(bg_gray)
            c.rect(50, y - 32, width - 100, 32, fill=True, stroke=False)
        c.setFillColor(dark_gray)
        c.setFont(font_bold, 10)
        c.drawString(70, y - 16, label)
        c.setFont('Helvetica', 10)
        c.drawString(200, y - 16, f"{score}%")
        c.setStrokeColor(HexColor('#CCCCCC'))
        c.setLineWidth(1)
        c.rect(300, y - 20, 200, 14, fill=False, stroke=True)
        c.setFillColor(color)
        c.rect(300, y - 20, 200 * (score / 100), 14, fill=True, stroke=False)
        y -= 37
    
    y -= 20
    
    if data.get('disease_prediction'):
        if y < 200:
            c.showPage()
            y = height - 50
        draw_section_header(c, "AI DISEASE RISK PREDICTIONS", 50, y, width - 100, HexColor('#ff9800'), font_bold)
        y -= 35
        disease_pred = data['disease_prediction']
        c.setFillColor(dark_gray)
        c.setFont(font_bold, 9)
        c.drawString(70, y, "Predicted Health Risks:")
        y -= 18
        for disease in disease_pred['diseases'][:5]:
            if y < 130:
                c.showPage()
                y = height - 50
            c.setFillColor(HexColor('#ff9800'))
            c.circle(70, y - 3, 3, fill=True, stroke=False)
            c.setFillColor(dark_gray)
            c.setFont(font_regular, 8.5)
            c.drawString(85, y, disease.replace('(', '- ').replace(')', ''))
            y -= 15
        y -= 15
    
    draw_section_header(c, "CLINICAL RECOMMENDATIONS", 50, y, width - 100, green, font_bold)
    y -= 35
    c.setFillColor(dark_gray)
    c.setFont(font_regular, 8.5)
    for i, rec in enumerate(data['recommendations'], 1):
        if y < 130:
            c.showPage()
            y = height - 50
        rec_lines = wrap_text(rec, 80)
        box_height = len(rec_lines) * 13 + 18
        c.setFillColor(bg_gray)
        c.roundRect(50, y - box_height, width - 100, box_height, 3, fill=True, stroke=False)
        c.setFillColor(green)
        c.circle(70, y - 13, 10, fill=True, stroke=False)
        c.setFillColor(HexColor('#FFFFFF'))
        c.setFont('Helvetica-Bold', 9)
        c.drawCentredString(70, y - 16, str(i))
        c.setFillColor(dark_gray)
        c.setFont(font_regular, 8.5)
        y_text = y - 13
        for line in rec_lines:
            c.drawString(90, y_text, line)
            y_text -= 13
        y -= box_height + 10
    
    y = 100
    c.setStrokeColor(dark_blue)
    c.setLineWidth(1)
    c.line(50, y, width - 50, y)
    y -= 15
    c.setFillColor(light_gray)
    c.setFont(font_bold, 8)
    c.drawCentredString(width/2, y, "IMPORTANT DISCLAIMER")
    y -= 13
    c.setFont(font_regular, 7)
    disclaimer = "This report provides educational and preventive health insights only. It is NOT a medical diagnosis. Always consult qualified healthcare professionals for medical advice."
    disc_lines = wrap_text(disclaimer, 95)
    for line in disc_lines:
        c.drawCentredString(width/2, y, line)
        y -= 10
    
    c.setFillColor(dark_blue)
    c.rect(0, 0, width, 30, fill=True, stroke=False)
    c.setFillColor(HexColor('#FFFFFF'))
    c.setFont('Helvetica', 8)
    c.drawCentredString(width/2, 12, "AyurAI Veda™ | AI-Powered Ayurvedic Health Assessment")
    
    c.save()
    buffer.seek(0)
    return send_file(buffer, as_attachment=True, download_name=f'AyurAI_Report_{assessment["id"]}.pdf', mimetype='application/pdf')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/analyze', methods=['POST'])
@login_required
def analyze():
    data = request.json
    result = tie.analyze(data)
    
    # Add disease predictions
    user_data = {
        **data,
        'vata_score': result['scores']['vata'],
        'pitta_score': result['scores']['pitta'],
        'kapha_score': result['scores']['kapha']
    }
    disease_prediction = disease_predictor.predict(user_data)
    result['disease_prediction'] = disease_prediction
    
    # Save assessment to database
    auth_db.save_assessment(
        session['user_id'], data, result,
        data.get('patient_name'), data.get('patient_phone')
    )
    
    return jsonify(result)

@app.route('/download-report', methods=['POST'])
def download_report():
    data = request.json
    lang = data.get('language', 'en')
    
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4
    
    # Register Unicode fonts for Hindi/Gujarati
    try:
        font_path = os.path.join(os.path.dirname(__file__), 'fonts')
        if os.path.exists(os.path.join(font_path, 'NotoSansDevanagari-Regular.ttf')):
            pdfmetrics.registerFont(TTFont('Devanagari', os.path.join(font_path, 'NotoSansDevanagari-Regular.ttf')))
            pdfmetrics.registerFont(TTFont('Devanagari-Bold', os.path.join(font_path, 'NotoSansDevanagari-Bold.ttf')))
        if os.path.exists(os.path.join(font_path, 'NotoSansGujarati-Regular.ttf')):
            pdfmetrics.registerFont(TTFont('Gujarati', os.path.join(font_path, 'NotoSansGujarati-Regular.ttf')))
            pdfmetrics.registerFont(TTFont('Gujarati-Bold', os.path.join(font_path, 'NotoSansGujarati-Bold.ttf')))
    except:
        pass
    
    # Select appropriate font
    if lang == 'hi':
        font_regular = 'Devanagari' if 'Devanagari' in pdfmetrics.getRegisteredFontNames() else 'Helvetica'
        font_bold = 'Devanagari-Bold' if 'Devanagari-Bold' in pdfmetrics.getRegisteredFontNames() else 'Helvetica-Bold'
    elif lang == 'gu':
        font_regular = 'Gujarati' if 'Gujarati' in pdfmetrics.getRegisteredFontNames() else 'Helvetica'
        font_bold = 'Gujarati-Bold' if 'Gujarati-Bold' in pdfmetrics.getRegisteredFontNames() else 'Helvetica-Bold'
    else:
        font_regular = 'Helvetica'
        font_bold = 'Helvetica-Bold'
    
    # Colors
    orange = HexColor('#FF9933')
    green = HexColor('#138808')
    dark_blue = HexColor('#1a237e')
    dark_gray = HexColor('#333333')
    light_gray = HexColor('#666666')
    bg_gray = HexColor('#f5f5f5')
    
    # Professional Header
    c.setFillColor(dark_blue)
    c.rect(0, height - 120, width, 120, fill=True, stroke=False)
    
    c.setFillColor(HexColor('#FFFFFF'))
    c.setFont(font_bold, 22)
    title = get_translation(lang, 'report_title')
    c.drawCentredString(width/2, height - 45, title)
    
    c.setFont(font_regular, 9)
    subtitle = get_translation(lang, 'powered_by')
    c.drawCentredString(width/2, height - 65, subtitle)
    
    # Report metadata
    from datetime import datetime
    c.setFont('Helvetica', 9)
    date_label = "Report Date:" if lang == 'en' else "रिपोर्ट तिथि:" if lang == 'hi' else "રિપોર્ટ તારીખ:"
    id_label = "Report ID:" if lang == 'en' else "रिपोर्ट आईडी:" if lang == 'hi' else "રિપોર્ટ ID:"
    
    month_names = {
        'en': datetime.now().strftime('%d %B %Y'),
        'hi': datetime.now().strftime('%d %B %Y'),
        'gu': datetime.now().strftime('%d %B %Y')
    }
    
    c.drawCentredString(width/2, height - 85, f"{date_label} {month_names[lang]}")
    c.drawCentredString(width/2, height - 100, f"{id_label} AV-{datetime.now().strftime('%Y%m%d%H%M%S')}")
    
    y = height - 150
    
    # Section 1: Clinical Summary
    draw_section_header(c, "CLINICAL SUMMARY" if lang == 'en' else "नैदानिक सारांश" if lang == 'hi' else "ક્લિનિકલ સારાંશ", 50, y, width - 100, dark_blue, font_bold)
    y -= 40
    
    # Dominant Dosha box
    c.setFillColor(bg_gray)
    c.roundRect(50, y - 45, width - 100, 50, 5, fill=True, stroke=False)
    c.setFillColor(dark_gray)
    c.setFont(font_bold, 13)
    dom_label = get_translation(lang, 'dominant_dosha')
    c.drawString(70, y - 18, f"{dom_label}:")
    c.setFillColor(orange)
    c.setFont(font_bold, 17)
    c.drawString(250, y - 18, data['dominant'])
    y -= 55
    
    # Risk Assessment
    risk = data['risk']
    risk_color = HexColor('#d32f2f') if risk == 'High' else HexColor('#f57c00') if risk == 'Moderate' else HexColor('#388e3c')
    c.setFillColor(dark_gray)
    c.setFont(font_bold, 11)
    risk_label = get_translation(lang, 'risk_level')
    c.drawString(70, y, f"{risk_label}:")
    c.setFillColor(risk_color)
    c.setFont(font_bold, 13)
    c.drawString(250, y, get_translation(lang, risk.lower()).upper())
    y -= 28
    
    # Description
    c.setFillColor(light_gray)
    c.setFont(font_regular, 9)
    desc = get_translation(lang, f"description.{data['dominant'].lower()}")
    lines = wrap_text(desc, 80 if lang == 'en' else 70)
    for line in lines:
        c.drawString(70, y, line)
        y -= 13
    y -= 20
    
    # Section 2: Dosha Analysis
    draw_section_header(c, "DOSHA ANALYSIS" if lang == 'en' else "दोष विश्लेषण" if lang == 'hi' else "દોષ વિશ્લેષણ", 50, y, width - 100, dark_blue, font_bold)
    y -= 40
    
    # Table header
    c.setFillColor(dark_blue)
    c.rect(50, y - 25, width - 100, 25, fill=True, stroke=False)
    c.setFillColor(HexColor('#FFFFFF'))
    c.setFont(font_bold, 10)
    
    col1 = "Dosha Type" if lang == 'en' else "दोष प्रकार" if lang == 'hi' else "દોષ પ્રકાર"
    col2 = "Score" if lang == 'en' else "स्कोर" if lang == 'hi' else "સ્કોર"
    col3 = "Visual" if lang == 'en' else "दृश्य" if lang == 'hi' else "દ્રશ્ય"
    
    c.drawString(70, y - 15, col1)
    c.drawString(200, y - 15, col2)
    c.drawString(320, y - 15, col3)
    y -= 30
    
    # Table rows
    doshas = [
        ('vata', HexColor('#9C27B0'), get_translation(lang, 'vata')),
        ('pitta', HexColor('#FF5722'), get_translation(lang, 'pitta')),
        ('kapha', HexColor('#4CAF50'), get_translation(lang, 'kapha'))
    ]
    
    for i, (dosha, color, label) in enumerate(doshas):
        score = data['scores'][dosha]
        
        if i % 2 == 0:
            c.setFillColor(bg_gray)
            c.rect(50, y - 32, width - 100, 32, fill=True, stroke=False)
        
        c.setFillColor(dark_gray)
        c.setFont(font_bold, 10)
        c.drawString(70, y - 16, label)
        
        c.setFont('Helvetica', 10)
        c.drawString(200, y - 16, f"{score}%")
        
        c.setStrokeColor(HexColor('#CCCCCC'))
        c.setLineWidth(1)
        c.rect(300, y - 20, 200, 14, fill=False, stroke=True)
        c.setFillColor(color)
        c.rect(300, y - 20, 200 * (score / 100), 14, fill=True, stroke=False)
        
        y -= 37
    
    y -= 20
    
    # Section 3: AI Disease Risk Predictions
    if data.get('disease_prediction'):
        if y < 200:
            c.showPage()
            y = height - 50
        
        draw_section_header(c, "AI DISEASE RISK PREDICTIONS" if lang == 'en' else "एआई रोग जोखिम पूर्वानुमान" if lang == 'hi' else "AI રોગ જોખમ આગાહી", 50, y, width - 100, HexColor('#ff9800'), font_bold)
        y -= 35
        
        disease_pred = data['disease_prediction']
        
        # Diseases list
        c.setFillColor(dark_gray)
        c.setFont(font_bold, 9)
        c.drawString(70, y, "Predicted Health Risks:" if lang == 'en' else "अनुमानित स्वास्थ्य जोखिम:" if lang == 'hi' else "અનુમાનિત આરોગ્ય જોખમો:")
        y -= 18
        
        for disease in disease_pred['diseases'][:5]:
            if y < 130:
                c.showPage()
                y = height - 50
            
            c.setFillColor(HexColor('#ff9800'))
            c.circle(70, y - 3, 3, fill=True, stroke=False)
            c.setFillColor(dark_gray)
            c.setFont(font_regular, 8.5)
            disease_text = disease.replace('(', '- ').replace(')', '')
            c.drawString(85, y, disease_text)
            y -= 15
        
        y -= 10
        
        # Risk factors
        if disease_pred.get('risk_factors'):
            c.setFillColor(dark_gray)
            c.setFont(font_bold, 9)
            c.drawString(70, y, "Risk Factors:" if lang == 'en' else "जोखिम कारक:" if lang == 'hi' else "જોખમ પરિબળો:")
            y -= 18
            
            for risk in disease_pred['risk_factors'][:3]:
                if y < 130:
                    c.showPage()
                    y = height - 50
                
                risk_lines = wrap_text(risk, 75)
                for line in risk_lines:
                    c.setFillColor(light_gray)
                    c.setFont(font_regular, 8)
                    c.drawString(85, y, f"• {line}")
                    y -= 12
        
        y -= 15
    
    # Section 4: Recommendations
    draw_section_header(c, "CLINICAL RECOMMENDATIONS" if lang == 'en' else "नैदानिक सिफारिशें" if lang == 'hi' else "ક્લિનિકલ ભલામણો", 50, y, width - 100, green, font_bold)
    y -= 35
    
    c.setFillColor(dark_gray)
    c.setFont(font_regular, 8.5)
    
    for i, rec in enumerate(data['recommendations'], 1):
        if y < 130:
            c.showPage()
            y = height - 50
        
        rec_lines = wrap_text(rec, 80 if lang == 'en' else 70)
        box_height = len(rec_lines) * 13 + 18
        
        c.setFillColor(bg_gray)
        c.roundRect(50, y - box_height, width - 100, box_height, 3, fill=True, stroke=False)
        
        c.setFillColor(green)
        c.circle(70, y - 13, 10, fill=True, stroke=False)
        c.setFillColor(HexColor('#FFFFFF'))
        c.setFont('Helvetica-Bold', 9)
        c.drawCentredString(70, y - 16, str(i))
        
        c.setFillColor(dark_gray)
        c.setFont(font_regular, 8.5)
        y_text = y - 13
        for line in rec_lines:
            c.drawString(90, y_text, line)
            y_text -= 13
        
        y -= box_height + 10
    
    # Footer
    y = 100
    c.setStrokeColor(dark_blue)
    c.setLineWidth(1)
    c.line(50, y, width - 50, y)
    y -= 15
    
    c.setFillColor(light_gray)
    c.setFont(font_bold, 8)
    disclaimer_title = "IMPORTANT DISCLAIMER" if lang == 'en' else "महत्वपूर्ण अस्वीकरण" if lang == 'hi' else "મહત્વપૂર્ણ અસ્વીકરણ"
    c.drawCentredString(width/2, y, disclaimer_title)
    y -= 13
    
    c.setFont(font_regular, 7)
    disclaimer = get_translation(lang, 'disclaimer')
    disc_lines = wrap_text(disclaimer, 95 if lang == 'en' else 85)
    for line in disc_lines:
        c.drawCentredString(width/2, y, line)
        y -= 10
    
    # Footer bar
    c.setFillColor(dark_blue)
    c.rect(0, 0, width, 30, fill=True, stroke=False)
    c.setFillColor(HexColor('#FFFFFF'))
    c.setFont('Helvetica', 8)
    c.drawCentredString(width/2, 12, "AyurAI Veda™ | AI-Powered Ayurvedic Health Assessment")
    
    c.save()
    buffer.seek(0)
    return send_file(buffer, as_attachment=True, download_name=f'AyurAI_Veda_Report_{lang}.pdf', mimetype='application/pdf')

def draw_section_header(c, title, x, y, width, color, font):
    """Draw professional section header"""
    c.setFillColor(color)
    c.rect(x, y - 22, width, 22, fill=True, stroke=False)
    c.setFillColor(HexColor('#FFFFFF'))
    c.setFont(font, 11)
    c.drawString(x + 10, y - 14, title)

def wrap_text(text, max_chars):
    """Wrap text to fit within max_chars per line"""
    words = text.split()
    lines = []
    current_line = []
    current_length = 0
    
    for word in words:
        if current_length + len(word) + 1 <= max_chars:
            current_line.append(word)
            current_length += len(word) + 1
        else:
            if current_line:
                lines.append(' '.join(current_line))
            current_line = [word]
            current_length = len(word)
    
    if current_line:
        lines.append(' '.join(current_line))
    
    return lines

@app.route('/rag-chatbot')
def rag_chatbot():
    return render_template('rag_chatbot.html')

@app.route('/rag-chat', methods=['POST'])
def rag_chat():
    try:
        data = request.json
        query = data.get('message', '')
        mode = data.get('mode', 'modern')
        
        from rag_retriever import AyurvedaRAGRetriever
        from llm_generator import AyurvedaLLM
        
        retriever = AyurvedaRAGRetriever()
        llm = AyurvedaLLM()
        
        result = llm.chat(query, retriever, mode=mode, top_k=5)
        
        return jsonify({
            'response': result['answer'],
            'citations': result['citations'],
            'mode': result['mode']
        })
    except Exception as e:
        return jsonify({
            'response': f'Error: {str(e)}',
            'citations': [],
            'mode': mode
        })

@app.route('/chat', methods=['POST'])
def chat():
    try:
        data = request.json
        message = data.get('message', '')
        
        if not message:
            return jsonify({'response': 'Please enter a message.'})
        
        # Try ML chatbot first
        try:
            from ml_chatbot import AyurvedaMLChatbot
            ml_bot = AyurvedaMLChatbot()
            
            if ml_bot.load_model():
                response = ml_bot.get_response(message)
                response = refine_text(response)
                return jsonify({'response': response})
        except:
            pass
        
        # Fallback to simple knowledge base
        from simple_pdf_reader import SimplePDFKnowledge
        kb = SimplePDFKnowledge()
        response = kb.get_answer(message)
        response = refine_text(response)
        
        return jsonify({'response': response})
    except Exception as e:
        print(f"Chat error: {str(e)}")
        return jsonify({'response': get_fallback_response(message)})

def refine_text(text):
    """Refine text with proper formatting: points, paragraphs, headings"""
    # Remove chapter/section references
    text = re.sub(r'Chapter\s+\d+[:\s-]*', '', text, flags=re.IGNORECASE)
    text = re.sub(r'Section\s+\d+[:\s-]*', '', text, flags=re.IGNORECASE)
    text = re.sub(r'According to Ashtanga Hridaya[:\s-]*', '', text, flags=re.IGNORECASE)
    text = re.sub(r'Ashtanga Hridaya Sutrasthana[^:]*:', '', text, flags=re.IGNORECASE)
    text = re.sub(r'\*\*Chapter.*?:\*\*', '', text)
    text = re.sub(r'Page\s+\d+', '', text, flags=re.IGNORECASE)
    text = re.sub(r'\(see.*?\)', '', text, flags=re.IGNORECASE)
    text = re.sub(r'\[.*?\]', '', text)
    
    # If already formatted with HTML, return as is
    if '<strong>' in text or '<br>' in text:
        return text
    
    # Split into sections
    lines = text.split('\n')
    formatted_lines = []
    current_section = []
    
    for line in lines:
        line = line.strip()
        if not line:
            continue
            
        # Detect headings (lines ending with :)
        if line.endswith(':') and len(line) < 60:
            if current_section:
                formatted_lines.append(' '.join(current_section))
                current_section = []
            formatted_lines.append(f'<br><br><strong>{line}</strong><br>')
        
        # Detect bullet points
        elif line.startswith(('-', '•', '*')) or re.match(r'^\d+\.', line):
            if current_section:
                formatted_lines.append(' '.join(current_section))
                current_section = []
            clean_line = re.sub(r'^[-•*]\s*', '', line)
            clean_line = re.sub(r'^\d+\.\s*', '', clean_line)
            formatted_lines.append(f'• {clean_line}<br>')
        
        # Regular text
        else:
            current_section.append(line)
    
    # Add remaining section
    if current_section:
        formatted_lines.append(' '.join(current_section))
    
    # Join and create paragraphs
    result = ''.join(formatted_lines)
    
    # Add paragraph breaks for better readability
    result = re.sub(r'\. ([A-Z])', r'. <br><br>\1', result)
    
    # Clean up extra whitespace
    result = re.sub(r'<br>\s*<br>\s*<br>+', '<br><br>', result)
    result = re.sub(r'\s+', ' ', result)
    result = result.strip()
    
    # Limit length for brief responses
    if len(result) > 1200:
        result = result[:1200].rsplit('<br>', 1)[0] + '...'
    
    return result

@app.route('/chat/history', methods=['GET'])
def get_chat_history():
    try:
        if 'chat_session_id' not in session:
            return jsonify({'history': []})
        
        session_id = session['chat_session_id']
        history = db.get_conversation_history(session_id, limit=50)
        return jsonify({'history': history})
    except Exception as e:
        print(f"History error: {str(e)}")
        return jsonify({'history': []})

@app.route('/chat/new-session', methods=['POST'])
def new_chat_session():
    try:
        session_id = db.create_session()
        session['chat_session_id'] = session_id
        return jsonify({'session_id': session_id, 'message': 'New chat session created'})
    except Exception as e:
        print(f"New session error: {str(e)}")
        return jsonify({'error': str(e)})

def get_fallback_response(message):
    """Fallback responses when Groq is unavailable"""
    message_lower = message.lower()
    
    if 'tridosha' in message_lower or 'tri dosha' in message_lower or 'three dosha' in message_lower:
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
    
    elif 'vata' in message_lower:
        return "Vata dosha (Air + Space) governs movement, creativity, and the nervous system. Imbalance causes anxiety, dry skin, and constipation. Balance with warm foods, regular routines, and oil massage."
    
    elif 'pitta' in message_lower:
        return "Pitta dosha (Fire + Water) governs metabolism, digestion, and transformation. Imbalance causes acidity, inflammation, and anger. Balance with cooling foods, meditation, and avoiding spicy items."
    
    elif 'kapha' in message_lower:
        return "Kapha dosha (Water + Earth) governs structure, stability, and immunity. Imbalance causes weight gain, lethargy, and congestion. Balance with light foods, regular exercise, and avoiding dairy."
    
    elif 'digestion' in message_lower or 'agni' in message_lower or 'digest' in message_lower:
        return "To improve digestion (Agni): Eat at regular times, use digestive spices (ginger, cumin, fennel), avoid overeating, drink warm water, and walk after meals. Strong Agni is key to health in Ayurveda."
    
    elif 'diet' in message_lower or 'food' in message_lower or 'eat' in message_lower:
        return "Ayurvedic diet principles: Eat according to your dosha, consume fresh cooked meals, avoid incompatible food combinations, eat your largest meal at midday, and maintain regular meal times."
    
    elif 'yoga' in message_lower or 'exercise' in message_lower:
        return "Ayurvedic yoga: Vata types benefit from gentle grounding poses, Pitta types from cooling poses, and Kapha types from energizing poses. Practice should balance your dominant dosha."
    
    elif 'stress' in message_lower or 'anxiety' in message_lower or 'tension' in message_lower or 'worry' in message_lower:
        return "Ayurvedic stress management: Regular routine, adequate sleep, meditation, pranayama (breathing exercises), Abhyanga (oil massage), and adaptogenic herbs like Ashwagandha. Stress is seen as Vata imbalance affecting the mind."
    
    elif 'sleep' in message_lower or 'insomnia' in message_lower:
        return "Ayurvedic sleep tips: Sleep 10 PM - 6 AM, establish regular bedtime, practice oil massage, drink warm milk with nutmeg, avoid screens before bed, and keep bedroom cool and dark."
    
    elif 'invent' in message_lower or 'origin' in message_lower or 'history' in message_lower or 'start' in message_lower or 'founder' in message_lower:
        return "Ayurveda wasn't invented by one person - it evolved over 5000+ years in ancient India. The knowledge was passed down orally by sages (Rishis) and later compiled in classical texts like Charaka Samhita, Sushruta Samhita, and Ashtanga Hridaya."
    
    elif 'pranayama' in message_lower or 'breathing' in message_lower or 'breath' in message_lower:
        return "Pranayama (breath control) balances doshas and calms the mind. Key practices: Anulom Vilom (alternate nostril) for balance, Sheetali (cooling breath) for Pitta, Kapalabhati (skull shining) for Kapha, and Bhramari (bee breath) for stress."
    
    elif 'herb' in message_lower or 'ashwagandha' in message_lower or 'turmeric' in message_lower or 'tulsi' in message_lower:
        return "Key Ayurvedic herbs: Ashwagandha (stress relief, strength), Turmeric (anti-inflammatory), Tulsi (immunity, stress), Amla (Vitamin C, rejuvenation), Brahmi (memory, clarity), and Neem (blood purification)."
    
    elif 'dosha' in message_lower:
        return """Doshas are three fundamental energies in Ayurveda:<br><br>
🌬️ <strong>Vata</strong> (Air+Space) - Governs movement, creativity, nervous system<br>
🔥 <strong>Pitta</strong> (Fire+Water) - Governs metabolism, digestion, transformation<br>
🌊 <strong>Kapha</strong> (Water+Earth) - Governs structure, stability, immunity<br><br>
Everyone has a unique combination of these doshas. Take our AI Health Assessment to discover yours!"""
    
    elif 'ayurveda' in message_lower or 'what is' in message_lower:
        return "Ayurveda is a 5000-year-old holistic healing system from India. It focuses on balance between body, mind, and spirit through the three doshas: Vata, Pitta, and Kapha. Visit the 'About Ayurveda' page to learn more!"
    
    else:
        return """Hello! I'm AyurVaani™, your Ayurvedic wellness assistant. I can help you with:<br><br>
🌬️ Understanding Vata, Pitta, and Kapha doshas<br>
🍽️ Personalized diet recommendations<br>
🌿 Herbal remedies and natural treatments<br>
🧘 Yoga and pranayama practices<br>
😌 Stress management and sleep improvement<br>
🔥 Digestive health and Agni strengthening<br>
🌞 Seasonal routines (Ritucharya)<br>
📚 Ayurveda history and classical texts<br>
🧬 Prakriti (constitution) understanding<br>
💆 Panchakarma detoxification<br>
⏰ Daily routines (Dinacharya)<br><br>
What would you like to know about Ayurveda today?"""

if __name__ == '__main__':
    app.run(debug=True)

# Vercel serverless function handler
app = app
