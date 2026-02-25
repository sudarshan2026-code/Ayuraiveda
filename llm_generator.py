"""
LLM Integration for Answer Generation
Uses Groq LLM with RAG context to generate grounded answers
"""

from groq import Groq
import os

class AyurvedaLLM:
    """LLM-based answer generation with RAG context"""
    
    def __init__(self):
        api_key = os.environ.get('GROQ_API_KEY', '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')
        self.client = Groq(api_key=api_key)
        
        self.mode_prompts = {
            'charaka': """You are a classical Charaka Samhita scholar. Answer questions using traditional Ayurvedic terminology, dosha-based reasoning, and internal medicine principles. Focus on kayachikitsa (internal medicine), diagnosis, and therapeutic approaches.""",
            
            'sushruta': """You are a Sushruta Samhita expert specializing in Shalya Tantra (surgery). Answer questions about surgical procedures, anatomy, marma science, surgical instruments, and wound management using classical terminology.""",
            
            'ashtanga': """You are an Ashtanga Hridaya scholar. Provide balanced answers integrating classical theory with practical formulations and preparations. Include both conceptual understanding and application.""",
            
            'modern': """You are a modern Ayurveda practitioner. Explain Ayurvedic concepts in simple, contemporary language while staying true to classical principles. Make the knowledge accessible to general users."""
        }
    
    def generate_answer(self, query, context, mode='modern', citations=None):
        """
        Generate answer using LLM with RAG context
        
        Args:
            query: User question
            context: Retrieved context from RAG
            mode: Selected Ayurveda mode
            citations: List of citation strings
        
        Returns:
            Generated answer with citations
        """
        system_prompt = self.mode_prompts.get(mode, self.mode_prompts['modern'])
        
        user_prompt = f"""Based STRICTLY on the following context from Ayurvedic texts, answer the question.

IMPORTANT RULES:
1. Answer ONLY using information from the provided context
2. If the answer is not in the context, say "This information is not available in the selected text."
3. Do not add information from your general knowledge
4. Cite the source when possible
5. Be concise and accurate

CONTEXT:
{context}

QUESTION: {query}

ANSWER:"""

        try:
            response = self.client.chat.completions.create(
                model="llama-3.1-70b-versatile",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.2,
                max_tokens=800,
                top_p=0.9
            )
            
            answer = response.choices[0].message.content.strip()
            
            # Add citations
            if citations:
                answer += "\n\n📚 Sources:\n" + "\n".join(f"• {cite}" for cite in citations)
            
            return answer
        
        except Exception as e:
            return f"Error generating answer: {str(e)}"
    
    def chat(self, query, retriever, mode='modern', top_k=5):
        """
        Complete RAG pipeline: retrieve + generate
        
        Args:
            query: User question
            retriever: AyurvedaRAGRetriever instance
            mode: Selected mode
            top_k: Number of chunks to retrieve
        
        Returns:
            Answer with citations
        """
        # Retrieve relevant chunks
        retrieved_chunks = retriever.retrieve(query, mode=mode, top_k=top_k)
        
        # Format context
        context = retriever.format_context(retrieved_chunks)
        
        # Get citations
        citations = retriever.get_citations(retrieved_chunks)
        
        # Generate answer
        answer = self.generate_answer(query, context, mode, citations)
        
        return {
            'answer': answer,
            'citations': citations,
            'mode': mode,
            'chunks_retrieved': len(retrieved_chunks)
        }

if __name__ == "__main__":
    from rag_retriever import AyurvedaRAGRetriever
    
    retriever = AyurvedaRAGRetriever()
    llm = AyurvedaLLM()
    
    query = "What is Vata dosha?"
    result = llm.chat(query, retriever, mode='charaka')
    
    print(f"Query: {query}\n")
    print(f"Mode: {result['mode']}\n")
    print(f"Answer:\n{result['answer']}")
