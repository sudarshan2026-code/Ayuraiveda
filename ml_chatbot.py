import PyPDF2
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import pickle
import os

class AyurvedaMLChatbot:
    def __init__(self):
        self.vectorizer = None
        self.tfidf_matrix = None
        self.chunks = []
        self.model_path = 'ayurveda_model.pkl'
        
    def extract_text_from_pdf(self, pdf_path):
        """Extract text from PDF"""
        text = ""
        try:
            with open(pdf_path, 'rb') as file:
                reader = PyPDF2.PdfReader(file)
                for page in reader.pages:
                    text += page.extract_text() + "\n"
        except Exception as e:
            print(f"Error reading {pdf_path}: {e}")
        return text
    
    def clean_text(self, text):
        """Clean and normalize text"""
        text = re.sub(r'\s+', ' ', text)
        text = re.sub(r'[^\w\s.,!?-]', '', text)
        return text.strip()
    
    def create_chunks(self, text, chunk_size=500):
        """Split text into chunks"""
        words = text.split()
        chunks = []
        for i in range(0, len(words), chunk_size):
            chunk = ' '.join(words[i:i + chunk_size])
            if len(chunk) > 100:
                chunks.append(chunk)
        return chunks
    
    def train(self, pdf_paths):
        """Train the model on PDF content"""
        print("Training model on PDFs...")
        
        all_text = ""
        for pdf_path in pdf_paths:
            if os.path.exists(pdf_path):
                print(f"Processing: {pdf_path}")
                text = self.extract_text_from_pdf(pdf_path)
                all_text += text + "\n\n"
        
        cleaned_text = self.clean_text(all_text)
        self.chunks = self.create_chunks(cleaned_text, chunk_size=400)
        
        print(f"Created {len(self.chunks)} knowledge chunks")
        
        self.vectorizer = TfidfVectorizer(
            max_features=1000,
            stop_words='english',
            ngram_range=(1, 2)
        )
        
        self.tfidf_matrix = self.vectorizer.fit_transform(self.chunks)
        
        self.save_model()
        print("Model trained and saved!")
    
    def save_model(self):
        """Save trained model"""
        with open(self.model_path, 'wb') as f:
            pickle.dump({
                'vectorizer': self.vectorizer,
                'tfidf_matrix': self.tfidf_matrix,
                'chunks': self.chunks
            }, f)
    
    def load_model(self):
        """Load trained model"""
        if os.path.exists(self.model_path):
            with open(self.model_path, 'rb') as f:
                data = pickle.load(f)
                self.vectorizer = data['vectorizer']
                self.tfidf_matrix = data['tfidf_matrix']
                self.chunks = data['chunks']
            return True
        return False
    
    def understand_query(self, query):
        """Understand user intent"""
        query_lower = query.lower()
        
        symptoms = ['yellow', 'pain', 'fever', 'cough', 'cold', 'headache', 'stomach', 'digestion', 
                   'constipation', 'diarrhea', 'vomit', 'nausea', 'tired', 'weak', 'sleep', 'stress',
                   'anxiety', 'skin', 'rash', 'itch', 'burn', 'pee', 'urine', 'blood']
        
        actions = ['cure', 'treat', 'remedy', 'help', 'fix', 'heal', 'prevent', 'avoid', 'stop', 'do']
        
        intent = {
            'has_symptom': any(s in query_lower for s in symptoms),
            'wants_remedy': any(a in query_lower for a in actions),
            'about_dosha': any(d in query_lower for d in ['vata', 'pitta', 'kapha', 'dosha'])
        }
        
        return intent
    
    def get_response(self, query, context="", top_k=5):
        """Get comprehensive response from trained model"""
        if not self.vectorizer:
            if not self.load_model():
                return "Model not trained. Please train the model first."
        
        query_vec = self.vectorizer.transform([query])
        similarities = cosine_similarity(query_vec, self.tfidf_matrix).flatten()
        
        top_indices = np.argsort(similarities)[-top_k:][::-1]
        
        if similarities[top_indices[0]] < 0.1:
            return self.get_intelligent_fallback(query)
        
        response_parts = []
        for idx in top_indices:
            if similarities[idx] > 0.1:
                response_parts.append(self.chunks[idx])
        
        response = ' '.join(response_parts)
        return self.format_response(response, query)
    
    def format_response(self, text, query):
        """Format comprehensive response from model"""
        # Remove chapter references
        text = re.sub(r'Chapter\s+\d+[:\s-]*', '', text, flags=re.IGNORECASE)
        text = re.sub(r'Section\s+\d+[:\s-]*', '', text, flags=re.IGNORECASE)
        text = re.sub(r'Page\s+\d+', '', text, flags=re.IGNORECASE)
        text = re.sub(r'\[.*?\]', '', text)
        
        # Clean and return full response
        text = re.sub(r'\s+', ' ', text).strip()
        return text[:2000]  # Increased limit for detailed responses
    
    def get_intelligent_fallback(self, query):
        """Fallback for queries not in trained model"""
        return "I don't have specific information about that in my knowledge base. Please try rephrasing your question or ask about Ayurvedic concepts like doshas, treatments, herbs, diet, or lifestyle practices."ng> - Digestive health, detoxification"""
        
        elif any(word in query_lower for word in ['digest', 'stomach', 'acidity']):
            return """<strong>Improve Digestion (Agni):</strong><br><br>
• Eat at regular times<br>
• Use digestive spices: ginger, cumin, fennel, coriander<br>
• Drink warm water throughout the day<br>
• Avoid overeating<br>
• Walk 100 steps after meals<br>
• Eat largest meal at midday<br>
• Avoid cold drinks with meals"""
        
        else:
            return """I can help with:<br><br>
🌬️ Dosha imbalances (Vata, Pitta, Kapha)<br>
💊 Ayurvedic remedies and herbs<br>
🍽️ Diet and lifestyle recommendations<br>
🧘 Yoga and pranayama<br>
😌 Stress and sleep management<br><br>
Please ask a specific question about your health concern!"""

if __name__ == "__main__":
    chatbot = AyurvedaMLChatbot()
    
    pdf_files = [
        'astang hrdaya.pdf',
        'Ayurvedic Medicine Encyclopedia.pdf'
    ]
    
    chatbot.train(pdf_files)
