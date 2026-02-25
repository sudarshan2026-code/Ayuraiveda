# SYSTEM ARCHITECTURE & FLOW DIAGRAMS

## AyurAI Veda™ - Technical Visualization

---

## 1. SYSTEM ARCHITECTURE

```
┌─────────────────────────────────────────────────────────────────┐
│                         USER LAYER                              │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐       │
│  │ Desktop  │  │  Tablet  │  │  Mobile  │  │  Laptop  │       │
│  └────┬─────┘  └────┬─────┘  └────┬─────┘  └────┬─────┘       │
│       └─────────────┴──────────────┴─────────────┘             │
│                          │                                      │
│                    Web Browser                                  │
└──────────────────────────┬──────────────────────────────────────┘
                           │
                           │ HTTP/HTTPS
                           ▼
┌─────────────────────────────────────────────────────────────────┐
│                    PRESENTATION LAYER                           │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │              HTML5 Templates                             │  │
│  │  • index.html (Homepage)                                 │  │
│  │  • assessment.html (Main Feature)                        │  │
│  │  • about.html (Education)                                │  │
│  │  • nep.html (Policy Alignment)                           │  │
│  │  • contact.html (Information)                            │  │
│  └──────────────────────────────────────────────────────────┘  │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │              CSS3 Styling                                │  │
│  │  • style.css (Indian aesthetics theme)                   │  │
│  │  • Responsive design (mobile-first)                      │  │
│  │  • Gradient effects, animations                          │  │
│  └──────────────────────────────────────────────────────────┘  │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │              JavaScript                                  │  │
│  │  • assessment.js (Form handling, API calls)              │  │
│  │  • Dynamic result rendering                              │  │
│  │  • PDF download trigger                                  │  │
│  └──────────────────────────────────────────────────────────┘  │
└──────────────────────────┬──────────────────────────────────────┘
                           │
                           │ AJAX/Fetch API
                           ▼
┌─────────────────────────────────────────────────────────────────┐
│                    APPLICATION LAYER                            │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │              Flask Backend (app.py)                      │  │
│  │                                                          │  │
│  │  Routes:                                                 │  │
│  │  • GET  /           → Homepage                           │  │
│  │  • GET  /about      → Ayurveda info                      │  │
│  │  • GET  /assessment → Assessment form                    │  │
│  │  • POST /analyze    → AI analysis endpoint               │  │
│  │  • POST /download   → PDF generation                     │  │
│  │  • GET  /nep        → NEP 2020 page                      │  │
│  │  • GET  /contact    → Contact page                       │  │
│  │                                                          │  │
│  │  Functions:                                              │  │
│  │  • Request handling                                      │  │
│  │  • JSON serialization                                    │  │
│  │  • PDF generation (ReportLab)                            │  │
│  │  • Template rendering                                    │  │
│  └──────────────────────────────────────────────────────────┘  │
└──────────────────────────┬──────────────────────────────────────┘
                           │
                           │ Function Call
                           ▼
┌─────────────────────────────────────────────────────────────────┐
│                    INTELLIGENCE LAYER                           │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │      Tridosha Intelligence Engine™ (ai_engine.py)        │  │
│  │                                                          │  │
│  │  Class: TridoshaIntelligenceEngine                      │  │
│  │                                                          │  │
│  │  Methods:                                                │  │
│  │  • analyze(user_data)                                    │  │
│  │  • _calculate_dosha_scores(data)                         │  │
│  │  • _calculate_risk(score)                                │  │
│  │  • _get_recommendations(dosha, data)                     │  │
│  │  • _get_dosha_description(dosha)                         │  │
│  │                                                          │  │
│  │  Logic:                                                  │  │
│  │  • Rule-based expert system                              │  │
│  │  • Weighted scoring algorithm                            │  │
│  │  • Pattern recognition                                   │  │
│  │  • Recommendation engine                                 │  │
│  └──────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
```

---

## 2. DATA FLOW DIAGRAM

