# 🚀 Quick Start Guide - Ananta Labs AyurAI Veda

## Immediate Setup (5 Minutes)

### Step 1: Install Node Dependencies
```bash
npm install
```

### Step 2: Setup PostgreSQL Database
```bash
# Create database
createdb ananta_labs

# Import schema
psql -d ananta_labs -f database/schema.sql
```

### Step 3: Configure Environment
```bash
# Copy example env file
copy .env.example .env

# Edit .env with your credentials
```

**Required Configuration:**
- `DATABASE_URL` - Your PostgreSQL connection string
- `JWT_SECRET` - Random 32+ character string
- `EMAIL_USER` - anantalabsindia@gmail.com
- `EMAIL_PASSWORD` - Gmail app password
- `CASHFREE_PAYMENT_LINK` - https://payments.cashfree.com/forms/Userplane

### Step 4: Create Admin User
```bash
node scripts/create-admin.js
```

**Admin Login:**
- Email: anantalabsindia@gmail.com
- Password: A@L!2026#Secure

### Step 5: Start Application
```bash
python run.py
```

Access at: http://localhost:5000

---

## 🎯 Key Features Implemented

✅ **Multi-Role Authentication**
- User, Doctor, College, Admin roles
- JWT-based authentication
- Bcrypt password hashing

✅ **Payment Integration**
- Cashfree payment link
- Order tracking
- Subscription management (30 days)
- Auto receipt emails

✅ **Membership Card System**
- Professional PDF generation
- MSME badge included
- User photo and details
- Download functionality

✅ **Admin Dashboard**
- Total users, revenue, subscriptions
- User management with filters
- Recent payments tracking
- Role-based statistics

✅ **Security Features**
- Right-click disabled
- DevTools protection
- Security alert on load
- Environment-based secrets

✅ **Email System**
- Welcome emails on registration
- Payment receipts with disclaimer
- Professional HTML templates

---

## 📁 Project Structure

```
Ayurveda/
├── api/
│   ├── auth/
│   │   ├── register.js      # User registration
│   │   ├── login.js          # User login
│   │   └── me.js             # Get current user
│   ├── profile/
│   │   └── update.js         # Update profile
│   ├── payment/
│   │   ├── initiate.js       # Start payment
│   │   ├── confirm.js        # Confirm payment
│   │   └── card.js           # Get card data
│   └── admin/
│       ├── dashboard.js      # Admin stats
│       └── users.js          # User management
├── database/
│   └── schema.sql            # PostgreSQL schema
├── lib/
│   ├── db.js                 # Database connection
│   ├── email.js              # Email utilities
│   ├── security.js           # Frontend security
│   └── cardGenerator.js      # Membership card PDF
├── middleware/
│   └── auth.js               # JWT middleware
├── scripts/
│   └── create-admin.js       # Admin user setup
└── run.py                    # Flask application
```

---

## 🔌 API Endpoints Reference

### Authentication
```
POST /api/auth/register
Body: { name, email, password, phone, role }
Returns: { token, user }

POST /api/auth/login
Body: { email, password }
Returns: { token, user }

GET /api/auth/me
Headers: Authorization: Bearer <token>
Returns: { user, profile, subscription }
```

### Profile
```
PUT /api/profile/update
Headers: Authorization: Bearer <token>
Body: Role-specific fields
Returns: { success, message }
```

### Payment
```
POST /api/payment/initiate
Headers: Authorization: Bearer <token>
Body: { amount }
Returns: { orderId, paymentLink }

POST /api/payment/confirm
Headers: Authorization: Bearer <token>
Body: { orderId, cfPaymentId }
Returns: { subscription }

GET /api/payment/card
Headers: Authorization: Bearer <token>
Returns: { cardData }
```

### Admin
```
GET /api/admin/dashboard
Headers: Authorization: Bearer <token>
Returns: { stats, recentUsers, roleBreakdown, recentPayments }

GET /api/admin/users?page=1&limit=20&role=user&search=name
Headers: Authorization: Bearer <token>
Returns: { users, pagination }
```

---

## 💡 Usage Examples

### Register New User
```javascript
const response = await fetch('/api/auth/register', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    name: 'John Doe',
    email: 'john@example.com',
    password: 'SecurePass123',
    phone: '9876543210',
    role: 'user'
  })
});
const data = await response.json();
// Store token: localStorage.setItem('token', data.token);
```

