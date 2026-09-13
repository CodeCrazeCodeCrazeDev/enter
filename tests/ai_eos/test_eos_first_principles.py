"""Unit and Integration Tests for First-Principles Entrepreneurial Operating System (EOS) Engine.
"""

import pytest
from apodex.ai_eos.intelligence.eos_first_principles import (
    EOSState,
    EOSStateMachine,
    OpportunityContext,
    OpportunityDecisionTree,
    BusinessLoopMetrics,
    CoupledBusinessLoopsEngine,
    CustomerLifecycleStage,
    CustomerLifecycleEngine,
    GrowthStage,
    GrowthStageClassifier,
    MoatAnalyzer,
    FailureMode,
    FailureModeMonitor,
    FirstPrinciplesEOSEngine,
)


def test_eos_state_machine_valid_transitions():
    sm = EOSStateMachine(initial_state=EOSState.SENSING)
    assert sm.current_state == EOSState.SENSING

    sm.transition_to(EOSState.HYPOTHESIS, "Anomaly detected")
    assert sm.current_state == EOSState.HYPOTHESIS

    sm.transition_to(EOSState.CHEAP_TEST, "Hypothesis formulated")
    assert sm.current_state == EOSState.CHEAP_TEST

    sm.transition_to(EOSState.VALIDATION, "Cheap test passed")
    assert sm.current_state == EOSState.VALIDATION

    sm.transition_to(EOSState.BUILD_GATE, "Economic viability confirmed")
    assert sm.current_state == EOSState.BUILD_GATE


def test_eos_state_machine_invalid_transition():
    sm = EOSStateMachine(initial_state=EOSState.SENSING)
    with pytest.raises(ValueError):
        sm.transition_to(EOSState.OPERATE, "Invalid direct jump")


def test_opportunity_decision_tree_pursue():
    dt = OpportunityDecisionTree()
    ctx = OpportunityContext(
        title="AI-Powered Optimization Engine",
        is_structural_anomaly=True,
        is_reversible_decision=True,
        high_confidence_multi_source=True,
        cheap_test_available=True,
        test_result_exceeds_kill_threshold=True,
        expected_value_clearly_positive=True,
        has_structural_advantage=True,
    )

    approved, reason = dt.evaluate(ctx)
    assert approved is True
    assert "Commit Resources" in reason


def test_opportunity_decision_tree_reject_noise():
    dt = OpportunityDecisionTree()
    ctx = OpportunityContext(
        title="Random Market Rumor",
        is_structural_anomaly=False,
        is_reversible_decision=True,
        high_confidence_multi_source=False,
        cheap_test_available=False,
        test_result_exceeds_kill_threshold=False,
        expected_value_clearly_positive=False,
        has_structural_advantage=False,
    )

    approved, reason = dt.evaluate(ctx)
    assert approved is False
    assert "noise" in reason.lower()


def test_coupled_business_loops_metrics():
    engine = CoupledBusinessLoopsEngine()
    metrics = BusinessLoopMetrics(
        pricing_arpu_cents=20000,
        marketing_cac_cents=4000,
        cs_churn_rate=0.02,
        financial_burn_multiple=1.1,
    )

    results = engine.evaluate_loop_interactions(metrics)
    assert results["ltv_cents"] == 1000000  # $10k
    assert results["ltv_cac_ratio"] == 250.0
    assert results["unit_economics_healthy"] is True


def test_customer_lifecycle_advancement():
    cle = CustomerLifecycleEngine()
    next_stage = cle.advance_stage(CustomerLifecycleStage.AWARENESS, stage_metric=0.85)
    assert next_stage == CustomerLifecycleStage.INTEREST

    same_stage = cle.advance_stage(CustomerLifecycleStage.AWARENESS, stage_metric=0.20)
    assert same_stage == CustomerLifecycleStage.AWARENESS


def test_growth_stage_classifier():
    classifier = GrowthStageClassifier()
    stage = classifier.classify_stage(
        paying_customers=150,
        retention_curve_flattened=True,
        cac_payback_months=8.0,
        nrr=1.20,
        ecosystem_gmv_cents=0,
    )
    assert stage == GrowthStage.PMF

    is_premature, msg = classifier.detect_premature_scaling(
        current_stage=GrowthStage.STARTUP,
        marketing_spend_scaling=True,
        retention_curve_flattened=False,
    )
    assert is_premature is True
    assert "PREMATURE SCALING WARNING" in msg


def test_moat_analyzer_scoring():
    analyzer = MoatAnalyzer()
    score = analyzer.calculate_moat_durability(
        network_effects_score=0.9,
        switching_costs_score=0.8,
        scale_economies_score=0.7,
        brand_trust_score=0.85,
        counter_positioning_score=0.95,
    )
    assert 0.80 <= score <= 1.0


def test_failure_mode_monitor_diagnostics():
    monitor = FailureModeMonitor()
    failures = monitor.diagnose_failures(
        build_velocity_high=True,
        demand_flat=True,
        retention_flattens=False,
        decision_latency_days=12.0,
        burn_multiple=3.0,
        nps=60.0,
        growth_flat=True,
    )

    failure_modes = [f["failure_mode"] for f in failures]
    assert FailureMode.BUILDING_BEFORE_VALIDATING.value in failure_modes
    assert FailureMode.LACK_OF_PMF.value in failure_modes
    assert FailureMode.ORGANIZATIONAL_BOTTLENECK.value in failure_modes
    assert FailureMode.CAPITAL_MISALLOCATION.value in failure_modes


def test_first_principles_eos_engine_e2e():
    engine = FirstPrinciplesEOSEngine()
    ctx = OpportunityContext(
        title="Autonomous AI Operating Platform",
        is_structural_anomaly=True,
        is_reversible_decision=True,
        high_confidence_multi_source=True,
        cheap_test_available=True,
        test_result_exceeds_kill_threshold=True,
        expected_value_clearly_positive=True,
        has_structural_advantage=True,
    )
    metrics = BusinessLoopMetrics(
        pricing_arpu_cents=30000,
        marketing_cac_cents=5000,
        cs_churn_rate=0.015,
        financial_burn_multiple=1.0,
        hiring_decision_latency_days=4.0,
    )

    result = engine.process_opportunity(ctx, metrics)

    assert result["status"] == "OPERATIONAL"
    assert result["state"] == EOSState.OPERATE.value
    assert result["moat_durability_score"] > 0.7
    assert "Commit Resources" in result["decision_reason"]
