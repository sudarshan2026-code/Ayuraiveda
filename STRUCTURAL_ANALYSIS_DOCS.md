# STRUCTURAL FACE PATTERN ANALYSIS SYSTEM

## 🎯 Overview

**Version:** 3.0 - Geometry-Based Dosha Detection  
**Technology:** MediaPipe Face Mesh + Structural Pattern Analysis  
**Approach:** Facial geometry and proportions (NOT color-based)

---

## 🔬 Key Innovation

### Previous System (Color-Based)
- ❌ Used skin brightness and color
- ❌ Affected by lighting conditions
- ❌ Influenced by camera settings
- ❌ Unstable across environments
- ❌ Biased by makeup/filters

### New System (Structural)
- ✅ Uses facial geometry and proportions
- ✅ Independent of lighting conditions
- ✅ Stable across different environments
- ✅ Based on physical structure
- ✅ 468 precise landmarks (MediaPipe)

---

## 📐 Geometric Features Extracted

### 1. Face Dimensions
- **Face Width:** Distance between left and right face edges
- **Face Height:** Distance from forehead to chin
- **Face Ratio:** Width / Height

### 2. Jaw Structure
- **Jaw Width:** Distance between jaw points
- **Forehead Width:** Distance between forehead points
- **Jaw Ratio:** Jaw Width / Forehead Width

### 3. Eye Size
- **Left Eye Width:** Distance between inner and outer corners
- **Right Eye Width:** Distance between inner and outer corners
- **Average Eye Size:** Mean of both eyes

### 4. Lip Thickness
- **Vertical Distance:** From upper lip to lower lip

### 5. Face Fullness
- **Face Area:** Convex hull area of face landmarks
- **Bounding Box Area:** Rectangle area around face
- **Fullness Ratio:** Face Area / Bounding Box Area

---

## ⚖️ Dosha Scoring Logic

### Initialization
```python
vata = 0
pitta = 0
kapha = 0
```

### Scoring Rules

#### 1. Face Shape (Face Ratio)
```python
if face_ratio > 0.9:
    kapha += 2  # Wide, round face
elif face_ratio < 0.75:
    vata += 2   # Narrow, elongated face
else:
    pitta += 2  # Medium, balanced face
```

#### 2. Jaw Structure (Jaw Ratio)
```python
if jaw_ratio > 1.0:
    kapha += 2  # Wide jaw (square/round)
elif jaw_ratio < 0.8:
    vata += 2   # Narrow jaw (pointed)
else:
    pitta += 2  # Angular jaw (triangular)
```

#### 3. Eye Size (Normalized)
```python
eye_size_norm = eye_size / face_width

if eye_size_norm > 0.15:
    kapha += 2  # Large eyes
elif eye_size_norm < 0.10:
    vata += 2   # Small eyes
else:
    pitta += 2  # Medium eyes
```

#### 4. Lip Thickness (Normalized)
```python
lip_thickness_norm = lip_thickness / face_width

if lip_thickness_norm > 0.08:
    kapha += 2  # Thick lips
elif lip_thickness_norm < 0.05:
    vata += 2   # Thin lips
else:
    pitta += 2  # Medium lips
```

#### 5. Face Fullness
```python
if fullness > 0.75:
    kapha += 3  # High fullness (round, fleshy)
elif fullness < 0.60:
    vata += 3   # Low fullness (angular, thin)
else:
    pitta += 2  # Medium fullness (balanced)
```

### Normalization
```python
total = vata + pitta + kapha

vata_percent = (vata / total) * 100
pitta_percent = (pitta / total) * 100
kapha_percent = (kapha / total) * 100
```

---

## 📊 Feature Interpretation Guide

### Face Ratio Thresholds
| Range | Dosha | Description |
|-------|-------|-------------|
| < 0.75 | Vata | Narrow, elongated face |
| 0.75 - 0.9 | Pitta | Medium, balanced face |
| > 0.9 | Kapha | Wide, round face |

### Jaw Ratio Thresholds
| Range | Dosha | Description |
|-------|-------|-------------|
| < 0.8 | Vata | Pointed, narrow jaw |
| 0.8 - 1.0 | Pitta | Angular, triangular jaw |
| > 1.0 | Kapha | Wide, square jaw |

### Eye Size (Normalized) Thresholds
| Range | Dosha | Description |
|-------|-------|-------------|
| < 0.10 | Vata | Small eyes |
| 0.10 - 0.15 | Pitta | Medium eyes |
| > 0.15 | Kapha | Large eyes |

### Lip Thickness (Normalized) Thresholds
| Range | Dosha | Description |
|-------|-------|-------------|
| < 0.05 | Vata | Thin lips |
| 0.05 - 0.08 | Pitta | Medium lips |
| > 0.08 | Kapha | Full lips |

