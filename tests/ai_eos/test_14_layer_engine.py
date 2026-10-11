"""
test_14_layer_engine.py: Unit tests for FourteenLayerEngine and sub-components.
"""

import pytest
from apodex.ai_eos.intelligence.fourteen_layer_engine import (
    FourteenLayerEngine,
    RealitySubstrate,
    OpportunitySignal,
    OpportunityGraphEngine,
    StructuralCausalEngine,
    ActiveInferencePlannerEngine,
    CapitalAllocationAndPortfolioEngine,
    CompetitiveIntelligenceAndMoatEngine,
    FailureAndReinventionEngine,
    EntrepreneurialMemoryAndGovernanceEngine,
)


def test_reality_substrate():
    reality = RealitySubstrate()
    env = reality.sense_environment()
    assert "environment_entropy" in env
    assert env["gdp_growth"] == 0.02


def test_opportunity_graph_engine():
    graph = OpportunityGraphEngine()
    sig = OpportunitySignal(
        title="AI Venture Opportunity",
        domain="ai",
        keywords=["ai", "causal", "active_inference"],
        tam_cents=1000000
    )
    node_id = graph.add_opportunity_signal(sig)
    assert node_id is not None
    matches = graph.match_similar(["ai", "causal"])
    assert len(matches) == 1
    assert matches[0][0] == node_id


def test_structural_causal_engine():
    causal = StructuralCausalEngine()
    causal.add_causal_edge("marketing", "revenue", 0.8)
    res = causal.do_intervention("marketing", 2.0)
    assert res["revenue"] == 1.6

    cf = causal.simulate_counterfactual(
        factual_obs={"marketing": 1.0, "revenue": 0.8},
        counterfactual_inter=("marketing", 2.0),
        target_var="revenue"
    )
    assert cf == 1.6


def test_active_inference_planner():
    planner = ActiveInferencePlannerEngine(curiosity_weight=1.0)
    efe = planner.calculate_efe(
        prior_entropy=1.5,
        post_entropy=0.5,
        success_prob=0.8,
        target_pref=0.9
    )
    assert isinstance(efe, float)


def test_portfolio_and_capital_allocation():
    engine = CapitalAllocationAndPortfolioEngine()
    res_b, ven_b = engine.proportion_portfolio(1000000, market_uncertainty=0.6)
    assert res_b == 400000
    assert ven_b == 600000

    allocs = engine.allocate_venture_capital({"cell_a": 0.8, "cell_b": 0.2}, ven_b)
    assert sum(allocs.values()) == ven_b


def test_competitive_moat():
    moat = CompetitiveIntelligenceAndMoatEngine()
    moat.register_competitor("comp_1", ["feat_a", "feat_b"])
    parity = moat.calculate_feature_parity(["feat_a"])
    assert parity == 0.5
    score = moat.score_moat_durability(0.8, 500000, 0.9, 0.3)
    assert 0.0 <= score <= 1.0


def test_failure_and_reinvention():
    engine = FailureAndReinventionEngine()
    hazard = engine.predict_insolvency_hazard(burn_multiple=3.0, runway_months=4.0, ltv_to_cac=1.5)
    assert hazard > 0.10
    pivot = engine.evaluate_reinvention_necessity(0.20, 0.25)
    assert pivot is True


def test_memory_and_governance():
    engine = EntrepreneurialMemoryAndGovernanceEngine()
    safe = engine.audit_alignment_and_safety("deploy_model", 0.2)
    assert safe is True
    engine.log_trajectory_step("cell_1", "deploy_model", {"risk": 0.2})
    assert len(engine.trajectory_log) == 1


def test_full_14_layer_engine_cycle():
    engine = FourteenLayerEngine()
    sig = OpportunitySignal(
        title="Full Pipeline Opportunity",
        domain="ai_intelligence",
        keywords=["active_inference", "causal_scm", "token_bidding"],
        tam_cents=50000000
    )
    res = engine.execute_full_14_layer_cycle(
        signals=[sig],
        total_budget_cents=10000000,
        venture_cells={"cell_alpha": {"score": 0.9}, "cell_beta": {"score": 0.4}}
    )
    assert res["status"] == "completed"
    assert res["layer_2_ingested_nodes"] == 1
    assert "layer_6_7_portfolio" in res
    assert "layer_8_9_moat" in res
    assert "layer_10_11_risk" in res
    assert res["layer_12_13_memory_logged"] == 2
