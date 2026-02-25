# 🚀 AyurAI Veda™ - Quick Start Guide

## Upgraded with AyurVaani™ + Groq LLM

---

## 📋 Installation Steps

### 1. Install Dependencies
```bash
pip install Flask reportlab groq
```

### 2. Set Groq API Key (Optional but Recommended)

**Windows (Command Prompt):**
```cmd
set GROQ_API_KEY=your_groq_api_key_here
python app.py
```

**Windows (PowerShell):**
```powershell
$env:GROQ_API_KEY="your_groq_api_key_here"
python app.py
```

**Linux/Mac:**
```bash
export GROQ_API_KEY=your_groq_api_key_here
python app.py
```

### 3. Run Application
```bash
python app.py
```

### 4. Open Browser
```
http://127.0.0.1:5000
```

---

## 🔑 Get Groq API Key

1. Visit: https://console.groq.com
2. Sign up (free)
3. Go to API Keys
4. Create new key
5. Copy key (starts with `gsk_`)

---

## ✨ Features

### 1. Tridosha Health Assessment
- AI-powered dosha analysis
- Personalized recommendations
- PDF reports

### 2. AyurVaani™ AI Chatbot
- **Without Groq:** Basic knowledge base responses
- **With Groq:** Enhanced, natural language explanations
- Topics: Doshas, diet, yoga, pranayama, lifestyle

### 3. Educational Content
- About Ayurveda
- Tridosha theory
- IKS integration

---

## 🎯 Using AyurVaani™ Chatbot

Navigate to: http://127.0.0.1:5000/chatbot

**Example Questions:**
- "What is Vata dosha?"
- "How to improve digestion?"
- "Best yoga for stress?"
- "Foods for summer season?"
- "What is Ayurvedic daily routine?"

---

## 🔄 Fallback Mode

If Groq API key is NOT set:
- ✅ Chatbot still works
- ✅ Uses local knowledge base
- ⚠️ Shorter responses
- ⚠️ Less natural language

---

## 🔒 Security

- API key loaded from environment variable
- Never hardcoded in source code
- Secure by design

---

## 📊 System Architecture

```
User Query
    ↓
Intent Detection (Local NLP)
    ↓
Ayurveda Knowledge Base (Validated)
    ↓
Tridosha Rules Validation
    ↓
Groq LLM Expansion (if available)
    ↓
Enhanced Response
```

---

## 🆘 Troubleshooting

**Chatbot gives short responses:**
- Groq API key not set
- Set environment variable and restart

**"Groq initialization warning":**
- Invalid API key
- Check key on Groq console

**Import error for groq:**
```bash
pip install groq
```

---

## 📁 Project Structure

```
Ayurveda/
├── app.py                    # Flask backend
├── ai_engine.py              # Tridosha assessment
├── ayurvaani_engine.py       # Chatbot logic
├── groq_client.py            # Groq LLM integration
├── templates/
│   ├── chatbot.html          # Chat interface
│   └── ...
└── requirements.txt
```

---

## ✅ Verify Setup

```python
import os
print("Groq:", "✓" if os.environ.get('GROQ_API_KEY') else "✗")
```

---

**AyurVaani™** | Ancient Ayurveda, Explained with Modern Intelligence
