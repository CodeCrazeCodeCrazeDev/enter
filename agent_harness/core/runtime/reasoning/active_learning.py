from __future__ import annotations

class ActiveLearningEngine:
    def __init__(self, confidence_threshold: float = 0.75) -> None:
        self.confidence_threshold = confidence_threshold

    def calculate_uncertainty_entropy(self, strengths: list[float]) -> float:
        """Compute uncertainty score as 1 - mean(strengths) bounded in [0, 1]."""
        if not strengths:
            return 1.0  # Maximum uncertainty when no observations exist

        # Compute average belief confidence/strength
        avg_strength = sum(max(0.0, min(1.0, float(s))) for s in strengths) / len(strengths)
        return max(0.0, min(1.0, 1.0 - avg_strength))

    def generate_probe_queries(self, beliefs: list[dict]) -> list[str]:
        probes = []
        for b in beliefs:
            if b.get("strength", 1.0) < self.confidence_threshold:
                probes.append(f"Probe query on {b.get('belief_id')} for {b.get('hypothesis')}")
        return probes
