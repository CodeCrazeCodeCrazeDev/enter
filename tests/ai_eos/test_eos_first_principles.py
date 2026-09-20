"""
Unit and Integration tests for the First-Principles Entrepreneurial Operating System (EOS) Engine.
"""

import pytest
from apodex.ai_eos.intelligence import (
    FirstPrinciplesEOSEngine,
    EOSStateMachine,
    EOSState,
    DecisionRiskType,
    OpportunityDecisionTree,
    CoupledBusinessLoopsEngine,
    CustomerLifecycleEngine,
    GTMSystemEngine,
    GrowthStageClassifier,
    MoatAnalyzer,
    FailureModeMonitor,
    FourteenLayerEntrepreneurialEngine,
)


def test_eos_state_machine_transitions():
    """Test state machine transitions and kill signal processing."""
    sm = EOSStateMachine()
    assert sm.current_state == EOSState.SENSING

    # Transition to Hypothesis on structural anomaly
    state = sm.process_signal(is_anomaly=True, is_structural=True)
    assert state == EOSState.HYPOTHESIS

    # Transition to CheapTest
    sm.transition_to(EOSState.CHEAP_TEST, "Cheap test started")
    assert sm.current_state == EOSState.CHEAP_TEST

    # Strengthened cheap test -> Validation
    state = sm.process_test_result(is_falsified=False, is_strengthened=True)
    assert state == EOSState.VALIDATION

    # Economic viability -> BuildGate
    state = sm.process_validation(economic_viability=True)
    assert state == EOSState.BUILD_GATE

    # Build and GTM test above threshold -> Scale
    state = sm.process_build_and_gtm(gtm_signal_score=0.85)
    assert state == EOSState.SCALE

    # Check history log
    assert len(sm.state_history) > 5


def test_eos_state_machine_falsification_and_kill():
    """Test state machine discard routing when falsified or below kill threshold."""
    sm = EOSStateMachine()
    sm.process_signal(is_anomaly=True, is_structural=True)
    sm.transition_to(EOSState.CHEAP_TEST, "Cheap test started")

    # Test falsification
    state = sm.process_test_result(is_falsified=True, is_strengthened=False)
    assert state == EOSState.DISCARD
    assert sm.falsified_hypotheses_count == 1


def test_opportunity_decision_tree_logic():
    """Test §10.2 decision tree logic across various decision paths."""
    tree = OpportunityDecisionTree()

    # Case 1: Noise signal -> Discard
    res1 = tree.evaluate(is_structural_anomaly=False, risk_type=DecisionRiskType.TYPE_II)
    assert res1["decision"] == "DISCARD"
    assert "Noise signal" in res1["reason"]

    # Case 2: Type I risk without multi-source high-confidence -> Discard
    res2 = tree.evaluate(
        is_structural_anomaly=True,
        risk_type=DecisionRiskType.TYPE_I,
        high_confidence_multi_source=False
    )
    assert res2["decision"] == "DISCARD"

    # Case 3: Type II risk with cheap test failing kill threshold -> Discard
    res3 = tree.evaluate(
        is_structural_anomaly=True,
        risk_type=DecisionRiskType.TYPE_II,
        cheap_test_available=True,
        cheap_test_result_exceeds_kill_threshold=False
    )
    assert res3["decision"] == "DISCARD"

    # Case 4: Complete valid path -> Commit resources
    res4 = tree.evaluate(
        is_structural_anomaly=True,
        risk_type=DecisionRiskType.TYPE_II,
        cheap_test_available=True,
        cheap_test_result_exceeds_kill_threshold=True,
        structural_advantage_buildable=True
    )
    assert res4["decision"] == "COMMIT_RESOURCES"


def test_coupled_business_loops_simulation():
    """Test 13 business loops simulation and stock/flow coupling."""
    loops = CoupledBusinessLoopsEngine()
    initial_cash = loops.stock_cash_cents

    res = loops.simulate_coupled_step(user_traffic=10000, monthly_spend_cents=5000_00)
    assert res["new_customers"] > 0
    assert res["revenue_generated_cents"] > 0
    assert loops.stock_data_volume > 1000
    assert res["runway_months"] > 0


