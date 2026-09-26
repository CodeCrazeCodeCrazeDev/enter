"""Unit and integration tests for First-Principles Entrepreneurial Operating System (EOS) Engine."""

import pytest
from apodex.ai_eos.intelligence.eos_first_principles import (
    EOSEngineFirstPrinciples,
    MasterNode,
    MasterLoopState,
    DecisionRiskType,
    AnomalySignal,
    CognitiveHypothesis,
    CognitivePipeline,
    BusinessLoopMetrics,
    BusinessLoopsEngine,
    CustomerStage,
    CustomerLifecycleState,
    GTMChannel,
    IntegratedGTMSystem,
    GrowthStage,
    GrowthStageMetrics,
    CompanyGrowthStateMachine,
    StrategicMoatEngine,
    FailureModeDiagnostics,
    SystemState,
    DecisionTreeEvaluator,
)


def test_master_loop_transitions_and_kill_signals():
    loop = MasterLoopState()
    assert loop.current_node == MasterNode.ENVIRONMENTAL_SENSING

    # Transition forward
    loop.transition_to(MasterNode.MVP_EXPERIMENTATION)
    assert loop.current_node == MasterNode.MVP_EXPERIMENTATION

    # Trigger re-entrant kill signal
    loop.transition_to(MasterNode.OPPORTUNITY_DISCOVERY, kill_signal=True)
    assert loop.current_node == MasterNode.OPPORTUNITY_DISCOVERY
    assert MasterNode.MVP_EXPERIMENTATION in loop.history


def test_cognitive_pipeline_anomaly_and_risk_evaluation():
    pipeline = CognitivePipeline()

    signal = AnomalySignal(
        signal_id="sig_001",
        description="Exponential compute elasticity vs pricing curve",
        observed_metric=10.5,
        expected_metric=2.0,
        is_structural_shift=True,
        confidence=0.85,
    )
    assert pipeline.detect_anomaly(signal) is True

    # Risk type check
    risk = pipeline.evaluate_risk_type(
        decision_name="Pivot core product to API",
        capital_at_risk_usd=1_000_000.0,
        regulatory_impact=False,
        reversible=False,
    )
    assert risk == DecisionRiskType.TYPE_I


def test_business_loops_evaluation():
    engine = BusinessLoopsEngine()
    metrics = BusinessLoopMetrics(
        retention_curve_flattening=0.55,
        cac_usd=300.0,
        sales_win_rate=0.25,
        net_revenue_retention=1.20,
        brand_price_elasticity=1.1,
        arpu_usd=100.0,
        viral_k_factor=0.25,
        decision_latency_hours=12.0,
        burn_multiple=1.2,
        regretted_attrition_rate=0.05,
        eNPS=45.0,
        hit_rate_experiments=0.22,
        feature_parity_gap=0.10,
    )
    results = engine.evaluate_loops(metrics)
    for loop_name, (is_healthy, msg) in results.items():
        assert is_healthy is True, f"Loop {loop_name} failed: {msg}"


def test_customer_lifecycle_and_gtm_selection():
    lifecycle = CustomerLifecycleState()
    assert lifecycle.current_stage == CustomerStage.AWARENESS
    lifecycle.advance_stage(CustomerStage.ACTIVATION)
    assert lifecycle.current_stage == CustomerStage.ACTIVATION

    gtm = IntegratedGTMSystem()
    channels = gtm.select_gtm_motion(acv_usd=2_500.0, product_complexity="low", network_effects=True)
    assert GTMChannel.PRODUCT_LED in channels
    assert GTMChannel.COMMUNITY_LED in channels


def test_growth_stage_machine_and_moats():
    growth = CompanyGrowthStateMachine()
    metrics = GrowthStageMetrics(
        paying_customers=500,
        ltv_to_cac=4.2,
        retention_curve_flat=True,
        growth_rate_yoy=0.85,
        rule_of_40=0.50,
        third_party_developers=150,
    )
    stage = growth.classify_stage(metrics)
    assert stage == GrowthStage.PLATFORM

    moat_engine = StrategicMoatEngine()
    moat_score = moat_engine.calculate_moat_score(
        network_density=0.8,
        switching_cost_score=0.9,
        scale_cost_advantage=0.7,
        brand_trust=0.85,
        counter_positioning=0.95,
    )
    assert 0.80 <= moat_score <= 1.0


def test_failure_mode_diagnostics():
    diagnostics = FailureModeDiagnostics()
    warnings = diagnostics.diagnose({
        "engagement": "low",
        "survey_positive": True,
        "decision_latency_hours": 72.0,
    })
    assert len(warnings) == 2
    failure_names = [w["failure_mode"] for w in warnings]
    assert "Solving the wrong problem" in failure_names
    assert "Organizational bottlenecks" in failure_names


def test_e2e_eos_first_principles_execution():
    orchestrator = EOSEngineFirstPrinciples()

    anomaly = AnomalySignal(
        signal_id="sig_002",
        description="CUDA compute demand mismatch",
        observed_metric=12.0,
        expected_metric=3.0,
        is_structural_shift=True,
        confidence=0.90,
    )
    op_metrics = BusinessLoopMetrics(
        retention_curve_flattening=0.60,
        cac_usd=200.0,
        sales_win_rate=0.30,
        net_revenue_retention=1.25,
        brand_price_elasticity=1.0,
        arpu_usd=150.0,
        viral_k_factor=0.30,
        decision_latency_hours=8.0,
        burn_multiple=1.1,
        regretted_attrition_rate=0.02,
        eNPS=55.0,
        hit_rate_experiments=0.30,
        feature_parity_gap=0.05,
    )
    growth_metrics = GrowthStageMetrics(
        paying_customers=1200,
        ltv_to_cac=5.0,
        retention_curve_flat=True,
        growth_rate_yoy=1.2,
        rule_of_40=0.65,
        third_party_developers=600,
    )
    decision_inputs = {
        "is_structural_anomaly": True,
        "is_reversible": True,
        "high_confidence_multi_source": True,
        "cheap_test_available": True,
        "test_result_exceeds_threshold": True,
        "ev_clearly_positive": True,
        "structural_advantage": True,
        "test_observed_val": 0.50,
    }

    # Cycle 1: Sensing -> Anomaly -> HYPOTHESIS
    res1 = orchestrator.run_execution_cycle(
        anomaly_signal=anomaly,
        operating_metrics=op_metrics,
        growth_metrics=growth_metrics,
        decision_inputs=decision_inputs,
    )
    assert orchestrator.current_state == SystemState.HYPOTHESIS

    # Cycle 2: HYPOTHESIS -> Decision Tree -> CHEAP_TEST
    res2 = orchestrator.run_execution_cycle(
        anomaly_signal=None,
        operating_metrics=op_metrics,
        growth_metrics=growth_metrics,
        decision_inputs=decision_inputs,
    )
    assert orchestrator.current_state == SystemState.CHEAP_TEST

    # Cycle 3: CHEAP_TEST -> VALIDATION
    res3 = orchestrator.run_execution_cycle(
        anomaly_signal=None,
        operating_metrics=op_metrics,
        growth_metrics=growth_metrics,
        decision_inputs=decision_inputs,
    )
    assert orchestrator.current_state == SystemState.VALIDATION
    assert res3["growth_stage"] == GrowthStage.ECOSYSTEM.value
