"""Unit and integration test suite for First-Principles EOS Subsystem."""

import pytest
from apodex.ai_eos.intelligence.eos_first_principles import (
    LoopTimescale,
    TimescaleLoop,
    AnomalySignal,
    SignalToIdeaPipeline,
    OpportunityDecisionTree,
    ExternalBusinessLoopSystem,
    CustomerStage,
    CustomerLifecycleState,
    GrowthStage,
    VentureMetrics,
    GrowthStageClassifier,
    MoatType,
    StrategicMoatProfile,
    FailureModeMonitor,
    AIEOSKernel
)


def test_timescale_loop_execution():
    fast_loop = TimescaleLoop(
        name="Ad Test Loop",
        timescale=LoopTimescale.FAST,
        cycle_time_days=3.0,
        signal_fidelity=0.9,
        compounding_score=1.0
    )
    initial_score = fast_loop.compounding_score
    updated_score = fast_loop.execute_cycle(feedback_quality=0.85)
    assert updated_score > initial_score


def test_signal_to_idea_pipeline():
    pipeline = SignalToIdeaPipeline()
    weak_signal = AnomalySignal(
        signal_id="sig_001",
        description="Compute cost drop",
        is_structural_shift=False,
        observed_value=10.0,
        expected_value=100.0,
        confidence=0.4
    )
    assert pipeline.evaluate_signal(weak_signal) is None

    structural_signal = AnomalySignal(
        signal_id="sig_002",
        description="GPU Memory Bandwidth Cost Cut",
        is_structural_shift=True,
        observed_value=10.0,
        expected_value=100.0,
        confidence=0.85
    )
    hypothesis = pipeline.evaluate_signal(structural_signal)
    assert hypothesis is not None
    assert hypothesis.is_reversible is True

    test_outcome = pipeline.execute_cheap_test(hypothesis, test_result_value=0.20)
    assert test_outcome == "STRENGTHENED"
    assert hypothesis.is_validated is True


def test_opportunity_decision_tree():
    # Reversible decision with passing cheap test
    res = OpportunityDecisionTree.evaluate_opportunity(
        is_structural_anomaly=True,
        is_reversible=True,
        cheap_test_available=True,
        test_passed=True,
        expected_value_positive=True,
        has_moat_advantage=True
    )
    assert res["decision"] == "COMMIT"

    # Reversible decision with failed cheap test
    res_failed = OpportunityDecisionTree.evaluate_opportunity(
        is_structural_anomaly=True,
        is_reversible=True,
        cheap_test_available=True,
        test_passed=False,
        expected_value_positive=True,
        has_moat_advantage=True
    )
    assert res_failed["decision"] == "DISCARD"

    # Irreversible decision without high confidence
    res_irreversible = OpportunityDecisionTree.evaluate_opportunity(
        is_structural_anomaly=True,
        is_reversible=False,
        cheap_test_available=False,
        test_passed=None,
        expected_value_positive=True,
        has_moat_advantage=True,
        high_confidence_signal=False
    )
    assert res_irreversible["decision"] == "DISCARD"


def test_external_business_loop_system():
    system = ExternalBusinessLoopSystem()
    assert len(system.loops) == 13
    assert "Product" in system.loops
    assert "Financial" in system.loops

    coupled_state = system.simulate_coupled_step()
    assert "gross_margin" in coupled_state["Financial"]


def test_customer_lifecycle_state():
    customer = CustomerLifecycleState(customer_id="cust_101", current_stage=CustomerStage.AWARENESS)
    next_stage = customer.transition_next()
    assert next_stage == CustomerStage.INTEREST

    # Fast forward to activation
    for _ in range(5):
        customer.transition_next()
    assert customer.current_stage == CustomerStage.ACTIVATION
    assert customer.activated is True


def test_growth_stage_classifier():
    metrics = VentureMetrics(
        validated_learnings_count=10,
        paying_customers_count=50,
        retention_curve_flattened=True,
        cac_payback_months=6.0,
        nrr=1.25,
        rule_of_40_score=0.42,
        third_party_developer_count=10,
        category_market_share=0.05
    )
    stage, constraint = GrowthStageClassifier.classify_stage(metrics)
    assert stage == GrowthStage.SCALE
    assert "Binding constraint" in constraint


def test_strategic_moat_profile():
    moat = StrategicMoatProfile(
        primary_moat=MoatType.NETWORK_EFFECTS,
        durability_score=0.80,
        switching_cost_barrier=7.0,
        network_density=0.90,
        cost_structure_advantage=0.60
    )
    durability = moat.evaluate_durability()
    assert 0.0 <= durability <= 1.0


def test_failure_mode_monitor():
    telemetry = {
        "build_velocity": 12.0,
        "demand_signal": 1.0,
        "growth_spend_scaling": 6.0,
        "retention_curve_flattened": False,
        "decision_latency_hrs": 80.0
    }
    alerts = FailureModeMonitor.audit_telemetry(telemetry)
    assert len(alerts) >= 3
    alert_modes = [a.failure_mode for a in alerts]
    assert "Building before validating" in alert_modes
    assert "Organizational bottlenecks" in alert_modes


def test_ai_eos_kernel_end_to_end():
    kernel = AIEOSKernel()
    anomaly = AnomalySignal(
        signal_id="sig_99",
        description="LLM inference price drop 100x",
        is_structural_shift=True,
        observed_value=0.001,
        expected_value=0.10,
        confidence=0.95
    )
    result = kernel.process_opportunity(anomaly)
    assert result["status"] == "COMMIT"
    assert result["growth_stage"] == "platform"
    assert result["moat_durability"] > 0.60
