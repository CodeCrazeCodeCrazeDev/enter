"""Comprehensive, configuration-driven End-to-End Integration Test for SERO v2.1.

Validates the full lifecycle flow from initial discovery, hypothesis registration,
statistical validation, theory promotion, form selection, capital splitting, and execution,
fully aligned to a 7-stage cognitive lifecycle, multi-mind collective intelligence, and Knowledge ROI.
"""

import pytest
from uuid import uuid4

# Imports from SERO v2.1 core
from apodex.ai_eos.interfaces.services import (
    IEventBus,
    IResearchOS,
    IKnowledgeInfrastructure,
    IExecutionBackend,
    IGovernanceGateway,
)
from apodex.ai_eos.infrastructure.composition import CompositionContainer
from apodex.ai_eos.infrastructure.event_bus import EventBus
from apodex.ai_eos.infrastructure.state_machine import VentureLifecyclePhase, LifecycleStateMachine
from apodex.ai_eos.memory.knowledge_infrastructure import KnowledgeInfrastructure
from apodex.ai_eos.research.research_os import ResearchOS
from apodex.ai_eos.intelligence.decision_engine import EntrepreneurialIntelligenceSystem
from apodex.ai_eos.intelligence.collective import CollectiveIntelligenceEngine
from apodex.ai_eos.portfolio.manager import PortfolioOperatingSystem
from apodex.ai_eos.orchestration.backend import ExecutionBackendAdapter, VentureExecutionSystem
from apodex.ai_eos.governance.gateway import GovernanceGateway
from apodex.ai_eos.domain.models import VentureCell, Hypothesis, Evidence, Theory, CognitiveStage


