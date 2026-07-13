from __future__ import annotations
from datetime import datetime
from typing import List
from uuid import UUID, uuid4
from pydantic import BaseModel, Field


class Belief(BaseModel):
    """Storage-independent domain Belief wrapping any Entity or Relationship in an epistemic state."""
    belief_id: UUID = Field(default_factory=uuid4)
    target_id: UUID  # Reference to Entity or Relationship being evaluated
    probability: float = Field(default=1.0, ge=0.0, le=1.0)  # P(Belief) Bayesian confidence score
    evidence: List[str] = Field(default_factory=list)  # Evidence hashes or source strings
    last_validated: datetime = Field(default_factory=datetime.utcnow)

    def update_confidence(self, likelihood: float, prior_probability: float) -> None:
        """Update probability using a simple Bayesian recursive rule."""
        # Simple illustration of a Bayesian update step:
        # P(B|E) = (P(E|B) * P(B)) / P(E)
        evidence_probability = likelihood * prior_probability + 0.5 * (1.0 - prior_probability)
        if evidence_probability > 0:
            self.probability = (likelihood * prior_probability) / evidence_probability
        self.last_validated = datetime.utcnow()
