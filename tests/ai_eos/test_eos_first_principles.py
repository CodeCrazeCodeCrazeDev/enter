import pytest
from apodex.ai_eos.intelligence import (
    EOSEngineFirstPrinciples,
    DecisionType,
    CompanyStage,
    CustomerLifecycleStage,
    BusinessLoopType,
    GTMSimulationConfig
)

def test_eos_sensing_and_hypothesis_filtering():
    engine = EOSEngineFirstPrinciples()

    # Noise signal
    sig1 = engine.sense_anomaly(
        signal_id="sig_001",
        source="CustomerSupport",
        description="Minor UI glitch report",
        is_structural=False,
        confidence=0.4
    )

    # Hypothesis generation should filter out non-structural noise
    hyp1 = engine.form_hypothesis(
        hypothesis_id="hyp_001",
        signal_id="sig_001",
        claim="UI glitch causes churn",
        kill_threshold=0.5
    )
    assert hyp1 is None

    # Structural anomaly signal
    sig2 = engine.sense_anomaly(
        signal_id="sig_002",
        source="MarketData",
        description="Bandwidth cost dropped 100x enabling streaming",
        is_structural=True,
        confidence=0.85
    )

    hyp2 = engine.form_hypothesis(
        hypothesis_id="hyp_002",
        signal_id="sig_002",
        claim="Video streaming becomes main distribution channel",
        kill_threshold=0.6,
        decision_type=DecisionType.TYPE_II
    )
    assert hyp2 is not None
    assert hyp2.belief_score == 0.85
    assert hyp2.status == "active"


def test_eos_cheap_testing_and_belief_updating():
    engine = EOSEngineFirstPrinciples()

    engine.sense_anomaly("sig_1", "TechShift", "CUDA enables general GPU compute", True, 0.7)
    engine.form_hypothesis("hyp_1", "sig_1", "Accelerated computing replaces CPU for ML", 0.65)

    # Run cheap test that passes
    res1 = engine.run_cheap_test("test_1", "hyp_1", cost=500.0, metric_measured="benchmarks", metric_value=0.8)
    assert res1.passed_kill_threshold is True
    hyp = engine.hypotheses["hyp_1"]
    assert hyp.status == "strengthened"
    assert hyp.belief_score > 0.7

    # Run cheap test that fails
    res2 = engine.run_cheap_test("test_2", "hyp_1", cost=200.0, metric_measured="conversion", metric_value=0.2)
    assert res2.passed_kill_threshold is False
    assert hyp.status == "falsified"


def test_eos_business_loop_monitoring_and_failure_mode():
    engine = EOSEngineFirstPrinciples()

    # Update product loop with negative retention slope
    state = engine.update_business_loop(
        loop_type=BusinessLoopType.PRODUCT,
        inputs={"features_shipped": 5},
        outputs={"mau": 1000},
        kpis={"retention_slope": -0.1, "nps": 20}
    )

    assert state.failure_mode_detected is not None

    alerts = engine.diagnose_failure_modes()
    assert len(alerts) > 0
    assert any("loudest customer" in alert.failure_mode.lower() or "wrong problem" in alert.failure_mode.lower() for alert in alerts)


def test_eos_customer_journey_analysis():
    engine = EOSEngineFirstPrinciples()

    metrics = engine.analyze_customer_journey(
        stage=CustomerLifecycleStage.ACTIVATION,
        conversion_rate=0.25,
        dropoff_rate=0.75,
        key_metric=0.25
    )

    assert metrics.stage == CustomerLifecycleStage.ACTIVATION
    assert "aha" in metrics.optimization_lever.lower()


def test_eos_gtm_simulation():
    engine = EOSEngineFirstPrinciples()

    # High price enterprise config
    config_ent = GTMSimulationConfig(
        positioning="Enterprise AI Security Platform",
        pricing_model="enterprise",
        price_point=50000.0,
        primary_channel="SLG",
        target_segment="Fortune 500"
    )
    res_ent = engine.simulate_gtm(config_ent)
    assert res_ent.recommended_motion == "Sales-Led Growth (SLG)"
    assert res_ent.channel_fit_score == 0.9

    # Low price PLG config
    config_plg = GTMSimulationConfig(
        positioning="Developer API for Async Jobs",
        pricing_model="usage_based",
        price_point=100.0,
        primary_channel="PLG",
        target_segment="Indie Hackers"
    )
    res_plg = engine.simulate_gtm(config_plg)
    assert res_plg.recommended_motion == "Product-Led Growth (PLG)"


def test_eos_growth_stage_assessment():
    engine = EOSEngineFirstPrinciples()

    assessment = engine.assess_growth_stage(
        stage=CompanyStage.STARTUP,
        metrics={"retention_flattened": 0.2, "cac_ltv_ratio": 0.5}
    )

    assert assessment.current_stage == CompanyStage.STARTUP
    assert assessment.premature_scaling_risk > 0.5


def test_eos_decision_tree_evaluation():
    engine = EOSEngineFirstPrinciples()

    # Case 1: Noise anomaly -> Discard
    res_noise = engine.evaluate_opportunity_decision_tree(
        is_structural_anomaly=False,
        is_reversible_decision=True,
        high_confidence_multi_source=False,
        cheap_test_available=True,
        test_result_exceeds_kill_threshold=True,
        expected_value_positive=True,
        has_structural_advantage=True
    )
    assert res_noise.pursue is False

    # Case 2: Structural + Reversible + Cheap Test Passed + Moat -> Pursue
    res_go = engine.evaluate_opportunity_decision_tree(
        is_structural_anomaly=True,
        is_reversible_decision=True,
        high_confidence_multi_source=True,
        cheap_test_available=True,
        test_result_exceeds_kill_threshold=True,
        expected_value_positive=True,
        has_structural_advantage=True
    )
    assert res_go.pursue is True
    assert "GO" in res_go.decision_path[-1]


def test_eos_research_os_cross_layer_ingestion():
    engine = EOSEngineFirstPrinciples()

    hyp = engine.ingest_validated_research(
        hypothesis_id="res_hyp_101",
        claim="Multi-agent token bidding reduces coordination latency by 40%",
        kill_threshold=0.65
    )

    assert hyp is not None
    assert hyp.hypothesis_id == "res_hyp_101"
    assert len(engine.get_active_hypotheses()) == 1