def test_customer_lifecycle_engine():
    """Test customer lifecycle cohort health and retention curve analysis."""
    lifecycle = CustomerLifecycleEngine()

    health = lifecycle.evaluate_cohort_health()
    assert health["retention_curve_flattens"] is True
    assert health["day_30_retention"] == 0.37
    assert "bottleneck_stage" in health


def test_gtm_system_engine():
    """Test GTM system motion selection and compounding strategy."""
    gtm = GTMSystemEngine()

    # Self-serve low price -> PLG
    res1 = gtm.evaluate_channel_fit(
        product_complexity="low",
        price_tier_cents=100_00,
        has_network_effects=True
    )
    assert "PLG (Product-Led Growth)" in res1["recommended_motions"]
    assert "CLG (Community-Led Growth)" in res1["recommended_motions"]

    # High complexity enterprise -> SLG
    res2 = gtm.evaluate_channel_fit(
        product_complexity="high",
        price_tier_cents=50000_00,
        has_network_effects=False
    )
    assert "SLG (Sales-Led Growth / Enterprise Sales)" in res2["recommended_motions"]


def test_growth_stage_classifier():
    """Test company growth stage classification and premature scaling risk detection."""
    classifier = GrowthStageClassifier()

    # Premature scaling flag
    res1 = classifier.classify_stage(
        validated_learnings=10,
        paying_customers=600,
        retention_flattens=False,
        cac_payback_months=18.0,
        developer_ecosystem_active=False
    )
    assert res1["risk"] == "PREMATURE_SCALING"

    # Scale stage
    res2 = classifier.classify_stage(
        validated_learnings=50,
        paying_customers=2000,
        retention_flattens=True,
        cac_payback_months=6.0,
        developer_ecosystem_active=False
    )
    assert res2["stage"] == "Scale"


def test_moat_analyzer():
    """Test moat durability calculation and cost curve checks."""
    moat = MoatAnalyzer()

    durability = moat.calculate_moat_durability(
        network_density=0.8,
        switching_cost_cents=5000_00,
        economies_of_scale_margin=0.5,
        brand_trust=0.7,
        counter_positioning_score=0.9
    )
    assert 0.0 <= durability["composite_moat_score"] <= 1.0
    assert durability["composite_moat_score"] > 0.5

    cost_check = moat.check_cost_curve_viability(unit_cost_history=[100.0, 50.0, 20.0], viability_threshold=25.0)
    assert cost_check is True


def test_failure_mode_monitor():
    """Test metric auditing and failure mode alert generation."""
    monitor = FailureModeMonitor()

    alerts = monitor.audit_metrics(
        engagement_rate=0.05,
        survey_positive_rate=0.90,
        cac_cents=200_00,
        ltv_cents=100_00,
        retention_flattens=False,
        decision_latency_hr=72.0
    )
    assert len(alerts) >= 2
    alert_modes = [a["mode"] for a in alerts]
    assert "SOLVING_WRONG_PROBLEM" in alert_modes
    assert "ORGANIZATIONAL_BOTTLENECK" in alert_modes


def test_fourteen_layer_engine():
    """Test 14-layer pipeline execution."""
    engine = FourteenLayerEntrepreneurialEngine()
    res = engine.execute_layer_pipeline("Autonomous AI Opportunity")
    assert res["layers_executed"] == 14
    assert res["status"] == "VALIDATED_AND_ROUTED"


def test_first_principles_eos_engine_master_loop():
    """Test end-to-end master loop cycle execution in FirstPrinciplesEOSEngine."""
    master_engine = FirstPrinciplesEOSEngine()

    # Cycle 1: Discard path
    res_discard = master_engine.run_master_loop_cycle(
        signal_title="Noise Signal",
        is_structural_anomaly=False
    )
    assert res_discard["loop_status"] == "TERMINATED_EARLY"

    # Cycle 2: Compounding path
    res_compound = master_engine.run_master_loop_cycle(
        signal_title="AI Inference Cost Curve Drop",
        is_structural_anomaly=True,
        risk_type=DecisionRiskType.TYPE_II,
        cheap_test_score=0.85,
        traffic=20000,
        monthly_spend_cents=10000_00
    )
    assert res_compound["loop_status"] == "COMPOUNDING"
    assert res_compound["growth_stage"]["stage"] in ("Growth", "Scale")
    assert res_compound["layer_pipeline"]["layers_executed"] == 14
