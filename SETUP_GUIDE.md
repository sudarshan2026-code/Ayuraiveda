# 🚀 Complete Setup & Deployment Guide - AyurAI Veda™

## Step 1: Install Node.js (Required for Vercel CLI)

### Option A: Download Node.js Installer (Recommended)
1. Go to: https://nodejs.org/
2. Download the **LTS version** (Long Term Support)
3. Run the installer
4. Follow the installation wizard (use default settings)
5. Restart your computer

### Option B: Check if Node.js is Already Installed
Open Command Prompt and run:
```bash
node --version
npm --version
```

If you see version numbers, Node.js is already installed! ✅

---

## Step 2: Install Vercel CLI

Open Command Prompt (as Administrator) and run:

```bash
npm install -g vercel
```

Wait for installation to complete (may take 1-2 minutes).

### Verify Installation
```bash
vercel --version
```

You should see a version number like `32.0.0` or similar.

---

## Step 3: Login to Vercel

### Option A: Create Free Vercel Account (if you don't have one)
1. Go to: https://vercel.com/signup
2. Sign up with GitHub, GitLab, Bitbucket, or Email
3. Verify your email

### Option B: Login via CLI
```bash
vercel login
```

Follow the prompts to authenticate.

---

## Step 4: Deploy Your Application

### Method 1: Using the Deployment Script
```bash
cd c:\Users\jayde\Documents\Ayurveda
deploy_to_vercel.bat
```

### Method 2: Manual Deployment
```bash
cd c:\Users\jayde\Documents\Ayurveda
vercel
```

Follow the prompts:
- **Set up and deploy?** → Y
- **Which scope?** → Select your account
- **Link to existing project?** → N (first time)
- **Project name?** → ayurveda (or your choice)
- **Directory?** → ./ (press Enter)
- **Override settings?** → N

### Method 3: Direct Production Deployment
```bash
cd c:\Users\jayde\Documents\Ayurveda
vercel --prod
```

---

## Step 5: Test Your Deployment

After deployment, you'll get a URL like:
```
https://ayurveda-xyz123.vercel.app
```

Test these pages:
- Homepage: `https://your-url.vercel.app/`
- Assessment: `https://your-url.vercel.app/assessment`
- Clinical: `https://your-url.vercel.app/clinical-assessment`
- Comprehensive: `https://your-url.vercel.app/comprehensive-assessment`
- Chatbot: `https://your-url.vercel.app/chatbot`
- Health Check: `https://your-url.vercel.app/health`

---

## Alternative: Deploy via Vercel Dashboard (No CLI Required!)

### Step 1: Push to GitHub
1. Create a GitHub account: https://github.com/signup
2. Create a new repository
3. Upload your project files

### Step 2: Import to Vercel
1. Go to: https://vercel.com/new
2. Click "Import Git Repository"
3. Select your GitHub repository
4. Configure:
   - **Framework Preset**: Other
   - **Root Directory**: ./
   - **Build Command**: (leave empty)
   - **Output Directory**: (leave empty)
5. Click "Deploy"

---

## Troubleshooting

### Issue: "npm is not recognized"
**Solution**: Node.js not installed or not in PATH
- Reinstall Node.js
- Restart Command Prompt
- Restart computer

### Issue: "vercel is not recognized"
**Solution**: Vercel CLI not installed globally
```bash
npm install -g vercel
```

### Issue: Permission Denied
**Solution**: Run Command Prompt as Administrator
- Right-click Command Prompt
- Select "Run as administrator"

### Issue: Deployment Fails
**Solution**: Check these files exist:
- ✅ `api/index.py`
- ✅ `vercel.json`
- ✅ `requirements.txt`
- ✅ `templates/` folder
- ✅ `static/` folder

---

## Quick Commands Reference

```bash
# Install Vercel CLI
npm install -g vercel

# Login to Vercel
vercel login

# Deploy to preview
vercel

# Deploy to production
vercel --prod

# Check deployments
vercel ls

# View logs
vercel logs

# Remove deployment
vercel rm [deployment-url]
```

---

## Environment Variables (Optional)

Set in Vercel Dashboard → Project → Settings → Environment Variables:

```
SECRET_KEY=your_secret_key_here
GROQ_API_KEY=your_groq_api_key_here
```

---

## Custom Domain (Optional)

1. Go to Vercel Dashboard
2. Select your project
3. Settings → Domains
4. Add your domain
5. Update DNS records

---

## Need Help?

- **Vercel Docs**: https://vercel.com/docs
- **Vercel Support**: https://vercel.com/support
- **Node.js Download**: https://nodejs.org/
- **GitHub**: https://github.com/

---

## ✅ Checklist Before Deployment

- [ ] Node.js installed
- [ ] Vercel CLI installed
- [ ] Vercel account created
- [ ] Logged in to Vercel
- [ ] In correct directory
- [ ] All files present
- [ ] Internet connection active

---

## 🎉 Success!

Once deployed, your AyurAI Veda™ application will be live with:
- ✅ All 9 pages
- ✅ 3 assessment types
- ✅ AI chatbot
- ✅ Feedback system
- ✅ Global CDN
- ✅ HTTPS enabled
- ✅ Automatic scaling

**Your app will be accessible worldwide in seconds!** 🌍

---

**AyurAI Veda™** | Powered by Tridosha Intelligence Engine™
