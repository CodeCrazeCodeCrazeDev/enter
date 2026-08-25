"""Unit tests for the Entrepreneurial Operating System (EOS) first-principles runtime."""

import pytest
from apodex.ai_eos.intelligence.eos_first_principles import (
    Timescale,
    DecisionRiskType,
    CustomerJourneyStage,
    CompanyGrowthStage,
    EOSState,
    WeakSignal,
    FalsifiableHypothesis,
    AnomalyFilter,
    SignalToIdeaPipeline,
    CoupledBusinessLoopsEngine,
    CustomerJourneyTracker,
    GrowthStageClassifier,
    OpportunityDecisionTree,
    EOSStateMachine,
    FailureModeMonitor,
    EOSKPIStack,
)


def test_signal_to_idea_pipeline():
    pipeline = SignalToIdeaPipeline()

    # Noise signal
    noise_sig = WeakSignal(description="Random Twitter post", source="social", is_structural_anomaly=False, confidence=0.3)
    hyp1 = pipeline.process_signal(noise_sig, "Some claim", "ctr", 0.05)
    assert hyp1 is None

    # Structural anomaly signal
    structural_sig = WeakSignal(
        description="CUDA compute demand doubling monthly while CPU flat",
        source="market_data",
        is_structural_anomaly=True,
        confidence=0.85
    )
    hyp2 = pipeline.process_signal(structural_sig, "General GPU compute market emerging", "monthly_growth", 0.15)
    assert hyp2 is not None
    assert hyp2.status == "PENDING"

    # Belief update -> Strengthened
    status_str = pipeline.update_belief(hyp2, 0.20)
    assert status_str == "STRENGTHENED"
    assert hyp2.status == "STRENGTHENED"

    # Belief update -> Falsified
    hyp3 = pipeline.process_signal(structural_sig, "Alt claim", "monthly_growth", 0.50)
    assert hyp3 is not None
    status_fal = pipeline.update_belief(hyp3, 0.10)
    assert status_fal == "FALSIFIED"
    assert hyp3.status == "FALSIFIED"


def test_coupled_business_loops_engine():
    engine = CoupledBusinessLoopsEngine()
    assert len(engine.loops) == 13
    assert "Product" in engine.loops
    assert "Financial" in engine.loops

    initial_cash = engine.stocks["cash"]
    updated_stocks = engine.step_simulation(delta_revenue=10000.0, delta_hiring=0.5, delta_churn=0.01)
    assert "cash" in updated_stocks
    assert "talent" in updated_stocks


def test_customer_journey_tracker():
    tracker = CustomerJourneyTracker()
    assert tracker.stage_counts[CustomerJourneyStage.AWARENESS] == 1000

    moved = tracker.transition_cohort(CustomerJourneyStage.AWARENESS, CustomerJourneyStage.INTEREST, 0.2)
    assert moved == 200
    assert tracker.stage_counts[CustomerJourneyStage.AWARENESS] == 800
    assert tracker.stage_counts[CustomerJourneyStage.INTEREST] == 200

    summary = tracker.get_funnel_summary()
    assert summary["AWARENESS"] == 800
    assert summary["INTEREST"] == 200


def test_growth_stage_classifier():
    classifier = GrowthStageClassifier()

    stage, constraint, risk = classifier.classify_stage({"paying_customers": 0})
    assert stage == CompanyGrowthStage.IDEA
    assert constraint == "Founder time"

    stage, constraint, risk = classifier.classify_stage({"paying_customers": 2})
    assert stage == CompanyGrowthStage.VALIDATION

    stage, constraint, risk = classifier.classify_stage({"paying_customers": 10})
    assert stage == CompanyGrowthStage.STARTUP

    stage, constraint, risk = classifier.classify_stage({"paying_customers": 100, "retention_curve_flat": 0.5})
    assert stage == CompanyGrowthStage.PMF

    stage, constraint, risk = classifier.classify_stage({"arr_usd": 15_000_000})
    assert stage == CompanyGrowthStage.GROWTH

    stage, constraint, risk = classifier.classify_stage({"arr_usd": 60_000_000, "rule_of_40": 0.5})
    assert stage == CompanyGrowthStage.SCALE


def test_opportunity_decision_tree():
    tree = OpportunityDecisionTree()

    # Pass all checks
    pursue, reason = tree.evaluate_opportunity(
        is_structural_anomaly=True,
        is_reversible=True,
        high_confidence_multi_source=False,
        cheap_test_available=True,
        test_exceeds_kill_threshold=True,
        ev_positive=True,
        has_structural_advantage=True
    )
    assert pursue is True
    assert "Commit resources" in reason

    # Fail anomaly check
    pursue, reason = tree.evaluate_opportunity(
        is_structural_anomaly=False,
        is_reversible=True,
        high_confidence_multi_source=True,
        cheap_test_available=True,
        test_exceeds_kill_threshold=True,
        ev_positive=True,
        has_structural_advantage=True
    )
    assert pursue is False
    assert "Signal is noise" in reason


def test_eos_state_machine():
    sm = EOSStateMachine()
    assert sm.current_state == EOSState.SENSING

    # Valid transition
    assert sm.transition_to(EOSState.HYPOTHESIS) is True
    assert sm.current_state == EOSState.HYPOTHESIS

    # Invalid transition
    assert sm.transition_to(EOSState.SCALE) is False
    assert sm.current_state == EOSState.HYPOTHESIS

    # Valid path
    assert sm.transition_to(EOSState.CHEAP_TEST) is True
    assert sm.transition_to(EOSState.VALIDATION) is True


def test_failure_mode_monitor():
    monitor = FailureModeMonitor()

    # Normal metrics
    warnings = monitor.check_failure_modes({})
    assert len(warnings) == 0

    # Failure metrics
    fail_metrics = {
        "engagement": 0.1,
        "survey_positive": 0.9,
        "build_velocity": 0.9,
        "demand_signal": 0.1
    }
    warnings = monitor.check_failure_modes(fail_metrics)
    assert len(warnings) == 2
    modes = [w["failure_mode"] for w in warnings]
    assert "Solving the wrong problem" in modes
    assert "Building before validating" in modes


def test_eos_kpi_stack():
    kpi_stack = EOSKPIStack()
    res = kpi_stack.compute_kpi_stack({
        "valid_signals": 15,
        "total_signals": 20,
        "validation_spend": 10000,
        "learnings_count": 5
    })
    assert res["sensing_signal_to_noise"] == 0.75
    assert res["validation_cost_per_learning"] == 2000.0
