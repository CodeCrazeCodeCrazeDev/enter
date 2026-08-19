"""
Unit and integration tests for the First-Principles EOS Cognitive Engine.
"""

import pytest
from apodex.ai_eos.intelligence.eos_first_principles import (
    Timescale,
    FeedbackLoop,
    TimescaleLoopManager,
    RiskType,
    SignalRecord,
    FalsifiableHypothesis,
    SignalToIdeaPipeline,
    OperationalLoopType,
    OperationalLoopState,
    OperationalLoopSuite,
    JourneyStage,
    CustomerCohort,
    CustomerJourneyTracker,
    CompanyGrowthStage,
    CompanyGrowthClassifier,
    OpportunityPursuitDecisionTree,
    FailureModeMonitor,
)


def test_timescale_loop_manager():
    manager = TimescaleLoopManager()
    fast_loop = FeedbackLoop(
        name="ad_experiment",
        timescale=Timescale.FAST,
        input_signals=["ctr", "cpc"],
        output_artifacts=["ad_copy_variant"],
        velocity_days=3.0,
    )
    medium_loop = FeedbackLoop(
        name="pricing_iteration",
        timescale=Timescale.MEDIUM,
        input_signals=["conversion", "arpu"],
        output_artifacts=["pricing_tier_v2"],
        velocity_days=30.0,
    )
    manager.register_loop(fast_loop)
    manager.register_loop(medium_loop)

    assert len(manager.get_loops_by_timescale(Timescale.FAST)) == 1
    assert len(manager.get_loops_by_timescale(Timescale.MEDIUM)) == 1

    results = manager.step_all({"ad_experiment": 0.9, "pricing_iteration": 0.8})
    assert results["ad_experiment"]["iterations"] == 1
    assert results["ad_experiment"]["compounding_yield"] > 1.0


def test_signal_to_idea_pipeline():
    pipeline = SignalToIdeaPipeline(min_anomaly_threshold=0.2)

    # Weak signal -> discarded
    weak_signal = SignalRecord(
        signal_id="SIG_001",
        description="Minor click noise",
        is_structural_anomaly=False,
        observed_magnitude=1.05,
        baseline_expectation=1.00,
        source="ad_network",
    )
    assert pipeline.evaluate_signal(weak_signal) is None

    # Structural anomaly -> forms hypothesis
    strong_signal = SignalRecord(
        signal_id="SIG_002",
        description="Compute elasticity spike",
        is_structural_anomaly=True,
        observed_magnitude=3.50,
        baseline_expectation=1.00,
        source="aws_billing",
    )
    hypothesis = pipeline.evaluate_signal(strong_signal)
    assert hypothesis is not None
    assert hypothesis.status == "PROPOSED"

    # Risk classification
    type_i_risk = pipeline.classify_risk({"capital_cents": 1_000_000_00, "reversibility_score": 0.1})
    assert type_i_risk == RiskType.TYPE_I

    type_ii_risk = pipeline.classify_risk({"capital_cents": 5_000_00, "reversibility_score": 0.9})
    assert type_ii_risk == RiskType.TYPE_II

    # Real option test
    hyp, passed = pipeline.run_real_option_test(hypothesis, test_cost_cents=1000_00, observed_metric_value=0.50)
    assert passed is True
    assert hyp.status == "CONFIRMED"


def test_operational_loop_suite():
    suite = OperationalLoopSuite()
    assert len(suite.loops) == 13

    coupling_res = suite.evaluate_coupling_impact()
    assert "ltv_cac_ratio" in coupling_res
    assert "overall_system_health" in coupling_res


def test_customer_journey_tracker():
    tracker = CustomerJourneyTracker()
    cohort = CustomerCohort(cohort_id="COHORT_2026_Q1", size=1000, current_stage=JourneyStage.AWARENESS)
    tracker.register_cohort(cohort)

    updated = tracker.advance_cohort("COHORT_2026_Q1", JourneyStage.INTEREST, conversion_rate=0.25)
    assert updated.size == 250
    assert updated.current_stage == JourneyStage.INTEREST

    # Test retention curve flattening
    cohort.retention_curve_slope = -0.005
    assert tracker.analyze_retention_flattening("COHORT_2026_Q1") is True


def test_company_growth_classifier():
    classifier = CompanyGrowthClassifier()

    p_idea = classifier.classify_stage({"paying_customers": 0})
    assert p_idea.stage == CompanyGrowthStage.IDEA

    p_val = classifier.classify_stage({"paying_customers": 3})
    assert p_val.stage == CompanyGrowthStage.VALIDATION

    p_growth = classifier.classify_stage({"paying_customers": 100, "arr_dollars": 5_000_000})
    assert p_growth.stage == CompanyGrowthStage.GROWTH


def test_opportunity_pursuit_decision_tree():
    tree = OpportunityPursuitDecisionTree()

    # Noise signal -> Discard
    res1 = tree.evaluate({"is_structural_anomaly": False})
    assert res1.action == "DISCARD"

    # Structural, reversible, cheap test available -> Run cheap test
    res2 = tree.evaluate({
        "is_structural_anomaly": True,
        "is_reversible": True,
        "cheap_test_available": True,
    })
    assert res2.action == "RUN_CHEAP_TEST"

    # Cheap test passed & structural advantage -> Commit
    res3 = tree.evaluate({
        "is_structural_anomaly": True,
        "is_reversible": True,
        "cheap_test_available": True,
        "cheap_test_passed": True,
        "has_structural_advantage": True,
    })
    assert res3.action == "COMMIT"


def test_failure_mode_monitor():
    monitor = FailureModeMonitor()

    warnings = monitor.audit_metrics({
        "survey_nps": 90,
        "daily_active_ratio": 0.02,
        "build_velocity_tickets": 60,
        "demand_conversion_rate": 0.005,
        "cac_growth_rate": 0.8,
        "ltv_growth_rate": 0.05,
        "active_unvalidated_bets": 6,
    })

    assert len(warnings) == 4
    failure_modes = {w.failure_mode for w in warnings}
    assert "Solving wrong problem" in failure_modes
    assert "Building before validating" in failure_modes
    assert "Scaling prematurely" in failure_modes
    assert "Capital misallocation" in failure_modes
