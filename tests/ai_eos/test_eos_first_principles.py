"""Tests for Entrepreneurial Operating System (EOS) First-Principles Engine."""

import pytest
from uuid import uuid4
from apodex.ai_eos.intelligence import (
    EOSState,
    GrowthStage,
    DecisionType,
    OpportunitySignal,
    FalsifiableHypothesis,
    ExperimentResult,
    VentureCohortMetrics,
    Initiative,
    SensingAgent,
    HypothesisEngineFirstPrinciples,
    ValidationAgent,
    GTMSimulator,
    GrowthStageClassifier,
    MoatAnalyzerFirstPrinciples,
    FailureModeMonitor,
    CapitalAllocator,
    ReinventionTrigger,
    GovernanceSafetyLayer,
    EOSEngineFirstPrinciples,
)


def test_sensing_agent_anomaly_detection():
    sensing = SensingAgent(surprise_threshold=2.0)
    normal_signal = OpportunitySignal(
        source="market_api",
        metric_name="traffic_growth",
        observed_value=10.5,
        baseline_expected_value=10.0,
        variance=1.0
    )
    res_normal = sensing.evaluate_signal(normal_signal)
    assert not res_normal["is_anomaly"]
    assert res_normal["recommendation"] == "IGNORE_NOISE"

    anomaly_signal = OpportunitySignal(
        source="market_api",
        metric_name="cuda_traffic",
        observed_value=50.0,
        baseline_expected_value=10.0,
        variance=1.0
    )
    res_anomaly = sensing.evaluate_signal(anomaly_signal)
    assert res_anomaly["is_anomaly"]
    assert res_anomaly["recommendation"] == "FORM_HYPOTHESIS"


def test_hypothesis_engine_lifecycle():
    engine = HypothesisEngineFirstPrinciples()
    hyp = engine.generate_hypothesis("Test Title", "Test Falsifiable Claim", prior=0.5)

    exp_success = ExperimentResult(
        hypothesis_id=hyp.hypothesis_id,
        cost_cents=100_00,
        p_value=0.01,
        effect_size=1.0,
        sample_size=100,
        success=True,
        summary="Positive conversion signal"
    )

    updated_1 = engine.update_hypothesis(hyp.hypothesis_id, exp_success)
    assert updated_1.posterior_confidence > 0.5
    assert len(updated_1.supporting_evidence) == 1

    exp_success_2 = ExperimentResult(
        hypothesis_id=hyp.hypothesis_id,
        cost_cents=100_00,
        p_value=0.01,
        effect_size=1.0,
        sample_size=100,
        success=True,
        summary="Second positive signal"
    )
    updated_2 = engine.update_hypothesis(hyp.hypothesis_id, exp_success_2)
    assert updated_2.posterior_confidence >= 0.80
    assert updated_2.status == "CONFIRMED"


def test_validation_agent_economic_viability():
    validator = ValidationAgent()
    hyp = FalsifiableHypothesis(
        title="Valid Hyp",
        falsifiable_claim="Claim",
        posterior_confidence=0.85,
        status="CONFIRMED"
    )

    res = validator.evaluate_economic_viability(
        hypothesis=hyp,
        estimated_tam_cents=100000000_00,  # $100M
        target_margin=0.80,
        test_cost_cents=1000_00
    )

    assert res["cleared_build_gate"]
    assert res["test_roi_ratio"] > 100.0


def test_gtm_simulator_unit_economics():
    simulator = GTMSimulator()
    metrics = VentureCohortMetrics(
        traffic=10000,
        conversion_rate=0.05,
        arpu_cents=100_00,  # $100
        cac_cents=200_00,   # $200
        churn_rate=0.02     # LTV = $100 / 0.02 = $5000 -> LTV:CAC = 25:1
    )
    sim_res = simulator.simulate_cohort(metrics)
    assert sim_res["acquired_customers"] == 500
    assert sim_res["ltv_cac_ratio"] == 25.0
    assert sim_res["payback_months"] == 2.0
    assert sim_res["is_scalable"]


