"""Comprehensive, configuration-driven End-to-End Integration Test for SERO v2.

Validates the full lifecycle flow from initial discovery, hypothesis registration,
statistical validation, theory promotion, form selection, capital splitting, and execution.
"""

import pytest
from uuid import uuid4

# Imports from SERO v2 core
from apodex.ai_eos.interfaces.services import (
    IEventBus,
    IResearchOS,
    IKnowledgeInfrastructure,
    IExecutiveOptimizer,
    IExecutionBackend,
    ICapabilityRegistry,
    IGovernanceGateway,
)
from apodex.ai_eos.infrastructure.composition import CompositionContainer
from apodex.ai_eos.infrastructure.event_bus import EventBus
from apodex.ai_eos.infrastructure.state_machine import VentureLifecyclePhase, LifecycleStateMachine
from apodex.ai_eos.memory.knowledge_infrastructure import KnowledgeInfrastructure
from apodex.ai_eos.research.research_os import ResearchOS
from apodex.ai_eos.intelligence.decision_engine import EntrepreneurialIntelligenceSystem
from apodex.ai_eos.portfolio.manager import PortfolioOperatingSystem
from apodex.ai_eos.orchestration.backend import ExecutionBackendAdapter, VentureExecutionSystem
from apodex.ai_eos.governance.gateway import GovernanceGateway
from apodex.ai_eos.domain.models import VentureCell, Hypothesis, Evidence, Theory


def test_sero_v2_end_to_end_generic_lifecycle():
    """Verify the entire SERO v2 lifecycle through all six cooperating subsystems."""
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
    # 2. OPPORTUNITY DISCOVERY (Phase 0 -> Phase 3)
    # ------------------------------------------------------------------
    # Blended opportunity mathematics: score commercial + expected information gain + option value
    # E[commercial] = $150,000, info_gain = 0.85, option = 4.0
    priority_score = ros.score_opportunity(
        commercial_value=150000.0,
        expected_info_gain=0.85,
        option_value=4.0,
        alpha=1.0,
        beta=1000.0,  # heavily weight information gain in discovery
        gamma=50.0
    )
    assert priority_score > 150000.0

    # ------------------------------------------------------------------
    # 3. HYPOTHESIS & SCIENTIFIC DESIGN (Phase 2 -> Phase 3)
    # ------------------------------------------------------------------
    # Register business hypothesis in ROS
    hyp = ros.register_hypothesis(
        title="Top Banner Conversion Boost",
        description="Fewer checkout clicks increases conversion",
        null_hypothesis="H0: conversion boost <= 0%",
        target_metric="conversion_rate"
    )
    # Ingest hypothesis into Knowledge substrate
    kos.hypotheses.save(str(hyp.hypothesis_id), hyp)
    kos.record_node(str(hyp.hypothesis_id), "hypothesis", {"statement": hyp.description})

    # Science Engine designs the experiment (power analysis)
    exp_design = ros.design_experiment(hyp.hypothesis_id)
    assert exp_design["recommended_sample_size"] > 0

    # Create and run the experiment sandbox simulation (Ground truth = 3.5% yield)
    exp = ros.create_experiment(hyp.hypothesis_id, seed=101)
    ros.execute_experiment_simulation(exp.experiment_id, ground_truth_yield=3.5)

    # Retrieve validated hypothesis
    validated_hyp = ros.hypotheses.get(hyp.hypothesis_id)
    assert validated_hyp.status == "validated"

    # ------------------------------------------------------------------
    # 4. BAYESIAN BELIEF UPDATING & THEORY PROMOTION (Phase 2)
    # ------------------------------------------------------------------
    # Translate validated outcome into KOS Evidence
    evidence_node = Evidence(
        evidence_id="ev_sandbox_pilot",
        source="ROS_sandbox_101",
        method="experiment",
        strength={"p_value": 0.001, "sample_size": 150, "effect_size": 3.5},
        causal_or_correlational="causal"
    )
    # Bayesian belief engine updates posterior confidence
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

    # Promote to Theory node
    promoted_theories = kos.promote_to_theories()
    assert len(promoted_theories) == 1
    active_theory = promoted_theories[0]
    assert "Fewer checkout clicks increases conversion" in active_theory.statement

    # ------------------------------------------------------------------
    # 5. META-ECONOMIC FORM SELECTION & PORTFOLIO ALLOCATION (Phase 4 -> Phase 5)
    # ------------------------------------------------------------------
    # EIS decides optimal economic form based on Theory and Capital
    chosen_form = eis.evaluate_opportunity_form(active_theory, available_capital_cents=50000_00)
    assert chosen_form == "BUILD_VENTURE"

    # Initialize a Venture Cell for the building venture
    cell = VentureCell(
        cell_id=uuid4(),
        name="CheckoutVenture",
        namespace="checkout_cell_ns",
        allocated_capital_cents=0,
        sub_agent_ids=["agent_scout", "agent_rebalancing"]
    )

    # POS distributes capital between Venture Execution and Research Portfolios
    # Since KOS uncertainty of cell is moderate, POS splits capital accordingly
    distribution = pos.allocate_portfolio_capital(
        cells=[cell],
        unresolved_uncertainty_score=cell.uncertainty,
        total_allocation_cents=40000_00  # allocate $400
    )
    assert distribution["venture_portfolio_cents"] > 0
    assert distribution["research_portfolio_cents"] > 0
    cell.allocated_capital_cents = distribution["venture_portfolio_cents"]

    # ------------------------------------------------------------------
    # 6. VENTURE EXECUTION CYCLE & CALIBRATION (Phase 5 -> Phase 7)
    # ------------------------------------------------------------------
    # Run Multi-Timescale Planning
    assert ves_planner.plan_multi_timescale(horizon_days=2) == "EXECUTE_EXPERIMENTS"
    assert ves_planner.plan_multi_timescale(horizon_days=30) == "GO_NO_GO_PROGRESSION"

    # Run execution backend adaptador cycle
    cycle_metrics = ves_adapter.run_cycle(cell.cell_id, capital_cents=cell.allocated_capital_cents)
    assert cycle_metrics["cycle_number"] == 1
    cell.spent_capital_cents += cycle_metrics["capital_deployed_cents"]
    cell.earned_revenue_cents += cycle_metrics["earned_revenue_cents"]

    # Record Decision and expected vs actual calibration trail
    # Expected success was 85%, actual yield was 88% (+3% bias)
    decision_record = gov.record_institutional_decision(
        decision_id=f"dec_launch_{cell.cell_id}",
        reasoning="Theory-backed conversion boost on top banner",
        confidence=0.85,
        actual_accuracy=0.88
    )
    assert decision_record["bias"] == pytest.approx(0.03)

    # Check GRC policy gates
    gate_clearance = gov.evaluate_action(
        action_type="launch_ad_spend",
        risk_score=0.15,
        context={"budget_cents": 10000}
    )
    assert gate_clearance["cleared"] is True
