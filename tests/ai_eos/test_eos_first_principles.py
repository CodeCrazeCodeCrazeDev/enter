"""Unit test suite for First-Principles Entrepreneurial Operating System (EOS)."""

import pytest
from uuid import uuid4
from apodex.ai_eos.intelligence.eos_first_principles import (
    FirstPrinciplesEOSEngine,
    EOSStateMachine,
    OpportunityDecisionTree,
    CoupledBusinessLoopsEngine,
    CustomerLifecycleEngine,
    GrowthStageClassifier,
    MoatAnalyzer,
    FailureModeMonitor,
    SystemState,
    CustomerStage,
    VentureGrowthStage,
    FailureModeType,
    OpportunityCandidate,
    AnomalySignal,
)


def test_eos_state_machine_valid_transitions():
    sm = EOSStateMachine()
    assert sm.current_state == SystemState.SENSING

    # Sensing -> Hypothesis -> CheapTest -> Validation -> BuildGate -> MVP -> GTMTest -> KillOrScale -> Scale -> Operate -> Reinvent -> Sensing
    assert sm.transition(SystemState.HYPOTHESIS) is True
    assert sm.current_state == SystemState.HYPOTHESIS

    assert sm.transition(SystemState.CHEAP_TEST) is True
    assert sm.transition(SystemState.VALIDATION) is True
    assert sm.transition(SystemState.BUILD_GATE) is True
    assert sm.transition(SystemState.MVP) is True
    assert sm.transition(SystemState.GTM_TEST) is True
    assert sm.transition(SystemState.KILL_OR_SCALE) is True
    assert sm.transition(SystemState.SCALE) is True
    assert sm.transition(SystemState.OPERATE) is True
    assert sm.transition(SystemState.REINVENT) is True
    assert sm.transition(SystemState.SENSING) is True

    assert len(sm.history) == 12


def test_eos_state_machine_invalid_transitions():
    sm = EOSStateMachine()
    # Direct jump from Sensing to Scale should fail
    assert sm.transition(SystemState.SCALE) is False
    assert sm.current_state == SystemState.SENSING


def test_opportunity_decision_tree_rejections():
    tree = OpportunityDecisionTree()

    # Reject Q1: noise
    c1 = OpportunityCandidate(is_structural_anomaly=False)
    app, msg = tree.evaluate(c1)
    assert app is False
    assert "Discarded at Q1" in msg

    # Reject Q2a: irreversible lacking high confidence
    c2 = OpportunityCandidate(
        is_structural_anomaly=True,
        is_reversible=False,
        multi_source_confidence=0.40
    )
    app, msg = tree.evaluate(c2)
    assert app is False
    assert "Discarded at Q2a" in msg

    # Reject Q4: cheap test failed threshold
    c3 = OpportunityCandidate(
        is_structural_anomaly=True,
        is_reversible=True,
        cheap_test_available=True,
        cheap_test_score=0.20,
        cheap_test_kill_threshold=0.50
    )
    app, msg = tree.evaluate(c3)
    assert app is False
    assert "Discarded at Q4" in msg

    # Reject Q4b: no cheap test and EV negative
    c4 = OpportunityCandidate(
        is_structural_anomaly=True,
        is_reversible=True,
        cheap_test_available=False,
        expected_value_positive=False
    )
    app, msg = tree.evaluate(c4)
    assert app is False
    assert "Discarded at Q4b" in msg

    # Reject Q5: no structural advantage
    c5 = OpportunityCandidate(
        is_structural_anomaly=True,
        is_reversible=True,
        cheap_test_available=True,
        cheap_test_score=0.80,
        cheap_test_kill_threshold=0.50,
        has_structural_advantage=False
    )
    app, msg = tree.evaluate(c5)
    assert app is False
    assert "Discarded at Q5" in msg


def test_opportunity_decision_tree_approval():
    tree = OpportunityDecisionTree()
    candidate = OpportunityCandidate(
        is_structural_anomaly=True,
        is_reversible=True,
        cheap_test_available=True,
        cheap_test_score=0.85,
        cheap_test_kill_threshold=0.50,
        has_structural_advantage=True
    )
    approved, msg = tree.evaluate(candidate)
    assert approved is True
    assert "Approved" in msg


