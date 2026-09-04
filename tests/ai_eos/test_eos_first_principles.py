"""Unit and Integration Tests for First-Principles Entrepreneurial Operating System (EOS).

Verifies all components specified in ENTREPRENEURIAL_OPERATING_SYSTEM_SPEC.md:
- State Machine (12 states and transition rules)
- Opportunity Decision Tree (5-step decision checks)
- Coupled Business Loops Engine (13 feedback loops)
- Customer Lifecycle Engine (15 stages & bottlenecks)
- Growth Stage Classifier (9 stages & premature scaling)
- Moat Analyzer (6 dimensions & durability score)
- Failure Mode Monitor (10 operational failure modes)
- Master Orchestrator (End-to-end loop cycle & KPI stack)
"""

from __future__ import annotations
import pytest
from apodex.ai_eos.intelligence import (
    EOSState,
    EOSStateMachine,
    OpportunityDecisionTree,
    CoupledBusinessLoopsEngine,
    CustomerLifecycleEngine,
    GrowthStageClassifier,
    MoatAnalyzer,
    FailureModeMonitor,
    FirstPrinciplesEOSEngine,
)


def test_eos_state_machine_valid_transitions():
    """Verify standard state transitions along the happy path and kill signal branches."""
    sm = EOSStateMachine()
    assert sm.current_state == EOSState.SENSING

    # Happy path
    assert sm.transition_to(EOSState.HYPOTHESIS, "Anomaly detected") is True
    assert sm.transition_to(EOSState.CHEAP_TEST, "Hypothesis formed") is True
    assert sm.transition_to(EOSState.VALIDATION, "Cheap test strengthened hypothesis") is True
    assert sm.transition_to(EOSState.BUILD_GATE, "Economic viability confirmed") is True
    assert sm.transition_to(EOSState.MVP, "Resourced MVP build") is True
    assert sm.transition_to(EOSState.GTM_TEST, "MVP shipped to market") is True
    assert sm.transition_to(EOSState.KILL_OR_SCALE, "GTM signal collected") is True
    assert sm.transition_to(EOSState.SCALE, "Metrics exceed scale threshold") is True
    assert sm.transition_to(EOSState.OPERATE, "Repeatable loop confirmed") is True
    assert sm.transition_to(EOSState.REINVENT, "Market leadership reached; reinvention requisite") is True
    assert sm.transition_to(EOSState.SENSING, "Re-entering sensing cycle") is True

    # Audit history length
    assert len(sm.history) == 12


def test_eos_state_machine_kill_branches_and_invalid():
    """Verify kill/discard branches and invalid transition rejections."""
    sm = EOSStateMachine(initial_state=EOSState.CHEAP_TEST)
    assert sm.transition_to(EOSState.DISCARD, "Cheap test falsified hypothesis") is True
    assert sm.transition_to(EOSState.SENSING, "Resetting back to sensing") is True

    # Invalid transition (e.g. SENSING directly to SCALE)
    assert sm.can_transition_to(EOSState.SCALE) is False
    assert sm.transition_to(EOSState.SCALE, "Invalid jump") is False
    assert sm.current_state == EOSState.SENSING


def test_opportunity_decision_tree_pursue():
    """Verify opportunity decision tree evaluation for a valid opportunity."""
    dt = OpportunityDecisionTree()
    opp_valid = {
        "is_structural_anomaly": True,
        "is_reversible": True,
        "cheap_test_available": True,
        "test_result_exceeds_kill_threshold": True,
        "expected_value_positive": True,
        "has_structural_advantage": True,
    }
    res = dt.evaluate(opp_valid)
    assert res["decision"] == "pursue"
    assert res["failed_step"] is None


def test_opportunity_decision_tree_discards():
    """Verify opportunity decision tree discards for various failure points."""
    dt = OpportunityDecisionTree()

    # Non-structural noise
    res_noise = dt.evaluate({"is_structural_anomaly": False})
    assert res_noise["decision"] == "discard"
    assert res_noise["failed_step"] == "Q1_structural_anomaly"

    # Type I risk without multi-source high-confidence signal
    res_type1 = dt.evaluate({
        "is_structural_anomaly": True,
        "is_reversible": False,
        "high_confidence_multi_source_signal": False,
    })
    assert res_type1["decision"] == "discard"
    assert res_type1["failed_step"] == "Q2a_high_confidence_multi_source_signal"

    # Cheap test failed kill threshold
    res_failed_test = dt.evaluate({
        "is_structural_anomaly": True,
        "is_reversible": True,
        "cheap_test_available": True,
        "test_result_exceeds_kill_threshold": False,
    })
    assert res_failed_test["decision"] == "discard"
    assert res_failed_test["failed_step"] == "Q4_test_result_kill_threshold"

    # No structural advantage
    res_no_moat = dt.evaluate({
        "is_structural_anomaly": True,
        "is_reversible": True,
        "cheap_test_available": True,
        "test_result_exceeds_kill_threshold": True,
        "has_structural_advantage": False,
    })
    assert res_no_moat["decision"] == "discard"
    assert res_no_moat["failed_step"] == "Q5_structural_advantage"


