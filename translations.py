# Multilingual Translation System for AyurAI Veda

TRANSLATIONS = {
    'en': {
        'report_title': 'AyurAI Veda Health Report',
        'powered_by': 'Powered by Tridosha Intelligence Engine',
        'dominant_dosha': 'Dominant Dosha',
        'risk_level': 'Risk Level',
        'dosha_scores': 'Dosha Scores',
        'vata': 'Vata',
        'pitta': 'Pitta',
        'kapha': 'Kapha',
        'recommendations': 'Personalized Recommendations',
        'disclaimer': 'This is for educational purposes only. Not a medical diagnosis. Consult qualified healthcare professionals for medical advice.',
        'high': 'High',
        'moderate': 'Moderate',
        'low': 'Low',
        'description': {
            'vata': 'Vata governs movement, creativity, and nervous system. Imbalance causes anxiety, dryness, and irregular patterns.',
            'pitta': 'Pitta governs metabolism, digestion, and transformation. Imbalance causes heat, inflammation, and anger.',
            'kapha': 'Kapha governs structure, stability, and lubrication. Imbalance causes weight gain, lethargy, and congestion.'
        }
    },
    'hi': {
        'report_title': 'आयुरएआई वेद स्वास्थ्य रिपोर्ट',
        'powered_by': 'त्रिदोष इंटेलिजेंस इंजन द्वारा संचालित',
        'dominant_dosha': 'प्रमुख दोष',
        'risk_level': 'जोखिम स्तर',
        'dosha_scores': 'दोष स्कोर',
        'vata': 'वात',
        'pitta': 'पित्त',
        'kapha': 'कफ',
        'recommendations': 'व्यक्तिगत सिफारिशें',
        'disclaimer': 'यह केवल शैक्षिक उद्देश्यों के लिए है। यह चिकित्सा निदान नहीं है। चिकित्सा सलाह के लिए योग्य स्वास्थ्य पेशेवरों से परामर्श लें।',
        'high': 'उच्च',
        'moderate': 'मध्यम',
        'low': 'निम्न',
        'description': {
            'vata': 'वात गति, रचनात्मकता और तंत्रिका तंत्र को नियंत्रित करता है। असंतुलन से चिंता, शुष्कता और अनियमित पैटर्न होते हैं।',
            'pitta': 'पित्त चयापचय, पाचन और परिवर्तन को नियंत्रित करता है। असंतुलन से गर्मी, सूजन और क्रोध होता है।',
            'kapha': 'कफ संरचना, स्थिरता और स्नेहन को नियंत्रित करता है। असंतुलन से वजन बढ़ना, सुस्ती और जमाव होता है।'
        }
    },
    'gu': {
        'report_title': 'આયુરએઆઈ વેદ આરોગ્ય અહેવાલ',
        'powered_by': 'ત્રિદોષ ઇન્ટેલિજન્સ એન્જિન દ્વારા સંચાલિત',
        'dominant_dosha': 'પ્રબળ દોષ',
        'risk_level': 'જોખમ સ્તર',
        'dosha_scores': 'દોષ સ્કોર',
        'vata': 'વાત',
        'pitta': 'પિત્ત',
        'kapha': 'કફ',
        'recommendations': 'વ્યક્તિગત ભલામણો',
        'disclaimer': 'આ ફક્ત શૈક્ષણિક હેતુઓ માટે છે। તબીબી નિદાન નથી। તબીબી સલાહ માટે લાયક આરોગ્ય વ્યાવસાયિકોની સલાહ લો।',
        'high': 'ઉચ્ચ',
        'moderate': 'મધ્યમ',
        'low': 'નીચું',
        'description': {
            'vata': 'વાત હલનચલન, સર્જનાત્મકતા અને ચેતાતંત્રને નિયંત્રિત કરે છે। અસંતુલન ચિંતા, શુષ્કતા અને અનિયમિત પેટર્ન તરફ દોરી જાય છે।',
            'pitta': 'પિત્ત ચયાપચય, પાચન અને પરિવર્તનને નિયંત્રિત કરે છે। અસંતુલન ગરમી, બળતરા અને ગુસ્સો તરફ દોરી જાય છે।',
            'kapha': 'કફ રચના, સ્થિરતા અને લુબ્રિકેશનને નિયંત્રિત કરે છે। અસંતુલન વજન વધારો, સુસ્તી અને ભીડ તરફ દોરી જાય છે।'
        }
    }
}

def get_translation(lang, key):
    """Get translation for a specific key"""
    if lang not in TRANSLATIONS:
        lang = 'en'
    
    keys = key.split('.')
    value = TRANSLATIONS[lang]
    
    for k in keys:
        if isinstance(value, dict):
            value = value.get(k, key)
        else:
            return key
    
    return value
