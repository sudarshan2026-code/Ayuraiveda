from backend.vector_db.vector_store import LightweightVectorStore
from backend.utils.web_searcher import WebSearcher
from backend.utils.ml_loader import AyurMLModelLoader
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

class RAGPipeline:
    def __init__(self):
        self.vector_store = LightweightVectorStore()
        self.web_searcher = WebSearcher()
        self.ml_loader = AyurMLModelLoader()

    def retrieve_references(self, query: str, top_k: int = 2) -> str:
        """Retrieves and formats matching classical scripture references, live web search, and CCRAS ML model guidelines"""
        matched_docs = self.vector_store.query(query, top_k=top_k)
        
        formatted_refs = []
        if matched_docs:
            formatted_refs.append("### 📚 Classical Ayurvedic References:")
            for doc in matched_docs:
                ref = (
                    f"- **Source**: {doc['book']} ({doc['chapter']}, {doc['verse']})\n"
                    f"  *Sanskrit*: \"{doc['sanskrit']}\"\n"
                    f"  *Translation*: {doc['translation']}\n"
                    f"  *Clinical note*: {doc['clinical_notes']}\n"
                )
                formatted_refs.append(ref)
        else:
            formatted_refs.append("No classical scriptural references found directly matching the query.")

        # CCRAS Prakriti SOP ML model matching
        if self.ml_loader.vectorizer and len(self.ml_loader.chunks) > 0:
            try:
                query_vec = self.ml_loader.vectorizer.transform([query])
                similarities = cosine_similarity(query_vec, self.ml_loader.tfidf_matrix).flatten()
                top_indices = np.argsort(similarities)[-3:][::-1]
                
                ml_matches = []
                for idx in top_indices:
                    if similarities[idx] > 0.08: # Low similarity threshold
                        ml_matches.append(self.ml_loader.chunks[idx].strip())
                        
                if ml_matches:
                    formatted_refs.append("\n### 🧠 CCRAS Clinical SOP Guidelines (ML-retrieved):")
                    for match in ml_matches:
                        # Truncate chunk for prompt size optimization if too long
                        formatted_refs.append(f"- {match[:500]}...")
            except Exception as e:
                print(f"[WARN] Failed to retrieve CCRAS ML references: {str(e)}")

        # Real-time web search enrichment
        web_results = self.web_searcher.search(query, num_results=3)
        if web_results:
            formatted_refs.append("\n### 🌐 Real-Time Web Search Results:")
            for res in web_results:
                ref = (
                    f"- **Title**: {res['title']}\n"
                    f"  *Snippet*: {res['snippet']}\n"
                    f"  *Link*: {res['link']}\n"
                )
                formatted_refs.append(ref)

        return "\n".join(formatted_refs)