```
┌─────────────┐
│    USER     │
│  (Browser)  │
└──────┬──────┘
       │
       │ 1. Fills assessment form
       │    (9 health parameters)
       ▼
┌─────────────────────┐
│  assessment.html    │
│  (Frontend Form)    │
└──────┬──────────────┘
       │
       │ 2. Submit button clicked
       │    JavaScript captures data
       ▼
┌─────────────────────┐
│  assessment.js      │
│  (Form Handler)     │
└──────┬──────────────┘
       │
       │ 3. POST request to /analyze
       │    JSON payload: {age, gender, sleep, ...}
       ▼
┌─────────────────────┐
│    Flask Route      │
│  @app.route         │
│  ('/analyze')       │
└──────┬──────────────┘
       │
       │ 4. Calls AI engine
       │    tie.analyze(data)
       ▼
┌─────────────────────────────────────────┐
│  Tridosha Intelligence Engine™          │
│                                         │
│  Step 1: Reset scores                   │
│  Step 2: Analyze each parameter         │
│          • Sleep → affects Vata/Kapha   │
│          • Stress → affects Vata/Pitta  │
│          • Digestion → all doshas       │
│          • Skin → specific dosha        │
│          • Temperature → Vata/Pitta     │
│          • Food → all doshas            │
│          • Age → life stage factor      │
│  Step 3: Calculate percentages          │
│  Step 4: Determine dominant dosha       │
│  Step 5: Calculate risk level           │
│  Step 6: Generate recommendations       │
└──────┬──────────────────────────────────┘
       │
       │ 5. Returns result object
       │    {scores, dominant, risk, recommendations}
       ▼
┌─────────────────────┐
│    Flask Route      │
│  (JSON Response)    │
└──────┬──────────────┘
       │
       │ 6. JSON response sent to frontend
       ▼
┌─────────────────────┐
│  assessment.js      │
│  (Result Handler)   │
└──────┬──────────────┘
       │
       │ 7. Renders results dynamically
       │    • Updates dosha meters
       │    • Shows risk badge
       │    • Lists recommendations
       ▼
┌─────────────────────┐
│  assessment.html    │
│  (Results Display)  │
└──────┬──────────────┘
       │
       │ 8. User views results
       ▼
┌─────────────┐
│    USER     │
│  (Browser)  │
└─────────────┘
```

---

## 3. AI ENGINE LOGIC FLOW

```
START: User submits health data
│
├─ INPUT VALIDATION
│  └─ Check all required fields present
│
├─ INITIALIZE SCORES
│  ├─ vata_score = 0
│  ├─ pitta_score = 0
│  └─ kapha_score = 0
│
├─ ANALYZE SLEEP QUALITY
│  ├─ If poor/very_poor → vata_score += 3
│  └─ If excessive → kapha_score += 2
│
├─ ANALYZE APPETITE
│  ├─ If irregular → vata_score += 3
│  ├─ If excessive → pitta_score += 2, kapha_score += 2
│  └─ If low → kapha_score += 2
│
├─ ANALYZE STRESS LEVEL
│  ├─ If high → vata_score += 4, pitta_score += 2
│  └─ If moderate → vata_score += 2
│
├─ ANALYZE DIGESTION
│  ├─ If constipation → vata_score += 4
│  ├─ If acidity → pitta_score += 4
│  ├─ If slow → kapha_score += 3
│  └─ If gas → vata_score += 3
│
├─ ANALYZE SKIN TYPE
│  ├─ If dry → vata_score += 3
│  ├─ If oily → kapha_score += 3
│  └─ If sensitive → pitta_score += 3
│
├─ ANALYZE BODY TEMPERATURE
│  ├─ If cold → vata_score += 2, kapha_score += 1
│  └─ If hot → pitta_score += 3
│
├─ ANALYZE FOOD PREFERENCE
│  ├─ If spicy → pitta_score += 2
│  ├─ If sweet → kapha_score += 2
│  └─ If bitter → vata_score += 1
│
├─ ANALYZE AGE FACTOR
│  ├─ If < 18 → kapha_score += 1 (growth phase)
│  ├─ If 18-50 → pitta_score += 1 (active phase)
│  └─ If > 50 → vata_score += 2 (aging phase)
│
├─ CALCULATE PERCENTAGES
│  ├─ total = vata_score + pitta_score + kapha_score
│  ├─ vata_percent = (vata_score / total) × 100
│  ├─ pitta_percent = (pitta_score / total) × 100
│  └─ kapha_percent = (kapha_score / total) × 100
│
├─ DETERMINE DOMINANT DOSHA
│  └─ dominant = max(vata_percent, pitta_percent, kapha_percent)
│
├─ CALCULATE RISK LEVEL
│  ├─ If dominant >= 50% → Risk = HIGH
│  ├─ If dominant >= 35% → Risk = MODERATE
│  └─ Else → Risk = LOW
│
├─ GENERATE RECOMMENDATIONS
│  ├─ Select recommendation set based on dominant dosha
│  ├─ Include: Diet, Yoga, Pranayama, Lifestyle, Herbs
│  └─ Customize based on user profile
│
└─ RETURN RESULT
   ├─ scores: {vata, pitta, kapha}
   ├─ dominant: "Vata" | "Pitta" | "Kapha"
   ├─ risk: "Low" | "Moderate" | "High"
   ├─ recommendations: [array of strings]
   └─ description: dosha explanation

END: Result displayed to user
```

