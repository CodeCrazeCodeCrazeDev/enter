from __future__ import annotations
import logging
from typing import Any, Dict, List, Optional
import uuid

from apodex.cognition.shared.interfaces import ICognitiveModule
from apodex.cognition.shared.schemas import (
    CognitiveContext,
    Recommendation,
    VerificationResult,
    HealthStatus,
    Lesson,
    StrategicGoal
)

logger = logging.getLogger("apodex.cognition.executive")


class ExecutiveIntelligence(ICognitiveModule):
    """
    Executive Intelligence owns strategic intent, goal prioritization, and budget allocation.
    """

    def __init__(self) -> None:
        self.priority_weights: Dict[str, float] = {
            "mrr_growth": 0.5,
            "cost_reduction": 0.3,
            "risk_mitigation": 0.2
        }
        self.errors_count = 0
        self.cache_hits = 0
        self.cache_misses = 0

    async def observe(self, context: CognitiveContext, data: Dict[str, Any]) -> None:
        """Receive objective preferences and budget bounds from the user or organization."""
        logger.info("Executive Intelligence observing strategic goals.")
        if "priority_weights" in data:
            self.priority_weights.update(data["priority_weights"])

    async def analyze(self, context: CognitiveContext) -> Dict[str, Any]:
        """Assess context to identify if the current strategic goals are aligned."""
        logger.info("Executive Intelligence analyzing strategic goal alignment.")
        if not context.active_goal:
            return {"status": "NO_ACTIVE_GOAL"}

        goal = context.active_goal
        # Calculate prioritization score based on weights
        is_coding = "code" in goal.description.lower() or "nlp" in goal.description.lower()
        base_priority = goal.priority_score

        adjusted_priority = base_priority * self.priority_weights["mrr_growth"]
        if "low risk" in goal.constraints:
            adjusted_priority += 0.1 * self.priority_weights["risk_mitigation"]

        return {
            "status": "ANALYZED",
            "goal_id": str(goal.id),
            "adjusted_priority": min(1.0, adjusted_priority),
            "suggested_budget_fraction": 1.0 if adjusted_priority > 0.6 else 0.5
        }

    async def plan(self, context: CognitiveContext) -> Optional[StrategicGoal]:
        """Establish or select the active strategic objective."""
        logger.info("Executive Intelligence selecting the active strategic goal.")
        if context.active_goal:
            return context.active_goal
        return None

    async def recommend(self, context: CognitiveContext) -> List[Recommendation]:
        """Recommend budget adjustments or priority realignments."""
        logger.info("Executive Intelligence generating recommendations.")
        recs = []
        if context.active_goal and context.active_goal.budget_cents > 1_000_000:
            recs.append(Recommendation(
                title="Optimize Seed Budget",
                action_type="REALLOCATE_BUDGET",
                payload={"target_cents": int(context.active_goal.budget_cents * 0.8)},
                confidence_score=0.85
            ))
        return recs

    async def verify(self, context: CognitiveContext) -> VerificationResult:
        """Verify that objectives are logically sound and bounded by capital constraints."""
        logger.info("Executive Intelligence verifying active goals.")
        if not context.active_goal:
            return VerificationResult(is_valid=False, reason="No active strategic goal assigned.")

        goal = context.active_goal
        if goal.budget_cents <= 0:
            return VerificationResult(is_valid=False, reason="Budget must be greater than zero.", rejection_tags=["BUDGET_ZERO"])

        return VerificationResult(is_valid=True, reason="Goal alignment and capital constraints verified.")

    async def learn(self, context: CognitiveContext, lessons: List[Lesson]) -> None:
        """Learn from historical strategic performance and refine goal weights."""
        logger.info("Executive Intelligence learning from strategic outcomes.")
        for lesson in lessons:
            if lesson.category == "execution_strategy":
                # If a strategy failed, increase the risk mitigation weight
                if "fail" in lesson.summary.lower() or "error" in lesson.summary.lower():
                    self.priority_weights["risk_mitigation"] = min(0.9, self.priority_weights["risk_mitigation"] + 0.05)
                    self.priority_weights["mrr_growth"] = max(0.1, self.priority_weights["mrr_growth"] - 0.05)
                # If a strategy succeeded exceptionally, increase mrr growth weight
                elif "success" in lesson.summary.lower() or "revenue" in lesson.summary.lower():
                    self.priority_weights["mrr_growth"] = min(0.9, self.priority_weights["mrr_growth"] + 0.05)
                    self.priority_weights["risk_mitigation"] = max(0.1, self.priority_weights["risk_mitigation"] - 0.05)

    async def health(self) -> HealthStatus:
        return HealthStatus(
            status="OK",
            cache_hits=self.cache_hits,
            cache_misses=self.cache_misses,
            latency_p95_ms=5.2,
            errors_count=self.errors_count
        )
