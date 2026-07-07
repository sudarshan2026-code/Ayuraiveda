const nodemailer = require('nodemailer');

const transporter = nodemailer.createTransport({
  host: process.env.EMAIL_HOST,
  port: process.env.EMAIL_PORT,
  secure: false,
  auth: {
    user: process.env.EMAIL_USER,
    pass: process.env.EMAIL_PASSWORD
  }
});

const sendReceiptEmail = async (userEmail, userName, amount, orderId, date) => {
  const mailOptions = {
    from: `"Ananta Labs India" <${process.env.EMAIL_USER}>`,
    to: userEmail,
    subject: 'Payment Receipt - AyurAI Veda Membership',
    html: `
      <!DOCTYPE html>
      <html>
      <head>
        <style>
          body { font-family: Arial, sans-serif; line-height: 1.6; color: #333; }
          .container { max-width: 600px; margin: 0 auto; padding: 20px; }
          .header { background: linear-gradient(135deg, #2A9D8F, #264653); color: white; padding: 30px; text-align: center; border-radius: 10px 10px 0 0; }
          .content { background: #f9f9f9; padding: 30px; border-radius: 0 0 10px 10px; }
          .receipt-box { background: white; padding: 20px; border-radius: 8px; margin: 20px 0; border: 2px solid #2A9D8F; }
          .row { display: flex; justify-content: space-between; padding: 10px 0; border-bottom: 1px solid #eee; }
          .label { font-weight: bold; color: #264653; }
          .disclaimer { background: #fff3cd; padding: 15px; border-radius: 5px; margin-top: 20px; border-left: 4px solid #ffc107; }
          .footer { text-align: center; padding: 20px; color: #666; font-size: 12px; }
        </style>
      </head>
      <body>
        <div class="container">
          <div class="header">
            <h1>🕉️ AyurAI Veda</h1>
            <p>Payment Receipt</p>
          </div>
          <div class="content">
            <p>Dear ${userName},</p>
            <p>Thank you for your payment! Your membership has been activated successfully.</p>
            
            <div class="receipt-box">
              <h3 style="color: #264653; margin-top: 0;">Payment Details</h3>
              <div class="row">
                <span class="label">Company:</span>
                <span>Ananta Labs India</span>
              </div>
              <div class="row">
                <span class="label">Product:</span>
                <span>AyurAI Veda Membership</span>
              </div>
              <div class="row">
                <span class="label">Amount:</span>
                <span>₹${amount}</span>
              </div>
              <div class="row">
                <span class="label">Order ID:</span>
                <span>${orderId}</span>
              </div>
              <div class="row">
                <span class="label">Date:</span>
                <span>${date}</span>
              </div>
            </div>

            <div class="disclaimer">
              <strong>⚠️ Important Notice:</strong><br>
              You may see the bank account name as "Jaydevsinh Zala" instead of company name due to banking processing and settlement configuration. This is normal and your payment is secure.
            </div>

            <p style="margin-top: 30px;">You can now access all premium features and generate your membership card from your dashboard.</p>
            
            <p>Best regards,<br><strong>Ananta Labs India Team</strong></p>
          </div>
          <div class="footer">
            <p>© 2026 Ananta Labs India. All rights reserved.</p>
            <p>Powered by Tridosha Intelligence Engine™</p>
          </div>
        </div>
      </body>
      </html>
    `
  };

  try {
    await transporter.sendMail(mailOptions);
    return { success: true };
  } catch (error) {
    console.error('Email error:', error);
    return { success: false, error: error.message };
  }
};

const sendWelcomeEmail = async (userEmail, userName, role) => {
  const mailOptions = {
    from: `"Ananta Labs India" <${process.env.EMAIL_USER}>`,
    to: userEmail,
    subject: 'Welcome to AyurAI Veda',
    html: `
      <!DOCTYPE html>
      <html>
      <head>
        <style>
          body { font-family: Arial, sans-serif; line-height: 1.6; color: #333; }
          .container { max-width: 600px; margin: 0 auto; padding: 20px; }
          .header { background: linear-gradient(135deg, #2A9D8F, #264653); color: white; padding: 30px; text-align: center; border-radius: 10px 10px 0 0; }
          .content { background: #f9f9f9; padding: 30px; border-radius: 0 0 10px 10px; }
          .footer { text-align: center; padding: 20px; color: #666; font-size: 12px; }
        </style>
      </head>
      <body>
        <div class="container">
          <div class="header">
            <h1>🕉️ Welcome to AyurAI Veda</h1>
          </div>
          <div class="content">
            <p>Dear ${userName},</p>
            <p>Welcome to AyurAI Veda! Your account has been created successfully as a <strong>${role}</strong>.</p>
            <p>You can now log in and complete your profile to get started.</p>
            <p>Best regards,<br><strong>Ananta Labs India Team</strong></p>
          </div>
          <div class="footer">
            <p>© 2026 Ananta Labs India. All rights reserved.</p>
          </div>
        </div>
      </body>
      </html>
    `
  };

  try {
    await transporter.sendMail(mailOptions);
    return { success: true };
  } catch (error) {
    console.error('Email error:', error);
    return { success: false, error: error.message };
  }
};

module.exports = { sendReceiptEmail, sendWelcomeEmail };
