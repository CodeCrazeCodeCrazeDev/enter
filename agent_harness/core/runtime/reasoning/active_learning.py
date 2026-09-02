from __future__ import annotations
import math

class ActiveLearningEngine:
    def __init__(self, confidence_threshold: float = 0.75) -> None:
        self.confidence_threshold = confidence_threshold

    def calculate_uncertainty_entropy(self, strengths: list[float]) -> float:
        if not strengths:
            return 1.0
        avg = sum(strengths) / len(strengths)
        variance = sum((s - avg) ** 2 for s in strengths) / len(strengths)
        uncertainty = max(0.0, min(1.0, (1.0 - avg) + 0.5 * math.sqrt(variance)))
        return round(uncertainty, 4)

    def generate_probe_queries(self, beliefs: list[dict]) -> list[str]:
        probes = []
        for b in beliefs:
            if b.get("strength", 1.0) < self.confidence_threshold:
                probes.append(f"Probe query on {b.get('belief_id')} for {b.get('hypothesis')}")
        return probes
