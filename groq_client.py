"""
Groq LLM Client for AyurVaani™
Secure API integration with environment variable handling
"""

import os

class GroqClient:
    """
    Groq LLM integration for natural language expansion
    Used ONLY for formatting validated Ayurveda knowledge
    """
    
    def __init__(self):
        self.api_key = os.environ.get('GROQ_API_KEY', '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')
        self.client = None
        
        if self.api_key:
            try:
                from groq import Groq
                self.client = Groq(api_key=self.api_key)
            except Exception as e:
                print(f"Groq initialization warning: {e}")
                self.client = None
    
    def expand_ayurveda_response(self, validated_content, user_query):
        """
        Expand validated Ayurveda content using Groq LLM
        Falls back to original content if Groq unavailable
        """
        if not self.client:
            return validated_content
        
        try:
            system_prompt = """You are AyurVaani™, an Ayurveda knowledge assistant powered by Tridosha Intelligence Engine™.

STRICT RULES:
- Expand ONLY the provided validated Ayurvedic content
- Use clear, educational, respectful language
- Never diagnose diseases or prescribe medicines
- Never add medical claims beyond provided content
- Always maintain preventive and educational tone
- Keep responses concise (200-300 words)
- Use simple language suitable for students

Your role is to make ancient Ayurvedic wisdom accessible and understandable."""

            user_prompt = f"""User asked: "{user_query}"

Validated Ayurvedic Knowledge:
{validated_content}

Expand this Ayurvedic explanation in a clear, educational manner. Stay strictly within the provided knowledge. Do not add diagnosis or medication advice."""

            response = self.client.chat.completions.create(
                model="llama-3.1-70b-versatile",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.3,
                max_tokens=500,
                top_p=0.9
            )
            
            return response.choices[0].message.content.strip()
        
        except Exception as e:
            print(f"Groq API error: {e}")
            return validated_content
    
    def is_available(self):
        """Check if Groq client is available"""
        return self.client is not None
