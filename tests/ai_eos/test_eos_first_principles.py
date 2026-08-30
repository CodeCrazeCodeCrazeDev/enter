"""Unit and Integration Tests for First-Principles EOS Engine."""

import pytest
from apodex.ai_eos.intelligence.eos_first_principles import (
    EOSState,
    EOSStateMachine,
    OpportunityInput,
    DecisionResult,
    OpportunityDecisionTree,
    CustomerLifecycleStage,
    LifecycleMetrics,
    CustomerLifecycleEngine,
    GTMChannel,
    GTMMotionConfig,
    GTMSystemSimulator,
    CompanyGrowthStage,
    CompanyGrowthStageClassifier,
    MoatType,
    StrategicMoatAnalyzer,
    FailureModeMonitor,
    MasterEOSOrchestrator,
)


def test_eos_state_machine_valid_transitions():
    sm = EOSStateMachine()
    assert sm.current_state == EOSState.SENSING

    # Transition to Hypothesis
    assert sm.transition_to(EOSState.HYPOTHESIS, "Anomaly detected") is True
    assert sm.current_state == EOSState.HYPOTHESIS

    # Transition to CheapTest
    assert sm.transition_to(EOSState.CHEAP_TEST, "Hypothesis formed") is True
    assert sm.current_state == EOSState.CHEAP_TEST

    # Invalid transition directly to Operate
    assert sm.transition_to(EOSState.OPERATE, "Invalid jump") is False
    assert sm.current_state == EOSState.CHEAP_TEST

    # Discard transition
    assert sm.transition_to(EOSState.DISCARD, "Falsified") is True
    assert sm.current_state == EOSState.DISCARD

    # Re-entry back to Sensing from Discard
    assert sm.transition_to(EOSState.SENSING, "Restart sensing") is True
    assert sm.current_state == EOSState.SENSING


def test_opportunity_decision_tree_noise_discard():
    tree = OpportunityDecisionTree()
    opp = OpportunityInput(
        opportunity_id="opp_noise",
        is_structural_anomaly=False,
        is_reversible=True,
    )
    result = tree.evaluate(opp)
    assert result.decision == "DISCARD"
    assert "Q1: Noise -> Discard" in result.path


def test_opportunity_decision_tree_irreversible_low_confidence():
    tree = OpportunityDecisionTree()
    opp = OpportunityInput(
        opportunity_id="opp_type1_low_conf",
        is_structural_anomaly=True,
        is_reversible=False,  # Irreversible
        multiple_source_confidence=0.4,  # Low confidence (<0.7)
    )
    result = tree.evaluate(opp)
    assert result.decision == "DISCARD"
    assert "Q2a: Low confidence -> Discard" in result.path


def test_opportunity_decision_tree_reversible_commit():
    tree = OpportunityDecisionTree()
    opp = OpportunityInput(
        opportunity_id="opp_type2_commit",
        is_structural_anomaly=True,
        is_reversible=True,
        cheap_test_available=True,
        test_result_exceeds_kill_threshold=True,
        has_structural_advantage=True,
        market_size_5_10_yr_large=True,
    )
    result = tree.evaluate(opp)
    assert result.decision == "COMMIT"
    assert "Q5: Structural advantage confirmed" in result.path


def test_customer_lifecycle_engine_analysis():
    engine = CustomerLifecycleEngine()
    metrics = LifecycleMetrics(
        time_to_first_value_days=10.0,  # Bottleneck
        activation_rate=0.20,            # Bottleneck
        dau_mau_ratio=0.30,
        cohort_retention_flattening=False, # Bottleneck
        net_revenue_retention_nrr=1.10,
    )
    analysis = engine.analyze_lifecycle(metrics)
    assert analysis["total_stages_tracked"] == 15
    assert len(analysis["bottlenecks"]) == 3
    assert analysis["overall_health"] == "CRITICAL"


