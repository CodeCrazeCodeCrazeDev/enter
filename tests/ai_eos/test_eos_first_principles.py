"""
Tests for the First-Principles Entrepreneurial Operating System (EOS) Engine.
"""

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


def test_eos_state_machine_valid_flow():
    sm = EOSStateMachine()
    assert sm.current_state == EOSState.SENSING

    # Sensing -> Hypothesis
    sm.transition(EOSState.HYPOTHESIS, reason="Anomaly detected")
    assert sm.current_state == EOSState.HYPOTHESIS

    # Hypothesis -> CheapTest
    sm.transition(EOSState.CHEAP_TEST, reason="Hypothesis formed")
    assert sm.current_state == EOSState.CHEAP_TEST

    # CheapTest -> Validation
    sm.transition(EOSState.VALIDATION, reason="Cheap test strengthened")
    assert sm.current_state == EOSState.VALIDATION

    # Validation -> BuildGate
    sm.transition(EOSState.BUILD_GATE, reason="Viability confirmed")
    assert sm.current_state == EOSState.BUILD_GATE

    # BuildGate -> MVP
    sm.transition(EOSState.MVP, reason="Resourced")
    assert sm.current_state == EOSState.MVP

    # MVP -> GTMTest
    sm.transition(EOSState.GTM_TEST, reason="Shipped")
    assert sm.current_state == EOSState.GTM_TEST

    # GTMTest -> KillOrScale
    sm.transition(EOSState.KILL_OR_SCALE, reason="Signal collected")
    assert sm.current_state == EOSState.KILL_OR_SCALE

    # KillOrScale -> Scale
    sm.transition(EOSState.SCALE, reason="Above threshold")
    assert sm.current_state == EOSState.SCALE

    # Scale -> Operate
    sm.transition(EOSState.OPERATE, reason="Loop confirmed")
    assert sm.current_state == EOSState.OPERATE

    # Operate -> Reinvent
    sm.transition(EOSState.REINVENT, reason="Market maturity")
    assert sm.current_state == EOSState.REINVENT

    # Reinvent -> Sensing
    sm.transition(EOSState.SENSING, reason="Loop reset")
    assert sm.current_state == EOSState.SENSING
    assert len(sm.history) == 11


def test_eos_state_machine_falsification_and_reset():
    sm = EOSStateMachine()
    sm.transition(EOSState.HYPOTHESIS)
    sm.transition(EOSState.CHEAP_TEST)
    sm.transition(EOSState.DISCARD, reason="Falsified")
    assert sm.current_state == EOSState.DISCARD

    sm.reset_to_sensing(reason="Re-entering sensing")
    assert sm.current_state == EOSState.SENSING


def test_eos_state_machine_invalid_transition():
    sm = EOSStateMachine()
    with pytest.raises(ValueError) as excinfo:
        sm.transition(EOSState.SCALE, reason="Invalid leap")
    assert "Invalid transition from sensing to scale" in str(excinfo.value)


def test_opportunity_decision_tree_noise_discard():
    tree = OpportunityDecisionTree()
    res = tree.evaluate({"is_structural_anomaly": False})
    assert res["pursue"] is False
    assert "Noise detected" in res["decision_path"][0]


def test_opportunity_decision_tree_irreversible_without_confidence():
    tree = OpportunityDecisionTree()
    res = tree.evaluate({
        "is_structural_anomaly": True,
        "is_reversible_decision": False,  # Type I
        "high_confidence_multi_source": False
    })
    assert res["pursue"] is False
    assert "Insufficient high-confidence multi-source signal" in res["decision_path"][-1]


def test_opportunity_decision_tree_cheap_test_failed():
    tree = OpportunityDecisionTree()
    res = tree.evaluate({
        "is_structural_anomaly": True,
        "is_reversible_decision": True,
        "cheap_test_available": True,
        "test_result_exceeds_kill_threshold": False
    })
    assert res["pursue"] is False
    assert "Cheap test failed kill threshold" in res["decision_path"][-1]


def test_opportunity_decision_tree_pursue_success():
    tree = OpportunityDecisionTree()
    res = tree.evaluate({
        "is_structural_anomaly": True,
        "is_reversible_decision": True,
        "cheap_test_available": True,
        "test_result_exceeds_kill_threshold": True,
        "structural_advantage_exists": True
    })
    assert res["pursue"] is True
    assert "Commit resources" in res["recommendation"]


