"""Hive Mind — multi-agent coordination via Agent Token Economics.

The Hive Mind allocates a finite pool of *compute tokens* across the tasks the
organism wants to run each cycle (sense demand, engineer narratives, produce
creative, run funnels, rebalance capital). Engines/tasks submit bids expressing
priority and expected value; the Hive Mind runs a simple second-price-style
arbitration to decide execution order and grants, providing graceful
degradation when tokens are scarce. This models the token-based resource
arbitration described in the AEAN spec without requiring a real message bus.
"""
from __future__ import annotations

import logging
from dataclasses import dataclass, field
from typing import Dict, List, Any

logger = logging.getLogger("aean.hive_mind")


@dataclass
class TaskBid:
    task: str
    priority: float  # 0..1 strategic priority
    expected_value: float  # relative EV of running the task this cycle
    token_cost: int  # tokens required to run

    @property
    def score(self) -> float:
        return self.priority * (0.5 + self.expected_value)


@dataclass
class Grant:
    task: str
    granted: bool
    tokens: int
    clearing_score: float


@dataclass
class HiveMind:
    token_budget: int = 100
    granted_history: List[Grant] = field(default_factory=list)
    registered_insights: Dict[str, Dict[str, Any]] = field(default_factory=dict)

    def register_research_insight(self, insight_id: str, topic: str, value: float) -> None:
        """Registers research insight from Research OS directly into HiveMind token bidding registry."""
        self.registered_insights[insight_id] = {
            "topic": topic,
            "value": value,
            "timestamp": time_now()
        }
        logger.info(f"[HiveMind] Registered research insight '{topic}' [id={insight_id}].")

    def evaluate_synergy(self, bids: List[TaskBid]) -> float:
        """
        Evaluates multi-agent synergy score with sycophancy mitigation.
        Penalizes unanimous agreement when variance is artificially zero without evidence.
        """
        if not bids:
            return 0.0

        scores = [b.score for b in bids]
        mean_score = sum(scores) / len(scores)

        # Variance check
        if len(scores) > 1:
            variance = sum((s - mean_score) ** 2 for s in scores) / (len(scores) - 1)
        else:
            variance = 0.5

        # Sycophancy mitigation penalty: if variance is exactly 0 and score > 0, penalize alignment drift
        sycophancy_penalty = 0.8 if variance < 1e-4 and mean_score > 0 else 1.0

        synergy = mean_score * sycophancy_penalty
        return float(synergy)

    def arbitrate(self, bids: List[TaskBid]) -> List[Grant]:
        """Allocate tokens to the highest-scoring bids within budget."""
        ordered = sorted(bids, key=lambda b: b.score, reverse=True)
        remaining = self.token_budget
        grants: List[Grant] = []
        for i, bid in enumerate(ordered):
            clearing = ordered[i + 1].score if i + 1 < len(ordered) else 0.0
            if bid.token_cost <= remaining:
                remaining -= bid.token_cost
                grants.append(Grant(bid.task, True, bid.token_cost, clearing))
            else:
                grants.append(Grant(bid.task, False, 0, clearing))
        self.granted_history.extend(grants)
        return grants

    def granted_tasks(self, grants: List[Grant]) -> Dict[str, bool]:
        return {g.task: g.granted for g in grants}


def time_now() -> str:
    import datetime
    return datetime.datetime.now(datetime.timezone.utc).isoformat()
