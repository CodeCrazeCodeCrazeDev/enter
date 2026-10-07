"""Comprehensive unit, integration, and first-principles tests for the EOS Cognitive Engine.

Verifies system state machine, decision tree, coupled business loops, risk classification,
failure mode monitors, customer lifecycle stages, and company growth state transitions.
"""

from __future__ import annotations
import math
import pytest
from uuid import uuid4

from apodex.ai_eos.domain.models import VentureCell, Hypothesis, Evidence
from apodex.ai_eos.intelligence.eos_engine import (
    EOSState,
    CompanyStage,
    EntrepreneurialWorldModel,
    OpportunityGraph,
    EOSOpportunityDecisionTree,
    HypothesisEngine,
    ExternalBusinessLoopsEngine,
    CustomerLifecycleEngine,
    GTMSystemSimulator,
    CompanyGrowthStateMachine,
    StrategicMoatEngine,
    FailureModeMonitor,
    EOSEngine,
)


def test_world_model_and_anomaly_detection():
    """Verify stochastic transitions and structural anomaly detection (§2.1)."""
    wm = EntrepreneurialWorldModel()
    signals = [
        {"id": "sig_001", "name": "Normal Growth", "growth_rate": 0.06, "expected_growth_rate": 0.05},
        {"id": "sig_002", "name": "CUDA/AI Compute Surge", "growth_rate": 0.85, "expected_growth_rate": 0.05, "is_structural_shift": True},
    ]

    anomalies = wm.detect_anomalies(signals)
    assert len(anomalies) == 1
    assert anomalies[0]["signal_id"] == "sig_002"
    assert anomalies[0]["is_structural"] is True


def test_eos_opportunity_decision_tree():
    """Verify §10.2 Decision Tree logic: 'Should We Pursue This Opportunity?'"""
    dt = EOSOpportunityDecisionTree()

    # Noise signal -> Discard at Q1
    noise_op = {"is_structural_anomaly": False}
    res_q1 = dt.evaluate(noise_op)
    assert res_q1["pursue"] is False
    assert "Q1" in res_q1["reason"]

    # Irreversible, low multi-source confidence -> Discard at Q2a
    irreversible_op = {
        "is_structural_anomaly": True,
        "is_reversible": False,  # Type I
        "multi_source_confidence": 0.4
    }
    res_q2a = dt.evaluate(irreversible_op)
    assert res_q2a["pursue"] is False
    assert "Q2a" in res_q2a["reason"]

    # Cheap test failed -> Discard at Q4
    failed_test_op = {
        "is_structural_anomaly": True,
        "is_reversible": True,
        "cheap_test_available": True,
        "test_result_score": 0.2,
        "kill_threshold": 0.5
    }
    res_q4 = dt.evaluate(failed_test_op)
    assert res_q4["pursue"] is False
    assert "Q4" in res_q4["reason"]

    # Valid opportunity -> Commit resources
    valid_op = {
        "is_structural_anomaly": True,
        "is_reversible": True,
        "cheap_test_available": True,
        "test_result_score": 0.8,
        "kill_threshold": 0.5,
        "has_structural_advantage": True
    }
    res_valid = dt.evaluate(valid_op)
    assert res_valid["pursue"] is True


def test_hypothesis_risk_type_classification():
    """Verify Type I (irreversible) vs Type II (reversible) risk classification (§2.1)."""
    engine = HypothesisEngine()
    assert "Type II" in engine.classify_risk_type(is_reversible=True)
    assert "Type I" in engine.classify_risk_type(is_reversible=False)


def test_external_business_loops_13_coupled_systems():
    """Verify standard execution across all 13 external business loops (§3)."""
    ebl = ExternalBusinessLoopsEngine()

    prod = ebl.execute_product_loop(user_feedback_score=0.8, dev_velocity=1.0)
    assert prod["retention_delta"] > 0

    mkt = ebl.execute_marketing_loop(spend_cents=10000_00, positioning_clarity=0.8)
    assert mkt["acquired_leads"] > 0

    sales = ebl.execute_sales_loop(qualified_leads=mkt["acquired_leads"], sales_efficiency=0.9)
    assert sales["closed_deals"] > 0

    cs = ebl.execute_customer_success_loop(active_customers=sales["closed_deals"], onboarding_quality=0.85)
    assert cs["nrr"] > 1.0

    brand = ebl.execute_brand_loop(product_experience_score=0.9, marketing_reach=1000)
    assert brand["pricing_power_multiplier"] > 1.0

    pricing = ebl.execute_pricing_loop(value_delivered_cents=100_00, cost_basis_cents=10_00)
    assert pricing["gross_margin"] == 0.50

    ref = ebl.execute_referral_loop(satisfied_customers=100, viral_incentive_score=0.5)
    assert ref["new_referrals"] > 0

    data = ebl.execute_data_loop(total_interactions=500)
    assert data["latency_reduction"] > 0

    fin = ebl.execute_financial_loop(revenue_cents=20000_00, costs_cents=10000_00)
    assert fin["cash_balance_cents"] > 100_000_00

    hiring = ebl.execute_hiring_loop(open_roles=4, employer_brand_score=1.0)
    assert hiring["filled_roles"] == 4

    culture = ebl.execute_culture_loop(values_alignment_score=0.9)
    assert culture["enps"] == 90

    innov = ebl.execute_innovation_loop(rd_spend_cents=5000_00, experiments_count=10)
    assert innov["shipped_bets"] >= 1

    comp = ebl.execute_competitive_intel_loop(competitor_moves=["price_cut"], feature_parity_gap=0.85)
    assert comp["repositioning_required"] is False


