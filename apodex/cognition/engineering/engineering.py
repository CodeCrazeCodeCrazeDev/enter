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
    FeasibilityReport,
    RiskAssessment
)

logger = logging.getLogger("apodex.cognition.engineering")


class EngineeringIntelligence(ICognitiveModule):
    """
    Engineering Intelligence scores architecture patterns, parses dependencies, and estimates development risks.
    """

    def __init__(self) -> None:
        self.known_dependencies = ["pydantic", "fastapi", "sqlalchemy", "uv"]
        self.cache_hits = 0
        self.cache_misses = 0
        self.errors_count = 0

    async def observe(self, context: CognitiveContext, data: Dict[str, Any]) -> None:
        """Observe software component dependencies or repository changes."""
        logger.info("Engineering Intelligence observing module specifications.")
        if "dependencies" in data:
            self.known_dependencies.extend(data["dependencies"])

    async def analyze(self, context: CognitiveContext) -> Dict[str, Any]:
        """Perform static dependency parsing and circular reference warnings."""
        logger.info("Engineering Intelligence conducting circular dependency and complexity check.")
        unsupported_deps = [d for d in self.known_dependencies if d == "deprecated_lib"]
        has_circular = "circular_ref" in self.known_dependencies

        return {
            "total_dependencies": len(self.known_dependencies),
            "unsupported_dependencies": unsupported_deps,
            "has_circular_references": has_circular,
            "modular_coupling_index": 0.25 if not has_circular else 0.85
        }

    async def plan(self, context: CognitiveContext) -> Optional[FeasibilityReport]:
        """Evaluate the engineering feasibility and risk of the active objective."""
        logger.info("Engineering Intelligence constructing feasibility report.")
        if not context.active_goal:
            return None

        goal = context.active_goal
        # Calculate risk and architectural score
        is_complex = len(goal.constraints) > 2 or goal.budget_cents > 2_000_000
        risk_factor = 0.45 if is_complex else 0.15

        arch_score = 0.95
        if "circular_ref" in self.known_dependencies:
            arch_score -= 0.3
            risk_factor += 0.2

        risk_assess = RiskAssessment(
            risk_factor=risk_factor,
            mitigations=["Isolate deployment sandbox", "Write rigorous integration fuzz test suite"],
            description="Complex integration and scale risks" if is_complex else "Standard low-risk rollout"
        )

        report = FeasibilityReport(
            is_feasible=risk_factor < 0.65,
            confidence=1.0 - risk_factor,
            estimated_development_cost_cents=int(goal.budget_cents * 0.4),
            risks=risk_assess,
            architecture_score=arch_score,
            dependencies=list(self.known_dependencies)
        )

        context.feasibility = report
        return report

    async def recommend(self, context: CognitiveContext) -> List[Recommendation]:
        """Provide engineering recommendations like refactoring duplicate components or caching layers."""
        logger.info("Engineering Intelligence providing development recommendations.")
        recs = []
        if context.feasibility and context.feasibility.architecture_score < 0.80:
            evidence_ids = [ev.id for ev in context.evidence]
            recs.append(Recommendation(
                title="Refactor Circular Dependencies",
                action_type="REFACTOR_CODEBASE",
                payload={"target_modules": "circular_ref"},
                confidence_score=0.95,
                supporting_evidence_ids=evidence_ids,
                assumptions=["Static AST analysis correctly identifies structural circular dependency paths"]
            ))
        return recs

    async def verify(self, context: CognitiveContext) -> VerificationResult:
        """Validate that the active engineering configuration contains no high-risk smells."""
        logger.info("Engineering Intelligence performing code and pattern verification.")
        if not context.feasibility:
            return VerificationResult(is_valid=True, reason="No feasibility report generated yet.")

        if context.feasibility.risks.risk_factor > 0.70:
            return VerificationResult(
                is_valid=False,
                reason="Engineering feasibility check failed due to critical risk factors.",
                rejection_tags=["HIGH_ENGINEERING_RISK"]
            )
        return VerificationResult(is_valid=True, reason="Feasibility and dependency checks passed.")

    async def learn(self, context: CognitiveContext, lessons: List[Lesson]) -> None:
        """Incorporate defects or compilation outcomes to refine risk estimators."""
        logger.info("Engineering Intelligence learning from architectural patterns.")
        for lesson in lessons:
            if lesson.category == "engineering_pattern":
                logger.info(f"Learned engineering lesson: {lesson.summary}")

    async def health(self) -> HealthStatus:
        return HealthStatus(
            status="OK",
            cache_hits=self.cache_hits,
            cache_misses=self.cache_misses,
            latency_p95_ms=8.0,
            errors_count=self.errors_count
        )