def test_coupled_business_loops_engine():
    engine = CoupledBusinessLoopsEngine()
    result = engine.step_simulation(product_quality_delta=0.2, marketing_spend_cents=150000_00)

    assert "ltv_cents" in result
    assert result["ltv_to_cac"] > 0
    assert result["viral_k_factor"] > 0
    assert result["nrr"] > 1.0


def test_customer_lifecycle_engine():
    engine = CustomerLifecycleEngine()
    funnel = engine.simulate_funnel()

    assert len(funnel) == 15
    assert funnel[CustomerStage.AWARENESS] == 10000
    assert funnel[CustomerStage.REPURCHASE] <= funnel[CustomerStage.AWARENESS]

    bottleneck, ratio = engine.identify_bottleneck_stage()
    assert isinstance(bottleneck, CustomerStage)
    assert 0.0 <= ratio <= 1.0


def test_growth_stage_classifier():
    classifier = GrowthStageClassifier()

    s1 = classifier.classify_stage(0, False, 0.0, 0.0, False)
    assert s1 == VentureGrowthStage.IDEA

    s2 = classifier.classify_stage(5, False, 0.1, 0.0, False)
    assert s2 == VentureGrowthStage.VALIDATION

    s3 = classifier.classify_stage(50, True, 0.30, 0.10, False)
    assert s3 == VentureGrowthStage.PMF

    s4 = classifier.classify_stage(500, True, 0.80, 0.10, False)
    assert s4 == VentureGrowthStage.GROWTH

    s5 = classifier.classify_stage(1000, True, 0.40, 0.40, False)
    assert s5 == VentureGrowthStage.SCALE


def test_moat_analyzer():
    analyzer = MoatAnalyzer()
    scores = analyzer.calculate_7powers_score(
        network_density=0.8,
        switching_cost_cents=8000_00,
        cornered_resource_uniqueness=0.9,
        counter_positioning_delta=0.7,
        scale_cost_advantage=0.6,
        process_power_efficiency=0.5,
        brand_trust_score=0.9
    )

    assert len(scores) == 8
    assert "composite_moat_score" in scores
    assert 0.0 <= scores["composite_moat_score"] <= 1.0


def test_failure_mode_monitor():
    monitor = FailureModeMonitor()

    # Telemetry triggering "Solving Wrong Problem" and "Premature Scaling"
    telemetry = {
        "survey_satisfaction": 0.90,
        "retention_30d": 0.05,
        "growth_rate": 0.80,
        "cac_cents": 20000_00,
        "ltv_cents": 10000_00,
    }

    alerts = monitor.evaluate_telemetry(telemetry)
    assert len(alerts) >= 2
    types = [a.failure_type for a in alerts]
    assert FailureModeType.SOLVING_WRONG_PROBLEM in types
    assert FailureModeType.PREMATURE_SCALING in types


def test_first_principles_eos_engine_orchestration():
    engine = FirstPrinciplesEOSEngine()

    candidate = OpportunityCandidate(
        is_structural_anomaly=True,
        is_reversible=True,
        cheap_test_available=True,
        cheap_test_score=0.90,
        cheap_test_kill_threshold=0.50,
        has_structural_advantage=True
    )

    telemetry = {
        "product_quality_delta": 0.15,
        "marketing_spend_cents": 60000_00,
        "paying_customers": 100,
        "retention_curve_flattened": True,
        "yoy_growth_rate": 0.70,
        "rule_of_40": 0.20,
        "has_ecosystem_developers": False,
        "network_density": 0.5,
        "switching_cost_cents": 4000_00,
    }

    result = engine.run_cycle(candidate, telemetry)

    assert result["opportunity_approved"] is True
    assert result["current_system_state"] == SystemState.HYPOTHESIS.value
    assert result["growth_stage"] == VentureGrowthStage.GROWTH.value
    assert "composite_moat_score" in result
    assert "coupled_loops" in result
