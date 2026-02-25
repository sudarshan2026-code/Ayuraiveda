# AyurAI Veda™
## Ancient Wisdom. Intelligent Health.

![NEP 2020 Aligned](https://img.shields.io/badge/NEP%202020-Aligned-green)
![IKS + AI](https://img.shields.io/badge/IKS-AI%20Powered-orange)
![Python](https://img.shields.io/badge/Python-3.8+-blue)

---

## 🎯 Project Overview

**AyurAI Veda™** is an AI-powered health prediction web application based on Indian Knowledge Systems (IKS), specifically Ayurveda. The system uses the **Tridosha Intelligence Engine™** to analyze health patterns and provide personalized preventive lifestyle guidance.

### Purpose
- Educational and preventive health insights
- Integration of traditional Ayurvedic wisdom with modern AI
- NEP 2020 compliant interdisciplinary learning platform

### Target Users
- Students learning about IKS and AI
- Researchers in traditional medicine
- General users interested in preventive healthcare

---

## ⚠️ Important Disclaimer

**This system provides educational and preventive insights only. It is NOT a medical diagnosis platform.**

Always consult qualified healthcare professionals for medical advice.

---

## 🧠 Tridosha Intelligence Engine™

The core AI engine analyzes user inputs based on Ayurvedic principles:

- **Vata** (Air + Space): Governs movement, creativity, nervous system
- **Pitta** (Fire + Water): Governs metabolism, digestion, transformation
- **Kapha** (Water + Earth): Governs structure, stability, immunity

### AI Logic
- Rule-based expert system
- Weighted scoring algorithm
- Pattern recognition in symptoms
- Personalized recommendations
- ML-ready architecture for future expansion

---

## ✨ Key Features

✅ AI-powered Tridosha analysis  
✅ AyurVaani™ AI Chatbot (Groq LLM powered)  
✅ Interactive health assessment form  
✅ Visual dosha meters and risk levels  
✅ Personalized diet, yoga, and lifestyle recommendations  
✅ Downloadable PDF reports  
✅ Educational content on Ayurveda and IKS  
✅ NEP 2020 alignment documentation  
✅ Responsive, mobile-friendly design  
✅ No data storage - privacy-focused  
✅ Offline compatible  

---

## 🛠️ Technology Stack

- **Backend**: Python Flask
- **Frontend**: HTML5, CSS3, JavaScript
- **AI Engine**: Custom Python logic module
- **PDF Generation**: ReportLab
- **Design**: Indian cultural aesthetics (Saffron/Green/White theme)

---

## 📁 Project Structure

```
Ayurveda/
├── app.py                      # Flask backend with routes
├── ai_engine.py                # Tridosha Intelligence Engine™
├── templates/
│   ├── index.html              # Homepage
│   ├── about.html              # About Ayurveda & Tridosha
│   ├── assessment.html         # AI Health Assessment form
│   ├── nep.html                # NEP 2020 & IKS alignment
│   └── contact.html            # Contact & Credits
├── static/
│   ├── css/
│   │   └── style.css           # Main stylesheet
│   └── js/
│       └── assessment.js       # Frontend logic
├── requirements.txt            # Python dependencies
└── README.md                   # This file
```

---

## 🚀 Installation & Setup

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)
- Groq API key (for enhanced chatbot responses)

### Step 1: Clone or Download
```bash
cd Ayurveda
```

### Step 2: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 3: Configure Groq API (Optional but Recommended)
For enhanced AyurVaani™ chatbot responses:

**Windows:**
```cmd
set GROQ_API_KEY=your_api_key_here
```

**Linux/Mac:**
```bash
export GROQ_API_KEY=your_api_key_here
```

See [GROQ_SETUP.md](GROQ_SETUP.md) for detailed instructions.

**Note:** AyurVaani™ works without Groq (fallback mode) but responses are shorter.

### Step 4: Run the Application
```bash
python app.py
```

### Step 5: Access the Application
Open your browser and navigate to:
```
http://127.0.0.1:5000
```

---

## 📦 Dependencies

```
Flask==3.0.0
reportlab==4.0.7
groq==0.4.1
```

Install all at once:
```bash
pip install Flask reportlab groq
```

**Note:** Groq is optional. AyurVaani™ chatbot works without it (fallback mode).

---

## 🎨 Features Walkthrough

### 1. Homepage
- Project introduction
- Tridosha Intelligence Engine™ branding
- How it works explanation
- Key features overview

### 2. About Ayurveda
- Ayurveda fundamentals
- Detailed Tridosha theory
- Scientific validation
- AI enhancement explanation

### 3. AyurVaani™ AI Chatbot
- Conversational Ayurveda assistant
- Powered by Tridosha Intelligence Engine™ + Groq LLM
- Comprehensive knowledge base
- Natural language responses
- Educational and preventive guidance

### 4. AI Health Assessment
- Interactive 9-question form
- Real-time AI analysis
- Visual dosha meters
- Risk level indicators
- Personalized recommendations
- PDF report download

### 4. NEP 2020 & IKS
- Educational policy alignment
- Interdisciplinary learning
- Future scope
- Ethical AI principles

### 5. Contact & Credits
- Project information
- Technology credits
- Privacy policy
- Medical disclaimer

---

## 🧪 How to Use

1. Navigate to **AI Health Assessment**
2. Fill out the health questionnaire honestly
3. Click **"Analyze with Tridosha Intelligence Engine™"**
4. View your results:
   - Dominant dosha
   - Risk level
   - Dosha percentage scores
   - Personalized recommendations
5. Download PDF report (optional)
6. Take new assessment anytime

---

## 🔬 AI Engine Logic

The Tridosha Intelligence Engine™ uses weighted scoring:

```python
# Example logic flow
if sleep == 'poor': vata_score += 3
if digestion == 'acidity': pitta_score += 4
if skin == 'oily': kapha_score += 3

# Calculate percentages
total = vata + pitta + kapha
vata_percent = (vata / total) * 100

# Determine risk level
if dominant_score >= 50: risk = 'High'
elif dominant_score >= 35: risk = 'Moderate'
else: risk = 'Low'
```

---

## 🎓 Educational Value

### For Students
- Learn AI application in traditional sciences
- Understand Ayurvedic principles scientifically
- Develop interdisciplinary thinking

### For Researchers
- Framework for digitizing traditional knowledge
- ML-ready architecture
- Bridge between traditional and modern medicine

### For Institutions
- Practical NEP 2020 implementation
- IKS integration in STEM curriculum
- Student project inspiration

---

## 🚀 Future Scope

- **Machine Learning**: Train models on clinical data
- **IoT Integration**: Connect wearable health devices
- **Mobile App**: iOS/Android applications
- **Multilingual**: Regional language support
- **Telemedicine**: Remote consultations
- **Research Database**: Contribute to IKS repositories

---

## 🔒 Privacy & Security

- ✅ No data storage
- ✅ Session-based processing
- ✅ No user tracking
- ✅ No third-party sharing
- ✅ Local deployment option
- ✅ Open-source transparency

---

## 📚 References

- Charaka Samhita (Ancient Ayurvedic text)
- Sushruta Samhita (Surgical principles)
- Ashtanga Hridaya (Comprehensive Ayurveda)
- NEP 2020 guidelines on IKS integration
- Modern research on Ayurvedic validation

---

## 🏆 Competition Ready

This project is designed for:
- National-level university competitions
- IKS + Technology hackathons
- NEP 2020 innovation challenges
- Interdisciplinary project showcases

### Presentation Points
✅ Clear problem statement (preventive healthcare)  
✅ Innovative solution (AI + Ayurveda)  
✅ Technical implementation (working prototype)  
✅ Educational alignment (NEP 2020)  
✅ Future scalability (ML, IoT ready)  
✅ Social impact (accessible health insights)  

---

## 🤝 Contributing

Areas for contribution:
- ML model development
- Clinical validation
- Mobile app development
- Multilingual interface
- IoT integration
- Research papers

---

## 📄 License

This project is for educational purposes. Please respect traditional knowledge and use ethically.

---

## 🙏 Acknowledgments

- Ancient Ayurvedic scholars and practitioners
- NEP 2020 initiative for promoting IKS
- Open-source community
- Researchers bridging traditional and modern medicine

---

## 📞 Support

For questions or feedback, refer to the Contact page in the application.

---

**AyurAI Veda™** | Reviving Indian Knowledge Systems through Artificial Intelligence

Powered by **Tridosha Intelligence Engine™** | NEP 2020 Aligned

---

## 🎯 Quick Start Commands

```bash
# Install dependencies
pip install Flask reportlab

# Run application
python app.py

# Access in browser
http://127.0.0.1:5000
```

**That's it! Your AI-powered Ayurvedic health system is ready to use.**
