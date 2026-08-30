from __future__ import annotations
import math

class ActiveLearningEngine:
    def __init__(self, confidence_threshold: float = 0.75) -> None:
        self.confidence_threshold = confidence_threshold

    def calculate_uncertainty_entropy(self, strengths: list[float]) -> float:
        if not strengths:
            return 1.0

        # Calculate mean confidence across strengths
        avg_confidence = sum(strengths) / len(strengths)

        # Uncertainty entropy is inversely related to overall confidence
        # High confidence (>0.75) yields low entropy (<0.2)
        # Low confidence yields high entropy
        uncertainty = max(0.0, min(1.0, 1.0 - avg_confidence))
        return round(float(uncertainty), 4)

    def generate_probe_queries(self, beliefs: list[dict]) -> list[str]:
        probes = []
        for b in beliefs:
            strength = b.get("strength", 1.0)
            if strength < self.confidence_threshold:
                belief_id = b.get("belief_id", "unknown_belief")
                hypothesis = b.get("hypothesis", "hypothesis evaluation")
                probes.append(f"Probe query on {belief_id} for {hypothesis}")
        return probes