### Initiate Payment
```javascript
const response = await fetch('/api/payment/initiate', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
    'Authorization': `Bearer ${token}`
  },
  body: JSON.stringify({ amount: 999 })
});
const { paymentLink, orderId } = await response.json();
// Redirect to: paymentLink
```

### Generate Membership Card
```javascript
import { generateMembershipCard } from './lib/cardGenerator';

const response = await fetch('/api/payment/card', {
  headers: { 'Authorization': `Bearer ${token}` }
});
const { cardData } = await response.json();

await generateMembershipCard(cardData);
// PDF downloaded automatically
```

---

## 🎨 Frontend Integration

### Security Setup (Add to main layout)
```javascript
import { initSecurity, disableConsole } from './lib/security';

useEffect(() => {
  initSecurity();
  disableConsole();
}, []);
```

### Protected Route Example
```javascript
const ProtectedRoute = ({ children }) => {
  const token = localStorage.getItem('token');
  
  if (!token) {
    return <Navigate to="/login" />;
  }
  
  return children;
};
```

---

## 🔐 Security Checklist

- [x] Passwords hashed with bcrypt
- [x] JWT tokens for authentication
- [x] Environment variables for secrets
- [x] SQL injection protection (parameterized queries)
- [x] Right-click disabled
- [x] DevTools detection
- [x] HTTPS recommended for production
- [x] Role-based access control

---

## 📧 Email Configuration

### Gmail Setup
1. Go to Google Account settings
2. Enable 2-Factor Authentication
3. Generate App Password
4. Use App Password in EMAIL_PASSWORD

### Email Templates
- Welcome email on registration
- Receipt email after payment
- Both use professional HTML templates

---

## 💳 Payment Configuration

### Cashfree Setup
1. Create Cashfree account
2. Get payment link: https://payments.cashfree.com/forms/Userplane
3. Add to CASHFREE_PAYMENT_LINK in .env

### Payment Flow
1. User clicks "Buy Membership"
2. Order created in database
3. Redirect to Cashfree link
4. User completes payment
5. User confirms in app
6. Subscription activated
7. Receipt email sent

---

## 🐛 Common Issues & Solutions

### "Database connection failed"
- Check DATABASE_URL format
- Ensure PostgreSQL is running
- Verify database exists

### "Email not sending"
- Use Gmail App Password, not regular password
- Check EMAIL_USER and EMAIL_PASSWORD
- Verify SMTP settings

### "Token invalid"
- Check JWT_SECRET is set
- Verify token format: "Bearer <token>"
- Check token expiration (7 days)

### "Payment not confirming"
- Verify order exists in database
- Check orderId matches
- Ensure user role is 'user'

---

## 📊 Database Queries

### Check Users
```sql
SELECT id, name, email, role, created_at FROM users;
```

### Check Subscriptions
```sql
SELECT u.name, s.status, s.start_date, s.end_date 
FROM subscriptions s 
JOIN users u ON s.user_id = u.id 
WHERE s.status = 'active';
```

### Check Revenue
```sql
SELECT SUM(amount) as total_revenue 
FROM payments 
WHERE payment_status = 'completed';
```

---

## 🚀 Deployment Tips

### Production Environment
```env
NODE_ENV=production
DATABASE_URL=<production-db-url>
JWT_SECRET=<strong-random-string-min-32-chars>
NEXT_PUBLIC_APP_URL=https://yourdomain.com
```

### Security Hardening
- Use HTTPS only
- Set secure cookie flags
- Enable CORS properly
- Rate limit API endpoints
- Monitor logs

---

## 📞 Support & Contact

**Company:** Ananta Labs India  
**Email:** anantalabsindia@gmail.com  
**Product:** AyurAI Veda  
**MSME:** UDYAM-GJ-24-0218250

---

## ✅ Testing Checklist

- [ ] User registration (all roles)
- [ ] User login
- [ ] Profile update
- [ ] Payment initiation
- [ ] Payment confirmation
- [ ] Subscription activation
- [ ] Email delivery
- [ ] Membership card generation
- [ ] Admin dashboard access
- [ ] User management
- [ ] Security features

---

**🎉 You're all set! Start building amazing Ayurvedic health solutions!**

Powered by Tridosha Intelligence Engine™
