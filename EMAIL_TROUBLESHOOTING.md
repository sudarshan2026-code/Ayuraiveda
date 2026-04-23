# 📧 Email System Troubleshooting Guide

## 🔍 Why Email Might Not Be Working

### Common Issues:
1. ❌ Gmail App Password not configured
2. ❌ 2-Step Verification not enabled
3. ❌ Wrong App Password entered
4. ❌ Environment variables not set in Vercel
5. ❌ "Less secure app access" disabled (old Gmail accounts)
6. ❌ SMTP blocked by firewall/network

---

## ✅ Step-by-Step Fix

### Step 1: Enable 2-Step Verification

1. Go to: https://myaccount.google.com/security
2. Scroll to "2-Step Verification"
3. Click "Get Started"
4. Follow the setup process
5. ✅ Verify it's enabled (should show "On")

**IMPORTANT**: This is REQUIRED for App Passwords!

---

### Step 2: Generate App Password (Correct Way)

1. **Go to App Passwords page**:
   - Direct link: https://myaccount.google.com/apppasswords
   - Or: Google Account → Security → 2-Step Verification → App passwords

2. **If you don't see "App passwords" option**:
   - Make sure 2-Step Verification is ON
   - Wait 5 minutes after enabling 2-Step
   - Refresh the page

3. **Generate the password**:
   - Select app: **Mail**
   - Select device: **Other (Custom name)**
   - Enter name: **AyurAI Veda**
   - Click **Generate**

4. **Copy the 16-character password**:
   - Example: `abcd efgh ijkl mnop`
   - Remove spaces: `abcdefghijklmnop`
   - Save it securely!

---

### Step 3: Set Environment Variables in Vercel

#### Option A: Via Vercel Dashboard (Recommended)

1. Go to: https://vercel.com/dashboard
2. Select your project
3. Click **Settings** (top menu)
4. Click **Environment Variables** (left sidebar)
5. Add these THREE variables:

**Variable 1:**
- Name: `SENDER_EMAIL`
- Value: `zjay5398@gmail.com`
- Environment: ✅ Production, ✅ Preview, ✅ Development
- Click **Save**

**Variable 2:**
- Name: `GMAIL_APP_PASSWORD`
- Value: `your_16_char_password` (NO SPACES!)
- Environment: ✅ Production, ✅ Preview, ✅ Development
- Click **Save**

**Variable 3:**
- Name: `ADMIN_EMAIL`
- Value: `zjay5398@gmail.com`
- Environment: ✅ Production, ✅ Preview, ✅ Development
- Click **Save**

6. **IMPORTANT**: Redeploy your application!
   - Go to Deployments tab
   - Click "..." on latest deployment
   - Click "Redeploy"
   - OR push a new commit to GitHub

#### Option B: Via Vercel CLI

```bash
vercel env add SENDER_EMAIL
# Enter: zjay5398@gmail.com

vercel env add GMAIL_APP_PASSWORD
# Enter: your_16_char_password

vercel env add ADMIN_EMAIL
# Enter: zjay5398@gmail.com

# Redeploy
vercel --prod
```

---

### Step 4: Verify Environment Variables

1. Go to Vercel Dashboard → Your Project → Settings → Environment Variables
2. You should see:
   - ✅ SENDER_EMAIL
   - ✅ GMAIL_APP_PASSWORD
   - ✅ ADMIN_EMAIL
3. All should have values (shown as `***`)
4. All should be enabled for Production, Preview, Development

---

### Step 5: Test Email System

#### Test 1: Check Logs

1. Go to Vercel Dashboard → Your Project → Deployments
2. Click on latest deployment
3. Click "View Function Logs"
4. Submit a feedback form
5. Look for:
   - ✅ "Feedback email sent to..."
   - ❌ "Email error: ..."

#### Test 2: Submit Feedback

1. Go to: `https://your-app.vercel.app/feedback`
2. Fill out the form:
   - Name: Test User
   - Mobile: 9876543210
   - Institute: Test Institute
   - Designation: Tester
   - Feedback: This is a test message
3. Click Submit
4. Check your email (zjay5398@gmail.com)
5. Check spam folder too!

#### Test 3: Send Assessment Report

1. Complete an assessment
2. Enter email: zjay5398@gmail.com
3. Click "Email Report"
4. Check your inbox

---

## 🔧 Advanced Troubleshooting

### Issue: "Authentication failed"

**Cause**: Wrong App Password or 2-Step not enabled

**Solution**:
1. Delete old App Password
2. Generate new App Password
3. Update in Vercel
4. Redeploy

### Issue: "SMTP connection failed"

**Cause**: Network/firewall blocking SMTP

**Solution**:
1. Check if port 587 is open
2. Try from different network
3. Check Vercel logs for exact error

### Issue: Environment variables not working

**Cause**: Not redeployed after adding variables

**Solution**:
```bash
# Force redeploy
vercel --prod --force
```

### Issue: Emails going to spam

**Solution**:
1. Add zjay5398@gmail.com to contacts
2. Mark test email as "Not Spam"
3. Check email content (avoid spam words)

### Issue: "App passwords" option not showing

**Cause**: 2-Step Verification not enabled or not propagated

