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

@app.route('/download-report', methods=['POST'])
def download_report():
    try:
        from reportlab.lib.pagesizes import letter
        from reportlab.lib import colors
        from reportlab.lib.units import inch
        from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
        from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
        from reportlab.lib.enums import TA_CENTER, TA_LEFT
        
        data = request.json
        
        # Create PDF in memory
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(
            buffer,
            pagesize=letter,
            rightMargin=72,
            leftMargin=72,
            topMargin=72,
            bottomMargin=18
        )
        
        # Container for PDF elements
        elements = []
        styles = getSampleStyleSheet()
        
        # Custom styles
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=20,
            textColor=colors.HexColor('#FF9933'),
            spaceAfter=6,
            alignment=TA_CENTER,
            fontName='Helvetica-Bold'
        )
        
        subtitle_style = ParagraphStyle(
            'Subtitle',
            parent=styles['Normal'],
            fontSize=14,
            textColor=colors.HexColor('#1a237e'),
            spaceAfter=20,
            alignment=TA_CENTER,
            fontName='Helvetica'
        )
        
        heading_style = ParagraphStyle(
            'CustomHeading',
            parent=styles['Heading2'],
            fontSize=14,
            textColor=colors.HexColor('#1a237e'),
            spaceAfter=10,
            spaceBefore=15,
            fontName='Helvetica-Bold'
        )
        
        body_style = ParagraphStyle(
            'CustomBody',
            parent=styles['Normal'],
            fontSize=10,
            spaceAfter=6,
            fontName='Helvetica'
        )
        
        # Title
        elements.append(Paragraph("AyurAI Veda", title_style))
        elements.append(Paragraph("Clinical Assessment Report", subtitle_style))
        elements.append(Spacer(1, 0.2*inch))
        
        # Results Summary
        elements.append(Paragraph("Assessment Results", heading_style))
        
        summary_data = [
            ['Dominant Dosha:', str(data.get('dominant', 'N/A'))],
            ['Dosha State:', str(data.get('dosha_state', 'N/A'))],
            ['Agni State:', str(data.get('agni_state', 'N/A'))],
            ['Ama Status:', str(data.get('ama_status', 'N/A'))],
            ['Risk Level:', str(data.get('risk', 'N/A'))]
        ]
        
        summary_table = Table(summary_data, colWidths=[2*inch, 4*inch])
        summary_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#f5f5f5')),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTNAME', (1, 0), (1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
            ('TOPPADDING', (0, 0), (-1, -1), 8),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey)
        ]))
        elements.append(summary_table)
        elements.append(Spacer(1, 0.2*inch))
        
        # Dosha Distribution
        elements.append(Paragraph("Dosha Distribution", heading_style))
        scores = data.get('scores', {})
        dosha_data = [
            ['Dosha', 'Percentage'],
            ['Vata', str(scores.get('vata', 0)) + '%'],
            ['Pitta', str(scores.get('pitta', 0)) + '%'],
            ['Kapha', str(scores.get('kapha', 0)) + '%']
        ]
        
        dosha_table = Table(dosha_data, colWidths=[3*inch, 3*inch])
        dosha_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1a237e')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
            ('TOPPADDING', (0, 0), (-1, -1), 8),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f9f9f9')])
        ]))
        elements.append(dosha_table)
        elements.append(Spacer(1, 0.2*inch))
        
        # Clinical Justification
        if data.get('justification'):
            elements.append(Paragraph("Clinical Justification", heading_style))
            justification_text = str(data['justification']).replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
            elements.append(Paragraph(justification_text, body_style))
            elements.append(Spacer(1, 0.15*inch))
        
        # Recommendations
        elements.append(Paragraph("Personalized Recommendations", heading_style))
        recommendations = data.get('recommendations', [])
        for i, rec in enumerate(recommendations[:8], 1):  # Limit to 8 recommendations
            rec_text = str(rec).replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
            elements.append(Paragraph(f"{i}. {rec_text}", body_style))
            elements.append(Spacer(1, 0.05*inch))
        
        elements.append(Spacer(1, 0.2*inch))
        
        # Disclaimer
        disclaimer_style = ParagraphStyle(
            'Disclaimer',
            parent=styles['Normal'],
            fontSize=8,
            textColor=colors.HexColor('#d32f2f'),
            leftIndent=10,
            rightIndent=10,
            fontName='Helvetica'
        )
        elements.append(Paragraph(
            "<b>Important Disclaimer:</b> This report provides educational and preventive health insights only. "
            "It is NOT a medical diagnosis. Always consult qualified healthcare professionals for medical advice.",
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
        elements.append(Paragraph("AyurAI Veda | Ancient Wisdom. Intelligent Health.", footer_style))
        timestamp = datetime.now().strftime('%d %B %Y at %I:%M %p')
        elements.append(Paragraph(f"Report generated on {timestamp}", footer_style))
        
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
