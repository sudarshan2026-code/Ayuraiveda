"""
Simple PDF Knowledge Extractor with NLP
Works without external dependencies
"""

class SimplePDFKnowledge:
    """Fallback knowledge base with NLP capabilities"""
    
    def __init__(self):
        self.synonyms = {
            'vata': ['vata', 'air', 'wind', 'movement', 'nervous'],
            'pitta': ['pitta', 'fire', 'heat', 'metabolism', 'digestion', 'bile'],
            'kapha': ['kapha', 'water', 'earth', 'mucus', 'phlegm', 'structure'],
            'stress': ['stress', 'anxiety', 'tension', 'worry', 'nervous', 'anxious', 'worried'],
            'sleep': ['sleep', 'insomnia', 'rest', 'tired', 'fatigue', 'sleepless'],
            'digestion': ['digest', 'agni', 'stomach', 'gut', 'intestine', 'constipat', 'acidity', 'gas', 'bloat'],
            'diet': ['diet', 'food', 'eat', 'meal', 'nutrition', 'hungry'],
            'yoga': ['yoga', 'asana', 'exercise', 'pose', 'stretch', 'workout'],
            'pranayama': ['pranayam', 'breathing', 'breath', 'breathe'],
            'herbs': ['herb', 'medicine', 'remedy', 'ashwagandha', 'turmeric', 'tulsi', 'amla'],
            'history': ['invent', 'origin', 'history', 'start', 'founder', 'who created', 'who made', 'began'],
            'panchakarma': ['panchakarma', 'detox', 'cleanse', 'purif', 'therapy'],
            'prakriti': ['prakriti', 'constitution', 'body type', 'nature'],
            'daily': ['daily', 'routine', 'dinacharya', 'morning', 'schedule'],
            'season': ['season', 'summer', 'winter', 'spring', 'monsoon', 'ritucharya', 'autumn'],
            'sutrasthana': ['sutra', 'fundamental', 'principle', 'basic', 'theory', 'dhatu', 'tissue'],
            'food_combo': ['food combination', 'incompatible', 'viruddha', 'mix', 'combine']
        }
        self.knowledge = {
            'vata': """Vata Dosha (Air + Space): Governs all movement in the body including breathing, circulation, nerve impulses, and elimination. 
            
Characteristics: Dry, light, cold, rough, subtle, mobile, clear.

Imbalance Signs: Anxiety, fear, insomnia, constipation, dry skin, weight loss, tremors, irregular appetite, restlessness, scattered thoughts.

Balancing Diet: Warm, cooked, moist foods. Favor sweet, sour, salty tastes. Use ghee, oils, nuts, cooked grains, root vegetables, warm milk. Avoid cold, raw, dry foods.

Herbs: Ashwagandha (stress relief), Brahmi (mental clarity), Shatavari (nourishment), Bala (strength).

Lifestyle: Regular routine, adequate rest, oil massage (Abhyanga), warm baths, gentle exercise, meditation.""",

            'pitta': """Pitta Dosha (Fire + Water): Governs digestion, metabolism, body temperature, intelligence, and transformation.

Characteristics: Hot, sharp, light, liquid, spreading, oily.

Imbalance Signs: Acidity, heartburn, inflammation, skin rashes, anger, irritability, excessive body heat, perfectionism, impatience.

Balancing Diet: Cool, fresh foods. Favor sweet, bitter, astringent tastes. Use cucumber, coconut, sweet fruits, leafy greens, milk, ghee. Avoid spicy, salty, fried foods.

Herbs: Amla (cooling), Neem (blood purifier), Aloe vera (soothing), Shatavari (cooling tonic).

Lifestyle: Avoid excessive heat, practice moderation, cooling pranayama (Sheetali), meditation, avoid competitive activities.""",

            'kapha': """Kapha Dosha (Water + Earth): Governs structure, lubrication, stability, immunity, and strength.

Characteristics: Heavy, slow, cool, oily, smooth, dense, soft, stable.

Imbalance Signs: Weight gain, lethargy, excessive sleep, congestion, depression, attachment, resistance to change, slow digestion.

Balancing Diet: Light, warm, dry foods. Favor pungent, bitter, astringent tastes. Use ginger, turmeric, leafy greens, legumes, light grains. Avoid dairy, sweets, heavy foods.

Herbs: Trikatu (metabolism), Guggulu (weight management), Punarnava (detox), Tulsi (immunity).

Lifestyle: Wake early, regular vigorous exercise, avoid daytime sleep, stay active, practice energizing yoga and pranayama (Kapalabhati).""",

            'digestion': """Agni (Digestive Fire): Central concept in Ayurveda. Strong Agni ensures proper digestion, absorption, and elimination.

Improve Agni:
- Eat at regular times
- Use digestive spices: ginger, cumin, coriander, fennel, black pepper
- Avoid overeating (fill stomach 3/4 full)
- Drink warm water throughout day
- Walk 100 steps after meals
- Avoid cold drinks with meals
- Fast occasionally

For Constipation (Vata): Triphala, warm water, ghee, fiber-rich foods, oil massage.

For Acidity (Pitta): Amla, coconut water, cooling foods, avoid spicy/fried foods.

For Slow Digestion (Kapha): Ginger tea, light meals, avoid heavy/oily foods, regular exercise.""",

            'stress': """Ayurvedic Stress Management:

Stress is primarily Vata imbalance affecting the mind (Manas).

Herbs for Stress:
- Ashwagandha: Adaptogen, reduces cortisol, improves sleep
- Brahmi: Mental clarity, reduces anxiety
- Jatamansi: Calming, promotes restful sleep
- Shankhpushpi: Anxiety relief, memory enhancement
- Tulsi: Stress resilience, immunity

Practices:
- Regular daily routine (Dinacharya)
- Adequate sleep (10 PM - 6 AM)
- Meditation and mindfulness
- Pranayama: Anulom Vilom, Bhramari
- Abhyanga (oil massage)
- Avoid overstimulation
- Spend time in nature""",

            'sleep': """Ayurvedic Sleep Guidelines:

Optimal Sleep: 10 PM - 6 AM (aligns with natural circadian rhythms)

For Insomnia (Vata):
- Establish regular bedtime
- Warm oil massage before bed
- Warm milk with nutmeg, cardamom
- Avoid screens 1 hour before bed
- Practice calming pranayama
- Keep bedroom warm, dark, quiet

For Disturbed Sleep (Pitta):
- Keep bedroom cool
- Avoid spicy dinner
- Practice Sheetali pranayama
- Meditate before sleep
- Use cooling herbs: Brahmi, Jatamansi

For Excessive Sleep (Kapha):
- Wake by 6 AM
- Avoid daytime naps
- Regular exercise
- Light dinner
- Energizing morning routine""",

            'herbs': """Key Ayurvedic Herbs:

Ashwagandha (Withania somnifera): Adaptogen, stress relief, strength, immunity, sleep quality.

Turmeric (Curcuma longa): Anti-inflammatory, blood purifier, liver support, skin health.

Tulsi/Holy Basil (Ocimum sanctum): Adaptogen, immunity, respiratory health, stress relief.

Amla (Emblica officinalis): Vitamin C, cooling, rejuvenation, digestion, longevity.

Brahmi (Bacopa monnieri): Memory, mental clarity, anxiety relief, nervous system support.

Neem (Azadirachta indica): Blood purifier, skin health, immunity, antimicrobial.

Triphala: Three fruits blend - gentle detox, digestion, rejuvenation.

Shatavari (Asparagus racemosus): Cooling tonic, reproductive health, nourishment.""",

            'history': """History and Origins of Ayurveda:

Ayurveda wasn't invented by a single person - it evolved over 5000+ years through divine revelation and empirical observation.

**Origins:**
- Knowledge passed down orally by ancient Rishis (sages)
- Believed to be revealed by Lord Brahma (creator)
- Transmitted through Prajapati, Ashwini Kumaras, and Indra
- Sage Bharadwaja brought knowledge to earth

**Classical Texts:**
1. **Charaka Samhita** (1st-2nd century CE): Internal medicine, compiled by Charaka
2. **Sushruta Samhita** (6th century BCE): Surgery and anatomy, by Sushruta
3. **Ashtanga Hridaya** (7th century CE): Comprehensive text by Vagbhata

**Eight Branches (Ashtanga Ayurveda):**
1. Kaya Chikitsa (Internal Medicine)
2. Shalya Tantra (Surgery)
3. Shalakya Tantra (ENT & Ophthalmology)
4. Kaumara Bhritya (Pediatrics)
5. Agada Tantra (Toxicology)
6. Bhuta Vidya (Psychiatry)
7. Rasayana (Rejuvenation)
8. Vajikarana (Reproductive health)

Ayurveda is one of the world's oldest holistic healing systems, recognized by WHO.""",

            'panchakarma': """Panchakarma - Five Purification Therapies:

Panchakarma is Ayurveda's deep detoxification and rejuvenation therapy.

**Five Main Procedures:**

1. **Vamana (Therapeutic Vomiting):**
   - Eliminates excess Kapha
   - For respiratory issues, skin diseases
   - Done under supervision

2. **Virechana (Purgation):**
   - Eliminates excess Pitta
   - For liver, skin, digestive issues
   - Uses herbal laxatives

3. **Basti (Medicated Enema):**
   - Eliminates excess Vata
   - Most powerful therapy
   - Uses herbal decoctions or oils

4. **Nasya (Nasal Administration):**
   - Clears head, neck region
   - For sinusitis, headaches, mental clarity
   - Herbal oils through nose

5. **Raktamokshana (Bloodletting):**
   - Purifies blood
   - For skin diseases, inflammation
   - Rarely used today

**Preparatory Procedures:**
- Snehana (oleation/oil massage)
- Swedana (steam therapy)

**Benefits:** Deep detox, rejuvenation, disease prevention, enhanced immunity.

**Note:** Must be done under qualified Ayurvedic practitioner supervision.""",

            'prakriti': """Prakriti - Your Ayurvedic Constitution:

Prakriti is your unique mind-body constitution determined at conception. It remains constant throughout life.

**Seven Prakriti Types:**
1. Vata Prakriti (Vata dominant)
2. Pitta Prakriti (Pitta dominant)
3. Kapha Prakriti (Kapha dominant)
4. Vata-Pitta (dual dosha)
5. Pitta-Kapha (dual dosha)
6. Vata-Kapha (dual dosha)
7. Sama Prakriti (balanced - rare)

**Determining Prakriti:**
- Physical characteristics
- Mental tendencies
- Digestive patterns
- Sleep patterns
- Stress response

**Importance:**
- Guides personalized diet
- Determines suitable lifestyle
- Predicts disease susceptibility
- Helps career/relationship choices

**Vikriti vs Prakriti:**
- Prakriti = Natural constitution (unchanging)
- Vikriti = Current state (imbalanced)
- Treatment aims to bring Vikriti back to Prakriti

Knowing your Prakriti is key to preventive health in Ayurveda.""",

            'daily_routine': """Dinacharya - Ayurvedic Daily Routine:

**Morning (Brahma Muhurta - 4-6 AM):**
- Wake before sunrise
- Eliminate (bowels, bladder)
- Scrape tongue (removes Ama)
- Oil pulling (Gandusha) - 5-10 min
- Brush teeth with herbal powder
- Drink warm water (cleanses system)
- Self-massage (Abhyanga) with oil
- Bath
- Yoga/Exercise
- Pranayama (15-20 min)
- Meditation (10-20 min)
- Light breakfast

**Midday:**
- Main meal at noon (Agni strongest)
- Brief rest after lunch
- Work/activities

**Evening:**
- Light exercise/walk
- Light dinner before sunset
- Avoid screens 1 hour before bed
- Calming activities
- Foot massage
- Sleep by 10 PM

**Benefits:**
- Balances doshas
- Strengthens Agni
- Prevents disease
- Enhances energy
- Promotes longevity

Regular routine is preventive medicine in Ayurveda.""",

            'sutrasthana': """Ashtanga Hridaya Sutrasthana (Fundamental Principles):

**Chapter 1 - Ayurveda Basics:**
Ayurveda aims to maintain health of healthy and cure diseases of sick. Life (Ayu) is combination of body, senses, mind, and soul.

**Tridosha Theory:**
- Vata: Governs all movement, made of Air + Space
- Pitta: Governs transformation, made of Fire + Water  
- Kapha: Governs structure, made of Water + Earth

**Sapta Dhatu (Seven Tissues):**
1. Rasa (Plasma)
2. Rakta (Blood)
3. Mamsa (Muscle)
4. Meda (Fat)
5. Asthi (Bone)
6. Majja (Marrow)
7. Shukra (Reproductive tissue)

**Agni (Digestive Fire):**
Central to health. 13 types of Agni in body. Jatharagni (main digestive fire) most important.

**Ama (Toxins):**
Undigested food becomes toxic Ama. Root cause of disease. Remove through proper diet, fasting, Panchakarma.

**Ojas (Vital Essence):**
Final product of perfect digestion. Provides immunity, strength, luster. Protect Ojas through proper lifestyle.

**Srotas (Channels):**
Body has numerous channels for transport. Keep channels clear for health.

**Prakriti (Constitution):**
Unique combination of doshas at birth. Determines physical, mental characteristics.

**Vikriti (Current State):**
Current dosha imbalance. Treatment brings Vikriti back to Prakriti.""",

            'food_combinations': """Incompatible Food Combinations (Viruddha Ahara) - Ashtanga Hridaya:

**Avoid These Combinations:**

1. **Milk with:**
   - Sour fruits (citrus, berries)
   - Fish or meat
   - Salt
   - Yogurt
   - Bananas (causes heaviness)

2. **Honey:**
   - Never heat honey (becomes toxic)
   - Not with hot water
   - Not equal quantity with ghee

3. **Yogurt:**
   - Not at night
   - Not with milk
   - Not with hot foods
   - Not with fruits

4. **Fruits:**
   - Eat alone, not with meals
   - Melons eat separately
   - Not with dairy (except dates, raisins)

5. **Nightshades:**
   - Not with dairy
   - Not with cucumber

6. **Hot and Cold:**
   - Don't mix hot and cold foods
   - Ice cream after hot meal harmful

**Why Avoid:**
- Creates Ama (toxins)
- Weakens Agni
- Causes digestive issues
- Leads to disease over time

**Safe Combinations:**
- Rice with mung dal
- Ghee with most foods
- Cooked vegetables with grains
- Spices with appropriate foods""",

            'seasonal_routine': """Ritucharya (Seasonal Routine) - Ashtanga Hridaya:

**Six Seasons in Ayurveda:**

1. **Shishira (Late Winter - Jan/Feb):**
   - Kapha accumulates
   - Diet: Heavy, nourishing foods; ghee, oils
   - Lifestyle: Oil massage, warm baths

2. **Vasanta (Spring - Mar/Apr):**
   - Kapha aggravates
   - Diet: Light, dry, pungent foods
   - Lifestyle: Exercise, avoid daytime sleep
   - Panchakarma: Vamana (emesis)

3. **Grishma (Summer - May/Jun):**
   - Pitta accumulates, Vata increases
   - Diet: Sweet, cold, liquid foods
   - Lifestyle: Avoid sun, stay cool
   - Drinks: Coconut water, buttermilk

4. **Varsha (Monsoon - Jul/Aug):**
   - All doshas aggravate
   - Diet: Warm, light, easily digestible
   - Lifestyle: Avoid dampness
   - Use: Digestive spices

5. **Sharad (Autumn - Sep/Oct):**
   - Pitta aggravates
   - Diet: Sweet, bitter, astringent
   - Lifestyle: Avoid sun exposure
   - Panchakarma: Virechana (purgation)

6. **Hemanta (Early Winter - Nov/Dec):**
   - Vata decreases, Agni strong
   - Diet: Nourishing, heavy foods
   - Lifestyle: Oil massage, exercise

**Key Principle:**
Adjust diet and lifestyle with seasons to prevent disease.""",

            'yoga': """Yoga in Ayurveda:

Yoga and Ayurveda are sister sciences. Yoga balances doshas through physical postures, breathing, and meditation.

**Vata-Balancing Yoga:**
- Gentle, grounding poses
- Slow, mindful movements
- Poses: Child pose, Cat-Cow, Legs-up-wall, Seated forward bend
- Focus on stability and calmness
- Avoid excessive jumping/vinyasa

**Pitta-Balancing Yoga:**
- Cooling, moderate intensity
- Moon salutations
- Poses: Forward bends, Shoulder stand, Fish pose, Shavasana
- Avoid excessive heat-building
- Practice with patience, not competition

**Kapha-Balancing Yoga:**
- Energizing, vigorous practice
- Sun salutations (multiple rounds)
- Poses: Warrior series, Backbends, Inversions, Twists
- Build heat and energy
- Practice with intensity

**Best Time:**
- Morning (6-8 AM) for Kapha
- Evening (5-7 PM) for Vata/Pitta

**Benefits:** Flexibility, strength, mental clarity, dosha balance, stress relief.""",

            'pranayama': """Pranayama - Breath Control:

Pranayama controls Prana (life force) through breath. Different techniques balance different doshas.

**Key Practices:**

1. **Anulom Vilom (Alternate Nostril):**
   - Balances both brain hemispheres
   - Calms Vata, balances all doshas
   - 10-15 minutes daily

2. **Sheetali (Cooling Breath):**
   - Cools Pitta, reduces body heat
   - Curl tongue, inhale through it
   - Exhale through nose

3. **Kapalabhati (Skull Shining):**
   - Energizes Kapha
   - Forceful exhalations, passive inhalations
   - Clears congestion, boosts metabolism

4. **Bhramari (Bee Breath):**
   - Calms Vata and Pitta
   - Humming sound while exhaling
   - Reduces stress, promotes peace

5. **Bhastrika (Bellows Breath):**
   - Energizing, warming
   - Good for Kapha
   - Forceful inhalations and exhalations

**Benefits:** Stress relief, mental clarity, dosha balance, improved lung capacity, enhanced Prana flow.

**Practice:** Empty stomach, morning or evening, in clean air."""
        }
    
    def get_answer(self, query):
        """Get comprehensive answer from knowledge base"""
        query_lower = query.lower()
        
        # Detect intent
        intent = self._detect_intent_nlp(query_lower)
        
        # Return full knowledge for detected intent
        if intent and intent in self.knowledge:
            return self._format_response(self.knowledge[intent], query)
        elif intent == 'diet':
            return self._handle_diet_query(query_lower)
        elif intent == 'season':
            return self._handle_seasonal_query(query_lower)
        else:
            # Search all knowledge for relevant content
            return self._search_all_knowledge(query_lower)
    
    def _search_all_knowledge(self, query):
        """Search all knowledge base for relevant information"""
        results = []
        for topic, content in self.knowledge.items():
            if any(word in content.lower() for word in query.split() if len(word) > 3):
                results.append(content)
        
        if results:
            return self._format_response(results[0], query)
        
        return """I can provide detailed information about all aspects of Ayurveda. Ask me anything about doshas, treatments, herbs, diet, yoga, pranayama, history, or any Ayurvedic concept!"""
    
    def _detect_intent_nlp(self, query):
        """NLP-based intent detection using synonym matching and scoring"""
        scores = {}
        
        # Score each intent based on synonym matches
        for intent, synonyms in self.synonyms.items():
            score = sum(1 for syn in synonyms if syn in query)
            if score > 0:
                scores[intent] = score
        
        # Return intent with highest score
        if scores:
            return max(scores, key=scores.get)
        return None
    
    def _format_response(self, knowledge, query):
        """Format knowledge as conversational response without chapter references"""
        # Remove chapter/section references
        import re
        knowledge = re.sub(r'Chapter\s+\d+[:\s-]*', '', knowledge, flags=re.IGNORECASE)
        knowledge = re.sub(r'According to Ashtanga Hridaya[:\s-]*', '', knowledge, flags=re.IGNORECASE)
        knowledge = re.sub(r'Ashtanga Hridaya Sutrasthana[^:]*:', '', knowledge, flags=re.IGNORECASE)
        knowledge = re.sub(r'\*\*Chapter.*?:\*\*', '', knowledge)
        
        # Clean up extra whitespace
        knowledge = re.sub(r'\n\s*\n', '\n\n', knowledge)
        knowledge = knowledge.strip()
        
        return knowledge
    
    def _handle_diet_query(self, query):
        """Handle diet-related queries with context"""
        response = "Based on your query, here are Ayurvedic dietary recommendations:\n\n"
        
        # Check for spicy food mention
        if 'spicy' in query:
            response += """🔥 Since you're eating spicy foods, this increases Pitta dosha (heat in body). Here's what to do:

**Immediate Actions:**
- Reduce or avoid spicy, fried, salty foods
- Increase cooling foods: cucumber, coconut water, sweet fruits (melons, grapes)
- Drink plenty of water, coconut water, or cooling herbal teas
- Add cooling spices: coriander, fennel, cardamom

**Summer Diet (Pitta Season):**
- Favor: Sweet, bitter, astringent tastes
- Best foods: Leafy greens, cucumber, zucchini, sweet fruits, milk, ghee
- Drinks: Coconut water, mint water, rose water, aloe vera juice
- Avoid: Spicy, salty, sour, fried foods; alcohol; caffeine

**Cooling Herbs:** Amla, Neem, Aloe vera, Coriander

**Lifestyle:** Avoid midday sun, wear light colors, practice cooling pranayama (Sheetali)

This will help balance excess Pitta and keep you cool!"""
        
        elif 'summer' in query:
            response += """☀️ Summer Diet (Pitta-Balancing):

Summer increases Pitta dosha, so focus on cooling foods:

**Best Foods:**
- Fruits: Watermelon, melons, grapes, sweet berries, coconut
- Vegetables: Cucumber, zucchini, leafy greens, asparagus
- Grains: Rice, wheat, oats, barley
- Dairy: Milk, ghee, fresh butter (cooling)
- Proteins: Mung beans, chickpeas (in moderation)

**Best Drinks:**
- Coconut water, mint water, rose water
- Cooling herbal teas: coriander, fennel, mint
- Fresh fruit juices (not citrus)

**Avoid:**
- Spicy, salty, sour, fried foods
- Hot beverages, alcohol, caffeine
- Garlic, onions, chilies, tomatoes (in excess)

**Cooling Spices:** Coriander, fennel, cardamom, mint, rose

Eat light meals, stay hydrated, and avoid eating during peak heat hours!"""
        
        elif 'winter' in query:
            response += """❄️ Winter Diet (Vata & Kapha-Balancing):

Winter increases Vata and Kapha, so focus on warm, nourishing foods:

**Best Foods:**
- Warm soups, stews, cooked grains
- Root vegetables: sweet potato, carrots, beets
- Warming spices: ginger, cinnamon, black pepper, turmeric
- Ghee, sesame oil, nuts, seeds
- Warm milk with spices

**Best Drinks:**
- Ginger tea, cinnamon tea, herbal teas
- Warm water with lemon and honey
- Golden milk (turmeric milk)

**Avoid:**
- Cold, raw foods and drinks
- Excessive dairy and sweets (increases Kapha)
- Dry, light foods (increases Vata)

**Warming Spices:** Ginger, black pepper, cinnamon, cloves, cardamom

Eat warm, cooked meals and maintain regular meal times!"""
        
        else:
            response += """**General Ayurvedic Diet Principles:**

1. **Eat According to Your Dosha:**
   - Vata: Warm, moist, grounding foods
   - Pitta: Cool, fresh, mild foods
   - Kapha: Light, warm, spicy foods

2. **Meal Timing:**
   - Breakfast: Light (7-8 AM)
   - Lunch: Largest meal (12-1 PM when Agni is strongest)
   - Dinner: Light, early (6-7 PM)

3. **Food Combinations (Avoid):**
   - Milk with sour fruits, fish, or meat
   - Honey when heated
   - Yogurt at night
   - Hot and cold foods together

4. **Eating Habits:**
   - Eat in calm environment
   - Chew thoroughly
   - Fill stomach 3/4 full
   - Drink warm water with meals

5. **Six Tastes (Include Daily):**
   Sweet, Sour, Salty, Pungent, Bitter, Astringent

Would you like specific recommendations for your dosha or season?"""
        
        return response
    
    def _handle_seasonal_query(self, query):
        """Handle seasonal routine queries"""
        return self._format_response(self.knowledge['seasonal_routine'], query)
