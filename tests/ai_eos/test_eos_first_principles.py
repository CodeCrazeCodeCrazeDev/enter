"""Unit and integration test suite for EOS First-Principles Reconstruction.

Verifies signal filtering, risk categorization, mental model evolution, 13 coupled business loops,
customer journey stages, GTM motions, growth classification, moats, failure modes,
state machine transitions, decision tree logic, and integrated AI OS execution.
"""

from __future__ import annotations
import pytest
from uuid import uuid4

from apodex.ai_eos.intelligence.eos_first_principles import (
    LoopTimescale,
    FeedbackLoopMetrics,
    DecisionRiskType,
    WeakSignal,
    SignalToHypothesisPipeline,
    MentalModelTracker,
    BusinessLoopType,
    BusinessLoopCoupler,
    JourneyStage,
    CustomerJourneyEngine,
    GTMMotion,
    GTMSystemEngine,
    CompanyGrowthStage,
    GrowthStageClassifier,
    MoatType,
    StrategicThinkingEngine,
    FailureModeType,
    FailureModeDetector,
    EOSState,
    EOSStateMachine,
    EOSDecisionTree,
    FirstPrinciplesEOSEngine,
)


def test_signal_to_hypothesis_pipeline_and_risk():
    """Verify weak signal filtering, anomaly detection, and Type I vs Type II risk heuristics."""
    pipeline = SignalToHypothesisPipeline()

    # Noise signal (low delta)
    noise_signal = WeakSignal("sig_01", "Daily Active Users", "analytics", observed_value=105.0, expected_value=100.0)
    assert pipeline.filter_signal(noise_signal, threshold=0.3) is False
    assert noise_signal.is_structural_anomaly is False

    # Structural anomaly signal (high delta)
    anomaly_signal = WeakSignal("sig_02", "Internet Broadband Penetration", "telecom_data", observed_value=85.0, expected_value=10.0)
    assert pipeline.filter_signal(anomaly_signal, threshold=0.3) is True
    assert anomaly_signal.is_structural_anomaly is True

    # Forced hypothesis generation
    hyp = pipeline.create_forced_hypothesis(
        signal=anomaly_signal,
        enabling_condition="Broadband penetration > 50%",
        test_cost_cents=500_00,  # $500
        kill_metric="conversion_rate",
        kill_value=0.01
    )
    assert "Broadband penetration > 50%" in hyp.claim
    assert hyp.test_cost_cents == 500_00

    # Risk categorization
    risk_type1 = pipeline.categorize_risk("Acquire Regulatory License", capital_impact_cents=2000000_00, regulatory_or_safety=True)
    assert risk_type1 == DecisionRiskType.TYPE_I

    risk_type2 = pipeline.categorize_risk("Test New Button Color", capital_impact_cents=1000_00, regulatory_or_safety=False)
    assert risk_type2 == DecisionRiskType.TYPE_II


def test_mental_model_evolution_and_ossification():
    """Verify parameter updates, structural paradigm shifts, and ossification flags."""
    tracker = MentalModelTracker("E-commerce Delivery Model")

    # Parameter update
    res1 = tracker.update_with_feedback("delivery_time_days", predicted=2.0, actual=2.4)
    assert res1["action"] == "parameter_tuned"
    assert tracker.structure_version == 1

    # Consecutive contradictions trigger structural update
    tracker.update_with_feedback("customer_churn", predicted=0.01, actual=0.10)
    res_shift = tracker.update_with_feedback("customer_churn", predicted=0.01, actual=0.12)
    assert res_shift["action"] == "structural_shift"
    assert tracker.structure_version == 2

    # Test ossification detection
    ossified_tracker = MentalModelTracker("Legacy Retail Model")
    for _ in range(12):
        ossified_tracker.parameters["cost"] = 100.0
        ossified_tracker.parameter_update_count += 1
    assert ossified_tracker.is_ossified() is True


def test_13_coupled_business_loops():
    """Verify business loop inputs, outputs, feedback signals, and failure flags."""
    coupler = BusinessLoopCoupler()

    # Product loop
    prod_state = coupler.evaluate_loop(
        BusinessLoopType.PRODUCT,
        {"retention_curve_slope": 0.05, "nps": 65.0, "building_for_loudest_customer": True}
    )
    assert prod_state.feedback_signal == 1.0
    assert prod_state.failure_mode_flagged is not None

    # Financial loop
    fin_state = coupler.evaluate_loop(
        BusinessLoopType.FINANCIAL,
        {"burn_multiple": 1.2, "runway_months": 24.0}
    )
    assert fin_state.feedback_signal == 1.0
    assert fin_state.kpis["burn_multiple"] == 1.2


