# Hierarchical Clinical Assessment System

## 🎯 Overview

This system implements **STRICT hierarchical reasoning** for Ayurvedic Prakriti determination, following classical principles where **body structure determines base dosha FIRST**, and surface features only provide minor adjustments.

---

## ⚠️ HARD RULES

### Rule #1: Structure First (MANDATORY)
```
You MUST determine BASE DOSHA from BODY STRUCTURE FIRST.
You are NOT allowed to finalize dosha using skin or dryness alone.
```

### Rule #2: Limited Surface Influence
```
Surface features (skin, dryness) can only ADJUST, not REPLACE base dosha.
Maximum adjustment: ±10 points
```

### Rule #3: Correction Rules (ENFORCED)
```
IF BASE DOSHA = Kapha:
  → Vata cannot exceed Kapha

IF structure is NOT lean:
  → Vata must remain below 30%

IF face is rounded:
  → Kapha must be highest or equal highest
```

---

## 📊 Assessment Pipeline

```
┌─────────────────────────────────────────┐
│  STEP 1: DETERMINE BASE DOSHA           │
│  (STRUCTURE ONLY - MANDATORY)           │
│  ├─ Body build: lean/medium/heavy       │
│  ├─ Face shape: angular/oval/round      │
│  └─ Fat distribution: low/mod/high      │
│                                         │
│  OUTPUT: Base Dosha + Initial Scores   │
└─────────────────────────────────────────┘
              ↓
┌─────────────────────────────────────────┐
│  STEP 2: SURFACE ADJUSTMENTS            │
│  (LIMITED - MAX ±10 POINTS)             │
│  ├─ Dryness → +Vata (small)             │
│  ├─ Oiliness → +Kapha (small)           │
│  └─ Heat/Pigmentation → +Pitta (small)  │
└─────────────────────────────────────────┘
              ↓
┌─────────────────────────────────────────┐
│  STEP 3: APPLY CORRECTION RULES         │
│  (HARD CONSTRAINTS)                     │
│  ├─ Enforce base dosha dominance        │
│  ├─ Limit Vata if not lean              │
│  └─ Ensure Kapha if rounded             │
└─────────────────────────────────────────┘
              ↓
┌─────────────────────────────────────────┐
│  STEP 4: NORMALIZE TO PERCENTAGES       │
│  Convert scores to Vata/Pitta/Kapha %  │
└─────────────────────────────────────────┘
              ↓
┌─────────────────────────────────────────┐
│  STEP 5: BALANCED CHECK (STRICT)        │
│  Balanced ONLY if all within 5%         │
│  (Should be rare)                       │
└─────────────────────────────────────────┘
              ↓
┌─────────────────────────────────────────┐
│  STEP 6: FINAL CLASSIFICATION           │
│  Output: Prakriti + Reasoning           │
└─────────────────────────────────────────┘
```

---

## 🏗️ STEP 1: Base Dosha Determination

### Input: Structural Features Only
- `body_frame` (0-1): 0=light, 1=heavy
- `body_width` (0-1): body width
- `body_ratio` (0-1): width/height (roundness)
- `shoulder_width` (0-1)
- `hip_width` (0-1)
- `limb_thickness` (0-1)

### Logic:

#### Rule 1: Heavy + Rounded → Kapha
```python
IF build_score >= 0.6 AND face_roundness >= 0.6:
    BASE DOSHA = Kapha
    Initial Scores = {vata: 20, pitta: 30, kapha: 50}
```

#### Rule 2: Medium-Heavy + Rounded → Kapha
```python
IF build_score >= 0.45 AND face_roundness >= 0.55:
    BASE DOSHA = Kapha
    Initial Scores = {vata: 25, pitta: 30, kapha: 45}
```

#### Rule 3: Lean + Angular → Vata
```python
IF build_score <= 0.35 AND face_roundness <= 0.45:
    BASE DOSHA = Vata
    Initial Scores = {vata: 50, pitta: 30, kapha: 20}
```

#### Rule 4: Medium + Sharp → Pitta
```python
IF 0.4 <= build_score <= 0.55 AND face_roundness <= 0.55:
    BASE DOSHA = Pitta
    Initial Scores = {vata: 25, pitta: 45, kapha: 30}
```

#### Rule 5: Default → Pitta
```python
ELSE:
    BASE DOSHA = Pitta
    Initial Scores = {vata: 30, pitta: 40, kapha: 30}
```

### Output:
- Base Dosha (locked)
- Initial Scores
- Structural Reasoning (list of observations)

---

## 🎨 STEP 2: Surface Adjustments

### Input: Gunas from Surface Features
- `ruksha` (dryness)
- `snigdha` (oiliness)
- `ushna` (heat)

### Adjustment Rules (LIMITED):

