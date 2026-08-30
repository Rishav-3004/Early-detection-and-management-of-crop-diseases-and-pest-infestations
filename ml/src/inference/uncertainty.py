"""
Out-of-Distribution (OOD) & Open-Set Uncertainty Detection Engine.
Prevents hallucinations on unknown diseases, non-supported crops, or anomalous inputs.
"""

import numpy as np
from typing import Dict, Any, List, Optional
from dataclasses import dataclass

@dataclass
class UncertaintyResult:
    is_uncertain: bool
    is_unknown_condition: bool
    confidence_tier: str  # HIGH CONFIDENCE, MEDIUM CONFIDENCE, LOW CONFIDENCE, UNKNOWN CONDITION
    entropy: float
    margin: float
    expert_review_recommended: bool
    advisory_message: Optional[str] = None

class UncertaintyDetector:
    def __init__(
        self,
        high_confidence_thresh: float = 0.80,
        medium_confidence_thresh: float = 0.58,
        max_entropy_thresh: float = 1.95,
        min_margin_thresh: float = 0.12
    ):
        self.high_confidence_thresh = high_confidence_thresh
        self.medium_confidence_thresh = medium_confidence_thresh
        self.max_entropy_thresh = max_entropy_thresh
        self.min_margin_thresh = min_margin_thresh

    def assess_uncertainty(self, probabilities: np.ndarray, top_k_candidates: List[Dict[str, Any]]) -> UncertaintyResult:
        """
        Evaluates prediction uncertainty across probability distribution and candidate margins.
        """
        # 1. Compute Shannon Entropy
        probs = np.clip(probabilities, 1e-7, 1.0)
        entropy = float(-np.sum(probs * np.log(probs)))

        top1_conf = top_k_candidates[0]["confidence"] if len(top_k_candidates) > 0 else 0.0
        top2_conf = top_k_candidates[1]["confidence"] if len(top_k_candidates) > 1 else 0.0
        margin = float(top1_conf - top2_conf)

        # 2. Out-of-Distribution / Unknown Condition Detection
        if top1_conf < 0.40 or (entropy > self.max_entropy_thresh and margin < self.min_margin_thresh):
            return UncertaintyResult(
                is_uncertain=True,
                is_unknown_condition=True,
                confidence_tier="UNKNOWN CONDITION",
                entropy=entropy,
                margin=margin,
                expert_review_recommended=True,
                advisory_message="The visual symptom pattern does not closely match supported condition benchmarks. Consultation with an agricultural extension officer is recommended."
            )

        # 3. Low Confidence Condition
        if top1_conf < self.medium_confidence_thresh:
            return UncertaintyResult(
                is_uncertain=True,
                is_unknown_condition=False,
                confidence_tier="LOW CONFIDENCE",
                entropy=entropy,
                margin=margin,
                expert_review_recommended=True,
                advisory_message="Confidence is below 58%. Consider uploading a closer, well-lit photograph or submit for expert verification."
            )

        # 4. Medium Confidence
        if top1_conf < self.high_confidence_thresh:
            return UncertaintyResult(
                is_uncertain=False,
                is_unknown_condition=False,
                confidence_tier="MEDIUM CONFIDENCE",
                entropy=entropy,
                margin=margin,
                expert_review_recommended=False,
                advisory_message="Probable match. Confirm symptoms against local field history before applying major chemical controls."
            )

        # 5. High Confidence
        return UncertaintyResult(
            is_uncertain=False,
            is_unknown_condition=False,
            confidence_tier="HIGH CONFIDENCE",
            entropy=entropy,
            margin=margin,
            expert_review_recommended=False,
            advisory_message=None
        )
