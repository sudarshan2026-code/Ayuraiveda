from backend.vector_db.vector_store import LightweightVectorStore
from backend.utils.web_searcher import WebSearcher

class RAGPipeline:
    def __init__(self):
        self.vector_store = LightweightVectorStore()
        self.web_searcher = WebSearcher()

    def retrieve_references(self, query: str, top_k: int = 2) -> str:
        """Retrieves and formats matching classical scripture references and live web search results"""
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
