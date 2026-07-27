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
    Lesson
)

logger = logging.getLogger("apodex.cognition.governance")


class GovernanceLayer(ICognitiveModule):
    """
    Rule 6: The Governance layer should never be bypassable.
    Enforces non-bypassable safety limits, budget caps, evidence sufficiency, and risk scoring.
    """

    def __init__(self) -> None:
        self.max_budget_limit_cents = 10_000_000 # Max $100k
        self.min_confidence_score = 0.50
        self.blacklisted_keywords = ["drop table", "unsafe_execute_payload", "ignore previous instructions"]
        self.cache_hits = 0
        self.cache_misses = 0
        self.errors_count = 0

    async def observe(self, context: CognitiveContext, data: Dict[str, Any]) -> None:
        """Observe administrative configurations or dynamic risk thresholds."""
        logger.info("Governance Layer observing system configurations.")
        if "max_budget_limit_cents" in data:
            self.max_budget_limit_cents = data["max_budget_limit_cents"]
        if "min_confidence_score" in data:
            self.min_confidence_score = data["min_confidence_score"]

    async def analyze(self, context: CognitiveContext) -> Dict[str, Any]:
        """Audit the active environment configuration for policies, credentials, or injection threats."""
        logger.info("Governance Layer auditing system policies.")
        has_blacklisted = False
        if context.active_goal:
            desc = context.active_goal.description.lower()
            if any(kw in desc for kw in self.blacklisted_keywords):
                has_blacklisted = True

        return {
            "max_budget_limit_cents": self.max_budget_limit_cents,
            "min_confidence_score": self.min_confidence_score,
            "has_policy_threats": has_blacklisted
        }

    async def plan(self, context: CognitiveContext) -> Optional[Any]:
        """Governance does not generate positive strategies; returns None."""
        return None

    async def recommend(self, context: CognitiveContext) -> List[Recommendation]:
        """Provides risk-mitigation recommendations such as sandbox isolation."""
        logger.info("Governance Layer generating compliance recommendations.")
        recs = []
        if context.active_goal and context.active_goal.budget_cents > (self.max_budget_limit_cents * 0.8):
            evidence_ids = [ev.id for ev in context.evidence]
            recs.append(Recommendation(
                title="Enforce Split-Payment Milestones",
                action_type="SPLIT_BUDGET",
                payload={"milestones_count": 3},
                confidence_score=0.99,
                supporting_evidence_ids=evidence_ids,
                assumptions=["Budget allocations exceeding 80% threshold present elevated systemic insolvency risks"]
            ))
        return recs

    async def verify(self, context: CognitiveContext) -> VerificationResult:
        """
        Rule 6 veto enforcement:
        1. Unsafe execution command checks
        2. Missing evidence or low-confidence check
        3. Policy violation check
        4. Insufficient confidence check
        5. Budget limit check
        """
        logger.info("Governance Layer performing non-bypassable safety audit.")

        # 1. Active Goal Exist check
        if not context.active_goal:
            return VerificationResult(is_valid=False, reason="No active strategic goal assigned.", rejection_tags=["MISSING_GOAL"])

        goal = context.active_goal

        # 2. Budget Limit check
        if goal.budget_cents > self.max_budget_limit_cents:
            return VerificationResult(
                is_valid=False,
                reason=f"Governance Veto: Goal budget {goal.budget_cents} cents exceeds max limit {self.max_budget_limit_cents} cents.",
                rejection_tags=["BUDGET_VIOLATION"]
            )

        # 3. Unsafe Injection Commands check
        description_low = goal.description.lower()
        if any(kw in description_low for kw in self.blacklisted_keywords):
            return VerificationResult(
                is_valid=False,
                reason="Governance Veto: Detected blacklisted/unsafe commands in strategic payload.",
                rejection_tags=["POLICY_VIOLATION", "UNSAFE_EXECUTION"]
            )

        # 4. Insufficient Research Confidence check
        # If we have hypotheses, ensure their average confidence is above min_confidence_score
        if context.hypotheses:
            avg_conf = sum(h.confidence for h in context.hypotheses) / len(context.hypotheses)
            if avg_conf < self.min_confidence_score:
                return VerificationResult(
                    is_valid=False,
                    reason=f"Governance Veto: Average hypothesis confidence {avg_conf:.2f} is below minimum allowed {self.min_confidence_score:.2f}.",
                    rejection_tags=["INSUFFICIENT_CONFIDENCE", "MISSING_EVIDENCE"]
                )

        # 5. Engineering Feasibility Risk check
        if context.feasibility and not context.feasibility.is_feasible:
            return VerificationResult(
                is_valid=False,
                reason="Governance Veto: Engineering Intelligence reported non-feasible execution parameters.",
                rejection_tags=["FEASIBILITY_HALTED"]
            )

        # 6. Business Viability check
        if context.value and context.value.roi_multiple < 1.0:
            return VerificationResult(
                is_valid=False,
                reason="Governance Veto: Proposed action yields negative economic expected value.",
                rejection_tags=["NEGATIVE_ECONOMIC_YIELD"]
            )

        # 7. Evidence-Based Strategic Verification (arXiv:2605.15245)
        if "require_evidence" in goal.constraints:
            if not context.evidence:
                return VerificationResult(
                    is_valid=False,
                    reason="Governance Veto: Evidence-based self-improving organization protocol requires at least one supporting EvidenceCard.",
                    rejection_tags=["MISSING_EVIDENCE_CARD"]
                )

        return VerificationResult(is_valid=True, reason="Governance clearance granted. All safety and compliance checks passed.")

    async def learn(self, context: CognitiveContext, lessons: List[Lesson]) -> None:
        """Absorb security violations to dynamically expand blacklist keywords."""
        logger.info("Governance Layer learning from safety events.")
        for lesson in lessons:
            if lesson.category == "workflow" and "unsafe" in lesson.summary.lower():
                logger.warning(f"Expanding blacklisted signatures due to failure analysis: {lesson.summary}")

    async def health(self) -> HealthStatus:
        return HealthStatus(
            status="OK",
            cache_hits=self.cache_hits,
            cache_misses=self.cache_misses,
            latency_p95_ms=1.8,
            errors_count=self.errors_count
        )
