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
    pending_tasks: Dict[str, Dict[str, Any]] = field(default_factory=dict)
    registered_agents: Dict[str, Dict[str, Any]] = field(default_factory=dict)
    active_bids: Dict[str, List[Dict[str, Any]]] = field(default_factory=dict)

    def register_task(
        self,
        task_id: str,
        description: str,
        required_role: str = "Generalist",
        token_reward: float = 100.0,
    ) -> None:
        """Register a new task in the HiveMind execution registry."""
        self.pending_tasks[task_id] = {
            "task_id": task_id,
            "description": description,
            "required_role": required_role,
            "token_reward": token_reward,
        }
        logger.info(f"[HiveMind] Registered task {task_id} requiring role {required_role}")

    def register_agent(
        self,
        agent_id: str,
        roles: List[str],
        initial_tokens: float = 100.0,
    ) -> None:
        """Register a specialized agent in the HiveMind swarm."""
        self.registered_agents[agent_id] = {
            "agent_id": agent_id,
            "roles": roles,
            "tokens": initial_tokens,
        }
        logger.info(f"[HiveMind] Registered agent {agent_id} with roles {roles}")

    def place_bid(self, agent_id: str, task_id: str, bid_amount: float) -> bool:
        """Place a token bid for a task by a registered agent."""
        if agent_id not in self.registered_agents or task_id not in self.pending_tasks:
            return False

        bids = self.active_bids.setdefault(task_id, [])
        bids.append({"agent_id": agent_id, "bid_amount": bid_amount})
        logger.info(f"[HiveMind] Agent {agent_id} placed bid {bid_amount} on task {task_id}")
        return True

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
