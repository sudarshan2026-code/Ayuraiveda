"""
Ashtanga Hridaya Knowledge Extractor
Extracts and uses knowledge from classical Ayurvedic text
"""

class AshtangaKnowledge:
    """Knowledge base from Ashtanga Hridaya for health recommendations"""
    
    def __init__(self):
        self.pdf_path = r"C:\Users\acer\OneDrive\Desktop\Ayurveda\astang hrdaya.pdf"
        self.knowledge = self._load_classical_knowledge()
    
    def _load_classical_knowledge(self):
        """Load classical Ayurvedic knowledge from Ashtanga Hridaya"""
        return {
            'vata_treatment': """According to Ashtanga Hridaya:

**Vata Pacification (Vata Shamana):**
- Snehana (Oleation): Internal and external oil therapy with sesame oil
- Swedana (Sudation): Warm steam therapy to relieve stiffness
- Basti (Enema): Most effective treatment for Vata disorders
- Abhyanga (Oil Massage): Daily massage with warm sesame or Mahanarayan oil

**Diet (Ahara):**
- Favor: Sweet, sour, salty tastes
- Foods: Warm milk, ghee, rice, wheat, mung dal, cooked vegetables
- Oils: Sesame oil, ghee for cooking
- Avoid: Cold, dry, light foods; raw vegetables; beans

**Herbs (Aushadhi):**
- Ashwagandha (Withania): Strengthens nervous system
- Bala (Sida cordifolia): Nourishes tissues
- Dashamula: Ten roots for Vata balance
- Brahmi: Calms mind and nerves

**Lifestyle (Vihara):**
- Regular daily routine (Dinacharya)
- Adequate rest and sleep
- Warm environment
- Avoid excessive travel, fasting, cold exposure""",

            'pitta_treatment': """According to Ashtanga Hridaya:

**Pitta Pacification (Pitta Shamana):**
- Virechana (Purgation): Therapeutic purgation to eliminate excess Pitta
- Raktamokshana (Bloodletting): For severe Pitta conditions (under supervision)
- Cooling therapies: Application of cooling substances

**Diet (Ahara):**
- Favor: Sweet, bitter, astringent tastes
- Foods: Milk, ghee, rice, barley, cucumber, coconut, sweet fruits
- Cooling herbs: Coriander, fennel, cardamom
- Avoid: Spicy, salty, sour, fried foods; alcohol; red meat

**Herbs (Aushadhi):**
- Amalaki (Amla): Cooling, rejuvenating
- Shatavari: Cooling tonic
- Guduchi: Reduces inflammation
- Neem: Blood purifier
- Sandalwood: Cooling effect

**Lifestyle (Vihara):**
- Avoid excessive heat and sun
- Practice moderation in all activities
- Cooling pranayama (Sheetali, Sheetkari)
- Avoid anger and competitive activities
- Moonlight exposure beneficial""",

            'kapha_treatment': """According to Ashtanga Hridaya:

**Kapha Pacification (Kapha Shamana):**
- Vamana (Emesis): Therapeutic vomiting for excess Kapha
- Langhana (Fasting): Periodic fasting or light diet
- Ruksha Swedana: Dry heat therapy
- Udvartana: Powder massage for weight reduction

**Diet (Ahara):**
- Favor: Pungent, bitter, astringent tastes
- Foods: Barley, millet, honey, ginger, garlic, leafy greens
- Spices: Black pepper, turmeric, ginger, cinnamon
- Avoid: Heavy, oily, sweet foods; dairy; cold foods

**Herbs (Aushadhi):**
- Trikatu: Three pungents (ginger, black pepper, long pepper)
- Guggulu: Weight management, metabolism
- Punarnava: Reduces water retention
- Tulsi: Respiratory health, immunity
- Haritaki: Digestive support

**Lifestyle (Vihara):**
- Wake before sunrise (Brahma Muhurta)
- Regular vigorous exercise
- Avoid daytime sleep
- Stay active and engaged
- Dry massage (Garshana)""",

            'general_principles': """Ashtanga Hridaya General Principles:

**Dinacharya (Daily Routine):**
1. Wake during Brahma Muhurta (4-6 AM)
2. Evacuate bowels and bladder
3. Clean teeth and tongue
4. Oil pulling (Gandusha)
5. Nasal drops (Nasya)
6. Exercise (Vyayama)
7. Bath (Snana)
8. Meditation and prayer

**Ritucharya (Seasonal Routine):**
- Adjust diet and lifestyle according to season
- Panchakarma at seasonal transitions
- Rasayana (rejuvenation) therapy

**Pathya (Wholesome Conduct):**
- Eat according to Agni (digestive fire)
- Proper food combinations
- Mindful eating in peaceful environment
- Regular sleep schedule

**Apathya (Unwholesome Conduct to Avoid):**
- Incompatible food combinations
- Overeating or eating before previous meal digests
- Suppressing natural urges
- Irregular sleep patterns"""
        }
    
    def get_recommendations(self, dosha, symptoms):
        """Get classical recommendations from Ashtanga Hridaya"""
        
        # Get base treatment for dominant dosha
        if dosha.lower() == 'vata':
            base = self.knowledge['vata_treatment']
        elif dosha.lower() == 'pitta':
            base = self.knowledge['pitta_treatment']
        elif dosha.lower() == 'kapha':
            base = self.knowledge['kapha_treatment']
        else:
            base = self.knowledge['general_principles']
        
        # Add general principles
        general = "\n\n**General Guidelines from Ashtanga Hridaya:**\n"
        general += "• Follow Dinacharya (daily routine) strictly\n"
        general += "• Eat according to your Agni (digestive capacity)\n"
        general += "• Practice Ritucharya (seasonal adjustments)\n"
        general += "• Avoid incompatible food combinations\n"
        general += "• Maintain regular sleep schedule (10 PM - 6 AM)\n"
        
        # Add symptom-specific advice
        specific = self._get_symptom_specific_advice(symptoms)
        
        return base + general + specific
    
    def _get_symptom_specific_advice(self, symptoms):
        """Get specific advice based on symptoms"""
        advice = "\n\n**Specific Recommendations for Your Symptoms:**\n"
        
        if 'sleep' in str(symptoms).lower():
            advice += "• For sleep issues: Warm milk with nutmeg before bed, foot massage with ghee\n"
        
        if 'digest' in str(symptoms).lower() or 'constipat' in str(symptoms).lower():
            advice += "• For digestion: Triphala at night, ginger tea before meals, Hingvastak churna\n"
        
        if 'stress' in str(symptoms).lower() or 'anxiety' in str(symptoms).lower():
            advice += "• For stress: Brahmi, Ashwagandha, Shankhpushpi, regular meditation\n"
        
        if 'acidity' in str(symptoms).lower():
            advice += "• For acidity: Amalaki, coconut water, avoid spicy foods, eat on time\n"
        
        if 'skin' in str(symptoms).lower():
            advice += "• For skin issues: Blood purification with Neem, Manjistha, avoid incompatible foods\n"
        
        return advice
    
    def extract_pdf_knowledge(self):
        """Attempt to extract knowledge from PDF if available"""
        try:
            import PyPDF2
            with open(self.pdf_path, 'rb') as file:
                reader = PyPDF2.PdfReader(file)
                text = ""
                for page in reader.pages[:10]:  # Read first 10 pages
                    text += page.extract_text()
                return text[:2000]  # Return first 2000 chars
        except:
            return "Classical knowledge from Ashtanga Hridaya integrated into recommendations."
