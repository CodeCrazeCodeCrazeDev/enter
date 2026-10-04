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
    research_insights: Dict[str, Dict] = field(default_factory=dict)

    def register_research_insight(self, insight_key: str, insight_data: Dict) -> None:
        """Registers research insight directly into HiveMind token bidding registry."""
        self.research_insights[insight_key] = insight_data
        logger.info(f"Registered research insight in HiveMind: {insight_key}")

    def submit_task_bid(
        self,
        agent_id: str,
        task_id: str,
        bid_tokens: float,
        capability_score: float
    ) -> Dict[str, Any]:
        """Submits a sub-agent task bid for token allocation."""
        bid = TaskBid(
            task=task_id,
            priority=min(1.0, capability_score),
            expected_value=bid_tokens / 100.0,
            token_cost=int(bid_tokens)
        )
        return {
            "status": "registered",
            "agent_id": agent_id,
            "task_id": task_id,
            "score": bid.score
        }

    def arbitrate(self, bids: List[TaskBid]) -> List[Grant]:
        """Allocate tokens to the highest-scoring bids within budget."""
        ordered = sorted(bids, key=lambda b: b.score, reverse=True)
        remaining = self.token_budget
        grants: List[Grant] = []
        for i, bid in enumerate(ordered):
            # Second-price-style signal: clearing score is the next-best bid.
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
