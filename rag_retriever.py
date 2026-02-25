"""
RAG Retrieval System with Mode Filtering
Retrieves relevant chunks based on query and selected mode
"""

import numpy as np
from sentence_transformers import SentenceTransformer
import pickle

class AyurvedaRAGRetriever:
    """RAG-based retrieval system for Ayurveda knowledge"""
    
    def __init__(self, embeddings_dir='embeddings'):
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
        self.embeddings = np.load(f'{embeddings_dir}/embeddings.npy')
        
        with open(f'{embeddings_dir}/chunks.pkl', 'rb') as f:
            self.chunks = pickle.load(f)
    
    def retrieve(self, query, mode='modern', top_k=5):
        """
        Retrieve top-k relevant chunks based on query and mode
        
        Args:
            query: User question
            mode: One of ['charaka', 'sushruta', 'ashtanga', 'modern']
            top_k: Number of chunks to retrieve
        
        Returns:
            List of relevant chunks with metadata
        """
        # Generate query embedding
        query_embedding = self.model.encode([query])[0]
        
        # Filter chunks by mode
        if mode != 'modern':
            filtered_indices = [i for i, chunk in enumerate(self.chunks) 
                              if chunk['mode'] == mode or chunk['mode'] == 'modern']
        else:
            filtered_indices = list(range(len(self.chunks)))
        
        # Calculate similarities for filtered chunks
        filtered_embeddings = self.embeddings[filtered_indices]
        similarities = np.dot(filtered_embeddings, query_embedding)
        
        # Get top-k indices
        top_indices = np.argsort(similarities)[-top_k:][::-1]
        
        # Map back to original indices
        original_indices = [filtered_indices[i] for i in top_indices]
        
        # Retrieve chunks
        results = []
        for idx in original_indices:
            chunk = self.chunks[idx]
            results.append({
                'text': chunk['text'],
                'page': chunk['page'],
                'mode': chunk['mode'],
                'similarity': float(similarities[np.where(filtered_indices == idx)[0][0]])
            })
        
        return results
    
    def format_context(self, retrieved_chunks):
        """Format retrieved chunks into context string"""
        context = ""
        for i, chunk in enumerate(retrieved_chunks, 1):
            context += f"\n[Source {i} - Page {chunk['page']}]\n{chunk['text']}\n"
        return context
    
    def get_citations(self, retrieved_chunks):
        """Extract citation information"""
        citations = []
        for chunk in retrieved_chunks:
            citations.append(f"Page {chunk['page']} ({chunk['mode'].capitalize()} Mode)")
        return citations

if __name__ == "__main__":
    retriever = AyurvedaRAGRetriever()
    
    # Test retrieval
    query = "What is Vata dosha?"
    results = retriever.retrieve(query, mode='charaka', top_k=3)
    
    print(f"Query: {query}\n")
    for i, result in enumerate(results, 1):
        print(f"Result {i} (Page {result['page']}, Mode: {result['mode']}):")
        print(result['text'][:200] + "...\n")