#### Dryness → +Vata (Max +10)
```python
IF ruksha > 0.6:
    vata_boost = min(10, (ruksha - 0.6) * 25)
    vata += vata_boost
    kapha -= vata_boost / 2
```

#### Oiliness → +Kapha (Max +10)
```python
IF snigdha > 0.6:
    kapha_boost = min(10, (snigdha - 0.6) * 25)
    kapha += kapha_boost
    vata -= kapha_boost / 2
```

#### Heat → +Pitta (Max +10)
```python
IF ushna > 0.6:
    pitta_boost = min(10, (ushna - 0.6) * 25)
    pitta += pitta_boost
    kapha -= pitta_boost / 2
```

### Key Point:
**Surface features can only adjust ±10 points maximum**

---

## ⚖️ STEP 3: Correction Rules (HARD CONSTRAINTS)

### Rule 1: Base Dosha Protection
```python
IF base_dosha == 'kapha':
    IF vata > kapha:
        # Vata cannot exceed Kapha
        excess = vata - kapha
        vata = kapha
        pitta += excess / 2
        kapha += excess / 2
```

### Rule 2: Vata Limitation for Non-Lean Bodies
```python
IF body_frame >= 0.4:  # Not lean
    vata_percent = (vata / total) * 100
    IF vata_percent > 30:
        # Force Vata below 30%
        vata = total * 0.30
        # Redistribute excess to base dosha
        base_dosha_score += excess
```

### Rule 3: Kapha Enforcement for Rounded Faces
```python
IF body_ratio >= 0.6:  # Rounded face
    max_dosha = max(all_scores)
    IF kapha < max_dosha:
        # Kapha must be highest
        kapha = max_dosha
        vata -= diff * 0.7
        pitta -= diff * 0.3
```

### Rule 4: Pitta Base Protection
```python
IF base_dosha == 'pitta':
    IF vata > pitta:
        # Vata cannot dominate Pitta base
        excess = vata - pitta
        vata = pitta
        pitta += excess * 0.6
        kapha += excess * 0.4
```

---

## 📊 STEP 4: Normalization

```python
total = vata + pitta + kapha

vata_percent = (vata / total) * 100
pitta_percent = (pitta / total) * 100
kapha_percent = (kapha / total) * 100
```

---

## ✅ STEP 5: Balanced Check (STRICT)

```python
max_score = max(vata_percent, pitta_percent, kapha_percent)
min_score = min(vata_percent, pitta_percent, kapha_percent)

IF (max_score - min_score) <= 5:
    OUTPUT: "Balanced (Sama Prakriti)"
ELSE:
    OUTPUT: Dominant combination
```

**Note:** Balanced should be RARE (< 5% of cases)

---

## 🎯 STEP 6: Classification

### Single Dominant (≥45%)
```
IF dominant_score >= 45:
    OUTPUT: "Kapha Predominant" (or Vata/Pitta)
```

### Dual Type (within 10%, both >30%)
```
IF abs(dominant - second) <= 10 AND second >= 30:
    OUTPUT: "Kapha-Pitta Type" (or other combination)
```

### Default
```
OUTPUT: "{Dominant} Predominant"
```

---

## 📝 Example Assessments

### Example 1: Heavy Build + Dry Skin

**Input:**
```json
{
  "body_frame": 0.70,      // Heavy
  "body_ratio": 0.70,      // Rounded
  "skin_texture": 0.80,    // Very dry
  "oiliness": 0.20         // Low oil
}
```

**Processing:**

**STEP 1: Base Dosha**
```
Build score: 0.70 (heavy)
Face roundness: 0.70 (rounded)
→ BASE DOSHA = KAPHA
→ Initial: {vata: 20, pitta: 30, kapha: 50}
```

**STEP 2: Surface Adjustments**
```
Dryness (0.80) detected
→ +Vata adjustment: +5 points
→ Adjusted: {vata: 25, pitta: 30, kapha: 47.5}
```

**STEP 3: Correction Rules**
```
Rule 1: Vata (25) < Kapha (47.5) ✓
Rule 2: Body not lean, Vata check: 24% < 30% ✓
Rule 3: Face rounded, Kapha highest ✓
```

**STEP 4: Normalize**
```
Total: 102.5
Vata: 24.4%
Pitta: 29.3%
Kapha: 46.3%
```

**STEP 5: Balanced Check**
```
Max - Min = 46.3 - 24.4 = 21.9% > 5%
→ NOT Balanced
```

**STEP 6: Classification**
```
Kapha (46.3%) is dominant
→ OUTPUT: "Kapha Predominant"
```

**✅ CORRECT: Structure (Kapha) wins over surface (dryness)**

---

### Example 2: Lean Build + Oily Skin

