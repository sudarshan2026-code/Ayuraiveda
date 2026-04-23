"""
Email Test Script for AyurAI Veda
Run this to test if your Gmail App Password is working
"""

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

print("=" * 60)
print("  AyurAI Veda - Email System Test")
print("=" * 60)
print()

# Get credentials
print("Enter your Gmail credentials:")
sender_email = input("Gmail address (zjay5398@gmail.com): ").strip() or "zjay5398@gmail.com"
app_password = input("Gmail App Password (16 characters, no spaces): ").strip()
recipient_email = input("Send test email to (press Enter for same): ").strip() or sender_email

print()
print("Testing email configuration...")
print("-" * 60)
print(f"From: {sender_email}")
print(f"To: {recipient_email}")
print(f"Password length: {len(app_password)} characters")
print(f"Has spaces: {'YES (REMOVE THEM!)' if ' ' in app_password else 'No'}")
print("-" * 60)
print()

if ' ' in app_password:
    print("⚠️  WARNING: App Password contains spaces!")
    print("   Remove all spaces and try again.")
    print()
    app_password = app_password.replace(' ', '')
    print(f"   Cleaned password: {app_password}")
    print()

try:
    print("Connecting to Gmail SMTP server...")
    
    # Create message
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = recipient_email
    msg['Subject'] = "🌿 Test Email from AyurAI Veda"
    
    body = """
    <html>
    <body style="font-family: Arial, sans-serif; padding: 20px;">
        <h2 style="color: #FF9933;">✅ Email System Working!</h2>
        <p>If you're reading this, your AyurAI Veda email system is configured correctly.</p>
        <p><strong>Next steps:</strong></p>
        <ol>
            <li>Add these environment variables to Vercel:
                <ul>
                    <li>SENDER_EMAIL = {}</li>
                    <li>GMAIL_APP_PASSWORD = your_password</li>
                    <li>ADMIN_EMAIL = {}</li>
                </ul>
            </li>
            <li>Redeploy your application</li>
            <li>Test the feedback form</li>
        </ol>
        <p style="color: #666; font-size: 12px; margin-top: 30px;">
            AyurAI Veda™ | Ancient Wisdom. Intelligent Health.
        </p>
    </body>
    </html>
    """.format(sender_email, recipient_email)
    
    msg.attach(MIMEText(body, 'html'))
    
    # Connect and send
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.set_debuglevel(0)  # Set to 1 for verbose output
    server.starttls()
    
    print("Authenticating...")
    server.login(sender_email, app_password)
    
    print("Sending email...")
    server.sendmail(sender_email, recipient_email, msg.as_string())
    server.quit()
    
    print()
    print("=" * 60)
    print("✅ SUCCESS! Email sent successfully!")
    print("=" * 60)
    print()
    print(f"Check your inbox: {recipient_email}")
    print("(Also check spam folder)")
    print()
    print("Your email system is working! Now add these to Vercel:")
    print()
    print("Environment Variables:")
    print(f"  SENDER_EMAIL = {sender_email}")
    print(f"  GMAIL_APP_PASSWORD = {app_password}")
    print(f"  ADMIN_EMAIL = {recipient_email}")
    print()
    print("Then redeploy your application.")
    print()
    
except smtplib.SMTPAuthenticationError as e:
    print()
    print("=" * 60)
    print("❌ AUTHENTICATION FAILED")
    print("=" * 60)
    print()
    print("Error:", str(e))
    print()
    print("Common fixes:")
    print("1. Enable 2-Step Verification:")
    print("   https://myaccount.google.com/security")
    print()
    print("2. Generate App Password:")
    print("   https://myaccount.google.com/apppasswords")
    print()
    print("3. Make sure you're using App Password, NOT your Gmail password")
    print()
    print("4. Remove all spaces from App Password")
    print()
    
except smtplib.SMTPException as e:
    print()
    print("=" * 60)
    print("❌ SMTP ERROR")
    print("=" * 60)
    print()
    print("Error:", str(e))
    print()
    print("Possible issues:")
    print("- Network/firewall blocking SMTP")
    print("- Gmail SMTP temporarily unavailable")
    print("- Check your internet connection")
    print()
    
except Exception as e:
    print()
    print("=" * 60)
    print("❌ ERROR")
    print("=" * 60)
    print()
    print("Error:", str(e))
    print()
    print("Please check:")
    print("- Email address is correct")
    print("- App Password is correct (16 characters, no spaces)")
    print("- Internet connection is working")
    print()

print("=" * 60)
print("Need help? Check EMAIL_TROUBLESHOOTING.md")
print("=" * 60)
