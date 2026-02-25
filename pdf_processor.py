"""
PDF Processing and Embedding Generation
Extracts text from Ayurveda PDF and creates vector embeddings
"""

import PyPDF2
import re
from sentence_transformers import SentenceTransformer
import numpy as np
import pickle
import os

class AyurvedaPDFProcessor:
    """Process Ayurveda PDF and generate embeddings"""
    
    def __init__(self, pdf_path):
        self.pdf_path = pdf_path
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
        self.chunks = []
        self.embeddings = None
        self.metadata = []
    
    def extract_text(self):
        """Extract text from PDF"""
        text = ""
        with open(self.pdf_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            for page_num, page in enumerate(pdf_reader.pages):
                page_text = page.extract_text()
                text += f"\n[PAGE {page_num + 1}]\n{page_text}"
        return text
    
    def classify_mode(self, text):
        """Classify text chunk into Ayurveda mode"""
        text_lower = text.lower()
        
        # Keywords for each mode
        charaka_keywords = ['charaka', 'kayachikitsa', 'dosha', 'vata', 'pitta', 'kapha', 
                           'diagnosis', 'chikitsa', 'internal medicine', 'rasa', 'rakta']
        sushruta_keywords = ['sushruta', 'shalya', 'surgery', 'marma', 'surgical', 
                            'anatomy', 'instrument', 'wound', 'fracture']
        ashtanga_keywords = ['ashtanga', 'hridaya', 'formulation', 'preparation', 
                            'compound', 'recipe', 'medicine preparation']
        
        scores = {
            'charaka': sum(1 for kw in charaka_keywords if kw in text_lower),
            'sushruta': sum(1 for kw in sushruta_keywords if kw in text_lower),
            'ashtanga': sum(1 for kw in ashtanga_keywords if kw in text_lower),
            'modern': 0  # Default for general content
        }
        
        max_mode = max(scores, key=scores.get)
        return max_mode if scores[max_mode] > 0 else 'modern'
    
    def chunk_text(self, text, chunk_size=1000):
        """Split text into chunks with metadata"""
        # Split by page markers
        pages = re.split(r'\[PAGE (\d+)\]', text)
        
        chunks = []
        for i in range(1, len(pages), 2):
            page_num = pages[i]
            page_text = pages[i + 1].strip()
            
            # Split page into sentences
            sentences = re.split(r'(?<=[.!?])\s+', page_text)
            
            current_chunk = ""
            for sentence in sentences:
                if len(current_chunk) + len(sentence) < chunk_size:
                    current_chunk += sentence + " "
                else:
                    if current_chunk:
                        mode = self.classify_mode(current_chunk)
                        chunks.append({
                            'text': current_chunk.strip(),
                            'page': int(page_num),
                            'mode': mode
                        })
                    current_chunk = sentence + " "
            
            if current_chunk:
                mode = self.classify_mode(current_chunk)
                chunks.append({
                    'text': current_chunk.strip(),
                    'page': int(page_num),
                    'mode': mode
                })
        
        return chunks
    
    def generate_embeddings(self):
        """Generate embeddings for all chunks"""
        texts = [chunk['text'] for chunk in self.chunks]
        self.embeddings = self.model.encode(texts, show_progress_bar=True)
        return self.embeddings
    
    def save_embeddings(self, output_dir='embeddings'):
        """Save embeddings and metadata"""
        os.makedirs(output_dir, exist_ok=True)
        
        np.save(f'{output_dir}/embeddings.npy', self.embeddings)
        
        with open(f'{output_dir}/chunks.pkl', 'wb') as f:
            pickle.dump(self.chunks, f)
        
        print(f"Saved {len(self.chunks)} chunks and embeddings")
    
    def load_embeddings(self, output_dir='embeddings'):
        """Load pre-generated embeddings"""
        self.embeddings = np.load(f'{output_dir}/embeddings.npy')
        
        with open(f'{output_dir}/chunks.pkl', 'rb') as f:
            self.chunks = pickle.load(f)
        
        print(f"Loaded {len(self.chunks)} chunks and embeddings")
    
    def process_pdf(self):
        """Complete PDF processing pipeline"""
        print("Extracting text from PDF...")
        text = self.extract_text()
        
        print("Chunking text...")
        self.chunks = self.chunk_text(text)
        
        print(f"Generated {len(self.chunks)} chunks")
        
        print("Generating embeddings...")
        self.generate_embeddings()
        
        print("Saving embeddings...")
        self.save_embeddings()
        
        return self.chunks, self.embeddings

if __name__ == "__main__":
    pdf_path = r"C:\Users\acer\OneDrive\Desktop\Ayurveda\Ayurvedic Medicine Encyclopedia.pdf"
    
    processor = AyurvedaPDFProcessor(pdf_path)
    processor.process_pdf()
    
    print("\nMode distribution:")
    modes = {}
    for chunk in processor.chunks:
        mode = chunk['mode']
        modes[mode] = modes.get(mode, 0) + 1
    
    for mode, count in modes.items():
        print(f"{mode}: {count} chunks")
