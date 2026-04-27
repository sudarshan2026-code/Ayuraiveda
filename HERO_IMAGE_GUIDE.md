# Hero Image Implementation Guide
## AyurAI Veda - Premium Hero Section

---

## 📸 Step 1: Get Your Hero Image

### Option A: AI Image Generation (Recommended)
Use **Midjourney**, **DALL-E 3**, or **Leonardo.ai** with this prompt:

```
Ultra HD 4K hero image for Ayurvedic AI health platform. 
Bright morning sunlight illuminating fresh Ayurvedic herbs 
(tulsi leaves, neem, golden turmeric root, fresh ginger) 
arranged on clean white marble surface. Soft natural shadows, 
warm color palette (sage green #2A9D8F, golden yellow #F4A261, 
cream white #FFF8F0). Modern minimalist composition with empty 
space on right side for text overlay. Premium health-tech 
aesthetic, Apple-style clean design. Soft focus background, 
sharp foreground herbs. Natural daylight, no artificial elements. 
Professional product photography style, 16:9 aspect ratio.
```

### Option B: Stock Photos
**Unsplash** (Free):
- Search: "ayurvedic herbs bright sunlight"
- Search: "turmeric ginger natural light minimal"
- Search: "herbal medicine modern clean"

**Recommended Images:**
1. https://unsplash.com/photos/[ayurvedic-herbs]
2. https://unsplash.com/photos/[turmeric-ginger]
3. https://unsplash.com/photos/[herbal-wellness]

---

## 📁 Step 2: Save Your Image

### File Naming:
```
hero-ayurveda.jpg          (Main hero image)
hero-ayurveda-mobile.jpg   (Mobile optimized)
hero-ayurveda.webp         (WebP format for performance)
```

### File Location:
```
Ayurveda/
└── static/
    └── images/
        ├── hero-ayurveda.jpg         ← Place here
        ├── hero-ayurveda-mobile.jpg  ← Place here
        └── hero-ayurveda.webp        ← Place here
```

### Image Specifications:
- **Desktop:** 1920x1080px (16:9), ~500KB
- **Mobile:** 1080x1920px (9:16), ~300KB
- **Format:** JPG (primary), WebP (optimized)
- **Quality:** 85% compression

---

## 💻 Step 3: Image Optimization

### Online Tools (Free):
1. **TinyPNG** - https://tinypng.com/
   - Upload your image
   - Download compressed version
   - Reduces size by 60-70%

2. **Squoosh** - https://squoosh.app/
   - Upload image
   - Convert to WebP
   - Adjust quality to 85%

3. **CloudConvert** - https://cloudconvert.com/
   - Convert JPG to WebP
   - Batch processing

### Command Line (Advanced):
```bash
# Install ImageMagick
# Convert to WebP
magick hero-ayurveda.jpg -quality 85 hero-ayurveda.webp

# Resize for mobile
magick hero-ayurveda.jpg -resize 1080x1920 hero-ayurveda-mobile.jpg
```

---

## 🎨 Step 4: Implementation Code

### HTML Structure (Already in index_dynamic.html):
```html
<!-- Background Images -->
<div class="bg-container">
    <!-- Replace these Unsplash URLs with your hero image -->
    <div class="bg-image active" style="background-image: url('{{ url_for('static', filename='images/hero-ayurveda.jpg') }}');"></div>
</div>
<div class="bg-overlay"></div>
```

### CSS (Already Implemented):
```css
.bg-container {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    z-index: -2;
}

.bg-image {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background-size: cover;
    background-position: center;
    background-repeat: no-repeat;
}

.bg-overlay {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: rgba(0, 0, 0, 0.4); /* Adjust darkness */
    z-index: -1;
}
```

---

## 🚀 Step 5: Update index_dynamic.html

Replace the current Unsplash URLs with your hero image:

```html
<!-- BEFORE (Current) -->
<div class="bg-image" id="bg-vata-1" style="background-image: url('https://images.unsplash.com/photo-1502082553048-f009c37129b9?w=1920&q=80');"></div>

<!-- AFTER (Your Hero Image) -->
<div class="bg-image active" style="background-image: url('{{ url_for('static', filename='images/hero-ayurveda.jpg') }}');"></div>
```

---

## 📱 Step 6: Responsive Images

### For Better Performance:
```html
<div class="bg-container">
    <!-- Desktop -->
    <picture>
        <source 
            media="(min-width: 768px)" 
            srcset="{{ url_for('static', filename='images/hero-ayurveda.webp') }}"
            type="image/webp">
        <source 
            media="(min-width: 768px)" 
            srcset="{{ url_for('static', filename='images/hero-ayurveda.jpg') }}">
        
        <!-- Mobile -->
        <source 
            media="(max-width: 767px)" 
            srcset="{{ url_for('static', filename='images/hero-ayurveda-mobile.webp') }}"
            type="image/webp">
        <source 
            media="(max-width: 767px)" 
            srcset="{{ url_for('static', filename='images/hero-ayurveda-mobile.jpg') }}">
        
        <div class="bg-image active" style="background-image: url('{{ url_for('static', filename='images/hero-ayurveda.jpg') }}');"></div>
    </picture>
</div>
```

---

## 🎯 Step 7: Adjust Overlay Darkness

### Light Image (Bright Herbs):
```css
.bg-overlay {
    background: rgba(0, 0, 0, 0.3); /* Lighter overlay */
}
```

