# 🎨 Quick Reference — Modern SaaS Layout

## 📁 File Structure

```
static/css/
├── tokens.css       ← Colors, spacing, typography
├── base.css         ← Reset, typography, body
├── layout.css       ← Sidebar, TopBar, MainContent
└── components.css   ← Button, Card, Badge, Alert

templates/
├── _base.html       ← Base template (extend this)
└── home_demo.html   ← Example page
```

## 🎨 Color Palette

```css
--color-primary:        #4F46E5  /* Indigo */
--color-secondary:      #06B6D4  /* Cyan */
--color-accent:         #22C55E  /* Green */
--color-bg:             #F8FAFC  /* Light gray */
--color-surface:        #FFFFFF  /* White */
--color-text-primary:   #0F172A  /* Dark */
--color-text-secondary: #64748B  /* Gray */
--color-border:         #E2E8F0  /* Border */
```

## 📏 Spacing Scale

```css
--space-2:  8px
--space-4:  16px
--space-6:  24px
--space-8:  32px
--space-12: 48px
```

## 🔤 Typography

```css
--text-xs:   12px
--text-sm:   14px
--text-base: 16px
--text-lg:   18px
--text-xl:   20px
--text-2xl:  24px
--text-3xl:  30px
--text-4xl:  36px
```

## 🧩 Component Classes

### Buttons
```html
.btn .btn-primary
.btn .btn-secondary
.btn .btn-outline
.btn .btn-ghost
.btn .btn-lg
.btn .btn-sm
```

### Cards
```html
.card
.card-header
.card-body
.card-footer
```

### Grid
```html
.content-grid .content-grid-2
.content-grid .content-grid-3
.content-grid .content-grid-4
```

### Badges
```html
.badge .badge-primary
.badge .badge-success
.badge .badge-warning
.badge .badge-error
```

### Alerts
```html
.alert .alert-info
.alert .alert-success
.alert .alert-warning
.alert .alert-error
```

## 📱 Responsive Breakpoints

```css
Desktop: > 768px  (sidebar visible)
Mobile:  ≤ 768px  (sidebar hidden, hamburger menu)
```

## 🏗️ Page Template

```html
{% extends "_base.html" %}

{% block title %}Page Title{% endblock %}

{% block breadcrumb %}
  <span class="topbar-breadcrumb-sep">/</span>
  <span class="topbar-breadcrumb-current">Page</span>
{% endblock %}

{% block content %}
  <div class="page-header">
    <h1 class="page-header-title">Title</h1>
    <p class="page-header-description">Description</p>
  </div>

  <div class="card">
    <div class="card-body">
      Content
    </div>
  </div>
{% endblock %}
```

## 🚀 Quick Start

```bash
# Run app
python app.py

# Test demo
http://127.0.0.1:5000/demo
```

## ✅ Checklist

- [ ] Extend `_base.html` for new pages
- [ ] Use design tokens (no hardcoded colors)
- [ ] Follow 8px spacing grid
- [ ] Use semantic HTML
- [ ] Add ARIA labels
- [ ] Test on mobile

---

**AyurAI Veda™** | Quick Reference  
**Version**: 1.0.0
