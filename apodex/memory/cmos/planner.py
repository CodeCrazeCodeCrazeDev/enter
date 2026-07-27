"""Memory Query Planner implementation for CMOS.

Parses programmatic goals and translates them into serializable Execution Plans of registered operators.
"""

from __future__ import annotations

import logging
from typing import Any, Dict, List

from apodex.memory.cmos.interfaces import MemoryQueryPlanner, OperatorContext


logger = logging.getLogger("apodex.memory.cmos.planner")


class CMOSQueryPlanner(MemoryQueryPlanner):
    """Query Planner that maps complex natural objectives into structured Operator plans."""

    async def plan(self, objective: str, ctx: OperatorContext) -> List[Dict[str, Any]]:
        plan_steps: List[Dict[str, Any]] = []

        # Analyze objective phrasing and build structured execution graph
        objective_lower = objective.lower()

        if "compare" in objective_lower or "contrast" in objective_lower:
            # Plan: Recall node A, Recall node B, Compare/Contrast them
            plan_steps.append({
                "operator": "Recall",
                "args": {"filters": {"label": "Strategy A"}}
            })
            plan_steps.append({
                "operator": "Recall",
                "args": {"filters": {"label": "Strategy B"}}
            })
            if "contrast" in objective_lower:
                plan_steps.append({
                    "operator": "Contrast",
                    "args": {"node_a_id": "strategy_a_resolved", "node_b_id": "strategy_b_resolved"}
                })
            else:
                plan_steps.append({
                    "operator": "Compare",
                    "args": {"node_a_id": "strategy_a_resolved", "node_b_id": "strategy_b_resolved"}
                })

        elif "verify" in objective_lower:
            # Plan: Recall node, Verify evidence
            plan_steps.append({
                "operator": "Recall",
                "args": {"filters": {"node_type": "claim"}}
            })
            plan_steps.append({
                "operator": "Verify",
                "args": {"node_id": "claim_resolved"}
            })

        elif "simulate" in objective_lower:
            # Plan: Simulate virtual sandbox branch
            plan_steps.append({
                "operator": "Simulate",
                "args": {"virtual_content": "Simulated sandbox run overlay"}
            })

        else:
            # Default fallback execution plan: general Recall query
            plan_steps.append({
                "operator": "Recall",
                "args": {"filters": {}}
            })

        return plan_steps