**Solution**:
1. Verify 2-Step is ON
2. Wait 10-15 minutes
3. Sign out and sign in again
4. Try incognito mode
5. Try different browser

---

## 🧪 Test Email Locally (Before Deploying)

Create a test file `test_email.py`:

```python
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Your credentials
sender_email = "zjay5398@gmail.com"
app_password = "your_16_char_password"  # NO SPACES!
recipient_email = "zjay5398@gmail.com"

try:
    # Create message
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = recipient_email
    msg['Subject'] = "Test Email from AyurAI Veda"
    
    body = "This is a test email. If you receive this, email system is working!"
    msg.attach(MIMEText(body, 'plain'))
    
    # Send email
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(sender_email, app_password)
    server.sendmail(sender_email, recipient_email, msg.as_string())
    server.quit()
    
    print("✅ Email sent successfully!")
    print("Check your inbox:", recipient_email)
    
except Exception as e:
    print("❌ Error:", str(e))
    print("\nCommon fixes:")
    print("1. Enable 2-Step Verification")
    print("2. Generate App Password")
    print("3. Remove spaces from App Password")
    print("4. Check email address is correct")
```

Run it:
```bash
python test_email.py
```

---

## 📋 Checklist

### Before Testing:
- [ ] 2-Step Verification enabled
- [ ] App Password generated (16 characters)
- [ ] App Password saved (no spaces)
- [ ] SENDER_EMAIL added to Vercel
- [ ] GMAIL_APP_PASSWORD added to Vercel
- [ ] ADMIN_EMAIL added to Vercel
- [ ] Application redeployed
- [ ] Waited 2-3 minutes after redeploy

### During Testing:
- [ ] Feedback form submitted
- [ ] Success message received
- [ ] Checked email inbox
- [ ] Checked spam folder
- [ ] Checked Vercel logs
- [ ] No error messages in logs

### If Still Not Working:
- [ ] Regenerated App Password
- [ ] Updated in Vercel
- [ ] Force redeployed
- [ ] Tested locally first
- [ ] Checked Gmail account settings
- [ ] Tried different email address

---

## 🔑 Correct App Password Format

### ❌ WRONG:
```
abcd efgh ijkl mnop  (with spaces)
```

### ✅ CORRECT:
```
abcdefghijklmnop  (no spaces)
```

---

## 📞 Still Not Working?

### Check These:

1. **Gmail Account Status**:
   - Account not suspended
   - Account not locked
   - Can send emails normally

2. **Vercel Logs**:
   ```bash
   vercel logs --follow
   ```
   Look for exact error message

3. **Test with Different Email**:
   - Try sending to different email address
   - Try using different Gmail account

4. **Network Issues**:
   - Check if SMTP is blocked
   - Try from different network
   - Check firewall settings

---

## 💡 Alternative: Use SendGrid (If Gmail Doesn't Work)

### Step 1: Create SendGrid Account
1. Go to: https://sendgrid.com/
2. Sign up for free (100 emails/day)
3. Verify your email
4. Create API key

### Step 2: Update Code
Replace Gmail SMTP with SendGrid:

```python
# Install sendgrid
# pip install sendgrid

from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

def send_email_sendgrid(to_email, subject, html_content):
    message = Mail(
        from_email='zjay5398@gmail.com',
        to_emails=to_email,
        subject=subject,
        html_content=html_content
    )
    
    try:
        sg = SendGridAPIClient(os.getenv('SENDGRID_API_KEY'))
        response = sg.send(message)
        return True
    except Exception as e:
        print(f"Error: {e}")
        return False
```

### Step 3: Add to Vercel
```
SENDGRID_API_KEY = your_api_key
```

---

## 📊 Email System Status Check

Run this in Vercel logs or locally:

```python
import os

print("Email Configuration Check:")
print("=" * 50)
print(f"SENDER_EMAIL: {'✅ Set' if os.getenv('SENDER_EMAIL') else '❌ Not Set'}")
print(f"GMAIL_APP_PASSWORD: {'✅ Set' if os.getenv('GMAIL_APP_PASSWORD') else '❌ Not Set'}")
print(f"ADMIN_EMAIL: {'✅ Set' if os.getenv('ADMIN_EMAIL') else '❌ Not Set'}")
print("=" * 50)

if os.getenv('GMAIL_APP_PASSWORD'):
    pwd = os.getenv('GMAIL_APP_PASSWORD')
    print(f"Password length: {len(pwd)} characters")
    print(f"Has spaces: {'❌ Yes (remove them!)' if ' ' in pwd else '✅ No'}")
```

---

## 🎯 Quick Fix Summary

1. **Enable 2-Step Verification**: https://myaccount.google.com/security
2. **Generate App Password**: https://myaccount.google.com/apppasswords
3. **Add to Vercel**: Settings → Environment Variables
4. **Redeploy**: Push new commit or manual redeploy
5. **Test**: Submit feedback form
6. **Check**: Email inbox and Vercel logs

---

## ✅ Success Indicators

When email is working:
- ✅ Feedback form shows success message
- ✅ Email appears in inbox within 1-2 minutes
- ✅ Vercel logs show "Email sent successfully"
- ✅ No error messages in console
- ✅ Email has proper formatting

---

**Need more help? Email: zjay5398@gmail.com** 📧