---

## 4. RECOMMENDATION ENGINE FLOW

```
Input: Dominant Dosha + User Profile
│
├─ IF VATA DOMINANT
│  ├─ DIET
│  │  └─ Warm, cooked foods; ghee, nuts, sweet fruits
│  ├─ YOGA
│  │  └─ Gentle poses: Child pose, Cat-Cow, Legs-up-wall
│  ├─ PRANAYAMA
│  │  └─ Nadi Shodhana (alternate nostril breathing)
│  ├─ LIFESTYLE
│  │  └─ Regular sleep, oil massage, warm baths
│  ├─ HERBS
│  │  └─ Ashwagandha, Brahmi
│  └─ AVOID
│     └─ Cold foods, irregular routines, excessive travel
│
├─ IF PITTA DOMINANT
│  ├─ DIET
│  │  └─ Cool, fresh foods; cucumber, coconut, sweet fruits
│  ├─ YOGA
│  │  └─ Cooling poses: Moon salutation, Forward bends
│  ├─ PRANAYAMA
│  │  └─ Sheetali (cooling breath)
│  ├─ LIFESTYLE
│  │  └─ Avoid midday sun, meditation, work-life balance
│  ├─ HERBS
│  │  └─ Amla, Neem, Aloe vera
│  └─ AVOID
│     └─ Spicy foods, competitive activities, anger triggers
│
└─ IF KAPHA DOMINANT
   ├─ DIET
   │  └─ Light, warm, spicy foods; ginger, turmeric, greens
   ├─ YOGA
   │  └─ Energizing poses: Sun salutation, Warrior, Backbends
   ├─ PRANAYAMA
   │  └─ Kapalabhati (skull shining breath)
   ├─ LIFESTYLE
   │  └─ Wake early, regular exercise, avoid daytime sleep
   ├─ HERBS
   │  └─ Trikatu, Guggulu
   └─ AVOID
      └─ Dairy, sweets, sedentary lifestyle, oversleeping

Output: Personalized recommendation list
```

---

## 5. USER JOURNEY MAP

```
┌─────────────────────────────────────────────────────────────────┐
│                    USER JOURNEY                                 │
└─────────────────────────────────────────────────────────────────┘

1. DISCOVERY
   User lands on homepage
   ↓
   Sees: "AyurAI Veda™ - Ancient Wisdom. Intelligent Health."
   ↓
   Reads about Tridosha Intelligence Engine™
   ↓
   Clicks: "Start Your AI Health Assessment"

2. LEARNING
   Navigates to "About Ayurveda"
   ↓
   Learns about Vata, Pitta, Kapha
   ↓
   Understands AI + Ayurveda integration
   ↓
   Returns to assessment

3. ASSESSMENT
   Fills 9-question form
   ↓
   Answers honestly about health patterns
   ↓
   Clicks: "Analyze with Tridosha Intelligence Engine™"
   ↓
   Waits < 1 second for results

4. RESULTS
   Views dominant dosha
   ↓
   Sees visual meters (Vata, Pitta, Kapha percentages)
   ↓
   Checks risk level badge
   ↓
   Reads personalized recommendations

5. ACTION
   Downloads PDF report
   ↓
   Implements lifestyle changes
   ↓
   Shares with friends/family
   ↓
   Returns for follow-up assessment

6. EDUCATION
   Explores NEP 2020 page
   ↓
   Understands IKS integration
   ↓
   Appreciates interdisciplinary approach
   ↓
   Becomes advocate for traditional knowledge
```