def test_gtm_system_simulator_mismatch():
    sim = GTMSystemSimulator()

    # SLG for low complexity low ACV
    bad_cfg = GTMMotionConfig(
        positioning="Low end self serve tool",
        target_segment="SMB",
        pricing_model="self_serve",
        primary_channel=GTMChannel.SLG,
        product_complexity="low",
        contract_value_acv=2000.0,
    )
    res = sim.evaluate_fit(bad_cfg)
    assert res["is_viable"] is False
    assert len(res["mismatches"]) >= 2
    assert res["fit_score"] < 0.5

    # PLG fit
    good_cfg = GTMMotionConfig(
        positioning="Developer self-serve API",
        target_segment="Developers",
        pricing_model="usage",
        primary_channel=GTMChannel.PLG,
        product_complexity="low",
        contract_value_acv=5000.0,
    )
    res_good = sim.evaluate_fit(good_cfg)
    assert res_good["is_viable"] is True
    assert res_good["fit_score"] == 1.0


def test_company_growth_stage_classifier():
    classifier = CompanyGrowthStageClassifier()

    # Idea stage
    res_idea = classifier.classify_stage({"arr": 0, "paying_customers": 0})
    assert res_idea["current_stage"] == CompanyGrowthStage.IDEA.value

    # PMF stage
    res_pmf = classifier.classify_stage({"arr": 200000, "paying_customers": 15, "retention_flattened": True})
    assert res_pmf["current_stage"] == CompanyGrowthStage.PMF.value

    # Premature scaling risk
    res_premature = classifier.classify_stage({"arr": 2000000, "retention_flattened": False})
    assert res_premature["current_stage"] == CompanyGrowthStage.GROWTH.value
    assert res_premature["premature_scaling_risk"] is True


def test_strategic_moat_analyzer():
    analyzer = StrategicMoatAnalyzer()
    moats = {
        MoatType.NETWORK_EFFECTS: 0.9,
        MoatType.SWITCHING_COSTS: 0.8,
        MoatType.COUNTER_POSITIONING: 0.7,
    }
    analysis = analyzer.analyze_moats(moats)
    assert analysis["durability_rating"] == "STRONG"
    assert analysis["durability_score"] > 0.5
    assert "Network Effects" in analysis["strongest_moats"]


def test_failure_mode_monitor():
    monitor = FailureModeMonitor()
    metrics = {
        "survey_satisfaction": 0.9,
        "daily_engagement": 0.05,
        "decision_latency_days": 20,
    }
    detected = monitor.audit_operating_metrics(metrics)
    assert len(detected) == 2
    failure_names = [d["failure_mode"] for d in detected]
    assert "Solving the wrong problem" in failure_names
    assert "Organizational bottlenecks" in failure_names


def test_master_eos_orchestrator():
    orchestrator = MasterEOSOrchestrator()
    opp = OpportunityInput(
        opportunity_id="opp_e2e",
        is_structural_anomaly=True,
        is_reversible=True,
        cheap_test_available=True,
        test_result_exceeds_kill_threshold=True,
        has_structural_advantage=True,
        market_size_5_10_yr_large=True,
    )
    result = orchestrator.process_opportunity(opp)
    assert result.decision == "COMMIT"
    assert orchestrator.state_machine.current_state == EOSState.HYPOTHESIS

    kpi_stack = orchestrator.get_kpi_stack({
        "arr": 1500000,
        "retention_flattened": True,
        "paying_customers": 50,
        "moat_scores": {MoatType.NETWORK_EFFECTS: 0.8, MoatType.SWITCHING_COSTS: 0.7},
    })
    assert kpi_stack["system_state"] == EOSState.HYPOTHESIS.value
    assert kpi_stack["strategic_kpis"]["growth_stage"] == CompanyGrowthStage.GROWTH.value
    assert kpi_stack["diagnostics"]["lifecycle_health"] == "HEALTHY"
