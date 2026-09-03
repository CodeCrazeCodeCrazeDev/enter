"""
Unit and integration tests for the Entrepreneurial Operating System (EOS)
First-Principles Engine (§0 - §11).
"""

import pytest
from uuid import uuid4
from apodex.ai_eos.intelligence import (
    EOSState,
    EOSStateMachine,
    DecisionRiskType,
    WeakSignal,
    FalsifiableHypothesis,
    MentalModelEvaluator,
    BusinessLoopName,
    BusinessLoopState,
    ExternalBusinessLoopsEngine,
    JourneyStage,
    CustomerLifecycleEngine,
    GrowthStage,
    GrowthStageClassifier,
    GTMSystemEngine,
    OpportunityDecisionTree,
    FailureModeMonitor,
    FirstPrinciplesEOSEngine,
)


def test_eos_state_machine_valid_and_invalid_transitions():
    sm = EOSStateMachine()
    assert sm.current_state == EOSState.SENSING

    # Sensing -> Hypothesis is valid
    assert sm.transition_to(EOSState.HYPOTHESIS, reason="Anomaly detected")
    assert sm.current_state == EOSState.HYPOTHESIS

    # Hypothesis -> Scale is INVALID
    assert not sm.can_transition(EOSState.SCALE)
    assert not sm.transition_to(EOSState.SCALE, reason="Invalid jump")
    assert sm.current_state == EOSState.HYPOTHESIS

    # Hypothesis -> CheapTest is valid
    assert sm.transition_to(EOSState.CHEAP_TEST, reason="Cheap test designed")
    assert sm.current_state == EOSState.CHEAP_TEST


def test_signal_pipeline_and_falsifiable_hypothesis():
    signal = WeakSignal(
        description="Genomic sequencing cost dropping 10x below Moore's Law",
        is_structural_shift=True,
        source="Cost curve analysis",
        confidence=0.85
    )
    engine = FirstPrinciplesEOSEngine()
    res = engine.process_signal(signal)

    assert res["status"] == "hypothesis_formed"
    assert len(engine.active_hypotheses) == 1
    assert engine.state_machine.current_state == EOSState.HYPOTHESIS


def test_mental_model_evaluator_updating():
    mm = MentalModelEvaluator(
        structure_name="SaaS Distribution Assumptions",
        parameters={"sensitivity": 1.0},
        structural_assumptions=["Search SEO yields linear CAC"]
    )
    pred = mm.predict_outcome(2.0)
    assert pred == 2.0

    # Contradicting market feedback -> update parameters
    mm.update_parameters(actual_outcome=5.0, predicted_outcome=2.0)
    assert mm.parameters["sensitivity"] > 1.0
    assert mm.falsification_events == 1

    # Multiple severe contradictions force structural reinvention
    mm.update_parameters(actual_outcome=10.0, predicted_outcome=2.0)
    mm.update_parameters(actual_outcome=12.0, predicted_outcome=2.0)
    assert mm.requires_structural_reinvention()


def test_external_business_loops_health_and_coupling():
    loops_engine = ExternalBusinessLoopsEngine()
    assert len(loops_engine.loops) == 13

    # Check pricing and financial loop coupling
    pricing_loop = loops_engine.loops[BusinessLoopName.PRICING]
    financial_loop = loops_engine.loops[BusinessLoopName.FINANCIAL]

    assert pricing_loop.core_kpis["arpu"] == 500.0
    assert financial_loop.core_kpis["burn_multiple"] == 1.2

    health = loops_engine.evaluate_system_health()
    assert "system_leverage_score" in health
    assert health["total_loops_tracked"] == 13


def test_customer_lifecycle_funnel_bottlenecks():
    lifecycle = CustomerLifecycleEngine()
    assert len(lifecycle.stages) == 15

    # Modify a stage to simulate a bottleneck
    lifecycle.stages[JourneyStage.AWARENESS].conversion_rate = 0.10

    analysis = lifecycle.analyze_funnel_bottlenecks()
    assert analysis["count"] >= 1
    bottleneck_stages = [b["stage"] for b in analysis["bottlenecks"]]
    assert JourneyStage.AWARENESS.value in bottleneck_stages


def test_gtm_engine_channel_selection():
    gtm = GTMSystemEngine()

    # Low complexity + low price -> PLG
    ch1 = gtm.select_optimal_channel(product_complexity=0.1, price_level_usd=200)
    assert "Product-Led" in ch1

    # High complexity + high price -> Enterprise SLG
    ch2 = gtm.select_optimal_channel(product_complexity=0.9, price_level_usd=50000)
    assert "Sales-Led" in ch2


def test_growth_stage_classifier():
    classifier = GrowthStageClassifier()

    # Pre-revenue -> Startup / Validation
    stage1 = classifier.classify_current_stage({"paying_customers": 0, "validated_learnings": 5})
    assert stage1.stage == GrowthStage.VALIDATION

    # Retention flattened + $2M ARR -> Growth
    stage2 = classifier.classify_current_stage({"paying_customers": 50, "retention_flattened": 1.0, "arr_usd": 2_000_000})
    assert stage2.stage == GrowthStage.GROWTH


def test_opportunity_decision_tree_flowchart():
    dt = OpportunityDecisionTree()

    # Discard if noise
    res1 = dt.evaluate(is_structural_anomaly=False, is_reversible_decision=True)
    assert res1["decision"] == "Discard"

    # Type I irreversible decision without high confidence -> Discard
    res2 = dt.evaluate(is_structural_anomaly=True, is_reversible_decision=False, high_confidence_multi_source_signal=False)
    assert res2["decision"] == "Discard"

    # Full green path -> Commit Resources
    res3 = dt.evaluate(
        is_structural_anomaly=True,
        is_reversible_decision=True,
        cheap_test_available=True,
        cheap_test_exceeds_kill_threshold=True,
        has_structural_advantage=True
    )
    assert res3["decision"] == "Commit Resources"


def test_failure_mode_monitor_alerts():
    monitor = FailureModeMonitor()

    # Simulating metric flags
    metrics = {
        "retention_curve_slope": -0.15,      # Lack of PMF
        "cac_to_ltv_growth_ratio": 2.2,       # Premature scaling
        "decision_latency_days": 10.0         # Org bottlenecks
    }
    alerts = monitor.audit_metrics(metrics)
    assert len(alerts) == 3
    alert_modes = [a["mode"] for a in alerts]
    assert "Lack of product-market fit" in alert_modes
    assert "Scaling prematurely" in alert_modes
    assert "Organizational bottlenecks" in alert_modes


def test_master_first_principles_eos_engine_integration():
    engine = FirstPrinciplesEOSEngine()

    # 1. Ingest Weak Signal
    sig = WeakSignal(
        description="Bandwidth cost curve threshold enables video streaming",
        is_structural_shift=True,
        source="Infrastructure report"
    )
    sig_res = engine.process_signal(sig)
    assert sig_res["status"] == "hypothesis_formed"
    hyp = sig_res["hypothesis"]

    # 2. Evaluate Opportunity
    eval_res = engine.evaluate_opportunity(
        hypothesis=hyp,
        is_reversible=True,
        test_result=0.85,
        has_moat=True
    )
    assert eval_res["decision"] == "Commit Resources"
    assert engine.state_machine.current_state == EOSState.MVP

    # 3. KPI Stack Rollup
    kpi_stack = engine.run_kpi_stack()
    assert kpi_stack["current_state"] == EOSState.MVP.value
    assert "system_leverage_score" in kpi_stack
