import os
import json
import urllib.request
import urllib.error

class AyurvedaLLMClient:
    def __init__(self):
        # Read API keys from environment
        self.openai_key = os.getenv("OPENAI_API_KEY")
        self.anthropic_key = os.getenv("ANTHROPIC_API_KEY")
        self.gemini_key = os.getenv("GEMINI_API_KEY")
        self.deepseek_key = os.getenv("DEEPSEEK_API_KEY")
        self.groq_key = os.getenv("GROQ_API_KEY")

        # Determine active provider
        if self.deepseek_key:
            self.provider = "deepseek"
            self.api_key = self.deepseek_key
            self.model = os.getenv("DEEPSEEK_MODEL", "deepseek-chat")
            self.url = "https://api.deepseek.com/chat/completions"
        elif self.anthropic_key:
            self.provider = "anthropic"
            self.api_key = self.anthropic_key
            self.model = os.getenv("ANTHROPIC_MODEL", "claude-3-5-sonnet-20241022")
            self.url = "https://api.anthropic.com/v1/messages"
        elif self.openai_key:
            self.provider = "openai"
            self.api_key = self.openai_key
            self.model = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
            self.url = "https://api.openai.com/v1/chat/completions"
        elif self.gemini_key:
            self.provider = "gemini"
            self.api_key = self.gemini_key
            self.model = os.getenv("GEMINI_MODEL", "gemini-1.5-flash")
            self.url = f"https://generativelanguage.googleapis.com/v1beta/models/{self.model}:generateContent?key={self.gemini_key}"
        elif self.groq_key:
            self.provider = "groq"
            self.api_key = self.groq_key
            self.model = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")
            self.url = "https://api.groq.com/openai/v1/chat/completions"
        else:
            self.provider = "fallback"
            self.api_key = None
            self.model = "local-clinical-rules"
            self.url = None

        try:
            from backend.utils.ml_loader import AyurMLModelLoader
            self.ml_loader = AyurMLModelLoader()
        except Exception as e:
            print(f"[WARN] Failed to initialize ML loader in LLM client: {e}")
            self.ml_loader = None

    def generate_response(self, system_prompt: str, user_message: str, history: list = None, language: str = 'en') -> str:
        """Sends chat completion query to active provider, handles history, returns response string"""
        if self.provider == "fallback":
            return self._generate_fallback(user_message, language=language)

        if not history:
            history = []

        try:
            if self.provider in ["openai", "deepseek", "groq"]:
                messages = [{"role": "system", "content": system_prompt}]
                # Add past history
                for h in history:
                    messages.append({"role": h["role"], "content": h["content"]})
                messages.append({"role": "user", "content": user_message})

                req_body = {
                    "model": self.model,
                    "messages": messages,
                    "temperature": 0.3
                }
                
                headers = {
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json"
                }
                
                req = urllib.request.Request(
                    self.url,
                    data=json.dumps(req_body).encode("utf-8"),
                    headers=headers,
                    method="POST"
                )
                
                with urllib.request.urlopen(req, timeout=8) as response:
                    res_data = json.loads(response.read().decode("utf-8"))
                    return res_data["choices"][0]["message"]["content"]

            elif self.provider == "anthropic":
                messages = []
                for h in history:
                    messages.append({"role": h["role"], "content": h["content"]})
                messages.append({"role": "user", "content": user_message})

                req_body = {
                    "model": self.model,
                    "max_tokens": 1500,
                    "system": system_prompt,
                    "messages": messages,
                    "temperature": 0.3
                }
                
                headers = {
                    "x-api-key": self.api_key,
                    "anthropic-version": "2023-06-01",
                    "Content-Type": "application/json"
                }
                
                req = urllib.request.Request(
                    self.url,
                    data=json.dumps(req_body).encode("utf-8"),
                    headers=headers,
                    method="POST"
                )
                
                with urllib.request.urlopen(req, timeout=8) as response:
                    res_data = json.loads(response.read().decode("utf-8"))
                    return res_data["content"][0]["text"]

            elif self.provider == "gemini":
                # Combine system prompt, history, and message since Gemini uses different prompt formats
                prompt_parts = [f"System Prompt: {system_prompt}\n"]
                for h in history:
                    role_lbl = "Patient" if h["role"] == "user" else "Doctor"
                    prompt_parts.append(f"{role_lbl}: {h['content']}")
                prompt_parts.append(f"Patient: {user_message}\nDoctor:")
                
                full_prompt = "\n".join(prompt_parts)
                
                req_body = {
                    "contents": [{
                        "parts": [{"text": full_prompt}]
                    }],
                    "generationConfig": {
                        "temperature": 0.3
                    }
                }
                
                headers = {
                    "Content-Type": "application/json"
                }
                
                req = urllib.request.Request(
                    self.url,
                    data=json.dumps(req_body).encode("utf-8"),
                    headers=headers,
                    method="POST"
                )
                
                with urllib.request.urlopen(req, timeout=8) as response:
                    res_data = json.loads(response.read().decode("utf-8"))
                    return res_data["candidates"][0]["content"]["parts"][0]["text"]

        except urllib.error.HTTPError as e:
            error_msg = e.read().decode("utf-8")
            print(f"HTTPError in {self.provider} API call: {e.code} - {error_msg}")
            return self._generate_fallback(user_message, api_error=f"API connection error ({self.provider})", language=language)
        except Exception as e:
            print(f"Error in {self.provider} LLM client: {str(e)}")
            return self._generate_fallback(user_message, api_error=str(e), language=language)

    def _generate_fallback(self, query: str, api_error: str = None, language: str = 'en') -> str:
        """Fallback response generator mimicking an Ayurvedic practitioner using heuristic template"""
        query_lower = query.strip().lower().rstrip("?./!")
        lang_lbl = language.split('-')[0].lower()
        
        # Check for emergency triggers
        emergencies = ["chest pain", "heart attack", "stroke", "breathing difficulty", "severe bleeding", "poison"]
        if any(e in query_lower for e in emergencies):
            if lang_lbl == 'hi':
                return """### 🚨 आपातकालीन चिकित्सा सूचना

* **स्थिति**: गंभीर चेतावनी (रेड फ्लैग)
* **नैदानिक मूल्यांकन**: वर्णित लक्षण एक संभावित जीवन-घातक आपातकाल का संकेत देते हैं।
* **तत्काल सिफारिश**: कृपया तुरंत आपातकालीन चिकित्सा सहायता लें या अपने स्थानीय आपातकालीन नंबर (जैसे 108 या 112) पर कॉल करें। उपचार में देरी न करें।

*अस्वीकरण: आयुर्वेदिक परामर्श केवल शैक्षिक और निवारक सहायता के लिए हैं और आपातकालीन स्थितियों का समाधान नहीं कर सकते।*"""
            elif lang_lbl == 'gu':
                return """### 🚨 ઇમરજન્સી મેડિકલ નોટિસ

* **સ્થિતિ**: ગંભીર ચેતવણી (રેડ ફ્લેગ)
* **ક્લિનિકલ મૂલ્યાંકન**: વર્ણવેલ લક્ષણો સંભવિત જીવન-જોખમી કટોકટી સૂચવે છે.
* **તાત્કાલિક ભલામણ**: કૃપા કરીને તાત્કાલિક તબીબી સહાય મેળવો અથવા તમારા સ્થાનિક ઇમરજન્સી નંબર (જેમ કે 108 અથવા 112) પર કૉલ કરો. સારવારમાં વિલંબ કરશો નહીં.

*ડિસ્ક્લેમર: આયુર્વેદિક પરામર્શ માત્ર શૈક્ષણિક અને નિવારક સહાય માટે છે અને કટોકટીની પરિસ્થિતિઓનો ઉકેલ લાવી શકતા નથી.*"""
            else:
                return """### 🚨 EMERGENCY MEDICAL NOTICE

* **Emergency Status**: CRITICAL RED FLAG DETECTED
* **Clinical Assessment**: The symptoms described suggest a potential life-threatening emergency.
* **Urgent Recommendation**: Please seek immediate medical attention or call emergency services (like 911 or local emergency numbers) immediately. Do not delay care.

*Disclaimer: Ayurvedic consultations are for educational and preventive support only and cannot address medical emergencies.*"""

        # 1. Greetings check
        greetings = ["hi", "hello", "namaste", "hey", "good morning", "good afternoon", "good evening"]
        is_pure_greeting = False
        temp_query = query_lower.strip(" ,.!?;:")
        if temp_query in greetings:
            is_pure_greeting = True
            
        if not is_pure_greeting:
            for g in greetings:
                if temp_query.startswith(g):
                    remaining = temp_query[len(g):].strip(" ,.!?;:")
                    if remaining:
                        query_lower = remaining
                        break
                        
        if is_pure_greeting or any(g == query_lower for g in greetings):
            if lang_lbl == 'hi':
                return """### 🌿 नमस्ते! आयुर्वाणी™ में आपका स्वागत है

मैं आपकी आयुर्वेदिक AI चिकित्सक हूँ, जो आपको पारंपरिक आयुर्वेदिक ज्ञान के माध्यम से स्वास्थ्य और संतुलन की ओर ले जाने के लिए यहाँ हूँ।

**आज मैं आपकी क्या सहायता कर सकती हूँ?**
कृपया मुझे बताएं:
* 🩺 **कोई भी लक्षण** जो आप महसूस कर रहे हैं (जैसे: कब्ज, एसिडिटी, भारीपन)।
* 🍽️ **आपकी भोजन की आदतें** (जैसे: खाने का समय, प्राथमिकताएं, पाचन समस्याएं)।
* 😴 **आपकी नींद और ऊर्जा का स्तर** (जैसे: नींद की गुणवत्ता, तनाव)।
* 🧬 **आयुर्वेद के बारे में सामान्य प्रश्न**।"""
            elif lang_lbl == 'gu':
                return """### 🌿 નમસ્તે! આયુર્વાણી™ માં આપનું સ્વાગત છે

હું તમારા આયુર્વેદિક AI ચિકિત્સક છું, જે તમને પરંપરાગત આયુર્વેદિક જ્ઞાન દ્વારા સ્વાસ્થ્ય અને સંતુલન તરફ દોરી જવા માટે અહીં છું.

**આજે હું તમને કેવી રીતે મદદ કરી શકું?**
કૃપા કરીને મને જણાવો:
* 🩺 **કોઈપણ લક્ષણો** જે તમે અનુભવી રહ્યા છો (જેમ કે: કબજિયાત, એસિડિટી, ભારેપણું).
* 🍽️ **તમારા ખોરાકની ટેવો** (જેમ કે: ખાવાનો સમય, પસંદગીઓ, પાચન સમસ્યાઓ).
* 😴 **તમારી ઊંઘ અને ઉર્જાનું સ્તર** (જેમ કે: ઊંઘની ગુણવત્તા, તણાવ).
* 🧬 **આયુર્વેદ વિશે સામાન્ય પ્રશ્નો**।"""
            else:
                return """### 🌿 Namaste! Welcome to AyurVaani™

I am your Ayurvedic AI physician, here to guide you towards health and balance through classical Ayurvedic wisdom.

**How can I help you today?**
Please tell me about:
* 🩺 **Any symptoms** you are experiencing (e.g., bloating, acidity, congestion).
* 🍽️ **Your food habits** (e.g., eating times, preferences, digestive issues).
* 😴 **Your sleep and energy levels** (e.g., sleep quality, stress).
* 🧬 **Your constitution or general queries** about Ayurveda.

*(Note: RAG LLM engine is running in Local Heuristic Mode)*"""

        # 2. General Ayurveda explanation check
        if "what is ayurveda" in query_lower or "about ayurveda" in query_lower or "define ayurveda" in query_lower or query_lower == "ayurveda":
            if lang_lbl == 'hi':
                return """### 🌿 आयुर्वेद क्या है?

**आयुर्वेद** (दो शब्दों से मिलकर बना है: *आयु* अर्थात "जीवन" और *वेद* अर्थात "विज्ञान" या "ज्ञान") भारत की 5,000 साल पुरानी पारंपरिक चिकित्सा प्रणाली है। यह शरीर, मन और आत्मा के बीच समग्र संतुलन बनाए रखने पर केंद्रित जीवन का विज्ञान है।

#### 🔑 आयुर्वेद के मूल सिद्धांत:
1. **त्रिदोष सिद्धांत**: प्रत्येक व्यक्ति तीन मूलभूत ऊर्जाओं या *दोषों* के एक अद्वितीय संयोजन से बना है:
   - 🌬️ **वात** (आकाश + वायु): गति, तंत्रिका तंत्र और रचनात्मकता को नियंत्रित करता है।
   - 🔥 **पित्त** (अग्नि + जल): चयापचय, पाचन और बुद्धि को नियंत्रित करता है।
   - 🌳 **कफ** (जल + पृथ्वी): शरीर की संरचना, स्थिरता और रोग प्रतिरोधक क्षमता को नियंत्रित करता है।
2. **प्रकृति और विकृति**:
   - **प्रकृति**: जन्म के समय निर्धारित आपका मूल शारीरिक और मानसिक संविधान।
   - **विकृति**: आपके असंतुलन की वर्तमान स्थिति। स्वास्थ्य तब प्राप्त होता है जब विकृति वापस प्रकृति के अनुकूल हो जाती है।
3. **अग्नि (पाचन अग्नि)**: जीवन और पाचन का स्रोत। एक मजबूत अग्नि अच्छा चयापचय सुनिश्चित करती है, जबकि एक कमजोर अग्नि **आम** (विषाक्त अपशिष्ट) पैदा करती है जो रोगों का मूल कारण है।
4. **आहार और विहार**: भोजन, दैनिक दिनचर्या (*दिनचर्या*), और मौसमी दिनचर्या (*ऋतुचर्या*) को प्राथमिक चिकित्सा के रूप में उपयोग करना।"""
            elif lang_lbl == 'gu':
                return """### 🌿 આયુર્વેદ શું છે?

**આયુર્વેદ** (બે શબ્દોનો બનેલો છે: *આયુ* એટલે "જીવન" અને *વેદ* એટલે "વિજ્ઞાન" અથવા "જ્ઞાન") એ ભારતની 5,000 વર્ષ જૂની પરંપરાગત સારવાર પદ્ધતિ છે. તે શરીર, મન અને આત્મા વચ્ચે સંતુલન જાળવવા પર કેન્દ્રિત જીવનનું વિજ્ઞાન છે.

#### 🔑 આયુર્વેદના મૂળ પાયા:
1. **ત્રિદોષ સિદ્ધાંત**: દરેક વ્યક્તિ ત્રણ મૂળભૂત ઉર્જાઓ અથવા *દોષો* ના અનન્ય મિશ્રણથી બનેલી છે:
   - 🌬️ **વાત** (આકાશ + વાયુ): હલનચલન, ચેતાતંત્ર અને સર્જનાત્મકતાને નિયંત્રિત કરે છે.
   - 🔥 **પિત્ત** (અગ્નિ + જળ): ચયાપચય, પાચન અને બુદ્ધિને નિયંત્રિત કરે છે.
   - 🌳 **કફ** (જળ + પૃથ્વી): શરીરનું માળખું, સ્થિરતા અને રોગપ્રતિકારક શક્તિને નિયંત્રિત કરે છે.
2. **પ્રકૃતિ અને વિકૃતિ**:
   - **પ્રકૃતિ**: જન્મ સમયે નક્કી થયેલું તમારું મૂળ બંધારણ.
   - **विकृति**: તમારી વર્તમાન અસંતુલનની સ્થિતિ. જ્યારે વિકૃતિ પાછી પ્રકૃતિ જેવી થઈ જાય ત્યારે સ્વાસ્થ્ય પ્રાપ્ત થાય છે.
3. **અગ્નિ (પાચન અગ્નિ)**: જીવન અને પાચનનો સ્ત્રોત. મજબૂત અગ્નિ સારું ચયાપચેય સુનિશ્ચિત કરે છે, જ્યારે નબળો અગ્નિ **આમ** (ઝેરી કચરો) પેદા કરે છે જે રોગોનું મુખ્ય કારણ છે.
4. **આહાર અને વિહાર**: ખોરાક, દૈનિક દિનચર્યા (*દિનચર્યા*), અને ઋતુચર્યાને પ્રાથમિક સારવાર તરીકે વાપરવી."""
            else:
                return """### 🌿 What is Ayurveda?

**Ayurveda** (composed of *Ayur* meaning "Life" and *Veda* meaning "Science" or "Knowledge") is the traditional 5,000-year-old healing system of India. It is a comprehensive science of life focused on prevention, longevity, and maintaining holistic balance between body, mind, and spirit.

#### 🔑 Core Pillars of Ayurveda:
1. **Tridosha Theory**: Every person is composed of a unique combination of three fundamental energies or *Doshas*:
   - 🌬️ **Vata** (Air + Space): Governing movement, nervous system, and creativity.
   - 🔥 **Pitta** (Fire + Water): Governing metabolism, digestion, and intellect.
   - 🌳 **Kapha** (Water + Earth): Governing physical structure, stability, and immunity.
2. **Prakriti & Vikriti**:
   - **Prakriti**: Your baseline genetic constitution determined at birth.
   - **Vikriti**: Your current state of imbalance. Health is achieved when Vikriti returns to match Prakriti.
3. **Agni (Digestive Fire)**: The source of life and digestion. A strong Agni ensures good metabolism, whereas an impaired Agni generates **Ama** (toxic metabolic residue), leading to disease.
4. **Ahara (Diet) & Vihara (Lifestyle)**: Using food, daily routines (*Dinacharya*), and seasonal routines (*Ritucharya*) as primary medicines.

*(Note: RAG LLM engine is running in Local Heuristic Mode)*"""

        # 3. Dosha descriptions check
        if "what is vata" in query_lower or "vata dosha" in query_lower or query_lower == "vata":
            if lang_lbl == 'hi':
                return """### 🌬️ वात दोष को समझना

**वात** आकाश और वायु तत्वों से बना है। यह शरीर की मुख्य ड्राइविंग फोर्स है, जो सभी गतियों, तंत्रिका आवेगों, श्वास और रक्त परिसंचरण को नियंत्रित करती है।

* **गुण**: रूखा (रूक्ष), हल्का (लघु), ठंडा (शीत), खुरदरा, सूक्ष्म और गतिशील (चल)।
* **वात का स्थान**: मलाशय, कूल्हे, जांघ, कान, हड्डियां और त्वचा।
* **संतुलित अवस्था**: रचनात्मकता, मानसिक चपलता, उत्साह और नियमित मल-त्याग।
* **असंतुलन के लक्षण**: शुष्कता, कब्ज, गैस, पेट फूलना, चिंता, अनिद्रा और थकान।
* **शांत करने के उपाय**: गर्मी, चिकनाई, गर्म पका हुआ भोजन, नियमित दिनचर्या और गर्म तेल से मालिश (अभ्यंग)।"""
            elif lang_lbl == 'gu':
                return """### 🌬️ વાત દોષને સમજવો

**વાત** આકાશ અને વાયુ તત્વોનો બનેલો છે. તે શરીરમાં તમામ હલનચલન, ચેતા આવેગ, શ્વાસ અને રક્ત પરિભ્રમણને નિયંત્રિત કરે છે.

* **ગુણો**: સૂકો (રૂક્ષ), હળવો (લઘુ), ઠંડો (શીત), ખરબચડો, સૂક્ષ્મ અને ગતિશીલ (ચલ).
* **વાતનું સ્થાન**: મોટું આંતરડું, થાપા, સાંધા, કાન, હાડકાં અને ત્વચા.
* **સંતુલિત સ્થિતિ**: સર્જનાત્મકતા, માનસિક સ્ફૂર્તિ, ઉત્સાહ અને સરળ મળોત્સર્જન.
* **અસંતુલનના લક્ષણો**: શુષ્કતા, કબજિયાત, ગેસ, પેટ ફૂલવું, ચિંતા, અનિદ્રા અને થાક.
* **શાંત કરવાના ઉપાયો**: ગરમી, તેલયુક્તતા, ગરમ રાંધેલો ખોરાક, નિયમિત દિનચર્યા અને ગરમ તેલથી માલિશ (અભ્યંગ)."""
            else:
                return """### 🌬️ Understanding Vata Dosha

**Vata** is composed of the **Space (Akasha)** and **Air (Vayu)** elements. It is the primary driving force in the body, governing all movements, nerve impulses, breathing, and circulation.

* **Qualities (Gunas)**: Dry (Ruksha), Light (Laghu), Cold (Sheeta), Rough (Khara), Subtle (Sukshma), and Mobile (Chala).
* **Seat of Vata**: Colon, hips, thighs, ears, bones, and skin.
* **Balanced State**: Creativity, mental agility, enthusiasm, and smooth elimination.
* **Imbalance Symptoms**: Dryness, constipation, gas, bloating, anxiety, insomnia, cracking joints, and fatigue.
* **Pacifying Principles**: Warmth, oiliness, cooked grounding foods, consistent routines, and warm oil self-massage (Abhyanga)."""

        if "what is pitta" in query_lower or "pitta dosha" in query_lower or query_lower == "pitta":
            if lang_lbl == 'hi':
                return """### 🔥 पित्त दोष को समझना

**पित्त** अग्नि और जल तत्वों से बना है। यह शरीर में सभी परिवर्तनों, गर्मी उत्पादन, चयापचय प्रक्रियाओं और पाचन को नियंत्रित करता है।

* **गुण**: गर्म (उष्ण), तीखा (तीक्ष्ण), हल्का (लघु), तरल (द्रव) और थोड़ा तैलीय।
* **पित्त का स्थान**: छोटी आंत, पेट, पसीने की ग्रंथियां, रक्त, त्वचा और आंखें।
* **संतुलित अवस्था**: मजबूत पाचन, स्पष्ट बुद्धि, साहस, नेतृत्व और इच्छाशक्ति।
* **असंतुलन के लक्षण**: एसिडिटी, सीने में जलन, सूजन, त्वचा पर चकत्ते, अत्यधिक पसीना और गुस्सा।
* **शांत करने के उपाय**: ठंडक, मीठे/कड़वे/कसैले स्वाद, विश्राम और मसालेदार/खट्टे भोजन से परहेज।"""
            elif lang_lbl == 'gu':
                return """### 🔥 પિત્ત દોષને સમજવો

**પિત્ત** અગ્નિ અને જળ તત્વોનો બનેલો છે. તે શરીરમાં તમામ રૂપાંતરણ, ગરમી ઉત્પાદન, ચયાપચયની પ્રક્રિયાઓ અને પાચનને નિયંત્રિત કરે છે.

* **ગુણો**: ગરમ (ઉષ્ણ), તીક્ષ્ણ, હળવો (લઘુ), પ્રવાહી (દ્રવ) અને થોડો ચીકણો.
* **પિત્તનું સ્થાન**: નાનું આંતરડું, પેટ, પરસેવાની ગ્રંથીઓ, રક્ત, ત્વચા અને આંખો.
* **સંતુલિત સ્થિતિ**: મજબૂત પાચન, સ્પષ્ટ બુદ્ધિ, હિંમત, નેતૃત્વ અને કાર્યશક્તિ.
* **અસંતુલનના લક્ષણો**: એસિડિટી, છાતીમાં બળતરા, સોજો, ત્વચા પર ફોલ્લીઓ, અતિશય પરસેવો અને ગુસ્સો.
* **શાંત કરવાના ઉપાયો**: ઠંડક, મીઠા/કડવા/તુરા સ્વાદ, આરામ અને તીખા/ખાટા ખોરાકથી પરહેજ."""
            else:
                return """### 🔥 Understanding Pitta Dosha

**Pitta** is composed of the **Fire (Agni)** and **Water (Jala)** elements. It governs all transformation, heat production, metabolic processes, and digestion in the body.

* **Qualities (Gunas)**: Hot (Ushna), Sharp (Tikshna), Light (Laghu), Liquid (Drava), Sour (Amla), and Oily (Sasneha).
* **Seat of Pitta**: Small intestine, stomach, sweat glands, blood, skin, and eyes.
* **Balanced State**: Strong digestion, clear intellect, courage, leadership, and drive.
* **Imbalance Symptoms**: Acidity, heartburn, inflammation, skin rashes, excessive sweating, anger, and heat sensitivity.
* **Pacifying Principles**: Coolness, sweet/bitter/astringent tastes, relaxation, and reducing spicy, sour, and fermented foods."""

        if "what is kapha" in query_lower or "kapha dosha" in query_lower or query_lower == "kapha":
            if lang_lbl == 'hi':
                return """### 🌳 कफ दोष को समझना

**कफ** जल और पृथ्वी तत्वों से बना है। यह शरीर को संरचना, चिकनाई, स्थिरता और रोग प्रतिरोधक क्षमता प्रदान करता है।

* **गुण**: भारी (गुरु), ठंडा (शीत), कोमल (मृदु), तैलीय (स्निग्ध), स्थिर और चिकना।
* **कफ का स्थान**: छाती, गला, सिर, जोड़, पेट और लसीका।
* **संतुलित अवस्था**: शारीरिक शक्ति, मजबूत रोग प्रतिरोधक क्षमता, धैर्य, करुणा और स्थिरता।
* **असंतुलन के लक्षण**: कफ/बलगम जमा होना, वजन बढ़ना, सुस्ती, मंद पाचन और अत्यधिक नींद।
* **शांत करने के उपाय**: गर्मी, सूखापन, हल्कापन, शारीरिक गतिविधि, मसाले और भारी/तैलीय खाद्य पदार्थों से परहेज।"""
            elif lang_lbl == 'gu':
                return """### 🌳 કફ દોષને સમજવો

**કફ** જળ અને પૃથ્વી તત્વોનો બનેલો છે. તે શરીરને માળખું, સ્નિગ્ધતા, સ્થિરતા અને રોગપ્રતિકારક શક્તિ આપે છે.

* **ગુણો**: ભારે (ગુરુ), ઠંડો (શીત), કોમળ (મૃદુ), ચીકણો (સ્નિગ્ધ), સ્થિર અને ચીકણો.
* **કફનું સ્થાન**: છાતી, ગળું, માથું, સાંધા, પેટ અને લસિકા.
* **સંતુલિત સ્થિતિ**: શારીરિક શક્તિ, મજબૂત રોગપ્રતિકારક શક્તિ, ધીરજ, કરુણા અને સ્થિરતા.
* **અસંતુલનના લક્ષણો**: કફ/ચીકણો કચરો જમા થવો, વજન વધવું, આળસ, મંદ પાચન અને વધુ ઊંઘ આવવી.
* **શાંત કરવાના ઉપાયો**: ગરમી, સૂકાપણું, હળવાશ, શારીરિક પ્રવૃત્તિ, મસાલા અને ભારે/તેલી ખોરાકથી પરહેજ."""
            else:
                return """### 🌳 Understanding Kapha Dosha

**Kapha** is composed of the **Water (Jala)** and **Earth (Prithvi)** elements. It provides structure, lubrication, cohesion, stability, and immunity to the body.

* **Qualities (Gunas)**: Heavy (Guru), Cold (Sheeta), Soft (Mridu), Oily (Snigdha), Stable (Sthira), and Slimy (Picchila).
* **Seat of Kapha**: Chest, throat, head, joints, stomach, and lymph.
* **Balanced State**: Physical strength, strong immunity, patience, compassion, and stability.
* **Imbalance Symptoms**: Congestion, mucus buildup, weight gain, lethargy, sluggish digestion, and oversleeping.
* **Pacifying Principles**: Warmth, dryness, lightness, activity, spices, and avoiding heavy, oily, and cold dairy foods."""

        # ML CCRAS SOP Model Integration
        ml_block = ""
        raw_ml_insights = []
        if self.ml_loader and self.ml_loader.vectorizer and len(self.ml_loader.chunks) > 0:
            try:
                from sklearn.metrics.pairwise import cosine_similarity
                import numpy as np
                query_vec = self.ml_loader.vectorizer.transform([query])
                similarities = cosine_similarity(query_vec, self.ml_loader.tfidf_matrix).flatten()
                top_indices = np.argsort(similarities)[-3:][::-1]
                
                for idx in top_indices:
                    if similarities[idx] > 0.08:
                        chunk_text = self.ml_loader.chunks[idx].strip()
                        
                        # Refine: clean and filter boilerplate text
                        boilerplate = [
                            r"(?i)ccras", r"(?i)manual\s+of\s+standard\s+operative\s+procedures",
                            r"(?i)prakriti\s+assessment", r"(?i)all\s+right\s+reserved",
                            r"(?i)ministry\s+of\s+ayush", r"(?i)government\s+of\s+india",
                            r"(?i)publisher", r"(?i)isbn", r"(?i)ccras\s+shall\s+not\s+be\s+accountable",
                            r"(?i)this\s+is\s+a\s+preview", r"(?i)some\s+pages\s+are\s+omitted",
                            r"(?i)successful\s+completion\s+of\s+training"
                        ]
                        import re
                        for pattern in boilerplate:
                            chunk_text = re.sub(pattern, "", chunk_text)
                            
                        # Clean spaces and OCR junk
                        chunk_text = re.sub(r'\s+', ' ', chunk_text).strip()
                        chunk_text = chunk_text.strip(".:,- ")
                        
                        # Sentence-level refinement: only take the most relevant sentences
                        sentences = re.split(r'(?<=[.!?])\s+', chunk_text)
                        relevant_sentences = []
                        keywords = ['vata', 'pitta', 'kapha', 'dosha', 'diet', 'food', 'body', 'mind', 'health', 'sleep', 'agni', 'prakriti', 'assessment']
                        for sentence in sentences:
                            if any(kw in sentence.lower() for kw in keywords) and len(sentence) > 15:
                                # Ensure no duplicates
                                if sentence not in relevant_sentences:
                                    relevant_sentences.append(sentence)
                                    
                        if relevant_sentences:
                            refined_chunk = " ".join(relevant_sentences[:3]) # Limit to top 3 sentences for output refinement
                            if len(refined_chunk) > 30 and refined_chunk not in raw_ml_insights:
                                raw_ml_insights.append(refined_chunk)
                                
                if raw_ml_insights:
                    if lang_lbl == 'hi':
                        ml_block = "\n\n### 🧠 राष्ट्रीय आयुर्वेद मानकों (CCRAS) से प्रमाणित अंतर्दृष्टि:\n"
                    elif lang_lbl == 'gu':
                        ml_block = "\n\n### 🧠 રાષ્ટ્રીય આયુર્વેદ ધોરણો (CCRAS) દ્વારા પ્રમાણિત માહિતી:\n"
                    else:
                        ml_block = "\n\n### 🧠 CCRAS Clinical SOP Standard Guidelines (ML-derived):\n"
                    for ins in raw_ml_insights[:2]:
                        ml_block += f"- {ins}\n"
            except Exception as e:
                print(f"Error getting ML insights in fallback: {str(e)}")

        # 4. Real-time web search integration and self-filtering (no urls, site names, or search words)
        web_block = ""
        raw_insights = []
        try:
            import re
            from backend.utils.web_searcher import WebSearcher
            searcher = WebSearcher()
            web_results = searcher.search(query, num_results=3)
            
            # Filter and clean up snippets
            for res in web_results:
                snippet = res['snippet']
                # Clean up promotional site mentions and scrapings
                site_patterns = [
                    r"(?i)planet\s*ayurveda", r"(?i)birla\s*ayurveda", r"(?i)easy\s*ayurveda",
                    r"(?i)ayurveda\s*experts", r"(?i)bams\s*physician", r"(?i)click\s*here",
                    r"(?i)read\s*more", r"(?i)learn\s*about", r"(?i)webmd", r"(?i)healthline",
                    r"(?i)visit\s*our", r"(?i)subscribe", r"(?i)contact\s*us", r"(?i)all\s*about\s*ayurveda"
                ]
                for pattern in site_patterns:
                    snippet = re.sub(pattern, "", snippet)
                
                # Strip duplicate whitespace and clean sentences
                snippet = re.sub(r'\s+', ' ', snippet).strip()
                # Remove leading/trailing dots, colons, or dashes
                snippet = snippet.strip(".:,- ")
                
                if len(snippet) > 20:
                    raw_insights.append(snippet)
            
            if raw_insights:
                if lang_lbl == 'hi':
                    web_block = "\n\n### 🌿 आयुर्वेदिक मार्गदर्शन एवं अंतर्दृष्टि:\n"
                elif lang_lbl == 'gu':
                    web_block = "\n\n### 🌿 આયુર્વેદિક માર્ગદર્શન અને આંતરદૃષ્ટિ:\n"
                else:
                    web_block = "\n\n### 🌿 Ayurvedic Guidance & Insights:\n"
                for ins in raw_insights[:3]:
                    cap_ins = ins[0].upper() + ins[1:] if ins else ""
                    web_block += f"- {cap_ins}\n"
        except Exception as e:
            print(f"Error getting fallback web search: {str(e)}")

        # 5. Non-clinical general queries check (if we have web results and it's not a standard symptom)
        symptom_words = ["constipation", "gas", "bloat", "acidity", "burn", "heat", "weight", "heavy", "congestion", "mucus", "cough", "fever", "pain"]
        is_symptom = any(sw in query_lower for sw in symptom_words)
        
        if (web_block or ml_block) and not is_symptom and not any(g in query_lower for g in ["what is vata", "what is pitta", "what is kapha", "what is ayurveda", "about ayurveda", "define ayurveda"]):
            if lang_lbl == 'hi':
                return f"""### 🌿 आयुर्वाणी™ आयुर्वेदिक परामर्श

पारंपरिक सिद्धांतों और नैदानिक टिप्पणियों के आधार पर, यहाँ **{query}** के संबंध में आवश्यक जानकारी दी गई है:
{ml_block}{web_block}
---
*अस्वीकरण: यह जानकारी केवल शैक्षिक उद्देश्यों के लिए है। व्यक्तिगत निदान के लिए कृपया एक योग्य BAMS आयुर्वेदिक चिकित्सक से परामर्श करें।*"""
            elif lang_lbl == 'gu':
                return f"""### 🌿 આયુર્વાણી™ આયુર્વેદિક પરામર્શ

પરંપરાગત સિદ્ધાંતો અને ક્લિનિકલ અવલોકનોના આધારે, અહીં **{query}** સંબંધિત માહિતી આપવામાં આવી છે:
{ml_block}{web_block}
---
*ડિસ્ક્લેમર: આ માહિતી માત્ર શૈક્ષણિક હેતુઓ માટે છે. વ્યક્તિગત નિદાન માટે કૃપા કરીને લાયક BAMS આયુર્વેદિક ચિકિત્સકનો સંપર્ક કરો.*"""
            else:
                return f"""### 🌿 AyurVaani™ Ayurvedic Consultation

Based on classical principles and therapeutic observations, here is what you need to know regarding **{query}**:
{ml_block}{web_block}
---
*Disclaimer: This information is for educational purposes. Please consult a qualified BAMS Ayurvedic practitioner for personalized diagnosis.*"""

        # 6. Fallback default symptom reporting for Vata, Pitta, and Kapha symptoms
        dosha = "Vata"
        vikriti = "Vata Imbalance"
        dhatu = "Rasa Dhatu"
        srotas = "Annavaha Srotas"
        explanation = "The symptoms point to an accumulation of dry and cold qualities, affecting the movement (Apana Vayu) within the lower intestines."
        
        if "acidity" in query_lower or "burn" in query_lower or "heat" in query_lower:
            dosha = "Pitta"
            vikriti = "Pitta Aggravation"
            dhatu = "Rakta Dhatu"
            srotas = "Annavaha Srotas"
            explanation = "This indicates an aggravation of Ushna (hot) and Tikshna (sharp) gunas, leading to hyperacidity in the stomach (Amashaya)."
        elif "weight" in query_lower or "heavy" in query_lower or "congestion" in query_lower or "mucus" in query_lower:
            dosha = "Kapha"
            vikriti = "Kapha Accumulation"
            dhatu = "Meda Dhatu"
            srotas = "Pranavaha Srotas"
            explanation = "This suggests an excess of Guru (heavy) and Manda (slow) gunas, causing sluggish metabolism (Manda Agni)."

        if lang_lbl == 'hi':
            # Translate Vata, Pitta, Kapha categories
            dosha_hi = "वात" if dosha == "Vata" else "पित्त" if dosha == "Pitta" else "कफ"
            vikriti_hi = "वात असंतुलन" if dosha == "Vata" else "पित्त प्रकोप" if dosha == "Pitta" else "कफ संचय"
            dhatu_hi = "रस धातु" if dosha == "Vata" else "रक्त धातु" if dosha == "Pitta" else "मेद धातु"
            srotas_hi = "अन्नवह स्रोतस" if srotas == "Annavaha Srotas" else "प्राणवह स्रोतस"
            
            if dosha == "Vata":
                explanation_hi = "सूखापन और ठंडापन बढ़ने के कारण मलाशय में अपान वायु का सामान्य प्रवाह अवरुद्ध हुआ है।"
            elif dosha == "Pitta":
                explanation_hi = "उष्ण (गर्म) और तीक्ष्ण (तीखे) गुणों के बढ़ने से पेट (आमाशय) में जलन और अम्लता (एसिडिटी) बढ़ गई है।"
            else:
                explanation_hi = "गुरु (भारी) और मंद (धीमी) गुणवत्ता के जमा होने से पाचन अग्नि मंद पड़ गई है।"

            return f"""### 🌿 आयुर्वेदिक परामर्श रिपोर्ट

#### 📋 नैदानिक सारांश
* **संभावित मुख्य दोष**: {dosha_hi} दोष शामिल है।
* **प्रकृति प्रभाव**: वर्तमान लक्षण आपके मूल शारीरिक संतुलन में बदलाव का संकेत देते हैं।
* **संभावित विकृति**: {vikriti_hi} (असंतुलन की वर्तमान स्थिति)।
* **चिकित्सीय कारण**: {explanation_hi}
* **आयुर्वेदिक व्याख्या**: प्रभावित स्रोतस: {srotas_hi}। प्रभावित धातु: {dhatu_hi}। पाचन अग्नि की स्थिति मंद या अनियमित है। अल्प मात्रा में आम (विषाक्त अपशिष्ट) की उपस्थिति है।{ml_block}{web_block}

---

#### 🥗 आहार निर्देश (आहार)
* **अनुकूल**: ताजा, गुनगुना और आसानी से पचने वाला भोजन। जीरा, अदरक, और सौंफ का अधिक प्रयोग करें।
* **परहेज**: ठंडी, सूखी, कच्ची, बासी और बहुत अधिक प्रसंस्कृत खाद्य पदार्थों से बचें। बर्फ का ठंडा पानी न पिएं।

#### 🧘 दैनिक दिनचर्या और जीवनशैली (विहार)
* **जीवनशैली**: भोजन और सोने का समय निश्चित रखें। गुनगुने तिल या नारियल के तेल से नियमित शरीर की मालिश (अभ्यंग) करें।
* **योग**: वज्रासन, बालासन (शिशु मुद्रा), और हल्के सूर्य नमस्कार।
* **प्राणायाम**: नाड़ी शोधन (अनुलोम-विलोम) प्रतिदिन 10 मिनट करें।
* **ऋतुचर्या**: मौसम के अनुसार अपने पहनावे और दिनचर्या में बदलाव लाएं, सर्दियों में शरीर गर्म रखें और गर्मियों में ठंडा।

---

#### ⚠️ चिकित्सा चेतावनी और अस्वीकरण
* **गंभीर लक्षण**: यदि आपको तीव्र दर्द, तेज बुखार, या मल में खून आने जैसी समस्या हो, तो तुरंत चिकित्सक से संपर्क करें।
* **अस्वीकरण**: यह जानकारी केवल शैक्षिक है। कोई भी विशेष जड़ी-बूटी लेने से पहले कृपया एक योग्य BAMS आयुर्वेदिक चिकित्सक से सलाह लें।"""
            
        elif lang_lbl == 'gu':
            # Translate Vata, Pitta, Kapha categories
            dosha_gu = "વાત" if dosha == "Vata" else "પિત્ત" if dosha == "Pitta" else "કફ"
            vikriti_gu = "વાત અસંતુલન" if dosha == "Vata" else "પિત્ત પ્રકોપ" if dosha == "Pitta" else "કફ સંચય"
            dhatu_gu = "રસ ધાતુ" if dosha == "Vata" else "રક્ત ધાતુ" if dosha == "Pitta" else "મેદ ધાતુ"
            srotas_gu = "અન્નવહ સ્રોતસ" if srotas == "Annavaha Srotas" else "પ્રાણવહ સ્રોતસ"
            
            if dosha == "Vata":
                explanation_gu = "શુષ્કતા અને ઠંડક વધવાને લીધે મળાશયમાં અપાન વાયુનો સામાન્ય માર્ગ અવરોધાયો છે."
            elif dosha == "Pitta":
                explanation_gu = "ઉષ્ણ (ગરમ) અને તીક્ષ્ણ ગુણો વધવાને કારણે હોજરીમાં બળતરા અને અમ્લતા (એસિડિટી) વધી છે."
            else:
                explanation_gu = "ગુરુ (ભારે) અને મંદ ગુણો જમા થવાને લીધે પાચન અગ્નિ નબળો પડ્યો છે."

            return f"""### 🌿 આયુર્વેદિક પરામર્શ રિપોર્ટ

#### 📋 ક્લિનિકલ નિદાન સારાંશ
* **સંભવિત દોષ**: {dosha_gu} દોષ સામેલ છે.
* **પ્રકૃતિ પ્રભાવ**: હાલના લક્ષણો તમારા મૂળ શારીરિક સંતુલનમાં ફેરફાર સૂચવે છે.
* **સંભવિત વિકૃતિ**: {vikriti_gu} (અસંતુલનની વર્તમાન સ્થિતિ).
* **ક્લિનિકલ કારણ**: {explanation_gu}
* **આયુર્વેદિક સ્પષ્ટીકરણ**: પ્રભાવિત સ્રોતસ: {srotas_gu}। પ્રભાવિત ધાતુ: {dhatu_gu}। પાચન અગ્નિની સ્થિતિ મંદ અથવા અનિયમિત છે. પાચનમાં સહેજ આમ (ઝેરી કચરો) ની હાજરી જણાય છે.{ml_block}{web_block}

---

#### 🥗 આહાર માર્ગદર્શન (આહાર)
* **અનુકૂળ**: તાજો, ગરમ અને હળવો પચી શકે તેવો ખોરાક. જીરું, વરિયાળી અને આદુનો ઉપયોગ કરો.
* **પરહેજ**: ઠંડા, સૂકા, કાચા, વાસી અને અતિ પ્રક્રિયા કરેલા ખોરાકથી બચો. બરફનું ઠંડું પાણી ન પીઓ.

#### 🧘 દૈનિક દિનચર્યા અને જીવનશૈલી (વિહાર)
* **જીવનશૈલી**: ખાવા અને સૂવાનો સમય ચોક્કસ રાખો. હૂંફાળા તલ અથવા નાળિયેરના તેલથી શરીર પર માલિશ (અભ્યંગ) કરો.
* **યોગ**: વજ્રાસન, બાલાસન, અને હળવા સૂર્ય નમસ્કાર.
* **પ્રાણાયામ**: રોજ ૧૦ મિનિટ નાડી શોધન (અનુલોમ-વિલોમ) કરો.
* **ઋતુચર્યા**: ઋતુ અનુસાર દિનચર્યા રાખો, ઠંડીમાં શરીર ગરમ રાખો અને ગરમીમાં ઠંડક તથા પ્રવાહી વધુ લો.

---

#### ⚠️ તબીબી ચેતવણી અને ડિસ્ક્લેમર
* **ગંભીર લક્ષણો**: જો તમને તીવ્ર દુખાવો, તીવ्र તાવ, અથવા મળમાં લોહી પડવા જેવી સમસ્યા થાય, તો તરત જ ડૉક્ટરનો સંપર્ક કરો.
* **ડિસ્ક્લેમર**: આ માહિતી માત્ર શૈક્ષણિક છે. કોઈપણ વિશેષ ઔષધિ લેતા પહેલા કૃપા કરીને BAMS લાયક આયુર્વેદિક ડૉક્ટરની સલાહ લો."""

        else:
            api_warning = f"\n*(Note: LLM API was not configured or hit an issue: {api_error}. Running in local Ayurvedic Heuristic Mode)*" if api_error else ""

            return f"""### 🌿 Ayurvedic Consultation Report{api_warning}

#### 📋 Clinical Diagnostic Summary
* **Possible Dosha**: {dosha} Dosha involved.
* **Prakriti Impact**: The current symptoms suggest an alteration in your baseline constitutional balance.
* **Possible Vikriti**: {vikriti} (Current imbalance state).
* **Clinical Reasoning**: The condition relates to the {explanation}
* **Ayurvedic Explanation**: Affected channels: {srotas}. Affected tissues: {dhatu}. Agni (digestive fire) status is likely impaired (sluggish or irregular). Possible Ama (digestive toxins) involvement is present.{ml_block}{web_block}

---

#### 🥗 Dietary Recommendations (Ahara)
* **Favor**: Warm, freshly prepared, and easily digestible foods. Add digestion-boosting spices like ginger, cumin, and fennel.
* **Avoid**: Cold, dry, raw, stale, and heavily processed food items. Avoid drinking ice-cold water.

#### 🧘 Daily Routine & Lifestyle (Vihara)
* **Lifestyle**: Establish a strict regular routine for eating and sleeping. Engage in warm self-massages (Abhyanga) using sesame or coconut oil.
* **Yoga**: Grounding postures like Vajrasana, child's pose (Balasana), and gentle sun salutations.
* **Pranayama**: Nadi Shodhana (Alternate nostril breathing) for 10 minutes daily.
* **Seasonal Advice**: Align your routine with the current season, staying warm during cold periods and keeping cool and hydrated during hot summers.

---

#### ⚠️ Medical Warning & Disclaimer
* **Red Flag Symptoms**: If you experience severe pain, high fever, or blood in stool, consult a physician immediately.
* **Disclaimer**: This information is educational only. Please consult a qualified BAMS Ayurvedic physician before taking any potent herbs.
"""