def test_coupled_business_loops_engine():
    engine = CoupledBusinessLoopsEngine()
    stocks = {"cash": 500000.0, "talent": 15.0, "trust": 0.85, "data": 80.0}
    flows = {"revenue": 50000.0, "hiring_rate": 2.0, "churn_rate": 0.03, "burn_rate": 25000.0}
    signals = {
        "pricing": {"arpu": 150.0},
        "hiring": {"quality_score": 0.9},
        "financial": {"burn_multiple": 1.2}
    }

    res = engine.evaluate_system_dynamics(stocks, flows, signals)
    assert res["financial_runway_months"] == 20.0
    assert res["burn_multiple"] == 1.2
    assert "pricing_to_financial" in res["leverage_points"]
    assert len(res["loop_health"]) == 13


def test_customer_lifecycle_engine():
    engine = CustomerLifecycleEngine()
    conversions = {
        "awareness": 0.8,
        "interest": 0.6,
        "consideration": 0.4,
        "evaluation": 0.15,  # Bottleneck < 0.2
        "purchase": 0.5,
        "activation": 0.65,
        "retention": 0.45,
        "expansion": 1.25,
        "referral": 0.35
    }

    res = engine.evaluate_lifecycle(conversions)
    assert res["primary_bottleneck_stage"] == "evaluation"
    assert res["activation_rate"] == 0.65
    assert res["net_revenue_retention"] == 1.25
    assert res["retention_flattened"] is True


def test_growth_stage_classifier():
    classifier = GrowthStageClassifier()

    # PMF stage test
    metrics_pmf = {
        "arr_cents": 50000000,  # $500k
        "retention_curve_flattened": True,
        "paying_customers": 50,
        "cac_payback_months": 8.0
    }
    res_pmf = classifier.classify(metrics_pmf)
    assert res_pmf["current_stage"] == "pmf"
    assert res_pmf["premature_scaling_alert"] is False

    # Premature scaling alert test
    metrics_premature = {
        "arr_cents": 1000000,
        "retention_curve_flattened": False,
        "paying_customers": 5,
        "monthly_marketing_spend": 100000  # High spend without retention
    }
    res_prem = classifier.classify(metrics_premature)
    assert res_prem["current_stage"] == "startup"
    assert res_prem["premature_scaling_alert"] is True


def test_moat_analyzer():
    analyzer = MoatAnalyzer()
    scores = {
        "network_effects": 0.8,
        "switching_costs": 0.7,
        "counter_positioning": 0.6,
        "economies_of_scale": 0.4,
        "brand": 0.5,
        "regulatory_ip": 0.1  # Vulnerability
    }

    res = analyzer.analyze(scores)
    assert res["has_defensible_moat"] is True
    assert res["dominant_moat"] == "network_effects"
    assert "regulatory_ip" in res["vulnerabilities"]


def test_failure_mode_monitor():
    monitor = FailureModeMonitor()

    metrics = {
        "feature_ship_velocity": 15,
        "demand_growth_rate": 0.0,  # Trigger building before validating
        "decision_latency_days": 20,  # Trigger org bottlenecks
        "disconfirming_data_ignored_count": 3  # Trigger founder bias
    }

    alerts = monitor.diagnose(metrics)
    triggered_modes = [a["failure_mode"] for a in alerts]

    assert "building_before_validating" in triggered_modes
    assert "organizational_bottlenecks" in triggered_modes
    assert "founder_bias" in triggered_modes


def test_first_principles_eos_engine_e2e():
    engine = FirstPrinciplesEOSEngine()

    # Process opportunity signal
    opp = {
        "is_structural_anomaly": True,
        "is_reversible_decision": True,
        "cheap_test_available": True,
        "test_result_exceeds_kill_threshold": True,
        "structural_advantage_exists": True
    }

    proc_res = engine.process_opportunity(opp)
    assert proc_res["current_state"] == EOSState.VALIDATION.value
    assert proc_res["opportunity_decision"]["pursue"] is True

    # Diagnostic run
    system_metrics = {
        "stocks": {"cash": 1000000.0, "talent": 20.0, "trust": 0.9, "data": 90.0},
        "flows": {"revenue": 100000.0, "hiring_rate": 3.0, "churn_rate": 0.02, "burn_rate": 50000.0},
        "loop_signals": {"pricing": {"arpu": 200.0}},
        "stage_conversions": {"activation": 0.7, "expansion": 1.3, "retention": 0.5},
        "venture_metrics": {"arr_cents": 120000000, "retention_curve_flattened": True, "paying_customers": 120},
        "moat_scores": {
            "network_effects": 0.9,
            "switching_costs": 0.8,
            "counter_positioning": 0.7,
            "brand": 0.6
        }
    }

    diag_res = engine.run_full_diagnostic(system_metrics)
    assert diag_res["system_state"] == EOSState.VALIDATION.value
    assert diag_res["growth_stage"]["current_stage"] == "growth"
    assert diag_res["moat_analysis"]["has_defensible_moat"] is True
    assert diag_res["is_system_healthy"] is True
