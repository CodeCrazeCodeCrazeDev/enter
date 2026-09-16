"""Unit and integration test suite for First-Principles Entrepreneurial Operating System (EOS).

Validates all 11 sections of the EOS specification including Master Loop, Cognitive Loops,
Coupled Business Loops, Customer Lifecycle, GTM Systems, Growth Stages, Moats,
Failure Modes, Scientific Foundations, System State Machine, Decision Tree, and Orchestration.
"""

from __future__ import annotations

import pytest
from apodex.ai_eos.intelligence.eos_first_principles import (
    MasterLoopEngine,
    MasterNode,
    SignalToIdeaPipeline,
    MentalModelEngine,
    CoupledBusinessLoopsEngine,
    BusinessLoopName,
    CustomerLifecycleEngine,
    CustomerStageName,
    GTMSystemEngine,
    MotionType,
    GrowthStageClassifier,
    GrowthStage,
    StrategicMoatEngine,
    FailureModeMonitor,
    FailureModeName,
    ScientificFoundationsRegistry,
    EOSStateMachine,
    EOSState,
    OpportunityDecisionTree,
    FirstPrinciplesEOSEngine,
    DecisionRiskType,
)


def test_master_loop_transitions_and_kill_signals():
    """Verify Section 1 Master Loop transitions and re-entrant kill signal logic."""
    engine = MasterLoopEngine()
    assert engine.current_node == MasterNode.ENVIRONMENTAL_SENSING

    # Normal transition
    engine.transition(MasterNode.SIGNAL_COLLECTION, "Signal acquired")
    assert engine.current_node == MasterNode.SIGNAL_COLLECTION

    # Test Validation Kill Signal (F -. kill signal .-> D)
    kill_node = engine.evaluate_kill_signals(
        validation_passed=False,
        mvp_passed=True,
        gtm_viable=True,
        economics_viable=True
    )
    assert kill_node == MasterNode.OPPORTUNITY_DISCOVERY
    assert engine.current_node == MasterNode.OPPORTUNITY_DISCOVERY
    assert len(engine.execution_history) == 2
    assert engine.execution_history[-1]["kill_signal"] is True

    # Test Weak GTM Feedback Loop (K -. weak GTM .-> J)
    gtm_node = engine.evaluate_kill_signals(
        validation_passed=True,
        mvp_passed=True,
        gtm_viable=False,
        economics_viable=True
    )
    assert gtm_node == MasterNode.GTM_SYSTEM
    assert engine.current_node == MasterNode.GTM_SYSTEM


def test_signal_to_idea_pipeline_and_risk_heuristics():
    """Verify Section 2.1 Anomaly detection, forced hypothesis, cheap tests, and Type I/II risks."""
    pipeline = SignalToIdeaPipeline()

    # 1. Anomaly detection
    is_anomaly = pipeline.detect_anomaly("internet_traffic_growth", observed_value=2.5, expected_value=0.5, threshold=0.2)
    assert is_anomaly is True
    assert len(pipeline.anomalies_detected) == 1

    # 2. Forced hypothesis formation with Type II risk
    hyp = pipeline.form_forced_hypothesis(
        statement="If broadband penetration > 50%, streaming video is viable",
        falsifiable_criteria="1,000 paid streaming signups in 30 days",
        prior_belief=0.40,
        risk_type=DecisionRiskType.TYPE_II,
        test_cost_cents=50_00
    )
    assert hyp.posterior_belief == 0.40
    assert hyp.risk_type == DecisionRiskType.TYPE_II

    # 3. Sequential cheap test Bayesian update
    post = pipeline.run_cheap_test(hyp, test_result_success=True, likelihood_ratio=3.0)
    assert post > 0.65
    assert hyp.is_falsified is False

    # 4. Opportunity cost filter
    passed = pipeline.filter_opportunity_cost(
        is_compounding=True,
        has_structural_advantage=True,
        tam_5_to_10_yr_cents=100_000_000_00
    )
    assert passed is True

    rejected = pipeline.filter_opportunity_cost(
        is_compounding=False,
        has_structural_advantage=True,
        tam_5_to_10_yr_cents=10_000_000_00
    )
    assert rejected is False