### Face Fullness Thresholds
| Range | Dosha | Description |
|-------|-------|-------------|
| < 0.60 | Vata | Angular, thin features |
| 0.60 - 0.75 | Pitta | Balanced features |
| > 0.75 | Kapha | Round, full features |

---

## 🔧 Installation

### Requirements
```bash
pip install mediapipe opencv-python numpy pillow
```

### Dependencies
- **mediapipe:** Face mesh landmark detection
- **opencv-python:** Image processing
- **numpy:** Numerical computations
- **pillow:** Image loading

---

## 💻 Usage

### Basic Usage
```python
from structural_face_analysis import StructuralFaceAnalyzer

# Initialize analyzer
analyzer = StructuralFaceAnalyzer()

# Analyze image
result = analyzer.analyze_face("image.jpg", input_type='path')

# Access results
print(f"Dominant Dosha: {result['dominant']}")
print(f"Vata:  {result['scores']['vata']}%")
print(f"Pitta: {result['scores']['pitta']}%")
print(f"Kapha: {result['scores']['kapha']}%")
```

### With Base64 Input
```python
# For web applications
result = analyzer.analyze_face(base64_string, input_type='base64')
```

### Accessing Features
```python
features = result['features']

# Face dimensions
print(f"Face Ratio: {features['face_dimensions']['face_ratio']}")

# Jaw structure
print(f"Jaw Ratio: {features['jaw_structure']['jaw_ratio']}")

# Eye size
print(f"Eye Size: {features['eye_size']['avg_eye_size']}")

# Lip thickness
print(f"Lip Thickness: {features['lip_thickness']['lip_thickness']}")

# Face fullness
print(f"Fullness: {features['face_fullness']['fullness']}")
```

---

## 📋 Output Format

### Success Response
```python
{
    'success': True,
    'features': {
        'face_dimensions': {
            'face_width': 250.45,
            'face_height': 320.12,
            'face_ratio': 0.782
        },
        'jaw_structure': {
            'jaw_width': 180.23,
            'forehead_width': 210.56,
            'jaw_ratio': 0.856
        },
        'eye_size': {
            'left_eye_width': 30.12,
            'right_eye_width': 29.87,
            'avg_eye_size': 30.00
        },
        'lip_thickness': {
            'lip_thickness': 15.34
        },
        'face_fullness': {
            'face_area': 45678.90,
            'bbox_area': 65432.10,
            'fullness': 0.698
        }
    },
    'scores': {
        'vata': 18.2,
        'pitta': 54.5,
        'kapha': 27.3
    },
    'dominant': 'Pitta',
    'risk': 'High',
    'explanation': 'Pitta dominance detected due to balanced facial proportions...',
    'face_detected': True
}
```

### Error Response
```python
{
    'error': 'No face detected in the image'
}
```

---

## 🧪 Testing

### Run Test Suite
```bash
python test_structural_analysis.py
```

### Test Single Image
```python
from structural_face_analysis import StructuralFaceAnalyzer

analyzer = StructuralFaceAnalyzer()
result = analyzer.analyze_face("test_face.jpg", input_type='path')

if 'error' not in result:
    print(f"✅ Analysis successful!")
    print(f"Dominant: {result['dominant']}")
else:
    print(f"❌ Error: {result['error']}")
```

---

## 🎯 Example Scenarios

### Scenario 1: Vata Type
**Features:**
- Face Ratio: 0.70 (narrow)
- Jaw Ratio: 0.75 (pointed)
- Eye Size: 0.09 (small)
- Lip Thickness: 0.04 (thin)
- Fullness: 0.55 (angular)

**Expected Result:** Vata dominance

### Scenario 2: Pitta Type
**Features:**
- Face Ratio: 0.82 (medium)
- Jaw Ratio: 0.90 (angular)
- Eye Size: 0.12 (medium)
- Lip Thickness: 0.06 (medium)
- Fullness: 0.68 (balanced)

**Expected Result:** Pitta dominance

### Scenario 3: Kapha Type
**Features:**
- Face Ratio: 0.95 (wide)
- Jaw Ratio: 1.05 (wide)
- Eye Size: 0.17 (large)
- Lip Thickness: 0.09 (full)
- Fullness: 0.80 (round)

**Expected Result:** Kapha dominance

---

## 🔬 MediaPipe Landmarks Used

### Key Landmark Indices
- **10:** Forehead top
- **152:** Chin bottom
- **234:** Left face edge
- **454:** Right face edge
- **172:** Left jaw point
- **397:** Right jaw point
- **33:** Left eye inner corner
- **133:** Left eye outer corner
- **362:** Right eye inner corner
- **263:** Right eye outer corner
- **0:** Upper lip top
- **17:** Lower lip bottom