def test_customer_journey_and_gtm_motions():
    """Verify customer journey bottleneck detection and GTM channel motion selection."""
    journey = CustomerJourneyEngine()
    bottlenecks = journey.evaluate_cohort_funnel({
        JourneyStage.AWARENESS: 0.50,
        JourneyStage.EVALUATION: 0.05,  # Bottleneck
        JourneyStage.ACTIVATION: 0.80,
    })
    assert len(bottlenecks) == 1
    assert "evaluation" in bottlenecks[0]

    gtm = GTMSystemEngine()
    motion_plg = gtm.determine_channel_motion(acv_cents=100_00, product_complexity=0.1)
    assert motion_plg == GTMMotion.PLG

    motion_ent = gtm.determine_channel_motion(acv_cents=100000_00, product_complexity=0.8)
    assert motion_ent == GTMMotion.ENTERPRISE


def test_growth_stage_classifier_and_premature_scaling():
    """Verify 9-stage company growth classification and premature scaling flags."""
    classifier = GrowthStageClassifier()

    info_startup = classifier.classify_stage(paying_customers=15, retention_curve_flattened=False, mrr_cents=5000_00, ecosystem_gmv_cents=0)
    assert info_startup["stage"] == CompanyGrowthStage.STARTUP
    assert info_startup["binding_constraint"] == "Cash runway"

    info_pmf = classifier.classify_stage(paying_customers=200, retention_curve_flattened=True, mrr_cents=150000_00, ecosystem_gmv_cents=0)
    assert info_pmf["stage"] == CompanyGrowthStage.GROWTH

    # Premature scaling check
    is_premature = classifier.detect_premature_scaling(
        current_stage=CompanyGrowthStage.STARTUP,
        marketing_spend_cents=100000_00,
        retention_flattened=False
    )
    assert is_premature is True


def test_strategic_moats_and_failure_modes():
    """Verify 7 Powers moat calculation and failure mode diagnosis."""
    strategic = StrategicThinkingEngine()
    moat_score = strategic.calculate_moat_score({
        MoatType.NETWORK_EFFECTS: 0.8,
        MoatType.SWITCHING_COSTS: 0.9,
        MoatType.COUNTER_POSITIONING: 0.7
    })
    assert 0.5 <= moat_score <= 1.0

    detector = FailureModeDetector()
    diagnoses = detector.diagnose_metrics(
        build_velocity_high=True,
        demand_signal_flat=True,
        retention_flattens=False,
        cac_rising_fast=True
    )
    assert len(diagnoses) >= 2
    types = [d.failure_type for d in diagnoses]
    assert FailureModeType.BUILDING_BEFORE_VALIDATING in types
    assert FailureModeType.LACK_OF_PMF in types


def test_state_machine_and_decision_tree():
    """Verify EOS State Machine transitions and Decision Tree outcomes."""
    sm = EOSStateMachine()
    assert sm.current_state == EOSState.SENSING

    # Sensing -> Hypothesis
    assert sm.transition(EOSState.HYPOTHESIS) is True
    assert sm.current_state == EOSState.HYPOTHESIS

    # Invalid transition (Hypothesis -> Scale directly)
    assert sm.transition(EOSState.SCALE) is False

    dt = EOSDecisionTree()
    res_pursue = dt.evaluate_opportunity(
        is_structural_anomaly=True,
        is_reversible_decision=True,
        high_confidence_signal=True,
        cheap_test_available=True,
        test_result_exceeds_kill_threshold=True,
        expected_value_positive=True,
        has_structural_advantage=True
    )
    assert res_pursue["decision"] == "pursue"

    res_discard = dt.evaluate_opportunity(
        is_structural_anomaly=False,
        is_reversible_decision=True,
        high_confidence_signal=True,
        cheap_test_available=True,
        test_result_exceeds_kill_threshold=True,
        expected_value_positive=True,
        has_structural_advantage=True
    )
    assert res_discard["decision"] == "discard"


def test_first_principles_eos_engine_e2e():
    """Verify complete end-to-end AI Operating System execution loop."""
    engine = FirstPrinciplesEOSEngine()

    signal = WeakSignal(
        signal_id="sig_ai_cost",
        description="LLM inference cost dropping by 10x",
        source="cost_curve_data",
        observed_value=0.001,
        expected_value=0.05
    )

    res = engine.execute_sensing_and_evaluation(
        signal=signal,
        enabling_condition="Inference cost < $0.005 / 1k tokens",
        test_cost_cents=1000_00,
        kill_metric="conversion",
        kill_value=0.05,
        acv_cents=200_00,
        product_complexity=0.2,
        active_moats={MoatType.NETWORK_EFFECTS: 0.6, MoatType.SWITCHING_COSTS: 0.5}
    )

    assert res["status"] == "pursuing"
    assert res["gtm_motion"] == GTMMotion.PLG
    assert res["moat_durability_score"] > 0.0
    assert res["current_state"] == EOSState.CHEAP_TEST.value
