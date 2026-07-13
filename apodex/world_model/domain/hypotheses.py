from __future__ import annotations
from typing import Any, Dict, List
from uuid import UUID, uuid4
from pydantic import BaseModel, Field


class Hypothesis(BaseModel):
    """Storage-independent speculative Hypothesis used as an anchor for counterfactual testing."""
    hypothesis_id: UUID = Field(default_factory=uuid4)
    description: str
    parent_belief_id: UUID
    test_conditions: Dict[str, Any] = Field(default_factory=dict)
    active_simulations: List[UUID] = Field(default_factory=list)
