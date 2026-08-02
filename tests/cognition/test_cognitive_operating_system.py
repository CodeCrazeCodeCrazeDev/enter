from __future__ import annotations
import pytest
import uuid
import asyncio

from apodex.cognition.shared.schemas import (
    StrategicGoal,
    CognitiveContext,
    Hypothesis,
    EvidenceCard,
    ExecutionOutcome,
    ExecutionPlan
)
from apodex.cognition.controller import CognitiveSystemController


@pytest.mark.asyncio
async def test_executive_intelligence_prioritization():
    """Test strategic goal prioritisation based on objective weights."""
    controller = CognitiveSystemController()

    goal = StrategicGoal(
        title="Increase Conversions",
        description="Optimize checkout pipeline with dynamic UI adaptations.",
        priority_score=0.8,
        budget_cents=500_000,
        constraints=["low risk"]
    )
    context = CognitiveContext(active_goal=goal)

    # Observe and analyze with dynamic weights
    await controller.executive.observe(context, {"priority_weights": {"mrr_growth": 0.8, "risk_mitigation": 0.5}})
    analysis = await controller.executive.analyze(context)

    assert analysis["status"] == "ANALYZED"
    assert analysis["adjusted_priority"] > 0.0

    # Check validation rules
    valid_res = await controller.executive.verify(context)
    assert valid_res.is_valid is True


@pytest.mark.asyncio
async def test_research_intelligence_hypotheses_and_contradictions():
    """Test hypothesis generation, literature referencing, evidence cards, and contradiction penalty."""
    controller = CognitiveSystemController()

    goal = StrategicGoal(
        title="Reduce Latency",
        description="Integrate edge caching layers.",
        priority_score=0.7,
        budget_cents=100_000
    )
    context = CognitiveContext(active_goal=goal)

    # Propose research hypotheses
    hyps = await controller.research.plan(context)
    assert len(hyps) > 0
    assert "Relevant Literature:" in context.hypotheses[0].rationale

    # Observe a highly reliable contradicting evidence card
    target_hyp_id = context.hypotheses[0].id
    evidence_payload = {
        "evidence": [
            {
                "source": "Core Benchmarks Team",
                "description": "Cache hits drop severely on dynamic transactional endpoints.",
                "reliability": 0.90,
                "contradicts_hypothesis_ids": [target_hyp_id]
            }
        ]
    }

    # Inject contradicting evidence
    await controller.research.observe(context, evidence_payload)
    assert len(context.evidence) == 1

    # Analyze contradictions and verify the confidence penalty
    initial_conf = context.hypotheses[0].confidence
    analysis = await controller.research.analyze(context)

    assert len(analysis["contradictions_found"]) == 1
    assert context.hypotheses[0].confidence < initial_conf


@pytest.mark.asyncio
async def test_engineering_intelligence_dependency_and_risk():
    """Test architecture pattern coupling, dependency tracking, and risk assessment."""
    controller = CognitiveSystemController()

    goal = StrategicGoal(
        title="Microservice Transition",
        description="Migrate code to independent nodes.",
        priority_score=0.6,
        budget_cents=2_500_000 # High budget increases complexity risk factor
    )
    context = CognitiveContext(active_goal=goal)

    # Observe dependency specifications containing a circular reference risk smell
    await controller.engineering.observe(context, {"dependencies": ["circular_ref", "pydantic", "fastapi"]})
    analysis = await controller.engineering.analyze(context)

    assert analysis["has_circular_references"] is True
    assert analysis["modular_coupling_index"] == 0.85

    # Plan feasibility report
    report = await controller.engineering.plan(context)
    assert report.is_feasible is False  # Circular reference + complex makes risk_factor > 0.65
    assert report.architecture_score < 0.80
    assert report.risks.risk_factor > 0.50


