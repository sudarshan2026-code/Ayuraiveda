# 📧 Email System Setup Guide - AyurAI Veda™

## ✅ Email Features Added

Your AyurAI Veda application now includes:

### 1. **Feedback Email System**
- Receives feedback from users
- Sends formatted HTML email to admin
- Includes all user details and feedback message
- Beautiful email template with branding

### 2. **Assessment Report Email**
- Sends personalized health reports to users
- Includes dosha analysis and recommendations
- Professional HTML email template
- Instant delivery after assessment

---

## 🔧 Setup Instructions

### Step 1: Get Gmail App Password

#### Why App Password?
Google requires App Passwords for third-party applications to send emails securely.

#### How to Create:

1. **Go to Google Account Settings**
   - Visit: https://myaccount.google.com/security

2. **Enable 2-Step Verification** (if not already enabled)
   - Click "2-Step Verification"
   - Follow the setup process
   - This is REQUIRED for App Passwords

3. **Generate App Password**
   - Go to: https://myaccount.google.com/apppasswords
   - Or search "App passwords" in Google Account settings
   - Select app: **Mail**
   - Select device: **Other (Custom name)**
   - Enter name: **AyurAI Veda**
   - Click **Generate**

4. **Copy the 16-character password**
   - Example: `abcd efgh ijkl mnop`
   - Save it securely (you won't see it again!)

---

### Step 2: Configure Environment Variables

#### For Local Development:

Create a `.env` file in your project root:

```bash
# Email Configuration
SENDER_EMAIL=zjay5398@gmail.com
GMAIL_APP_PASSWORD=your_16_char_app_password_here
ADMIN_EMAIL=zjay5398@gmail.com
```

#### For Vercel Deployment:

1. Go to: https://vercel.com/dashboard
2. Select your project
3. Click **Settings** → **Environment Variables**
4. Add these variables:

| Name | Value | Environment |
|------|-------|-------------|
| `SENDER_EMAIL` | `zjay5398@gmail.com` | Production, Preview |
| `GMAIL_APP_PASSWORD` | `your_app_password` | Production, Preview |
| `ADMIN_EMAIL` | `zjay5398@gmail.com` | Production, Preview |

5. Click **Save**
6. Redeploy your application

---

## 📧 Email Features

### 1. Feedback Email

**Triggered when**: User submits feedback form

**Sent to**: Admin email (ADMIN_EMAIL)

**Contains**:
- User's name, mobile, institute, designation
- Feedback message
- Timestamp
- Character count
- Beautiful HTML formatting

**Example**:
```
Subject: 🌿 AyurAI Veda Feedback from John Doe - Student
```

### 2. Assessment Report Email

**Triggered when**: User requests email report after assessment

**Sent to**: User's email address

**Contains**:
- Dominant dosha
- Risk level
- Dosha distribution (percentages with visual bars)
- Personalized recommendations
- Disclaimer
- Branding

**Example**:
```
Subject: 🌿 Your AyurAI Veda Health Assessment Report - Vata Dosha
```

---

## 🔌 API Endpoints

### 1. Submit Feedback
```
POST /submit-feedback
```

**Request Body**:
```json
{
  "name": "John Doe",
  "mobile": "9876543210",
  "institute": "ABC University",
  "designation": "Student",
  "feedback": "Great application! Very helpful."
}
```

**Response**:
```json
{
  "success": true,
  "message": "Feedback submitted successfully! We will contact you soon."
}
```

### 2. Send Report Email
```
POST /send-report-email
```

**Request Body**:
```json
{
  "email": "user@example.com",
  "report_data": {
    "dominant": "Vata",
    "risk": "Moderate",
    "scores": {
      "vata": 45,
      "pitta": 30,
      "kapha": 25
    },
    "recommendations": [
      "Follow regular daily routine",
      "Eat warm, cooked foods",
      "Practice oil massage"
    ]
  }
}
```

**Response**:
```json
{
  "success": true,
  "message": "Report sent successfully to user@example.com"
}
```

---

## 🎨 Email Templates

### Feedback Email Template Features:
- ✅ Gradient header with branding
- ✅ Contact information table
- ✅ Highlighted feedback message
- ✅ Character count
- ✅ Timestamp
- ✅ Professional footer
- ✅ Mobile-responsive design

### Assessment Report Email Features:
- ✅ Branded header
- ✅ Results summary cards
- ✅ Visual dosha distribution bars
- ✅ Color-coded risk levels
- ✅ Bulleted recommendations
- ✅ Important disclaimer
- ✅ Professional footer
- ✅ Mobile-responsive design

---

## 🔒 Security Features

### Email Security:
- ✅ Uses Gmail's secure SMTP with TLS
- ✅ App Password instead of account password
- ✅ Environment variables for credentials
- ✅ No credentials in code
- ✅ Secure connection (port 587 with STARTTLS)

### Input Validation:
- ✅ Email format validation
- ✅ Mobile number validation (10 digits)
- ✅ Feedback length limit (2000 characters)
- ✅ Required field validation
- ✅ XSS protection in HTML emails

---

## 🧪 Testing

### Test Feedback Email:

1. Go to: `https://your-app.vercel.app/feedback`
2. Fill out the form:
   - Name: Test User
   - Mobile: 9876543210
   - Institute: Test Institute
   - Designation: Tester
   - Feedback: This is a test feedback
3. Click Submit
4. Check admin email inbox

### Test Assessment Report Email:

1. Complete an assessment
2. Enter your email address
3. Click "Email Report"
4. Check your inbox (and spam folder)

---

## 🆘 Troubleshooting

### Issue: Email not sending

**Possible Causes**:
1. App Password not configured
2. 2-Step Verification not enabled
3. Wrong App Password
4. Environment variables not set

**Solutions**:
```bash
# Check environment variables
echo $GMAIL_APP_PASSWORD

# Verify in Vercel Dashboard
Settings → Environment Variables

# Check logs
vercel logs
```

### Issue: "Authentication failed"

**Solution**: 
- Regenerate App Password
- Make sure 2-Step Verification is enabled
- Use the App Password, not your Gmail password

### Issue: Emails going to spam

**Solution**:
- Add sender email to contacts
- Mark as "Not Spam"
- Check SPF/DKIM records (advanced)

### Issue: "SMTP connection failed"

**Solution**:
- Check internet connection
- Verify SMTP server: smtp.gmail.com
- Verify port: 587
- Check firewall settings

---

## 📊 Email Delivery Status

### Success Indicators:
- ✅ Console log: "Feedback email sent to..."
- ✅ Console log: "Assessment report sent to..."
- ✅ User receives success message
- ✅ Email appears in inbox

### Failure Indicators:
- ❌ Console log: "Email error: ..."
- ❌ Feedback logged to console instead
- ❌ User receives fallback message

---

## 🔄 Fallback Mechanism

If email sending fails:
1. Feedback is logged to console
2. User still receives success message
3. Admin can check logs for feedback
4. No data is lost

---

## 📈 Email Analytics (Optional)

To track email opens and clicks, integrate:
- SendGrid
- Mailgun
- Amazon SES
- Postmark

---

## 🌟 Email Customization

### Change Sender Name:
```python
msg['From'] = f"Your Name <{sender_email}>"
```

### Change Email Colors:
Edit the HTML templates in `api/index.py`:
- Header gradient: `#FF9933, #138808`
- Primary color: `#1a237e`
- Accent color: `#FF9933`

### Add Logo:
```html
<img src="https://your-domain.com/logo.png" alt="Logo" style="width: 100px;">
```

---

## 📱 Mobile Email Preview

Both email templates are mobile-responsive:
- ✅ Adapts to screen size
- ✅ Readable on all devices
- ✅ Touch-friendly buttons
- ✅ Optimized images

---

## ✅ Setup Checklist

- [ ] Gmail account ready
- [ ] 2-Step Verification enabled
- [ ] App Password generated
- [ ] Environment variables set (local)
- [ ] Environment variables set (Vercel)
- [ ] Application redeployed
- [ ] Feedback email tested
- [ ] Report email tested
- [ ] Emails not in spam
- [ ] All features working

---

## 🎯 Quick Setup Commands

### For Vercel:

```bash
# Set environment variables
vercel env add SENDER_EMAIL
vercel env add GMAIL_APP_PASSWORD
vercel env add ADMIN_EMAIL

# Redeploy
vercel --prod
```

---

## 📞 Support

**Email Issues?**
- Gmail Help: https://support.google.com/mail
- App Passwords: https://support.google.com/accounts/answer/185833
- Vercel Env Vars: https://vercel.com/docs/environment-variables

**Project Support**: zjay5398@gmail.com

---

## 🎉 Success!

Your AyurAI Veda application now has a complete email system!

**Features**:
- ✅ Feedback collection via email
- ✅ Assessment reports via email
- ✅ Beautiful HTML templates
- ✅ Secure authentication
- ✅ Error handling
- ✅ Fallback mechanism
- ✅ Mobile-responsive
- ✅ Production-ready

---

**🚀 Deploy and start receiving emails!**

```bash
vercel --prod
```

---

**AyurAI Veda™** | Ancient Wisdom. Intelligent Health. | Now with Email! 📧
