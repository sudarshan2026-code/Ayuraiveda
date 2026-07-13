"""
Expanded Model Fine-Tuning and Training Script for Ayurvedic Clinical Assessment RAG
"""

import os
import glob
import pickle
import re
import warnings
import sys
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.exceptions import InconsistentVersionWarning

# Configure UTF-8 for console encoding
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    sys.stderr.reconfigure(encoding='utf-8', errors='replace')

# Suppress warnings
warnings.filterwarnings("ignore", category=InconsistentVersionWarning)
warnings.filterwarnings("ignore", category=UserWarning)

def clean_text(text):
    """Clean and normalize text"""
    text = re.sub(r'\s+', ' ', text)
    text = re.sub(r'[^\w\s.,!?-]', '', text)
    return text.strip()

def create_chunks(text, chunk_size=400):
    """Split text into chunks of specified word length"""
    words = text.split()
    chunks = []
    for i in range(0, len(words), chunk_size):
        chunk = ' '.join(words[i:i + chunk_size])
        if len(chunk) > 100:
            chunks.append(chunk)
    return chunks

def main():
    model_path = 'ayurveda_model.pkl'
    
    # 1. Load existing model
    if not os.path.exists(model_path):
        print(f"Error: Existing model not found at {model_path}")
        return
        
    print(f"Loading existing model from {model_path}...")
    with open(model_path, 'rb') as f:
        data = pickle.load(f)
        original_chunks = data.get('chunks', [])
        
    print(f"Loaded {len(original_chunks)} total chunks from previous file.")
    
    # 2. Reset back to the original 1,115 base CCRAS chunks
    ccras_count = 1115
    original_ccras_chunks = original_chunks[:ccras_count]
    print(f"Retained {len(original_ccras_chunks)} original CCRAS base chunks.")
    
    # 3. Scan for all PMC text files dynamically in root directory
    pmc_files = glob.glob('PMC*.txt')
    print(f"Found {len(pmc_files)} PMC research papers to index:")
    for f_name in pmc_files:
        print(f" - {f_name}")
        
    # 4. Extract chunks from all PMC papers
    new_chunks = []
    for file_name in pmc_files:
        print(f"Processing text data from {file_name}...")
        try:
            with open(file_name, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
            cleaned = clean_text(content)
            chunks = create_chunks(cleaned, chunk_size=400)
            new_chunks.extend(chunks)
            print(f"  -> Extracted {len(chunks)} chunks.")
        except Exception as e:
            print(f"  -> [ERROR] Failed to process {file_name}: {e}")
            
    if not new_chunks:
        print("No new chunks extracted. Aborting.")
        return
        
    # 5. Combine CCRAS and PMC chunks
    all_chunks = original_ccras_chunks + new_chunks
    print(f"Combined corpus: {len(all_chunks)} chunks (CCRAS: {len(original_ccras_chunks)}, PMC: {len(new_chunks)})")
    
    # 6. Fit new TfidfVectorizer with expanded vocabulary
    print("Re-fitting TfidfVectorizer on expanded corpus...")
    vectorizer = TfidfVectorizer(
        max_features=5000,  # Increased max features to accommodate the new papers
        stop_words='english',
        ngram_range=(1, 2)
    )
    
    tfidf_matrix = vectorizer.fit_transform(all_chunks)
    print(f"New TF-IDF Matrix shape: {tfidf_matrix.shape}")
    
    # 7. Save updated model back to pickle
    print(f"Saving updated model back to {model_path}...")
    with open(model_path, 'wb') as f:
        pickle.dump({
            'vectorizer': vectorizer,
            'tfidf_matrix': tfidf_matrix,
            'chunks': all_chunks
        }, f)
        
    print("Expanded model successfully fine-tuned, serialized, and saved!")

if __name__ == "__main__":
    main()
