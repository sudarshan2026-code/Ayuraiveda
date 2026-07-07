from backend.models.llm_client import AyurvedaLLMClient
from backend.prompts.system_prompt import AYURVEDIC_SYSTEM_PROMPT
from backend.prakriti_engine.prakriti_analyzer import PrakritiAnalyzer
from backend.dosha_engine.dosha_analyzer import DoshaAnalyzer
from backend.clinical_logic.reasoning_engine import ClinicalReasoningEngine
from backend.rag.rag_pipeline import RAGPipeline
from backend.memory.session_memory import SessionMemoryStore

class AyurvedicChatService:
    def __init__(self):
        self.llm_client = AyurvedaLLMClient()
        self.prakriti_analyzer = PrakritiAnalyzer()
        self.dosha_analyzer = DoshaAnalyzer()
        self.clinical_engine = ClinicalReasoningEngine()
        self.rag_pipeline = RAGPipeline()
        self.memory_store = SessionMemoryStore()

    def process_chat_message(self, session_id: str, message: str, user_profile: dict = None, language: str = 'en') -> dict:
        """Coordinated Ayurvedic workflow for multi-turn chats"""
        # Step 1: Detect Emergency Conditions
        if self.clinical_engine.check_emergency(message):
            emergency_resp = self.clinical_engine.get_emergency_message()
            # Still record to history for continuity
            self.memory_store.add_message(session_id, "user", message)
            self.memory_store.add_message(session_id, "assistant", emergency_resp)
            return {
                "response": emergency_resp,
                "prakriti": "Unknown",
                "vikriti": "Emergency Warning",
                "agni": "Unknown",
                "ama": "Unknown",
                "emergency": True
            }

        # Step 2: Get or create session
        session = self.memory_store.get_or_create_session(session_id)
        if user_profile:
            # Sync user profile fields (e.g. name, age, weight, height, prakriti)
            self.memory_store.update_user_context(session_id, user_profile)

        user_ctx = session["user_context"]
        history = self.memory_store.get_history(session_id)

        # Step 3: Prakriti baseline analysis
        prakriti_info = self.prakriti_analyzer.extract_user_prakriti(user_ctx)

        # Step 4: Vikriti & Active doshic imbalance analysis
        vikriti_info = self.dosha_analyzer.analyze_vikriti(message, history)

        # Step 5: Clinical pathology assessment (Dhatu, Srotas, Agni, Ama)
        pathology = self.clinical_engine.assess_pathology(message, vikriti_info)
        
        # Keep track of symptoms dynamically for multi-turn memory
        self.memory_store.record_symptoms(session_id, pathology["matched_lakshanas"])

        # Step 6: Retrieve Classical RAG References
        retrieved_refs = self.rag_pipeline.retrieve_references(message, top_k=2)

        # Step 7: Prompt Engineering - Compile Custom System Prompt
        # Inject retrieved verses, user Prakriti, and clinical history
        sys_prompt = AYURVEDIC_SYSTEM_PROMPT
        sys_prompt = sys_prompt.replace("[RETRIEVED_REFERENCES]", retrieved_refs)
        sys_prompt = sys_prompt.replace("[USER_PRAKRITI]", f"{prakriti_info['dominant_prakriti']} (Vata: {prakriti_info['vata_percentage']}%, Pitta: {prakriti_info['pitta_percentage']}%, Kapha: {prakriti_info['kapha_percentage']}%)")
        sys_prompt = sys_prompt.replace("[USER_METRICS]", f"Age: {user_ctx.get('age', 'N/A')}, Gender: {user_ctx.get('gender', 'N/A')}, Weight: {user_ctx.get('weight', 'N/A')} kg, Height: {user_ctx.get('height', 'N/A')} cm")
        
        active_sympt_str = ", ".join(list(session["symptoms_mentioned"])) if session["symptoms_mentioned"] else "None recorded yet"
        sys_prompt = sys_prompt.replace("[USER_HISTORY]", f"Active symptoms reported in this session: {active_sympt_str}")

        # Inject language instructions so the LLM responds in Hindi or Gujarati if selected
        lang_lbl = language.split('-')[0].lower()
        if lang_lbl == 'hi':
            sys_prompt += "\nIMPORTANT: The user has selected Hindi. You MUST write your entire response in clear, professional Hindi (हिंदी). Do not use English."
        elif lang_lbl == 'gu':
            sys_prompt += "\nIMPORTANT: The user has selected Gujarati. You MUST write your entire response in clear, professional Gujarati (ગુજરાતી). Do not use English."
        else:
            sys_prompt += "\nIMPORTANT: You must write your entire response in English."

        # Step 8: Generate LLM Response
        # Log query to session memory before LLM call
        self.memory_store.add_message(session_id, "user", message)
        
        assistant_response = self.llm_client.generate_response(sys_prompt, message, history, language=language)
        
        # Log response back to history
        self.memory_store.add_message(session_id, "assistant", assistant_response)

        # Return response with clinical state metadata for frontend sidebar
        return {
            "response": assistant_response,
            "prakriti": prakriti_info["dominant_prakriti"],
            "vikriti": vikriti_info["active_imbalance"],
            "agni": pathology["agni_state"],
            "ama": pathology["ama_status"],
            "emergency": False
        }
