import math
from typing import List, Dict, Any
from backend.knowledge.ayur_knowledge import AYURVEDIC_CLASSICAL_DATABASE

class LightweightVectorStore:
    def __init__(self):
        self.documents = AYURVEDIC_CLASSICAL_DATABASE
        self.vocab = {}
        self._build_index()

    def _tokenize(self, text: str) -> List[str]:
        """Cleans and tokenizes text into lowercase words"""
        text = text.lower()
        words = []
        for word in text.split():
            # Strip punctuation
            cleaned = "".join(char for char in word if char.isalnum())
            if cleaned and len(cleaned) > 2:
                words.append(cleaned)
        return words

    def _build_index(self):
        """Indexes vocabulary across all classical texts"""
        doc_idx = 0
        for doc in self.documents:
            # Combine keywords, disease, translation, book name for rich text context
            doc_text = " ".join([
                doc["book"],
                doc["chapter"],
                doc["disease"],
                doc["dosha"],
                " ".join(doc["keywords"]),
                doc["translation"],
                doc["clinical_notes"]
            ])
            tokens = self._tokenize(doc_text)
            doc["_tokens"] = tokens
            doc["_tf"] = self._compute_tf(tokens)
            
            for token in set(tokens):
                if token not in self.vocab:
                    self.vocab[token] = []
                self.vocab[token].append(doc_idx)
            doc_idx += 1

        self.num_docs = len(self.documents)

    def _compute_tf(self, tokens: List[str]) -> Dict[str, float]:
        tf = {}
        for token in tokens:
            tf[token] = tf.get(token, 0) + 1
        # Normalize
        total = len(tokens) or 1
        for k in tf:
            tf[k] = tf[k] / total
        return tf

    def _compute_idf(self, term: str) -> float:
        doc_freq = len(self.vocab.get(term, []))
        if doc_freq == 0:
            return 0.0
        return math.log(self.num_docs / doc_freq)

    def query(self, query_text: str, top_k: int = 2) -> List[Dict[str, Any]]:
        """Retrieves top_k closest classical verses using TF-IDF cosine similarity"""
        query_tokens = self._tokenize(query_text)
        if not query_tokens:
            return self.documents[:top_k]

        query_tf = self._compute_tf(query_tokens)
        query_vec = {}
        for term in query_tf:
            idf = self._compute_idf(term)
            query_vec[term] = query_tf[term] * idf

        scores = []
        doc_idx = 0
        for doc in self.documents:
            doc_tf = doc["_tf"]
            dot_product = 0.0
            query_norm = 0.0
            doc_norm = 0.0

            # Calculate dot product
            for term, q_val in query_vec.items():
                if term in doc_tf:
                    idf = self._compute_idf(term)
                    d_val = doc_tf[term] * idf
                    dot_product += q_val * d_val
                query_norm += q_val * q_val

            for term in doc_tf:
                idf = self._compute_idf(term)
                d_val = doc_tf[term] * idf
                doc_norm += d_val * d_val

            query_norm = math.sqrt(query_norm)
            doc_norm = math.sqrt(doc_norm)

            similarity = 0.0
            if query_norm > 0 and doc_norm > 0:
                similarity = dot_product / (query_norm * doc_norm)
            
            # Boost score if keywords overlap directly
            keyword_matches = sum(1 for kw in doc["keywords"] if kw in query_text.lower())
            similarity += keyword_matches * 0.25

            scores.append((similarity, doc))
            doc_idx += 1

        # Sort by similarity descending
        scores.sort(key=lambda x: x[0], reverse=True)
        return [item[1] for item in scores[:top_k]]