def test_coupled_business_loops_evaluation():
    """Verify evaluation of the 13 coupled business loops."""
    engine = CoupledBusinessLoopsEngine()
    metrics = {
        "retention_curve_slope": -0.01,
        "nps": 50,
        "cac_cents": 120_00,
        "conversion_rate": 0.03,
        "win_rate": 0.30,
        "sales_cycle_days": 30,
        "nrr": 1.20,
        "churn_rate": 0.01,
        "share_of_voice": 0.20,
        "arpu_cents": 60_00,
        "viral_coefficient_k": 0.6,
        "decision_cycle_days": 3,
        "burn_multiple": 1.1,
        "runway_months": 24.0,
        "regretted_attrition_rate": 0.03,
        "enps": 55,
        "experiments_run_quarterly": 12,
        "experiment_hit_rate": 0.25,
        "feature_parity_gap": 0.05,
    }
    res = engine.evaluate_loops(metrics)
    assert res["health_score"] == 1.0
    assert len(res["failing_loops"]) == 0


def test_customer_lifecycle_engine_bottlenecks():
    """Verify customer journey bottleneck detection across 15 stages."""
    cle = CustomerLifecycleEngine()
    bad_lifecycle = {
        "time_to_first_value_hours": 72.0,      # > 48h bottleneck
        "activation_rate": 0.20,                 # < 30% bottleneck
        "retention_curve_flattened": False,      # unflattened bottleneck
        "nrr": 0.90,                              # shrinkage bottleneck
        "viral_coefficient_k": 0.1,
    }
    res = cle.evaluate_lifecycle(bad_lifecycle)
    assert res["healthy"] is False
    assert "onboarding_delay" in res["bottlenecks"]
    assert "activation_failure" in res["bottlenecks"]
    assert "unflattened_retention_curve" in res["bottlenecks"]
    assert "net_revenue_shrinkage" in res["bottlenecks"]


def test_growth_stage_classifier_and_premature_scaling():
    """Verify 9-stage company growth classification and premature scaling detection."""
    gsc = GrowthStageClassifier()

    # Healthy PMF stage
    res_pmf = gsc.classify_stage({
        "paying_customers": 100,
        "monthly_revenue_cents": 20_000_00,
        "retention_curve_flattened": True,
        "sales_marketing_spend_cents": 10_000_00,
    })
    assert res_pmf["current_stage"] == "pmf"
    assert res_pmf["premature_scaling_risk"] is False

    # Premature scaling warning: high marketing spend before retention flattens
    res_premature = gsc.classify_stage({
        "paying_customers": 20,
        "monthly_revenue_cents": 5_000_00,
        "retention_curve_flattened": False,
        "sales_marketing_spend_cents": 100_000_00,
    })
    assert res_premature["premature_scaling_risk"] is True


def test_moat_analyzer_durability_scoring():
    """Verify moat durability scoring across all 6 dimensions."""
    ma = MoatAnalyzer()
    res = ma.score_moats({
        "network_effects_density": 0.80,
        "switching_cost_score": 0.90,
        "cost_advantage_percent": 0.50,
        "brand_trust_score": 0.85,
        "regulatory_ip_protection_score": 0.70,
        "counter_positioning_score": 0.95,
    })
    durability = res["durability_score"]
    assert 0.70 <= durability <= 1.00
    assert len(res["dimensions"]) == 6


def test_failure_mode_monitor_diagnostics():
    """Verify detection of operating failure modes and correction mechanisms."""
    fmm = FailureModeMonitor()
    problematic_metrics = {
        "user_engagement_rate": 0.05,
        "survey_satisfaction": 0.90,            # Solving wrong problem
        "build_velocity_features_per_mo": 15,
        "demand_signal_growth": -0.05,          # Building before validating
        "disconfirming_evidence_ignored": True, # Founder bias
    }
    diagnostics = fmm.diagnose_failure_modes(problematic_metrics)
    assert len(diagnostics) == 3
    modes = [d["failure_mode"] for d in diagnostics]
    assert "solving_wrong_problem" in modes
    assert "building_before_validating" in modes
    assert "founder_bias" in modes


def test_first_principles_eos_engine_e2e_cycle():
    """Verify end-to-end master loop cycle execution in FirstPrinciplesEOSEngine."""
    engine = FirstPrinciplesEOSEngine()

    input_payload = {
        "opportunity": {
            "is_structural_anomaly": True,
            "is_reversible": True,
            "cheap_test_available": True,
            "test_result_exceeds_kill_threshold": True,
            "expected_value_positive": True,
            "has_structural_advantage": True,
        },
        "business_loop_metrics": {
            "retention_curve_slope": -0.01,
            "nps": 60,
            "cac_cents": 100_00,
            "conversion_rate": 0.04,
            "burn_multiple": 1.0,
            "runway_months": 24.0,
        },
        "customer_lifecycle_metrics": {
            "time_to_first_value_hours": 12.0,
            "activation_rate": 0.50,
            "retention_curve_flattened": True,
            "nrr": 1.25,
            "viral_coefficient_k": 0.7,
        },
        "venture_metrics": {
            "paying_customers": 150,
            "monthly_revenue_cents": 500_000_00,
            "retention_curve_flattened": True,
            "category_market_share": 0.15,
        },
        "moat_inputs": {
            "network_effects_density": 0.70,
            "switching_cost_score": 0.80,
            "brand_trust_score": 0.90,
        },
        "operating_metrics": {
            "user_engagement_rate": 0.60,
            "survey_satisfaction": 0.85,
        }
    }

    res = engine.run_master_loop_cycle(input_payload)

    assert res["current_state"] == "sensing"
    assert res["decision_tree_result"]["decision"] == "pursue"
    assert res["business_loops_result"]["health_score"] > 0.80
    assert res["customer_lifecycle_result"]["healthy"] is True
    assert res["growth_stage_result"]["current_stage"] == "growth"
    assert res["moat_result"]["durability_score"] > 0.40
    assert "kpi_stack" in res
    assert res["kpi_stack"]["sensing"]["signal_to_noise_ratio"] == 0.85
