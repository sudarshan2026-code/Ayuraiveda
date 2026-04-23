# AyurAI Veda - Vercel Deployment Guide

## 🚀 Quick Deploy to Vercel

### Method 1: Direct GitHub Integration (Recommended)

1. **Go to Vercel**: https://vercel.com
2. **Sign up/Login** with your GitHub account
3. **Import Project**: Click "New Project" → Import from GitHub
4. **Select Repository**: Choose `sudarshan2026-code/Ayuraiveda`
5. **Configure**:
   - Framework Preset: `Other`
   - Root Directory: `./`
   - Build Command: (leave empty)
   - Output Directory: (leave empty)
6. **Environment Variables** (Optional):
   ```
   GROQ_API_KEY=your_groq_api_key_here
   GMAIL_APP_PASSWORD=dexy zbgn qyte uhzl
   ```
7. **Deploy**: Click "Deploy"

### Method 2: Vercel CLI

```bash
# Install Vercel CLI
npm i -g vercel

# Login to Vercel
vercel login

# Deploy from project directory
cd C:\Users\jayde\Documents\Ayurveda
vercel

# Follow prompts:
# - Set up and deploy? Y
# - Which scope? (your account)
# - Link to existing project? N
# - Project name: ayuraiveda
# - Directory: ./
# - Override settings? N
```

## 📁 Files Created for Vercel

- ✅ `vercel.json` - Vercel configuration
- ✅ `requirements.txt` - Python dependencies (optimized)
- ✅ `runtime.txt` - Python version specification
- ✅ `.vercelignore` - Files to exclude from deployment

## 🔧 Optimizations Made

### **Serverless Compatibility:**
- ✅ Flask app configured for serverless functions
- ✅ ML model loading with Vercel environment detection
- ✅ Graceful fallback to rule-based analysis
- ✅ Optimized dependencies for faster cold starts

### **File Size Optimization:**
- ✅ Large ML models excluded (.vercelignore)
- ✅ Documentation files excluded
- ✅ Database files excluded
- ✅ Only essential files deployed

### **Performance:**
- ✅ 30-second function timeout
- ✅ Lightweight dependencies
- ✅ Efficient error handling
- ✅ Fast startup time

## 🌐 Expected Deployment URL

Your app will be available at:
```
https://ayuraiveda-[random-string].vercel.app
```

## ⚙️ Environment Variables (Optional)

Set these in Vercel Dashboard → Project → Settings → Environment Variables:

```
GROQ_API_KEY=your_groq_api_key_here
GMAIL_APP_PASSWORD=dexy zbgn qyte uhzl
FLASK_ENV=production
```

## 🔍 Features Available on Vercel

✅ **Core Features:**
- Home page with branding
- About Ayurveda information
- Clinical Assessment (rule-based)
- 59-Point Comprehensive Assessment
- AyurVaani AI Chatbot (with Groq API)
- Contact and Feedback forms
- Email functionality

⚠️ **Limitations:**
- ML model disabled (too large for serverless)
- Database features limited (use external DB for production)
- File uploads limited to Vercel's constraints

## 🛠️ Troubleshooting

### Common Issues:

1. **Build Fails**: Check requirements.txt for incompatible packages
2. **Function Timeout**: Reduce processing complexity
3. **Memory Issues**: Optimize imports and data processing
4. **Email Not Working**: Verify environment variables

### Solutions:

```python
# If imports fail, add try-catch blocks
try:
    from enhanced_clinical_engine import EnhancedClinicalEngine
    engine = EnhancedClinicalEngine()
except:
    # Fallback to basic engine
    from ai_engine import TridoshaIntelligenceEngine
    engine = TridoshaIntelligenceEngine()
```

## 📊 Deployment Status

After deployment, test these URLs:
- `/` - Home page
- `/about` - About page
- `/clinical-assessment` - Assessment form
- `/chatbot` - AI chatbot
- `/feedback` - Feedback form

## 🔄 Updates

To update your deployment:
1. Push changes to GitHub
2. Vercel auto-deploys from main branch
3. Or use `vercel --prod` for manual deployment

## 📞 Support

If deployment fails:
1. Check Vercel build logs
2. Verify all files are committed to GitHub
3. Ensure requirements.txt is correct
4. Check vercel.json configuration

Your AyurAI Veda app is now ready for Vercel deployment! 🌿✨