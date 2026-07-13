from __future__ import annotations
from typing import List, Dict, Any, Optional


class ActiveLearningEngine:
    """Active Learning engine designed to query high-entropy/uncertain areas of the World Model."""

    def __init__(self, confidence_threshold: float = 0.75) -> None:
        self.confidence_threshold = confidence_threshold

    def calculate_uncertainty_entropy(self, probabilities: List[float]) -> float:
        """Calculate Shannon-like uncertainty deviation index over a list of probability estimates."""
        if not probabilities:
            return 0.0
        return sum(1.0 - p for p in probabilities) / len(probabilities)

    def generate_probe_queries(self, beliefs: List[Dict[str, Any]]) -> List[str]:
        """Generate targeted probes/queries targeting high-entropy belief structures."""
        probes = []
        for b in beliefs:
            strength = b.get("strength", 0.5)
            # High uncertainty lies when strength is close to 0.5 (random/unknown)
            # If strength is less than our threshold, it is high entropy/uncertain
            if strength < self.confidence_threshold:
                belief_id = b.get("belief_id")
                hypothesis = b.get("hypothesis", "")
                probes.append(f"Investigate high-uncertainty belief [{belief_id}]: {hypothesis}")
        return probes
