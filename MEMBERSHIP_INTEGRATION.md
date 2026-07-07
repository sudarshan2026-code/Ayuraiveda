# 🎯 Membership System Integration Guide

## Overview

This guide explains how to integrate the new authentication and membership system with free tier limitations into your existing AyurAI Veda application.

---

## 🆓 Free Tier Limitations

### Clinical Assessment
- **Free Users:** 1 assessment per day
- **Premium Members:** Unlimited assessments

### AyurVaani Chat
- **Free Users:** 10 messages per day
- **Premium Members:** 24/7 unlimited chat

---

## 🔗 Integration Steps

### 1. Add Routes to Flask App

Already added to `api/index.py`:
```python
@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')
```

### 2. Update Navigation Menu

Add to `base_dynamic.html` navigation:
```html
<nav id="mainNav">
    <ul>
        <li><a href="/">Home</a></li>
        <li><a href="/about">About</a></li>
        <li><a href="/clinical-assessment">Clinical Assessment</a></li>
        <li><a href="/chatbot">AyurVaani Chat</a></li>
        <li><a href="/contact">Contact</a></li>
        <li><a href="/feedback">Feedback</a></li>
        <!-- New Auth Links -->
        <li id="authLinks">
            <a href="/login" id="loginLink">Login</a>
            <a href="/register" id="registerLink">Register</a>
        </li>
        <li id="userLinks" style="display:none;">
            <a href="/dashboard" id="dashboardLink">Dashboard</a>
            <a href="#" id="logoutLink">Logout</a>
        </li>
    </ul>
</nav>
```

### 3. Add Authentication Check Script

Add to all protected pages:
```javascript
<script>
// Check if user is logged in
const token = localStorage.getItem('token');
const user = JSON.parse(localStorage.getItem('user') || '{}');

if (token && user.id) {
    // User is logged in
    document.getElementById('authLinks').style.display = 'none';
    document.getElementById('userLinks').style.display = 'block';
    
    // Check usage limits
    fetch('/api/usage/check', {
        headers: {
            'Authorization': `Bearer ${token}`
        }
    })
    .then(res => res.json())
    .then(data => {
        if (data.success) {
            // Store usage data
            localStorage.setItem('usage', JSON.stringify(data.usage));
            localStorage.setItem('subscription', JSON.stringify(data.subscription));
        }
    });
} else {
    // User not logged in - show auth links
    document.getElementById('authLinks').style.display = 'block';
    document.getElementById('userLinks').style.display = 'none';
}

// Logout handler
document.getElementById('logoutLink')?.addEventListener('click', (e) => {
    e.preventDefault();
    localStorage.removeItem('token');
    localStorage.removeItem('user');
    localStorage.removeItem('usage');
    localStorage.removeItem('subscription');
    window.location.href = '/';
});
</script>
```

### 4. Protect Clinical Assessment

Update `clinical_assessment_dynamic.html`:
```javascript
<script>
// Check authentication before allowing assessment
document.getElementById('assessmentForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const token = localStorage.getItem('token');
    
    if (!token) {
        alert('Please login to use Clinical Assessment');
        window.location.href = '/login';
        return;
    }
    
    // Check usage limits
    const usage = JSON.parse(localStorage.getItem('usage') || '{}');
    const subscription = JSON.parse(localStorage.getItem('subscription') || '{}');
    
    if (!subscription.active && usage.assessments?.remaining === 0) {
        if (confirm('You have used your free assessment for today. Upgrade to premium for unlimited access?')) {
            window.location.href = '/dashboard#membership';
        }
        return;
    }
    
    // Proceed with assessment
    const formData = new FormData(e.target);
    const data = Object.fromEntries(formData);
    
    try {
        const response = await fetch('/clinical-analyze', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}`
            },
            body: JSON.stringify(data)
        });
        
        const result = await response.json();
        
        if (result.limitReached) {
            alert(result.message);
            if (confirm('Upgrade to premium?')) {
                window.location.href = '/dashboard#membership';
            }
            return;
        }
        
        if (result.requiresAuth) {
            alert('Session expired. Please login again.');
            window.location.href = '/login';
            return;
        }
        
        // Display results
        displayResults(result);
        
        // Refresh usage data
        refreshUsageData();
        
    } catch (error) {
        alert('An error occurred. Please try again.');
    }
});

