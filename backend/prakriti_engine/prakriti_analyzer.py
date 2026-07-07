class PrakritiAnalyzer:
    def __init__(self):
        pass

    def extract_user_prakriti(self, user_context: dict) -> dict:
        """Parses user profile and assessment history to extract baseline Prakriti details"""
        prakriti = user_context.get("prakriti", "Unknown (Assessment pending)")
        
        # If user has past assessment scores
        scores = user_context.get("prakriti_scores", {"vata": 33.3, "pitta": 33.3, "kapha": 33.3})
        
        return {
            "dominant_prakriti": prakriti,
            "vata_percentage": scores.get("vata", 33.3),
            "pitta_percentage": scores.get("pitta", 33.3),
            "kapha_percentage": scores.get("kapha", 33.3)
        }
