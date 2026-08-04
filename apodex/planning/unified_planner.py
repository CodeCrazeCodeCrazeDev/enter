from __future__ import annotations
import logging
from typing import List, Dict, Any, Optional
import uuid

from apodex.cognition.shared.schemas import StrategicGoal, Hypothesis, Recommendation

logger = logging.getLogger("apodex.planning.unified")


class UnifiedPlanner:
    """
    Rule 2: Only one planning engine.
    Handles the structured generation of plans, alternatives, and options.
    Research proposes hypotheses/ideas, and this planner maps out execution steps.
    """

    def __init__(self) -> None:
        self.active_plan_id: Optional[uuid.UUID] = None

    def construct_execution_steps(self, goal: StrategicGoal, hypotheses: List[Hypothesis]) -> List[Dict[str, Any]]:
        """
        Derives concrete execution steps based on the strategic goal and verified hypotheses.
        """
        logger.info(f"UnifiedPlanner deriving steps for Goal: {goal.title}")
        steps = []

        # Step 1: Initial Setup
        steps.append({
            "sequence": 1,
            "action_name": "initialize_sandbox_environment",
            "parameters": {"tenant_id": "global_tenant"},
            "assigned_role": "Engineering"
        })

        # Step 2: Scientific/Experimental Probes based on research hypotheses
        for idx, hyp in enumerate(hypotheses, start=2):
            steps.append({
                "sequence": idx,
                "action_name": "execute_hypothesis_validation",
                "parameters": {"hypothesis_id": str(hyp.id), "statement": hyp.statement},
                "assigned_role": "Research"
            })

        # Step 3: Deployment or scale
        steps.append({
            "sequence": len(steps) + 1,
            "action_name": "deploy_solution_to_production",
            "parameters": {"budget_cents": goal.budget_cents},
            "assigned_role": "Operations"
        })

        return steps

    def rank_alternatives(self, recommendations: List[Recommendation]) -> List[Recommendation]:
        """Rank various recommendations based on confidence and expected utility."""
        return sorted(recommendations, key=lambda r: r.confidence_score, reverse=True)
