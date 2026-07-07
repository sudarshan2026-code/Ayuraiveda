# Ananta Labs India - AyurAI Veda Platform
## Complete Setup & Deployment Guide

---

## 🎯 Project Overview

Full-stack production-ready web application for Ananta Labs India offering AyurAI Veda product with:
- Multi-role authentication (User, Doctor, College, Admin)
- Payment integration with Cashfree
- Membership card generation
- Admin dashboard
- Email notifications
- Security features

---

## 📋 Prerequisites

- Node.js 16+ and npm
- PostgreSQL 12+
- Gmail account for email notifications
- Cashfree account for payments

---

## 🚀 Installation Steps

### 1. Database Setup

```bash
# Create database
createdb ananta_labs

# Run schema
psql -d ananta_labs -f database/schema.sql
```

### 2. Install Dependencies

```bash
npm install
```

Required packages:
- pg (PostgreSQL client)
- bcrypt (Password hashing)
- jsonwebtoken (JWT authentication)
- nodemailer (Email service)
- jspdf & html2canvas (PDF generation)

### 3. Environment Configuration

Copy `.env.example` to `.env` and configure:

```env
# Database
DATABASE_URL=postgresql://username:password@localhost:5432/ananta_labs

# JWT Secret (minimum 32 characters)
JWT_SECRET=your_super_secret_jwt_key_change_this_in_production

# Cashfree
CASHFREE_APP_ID=your_cashfree_app_id
CASHFREE_SECRET_KEY=your_cashfree_secret_key
CASHFREE_PAYMENT_LINK=https://payments.cashfree.com/forms/Userplane

# Email (Gmail)
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USER=anantalabsindia@gmail.com
EMAIL_PASSWORD=your_gmail_app_password

# App
NEXT_PUBLIC_APP_URL=http://localhost:5000
NODE_ENV=development
```

### 4. Create Admin User

```bash
node scripts/create-admin.js
```

Admin credentials:
- Email: anantalabsindia@gmail.com
- Password: A@L!2026#Secure

### 5. Start Application

```bash
# Development
npm run dev

# Production
npm run build
npm start
```

---

## 🔐 Security Features

### Frontend Protection
- Right-click disabled
- F12, Ctrl+Shift+I, Ctrl+U disabled
- DevTools detection
- Security alert on page load

### Backend Security
- JWT authentication
- Bcrypt password hashing
- Environment variables for secrets
- SQL injection protection
- Role-based access control

---

## 📊 Database Schema

### Tables

**users**
- Multi-role authentication
- Stores: name, email, password_hash, phone, role, profile_image

**user_profiles / doctor_profiles / college_profiles**
- Role-specific profile data

**orders**
- Payment order tracking

**payments**
- Payment transaction records

**subscriptions**
- Membership status and validity

**reports**
- Health assessment reports

---

## 🔌 API Endpoints

### Authentication
```
POST /api/auth/register - Register new user with role
POST /api/auth/login - Login and get JWT token
GET /api/auth/me - Get current user (protected)
```

### Profile
```
PUT /api/profile/update - Update user profile (protected)
```

### Payment
```
POST /api/payment/initiate - Initiate payment (users only)
POST /api/payment/confirm - Confirm payment and activate subscription
GET /api/payment/card - Get membership card data
```

### Admin
```
GET /api/admin/dashboard - Admin statistics (admin only)
GET /api/admin/users - List all users with filters (admin only)
```

---

## 💳 Payment Flow

1. User clicks "Buy Membership"
2. System creates order in database
3. User redirected to Cashfree payment link
4. After successful payment, user confirms via app
5. System:
   - Updates order status
   - Activates subscription (30 days)
   - Sends receipt email
6. User can generate membership card

---

## 📧 Email System

### Welcome Email
Sent on registration with account details

### Receipt Email
Sent after successful payment with:
- Company: Ananta Labs India
- Product: AyurAI Veda
- Amount, Order ID, Date
- Disclaimer about bank account name