def test_customer_lifecycle_stages():
    """Verify customer journey 15-stage conversion evaluation (§4)."""
    cle = CustomerLifecycleEngine()
    cohort_data = {"Activation": 0.45, "Retention": 0.12}

    act_eval = cle.evaluate_stage_conversion("Activation", cohort_data)
    assert act_eval["health"] == "healthy"

    ret_eval = cle.evaluate_stage_conversion("Retention", cohort_data)
    assert ret_eval["health"] == "bottleneck"


def test_gtm_system_simulator():
    """Verify GTM channel fit, pricing, and compounding motions (§5)."""
    simulator = GTMSystemSimulator()

    # Mismatched motion: High complexity with self-serve PLG
    mismatch = simulator.simulate_gtm_system(positioning_score=0.9, price_cents=50000_00, complexity="high", motion="PLG")
    assert mismatch["channel_fit"] is False

    # Aligned SLG enterprise motion
    aligned = simulator.simulate_gtm_system(positioning_score=0.85, price_cents=50000_00, complexity="high", motion="SLG")
    assert aligned["channel_fit"] is True
    assert aligned["compounding_motion_enabled"] is True


def test_company_growth_state_machine():
    """Verify company growth transitions across stages and constraint checks (§6)."""
    sm = CompanyGrowthStateMachine(CompanyStage.IDEA)

    # Validated learnings < 5 -> stay at Idea
    stage, msg = sm.transition_stage({"validated_learnings": 2})
    assert stage == CompanyStage.IDEA
    assert "Founder time" in msg

    # Validated learnings >= 5 -> promote to Validation
    stage, msg = sm.transition_stage({"validated_learnings": 6})
    assert stage == CompanyStage.VALIDATION

    # Paying customers >= 3 -> promote to Startup
    stage, msg = sm.transition_stage({"paying_customers": 4})
    assert stage == CompanyStage.STARTUP


def test_strategic_moats_and_capital_ranking():
    """Verify composite moat score and opportunity-cost initiative ranking (§7)."""
    sme = StrategicMoatEngine()

    moat_scores = {
        "network_effects": 0.8,
        "switching_costs": 0.7,
        "economies_of_scale": 0.9,
        "brand": 0.6,
        "regulatory_ip": 0.5,
        "counter_positioning": 0.8,
    }
    composite = sme.score_composite_moat(moat_scores)
    assert 0.70 <= composite <= 0.80

    initiatives = [
        {"name": "Init A", "expected_return_cents": 1000, "capital_required_cents": 100},  # ROI = 10
        {"name": "Init B", "expected_return_cents": 5000, "capital_required_cents": 100},  # ROI = 50
    ]
    ranked = sme.rank_opportunity_cost_initiatives(initiatives)
    assert ranked[0]["name"] == "Init B"


def test_failure_mode_monitor():
    """Verify detection of failure modes (building before validating, bottlenecks, premature scaling) (§8)."""
    fmm = FailureModeMonitor()

    metrics = {
        "high_build_velocity": True,
        "demand_signal": 0.05,  # low
        "decision_latency_seconds": 100000,  # > 1 day
        "cac_trend": 3.0,
        "ltv_trend": 1.0  # cac rising 3x ltv
    }

    warnings = fmm.audit_operating_metrics(metrics)
    assert len(warnings) == 3
    failure_types = {w["failure_mode"] for w in warnings}
    assert "building_before_validating" in failure_types
    assert "organizational_bottlenecks" in failure_types
    assert "scaling_prematurely" in failure_types


def test_eos_engine_system_state_machine():
    """Verify full state machine transitions across Section 10.1 System State Machine."""
    engine = EOSEngine()
    assert engine.current_state == EOSState.SENSING

    assert engine.transition_system_state("anomaly_detected", {}) == EOSState.HYPOTHESIS
    assert engine.transition_system_state("hypothesis_formed", {}) == EOSState.CHEAP_TEST
    assert engine.transition_system_state("strengthened", {}) == EOSState.VALIDATION
    assert engine.transition_system_state("economic_viability_confirmed", {}) == EOSState.BUILD_GATE
    assert engine.transition_system_state("resourced", {}) == EOSState.MVP
    assert engine.transition_system_state("shipped", {}) == EOSState.GTM_TEST
    assert engine.transition_system_state("signal_collected", {}) == EOSState.KILL_OR_SCALE
    assert engine.transition_system_state("above_threshold", {}) == EOSState.SCALE
    assert engine.transition_system_state("repeatable_loop_confirmed", {}) == EOSState.OPERATE
    assert engine.transition_system_state("market_maturity", {}) == EOSState.REINVENT
    assert engine.transition_system_state("loop_reset", {}) == EOSState.SENSING