@pytest.mark.asyncio
async def test_business_intelligence_roi_ranking():
    """Test ROI multiple, expected revenue, and competitor strength assessments."""
    controller = CognitiveSystemController()

    goal = StrategicGoal(
        title="Enterprise Plan Launch",
        description="Launch an automated SLA tracking tier.",
        priority_score=0.9,
        budget_cents=2_000_000
    )
    context = CognitiveContext(active_goal=goal)

    # Observe high growth trend
    await controller.business.observe(context, {"market_growth_factor": 1.2})
    report = await controller.business.plan(context)

    assert report.roi_multiple > 4.0
    assert report.expected_return_cents > goal.budget_cents

    # Verify economic viability
    valid_res = await controller.business.verify(context)
    assert valid_res.is_valid is True


@pytest.mark.asyncio
async def test_operations_intelligence_step_sequencing():
    """Test workflow generation, step durations, and duplicate sequence checking."""
    controller = CognitiveSystemController()

    goal = StrategicGoal(
        title="Deploy Patch",
        description="Deploy cache parameter optimization.",
        priority_score=0.5,
        budget_cents=50_000
    )
    context = CognitiveContext(active_goal=goal)

    # Plan step-by-step workflow
    exec_plan = await controller.operations.plan(context)
    assert len(exec_plan.steps) > 0
    assert exec_plan.estimated_duration_sec > 0.0

    # Verify sequences: duplicate sequence check should fail if forced
    valid_res = await controller.operations.verify(context)
    assert valid_res.is_valid is True

    # Manually inject duplicate step sequence to trigger validation failure
    exec_plan.steps[1].sequence = 1
    bad_res = await controller.operations.verify(context)
    assert bad_res.is_valid is False
    assert "DUPLICATE_STEP_SEQUENCE" in bad_res.rejection_tags


@pytest.mark.asyncio
async def test_governance_layer_veto_authority():
    """Test Rule 6: Non-bypassable veto checks for policy, safety, budget, and confidence limits."""
    controller = CognitiveSystemController()

    # 1. Budget violation veto
    giant_goal = StrategicGoal(
        title="Massive Infrastructure Build",
        description="Build direct parallel clusters.",
        priority_score=0.9,
        budget_cents=100_000_000, # 100M cents exceeds limit
    )
    context1 = CognitiveContext(active_goal=giant_goal)
    res1 = await controller.governance.verify(context1)
    assert res1.is_valid is False
    assert "BUDGET_VIOLATION" in res1.rejection_tags

    # 2. Safety command injection veto
    toxic_goal = StrategicGoal(
        title="Data Backup Clean",
        description="Truncate database records; drop table production_records;",
        priority_score=0.8,
        budget_cents=10_000
    )
    context2 = CognitiveContext(active_goal=toxic_goal)
    res2 = await controller.governance.verify(context2)
    assert res2.is_valid is False
    assert "POLICY_VIOLATION" in res2.rejection_tags

    # 3. Insufficient research confidence veto
    goal = StrategicGoal(
        title="A/B Test Variant",
        description="Run A/B variants.",
        priority_score=0.5,
        budget_cents=50_000
    )
    context3 = CognitiveContext(active_goal=goal)
    # Add a hypothesis with critically low confidence
    low_hyp = Hypothesis(goal_id=goal.id, statement="Test statement", rationale="Some rationale", confidence=0.20)
    context3.hypotheses.append(low_hyp)
    res3 = await controller.governance.verify(context3)
    assert res3.is_valid is False
    assert "INSUFFICIENT_CONFIDENCE" in res3.rejection_tags


