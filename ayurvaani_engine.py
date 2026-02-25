"""
AyurVaani™ - The Ayurveda Knowledge Assistant
Powered by Tridosha Intelligence Engine™ + Groq LLM
Ancient Ayurveda, Explained with Modern Intelligence
"""

import re
from groq_client import GroqClient

class AyurVaaniEngine:
    """
    AyurVaani™ Chatbot Engine
    Hybrid AI: Rule-based Ayurveda + Groq LLM expansion
    """
    
    def __init__(self):
        self.knowledge_base = self._load_knowledge_base()
        self.intents = self._define_intents()
        self.groq_client = GroqClient()
    
    def chat(self, user_message):
        """Process user message and return enhanced Ayurveda response"""
        user_message_lower = user_message.lower().strip()
        
        # Detect intent
        intent = self._detect_intent(user_message_lower)
        
        # Get validated Ayurveda content
        validated_content = self._get_validated_content(intent, user_message_lower)
        
        # Expand with Groq LLM if available
        if self.groq_client.is_available():
            response = self.groq_client.expand_ayurveda_response(validated_content, user_message)
        else:
            response = validated_content
        
        return {
            'response': response,
            'intent': intent,
            'groq_enabled': self.groq_client.is_available()
        }
    
    def _detect_intent(self, message):
        """Detect user intent using keyword matching"""
        best_match = 'general'
        best_score = 0
        
        for intent, keywords in self.intents.items():
            score = sum(1 for keyword in keywords if keyword in message)
            if score > best_score:
                best_score = score
                best_match = intent
        
        return best_match if best_score > 0 else 'general'
    
    def _get_validated_content(self, intent, message):
        """Get validated Ayurveda content from knowledge base"""
        knowledge = self.knowledge_base.get(intent, {})
        
        # Find best matching content
        if isinstance(knowledge, dict):
            for key, value in knowledge.items():
                if any(word in message for word in key.split()):
                    return value
            return list(knowledge.values())[0] if knowledge else self.knowledge_base['general']['default']
        
        return knowledge if isinstance(knowledge, str) else self.knowledge_base['general']['default']
    
    def _define_intents(self):
        """Define intent keywords for NLP detection"""
        return {
            'vata': ['vata', 'air', 'space', 'movement', 'anxiety', 'dry', 'constipation', 'nervous'],
            'pitta': ['pitta', 'fire', 'water', 'heat', 'acidity', 'anger', 'inflammation', 'metabolism'],
            'kapha': ['kapha', 'earth', 'heavy', 'lazy', 'congestion', 'weight', 'mucus', 'lethargy'],
            'diet': ['food', 'eat', 'diet', 'nutrition', 'meal', 'hungry', 'appetite', 'pathya'],
            'yoga': ['yoga', 'asana', 'exercise', 'pose', 'stretch', 'physical'],
            'pranayama': ['pranayama', 'breathing', 'breath', 'anulom', 'sheetali', 'kapalabhati'],
            'sleep': ['sleep', 'insomnia', 'rest', 'tired', 'fatigue', 'wake'],
            'stress': ['stress', 'anxiety', 'worry', 'tension', 'mental', 'mind'],
            'digestion': ['digestion', 'stomach', 'agni', 'digestive', 'gut', 'intestine'],
            'season': ['season', 'monsoon', 'summer', 'winter', 'spring', 'autumn', 'ritucharya'],
            'daily': ['daily', 'routine', 'dinacharya', 'morning', 'evening', 'schedule'],
            'herbs': ['herb', 'ashwagandha', 'turmeric', 'tulsi', 'amla', 'neem', 'brahmi'],
            'prakriti': ['prakriti', 'constitution', 'body type', 'nature'],
            'agni': ['agni', 'digestive fire', 'metabolism'],
            'ama': ['ama', 'toxin', 'waste', 'undigested'],
            'ojas': ['ojas', 'immunity', 'vitality', 'strength', 'vigor'],
            'meditation': ['meditation', 'mindfulness', 'dhyana', 'calm', 'peace']
        }
    
    def _load_knowledge_base(self):
        """Comprehensive Ayurveda knowledge base"""
        return {
            'vata': {
                'what': "Vata Dosha is composed of Air and Space elements. It governs all movement in the body - circulation, breathing, nerve impulses, and elimination. Vata is responsible for creativity, enthusiasm, and mental agility.",
                'imbalance': "Vata imbalance manifests as anxiety, insomnia, dry skin, constipation, irregular appetite, restlessness, and scattered thoughts. Cold, dry, and windy conditions aggravate Vata.",
                'balance': "To balance Vata: Follow regular routines, eat warm cooked foods, practice oil massage (Abhyanga), maintain consistent sleep schedule, avoid cold and raw foods, practice grounding yoga poses, and stay warm.",
                'diet': "Vata-balancing diet includes warm soups, cooked grains, ghee, nuts, sweet fruits, root vegetables, and warming spices like ginger and cinnamon. Avoid cold drinks, raw salads, and dry foods."
            },
            'pitta': {
                'what': "Pitta Dosha is composed of Fire and Water elements. It governs digestion, metabolism, body temperature, and transformation. Pitta is responsible for intelligence, courage, and ambition.",
                'imbalance': "Pitta imbalance shows as acidity, heartburn, inflammation, skin rashes, anger, irritability, excessive heat, and perfectionism. Hot weather and spicy foods aggravate Pitta.",
                'balance': "To balance Pitta: Eat cooling foods, avoid excessive heat, practice moderation, maintain work-life balance, do cooling pranayama, avoid spicy and fried foods, and practice patience.",
                'diet': "Pitta-balancing diet includes cucumber, coconut, sweet fruits, leafy greens, milk, ghee, and cooling herbs like coriander and fennel. Avoid spicy, salty, and fried foods."
            },
            'kapha': {
                'what': "Kapha Dosha is composed of Water and Earth elements. It governs structure, lubrication, and stability in the body. Kapha provides strength, immunity, and emotional calmness.",
                'imbalance': "Kapha imbalance manifests as weight gain, lethargy, excessive sleep, congestion, depression, attachment, and resistance to change. Cold and damp conditions aggravate Kapha.",
                'balance': "To balance Kapha: Exercise regularly, wake early, eat light meals, use warming spices, avoid daytime sleep, practice vigorous yoga, and maintain active lifestyle.",
                'diet': "Kapha-balancing diet includes light foods, bitter and astringent tastes, warming spices like ginger and black pepper, leafy greens, and legumes. Avoid dairy, sweets, and heavy foods."
            },
            'diet': {
                'general': "Ayurveda emphasizes eating according to your Dosha, season, and digestive capacity (Agni). Eat freshly cooked meals, avoid incompatible food combinations, and eat mindfully in a calm environment.",
                'timing': "Eat your largest meal at midday when Agni is strongest. Have light breakfast and dinner. Avoid eating late at night. Leave 3-4 hours between meals for proper digestion.",
                'combinations': "Avoid incompatible combinations (Viruddha Ahara): milk with sour fruits, fish with milk, honey when heated, yogurt at night, and mixing hot and cold foods.",
                'seasonal': "Eat seasonal foods: cooling foods in summer, warming foods in winter, light foods in monsoon. This maintains harmony with nature's rhythms."
            },
            'yoga': {
                'vata': "Vata-balancing yoga: Gentle, grounding poses like Child Pose, Cat-Cow, Legs-up-the-wall, and slow Sun Salutations. Focus on stability and calmness.",
                'pitta': "Pitta-balancing yoga: Cooling poses like Moon Salutation, Forward Bends, Shoulder Stand, and Shavasana. Avoid excessive heat-building practices.",
                'kapha': "Kapha-balancing yoga: Energizing poses like Sun Salutation, Warrior poses, Backbends, and inversions. Practice with vigor and intensity.",
                'general': "Yoga in Ayurveda is about balancing Doshas through physical postures, breathing, and meditation. Practice according to your constitution and current imbalance."
            },
            'pranayama': {
                'anulom': "Anulom Vilom (Alternate Nostril Breathing): Balances both brain hemispheres, calms Vata, and promotes mental clarity. Practice 10-15 minutes daily.",
                'sheetali': "Sheetali Pranayama (Cooling Breath): Cools Pitta, reduces body heat, and calms anger. Curl tongue and inhale through it, exhale through nose.",
                'kapalabhati': "Kapalabhati (Skull Shining Breath): Energizes Kapha, clears congestion, and boosts metabolism. Forceful exhalations with passive inhalations.",
                'bhramari': "Bhramari (Bee Breath): Calms Vata and Pitta, reduces stress, and promotes mental peace. Make humming sound while exhaling.",
                'general': "Pranayama controls Prana (life force) through breath. Different techniques balance different Doshas and mental states."
            },
            'sleep': {
                'importance': "Sleep is when the body repairs and rejuvenates. Ayurveda recommends 7-8 hours of sleep, ideally from 10 PM to 6 AM, aligning with natural circadian rhythms.",
                'vata': "Vata types often have difficulty falling asleep. Establish regular bedtime, practice oil massage, drink warm milk with nutmeg, and avoid screens before bed.",
                'pitta': "Pitta types may wake in the middle of night. Keep bedroom cool, avoid spicy dinner, practice cooling pranayama, and meditate before sleep.",
                'kapha': "Kapha types tend to oversleep. Wake by 6 AM, avoid daytime naps, exercise regularly, and keep bedroom well-ventilated.",
                'tips': "Sleep tips: Consistent schedule, light dinner 3 hours before bed, warm bath, gentle yoga, avoid caffeine after 2 PM, and create dark, quiet environment."
            },
            'stress': {
                'ayurvedic': "Ayurveda views stress as Vata imbalance affecting the mind. It disrupts Prana flow and weakens Ojas (immunity). Chronic stress leads to disease.",
                'management': "Stress management: Regular routine, adequate sleep, meditation, pranayama, Abhyanga (oil massage), adaptogenic herbs like Ashwagandha, and mindful eating.",
                'herbs': "Stress-relieving herbs: Ashwagandha (adaptogen), Brahmi (mental clarity), Jatamansi (calming), Shankhpushpi (anxiety relief), and Tulsi (stress resilience).",
                'lifestyle': "Anti-stress lifestyle: Wake and sleep at same time, practice yoga daily, spend time in nature, maintain social connections, and avoid overstimulation."
            },
            'digestion': {
                'agni': "Agni (digestive fire) is central to Ayurveda. Strong Agni ensures proper digestion, absorption, and elimination. Weak Agni creates Ama (toxins).",
                'improve': "Improve Agni: Eat at regular times, avoid overeating, use digestive spices (ginger, cumin, fennel), drink warm water, and avoid cold drinks with meals.",
                'signs': "Strong Agni signs: Regular appetite, good energy, clear tongue, regular elimination, and mental clarity. Weak Agni: bloating, fatigue, coated tongue, and irregular bowels.",
                'tips': "Digestive tips: Eat largest meal at noon, avoid snacking, chew thoroughly, eat in calm environment, and walk 100 steps after meals."
            },
            'season': {
                'summer': "Summer increases Pitta. Eat cooling foods, avoid excessive sun, wear light colors, practice cooling pranayama, and stay hydrated with coconut water.",
                'monsoon': "Monsoon increases Vata and Kapha. Eat warm, light foods, use digestive spices, avoid daytime sleep, and maintain regular routine.",
                'winter': "Winter increases Kapha. Eat warming foods, exercise regularly, use heating spices, practice vigorous yoga, and avoid cold, heavy foods.",
                'spring': "Spring is Kapha season. Detoxify with light foods, bitter tastes, regular exercise, and avoid dairy and sweets.",
                'general': "Ritucharya (seasonal routine) aligns lifestyle with nature's cycles. Adjust diet, exercise, and daily routine according to season."
            },
            'daily': {
                'morning': "Ayurvedic morning routine (Dinacharya): Wake before sunrise, eliminate, scrape tongue, oil pull, brush teeth, drink warm water, practice yoga/pranayama, and meditate.",
                'evening': "Evening routine: Light dinner before sunset, gentle walk, avoid screens 1 hour before bed, practice calming pranayama, and sleep by 10 PM.",
                'general': "Dinacharya creates rhythm and stability. Regular routines balance Vata, strengthen Agni, and promote overall health and longevity.",
                'importance': "Daily routine is preventive medicine in Ayurveda. It maintains Dosha balance, supports natural body rhythms, and prevents disease."
            },
            'herbs': {
                'ashwagandha': "Ashwagandha: Adaptogen that reduces stress, improves strength, balances Vata, enhances immunity, and promotes restful sleep. Take with warm milk at night.",
                'turmeric': "Turmeric: Anti-inflammatory, purifies blood, supports liver, balances all Doshas, and promotes skin health. Use in cooking or with warm milk.",
                'tulsi': "Tulsi (Holy Basil): Adaptogen, immune booster, reduces stress, clears respiratory passages, and promotes mental clarity. Drink as tea.",
                'amla': "Amla: Rich in Vitamin C, cools Pitta, rejuvenates tissues, supports digestion, and promotes longevity. Eat fresh or as powder.",
                'brahmi': "Brahmi: Enhances memory, reduces anxiety, promotes mental clarity, balances Vata and Pitta, and supports nervous system. Take as tea or powder.",
                'neem': "Neem: Purifies blood, cools Pitta, supports skin health, boosts immunity, and has antimicrobial properties. Use internally and externally."
            },
            'prakriti': {
                'what': "Prakriti is your unique constitution determined at conception. It's your natural balance of Vata, Pitta, and Kapha that remains constant throughout life.",
                'importance': "Understanding Prakriti helps you make lifestyle choices aligned with your nature. It guides diet, exercise, career, and relationships for optimal health.",
                'types': "Seven Prakriti types: Vata, Pitta, Kapha (single Dosha dominant), Vata-Pitta, Pitta-Kapha, Vata-Kapha (dual Dosha), and Sama (balanced - rare).",
                'vikriti': "Vikriti is current state of imbalance. Treatment aims to bring Vikriti back to Prakriti through diet, lifestyle, herbs, and therapies."
            },
            'agni': {
                'types': "Four types of Agni: Sama (balanced), Vishama (irregular - Vata), Tikshna (sharp - Pitta), and Manda (slow - Kapha).",
                'importance': "Agni is the foundation of health. It digests food, emotions, and experiences. Strong Agni prevents Ama formation and maintains immunity.",
                'improve': "Strengthen Agni: Eat at regular times, use digestive spices, avoid overeating, fast occasionally, drink ginger tea, and maintain active lifestyle.",
                'signs': "Balanced Agni: Strong appetite at meal times, good energy, clear mind, healthy elimination, and pink tongue without coating."
            },
            'ama': {
                'what': "Ama is undigested food material that becomes toxic. It results from weak Agni and is the root cause of most diseases in Ayurveda.",
                'signs': "Ama signs: Thick tongue coating, bad breath, fatigue, heaviness, loss of appetite, body aches, and cloudy urine.",
                'remove': "Remove Ama: Fast or eat light foods, drink warm water with ginger, use digestive spices, practice gentle exercise, and avoid heavy, cold foods.",
                'prevent': "Prevent Ama: Eat according to Agni strength, avoid overeating, eat freshly cooked food, maintain regular meal times, and avoid incompatible food combinations."
            },
            'ojas': {
                'what': "Ojas is the essence of all tissues, representing immunity, vitality, and consciousness. It's the finest product of digestion and gives luster to body and mind.",
                'increase': "Increase Ojas: Eat fresh, wholesome foods, practice meditation, maintain celibacy or moderation, avoid stress, sleep well, and use rejuvenating herbs.",
                'foods': "Ojas-building foods: Ghee, milk, almonds, dates, saffron, honey, and fresh fruits. These are called Rasayana (rejuvenating) foods.",
                'importance': "Strong Ojas provides disease resistance, mental clarity, emotional stability, and longevity. Weak Ojas leads to frequent illness and low vitality."
            },
            'meditation': {
                'ayurvedic': "Meditation in Ayurveda calms Vata, balances Prana, strengthens Ojas, and promotes Sattva (mental clarity). It's essential for mental and spiritual health.",
                'practice': "Start with 5-10 minutes daily. Sit comfortably, focus on breath, observe thoughts without judgment, and gradually increase duration.",
                'benefits': "Benefits: Reduces stress, improves focus, balances emotions, enhances self-awareness, supports digestion, and promotes overall well-being.",
                'timing': "Best times: Early morning (Brahma Muhurta - 4-6 AM) or evening before sunset. Practice on empty stomach in quiet, clean space."
            },
            'general': {
                'default': "I'm AyurVaani™, your Ayurveda knowledge assistant. I can help you understand Ayurvedic concepts like Doshas, diet, yoga, pranayama, daily routines, and preventive health. Please ask me about any Ayurveda topic!",
                'greeting': "Namaste! I'm AyurVaani™, powered by Tridosha Intelligence Engine™. I'm here to share ancient Ayurvedic wisdom for your wellness journey. How may I assist you today?",
                'disclaimer': "Remember: This information is educational only. For personalized health advice, please consult a qualified Ayurvedic practitioner or healthcare professional."
            }
        }