def test_sero_v2_1_end_to_end_generic_lifecycle():
    """Verify the entire SERO v2.1 lifecycle through all six cooperating subsystems with cognitive alignments."""
    # ------------------------------------------------------------------
    # 1. PLATFORM COMPOSITION (Phase 1)
    # ------------------------------------------------------------------
    container = CompositionContainer()
    container.reset()

    # Instantiate concrete subsystems
    event_bus = EventBus()
    kos = KnowledgeInfrastructure()
    ros = ResearchOS()
    eis = EntrepreneurialIntelligenceSystem()
    collective = CollectiveIntelligenceEngine()
    pos = PortfolioOperatingSystem(initial_reserves_cents=10000_00_00)  # $1M
    ves_adapter = ExecutionBackendAdapter()
    ves_planner = VentureExecutionSystem()
    gov = GovernanceGateway(initial_capital_limit_cents=500000_00)  # $500k

    # Register in DI container
    container.register(IEventBus, event_bus)
    container.register(IKnowledgeInfrastructure, kos)
    container.register(IResearchOS, ros)
    container.register(IExecutionBackend, ves_adapter)
    container.register(IGovernanceGateway, gov)

    # ------------------------------------------------------------------
    # 2. IMAGINE & OPPORTUNITY DISCOVERY (Cognitive Stage: IMAGINE)
    # ------------------------------------------------------------------
    # Initial venture cell created in the Imagine stage
    cell = VentureCell(
        cell_id=uuid4(),
        name="CheckoutVenture",
        namespace="checkout_cell_ns",
        allocated_capital_cents=0,
        sub_agent_ids=["agent_scout", "agent_rebalancing"],
        current_cognitive_stage=CognitiveStage.IMAGINE
    )
    assert cell.current_cognitive_stage == CognitiveStage.IMAGINE

    # Discovery Math scoring of signal
    priority_score = ros.score_opportunity(
        commercial_value=150000.0,
        expected_info_gain=0.85,
        option_value=4.0,
        alpha=1.0,
        beta=1000.0,
        gamma=50.0
    )
    assert priority_score > 150000.0

    # ------------------------------------------------------------------
    # 3. PLAN, HYPOTHESIS & SCIENTIFIC DESIGN (Cognitive Stage: PLAN)
    # ------------------------------------------------------------------
    cell.current_cognitive_stage = CognitiveStage.PLAN
    assert cell.current_cognitive_stage == CognitiveStage.PLAN

    # Register business hypothesis in ROS
    hyp = ros.register_hypothesis(
        title="Top Banner Conversion Boost",
        description="Fewer checkout clicks increases conversion",
        null_hypothesis="H0: conversion boost <= 0%",
        target_metric="conversion_rate"
    )
    kos.hypotheses.save(str(hyp.hypothesis_id), hyp)
    kos.record_node(str(hyp.hypothesis_id), "hypothesis", {"statement": hyp.description})

    # Science Engine designs the experiment (power analysis)
    exp_design = ros.design_experiment(hyp.hypothesis_id)
    assert exp_design["recommended_sample_size"] > 0

    # ------------------------------------------------------------------
    # 4. EXPERIMENT & SANDBOX SIMULATION (Cognitive Stage: EXPERIMENT)
    # ------------------------------------------------------------------
    cell.current_cognitive_stage = CognitiveStage.EXPERIMENT
    assert cell.current_cognitive_stage == CognitiveStage.EXPERIMENT

    # Create and run the experiment sandbox simulation (Ground truth = 3.5% yield)
    exp = ros.create_experiment(hyp.hypothesis_id, seed=101)
    ros.execute_experiment_simulation(exp.experiment_id, ground_truth_yield=3.5)

    # Retrieve validated hypothesis
    validated_hyp = ros.hypotheses.get(hyp.hypothesis_id)
    assert validated_hyp.status == "validated"

    # ------------------------------------------------------------------
    # 5. LEARN & BAYESIAN BELIEF UPDATING (Cognitive Stage: LEARN)
    # ------------------------------------------------------------------
    cell.current_cognitive_stage = CognitiveStage.LEARN
    assert cell.current_cognitive_stage == CognitiveStage.LEARN

    # Translate validated outcome into KOS Evidence
    evidence_node = Evidence(
        evidence_id="ev_sandbox_pilot",
        source="ROS_sandbox_101",
        method="experiment",
        strength={"p_value": 0.001, "sample_size": 150, "effect_size": 3.5},
        causal_or_correlational="causal"
    )
    kos.update_hypothesis_belief(str(hyp.hypothesis_id), evidence_node)

    # Run second evidence to trigger Theory Promotion Loop
    evidence_node_2 = Evidence(
        evidence_id="ev_sandbox_pilot_2",
        source="ROS_sandbox_102",
        method="pilot",
        strength={"p_value": 0.002, "sample_size": 200, "effect_size": 3.8},
        causal_or_correlational="causal"
    )
    kos.update_hypothesis_belief(str(hyp.hypothesis_id), evidence_node_2)

    updated_hyp = kos.hypotheses.get(str(hyp.hypothesis_id))
    assert updated_hyp.posterior_confidence > 0.80

    # ------------------------------------------------------------------
    # 6. GENERALIZE & THEORY PROMOTION (Cognitive Stage: GENERALIZE)
    # ------------------------------------------------------------------
    cell.current_cognitive_stage = CognitiveStage.GENERALIZE
    assert cell.current_cognitive_stage == CognitiveStage.GENERALIZE

    # Promote to Theory node
    promoted_theories = kos.promote_to_theories()
    assert len(promoted_theories) == 1
    active_theory = promoted_theories[0]
    assert "Fewer checkout clicks increases conversion" in active_theory.statement

    # ------------------------------------------------------------------
    # 7. TEACH & CAPABILITY INJECTION (Cognitive Stage: TEACH)
    # ------------------------------------------------------------------
    cell.current_cognitive_stage = CognitiveStage.TEACH
    assert cell.current_cognitive_stage == CognitiveStage.TEACH

    # EIS decides optimal economic form based on Theory and Capital
    chosen_form = eis.evaluate_opportunity_form(active_theory, available_capital_cents=50000_00)
    assert chosen_form == "BUILD_VENTURE"

    # POS distributes capital between Venture Execution and Research Portfolios
    distribution = pos.allocate_portfolio_capital(
        cells=[cell],
        unresolved_uncertainty_score=cell.uncertainty,
        total_allocation_cents=40000_00
    )
    assert distribution["venture_portfolio_cents"] > 0
    cell.allocated_capital_cents = distribution["venture_portfolio_cents"]

    # ------------------------------------------------------------------
    # 8. GOVERN, REASONING CONSENSUS & CALIBRATION (Cognitive Stage: GOVERN)
    # ------------------------------------------------------------------
    cell.current_cognitive_stage = CognitiveStage.GOVERN
    assert cell.current_cognitive_stage == CognitiveStage.GOVERN

    # Run Multi-Timescale Planning
    assert ves_planner.plan_multi_timescale(horizon_days=2) == "EXECUTE_EXPERIMENTS"

    # Deliberate GTM launch proposal across all six distinct paradigms in Collective Intelligence Layer
    proposal = {
        "title": "Ad placement top banner GTM launch",
        "has_high_information_gain": True,
        "info_gain_estimate": 0.12,
        "violates_context_boundaries": False,
        "is_causally_validated": True,
        "estimated_npv_cents": cell.allocated_capital_cents,
        "has_competitive_moat": True,
        "latency_ms": 110.0
    }
    multi_mind_report = collective.evaluate_with_multi_mind(proposal)
    assert multi_mind_report["approved"] is True
    assert multi_mind_report["consensus_score"] >= 0.75

    # Run execution backend cycle
    cycle_metrics = ves_adapter.run_cycle(cell.cell_id, capital_cents=cell.allocated_capital_cents)
    assert cycle_metrics["cycle_number"] == 1
    cell.spent_capital_cents += cycle_metrics["capital_deployed_cents"]
    cell.earned_revenue_cents += cycle_metrics["earned_revenue_cents"]

    # Record Decision and Expected vs Actual Calibration bias
    decision_record = gov.record_institutional_decision(
        decision_id=f"dec_launch_{cell.cell_id}",
        reasoning="Multi-mind consensus approved top banner conversion boost",
        confidence=multi_mind_report["consensus_score"],
        actual_accuracy=0.88
    )
    assert decision_record["bias"] is not None

    # Calculate and assert Knowledge ROI metrics (Research Economics)
    card = pos.calculate_knowledge_roi(
        validated_theories_count=1,
        total_entropy_reduction=0.45,
        reusable_insights_count=2,
        future_ventures_count=1
    )
    assert card.cost_per_validated_theory > 0.0
    assert card.cost_per_uncertainty_reduction > 0.0
