from __future__ import annotations
from enum import Enum
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field


class CostMode(str, Enum):
    FAST_CHEAP = "fast_cheap"
    BALANCED = "balanced"
    MAX_QUALITY = "max_quality"


class ConfigDelta(BaseModel):
    """Represents a delta patch applied to prompt/workflow configuration."""
    target_id: str  # ID of prompt parameter or workflow node
    delta_type: str  # "prompt", "workflow", "tool_routing"
    old_value: Any
    new_value: Any
    metadata: Dict[str, Any] = Field(default_factory=dict)


class ChangelogEntry(BaseModel):
    """An entry in the immutable evolution changelog."""
    entry_id: str
    timestamp: float
    cost_mode: CostMode
    applied_deltas: List[ConfigDelta]
    verifier_score_before: float
    verifier_score_after: float
    description: str
    metadata: Dict[str, Any] = Field(default_factory=dict)


class MultiObjectiveMetric(BaseModel):
    """Holds individual metrics for scoring."""
    quality: float  # [0.0, 1.0]
    cost: float     # raw metric or estimated token cost [0.0, 1.0] scaled
    latency: float  # elapsed time in seconds or scaled [0.0, 1.0]


def calculate_multiobjective_score(metrics: MultiObjectiveMetric, mode: CostMode) -> float:
    """
    Computes a multi-objective score based on the current CostMode:
    Score = Quality - lambda * Cost - mu * Latency
    """
    if mode == CostMode.FAST_CHEAP:
        # Heavily penalize cost and latency
        lam = 0.5
        mu = 0.4
    elif mode == CostMode.BALANCED:
        # Balanced trade-offs
        lam = 0.2
        mu = 0.2
    else:  # MAX_QUALITY
        # Almost ignore cost/latency, maximize quality
        lam = 0.02
        mu = 0.01

    return max(0.0, metrics.quality - (lam * metrics.cost) - (mu * metrics.latency))


class EvolutionChangelog(BaseModel):
    """Manages the history of changes and rollback operations."""
    history: List[ChangelogEntry] = Field(default_factory=list)
    current_config: Dict[str, Any] = Field(default_factory=dict)

    def apply_change(self, entry: ChangelogEntry) -> None:
        """Applies a change and logs it."""
        self.history.append(entry)
        for delta in entry.applied_deltas:
            self.current_config[delta.target_id] = delta.new_value

    def rollback_last_change(self) -> Optional[ChangelogEntry]:
        """Rolls back the most recent change, returning the entry rolled back."""
        if not self.history:
            return None
        last_entry = self.history.pop()
        # Apply the old values in reverse order to restore previous state
        for delta in reversed(last_entry.applied_deltas):
            self.current_config[delta.target_id] = delta.old_value
        return last_entry
