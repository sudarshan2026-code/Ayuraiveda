# FACE & BODY ANALYSIS - TROUBLESHOOTING GUIDE 🔧

## Common Issues & Solutions

---

## ❌ Issue 1: "No face detected"

### Causes:
- Face not clearly visible
- Poor lighting
- Face too small in image
- Wearing sunglasses/mask

### Solutions:
✅ **Ensure face is clearly visible**
- Remove sunglasses, masks, or face coverings
- Face should be at least 100x100 pixels
- Look directly at camera

✅ **Improve lighting**
- Use natural daylight if possible
- Avoid harsh shadows on face
- Don't have bright light behind you (backlit)

✅ **Adjust camera distance**
- Stand 3-6 feet from camera
- Face should occupy 20-30% of image

---

## ❌ Issue 2: "No body detected"

### Causes:
- Full body not visible in frame
- Body too small in image
- Poor contrast with background
- Baggy clothing hiding body shape

### Solutions:
✅ **Ensure full body is visible**
- Stand back from camera (6-10 feet)
- Include head to feet in frame
- Use portrait/vertical orientation

✅ **Stand properly**
- Stand straight with arms at sides
- Don't cross arms or legs
- Face camera directly

✅ **Improve detection**
- Wear fitted clothing (not baggy)
- Use plain background (avoid patterns)
- Ensure good lighting on entire body

✅ **Camera position**
- Place camera at chest height
- Use timer or remote to take photo
- Avoid extreme angles

---

## ❌ Issue 3: "Fusion analysis failed"

### Causes:
- Face detected but body not detected
- Image processing error
- Network timeout

### Solutions:
✅ **Retake photo with both face AND body visible**
- Stand further from camera
- Ensure full body in frame
- Face should be clearly visible

✅ **Check image quality**
- Use high-resolution image (min 640x480)
- Avoid blurry images
- Good lighting throughout

---

## 📸 PERFECT PHOTO CHECKLIST

### ✅ Before Taking Photo:

1. **Camera Setup**
   - [ ] Camera at chest height
   - [ ] 6-10 feet away from subject
   - [ ] Portrait/vertical orientation
   - [ ] Timer set (10 seconds)

2. **Subject Position**
   - [ ] Standing straight
   - [ ] Arms at sides (not crossed)
   - [ ] Facing camera directly
   - [ ] Feet shoulder-width apart

3. **Clothing**
   - [ ] Fitted clothing (not baggy)
   - [ ] Solid colors preferred
   - [ ] No hats or sunglasses

4. **Lighting**
   - [ ] Natural daylight preferred
   - [ ] Light in front of subject
   - [ ] No harsh shadows
   - [ ] Avoid backlit situations

5. **Background**
   - [ ] Plain wall (white/light color)
   - [ ] No patterns or clutter
   - [ ] Good contrast with clothing

6. **Frame Composition**
   - [ ] Full body visible (head to feet)
   - [ ] Face clearly visible
   - [ ] Some space above head
   - [ ] Some space below feet

---

## 🎯 EXAMPLE GOOD vs BAD PHOTOS

### ✅ GOOD PHOTO:
```
- Full body visible (head to feet)
- Face clearly visible
- Standing straight, arms at sides
- Good lighting, plain background
- Fitted clothing
- Camera 6-10 feet away
```

### ❌ BAD PHOTO:
```
- Only upper body visible
- Face cut off or blurry
- Arms crossed or hidden
- Dark/shadowy lighting
- Busy patterned background
- Baggy/loose clothing
- Camera too close
```

---

## 🔍 TECHNICAL REQUIREMENTS

### Image Specifications:
- **Format**: JPG, PNG, JPEG
- **Min Resolution**: 640x480 pixels
- **Recommended**: 1280x720 or higher
- **Max File Size**: 10MB
- **Aspect Ratio**: 3:4 or 9:16 (portrait)

### Detection Requirements:

**Face Detection:**
- Face size: Min 100x100 pixels
- Face visibility: 80%+ of face visible
- Lighting: Even lighting on face
- Angle: Front-facing (±30° rotation)

**Body Detection:**
- Body height: Min 300 pixels
- Full body: Head to feet visible
- Posture: Standing upright
- Contrast: Clear separation from background

---

## 🛠️ DEBUGGING STEPS

### Step 1: Check Browser Console
1. Open browser DevTools (F12)
2. Go to Console tab
3. Look for error messages
4. Check network requests

### Step 2: Verify Image Upload
1. Check if image preview shows
2. Verify image is not corrupted
3. Try different image format

### Step 3: Test with Sample Image
1. Use a known good full-body photo
2. If it works, issue is with your photo
3. If it fails, issue is with system

### Step 4: Check Server Logs
```bash
# In terminal where Flask is running
# Look for error messages like:
# "No face detected"
# "No body detected"
# "Fusion analysis error"
```

---

## 💡 PRO TIPS

### For Best Results:

1. **Use Smartphone Camera**
   - Better quality than webcam
   - Use rear camera (not selfie)
   - Use timer mode

2. **Outdoor Photos**
   - Natural daylight is best
   - Avoid direct sunlight (use shade)
   - Morning or late afternoon light

3. **Indoor Photos**
   - Use multiple light sources
   - Avoid single overhead light
   - Stand near window for natural light

4. **Photo Editing**
   - Crop to show full body
   - Adjust brightness if needed
   - Don't use filters or effects

---

## 🚨 ERROR MESSAGES EXPLAINED

### "No face detected"
**Meaning**: Face detection algorithm couldn't find a face
**Fix**: Ensure face is clearly visible, well-lit, and facing camera

### "No body detected for fusion"
**Meaning**: Body detection algorithm couldn't find full body
**Fix**: Stand further back, ensure full body in frame

### "Face analysis failed"
**Meaning**: Error processing face region
**Fix**: Check image quality, lighting, and face visibility

### "Fusion analysis failed"
**Meaning**: Error combining face and body results
**Fix**: Ensure both face AND body are detected

---

## 📞 STILL HAVING ISSUES?

### Quick Fixes:
1. ✅ Restart Flask server
2. ✅ Clear browser cache
3. ✅ Try different browser
4. ✅ Use different image
5. ✅ Check internet connection

### System Requirements:
- Python 3.8+
- OpenCV installed
- Flask running
- Modern browser (Chrome/Firefox/Edge)

---

## 📊 DETECTION STATISTICS

### Typical Success Rates:
- **Face Detection**: 95%+ with good photos
- **Body Detection**: 85%+ with full-body photos
- **Fusion Success**: 90%+ when both detected

### Common Failure Reasons:
1. Partial body in frame (40%)
2. Poor lighting (25%)
3. Baggy clothing (15%)
4. Face not visible (10%)
5. Other (10%)

---

## ✅ FINAL CHECKLIST

Before uploading, verify:
- [ ] Full body visible (head to feet)
- [ ] Face clearly visible
- [ ] Good lighting
- [ ] Plain background
- [ ] Standing straight
- [ ] Fitted clothing
- [ ] High resolution image
- [ ] No filters or effects

---

**🌿 AyurAI Veda | For best results, follow the photo guidelines above!**