**Input:**
```json
{
  "body_frame": 0.30,      // Lean
  "body_ratio": 0.40,      // Angular
  "skin_texture": 0.30,    // Smooth
  "oiliness": 0.80         // Very oily
}
```

**Processing:**

**STEP 1: Base Dosha**
```
Build score: 0.30 (lean)
Face roundness: 0.40 (angular)
→ BASE DOSHA = VATA
→ Initial: {vata: 50, pitta: 30, kapha: 20}
```

**STEP 2: Surface Adjustments**
```
Oiliness (0.80) detected
→ +Kapha adjustment: +5 points
→ Adjusted: {vata: 47.5, pitta: 30, kapha: 25}
```

**STEP 3: Correction Rules**
```
No violations (Vata base, lean structure)
```

**STEP 4: Normalize**
```
Total: 102.5
Vata: 46.3%
Pitta: 29.3%
Kapha: 24.4%
```

**STEP 5: Balanced Check**
```
Max - Min = 46.3 - 24.4 = 21.9% > 5%
→ NOT Balanced
```

**STEP 6: Classification**
```
Vata (46.3%) is dominant
→ OUTPUT: "Vata Predominant"
```

**✅ CORRECT: Structure (Vata) maintained despite oily skin**

---

## 🚫 Safety Rules

### Final Safety Check
```python
IF base_dosha in ['kapha', 'pitta']:
    IF final_classification == 'Vata Predominant':
        # VIOLATION: Cannot output Vata-dominant
        # when structure indicates Kapha/Pitta
        RAISE ERROR or FORCE CORRECTION
```

---

## 📊 Output Format

```json
{
  "dosha": {
    "vata": 24.4,
    "pitta": 29.3,
    "kapha": 46.3
  },
  "type": "Kapha Predominant",
  "confidence": 85.0,
  "base_dosha": "kapha",
  "structural_reasoning": [
    "Heavy body build (score: 0.70)",
    "Rounded face shape (ratio: 0.70)",
    "Base Dosha: KAPHA (heavy, rounded structure)"
  ],
  "explanation": "**STEP 1 - Base Dosha (Structure):** KAPHA | Heavy body build (score: 0.70) | Rounded face shape (ratio: 0.70) | Base Dosha: KAPHA (heavy, rounded structure) | **STEP 2 - Surface Adjustments:** Dryness detected (Ruksha: 0.80) → +Vata adjustment | **FINAL RESULT:** Kapha constitution with Vata: 24.4%, Pitta: 29.3%, Kapha: 46.3%"
}
```

---

## 🧪 Test Cases

### Test 1: Heavy + Rounded (Expected: Kapha)
```python
body_frame: 0.75, body_ratio: 0.75
→ Result: Kapha Predominant ✓
```

### Test 2: Lean + Angular (Expected: Vata)
```python
body_frame: 0.25, body_ratio: 0.35
→ Result: Vata Predominant ✓
```

### Test 3: Medium + Balanced (Expected: Pitta)
```python
body_frame: 0.50, body_ratio: 0.50
→ Result: Pitta Predominant ✓
```

### Test 4: Edge Case - Dry + Heavy (Expected: Kapha, NOT Vata)
```python
body_frame: 0.70, skin_texture: 0.80
→ Result: Kapha Predominant ✓
→ Vata limited to <30% ✓
```

---

## ✅ Validation

Run tests:
```bash
python clinical_engine.py
```

Expected output:
```
TEST CASE 1: Heavy Build + Rounded Face
→ BASE DOSHA: KAPHA
→ RESULT: Kapha Predominant
→ Vata: 22%, Pitta: 28%, Kapha: 50% ✓

TEST CASE 4: Dry Skin BUT Heavy Build
→ BASE DOSHA: KAPHA
→ RESULT: Kapha Predominant (NOT Vata)
→ Vata: 28%, Pitta: 26%, Kapha: 46% ✓
```

---

## 📚 Classical References

### Charaka Samhita
- Vimana Sthana 8: Prakriti determination
- Emphasis on structural features (Sharira Prakriti)

### Sushruta Samhita
- Sharira Sthana 4: Body constitution
- Structural analysis methods

### Ashtanga Hridaya
- Sharira Sthana 3: Prakriti assessment
- Guna-Dosha relationships

---

## 🎯 Key Takeaways

1. **Structure First** - Always determine base dosha from body structure
2. **Limited Surface Influence** - Skin/dryness can only adjust ±10 points
3. **Correction Rules** - Hard constraints prevent violations
4. **Rare Balanced** - Only if all within 5% (strict)
5. **Safety Checks** - Cannot output Vata-dominant if structure is Kapha/Pitta

---

**AyurAI Veda™** | Hierarchical Clinical Assessment  
Structure-First Reasoning | Classical Ayurvedic Principles  
Powered by Tridosha Intelligence Engine™
