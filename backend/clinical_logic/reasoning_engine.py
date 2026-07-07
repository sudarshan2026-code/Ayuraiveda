import re

class ClinicalReasoningEngine:
    def __init__(self):
        # Emergency keywords
        self.emergency_keywords = [
            r"\bchest\s*pain\b", r"\bheart\s*attack\b", r"\bstroke\b", r"\bbreathing\s*diffic\b", 
            r"\bshortness\s*of\s*breath\b", r"\bsevere\s*bleed\b", r"\bloss\s*of\s*conscious\b", 
            r"\bpoison\b", r"\bparaly\b", r"\bspeech\s*diffic\b", r"\bsevere\s*head\s*injury\b"
        ]

    def check_emergency(self, query: str) -> bool:
        """Scan query for life-threatening emergency terms"""
        query_lower = query.lower()
        for pattern in self.emergency_keywords:
            if re.search(pattern, query_lower):
                return True
        return False

    def assess_pathology(self, query: str, vikriti: dict) -> dict:
        """Determines affected Dhatu, Srotas, Nidana, Lakshana matching, Agni, and Ama states"""
        query_lower = query.lower()
        
        # Default Vata pathology
        dhatu = "Rasa Dhatu (Plasma/Fluids)"
        srotas = "Annavaha Srotas (Digestive tract)"
        nidana = "Consumption of dry, cold, light foods, irregular routines, or excessive stress"
        lakshanas = ["irregular appetite", "constipation", "bloating", "nervousness"]
        agni = "Vishama Agni (Irregular/Variable)"
        ama = "Mild"

        if "acidity" in query_lower or "burn" in query_lower or "heat" in query_lower:
            dhatu = "Rakta Dhatu (Blood/Circulatory system)"
            srotas = "Annavaha Srotas & Purishavaha Srotas"
            nidana = "Excessive intake of spicy, sour, fried, or fermented foods, and exposure to intense heat"
            lakshanas = ["burning sensation", "heartburn", "acid reflux", "skin rashes"]
            agni = "Tikshna Agni (Sharp/Hyperactive)"
            ama = "Moderate"
        elif "congestion" in query_lower or "cough" in query_lower or "weight" in query_lower or "heavy" in query_lower:
            dhatu = "Meda Dhatu (Adipose/Fat tissue) & Rasa Dhatu"
            srotas = "Pranavaha Srotas (Respiratory channels) & Annavaha Srotas"
            nidana = "Excessive intake of sweet, oily, cold, heavy foods, sleeping during the day, or lack of exercise"
            lakshanas = ["lethargy", "heaviness in chest/stomach", "cough/mucus", "weight gain"]
            agni = "Manda Agni (Sluggish/Slow)"
            ama = "Moderate to High"

        return {
            "affected_dhatu": dhatu,
            "affected_srotas": srotas,
            "possible_nidana": nidana,
            "matched_lakshanas": lakshanas,
            "agni_state": agni,
            "ama_status": ama
        }

    def generate_recommendations(self, dominant_dosha: str) -> dict:
        """Returns structured advice for Ahara (Diet), Vihara (Lifestyle), Yoga, Pranayama, and Ritucharya"""
        d = dominant_dosha.lower()
        
        if "pitta" in d:
            return {
                "ahara_favor": ["Cooling, refreshing, sweet, bitter, and astringent foods", "Cucumbers, melons, leafy greens, coconut, ghee"],
                "ahara_avoid": ["Hot, spicy, sour, salty, and fermented foods", "Citrus, tomatoes, chili, vinegar, alcohol"],
                "vihara_lifestyle": ["Maintain work-life balance, stay cool, and spend time near water or under moonlight"],
                "yoga": ["Cooling poses: Moon Salutations (Chandra Namaskar), Child's Pose, Shavasana"],
                "pranayama": ["Sheetali (Cooling breath) or Sheetkari for 10 minutes"],
                "seasonal": ["In hot Summer (Grishma Ritu), drink coconut water, wear light clothes, and avoid midday sun"]
            }
        elif "kapha" in d:
            return {
                "ahara_favor": ["Light, warm, dry, and spicy foods", "Fresh ginger, turmeric, black pepper, leafy vegetables, lentils"],
                "ahara_avoid": ["Heavy, oily, sweet, cold, and dairy-rich foods", "Cheese, ice cream, wheat, cold water"],
                "vihara_lifestyle": ["Wake up early (before 6 AM), stay physically active, and avoid daytime sleeping"],
                "yoga": ["Stimulating/active poses: Sun Salutations (Surya Namaskar), Warrior series, Backbends"],
                "pranayama": ["Kapalabhati (Skull shining breath) or Bhastrika for metabolism stimulation"],
                "seasonal": ["In damp Spring (Vasanta Ritu), increase exercise, reduce heavy foods, and take warming ginger tea"]
            }
        else: # Vata or Sama
            return {
                "ahara_favor": ["Warm, freshly cooked, moist, and grounding meals", "Ghee, warm milk, sweet fruits, avocados, cooked grains"],
                "ahara_avoid": ["Cold, raw, dry, and light foods", "Salads, crackers, ice water, carbonated drinks, caffeine"],
                "vihara_lifestyle": ["Establish a consistent daily routine, practice warm oil massage (Abhyanga) daily"],
                "yoga": ["Grounding/stabilizing poses: Tadasana, Balasana, Legs-up-the-wall (Viparita Karani)"],
                "pranayama": ["Nadi Shodhana (Alternate nostril breathing) for calm nervous system support"],
                "seasonal": ["In cold/dry Autumn & Winter (Sharad & Hemanta Ritu), wear warm layers, avoid cold winds, and favor warm baths"]
            }
        
    def get_emergency_message(self) -> str:
        """Standard red flag message"""
        return """### 🚨 EMERGENCY MEDICAL NOTICE DETECTED

Our clinical filters have identified signs that may represent a medical emergency. 

**Immediate Action Required:**
* **Cease Ayurvedic consultation immediately.**
* **Go to the nearest emergency room or call local emergency services (like 911 / 112 / 102).**
* **Do not consume any herbs or delay professional emergency treatment.**

*Disclaimer: Ayurvedic consultations are for educational and preventive support only and cannot address medical emergencies.*"""