### Dark Image:
```css
.bg-overlay {
    background: rgba(0, 0, 0, 0.5); /* Darker overlay */
}
```

### No Overlay (Very Bright Image):
```css
.bg-overlay {
    background: rgba(0, 0, 0, 0.2); /* Minimal overlay */
}
```

---

## ✨ Step 8: Text Positioning

### Current Setup (Centered):
```css
.container {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
}
```

### Left-Aligned Text:
```css
.container {
    align-items: flex-start;
    padding-left: 5%;
}
```

### Right-Aligned Text:
```css
.container {
    align-items: flex-end;
    padding-right: 5%;
}
```

---

## 🔍 Step 9: Testing Checklist

### Visual Tests:
- [ ] Image loads on desktop
- [ ] Image loads on mobile
- [ ] Text is readable over image
- [ ] Overlay darkness is appropriate
- [ ] Image doesn't pixelate
- [ ] Colors match brand (greens, golds)

### Performance Tests:
- [ ] Image loads in < 2 seconds
- [ ] File size < 500KB (desktop)
- [ ] File size < 300KB (mobile)
- [ ] WebP format works
- [ ] Fallback JPG works

### Responsive Tests:
- [ ] Looks good at 1920px
- [ ] Looks good at 1366px
- [ ] Looks good at 768px
- [ ] Looks good at 375px
- [ ] Looks good at 320px

---

## 🎨 Step 10: Color Palette Reference

### Your Brand Colors:
```css
--vata-primary: #F4A261;   /* Golden Orange */
--vata-accent: #E9C46A;    /* Warm Yellow */

--pitta-primary: #E76F51;  /* Coral Red */
--pitta-accent: #FFD166;   /* Bright Yellow */

--kapha-primary: #264653;  /* Deep Teal */
--kapha-accent: #2A9D8F;   /* Sage Green */
```

### Hero Image Should Include:
- ✅ Sage green (#2A9D8F) - Herbs, leaves
- ✅ Golden yellow (#F4A261) - Turmeric, ginger
- ✅ Cream white (#FFF8F0) - Background, marble
- ✅ Natural browns - Wooden elements
- ✅ Soft lighting - Morning sunlight

---

## 📦 Quick Start Commands

### 1. Download Image:
```bash
# Save to correct location
# Windows:
move hero-ayurveda.jpg C:\Users\jayde\Documents\Ayurveda\static\images\

# Mac/Linux:
mv hero-ayurveda.jpg ~/Documents/Ayurveda/static/images/
```

### 2. Optimize Image:
- Visit https://tinypng.com/
- Upload hero-ayurveda.jpg
- Download compressed version
- Replace original file

### 3. Test Locally:
```bash
# Run your Flask app
python app.py

# Open browser
http://127.0.0.1:5000
```

---

## 🎯 Expected Result

### Desktop View:
```
┌─────────────────────────────────────────────────┐
│                                                 │
│  [Bright Ayurvedic Herbs Image]                │
│                                                 │
│         AyurAI Veda                            │
│    Ancient Wisdom. Intelligent Health.         │
│                                                 │
│    [Current Cycle: Vata Time]                  │
│                                                 │
│  [Start Assessment] [Chat with AyurVaani]      │
│                                                 │
└─────────────────────────────────────────────────┘
```

### Mobile View:
```
┌─────────────────┐
│                 │
│  [Hero Image]   │
│                 │
│  AyurAI Veda   │
│  Ancient Wisdom │
│                 │
│  [Cycle Info]   │
│                 │
│  [Assessment]   │
│  [Chat]         │
│                 │
└─────────────────┘
```

---

## 🚨 Troubleshooting

### Image Not Showing:
1. Check file path is correct
2. Verify file exists in `static/images/`
3. Clear browser cache (Ctrl+Shift+R)
4. Check browser console for errors

### Image Too Dark:
```css
.bg-overlay {
    background: rgba(0, 0, 0, 0.2); /* Reduce opacity */
}
```

### Image Too Bright:
```css
.bg-overlay {
    background: rgba(0, 0, 0, 0.6); /* Increase opacity */
}
```

### Text Not Readable:
```css
.logo, .subtitle {
    text-shadow: 2px 2px 8px rgba(0, 0, 0, 0.8); /* Stronger shadow */
}
```

### Image Pixelated:
- Use higher resolution (minimum 1920x1080)
- Reduce compression quality
- Use original uncompressed image

---

## 📞 Next Steps

1. **Get your hero image** (AI generation or stock photo)
2. **Optimize it** (compress to ~500KB)
3. **Save to** `static/images/hero-ayurveda.jpg`
4. **Update** `index_dynamic.html` with new image path
5. **Test** on desktop and mobile
6. **Adjust** overlay darkness if needed

---

## ✅ Checklist

- [ ] Hero image obtained (AI or stock)
- [ ] Image optimized (< 500KB)
- [ ] Image saved to `static/images/`
- [ ] index_dynamic.html updated
- [ ] Tested on desktop
- [ ] Tested on mobile
- [ ] Text is readable
- [ ] Colors match brand
- [ ] Performance is good

---

**Your hero section is ready! Just add your image and you're done!** 🎉

**Current Status:** ✅ Code implemented, waiting for hero image
**Action Required:** Upload your hero image to `static/images/hero-ayurveda.jpg`
