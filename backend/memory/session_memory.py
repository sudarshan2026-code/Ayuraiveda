class SessionMemoryStore:
    def __init__(self):
        # Maps session_id or user_id to session details
        self.sessions = {}

    def get_or_create_session(self, session_id: str, default_user_context: dict = None) -> dict:
        """Retrieves or creates memory store for a given session"""
        if session_id not in self.sessions:
            self.sessions[session_id] = {
                "history": [],
                "user_context": default_user_context or {
                    "name": "Anonymous Patient",
                    "age": "Unknown",
                    "gender": "Unknown",
                    "weight": "Unknown",
                    "height": "Unknown",
                    "prakriti": "Unknown (Assessment pending)",
                    "prakriti_scores": {"vata": 33.3, "pitta": 33.3, "kapha": 33.3}
                },
                "symptoms_mentioned": set(),
                "last_recommendations": []
            }
        return self.sessions[session_id]

    def add_message(self, session_id: str, role: str, content: str):
        """Appends a new turn to the conversation history"""
        session = self.get_or_create_session(session_id)
        session["history"].append({"role": role, "content": content})
        
        # Keep history within reasonable window (e.g. last 15 turns) to prevent context blowup
        if len(session["history"]) > 15:
            session["history"] = session["history"][-15:]

    def update_user_context(self, session_id: str, user_data: dict):
        """Updates static user indicators (prakriti, age, gender)"""
        session = self.get_or_create_session(session_id)
        session["user_context"].update(user_data)

    def record_symptoms(self, session_id: str, symptoms: list):
        """Updates running set of mentioned symptoms for multi-turn tracking"""
        session = self.get_or_create_session(session_id)
        for s in symptoms:
            session["symptoms_mentioned"].add(s)

    def get_history(self, session_id: str) -> list:
        """Retrieves raw history array"""
        session = self.get_or_create_session(session_id)
        return session["history"]