def test_mental_model_evolution_and_paradigm_shifts():
    """Verify Section 2.2 Mental model parameter updates vs structural paradigm shifts."""
    engine = MentalModelEngine(
        parameters={"conversion_baseline": 0.02, "cac_estimate": 50.0},
        structural_assumptions=["DVDs are primary movie distribution"]
    )

    # Update parameters (fast loop)
    engine.update_parameters({"conversion_baseline": 0.03})
    assert engine.parameters["conversion_baseline"] == 0.03

    # Record repeated market contradictions leading to model ossification
    for i in range(4):
        ossified = engine.record_market_contradiction(f"Contradiction {i}")
        assert ossified is False

    # 5th contradiction triggers model ossification warning
    ossified = engine.record_market_contradiction("Late fee revenue model collapsing")
    assert ossified is True
    assert engine.is_ossified is True

    # Paradigm shift resets structural model and resolves ossification
    engine.execute_paradigm_shift(["Subscription streaming is primary distribution"])
    assert engine.is_ossified is False
    assert engine.contradiction_count == 0
    assert "Subscription streaming is primary distribution" in engine.structural_assumptions


def test_coupled_business_loops_and_stocks():
    """Verify Section 3 external business loops and coupled stock-and-flow dynamics."""
    engine = CoupledBusinessLoopsEngine()

    # Confirm all 12 loops initialized
    assert len(engine.loops) == 13  # 12 loops + competitive intel
    assert BusinessLoopName.PRODUCT in engine.loops
    assert BusinessLoopName.FINANCIAL in engine.loops

    # Simulate coupled feedback loop (Pricing -> ARPU -> Cash Stock -> Talent Stock & Product Health)
    updated_stocks = engine.simulate_loop_coupling(
        arpu_cents=100_00,   # $100 ARPU
        churn_rate=0.01,     # 1% low churn
        burn_multiple=0.5     # Highly capital efficient
    )

    assert updated_stocks["cash_cents"] > 1000000_00
    assert updated_stocks["talent_headcount"] > 10.0
    assert engine.loops[BusinessLoopName.PRODUCT].health_score > 0.90


def test_customer_lifecycle_funnel_throughput():
    """Verify Section 4 Customer Journey engine across all 15 stages."""
    lifecycle = CustomerLifecycleEngine()
    assert len(lifecycle.stages) == 15
    assert CustomerStageName.AWARENESS in lifecycle.stages
    assert CustomerStageName.REPURCHASE in lifecycle.stages

    funnel = lifecycle.compute_funnel_throughput(initial_cohort_size=100000)
    assert funnel["initial_cohort"] == 100000
    assert funnel["stage_counts"]["Awareness"] == 50000
    assert funnel["overall_conversion"] < 0.001


def test_gtm_system_motion_fit():
    """Verify Section 5 GTM system channel fit determination."""
    gtm = GTMSystemEngine()

    # Low complexity + low ACV -> PLG
    motion_plg = gtm.determine_channel_fit(complexity_score=0.1, price_acv_cents=1000_00)
    assert motion_plg == MotionType.PLG

    # High complexity + high ACV -> SLG
    motion_slg = gtm.determine_channel_fit(complexity_score=0.8, price_acv_cents=100000_00)
    assert motion_slg == MotionType.SLG


def test_company_growth_stage_classification():
    """Verify Section 6 Growth Stage Classifier transitions."""
    classifier = GrowthStageClassifier()
    assert classifier.current_stage == GrowthStage.IDEA

    # Startup stage
    stage = classifier.classify_stage(paying_customers=5, mrr_cents=500_00, retention_curve_flattened=False, rule_of_40=0.1, has_ecosystem_developers=False)
    assert stage == GrowthStage.STARTUP

    # PMF stage
    stage = classifier.classify_stage(paying_customers=50, mrr_cents=20000_00, retention_curve_flattened=True, rule_of_40=0.2, has_ecosystem_developers=False)
    assert stage == GrowthStage.PMF

    # Market Leadership stage
    stage = classifier.classify_stage(paying_customers=10000, mrr_cents=50000000_00, retention_curve_flattened=True, rule_of_40=0.5, has_ecosystem_developers=True)
    assert stage == GrowthStage.MARKET_LEADERSHIP


