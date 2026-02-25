# AyurVaani™ Setup Guide - Groq LLM Integration

## 🔐 Secure API Key Configuration

### Step 1: Get Groq API Key
1. Visit https://console.groq.com
2. Sign up or log in
3. Navigate to API Keys section
4. Create a new API key
5. Copy the key (starts with `gsk_...`)

### Step 2: Set Environment Variable

#### Windows (Command Prompt)
```cmd
set GROQ_API_KEY=your_api_key_here
```

#### Windows (PowerShell)
```powershell
$env:GROQ_API_KEY="your_api_key_here"
```

#### Linux/Mac
```bash
export GROQ_API_KEY=your_api_key_here
```

#### Permanent Setup (Windows)
1. Search "Environment Variables" in Windows
2. Click "Edit system environment variables"
3. Click "Environment Variables" button
4. Under "User variables", click "New"
5. Variable name: `GROQ_API_KEY`
6. Variable value: Your API key
7. Click OK

#### Permanent Setup (Linux/Mac)
Add to `~/.bashrc` or `~/.zshrc`:
```bash
export GROQ_API_KEY="your_api_key_here"
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Run Application
```bash
python app.py
```

## 🔄 Fallback Mode

If `GROQ_API_KEY` is not set:
- AyurVaani™ will still work
- Uses local knowledge base only
- No LLM expansion
- Responses are shorter but accurate

## ✅ Verify Setup

Run this test:
```python
import os
print("Groq API Key:", "✓ Set" if os.environ.get('GROQ_API_KEY') else "✗ Not Set")
```

## 🔒 Security Best Practices

✅ **DO:**
- Use environment variables
- Keep API key private
- Rotate keys periodically
- Use `.env` files (add to `.gitignore`)

❌ **DON'T:**
- Hardcode API keys in code
- Commit keys to Git
- Share keys publicly
- Use same key across projects

## 📊 Groq Usage

- Model: `llama-3.1-70b-versatile`
- Temperature: 0.3 (controlled)
- Max tokens: 500 (concise responses)
- Purpose: Expand validated Ayurveda content only

## 🎯 Architecture

```
User Query
    ↓
Intent Detection (Local)
    ↓
Knowledge Base (Validated Ayurveda)
    ↓
Tridosha Rules Validation
    ↓
Groq LLM (Natural Language Expansion)
    ↓
Response to User
```

## 🆘 Troubleshooting

**Error: "Groq initialization warning"**
- Check if API key is set correctly
- Verify key is valid on Groq console
- Restart terminal after setting variable

**Chatbot works but responses are short**
- Groq is not enabled (fallback mode)
- Check environment variable setup

**API rate limit errors**
- Groq free tier has limits
- Wait and retry
- Consider upgrading plan

## 📞 Support

For Groq API issues: https://console.groq.com/docs
For AyurVaani™ issues: Check application logs

---

**AyurVaani™** | Ancient Ayurveda, Explained with Modern Intelligence
