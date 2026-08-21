"""Tests for First-Principles Reconstruction of the Entrepreneurial Operating System (EOS)."""

import pytest
from apodex.ai_eos.intelligence.eos_first_principles import (
    FirstPrinciplesEOSEngine,
    SignalPipelineEngine,
    BusinessLoopEngine,
    CustomerJourneyTracker,
    GrowthStageClassifier,
    MoatStrategyAnalyzer,
    FailureModeMonitor,
    SystemState,
    CustomerStage,
    VentureGrowthStage,
)


def test_signal_pipeline_and_hypothesis_testing():
    pipeline = SignalPipelineEngine()

    # Filter non-structural vs structural signals
    noise = pipeline.filter_signal("Ad click bump", is_structural_shift=False, magnitude=0.1)
    assert noise is None

    structural = pipeline.filter_signal("Compute cost drop", is_structural_shift=True, magnitude=0.85)
    assert structural is not None
    assert structural.name == "Compute cost drop"

    # Form hypothesis
    hyp = pipeline.form_hypothesis(
        claim="Streaming viable if bandwidth > 100Mbps",
        falsification_metric="buffer_rate",
        threshold=0.01,
        is_reversible=True,
        cost_cents=5000
    )
    assert hyp.status == "proposed"

    # Run cheap test - pass
    success, posterior = pipeline.run_cheap_test(hyp.hypothesis_id, observed_metric_value=0.05)
    assert success is True
    assert posterior > 0.5
    assert hyp.status == "validated"


def test_business_loop_engine_coupling():
    engine = BusinessLoopEngine()
    initial_nrr = engine.state.nrr

    # Step coupled loops with product investment
    updated_state = engine.step_coupled_loops({"product": 2.0, "customer_success": 1.5})

    assert updated_state.product_retention_slope > 0.5
    assert updated_state.nrr > initial_nrr
    assert updated_state.arpu_cents > 20000


def test_customer_journey_tracker():
    tracker = CustomerJourneyTracker()
    tracker.set_cohort_distribution({
        CustomerStage.AWARENESS: 10000,
        CustomerStage.ACTIVATION: 1200,
        CustomerStage.RETENTION: 840,
    })

    activation_rate = tracker.calculate_activation_rate()
    retention_score = tracker.calculate_retention_score()

    assert activation_rate == 0.12
    assert retention_score == 0.70


def test_growth_stage_classifier():
    classifier = GrowthStageClassifier()

    # Idea stage
    stage, constraint = classifier.evaluate_stage(0, 0, False, False)
    assert stage == VentureGrowthStage.IDEA

    # PMF stage
    stage, constraint = classifier.evaluate_stage(120, 2000000, True, False)
    assert stage == VentureGrowthStage.PMF


def test_moat_strategy_analyzer():
    analyzer = MoatStrategyAnalyzer()
    score = analyzer.compute_moat_durability(
        network_density=0.80,
        switching_cost_cents=8000_00,
        scale_advantage_pct=0.60,
        brand_trust_score=0.90,
        counter_positioning=True,
        cornered_resource=False,
        process_power_score=0.75
    )

    assert 0.0 <= score <= 1.0
    assert score > 0.60


def test_failure_mode_monitor():
    monitor = FailureModeMonitor()

    # Healthy metrics
    alerts = monitor.audit_metrics(
        retention_curve_flattens=True,
        cac_cents=10000,
        ltv_cents=50000,
        burn_multiple=1.2,
        decision_latency_seconds=30.0,
        runway_months=18.0
    )
    assert len(alerts) == 0

    # Unhealthy metrics triggering multiple failure modes
    alerts = monitor.audit_metrics(
        retention_curve_flattens=False,
        cac_cents=20000,
        ltv_cents=30000,
        burn_multiple=3.5,
        decision_latency_seconds=400.0,
        runway_months=4.0
    )
    assert len(alerts) >= 4
    failure_modes = [a.failure_mode for a in alerts]
    assert "Lack of Product-Market Fit" in failure_modes
    assert "Capital Misallocation" in failure_modes


def test_decision_tree_and_state_machine():
    engine = FirstPrinciplesEOSEngine()

    # Decision tree - discard non-structural anomaly
    pursue, msg = engine.execute_decision_tree(
        is_structural_anomaly=False,
        is_reversible=True,
        high_confidence_signal=False,
        cheap_test_available=True,
        test_passed=True,
        ev_clearly_positive=True,
        has_structural_advantage=True
    )
    assert pursue is False
    assert "Signal is non-structural noise" in msg

    # Decision tree - pursue valid opportunity
    pursue, msg = engine.execute_decision_tree(
        is_structural_anomaly=True,
        is_reversible=True,
        high_confidence_signal=True,
        cheap_test_available=True,
        test_passed=True,
        ev_clearly_positive=True,
        has_structural_advantage=True
    )
    assert pursue is True

    # State machine transition sequence
    assert engine.state == SystemState.SENSING
    engine.transition_state_machine("anomaly_detected", {})
    assert engine.state == SystemState.HYPOTHESIS
    engine.transition_state_machine("hypothesis_formed", {})
    assert engine.state == SystemState.CHEAP_TEST
    engine.transition_state_machine("strengthened", {})
    assert engine.state == SystemState.VALIDATION