def test_strategic_moat_durability():
    """Verify Section 7 Strategic Moat durability score calculation."""
    moat = StrategicMoatEngine(
        network_effects_score=0.9,
        switching_costs_score=0.8,
        economies_of_scale_score=0.7,
        brand_trust_score=0.8,
        ip_regulatory_score=0.6,
        counter_positioning_score=1.0
    )
    score = moat.compute_composite_moat_durability()
    assert score == pytest.approx(0.80, abs=0.01)


def test_failure_mode_diagnostics():
    """Verify Section 8 Failure Mode pattern-matching diagnostic monitor."""
    monitor = FailureModeMonitor()

    # Trigger multiple failure modes
    warnings = monitor.evaluate_diagnostics(
        survey_vs_engagement_gap=0.6,      # Trigger Wrong Problem
        build_velocity_vs_demand_gap=0.7,  # Trigger Build Before Validate
        retention_flattened=False,          # Trigger Lack of PMF
        cac_growth_vs_ltv_growth=2.0,       # Trigger Premature Scaling
        decision_latency_sec=100000.0       # Trigger Org Bottleneck
    )

    assert len(warnings) == 5
    failure_modes = [w["failure_mode"] for w in warnings]
    assert FailureModeName.WRONG_PROBLEM.value in failure_modes
    assert FailureModeName.LACK_OF_PMF.value in failure_modes
    assert FailureModeName.PREMATURE_SCALING.value in failure_modes


def test_scientific_foundations_registry():
    """Verify Section 9 Scientific Foundations Registry coverage."""
    registry = ScientificFoundationsRegistry()
    assert "Economics" in registry.domains
    assert "Strategy" in registry.domains
    assert "Complexity Science" in registry.domains
    assert registry.domains["Systems Thinking"]["sources"] == "Donella Meadows"


def test_eos_state_machine_and_decision_tree():
    """Verify Section 10.1 State Machine and 10.2 Sequential Decision Tree."""
    sm = EOSStateMachine()
    assert sm.current_state == EOSState.SENSING

    sm.transition_to(EOSState.HYPOTHESIS, "Anomaly detected")
    assert sm.current_state == EOSState.HYPOTHESIS
    assert len(sm.transition_log) == 1

    dt = OpportunityDecisionTree()

    # Test Noise Rejection (Q1)
    pursue, reason = dt.evaluate_opportunity(
        is_structural_anomaly=False,
        is_reversible_decision=True,
        has_high_confidence_multi_source=True,
        cheap_test_available=True,
        test_exceeds_kill_threshold=True,
        expected_value_positive=True,
        has_structural_advantage=True
    )
    assert pursue is False
    assert "Noise" in reason

    # Test Valid Opportunity (Q1-Q5 All Pass)
    pursue, reason = dt.evaluate_opportunity(
        is_structural_anomaly=True,
        is_reversible_decision=True,
        has_high_confidence_multi_source=True,
        cheap_test_available=True,
        test_exceeds_kill_threshold=True,
        expected_value_positive=True,
        has_structural_advantage=True
    )
    assert pursue is True
    assert "Commit resources" in reason


def test_first_principles_eos_engine_end_to_end():
    """Verify unified FirstPrinciplesEOSEngine end-to-end signal processing and KPI stack rollup."""
    engine = FirstPrinciplesEOSEngine()

    # Process signal through complete state machine and decision tree
    res = engine.process_opportunity_signal(
        signal_name="cuda_general_compute_mismatch",
        observed_val=10.0,
        expected_val=1.0,
        is_reversible=True,
        has_structural_advantage=True
    )

    assert res["action"] == "pursue"
    assert engine.state_machine.current_state == EOSState.OPERATE

    # Roll up KPI stack
    kpi_stack = engine.compute_kpi_stack()
    assert kpi_stack["sensing_signal_fidelity"] == 0.85
    assert kpi_stack["moat_durability_score"] == 0.50
    assert kpi_stack["financial_cash_balance"] == 1000000.0