def test_growth_stage_classifier():
    classifier = GrowthStageClassifier()
    stage_res = classifier.classify_stage(
        validated_learnings_count=10,
        paying_customers=500,
        retention_curve_flattened=True,
        growth_rate_mom=0.15,
        ecosystem_gmv_cents=0
    )
    assert stage_res["growth_stage"] == GrowthStage.PMF.value
    assert stage_res["binding_constraint"] == "Team Bandwidth & Process Execution"
    assert not stage_res["premature_scaling_risk"]


def test_moat_analyzer_scoring():
    moat_analyzer = MoatAnalyzerFirstPrinciples()
    res = moat_analyzer.score_moat(
        network_density=0.8,
        switching_cost_score=0.9,
        scale_economies_score=0.7,
        brand_trust_score=0.6,
        counter_positioning=True,
        cornered_resource=False
    )
    assert res["moat_durability_score"] >= 0.70
    assert res["is_defensible"]


def test_failure_mode_monitor():
    monitor = FailureModeMonitor()
    alerts = monitor.evaluate_health(
        burn_multiple=3.5,
        retention_curve_flattened=False,
        decision_latency_days=20.0,
        cac_payback_months=24.0
    )
    assert len(alerts) == 3
    failure_types = [a["failure_mode"] for a in alerts]
    assert "Capital Misallocation / High Burn" in failure_types
    assert "Organizational Bottleneck" in failure_types


def test_capital_allocator_opportunity_cost():
    allocator = CapitalAllocator()
    i1 = Initiative(
        name="High EV Bet",
        expected_return_cents=10000_00,
        required_budget_cents=1000_00,
        risk_factor=0.1,
        strategic_alignment=0.9
    )
    i2 = Initiative(
        name="Low EV Bet",
        expected_return_cents=2000_00,
        required_budget_cents=1000_00,
        risk_factor=0.8,
        strategic_alignment=0.5
    )

    alloc_res = allocator.allocate_capital([i1, i2], total_available_budget_cents=1500_00)
    assert alloc_res["funded_count"] == 1
    assert str(i1.initiative_id) in alloc_res["allocations"]


def test_reinvention_trigger():
    trigger = ReinventionTrigger()
    res = trigger.evaluate_reinvention_need(
        revenue_decay_rate_mom=0.20,
        churn_rate=0.25,
        competitor_feature_disruption=True
    )
    assert res["should_reinvent"]
    assert res["action"] == "TRIGGER_PARALLEL_SENSING"


def test_governance_safety_layer():
    gov = GovernanceSafetyLayer()
    # Type I irreversible decision without human approval
    t1_res = gov.evaluate_decision(
        decision_name="Major M&A Acquisition",
        decision_type=DecisionType.TYPE_I,
        is_reversible=False,
        capital_at_risk_cents=50000000_00,
        human_approved=False
    )
    assert not t1_res["allowed"]

    # Type II reversible decision
    t2_res = gov.evaluate_decision(
        decision_name="Ad Copy Experiment",
        decision_type=DecisionType.TYPE_II,
        is_reversible=True,
        capital_at_risk_cents=500_00,
        human_approved=False
    )
    assert t2_res["allowed"]


def test_eos_engine_master_loop():
    engine = EOSEngineFirstPrinciples()

    signals = [
        OpportunitySignal(
            source="market_feed",
            metric_name="genai_adoption_rate",
            observed_value=85.0,
            baseline_expected_value=10.0,
            variance=1.0
        )
    ]

    master_res = engine.run_master_cycle(
        signals=signals,
        available_capital_cents=50000_00,
        human_governance_approved=True
    )

    assert master_res["anomalies_detected"] == 1
    assert master_res["hypotheses_created"] == 1
    assert master_res["validated_hypotheses_count"] == 1
    assert master_res["final_state"] == EOSState.OPERATE.value
