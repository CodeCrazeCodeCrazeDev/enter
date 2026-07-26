from __future__ import annotations
import math
import uuid
from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field


class TheoryNode(BaseModel):
    theory_id: uuid.UUID = Field(default_factory=uuid.uuid4)
    name: str
    target_variable: str
    expected_value: float
    confidence_level: float = 0.95


class EvidenceCard(BaseModel):
    evidence_id: uuid.UUID = Field(default_factory=uuid.uuid4)
    hypothesis_id: uuid.UUID
    empirical_mean: float
    replications_count: int = 1
    sample_size: int = 100


class UncertaintyAnalyzer:
    """
    Evaluates epistemic uncertainty and performs conjugate Beta-Binomial belief updates.
    Enforces automatic contradiction detection and theory promotion loops.
    """

    def __init__(self, decay_rate: float = 0.05) -> None:
        self.decay_rate = decay_rate
        self.active_theories: Dict[uuid.UUID, TheoryNode] = {}

    def calculate_epistemic_entropy(self, alpha: float, beta: float) -> float:
        """Calculates Shannon entropy of Beta distribution as an uncertainty measure."""
        # Standard beta entropy approximation
        total = alpha + beta
        if total <= 0:
            return 1.0
        return - (alpha / total) * math.log(alpha / total) - (beta / total) * math.log(beta / total)

    def update_beliefs_with_decay(
        self,
        prior_alpha: float,
        prior_beta: float,
        successes: int,
        failures: int,
        elapsed_days: float
    ) -> tuple[float, float]:
        """Applies Ebbinghaus Forgetting Curve exponential decay on historical priors before updating."""
        decay_factor = math.exp(-self.decay_rate * elapsed_days)

        # Decay excess evidence beyond uniform prior
        decayed_alpha_excess = max(0.0, prior_alpha - 1.0) * decay_factor
        decayed_beta_excess = max(0.0, prior_beta - 1.0) * decay_factor

        return (1.0 + decayed_alpha_excess + successes, 1.0 + decayed_beta_excess + failures)

    def detect_contradictions(self, evidence: EvidenceCard) -> List[Dict[str, Any]]:
        """Scans active theories for claims contradicting the empirical evidence."""
        contradictions = []
        for theory_id, theory in self.active_theories.items():
            # If evidence mean diverges by > 25% from theory expected value, flag contradiction
            divergence = abs(evidence.empirical_mean - theory.expected_value)
            if divergence > 0.25 * abs(theory.expected_value):
                contradictions.append({
                    "theory_id": theory_id,
                    "theory_name": theory.name,
                    "evidence_mean": evidence.empirical_mean,
                    "expected_value": theory.expected_value,
                    "divergence": divergence,
                    "status": "critical_contradiction"
                })
        return contradictions

    def promote_to_theory(self, hypothesis_name: str, evidence: EvidenceCard) -> Optional[TheoryNode]:
        """Promotes validated hypotheses to TheoryNodes if replications >= 3 and sample size >= 100."""
        if evidence.replications_count >= 3 and evidence.sample_size >= 100:
            theory = TheoryNode(
                name=hypothesis_name,
                target_variable="performance_metric",
                expected_value=evidence.empirical_mean,
                confidence_level=0.95
            )
            self.active_theories[theory.theory_id] = theory
            return theory
        return None
