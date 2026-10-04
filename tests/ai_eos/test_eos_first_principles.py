"""Tests for EOSEngineFirstPrinciples and first-principles EOS components."""

import pytest
from apodex.ai_eos.intelligence.eos_first_principles import (
    EOSEngineFirstPrinciples,
    EOSStage,
    RiskType,
    ExternalLoopType,
    CustomerLifecycleStage,
    GrowthStage,
    MoatType,
    FailureModeType,
    AnomalySignal,
    EOSHypothesis,
    OpportunityDecision,
    SystemStateMachine,
    EOSOpportunityDecisionTree,
    AnomaliesAndSensingEngine,
    ExternalBusinessLoopsEngine,
    CustomerLifecycleEngine,
    GTMSystemSimulator,
    CompanyGrowthStateMachine,
    StrategicMoatEngine,
    FailureModeMonitor,
    KPISystemStack,
)


def test_system_state_machine_valid_and_invalid_transitions():
    sm = SystemStateMachine(EOSStage.SENSING)
    assert sm.current_stage == EOSStage.SENSING

    # Valid transition Sensing -> Hypothesis
    assert sm.transition_to(EOSStage.HYPOTHESIS, "Anomaly detected") is True
    assert sm.current_stage == EOSStage.HYPOTHESIS

    # Invalid transition Hypothesis -> OPERATE (not allowed)
    assert sm.transition_to(EOSStage.OPERATE, "Illegal skip") is False
    assert sm.current_stage == EOSStage.HYPOTHESIS

    # Valid Hypothesis -> CHEAP_TEST
    assert sm.transition_to(EOSStage.CHEAP_TEST) is True
    assert len(sm.history) == 3


def test_eos_opportunity_decision_tree_branches():
    tree = EOSOpportunityDecisionTree()

    # Case 1: Noise -> Discard
    d1 = tree.evaluate("op1", is_structural_anomaly=False, is_reversible=True)
    assert d1.pursue is False
    assert "noise" in d1.rationale.lower()

    # Case 2: Type I irreversible without high confidence -> Discard
    d2 = tree.evaluate(
        "op2",
        is_structural_anomaly=True,
        is_reversible=False,
        high_confidence_multi_source=False
    )
    assert d2.pursue is False
    assert "type i" in d2.rationale.lower()

    # Case 3: Cheap test failed -> Discard
    d3 = tree.evaluate(
        "op3",
        is_structural_anomaly=True,
        is_reversible=True,
        cheap_test_available=True,
        cheap_test_result_exceeds_kill=False
    )
    assert d3.pursue is False
    assert "cheap test result failed" in d3.rationale.lower()

    # Case 4: No structural advantage -> Discard
    d4 = tree.evaluate(
        "op4",
        is_structural_anomaly=True,
        is_reversible=True,
        cheap_test_available=True,
        cheap_test_result_exceeds_kill=True,
        structural_advantage_possible=False
    )
    assert d4.pursue is False
    assert "no structural advantage" in d4.rationale.lower()

    # Case 5: Fully approved
    d5 = tree.evaluate(
        "op5",
        is_structural_anomaly=True,
        is_reversible=True,
        cheap_test_available=True,
        cheap_test_result_exceeds_kill=True,
        structural_advantage_possible=True
    )
    assert d5.pursue is True
    assert "approved" in d5.rationale.lower()


def test_anomalies_and_sensing_engine():
    engine = AnomaliesAndSensingEngine()

    sig_noise = AnomalySignal("s1", "Random noise", is_structural_shift=False, confidence=0.3, source="test")
    assert engine.process_signal(sig_noise) is None

    sig_shift = AnomalySignal("s2", "CUDA mismatch anomaly", is_structural_shift=True, confidence=0.8, source="test")
    hyp = engine.process_signal(sig_shift)
    assert hyp is not None
    assert "CUDA mismatch anomaly" in hyp.claim

    # Risk classification
    assert engine.classify_decision_risk("pricing_test", is_reversible=True) == RiskType.TYPE_II_REVERSIBLE
    assert engine.classify_decision_risk("regulatory_launch", is_reversible=False) == RiskType.TYPE_I_IRREVERSIBLE

    # Model update
    res = engine.update_mental_model("market_growth_rate", 0.12, structural_shift=True)
    assert res["structure"]["paradigm_shift"] is True