@pytest.mark.asyncio
async def test_learning_engine_optimization_loop():
    """Test Rule 7: Learning outcomes, distilling lessons, and system/model parameter updates."""
    controller = CognitiveSystemController()

    goal = StrategicGoal(
        title="Scale Routing",
        description="Optimize multi-tenant database routing.",
        priority_score=0.7,
        budget_cents=200_000
    )
    context = CognitiveContext(active_goal=goal)

    # Set a predicted cost projection
    context.execution_plan = ExecutionPlan(
        goal_id=goal.id,
        steps=[],
        estimated_duration_sec=120.0,
        total_cost_projection_cents=200_000
    )

    # Simulate a failed execution outcome with specific errors
    failure_outcome_payload = {
        "execution_outcome": {
            "success": False,
            "actual_cost_cents": 250_000, # Cost overrun
            "actual_duration_sec": 450.0,
            "performance_metrics": {"throughput": 12},
            "error_logs": ["Database out of memory error.", "Connection dropped."]
        }
    }

    # Ingest outcome and analyze post-mortem
    await controller.learning.observe(context, failure_outcome_payload)
    analysis = await controller.learning.analyze(context)

    assert analysis["is_success"] is False
    assert analysis["cost_variance_cents"] == 50_000
    assert analysis["error_count"] == 2

    # Plan lessons
    lessons = await controller.learning.plan(context)
    assert len(lessons) >= 2
    categories = [L.category for L in lessons]
    assert "workflow" in categories
    assert "execution_strategy" in categories

    # Learning updates predictive model parameters (Rule 7)
    assert controller.world_model.base_parameters["complexity_cost_multiplier"] == 1.2 # Initially

    # Run full cycle with failure to trigger learning parameter updates
    provenance = await controller.execute_decision_cycle(
        goal_title="Scale Routing Failed Trial",
        goal_description="Optimize routing to database.",
        budget_cents=200_000,
        simulate_success=False
    )

    assert provenance.final_decision == "APPROVED"
    assert provenance.execution_outcome.success is False
    assert len(provenance.lessons_learned) >= 2

    # Verify that global world model parameters are adjusted (tuned) based on failures
    assert controller.world_model.base_parameters["complexity_cost_multiplier"] == 1.4
    assert controller.world_model.base_parameters["failure_probability_offset"] == 0.12


@pytest.mark.asyncio
async def test_controller_end_to_end_decision_cycle():
    """Test full controller execution cycle, producing a perfectly traceable audited DecisionProvenance."""
    controller = CognitiveSystemController()

    provenance = await controller.execute_decision_cycle(
        goal_title="Deploy Automated Code Reviewer",
        goal_description="Integrate an AST analyzer for pull request audits.",
        budget_cents=1_500_000,
        constraints=["SaaS", "python"],
        priority_score=0.85,
        observation_data={"market_growth_factor": 1.15, "default_step_duration_sec": 30.0},
        simulate_success=True
    )

    # Rule 4: Verify detailed provenance metrics
    assert provenance.id is not None
    assert provenance.objective.title == "Deploy Automated Code Reviewer"
    assert provenance.objective.budget_cents == 1_500_000
    assert len(provenance.hypotheses) > 0
    assert len(provenance.evidence) == 0 # No contradicting evidence injected
    assert provenance.feasibility.is_feasible is True
    assert provenance.value_assessment.roi_multiple > 1.0
    assert len(provenance.execution_plan.steps) == 4
    assert provenance.final_decision == "APPROVED"
    assert provenance.execution_outcome.success is True
    assert provenance.execution_outcome.actual_cost_cents == int(1_500_000 * 0.95)
    assert len(provenance.lessons_learned) > 0

    # Retrieve from memory and double check
    mem_prov = controller.memory.get_provenance(provenance.id)
    assert mem_prov is not None
    assert mem_prov.objective.title == "Deploy Automated Code Reviewer"


@pytest.mark.asyncio
async def test_controller_self_correction_backtracking():
    """Verify that the Cognitive OS controller successfully executes self-correction backtracking."""
    controller = CognitiveSystemController()

    provenance = await controller.execute_decision_cycle(
        goal_title="Scale Routing Backtrack Trial",
        goal_description="Optimize routing to database with recovery.",
        budget_cents=200_000,
        simulate_success=False,
        enable_backtracking=True
    )

    # Verify that backtracking executed and recovered the decision cycle outcome successfully
    assert provenance.final_decision == "APPROVED"
    assert provenance.execution_outcome.success is True
    assert provenance.discrepancy_analysis["backtracking_executed"] is True
    assert provenance.discrepancy_analysis["escalated_budget_cents"] == 300_000
    assert any("Backtracking recovery executed" in log for log in provenance.execution_outcome.error_logs)
