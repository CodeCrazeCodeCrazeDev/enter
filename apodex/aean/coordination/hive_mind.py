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

    def register_research_insight(
        self,
        task: str,
        priority: float = 0.8,
        expected_value: float = 0.75,
        token_cost: int = 10
    ) -> Grant:
        """Register a research insight bid from ResearchOS into Hive Mind arbitration."""
        bid = TaskBid(task=task, priority=priority, expected_value=expected_value, token_cost=token_cost)
        grants = self.arbitrate([bid])
        return grants[0] if grants else Grant(task=task, granted=False, tokens=0, clearing_score=0.0)

    def arbitrate(self, bids: List[TaskBid]) -> List[Grant]:
        """Allocate tokens to highest-scoring bids with sycophancy penalty mitigation."""
        # Detect sycophantic duplicate bids with identical priority and expected value
        seen_scores: Dict[float, int] = {}
        for b in bids:
            s = round(b.score, 4)
            seen_scores[s] = seen_scores.get(s, 0) + 1

        def effective_score(b: TaskBid) -> float:
            base = b.score
            s = round(base, 4)
            # Apply sycophancy dampening factor if duplicate scores exist in bidding batch
            if seen_scores.get(s, 0) > 1:
                return base * 0.85
            return base

        ordered = sorted(bids, key=effective_score, reverse=True)
        remaining = self.token_budget
        grants: List[Grant] = []
        for i, bid in enumerate(ordered):
            # Second-price-style signal: clearing score is the next-best bid.
            clearing = effective_score(ordered[i + 1]) if i + 1 < len(ordered) else 0.0
            if bid.token_cost <= remaining:
                remaining -= bid.token_cost
                grants.append(Grant(bid.task, True, bid.token_cost, clearing))
            else:
                grants.append(Grant(bid.task, False, 0, clearing))
        self.granted_history.extend(grants)
        return grants

    def granted_tasks(self, grants: List[Grant]) -> Dict[str, bool]:
        return {g.task: g.granted for g in grants}
