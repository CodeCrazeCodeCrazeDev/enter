"""
Unit and integration tests for the 14-Layer Computational Architecture of Entrepreneurship engine.
"""

import pytest
from apodex.ai_eos.intelligence import (
    FourteenLayerEngine,
    OpportunityData,
    RealitySubstrateLayer,
    OpportunityDiscoveryLayer,
    ProblemDiscoveryLayer,
    DecisionMakingLayer,
    OpportunityEvaluationLayer,
    ProductCreationLayer,
    CustomerUnderstandingLayer,
    MarketingEngineLayer,
    SalesPipelineLayer,
    GrowthEcosystemLayer,
    CompetitionMoatLayer,
    OrganizationalDesignLayer,
    MetaLearningLayer,
)


def test_reality_substrate_layer():
    layer = RealitySubstrateLayer()
    res = layer.evaluate_invariants(capital_at_risk_cents=10_000, expected_return_cents=50_000)
    assert res["asymmetric_ratio"] == 5.0
    assert res["meets_invariant"] is True


def test_opportunity_discovery_layer():
    layer = OpportunityDiscoveryLayer()
    signals = [
        {"title": "Low Signal", "anomaly_score": 0.1, "derivative_spike": 0.1},
        {"title": "High Signal", "anomaly_score": 0.9, "derivative_spike": 0.8},
    ]
    filtered = layer.detect_weak_signals(signals, signal_threshold=0.5)
    assert len(filtered) == 1
    assert filtered[0]["title"] == "High Signal"


def test_problem_discovery_layer():
    layer = ProblemDiscoveryLayer()
    res = layer.decompose_problem("Churn", {"ui_bugs": 0.2, "wrong_icp": 0.8})
    assert res["isolated_root_cause"] == "wrong_icp"
    assert res["stated_vs_real_divergence"] is True


def test_decision_making_layer():
    layer = DecisionMakingLayer()
    opp = OpportunityData(title="Test Opp", success_probability=0.8, prior_entropy=1.5, post_entropy_simulated=0.2)
    efe = layer.calculate_expected_free_energy(opp)
    assert isinstance(efe, float)
    kill_eval = layer.evaluate_kill_criteria(efe, max_efe_threshold=10.0)
    assert kill_eval["should_kill"] is False


def test_opportunity_evaluation_layer():
    layer = OpportunityEvaluationLayer()
    opp = OpportunityData(title="Eval Opp", tam_cents=100_000_000, success_probability=0.6, var_alpha_cents=5_000_000)
    eval_res = layer.evaluate_opportunity(opp)
    assert eval_res["expected_value_cents"] > 0
    assert eval_res["cvar_downside_cents"] == 7_500_000


def test_product_creation_layer():
    layer = ProductCreationLayer()
    res = layer.evaluate_feature("Analytics", delta_wtp_cents=10_000, complexity_cost_cents=3_000)
    assert res["should_build"] is True
    assert res["decision"] == "build"


def test_customer_understanding_layer():
    layer = CustomerUnderstandingLayer()
    util = layer.compute_customer_utility(gain_value=10.0, loss_value=2.0, friction=1.0)
    assert util == 10.0 - (2.25 * 2.0) - 1.0


def test_marketing_engine_layer():
    layer = MarketingEngineLayer()
    res = layer.simulate_viral_spread(s0=1000, i0=10, beta=0.003, gamma=0.1, steps=5)
    assert res["r0"] > 1.0
    assert res["is_viral"] is True


def test_sales_pipeline_layer():
    layer = SalesPipelineLayer()
    res_plg = layer.route_sales_channel(acv_cents=200_000)
    assert res_plg["recommended_channel"] == "automated_plg"

    res_ent = layer.route_sales_channel(acv_cents=10_000_000)
    assert res_ent["recommended_channel"] == "enterprise_human_sales"


def test_growth_ecosystem_layer():
    layer = GrowthEcosystemLayer()
    res = layer.evaluate_growth_health(nrr_percent=130.0, ltv_cac_ratio=4.0, nps=70.0)
    assert res["healthy"] is True
    assert res["action"] == "scale"


def test_competition_moat_layer():
    layer = CompetitionMoatLayer()
    res = layer.evaluate_pivot_criteria(ltv_cac_ratio=0.5, structural_iterations=3)
    assert res["should_pivot"] is True


def test_organizational_design_layer():
    layer = OrganizationalDesignLayer()
    res = layer.evaluate_hiring_trigger(team_load_percent=90.0, marginal_roi=4.0)
    assert res["should_hire"] is True


def test_meta_learning_layer():
    layer = MetaLearningLayer()
    brier = layer.calculate_brier_score([0.9, 0.1], [1, 0])
    assert brier == pytest.approx(0.01)


def test_fourteen_layer_engine_end_to_end():
    engine = FourteenLayerEngine()
    result = engine.run_full_14_layer_pipeline(
        raw_signals=[{"title": "Autonomous AI Disruption", "domain": "software", "anomaly_score": 0.95, "derivative_spike": 0.9}],
        capital_at_risk_cents=20_000_000,
        expected_return_cents=100_000_000,
        acv_cents=3_000_000
    )
    assert result["status"] == "success"
    assert result["layer1_reality"]["meets_invariant"] is True
    assert result["layer2_discovery"]["signals_detected"] == 1
    assert result["layer14_ai_orchestrated"] is True
