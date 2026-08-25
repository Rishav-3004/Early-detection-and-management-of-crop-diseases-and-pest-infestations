# AI/ML Architecture & Agronomic Risk Engine

## 1. Machine Learning Abstraction Layer

The platform is designed around the `CropDiagnosisModel` abstract interface:

```python
class CropDiagnosisModel(ABC):
    @abstractmethod
    async def predict(self, image_bytes: bytes, crop_hint: Optional[str] = None, filename: Optional[str] = None) -> DiagnosisOutput:
        pass
```

### Supported Providers:
- **`MockDiagnosisModel`**: Deterministic, high-fidelity mock model computing realistic multi-class disease/pest predictions, ranked alternative candidates (e.g. Tomato Early Blight 91%, Septoria Leaf Spot 5%, Healthy 4%), and canopy surface area damage percentages.
- **`ONNXModel` / `PyTorchModel` / `CloudAPIModel`**: Pluggable vision transformers and convolutional backbones (e.g. EfficientNet, ResNet, Vision Transformer trained on PlantVillage / PlantDoc datasets).

---

## 2. Safety & Diagnostic Thresholds

| Confidence Tier | Threshold | Platform Behavior |
|---|---|---|
| **High Confidence** | &ge; 80% | Confirmed diagnostic match. Standard recommendations rendered. |
| **Medium Confidence** | 60% – 79% | Probable match. Farmer is advised to inspect adjacent foliage and check secondary symptoms. |
| **Low Confidence** | &lt; 60% | Uncertain match. Display prominent warning and encourage submitting the scan for **Agronomist Case Review**. |

> **AI Safety Principle**: The user interface always distinguishes AI probability estimations from guaranteed clinical diagnosis.

---

## 3. Multi-Factor Risk Assessment Algorithm

```text
Risk Score (0–100) = Base Severity Score
                   × Confidence Scaling
                   + Growth Stage Vulnerability Factor (+10 to +15)
                   + Meteorological Multipliers (+8 to +15 for RH ≥ 75% or Rainfall)
                   + Historical Field Recurrence (+5 to +10)
```

### Risk Level Classification:
- **`CRITICAL`** (Score &ge; 80): Urgent intervention needed to avoid severe crop loss.
- **`HIGH`** (Score 60–79): Active sporulation or pest outbreak likely spreading.
- **`MEDIUM`** (Score 35–59): Localized symptoms detected. Routine management advised.
- **`LOW`** (Score &lt; 35): Healthy or minimal stress. Standard preventive scouting.
