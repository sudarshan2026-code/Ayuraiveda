# Face Analysis Feature - Installation Guide

## 🎯 Overview
The Face Analysis feature uses AI to detect facial features and predict Ayurvedic dosha (Vata, Pitta, Kapha) based on visual characteristics.

## 📦 Required Packages

### Install all dependencies:
```bash
pip install -r requirements.txt
```

### Or install individually:
```bash
pip install Flask==3.0.0
pip install reportlab==4.0.7
pip install groq==0.4.1
pip install opencv-python==4.8.1.78
pip install mediapipe==0.10.8
pip install numpy==1.24.3
pip install Pillow==10.1.0
```

## 🔧 Technology Stack

### 1. **OpenCV (opencv-python)**
- Image processing and manipulation
- Color space conversions
- Feature extraction

### 2. **MediaPipe**
- Face detection using Face Mesh
- Facial landmark detection
- Real-time face tracking

### 3. **NumPy**
- Numerical computations
- Array operations
- Statistical calculations

### 4. **Pillow (PIL)**
- Image format conversions
- Base64 encoding/decoding
- Image preprocessing

## 🚀 How It Works

### 1. **Image Input**
- Upload image from device
- Capture photo using webcam
- Supports JPG, PNG formats

### 2. **Face Detection**
- MediaPipe Face Mesh detects face
- Extracts 468 facial landmarks
- Calculates bounding box

### 3. **Feature Extraction**
- **Skin Brightness**: Mean grayscale value (0-255)
- **Redness**: Average red channel intensity
- **Face Ratio**: Width/Height proportion
- **Skin Texture**: Laplacian variance (roughness)

### 4. **Dosha Scoring (Rule-Based)**

#### Vata Indicators:
- Low brightness (< 100) → Dry, thin skin
- Narrow face ratio (< 0.75) → Angular features
- High texture variance (> 500) → Rough skin

#### Pitta Indicators:
- High redness (> 140) → Warm, sensitive skin
- Medium face ratio (0.75-0.9) → Balanced features
- Moderate brightness → Normal skin tone

#### Kapha Indicators:
- High brightness (> 160) → Oily, smooth skin
- Wide face ratio (> 0.9) → Round features
- Low texture variance (< 200) → Smooth skin

### 5. **Output**
- Dosha percentages (Vata, Pitta, Kapha)
- Dominant dosha identification
- Risk level assessment
- Personalized recommendations
- Diet and lifestyle suggestions

## 📊 Features

✅ **Image Upload** - Upload from device
✅ **Camera Capture** - Real-time photo capture
✅ **Face Detection** - Automatic face detection
✅ **Feature Analysis** - Extract visual characteristics
✅ **Dosha Prediction** - Rule-based scoring
✅ **Recommendations** - Personalized diet & lifestyle
✅ **PDF Report** - Download detailed report
✅ **Privacy** - No image storage

## 🔒 Privacy & Security

- Images processed in-memory only
- No data stored on server
- Secure base64 transmission
- GDPR compliant

## 🎨 User Interface

### Personal Details Form:
- Name
- Age
- Gender
- Location

### Image Input Options:
- 📁 Upload Image button
- 📸 Use Camera button

### Results Display:
- Detected features (brightness, redness, ratio, texture)
- Dosha meters (visual bars)
- Dominant dosha
- Risk level
- Explanation
- Recommendations (General, Diet, Lifestyle)

## 🧪 Testing

### Test with sample images:
```python
from face_analysis_engine import FaceAnalysisEngine

engine = FaceAnalysisEngine()
result = engine.analyze_face('test_image.jpg', input_type='path')

print(f"Dominant Dosha: {result['dominant']}")
print(f"Scores: {result['scores']}")
```

## 🐛 Troubleshooting

### Issue: "No face detected"
**Solution**: 
- Ensure face is clearly visible
- Use front-facing photo
- Good lighting conditions
- Face not too small or large

### Issue: Camera not working
**Solution**:
- Check browser permissions
- Use HTTPS (required for camera access)
- Try different browser

### Issue: Import errors
**Solution**:
```bash
pip uninstall opencv-python opencv-python-headless
pip install opencv-python==4.8.1.78
pip install mediapipe==0.10.8
```

## 📱 Browser Compatibility

✅ Chrome/Edge (Recommended)
✅ Firefox
✅ Safari (iOS 11+)
⚠️ Requires HTTPS for camera access

## 🔄 Integration Points

### Flask Routes:
- `/face-analysis` - Main page
- `/analyze-face` - POST endpoint for analysis

### API Response Format:
```json
{
  "success": true,
  "features": {
    "brightness": 145.2,
    "redness": 132.5,
    "face_ratio": 0.82,
    "texture": 345.6
  },
  "scores": {
    "vata": 25.5,
    "pitta": 45.2,
    "kapha": 29.3
  },
  "dominant": "Pitta",
  "risk": "Moderate",
  "explanation": "Pitta dominance detected...",
  "recommendations": [...],
  "diet_suggestions": {...},
  "lifestyle_tips": {...}
}
```

## 📚 References

- MediaPipe Face Mesh: https://google.github.io/mediapipe/solutions/face_mesh
- OpenCV Documentation: https://docs.opencv.org/
- Ayurvedic Facial Analysis Principles
- Charaka Samhita (Classical Ayurvedic text)

## 🎯 Future Enhancements

- [ ] Multiple face detection
- [ ] Age estimation
- [ ] Emotion detection
- [ ] Skin condition analysis
- [ ] Historical tracking
- [ ] ML model training option

## 💡 Tips for Best Results

1. Use clear, well-lit photos
2. Face should be front-facing
3. Remove glasses if possible
4. Neutral expression recommended
5. Plain background preferred

## 🆘 Support

For issues or questions:
- Check troubleshooting section
- Review error messages
- Test with sample images
- Verify all dependencies installed

---

**AyurAI Veda** | Ancient Wisdom. Intelligent Health.
Powered by Tridosha Intelligence Engine™