def test_external_business_loops_engine():
    loops = ExternalBusinessLoopsEngine()

    p_state = loops.update_loop_kpis(ExternalLoopType.PRODUCT, {"retention_flattening": 0.10})
    assert p_state["status"] == "degraded"
    assert p_state["failure_mode_flagged"] is True

    f_state = loops.update_loop_kpis(ExternalLoopType.FINANCIAL, {"burn_multiple": 1.2})
    assert f_state["status"] == "healthy"


def test_customer_lifecycle_engine():
    lc = CustomerLifecycleEngine()
    lc.record_stage_conversion(CustomerLifecycleStage.ONBOARDING, 0.8)
    lc.record_stage_conversion(CustomerLifecycleStage.ACTIVATION, 0.6)
    lc.record_stage_conversion(CustomerLifecycleStage.RETENTION, 0.7)

    score = lc.calculate_health_score()
    assert 0.0 < score <= 1.0


def test_gtm_system_simulator():
    sim = GTMSystemSimulator()

    plg_motions = sim.select_gtm_motion("low", 100_00, network_effect=False)
    assert "Product-Led Growth (PLG)" in plg_motions

    slg_motions = sim.select_gtm_motion("high", 10000_00, network_effect=False)
    assert "Sales-Led Growth (SLG)" in slg_motions

    pricing_eval = sim.evaluate_pricing_alignment(value_delivered_dollars=1000.0, price_dollars=200.0)
    assert pricing_eval["is_value_based_aligned"] is True


def test_company_growth_state_machine():
    sm = CompanyGrowthStateMachine(GrowthStage.IDEA)

    assert sm.evaluate_stage_transition({"validated_learnings": 1}) == GrowthStage.IDEA
    assert sm.evaluate_stage_transition({"validated_learnings": 4}) == GrowthStage.VALIDATION
    assert sm.evaluate_stage_transition({"paying_customers": 6}) == GrowthStage.STARTUP


def test_strategic_moat_engine():
    moat_eng = StrategicMoatEngine()

    moat_eng.track_cost_curve("compute", 100.0)
    moat_eng.track_cost_curve("compute", 50.0)
    moat_eng.track_cost_curve("compute", 20.0)

    assert moat_eng.evaluate_timing_viability("compute", 25.0) is True

    score = moat_eng.calculate_moat_durability({
        MoatType.NETWORK_EFFECTS: 0.9,
        MoatType.SWITCHING_COSTS: 0.8,
        MoatType.ECONOMIES_OF_SCALE: 0.7,
        MoatType.BRAND: 0.8,
        MoatType.COUNTER_POSITIONING: 0.9,
        MoatType.REGULATORY_IP: 0.5,
    })
    assert score > 0.75


def test_failure_mode_monitor():
    monitor = FailureModeMonitor()

    metrics = {
        "survey_satisfaction": 0.9,
        "active_usage": 0.1,
        "build_velocity": 0.9,
        "demand_growth": 0.01,
        "retention_curve_slope": -0.10,
        "months_active": 12,
    }

    failures = monitor.detect_failure_modes(metrics)
    failure_types = [f[0] for f in failures]

    assert FailureModeType.SOLVING_WRONG_PROBLEM in failure_types
    assert FailureModeType.BUILDING_BEFORE_VALIDATING in failure_types
    assert FailureModeType.LACK_OF_PMF in failure_types


def test_kpi_system_stack():
    stack = KPISystemStack()
    res = stack.aggregate_kpis(
        signal_noise_ratio=0.8,
        cost_per_validated_learning=150.0,
        activation_rate=0.65,
        cac=120.0,
        burn_multiple=1.1,
        decision_latency_days=2.5,
        moat_score=0.85,
        loop_closure_time_days=7.0
    )
    assert res["sensing_signal_noise_ratio"] == 0.8
    assert res["system_loop_closure_time_days"] == 7.0


def test_eos_engine_first_principles_e2e_master_loop():
    engine = EOSEngineFirstPrinciples()

    signals = [
        AnomalySignal("sig_1", "AWS compute elasticity shift", is_structural_shift=True, confidence=0.85, source="market")
    ]

    result = engine.run_master_loop_cycle(
        signals=signals,
        opportunity_id="opp_aws_elasticity",
        human_approved_type1=True
    )

    assert result["filtered_signals_count"] == 1
    assert result["hypotheses_generated"] == 1
    assert result["decision"].pursue is True
    assert result["test_result"]["passed"] is True
    assert result["final_stage"] == EOSStage.BUILD_GATE.value