**Total Landmarks:** 468 facial points

---

## 📈 Advantages Over Color-Based System

### 1. Lighting Independence
- ✅ Works in bright light
- ✅ Works in dim light
- ✅ Works with different color temperatures

### 2. Environmental Stability
- ✅ Indoor/outdoor consistency
- ✅ Different camera settings
- ✅ Various image qualities

### 3. Accuracy
- ✅ Based on physical structure
- ✅ Follows Ayurvedic principles
- ✅ More reliable predictions

### 4. Robustness
- ✅ Not affected by makeup
- ✅ Not affected by filters
- ✅ Not affected by skin tone

---

## 🌿 Ayurvedic Principles

### Vata Characteristics
- **Face:** Narrow, elongated, angular
- **Jaw:** Pointed, narrow
- **Eyes:** Small, deep-set
- **Lips:** Thin, dry
- **Overall:** Thin, bony structure

### Pitta Characteristics
- **Face:** Medium, balanced, triangular
- **Jaw:** Angular, defined
- **Eyes:** Medium, penetrating
- **Lips:** Medium, well-defined
- **Overall:** Athletic, proportionate

### Kapha Characteristics
- **Face:** Round, wide, full
- **Jaw:** Wide, square
- **Eyes:** Large, attractive
- **Lips:** Full, thick
- **Overall:** Soft, fleshy structure

---

## ⚠️ Important Notes

### Best Practices
1. Use clear, front-facing photos
2. Ensure good face visibility
3. Avoid extreme angles
4. Remove obstructions (hair, glasses)
5. Use neutral expressions

### Limitations
- Requires visible face landmarks
- Works best with frontal views
- May be affected by extreme facial expressions
- Requires clear image quality

### Disclaimer
This system provides educational and preventive health insights only.  
It is NOT a medical diagnosis platform.  
Always consult qualified healthcare professionals for medical advice.

---

## 🔄 Integration with Existing System

### Replace Color-Based Engine
```python
# OLD (Color-based)
from face_analysis_engine import FaceAnalysisEngine
engine = FaceAnalysisEngine()

# NEW (Structural)
from structural_face_analysis import StructuralFaceAnalyzer
analyzer = StructuralFaceAnalyzer()
```

### API Compatibility
Both systems return the same output format:
```python
{
    'success': True,
    'scores': {'vata': X, 'pitta': Y, 'kapha': Z},
    'dominant': 'Dosha Name',
    'explanation': '...'
}
```

---

## 📚 References

### Ayurvedic Texts
- Charaka Samhita (Darshana Pariksha)
- Sushruta Samhita (Physical examination)
- Ashtanga Hridaya (Constitutional analysis)

### Technical References
- MediaPipe Face Mesh: https://google.github.io/mediapipe/
- OpenCV Documentation: https://opencv.org/
- Ayurvedic Prakriti Analysis

---

## 🚀 Future Enhancements

### Planned Features
- [ ] Multi-angle face analysis
- [ ] Temporal analysis (video input)
- [ ] Age-adjusted scoring
- [ ] Gender-specific thresholds
- [ ] Confidence scoring
- [ ] Batch processing

### Research Directions
- [ ] Clinical validation studies
- [ ] Machine learning integration
- [ ] Cross-cultural adaptation
- [ ] Mobile optimization

---

## 📞 Support

For questions or issues:
1. Check the test suite: `python test_structural_analysis.py`
2. Review the documentation
3. Ensure all dependencies are installed
4. Verify image quality and format

---

## 📄 License

This project is for educational purposes.  
Please respect traditional knowledge and use ethically.

---

## 🙏 Acknowledgments

- Ancient Ayurvedic scholars and practitioners
- MediaPipe team at Google
- OpenCV community
- NEP 2020 initiative for promoting IKS

---

**AyurAI Veda™** | Reviving Indian Knowledge Systems through AI

Powered by **Structural Face Pattern Analysis™** | NEP 2020 Aligned

---

## 📊 Quick Reference

### Command Summary
```bash
# Install dependencies
pip install mediapipe opencv-python numpy pillow

# Run test suite
python test_structural_analysis.py

# Analyze single image
python structural_face_analysis.py
```

### Code Summary
```python
from structural_face_analysis import StructuralFaceAnalyzer

analyzer = StructuralFaceAnalyzer()
result = analyzer.analyze_face("image.jpg", input_type='path')

print(f"Dominant: {result['dominant']}")
print(f"Vata: {result['scores']['vata']}%")
print(f"Pitta: {result['scores']['pitta']}%")
print(f"Kapha: {result['scores']['kapha']}%")
```

---

**That's it! Your structural face analysis system is ready to use.**
