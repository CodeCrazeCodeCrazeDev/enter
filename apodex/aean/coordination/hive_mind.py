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
    research_registry: Dict[str, Dict[str, Any]] = field(default_factory=dict)
    active_bids: Dict[str, List[Any]] = field(default_factory=dict)

    def register_research_insight(
        self,
        topic: str,
        insight_summary: str,
        confidence: float = 0.95
    ) -> None:
        """Register research insight from Research OS for cross-layer multi-agent execution."""
        self.research_registry[topic] = {
            "topic": topic,
            "summary": insight_summary,
            "confidence": confidence
        }
        logger.info(f"[HiveMind] Registered research insight: {topic}")

    def submit_bid(self, bid: Any) -> None:
        """Submit a bid for a task auction."""
        task_id = getattr(bid, "task_id", getattr(bid, "task", "default_task"))
        self.active_bids.setdefault(task_id, []).append(bid)

    def resolve_auction(self, task_id: str) -> Optional[Any]:
        """Resolve task auction by selecting highest priority/lowest cost bid."""
        bids = self.active_bids.get(task_id, [])
        if not bids:
            return None

        # Sort by score or expected_value/bid_amount
        def get_bid_score(b: Any) -> float:
            if hasattr(b, "score"):
                return float(b.score)
            priority = getattr(b, "priority", 1.0)
            amount = getattr(b, "bid_amount", 100.0)
            return priority * 100.0 / max(1.0, amount)

        sorted_bids = sorted(bids, key=get_bid_score, reverse=True)
        return sorted_bids[0]

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
