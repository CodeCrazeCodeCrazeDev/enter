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
from typing import Dict, List

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
    token_burn_deflator: float = 1.0
    granted_history: List[Grant] = field(default_factory=list)
    research_insights: List[Dict[str, Any]] = field(default_factory=list)

    def register_research_insight(self, insight: Dict[str, Any]) -> None:
        """Register a research insight from Research OS for token-weighted task bidding."""
        self.research_insights.append(insight)

    def arbitrate(self, bids: List[TaskBid]) -> List[Grant]:
        """Allocate tokens to the highest-scoring bids within budget using token burn deflator."""
        ordered = sorted(bids, key=lambda b: b.score, reverse=True)
        remaining = float(self.token_budget)
        grants: List[Grant] = []
        for i, bid in enumerate(ordered):
            # Apply token burn deflator to token cost
            effective_cost = max(1, int(bid.token_cost * self.token_burn_deflator))
            clearing = ordered[i + 1].score if i + 1 < len(ordered) else 0.0
            if effective_cost <= remaining:
                remaining -= effective_cost
                grants.append(Grant(bid.task, True, effective_cost, clearing))
            else:
                grants.append(Grant(bid.task, False, 0, clearing))
        self.granted_history.extend(grants)
        return grants

    def granted_tasks(self, grants: List[Grant]) -> Dict[str, bool]:
        return {g.task: g.granted for g in grants}
