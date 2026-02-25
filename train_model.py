"""
Train the Ayurveda ML Chatbot on PDF documents
Run this script once to train the model
"""

from ml_chatbot import AyurvedaMLChatbot

def main():
    print("=" * 60)
    print("AyurAI Veda™ - ML Chatbot Training")
    print("=" * 60)
    
    chatbot = AyurvedaMLChatbot()
    
    # PDF files to train on
    pdf_files = [
        'astanga-hridaya-sutrasthan-handbook-pdf.pdf',
        'Ayurvedic Medicine Encyclopedia.pdf',
        'astang hrdaya.pdf'
    ]
    
    print("\nTraining on the following PDFs:")
    for pdf in pdf_files:
        print(f"  - {pdf}")
    
    print("\nStarting training process...")
    chatbot.train(pdf_files)
    
    print("\n" + "=" * 60)
    print("Training Complete!")
    print("=" * 60)
    
    # Test the model
    print("\n--- Testing Trained Model ---\n")
    
    test_queries = [
        "What is Tridosha?",
        "What is Vata dosha?",
        "How to improve digestion?",
        "Tell me about Ayurvedic herbs",
        "What is Pitta?"
    ]
    
    for query in test_queries:
        print(f"Q: {query}")
        response = chatbot.get_response(query)
        print(f"A: {response}\n")
    
    print("=" * 60)
    print("Model is ready! You can now use the chatbot.")
    print("=" * 60)

if __name__ == "__main__":
    main()
