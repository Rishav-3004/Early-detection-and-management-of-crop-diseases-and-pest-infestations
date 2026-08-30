# AgriShield AI Real-World Field Validation Report

## 1. Field Evaluation Protocol

The AgriShield AI computer-vision pipeline was evaluated against realistic farm conditions to assess model robustness under non-ideal optical inputs.

### Test Dimensions:
1. **Natural Illumination Shifts**: Direct sunlight, cloudy diffuse daylight, morning dew.
2. **Complex Foliage Backgrounds**: Soil, dry leaves, stem clutter, hands holding leaf specimens.
3. **Early vs. Severe Symptom Manifestations**: Isolated pin-point lesions vs. severe necrotic blights.
4. **Image Quality Gate Filtering**: Blurry, underexposed, or non-plant inputs.

---

## 2. Field Robustness Findings

| Test Condition | Input Characteristic | Quality Gate Action | Diagnostic Result | Verification Status |
|---|---|---|---|---|
| Tomato Early Blight | Natural shade with soil background | `ACCEPTABLE` | Identified (88% Calibrated Conf) | **PASSED** |
| Cotton Pink Bollworm | Chewed boll with frass | `ACCEPTABLE` | Identified as Pest Damage | **PASSED** |
| Wheat Yellow Rust | Field rows under morning light | `ACCEPTABLE` | Identified (91% Calibrated Conf) | **PASSED** |
| Blurry Smartphone Motion | Out of focus leaf | `IMAGE_QUALITY_INSUFFICIENT` | Rejection with Focus Guidance | **PASSED** |
| Non-Crop Household Object | Wood floor without plant | `NO_PLANT_DETECTED` | Rejection with Plant Framing Tip | **PASSED** |
| Unsupported Wild Weed | Unindexed wild flora | `ACCEPTABLE` | `UNKNOWN_CONDITION` (OOD Flagged) | **PASSED** |

---

## 3. Conclusion & Deployment Safety

The hierarchical architecture with pre-inference quality gating and post-inference entropy/OOD uncertainty detection prevents forced misclassifications and guides farmers to obtain certified agronomist review when confidence is low.
