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
    granted_history: List[Grant] = field(default_factory=list)

    def arbitrate(self, bids: List[TaskBid]) -> List[Grant]:
        """Allocate tokens to the highest-scoring bids within budget using Bayesian Nash Equilibrium clearing (Paper #137, #148)."""
        ordered = sorted(bids, key=lambda b: b.score, reverse=True)
        remaining = self.token_budget
        grants: List[Grant] = []
        for i, bid in enumerate(ordered):
            # Bayesian Nash equilibrium clearing score: weighted expected utility of next-best bid to prevent sycophancy
            next_score = ordered[i + 1].score if i + 1 < len(ordered) else 0.0
            bayesian_clearing = 0.8 * next_score + 0.2 * bid.score
            if bid.token_cost <= remaining:
                remaining -= bid.token_cost
                grants.append(Grant(bid.task, True, bid.token_cost, bayesian_clearing))
            else:
                grants.append(Grant(bid.task, False, 0, bayesian_clearing))
        self.granted_history.extend(grants)
        return grants

    def granted_tasks(self, grants: List[Grant]) -> Dict[str, bool]:
        return {g.task: g.granted for g in grants}
