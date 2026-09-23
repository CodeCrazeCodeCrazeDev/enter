"""
Unit and Integration Test Suite for the Entrepreneurial Operating System (EOS) First-Principles Engine.
"""

import pytest
from apodex.ai_eos.intelligence.eos_first_principles import (
    EOSEngineFirstPrinciples,
    AnomaliesAndSensingEngine,
    ExternalBusinessLoopsEngine,
    CustomerLifecycleEngine,
    GTMSystemSimulator,
    CompanyGrowthStateMachine,
    StrategicMoatEngine,
    FailureModeMonitor,
    EOSOpportunityDecisionTree,
    GrowthStage,
    LifecycleStage,
    RiskType,
    FailureMode,
    AnomalySignal,
    GTMStrategyConfig,
    StrategicMoatProfile,
)


def test_anomaly_detection_and_sensing_pipeline():
    sensing = AnomaliesAndSensingEngine()

    # Non-structural noise signal
    noise = AnomalySignal(
        signal_id="sig_001",
        description="Minor temporary traffic spike",
        is_structural_shift=False,
        observed_magnitude=105.0,
        expected_magnitude=100.0,
        domain="web_traffic",
    )
    assert sensing.evaluate_signal(noise) is None

    # Structural anomaly signal
    structural = AnomalySignal(
        signal_id="sig_002",
        description="Exponential growth in compute cost curve crossing threshold",
        is_structural_shift=True,
        observed_magnitude=500.0,
        expected_magnitude=100.0,
        domain="compute_infrastructure",
    )
    hyp = sensing.evaluate_signal(structural)
    assert hyp is not None
    assert hyp.risk_type == RiskType.TYPE_II
    assert hyp.status == "formed"

    # Test cheap experiment validation
    status = sensing.run_cheap_test(hyp.hypothesis_id, test_outcome_metric=150.0, baseline_metric=100.0)
    assert status == "validated"
    assert hyp.confidence_score > 0.5


def test_external_business_loops_and_coupling():
    loops_engine = ExternalBusinessLoopsEngine()
    assert len(loops_engine.loops) == 13
    assert "Product" in loops_engine.loops
    assert "Financial" in loops_engine.loops

    coupling = loops_engine.evaluate_loop_coupling()
    assert "hiring_capacity_score" in coupling
    assert "product_velocity_index" in coupling
    assert coupling["financial_health"] == "strong"


def test_customer_lifecycle_mapping():
    lifecycle = CustomerLifecycleEngine()
    stage_state = lifecycle.get_stage_details(LifecycleStage.ACTIVATION, current_metric_val=0.42)

    assert stage_state.stage == LifecycleStage.ACTIVATION
    assert stage_state.founder_objective == "Cross the 'aha' threshold"
    assert "habit loop" in stage_state.customer_psychology
    assert stage_state.key_metric_value == 0.42


def test_gtm_system_simulator():
    simulator = GTMSystemSimulator()

    # Valid self-serve PLG strategy
    config = GTMStrategyConfig(
        positioning_statement="For developer teams, we provide autonomous test generation to eliminate QA bottlenecks",
        target_segment="Developer Teams",
        pricing_model="value_based",
        price_point=49.0,
        primary_motion="PLG",
        selected_channels=["Organic", "Content", "PLG"],
    )
    fit = simulator.evaluate_gtm_fit(config)
    assert fit["positioning_valid"] is True
    assert fit["recommended_motion"] == "PLG"
    assert fit["motion_aligned"] is True
    assert fit["gtm_readiness_score"] >= 0.8


def test_company_growth_state_machine():
    growth = CompanyGrowthStateMachine(initial_stage=GrowthStage.IDEA)

    # Cannot transition when metric is below threshold
    allowed, msg = growth.can_transition_next(key_metric_value=2.0, metric_threshold=5.0)
    assert allowed is False
    assert "below threshold" in msg

    # Transition from IDEA to VALIDATION
    new_stage = growth.transition(key_metric_value=6.0, metric_threshold=5.0)
    assert new_stage == GrowthStage.VALIDATION


def test_strategic_moat_engine():
    moat_engine = StrategicMoatEngine()

    # Cost curve projection
    cost_res = moat_engine.evaluate_cost_curve_viability(
        baseline_cost=1000.0, annual_decay_rate=0.30, years=3, target_threshold=400.0
    )
    assert cost_res["is_commercially_viable"] is True
    assert cost_res["crossing_year"] <= 3

    # Moat durability
    profile = StrategicMoatProfile(
        network_effects_score=0.8,
        switching_costs_score=0.9,
        economies_of_scale_score=0.7,
        brand_trust_score=0.6,
        counter_positioning_score=0.85,
        regulatory_ip_score=0.5,
    )
    durability = moat_engine.calculate_moat_durability(profile)
    assert durability > 0.7


def test_failure_mode_diagnostics():
    monitor = FailureModeMonitor()

    # Simulate premature scaling / lack of PMF metrics
    bad_metrics = {
        "survey_satisfaction": 0.85,
        "daily_engagement": 0.05,
        "retention_curve_flattened": 0.0,
        "marketing_spend": 25000.0,
        "cac": 500.0,
        "arpu": 50.0,
        "sales_cycle_days": 90.0,
        "burn_multiple": 4.5,
        "growth_rate": 0.02,
    }

    warnings = monitor.diagnose_operational_metrics(bad_metrics)
    assert len(warnings) >= 3
    failure_types = [w["failure_mode"] for w in warnings]
    assert FailureMode.SOLVING_WRONG_PROBLEM.value in failure_types
    assert FailureMode.LACK_OF_PMF.value in failure_types
    assert FailureMode.WEAK_POSITIONING.value in failure_types


def test_opportunity_decision_tree():
    dt = EOSOpportunityDecisionTree()

    # Positive pursuit path
    pursue, reason = dt.evaluate_opportunity(
        is_structural_anomaly=True,
        is_reversible_decision=True,
        high_confidence_multi_source_signal=True,
        cheap_test_available=True,
        cheap_test_result_exceeds_kill_threshold=True,
        expected_value_clearly_positive=True,
        has_or_can_build_structural_advantage=True,
    )
    assert pursue is True
    assert "Commit Resources" in reason

    # Reject due to non-structural anomaly
    pursue_noise, reason_noise = dt.evaluate_opportunity(
        is_structural_anomaly=False,
        is_reversible_decision=True,
        high_confidence_multi_source_signal=True,
        cheap_test_available=True,
        cheap_test_result_exceeds_kill_threshold=True,
        expected_value_clearly_positive=True,
        has_or_can_build_structural_advantage=True,
    )
    assert pursue_noise is False
    assert "Discard" in reason_noise


def test_eos_engine_first_principles_master_loop():
    master = EOSEngineFirstPrinciples()

    signal = AnomalySignal(
        signal_id="sig_100",
        description="Shift in AI reasoning efficiency allows real-time founder simulation",
        is_structural_shift=True,
        observed_magnitude=250.0,
        expected_magnitude=50.0,
        domain="ai_infrastructure",
    )

    res = master.process_anomaly_and_decide(
        signal=signal,
        cheap_test_metric=180.0,
        baseline_metric=100.0,
        has_moat_advantage=True,
    )

    assert res["pursue_decision"] is True
    assert res["test_status"] == "validated"

    kpis = master.get_rolled_up_kpi_stack()
    assert "sensing" in kpis
    assert "validation" in kpis
    assert "financial" in kpis
    assert kpis["system_level"]["overall_loop_closure_time_days"] > 0
