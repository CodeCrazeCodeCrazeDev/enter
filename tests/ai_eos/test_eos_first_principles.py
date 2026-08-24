"""Comprehensive unit and integration test suite for the First-Principles EOS Engine.

Verifies Bayesian anomaly detection, Type I / Type II risk classification,
living mental model evolution, 13 coupled business loops, 15 customer journey stages,
9 growth stage classifications, 6 competitive moats, failure mode monitoring,
system state transitions, pursuit decision trees, and full end-to-end execution cycles.
"""

from __future__ import annotations
import pytest
from apodex.ai_eos.intelligence.eos_first_principles import (
    FirstPrinciplesEOS,
    Timescale,
    RiskType,
    JourneyStage,
    GrowthStage,
    SystemState,
    AnomalyDetector,
    RiskEvaluator,
    MentalModelTracker,
    CoupledBusinessLoops,
    CustomerLifecycleManager,
    GrowthStageClassifier,
    StrategicThinkingEngine,
    FailureModeMonitor,
    SystemStateMachine,
    PursuitDecisionTree,
    CompanyStocks,
)


def test_anomaly_detector_bayesian_surprise():
    detector = AnomalyDetector()

    # Low surprise signal
    sig_low = detector.process_signal("demand", observed=1.05, expected=1.0, variance=1.0)
    assert not sig_low.is_structural_shift
    assert sig_low.bayesian_surprise_score < 1.0

    # Structural anomaly signal
    sig_high = detector.process_signal("demand", observed=3.5, expected=1.0, variance=1.0)
    assert sig_high.is_structural_shift
    assert sig_high.bayesian_surprise_score >= 2.5


def test_risk_evaluator_doors():
    evaluator = RiskEvaluator()

    # Reversible / low exposure -> Type II door
    risk_type_2 = evaluator.evaluate_risk(
        reversibility_score=0.9,
        financial_exposure_cents=5_000_00,
        total_cash_cents=100_000_00
    )
    assert risk_type_2 == RiskType.TYPE_II

    # Irreversible / high exposure -> Type I door
    risk_type_1 = evaluator.evaluate_risk(
        reversibility_score=0.2,
        financial_exposure_cents=30_000_00,
        total_cash_cents=100_000_00
    )
    assert risk_type_1 == RiskType.TYPE_I


def test_mental_model_tracker_ossification():
    tracker = MentalModelTracker("Pricing Model")
    tracker.update_parameter("price", 99.0)

    # Simulate parameter tuning despite failed predictions
    for _ in range(12):
        tracker.update_parameter("price", 99.0)
        tracker.record_prediction_outcome(predicted=100.0, actual=10.0)

    assert tracker.is_ossified() is True

    # Paradigm shift / structural update resets ossification
    tracker.update_structure({"freemium_tier": 0.0, "enterprise_tier": 500.0})
    assert tracker.is_ossified() is False


def test_coupled_business_loops():
    stocks = CompanyStocks(cash_cents=1_000_000_00, talent_count=5, brand_trust_score=0.5)
    loops = CoupledBusinessLoops(initial_stocks=stocks)

    updated_stocks = loops.execute_coupled_cycle(
        R_and_D_spend_cents=50_000_00,
        marketing_spend_cents=100_000_00
    )

    assert updated_stocks.data_points > 1000
    assert updated_stocks.brand_trust_score > 0.5


def test_customer_lifecycle_manager():
    mgr = CustomerLifecycleManager()
    assert mgr.stage_counts[JourneyStage.AWARENESS] == 1000

    # Transition cohort Awareness -> Interest
    converted = mgr.transition_cohort(JourneyStage.AWARENESS, conversion_rate=0.10)
    assert converted == 100
    assert mgr.stage_counts[JourneyStage.INTEREST] == 100

    health = mgr.calculate_health_index()
    assert 0.0 <= health <= 1.0


def test_growth_stage_classifier_and_premature_scaling():
    classifier = GrowthStageClassifier()

    # Stage classification
    stage = classifier.classify_stage(
        paying_customers=150,
        retention_flattened=True,
        yoy_growth_rate=0.2,
        rule_of_40=0.1,
        ecosystem_gmv_cents=0
    )
    assert stage == GrowthStage.PMF

    # Premature scaling check
    is_premature = classifier.detect_premature_scaling(
        stage=GrowthStage.STARTUP,
        cac_growth_rate=0.5,
        ltv_growth_rate=0.1
    )
    assert is_premature is True


def test_strategic_thinking_moats_and_cost_curves():
    engine = StrategicThinkingEngine()

    # Cost curve crossing
    viable, projected = engine.check_cost_curve_viability(
        current_unit_cost=100.0,
        threshold_cost=20.0,
        annual_reduction_rate=0.30,
        years_out=5.0
    )
    assert viable is True
    assert projected < 20.0

    # 6 Moats durability scoring
    moats = engine.evaluate_6_moats(
        network_density=0.8,
        switching_cost_cents=4000_00,
        cost_advantage_percent=0.25,
        brand_trust=0.9,
        ip_count=5,
        counter_positioning_score=0.7
    )
    assert moats["durability_composite"] > 0.5


def test_failure_mode_monitor():
    monitor = FailureModeMonitor()
    warnings = monitor.check_failure_modes({
        "survey_satisfaction": 0.9,
        "active_usage": 0.05,
        "decision_latency_hours": 72.0,
        "cac_growth_rate": 0.4,
        "ltv_growth_rate": 0.1
    })

    assert len(warnings) >= 3
    failure_names = [w["failure_mode"] for w in warnings]
    assert "Solving wrong problem" in failure_names
    assert "Organizational bottlenecks" in failure_names
    assert "Scaling prematurely" in failure_names


def test_system_state_machine_and_pursuit_decision_tree():
    sm = SystemStateMachine()
    assert sm.current_state == SystemState.SENSING

    sm.transition_to(SystemState.HYPOTHESIS, "Anomaly observed")
    assert sm.current_state == SystemState.HYPOTHESIS

    tree = PursuitDecisionTree()
    res_commit = tree.evaluate_pursuit(
        is_structural_anomaly=True,
        is_reversible_risk=True,
        has_high_confidence_multi_signal=True,
        cheap_test_available=True,
        test_result_exceeds_kill_threshold=True,
        expected_value_positive=True,
        has_structural_advantage=True
    )
    assert res_commit["decision"] == "COMMIT_RESOURCES"

    res_discard = tree.evaluate_pursuit(
        is_structural_anomaly=False,
        is_reversible_risk=True,
        has_high_confidence_multi_signal=True,
        cheap_test_available=True,
        test_result_exceeds_kill_threshold=True,
        expected_value_positive=True,
        has_structural_advantage=True
    )
    assert res_discard["decision"] == "DISCARD"


def test_first_principles_eos_e2e_cycle():
    eos = FirstPrinciplesEOS()

    res = eos.run_full_execution_cycle(
        observed_market_signal=4.0,
        expected_market_signal=1.0,
        reversibility=0.8,
        proposed_spend_cents=10000_00,
        R_and_D_spend_cents=50000_00,
        marketing_spend_cents=100000_00
    )

    assert res["anomaly_signal"]["is_structural_shift"] is True
    assert res["risk_type"] == "type_ii"
    assert res["pursuit_decision"]["decision"] == "COMMIT_RESOURCES"
    assert "kpi_stack" in res
    assert res["kpi_stack"]["current_system_state"] == "hypothesis"
