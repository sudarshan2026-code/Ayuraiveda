class DoshaAnalyzer:
    def __init__(self):
        # Maps keywords in query to active doshic imbalances
        self.symptom_mapping = {
            "vata": [
                "constipation", "dry", "rough", "bloating", "gas", "anxiety", "insomnia", 
                "cracking joints", "cold hands", "shivering", "stiffness", "low sleep", "pain"
            ],
            "pitta": [
                "acidity", "burning", "heartburn", "ulcer", "rash", "acne", "inflammation", 
                "fever", "sweating", "heat", "hot", "irritability", "anger", "moles"
            ],
            "kapha": [
                "congestion", "mucus", "weight gain", "heaviness", "lethargy", "sluggish", 
                "slow", "water retention", "swelling", "oversleeping", "attachment", "greasy"
            ]
        }

    def analyze_vikriti(self, query: str, conversation_history: list = None) -> dict:
        """Parses current query and chat history to identify active dosha aggravation and Vikriti state"""
        query_text = query.lower()
        if conversation_history:
            for message in conversation_history:
                if message.get("role") == "user":
                    query_text += " " + message.get("content", "").lower()

        vata_hits = sum(1 for word in self.symptom_mapping["vata"] if word in query_text)
        pitta_hits = sum(1 for word in self.symptom_mapping["pitta"] if word in query_text)
        kapha_hits = sum(1 for word in self.symptom_mapping["kapha"] if word in query_text)

        total_hits = vata_hits + pitta_hits + kapha_hits
        if total_hits == 0:
            return {
                "active_imbalance": "Balanced State (Sama)",
                "vata_aggravation": 0.0,
                "pitta_aggravation": 0.0,
                "kapha_aggravation": 0.0
            }

        return {
            "active_imbalance": (
                "Vata Aggravation" if vata_hits >= pitta_hits and vata_hits >= kapha_hits else
                "Pitta Aggravation" if pitta_hits >= vata_hits and pitta_hits >= kapha_hits else
                "Kapha Aggravation"
            ),
            "vata_aggravation": round((vata_hits / total_hits) * 100, 1),
            "pitta_aggravation": round((pitta_hits / total_hits) * 100, 1),
            "kapha_aggravation": round((kapha_hits / total_hits) * 100, 1)
        }
