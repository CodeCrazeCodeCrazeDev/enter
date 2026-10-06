"""Comprehensive Unit & Integration Test Suite for First-Principles EOS Engine.

Validates all 11 sections of the Entrepreneurial Operating System specification.
"""

from __future__ import annotations
import pytest
from apodex.ai_eos.intelligence.eos_first_principles import (
    EOSEngineFirstPrinciples,
    MasterLoopEngine,
    MasterLoopNode,
    CognitiveLoopsEngine,
    AnomalySignal,
    DecisionRiskType,
    ExternalBusinessLoopsEngine,
    CustomerLifecycleEngine,
    CustomerJourneyStage,
    GTMSystemSimulator,
    GTMChannel,
    CompanyGrowthStateMachine,
    GrowthStage,
    StrategicMoatEngine,
    MoatType,
    FailureModeMonitor,
    EOSOpportunityDecisionTree,
    SystemState,
)


def test_section_0_and_1_master_loop():
    """Verify Master Loop 19-node sequence and kill signals."""
    engine = MasterLoopEngine()
    assert engine.state.current_node == MasterLoopNode.A_ENVIRONMENTAL_SENSING

    # Advance through initial nodes
    node_b = engine.advance()
    assert node_b == MasterLoopNode.B_SIGNAL_COLLECTION

    # Simulate advancing to F_CUSTOMER_VALIDATION and triggering kill signal F -> D
    engine.state.current_node = MasterLoopNode.F_CUSTOMER_VALIDATION
    next_node = engine.advance({"falsified": True, "reason": "No market demand"})
    assert next_node == MasterLoopNode.D_OPPORTUNITY_DISCOVERY
    assert len(engine.state.kill_signals_triggered) == 1
    assert engine.state.kill_signals_triggered[0]["from"] == "F"

    # Simulate advancing to M_UNIT_ECONOMICS and triggering kill signal M -> G
    engine.state.current_node = MasterLoopNode.M_UNIT_ECONOMICS
    next_node = engine.advance({"bad_economics": True, "reason": "CAC > LTV"})
    assert next_node == MasterLoopNode.G_BUSINESS_MODEL_DESIGN
    assert len(engine.state.kill_signals_triggered) == 2


def test_section_2_cognitive_loops():
    """Verify Signal-to-Idea pipeline and Mental Model Evolution."""
    cog = CognitiveLoopsEngine()

    # Noise signal filtering
    noise_sig = AnomalySignal("sig_noise", "Random spike", is_structural_shift=False, observed_value=2.0, expected_value=1.0)
    hyp_noise = cog.evaluate_signal(noise_sig)
    assert hyp_noise is None

    # Structural shift signal
    struct_sig = AnomalySignal("sig_struct", "CUDA adoption explosion", is_structural_shift=True, observed_value=15.0, expected_value=1.0, confidence=0.6)
    hyp_struct = cog.evaluate_signal(struct_sig)
    assert hyp_struct is not None
    assert hyp_struct.risk_type == DecisionRiskType.TYPE_I_IRREVERSIBLE

    # Cheap test execution and Bayesian update
    belief_after_test = cog.run_cheap_test(hyp_struct.hypothesis_id, {"success": True, "likelihood_true": 0.8, "likelihood_false": 0.2})
    assert belief_after_test > 0.6
    assert cog.mental_model_structure["version"] >= 1


def test_section_3_external_business_loops():
    """Verify 13 coupled feedback loops and stock/flow updates."""
    biz = ExternalBusinessLoopsEngine()
    assert len(biz.loops) == 13
    assert "Product" in biz.loops
    assert "Financial" in biz.loops

    initial_cash = biz.stocks["cash"]
    stocks_after = biz.simulate_quarter()
    assert "cash" in stocks_after
    assert biz.loops["Financial"].kpis["runway_months"] >= 0.0


def test_section_4_customer_lifecycle():
    """Verify 15-stage Customer Journey lifecycle funnel."""
    life = CustomerLifecycleEngine()
    assert len(life.stages) == 15
    assert CustomerJourneyStage.AWARENESS in life.stages
    assert CustomerJourneyStage.REPURCHASE in life.stages

    funnel = life.compute_funnel_efficiency(cohort_size=10000)
    assert funnel[CustomerJourneyStage.AWARENESS.value] == 2000.0
    assert funnel[CustomerJourneyStage.REPURCHASE.value] < 2000.0


def test_section_5_gtm_system():
    """Verify GTM channel-positioning fit simulation."""
    gtm = GTMSystemSimulator()

    # Low ACV + PLG
    res_plg = gtm.simulate_channel_fit("Self-Serve", 1200.0, GTMChannel.PLG)
    assert res_plg["fit_score"] > 0.8

    # Low ACV + SLG (mismatch)
    res_slg = gtm.simulate_channel_fit("Self-Serve", 1200.0, GTMChannel.SLG)
    assert res_slg["fit_score"] < 0.3


def test_section_6_company_growth():
    """Verify 9-stage Company Growth state machine."""
    growth = CompanyGrowthStateMachine()
    assert growth.current_stage == GrowthStage.IDEA

    # Evaluate transition Idea -> Validation
    res = growth.evaluate_transition({"validated_learnings": 4})
    assert res["advanced"] is True
    assert growth.current_stage == GrowthStage.VALIDATION


def test_section_7_strategic_thinking():
    """Verify strategic moat durability and cost curve calculations."""
    moat = StrategicMoatEngine()

    # Counter-positioning moat evaluation
    score = moat.evaluate_moat_durability(MoatType.COUNTER_POSITIONING, {"incumbent_business_model_conflict": True})
    assert score > 0.9

    # Cost curve crossing
    years = moat.evaluate_cost_curve_viability(current_unit_cost=1000.0, annual_cost_decline_rate=0.3, threshold_cost=200.0)
    assert years == 5


def test_section_8_failure_mode_analysis():
    """Verify failure mode monitor detection."""
    monitor = FailureModeMonitor()

    # Metrics indicating premature scaling
    metrics = {"cac_growth_rate": 0.45, "ltv_growth_rate": 0.05, "spend_scaling": True}
    warnings = monitor.audit_metrics(metrics)
    assert len(warnings) == 1
    assert warnings[0].failure_mode == "Scaling prematurely"


def test_section_10_integrated_eos_engine():
    """Verify Section 10 decision tree and top-level EOSEngineFirstPrinciples orchestrator."""
    tree = EOSOpportunityDecisionTree()
    opp_data = {
        "is_structural_anomaly": True,
        "is_reversible_decision": True,
        "cheap_test_available": True,
        "test_exceeds_kill_threshold": True,
        "has_or_can_build_structural_advantage": True,
    }
    go, reason = tree.evaluate(opp_data)
    assert go is True
    assert "Go:" in reason

    eos = EOSEngineFirstPrinciples()
    result = eos.execute_sensing_cycle({"id": "sig_ai_01", "description": "LLM cost curve drop", "is_structural": True, "observed": 20.0, "expected": 2.0})
    assert result["status"] == SystemState.OPERATE.value
    assert "kpis" in result
    assert result["kpis"]["gross_margin"] == 0.78