---

## 🎫 Membership Card

### Features
- Professional design with gradient background
- MSME badge
- User photo
- Name, Email, Role
- Membership ID
- Start and expiry dates
- Downloadable as PDF

### Generation
Frontend uses jsPDF and html2canvas to create PDF from HTML template

---

## 👨‍💼 Admin Panel

### Dashboard Statistics
- Total users
- Total revenue
- Active subscriptions
- Recent users
- User breakdown by role
- Recent payments

### User Management
- View all users
- Filter by role
- Search by name/email
- Pagination
- View subscription status

---

## 🎨 UI Design

### Theme
- Ayurvedic colors (Green #2A9D8F, Dark #264653)
- Gold accents
- Clean, professional layout
- Fully responsive

### Components
- Glassmorphism cards
- Gradient backgrounds
- Smooth animations
- Mobile-friendly navigation

---

## 🔄 User Flow

1. **Registration**
   - Select role (User/Doctor/College)
   - Fill details
   - Auto-create profile
   - Receive welcome email

2. **Login**
   - Enter credentials
   - Get JWT token
   - Redirect to dashboard

3. **Profile**
   - Complete role-specific profile
   - Upload profile image

4. **Payment** (Users only)
   - Click "Buy Membership"
   - Redirect to Cashfree
   - Complete payment
   - Confirm in app
   - Receive receipt email

5. **Membership Card**
   - Generate card
   - Download as PDF

6. **Admin**
   - View dashboard
   - Manage users
   - Track revenue

---

## 🛡️ Role Permissions

### User
- Complete profile
- Purchase membership
- Generate membership card
- Access health assessments

### Doctor
- Complete professional profile
- View patient data (future feature)

### College
- Complete institutional profile
- Access educational content

### Admin
- Full dashboard access
- View all users
- Track payments
- System management

---

## 📱 Responsive Design

- Desktop: Full layout
- Tablet: Optimized navigation
- Mobile: Hamburger menu, stacked layout

---

## 🚨 Important Notes

### Bank Account Disclaimer
Payment receipts include:
> "You may see the bank account name as Jaydevsinh Zala instead of company name due to banking processing and settlement configuration."

### Security Alert
On page load:
> "🔒 Tridosha Intelligence Engine Security System is Activated"

### MSME Badge
Display on:
- Navbar
- Membership card
- Footer

MSME Registration: UDYAM-GJ-24-0218250

---

## 🔧 Troubleshooting

### Database Connection Issues
- Check DATABASE_URL in .env
- Ensure PostgreSQL is running
- Verify database exists

### Email Not Sending
- Enable "Less secure app access" in Gmail
- Use App Password instead of regular password
- Check EMAIL_USER and EMAIL_PASSWORD

### Payment Issues
- Verify Cashfree credentials
- Check payment link URL
- Ensure order is created in database

### JWT Errors
- Ensure JWT_SECRET is at least 32 characters
- Check token expiration
- Verify Authorization header format

---

## 📦 Deployment

### Production Checklist
- [ ] Set NODE_ENV=production
- [ ] Use strong JWT_SECRET
- [ ] Configure production database
- [ ] Set up SSL/HTTPS
- [ ] Configure email service
- [ ] Test payment flow
- [ ] Enable security features
- [ ] Set up monitoring

### Environment Variables
All sensitive data must be in environment variables, never hardcoded.

---

## 📞 Support

For issues or questions:
- Email: anantalabsindia@gmail.com
- Company: Ananta Labs India
- Product: AyurAI Veda

---

## 📄 License

© 2026 Ananta Labs India. All rights reserved.
Powered by Tridosha Intelligence Engine™

---

## 🎯 Next Steps

1. Set up database
2. Configure environment variables
3. Create admin user
4. Test registration flow
5. Test payment integration
6. Deploy to production
7. Monitor and maintain

---

**Built with ❤️ by Ananta Labs India**