---

## 6. TECHNOLOGY STACK DIAGRAM

```
┌─────────────────────────────────────────────────────────────────┐
│                    FRONTEND STACK                               │
├─────────────────────────────────────────────────────────────────┤
│  HTML5          │  Structure & Semantic markup                  │
│  CSS3           │  Styling, animations, responsive design       │
│  JavaScript     │  Interactivity, AJAX, dynamic rendering       │
│  (Vanilla JS)   │  No frameworks - lightweight & fast           │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│                    BACKEND STACK                                │
├─────────────────────────────────────────────────────────────────┤
│  Python 3.8+    │  Core programming language                    │
│  Flask 3.0      │  Web framework (lightweight, flexible)        │
│  ReportLab 4.0  │  PDF generation library                       │
│  Werkzeug       │  WSGI utility (Flask dependency)              │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│                    AI/LOGIC STACK                               │
├─────────────────────────────────────────────────────────────────┤
│  Custom Python  │  Rule-based expert system                     │
│  Algorithm      │  Weighted scoring, pattern recognition        │
│  (No ML libs)   │  Pure logic - no TensorFlow/PyTorch needed    │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│                    DEPLOYMENT STACK                             │
├─────────────────────────────────────────────────────────────────┤
│  Local Server   │  Flask development server                     │
│  (Current)      │  http://127.0.0.1:5000                        │
│                 │                                               │
│  Future Options │  • Heroku (cloud deployment)                  │
│                 │  • AWS EC2 (scalable hosting)                 │
│                 │  • Docker (containerization)                  │
│                 │  • Nginx + Gunicorn (production)              │
└─────────────────────────────────────────────────────────────────┘
```

---

## 7. SECURITY & PRIVACY ARCHITECTURE

```
┌─────────────────────────────────────────────────────────────────┐
│                    PRIVACY-FIRST DESIGN                         │
└─────────────────────────────────────────────────────────────────┘

USER DATA
    │
    ├─ Entered in browser form
    │
    ├─ Sent via HTTPS (in production)
    │
    ├─ Processed in Flask session
    │  (temporary, in-memory)
    │
    ├─ Analyzed by AI engine
    │  (no storage, immediate processing)
    │
    ├─ Results returned to browser
    │  (displayed, not stored on server)
    │
    └─ Session ends when browser closes
       (all data discarded)

NO DATABASE
NO COOKIES (except session)
NO TRACKING
NO THIRD-PARTY ANALYTICS
NO DATA RETENTION

Result: Complete user privacy
```

---

## 8. SCALABILITY ARCHITECTURE (FUTURE)

```
Current (Phase 1):
┌──────────┐
│  Flask   │ ← Single server, rule-based AI
└──────────┘

Future (Phase 2):
┌──────────┐     ┌──────────┐
│  Flask   │ ←→  │ ML Model │ ← TensorFlow/PyTorch
└──────────┘     └──────────┘

Future (Phase 3):
┌──────────┐     ┌──────────┐     ┌──────────┐
│  Flask   │ ←→  │ ML Model │ ←→  │   IoT    │
│  (API)   │     │ (Cloud)  │     │ Devices  │
└──────────┘     └──────────┘     └──────────┘
     ↓                                   ↓
┌──────────┐                      ┌──────────┐
│  Mobile  │                      │ Wearable │
│   App    │                      │  Health  │
└──────────┘                      └──────────┘
```

---

**This architecture ensures:**
✅ Clean separation of concerns  
✅ Modular, maintainable code  
✅ Scalable for future enhancements  
✅ Privacy-first design  
✅ Fast, responsive user experience  

---

**AyurAI Veda™** | Ancient Wisdom. Intelligent Health.  
Powered by Tridosha Intelligence Engine™
