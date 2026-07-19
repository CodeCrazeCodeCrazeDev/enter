from __future__ import annotations
import logging
import uuid
from datetime import datetime
from typing import Any, Dict, List, Optional

from apodex.cognition.shared.schemas import (
    CognitiveContext,
    StrategicGoal,
    DecisionProvenance,
    ExecutionOutcome,
    Lesson
)
from apodex.cognition.memory.unified_memory import UnifiedMemory
from apodex.cognition.world_model.predictive_model import UnifiedPredictiveModel
from apodex.cognition.planning.unified_planner import UnifiedPlanner

from apodex.cognition.executive.executive import ExecutiveIntelligence
from apodex.cognition.research.research import ResearchIntelligence
from apodex.cognition.engineering.engineering import EngineeringIntelligence
from apodex.cognition.business.business import BusinessIntelligence
from apodex.cognition.operations.operations import OperationsIntelligence
from apodex.cognition.governance.governance import GovernanceLayer
from apodex.cognition.learning.learning import LearningEngine

logger = logging.getLogger("apodex.cognition.controller")


class CognitiveSystemController:
    """
    The Single Brain (Central Controller) of the Cognitive Operating System.
    Coordinates all capability modules in a single deterministic decision cycle.
    """

    def __init__(self) -> None:
        # Central Services (Rules 1, 2, 3)
        self.memory = UnifiedMemory()
        self.world_model = UnifiedPredictiveModel()
        self.planner = UnifiedPlanner()

        # Core Specialist Modules (Rule 5 uniform interface)
        self.executive = ExecutiveIntelligence()
        self.research = ResearchIntelligence()
        self.engineering = EngineeringIntelligence()
        self.business = BusinessIntelligence()
        self.operations = OperationsIntelligence()
        self.governance = GovernanceLayer()
        self.learning = LearningEngine()

    async def execute_decision_cycle(
        self,
        goal_title: str,
        goal_description: str,
        budget_cents: int,
        constraints: List[str] = None,
        priority_score: float = 0.5,
        observation_data: Dict[str, Any] = None,
        simulate_success: bool = True
    ) -> DecisionProvenance:
        """
        Executes a single deterministic, audited decision cycle:
        Observe -> Understand -> Strat Objective -> Hypotheses -> Feasibility -> ROI -> Operations Plan -> Governance Veto -> Execution -> Learn & Record
        """
        logger.info(f"Initiating decision cycle for: {goal_title}")
        context = CognitiveContext()
        obs_data = observation_data or {}

        # 1. Observe: Initialize environment inputs and strategic intent
        active_goal = StrategicGoal(
            title=goal_title,
            description=goal_description,
            priority_score=priority_score,
            budget_cents=budget_cents,
            constraints=constraints or []
        )
        context.active_goal = active_goal
        self.memory.add_goal(active_goal)

        # Notify Executive, Research, Engineering, Business, Operations, Governance
        await self.executive.observe(context, obs_data)
        await self.research.observe(context, obs_data)
        await self.engineering.observe(context, obs_data)
        await self.business.observe(context, obs_data)
        await self.operations.observe(context, obs_data)
        await self.governance.observe(context, obs_data)

        # 2. Understand & Strategic Objective Setting (Executive Intelligence)
        exec_analysis = await self.executive.analyze(context)
        context.system_metrics["executive_adjusted_priority"] = exec_analysis.get("adjusted_priority", priority_score)

        # 3. Hypothesis Generation (Research Intelligence)
        # Research proposes, Planner coordinates
        await self.research.plan(context)
        await self.research.analyze(context)

        # 4. Feasibility & Risk Analysis (Engineering Intelligence)
        # Engineering queries global predictive model for feasibility estimation (Rule 3)
        proj_params = {
            "estimated_cost_cents": int(budget_cents * 0.4),
            "base_risk": 0.45 if len(active_goal.constraints) > 2 else 0.15,
            "market_size_cents": 50_000_000
        }
        prediction = self.world_model.predict_strategy_outcome("engineering_feasibility", proj_params)

        # Engineering populates structured FeasibilityReport
        await self.engineering.plan(context)
        await self.engineering.analyze(context)

        # 5. Value and ROI Assessment (Business Intelligence)
        # Business queries same global predictive model for ROI simulation (Rule 3)
        biz_params = {
            "estimated_cost_cents": budget_cents,
            "base_risk": 0.45 if len(active_goal.constraints) > 2 else 0.15,
            "market_size_cents": 50_000_000
        }
        biz_prediction = self.world_model.predict_strategy_outcome("business_roi", biz_params)

        # Business populates structured ValueReport
        await self.business.plan(context)
        await self.business.analyze(context)

        # 6. Structured Operational Plan generation (Operations Intelligence)
        await self.operations.plan(context)
        await self.operations.analyze(context)

        # 7. Non-Bypassable Governance Veto Check (Governance Layer)
        gov_clearance = await self.governance.verify(context)

        # 8. Execution Stage
        final_decision = "REJECTED_GOVERNANCE"
        outcome = None

        if gov_clearance.is_valid:
            final_decision = "APPROVED"

            # Simulate sequential execution of steps
            actual_cost = int(budget_cents * 0.95) if simulate_success else int(budget_cents * 1.25)
            actual_duration = 240.0

            outcome = ExecutionOutcome(
                success=simulate_success,
                actual_cost_cents=actual_cost,
                actual_duration_sec=actual_duration,
                performance_metrics={
                    "conversions": 120 if simulate_success else 5,
                    "avg_response_ms": 115.2
                },
                error_logs=[] if simulate_success else ["Connection timed out during database write."]
            )
            context.execution_outcome = outcome
        else:
            final_decision = f"REJECTED: {gov_clearance.reason}"
            logger.warning(f"Governance vetoed execution: {gov_clearance.reason}")

        # 9. Learning and Optimization (Learning Engine)
        lessons: List[Lesson] = []
        if outcome:
            # Let Learning Engine observe outcomes and analyze
            outcome_data = {
                "execution_outcome": {
                    "success": outcome.success,
                    "actual_cost_cents": outcome.actual_cost_cents,
                    "actual_duration_sec": outcome.actual_duration_sec,
                    "performance_metrics": outcome.performance_metrics,
                    "error_logs": outcome.error_logs
                }
            }
            await self.learning.observe(context, outcome_data)
            await self.learning.analyze(context)
            lessons = await self.learning.plan(context)

            # Commit lessons to Memory (Rule 1) and optimize (Rule 7)
            for lesson in lessons:
                self.memory.add_lesson(lesson)

            # Direct system optimization: tune predictive model and planning parameters based on lessons
            if not outcome.success:
                self.world_model.update_model_parameters({
                    "complexity_cost_multiplier": 1.4,
                    "failure_probability_offset": 0.12
                })

            # Notify modules to learn from these lessons
            await self.executive.learn(context, lessons)
            await self.research.learn(context, lessons)
            await self.engineering.learn(context, lessons)
            await self.business.learn(context, lessons)
            await self.operations.learn(context, lessons)
            await self.governance.learn(context, lessons)
            await self.learning.learn(context, lessons)

        # 10. Generate Complete Traceable DecisionProvenance (Rule 4)
        provenance = DecisionProvenance(
            objective=active_goal,
            hypotheses=list(context.hypotheses),
            evidence=list(context.evidence),
            feasibility=context.feasibility,
            value_assessment=context.value,
            execution_plan=context.execution_plan,
            assumptions=["Model weights represent baseline accuracy", "Competitor API endpoints are reachable"],
            confidence=context.feasibility.confidence if context.feasibility else 0.5,
            uncertainty=1.0 - (context.feasibility.confidence if context.feasibility else 0.5),
            alternatives_considered=["Heuristic fallback pipeline", "Sequential sequential check"],
            final_decision=final_decision,
            execution_outcome=outcome,
            lessons_learned=lessons
        )

        self.memory.add_provenance(provenance)
        context.provenance_log.append(provenance)
        logger.info(f"Decision cycle complete. Provenance saved: {provenance.id}")
        return provenance