function refreshUsageData() {
    const token = localStorage.getItem('token');
    fetch('/api/usage/check', {
        headers: { 'Authorization': `Bearer ${token}` }
    })
    .then(res => res.json())
    .then(data => {
        if (data.success) {
            localStorage.setItem('usage', JSON.stringify(data.usage));
        }
    });
}
</script>
```

### 5. Protect AyurVaani Chat

Update `chatbot_dynamic.html`:
```javascript
<script>
let messageCount = 0;

document.getElementById('chatForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const token = localStorage.getItem('token');
    
    if (!token) {
        alert('Please login to use AyurVaani Chat');
        window.location.href = '/login';
        return;
    }
    
    // Check usage limits
    const usage = JSON.parse(localStorage.getItem('usage') || '{}');
    const subscription = JSON.parse(localStorage.getItem('subscription') || '{}');
    
    if (!subscription.active && usage.chat?.remaining === 0) {
        if (confirm('You have reached your free chat limit (10 messages/day). Upgrade to premium for 24/7 unlimited chat?')) {
            window.location.href = '/dashboard#membership';
        }
        return;
    }
    
    messageCount++;
    
    // Send message
    const message = document.getElementById('messageInput').value;
    
    try {
        const response = await fetch('/chat', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}`
            },
            body: JSON.stringify({ message })
        });
        
        const result = await response.json();
        
        // Display response
        displayMessage(result.response, 'bot');
        
        // Update usage display
        if (!subscription.active) {
            const remaining = 10 - messageCount;
            document.getElementById('chatLimit').textContent = 
                `Free tier: ${remaining} messages remaining today`;
        }
        
    } catch (error) {
        alert('An error occurred. Please try again.');
    }
});
</script>
```

---

## 📊 Dashboard Page

Create `templates/dashboard.html`:
```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Dashboard - AyurAI Veda</title>
    <link rel="icon" type="image/png" href="{{ url_for('static', filename='images/favicon.png') }}">
    <style>
        /* Use same dynamic theme styles */
        body {
            font-family: 'Inter', sans-serif;
            background: linear-gradient(135deg, #F4A261 0%, #E76F51 100%);
            min-height: 100vh;
            padding: 20px;
        }
        
        .dashboard-container {
            max-width: 1200px;
            margin: 0 auto;
            background: rgba(255, 255, 255, 0.1);
            backdrop-filter: blur(20px);
            border-radius: 20px;
            padding: 40px;
            border: 1px solid rgba(255, 255, 255, 0.2);
        }
        
        .welcome-section {
            text-align: center;
            margin-bottom: 40px;
            color: #FFFFFF;
        }
        
        .stats-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            margin-bottom: 40px;
        }
        
        .stat-card {
            background: rgba(255, 255, 255, 0.15);
            padding: 25px;
            border-radius: 15px;
            text-align: center;
            color: #FFFFFF;
        }
        
        .stat-value {
            font-size: 36px;
            font-weight: bold;
            margin: 10px 0;
        }
        
        .membership-section {
            background: rgba(255, 255, 255, 0.15);
            padding: 30px;
            border-radius: 15px;
            margin-bottom: 30px;
        }
        
        .btn-upgrade {
            background: linear-gradient(135deg, #2A9D8F, #264653);
            color: white;
            padding: 15px 40px;
            border: none;
            border-radius: 10px;
            font-size: 18px;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.3s ease;
        }
        
        .btn-upgrade:hover {
            transform: translateY(-3px);
            box-shadow: 0 6px 20px rgba(0, 0, 0, 0.3);
        }
    </style>
</head>
<body>
    <div class="dashboard-container">
        <div class="welcome-section">
            <h1>🕉️ Welcome to Your Dashboard</h1>
            <p id="userName"></p>
        </div>
        
        <div class="stats-grid">
            <div class="stat-card">
                <h3>Assessments Today</h3>
                <div class="stat-value" id="assessmentsUsed">0</div>
                <p id="assessmentsLimit">of 1 (Free)</p>
            </div>
            
            <div class="stat-card">
                <h3>Chat Messages Today</h3>
                <div class="stat-value" id="chatUsed">0</div>
                <p id="chatLimit">of 10 (Free)</p>
            </div>
            
            <div class="stat-card">
                <h3>Membership Status</h3>
                <div class="stat-value" id="membershipStatus">Free</div>
                <p id="membershipExpiry"></p>
            </div>
        </div>
        
        <div class="membership-section" id="membershipSection">
            <h2 style="color: #FFFFFF; margin-bottom: 20px;">🎯 Upgrade to Premium</h2>
            <p style="color: #FFFFFF; margin-bottom: 20px;">
                Get unlimited access to all features:
            </p>
            <ul style="color: #FFFFFF; margin-bottom: 30px;">
                <li>✓ Unlimited Clinical Assessments</li>
                <li>✓ 24/7 AyurVaani Chat</li>
                <li>✓ Downloadable Membership Card</li>
                <li>✓ Priority Support</li>
            </ul>
            <button class="btn-upgrade" onclick="buyMembership()">
                Buy Membership - ₹999
            </button>
        </div>
        
        <div style="text-align: center; margin-top: 30px;">
            <a href="/" style="color: #FFFFFF; text-decoration: none;">← Back to Home</a>
        </div>
    </div>
    
    <script>
        // Load user data
        const token = localStorage.getItem('token');
        const user = JSON.parse(localStorage.getItem('user') || '{}');
        
        if (!token || !user.id) {
            window.location.href = '/login';
        }
        
        document.getElementById('userName').textContent = `Hello, ${user.name}!`;
        
        // Load usage data
        async function loadUsageData() {
            try {
                const response = await fetch('/api/usage/check', {
                    headers: {
                        'Authorization': `Bearer ${token}`
                    }
                });
                
                const data = await response.json();
                
                if (data.success) {
                    // Update assessments
                    document.getElementById('assessmentsUsed').textContent = data.usage.assessments.used;
                    document.getElementById('assessmentsLimit').textContent = 
                        data.subscription.active ? 'Unlimited' : `of ${data.usage.assessments.limit} (Free)`;
                    
                    // Update chat
                    document.getElementById('chatUsed').textContent = data.usage.chat.used;
                    document.getElementById('chatLimit').textContent = 
                        data.subscription.active ? 'Unlimited' : `of ${data.usage.chat.limit} (Free)`;
                    
                    // Update membership
                    if (data.subscription.active) {
                        document.getElementById('membershipStatus').textContent = 'Premium';
                        document.getElementById('membershipExpiry').textContent = 
                            `Expires: ${new Date(data.subscription.endDate).toLocaleDateString()}`;
                        document.getElementById('membershipSection').style.display = 'none';
                    }
                }
            } catch (error) {
                console.error('Failed to load usage data:', error);
            }
        }
        
        loadUsageData();
        
        async function buyMembership() {
            try {
                const response = await fetch('/api/payment/initiate', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'Authorization': `Bearer ${token}`
                    },
                    body: JSON.stringify({ amount: 999 })
                });
                
                const data = await response.json();
                
                if (data.success) {
                    // Redirect to Cashfree payment link
                    window.location.href = data.paymentLink;
                } else {
                    alert(data.error || 'Failed to initiate payment');
                }
            } catch (error) {
                alert('An error occurred. Please try again.');
            }
        }
    </script>
</body>
</html>
```

---

## 🎨 Theme Consistency

All new pages (login, register, dashboard) use the same dynamic Ayurvedic theme:
- Gradient backgrounds matching existing pages
- Glassmorphism effects
- Same color scheme (Saffron/Green/White)
- Responsive design
- Smooth animations

---

## 🔒 Security Features

All pages include:
- Right-click disabled
- F12, Ctrl+Shift+I, Ctrl+U disabled
- DevTools detection
- Security alert on page load

---

## 📝 Summary

**Free Tier:**
- 1 clinical assessment per day
- 10 chat messages per day
- Basic features

**Premium Membership (₹999):**
- Unlimited clinical assessments
- 24/7 unlimited chat
- Membership card generation
- Priority support
- 30 days validity

**User Flow:**
1. Register → Select Role → Login
2. Use free features (limited)
3. Upgrade to premium
4. Pay via Cashfree
5. Get unlimited access
6. Generate membership card

---

© 2026 Ananta Labs India | AyurAI Veda
