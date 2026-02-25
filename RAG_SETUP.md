# 📚 Classical Ayurveda Knowledge Intelligence System - Setup Guide

## RAG-Powered AI with Authentic Ayurvedic Texts

---

## 🎯 System Overview

This system uses **Retrieval-Augmented Generation (RAG)** to answer questions strictly based on the Ayurvedic Medicine Encyclopedia PDF.

### Architecture:
```
PDF → Text Extraction → Chunking → Embeddings → Vector DB → RAG Retrieval → LLM → Answer
```

---

## 📋 Prerequisites

1. Python 3.8+
2. Ayurvedic Medicine Encyclopedia PDF at:
   `C:\Users\acer\OneDrive\Desktop\Ayurveda\Ayurvedic Medicine Encyclopedia.pdf`
3. Groq API key (already configured)

---

## 🚀 Installation Steps

### Step 1: Install Dependencies
```bash
pip install Flask reportlab groq PyPDF2 sentence-transformers numpy scikit-learn
```

Or use requirements.txt:
```bash
pip install -r requirements.txt
```

### Step 2: Process PDF and Generate Embeddings
```bash
python pdf_processor.py
```

This will:
- Extract text from PDF
- Chunk into 800-1000 token segments
- Classify chunks by mode (Charaka/Sushruta/Ashtanga/Modern)
- Generate embeddings
- Save to `embeddings/` directory

**Expected output:**
```
Extracting text from PDF...
Chunking text...
Generated XXX chunks
Generating embeddings...
Saving embeddings...
```

### Step 3: Run Application
```bash
python app.py
```

### Step 4: Access RAG Chatbot
```
http://127.0.0.1:5000/rag-chatbot
```

---

## 🎭 Knowledge Modes

### 1. Charaka Mode 🌿
**Focus:** Internal medicine (Kayachikitsa)
- Dosha theory and diagnosis
- Therapeutic approaches
- Classical terminology
- Preventive medicine

**Example Questions:**
- "What is Vata dosha according to Charaka?"
- "How to diagnose Pitta imbalance?"
- "What are the principles of Kayachikitsa?"

### 2. Sushruta Mode ⚕️
**Focus:** Surgery (Shalya Tantra)
- Surgical procedures
- Anatomy and marma points
- Surgical instruments
- Wound management

**Example Questions:**
- "What are marma points?"
- "Describe surgical instruments in Sushruta Samhita"
- "How to treat wounds according to Sushruta?"

### 3. Ashtanga Mode 📖
**Focus:** Balanced classical approach
- Theory + practical formulations
- Medicine preparation
- Compound recipes
- Integrated knowledge

**Example Questions:**
- "How to prepare Ayurvedic formulations?"
- "What are the eight branches of Ayurveda?"
- "Describe classical medicine preparation methods"

### 4. Modern Ayurveda Mode 🔬
**Focus:** Contemporary interpretation
- Simple modern language
- Clinical applications
- Accessible explanations
- Practical usage

**Example Questions:**
- "Explain Ayurveda in simple terms"
- "How is Ayurveda relevant today?"
- "Modern applications of Ayurvedic principles"

---

## 🔧 How It Works

### 1. PDF Processing
```python
# Extract text with page numbers
text = extract_text_from_pdf()

# Chunk into segments
chunks = chunk_text(text, size=1000)

# Classify by mode
for chunk in chunks:
    chunk['mode'] = classify_mode(chunk['text'])
```

### 2. Embedding Generation
```python
# Use sentence-transformers
model = SentenceTransformer('all-MiniLM-L6-v2')
embeddings = model.encode(chunks)
```

### 3. RAG Retrieval
```python
# Convert query to embedding
query_embedding = model.encode(query)

# Filter by mode
filtered_chunks = filter_by_mode(chunks, selected_mode)

# Calculate similarity
similarities = cosine_similarity(query_embedding, filtered_chunks)

# Retrieve top-5
top_chunks = get_top_k(similarities, k=5)
```

### 4. LLM Generation
```python
# Format context
context = format_chunks(top_chunks)

# Generate answer with Groq
answer = groq_llm.generate(
    query=query,
    context=context,
    mode=selected_mode
)
```

---

## 📊 File Structure

```
Ayurveda/
├── pdf_processor.py          # PDF extraction & embedding generation
├── rag_retriever.py          # RAG retrieval system
├── llm_generator.py          # LLM answer generation
├── app.py                    # Flask backend
├── templates/
│   └── rag_chatbot.html      # RAG chat interface
├── embeddings/               # Generated embeddings (auto-created)
│   ├── embeddings.npy        # Vector embeddings
│   └── chunks.pkl            # Text chunks with metadata
└── requirements.txt          # Dependencies
```

---

## 🎯 Usage Examples

### Example 1: Charaka Mode Query
```
Mode: Charaka
Query: "What causes Vata imbalance?"

Response: According to classical texts, Vata imbalance occurs due to...
[Classical terminology and dosha-based reasoning]

Citations:
• Page 45 (Charaka Mode)
• Page 67 (Charaka Mode)
```

### Example 2: Modern Mode Query
```
Mode: Modern Ayurveda
Query: "What is Vata dosha in simple terms?"

Response: Vata dosha represents the air and space elements in the body...
[Simple, contemporary language]

Citations:
• Page 12 (Modern Mode)
• Page 89 (Modern Mode)
```

---

## 🔒 Hallucination Prevention

The system prevents AI hallucination through:

1. **Strict Context Grounding**
   - LLM only uses provided context
   - No general knowledge allowed

2. **Explicit Instructions**
   ```
   "If answer not found in context, say:
   'This information is not available in the selected text.'"
   ```

3. **Low Temperature**
   - Temperature = 0.2 (more deterministic)

4. **Citation Requirement**
   - Every answer includes source pages

---

## 🐛 Troubleshooting

### Issue: "embeddings/ directory not found"
**Solution:**
```bash
python pdf_processor.py
```

### Issue: "PDF not found"
**Solution:** Ensure PDF is at:
```
C:\Users\acer\OneDrive\Desktop\Ayurveda\Ayurvedic Medicine Encyclopedia.pdf
```

### Issue: "Groq API error"
**Solution:** API key is already configured in code. If issues persist:
```bash
set GROQ_API_KEY=your_key_here
```

### Issue: "No relevant chunks found"
**Solution:** 
- Try different mode
- Rephrase question
- Check if topic is in PDF

---

## 📈 Performance Metrics

- **Chunk Size:** 800-1000 tokens
- **Embedding Model:** all-MiniLM-L6-v2 (384 dimensions)
- **Retrieval:** Top-5 most relevant chunks
- **LLM:** Llama-3.1-70B via Groq
- **Response Time:** 2-5 seconds

---

## 🔮 Future Enhancements

1. **Multiple PDFs**
   - Add more classical texts
   - Charaka Samhita, Sushruta Samhita separately

2. **Advanced Filtering**
   - Filter by chapter/section
   - Filter by topic

3. **Conversation Memory**
   - Multi-turn conversations
   - Context retention

4. **Export Features**
   - Download answers as PDF
   - Save conversation history

---

## ✅ Verification

Test the system:
```bash
# 1. Check embeddings exist
ls embeddings/

# 2. Test retrieval
python rag_retriever.py

# 3. Test LLM generation
python llm_generator.py

# 4. Run full system
python app.py
```

---

## 📞 Support

For issues:
1. Check PDF path is correct
2. Verify embeddings are generated
3. Ensure all dependencies installed
4. Check Groq API key

---

**Classical Ayurveda Knowledge Intelligence System** | RAG-Powered AI with Authentic Texts
