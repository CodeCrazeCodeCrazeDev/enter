"""
Tests for the 14-Layer Computational Architecture Engine.
"""

import pytest
from apodex.ai_eos.intelligence import (
    Layer1RealityEngine,
    Layer2OpportunityDiscoveryEngine,
    Layer3ProblemDiscoveryEngine,
    Layer4DecisionMakingEngine,
    Layer5OpportunityEvaluationEngine,
    Layer6ProductCreationEngine,
    Layer7CustomerUnderstandingEngine,
    Layer8MarketingEngine,
    Layer9SalesEngine,
    Layer10GrowthEngine,
    Layer11CompetitionEngine,
    Layer12OrgDesignEngine,
    Layer13MetaLearningEngine,
    Layer14AIEntrepreneurshipEngine,
    FourteenLayerEntrepreneurshipOrchestrator,
)


def test_layer1_reality_engine():
    engine = Layer1RealityEngine()
    res = engine.evaluate_bounds(100000, 20000, 30)
    assert res["is_sustainable"] is True
    assert res["net_capital"] == 80000
    assert res["runway_days"] == 150.0


def test_layer2_opportunity_discovery_engine():
    engine = Layer2OpportunityDiscoveryEngine()
    kl = engine.search_kl_divergence([0.8, 0.2], [0.3, 0.7])
    assert kl > 0.0

    weak_signals = engine.detect_weak_signals([{"variance": 5.0, "frequency": 1.0}])
    assert len(weak_signals) == 1

    combined = engine.combine_unrelated_domains(["ai"], ["bio"])
    assert combined == ["ai_x_bio"]


def test_layer3_problem_discovery_engine():
    engine = Layer3ProblemDiscoveryEngine()
    decomposition = engine.decompose_causal_problem([("root", "symptom")], "symptom")
    assert decomposition["probable_root_causes"] == ["root"]

    evig, ignore = engine.calculate_evig(2.0, 0.5, 0.5)
    assert evig == 1.0
    assert ignore is False


def test_layer4_decision_making_engine():
    engine = Layer4DecisionMakingEngine()
    mean, prec = engine.bayesian_update(1.0, 1.0, 3.0, 1.0)
    assert mean == 2.0
    assert prec == 2.0

    action = engine.sprt_idea_kill_check(-5.0)
    assert action == "KILL"


def test_layer5_opportunity_evaluation_engine():
    engine = Layer5OpportunityEvaluationEngine()
    ev = engine.calculate_jump_diffusion_ev(100, 0.1, 0.2, 0.1, -0.2, 1.0)
    assert ev > 0.0


def test_layer6_product_creation_engine():
    engine = Layer6ProductCreationEngine()
    pruned = engine.prune_features_jtbd([
        {"name": "f1", "utility": 10, "cost": 2},
        {"name": "f2", "utility": 1, "cost": 10},
    ])
    assert len(pruned) == 1
    assert pruned[0]["name"] == "f1"


def test_layer7_customer_understanding_engine():
    engine = Layer7CustomerUnderstandingEngine()
    u_gain = engine.prospect_theory_utility(10.0)
    u_loss = engine.prospect_theory_utility(-10.0)
    assert u_gain > 0.0
    assert u_loss < 0.0
    assert abs(u_loss) > u_gain  # Loss aversion

    switch = engine.evaluate_switching_decision(10.0, 5.0, 2.0)
    assert switch is True


def test_layer8_marketing_engine():
    engine = Layer8MarketingEngine()
    k, is_viral = engine.calculate_viral_spread(0.1, 15.0)
    assert k == 1.5
    assert is_viral is True


def test_layer9_sales_engine():
    engine = Layer9SalesEngine()
    route = engine.route_sales_model(100000)
    assert route == "HIGH_TOUCH_ENTERPRISE"


def test_layer10_growth_engine():
    engine = Layer10GrowthEngine()
    val = engine.calculate_network_value(100)
    assert val > 0.0

    slowdown = engine.check_intentional_slowdown(98.0, 100.0)
    assert slowdown is True


def test_layer11_competition_engine():
    engine = Layer11CompetitionEngine()
    pivot = engine.check_pivot_trigger(0.05, 0.10)
    assert pivot is True


def test_layer12_org_design_engine():
    engine = Layer12OrgDesignEngine()
    roles = engine.evaluate_hiring_triggers({"eng": 160000}, {"eng": 120000})
    assert roles == ["eng"]

    boundary = engine.coase_delegation_boundary(100, 200)
    assert boundary == "KEEP_IN_HOUSE"


def test_layer13_meta_learning_engine():
    engine = Layer13MetaLearningEngine()
    updated = engine.backpropagate_error({"w1": 1.0}, 2.0, 0.1)
    assert updated["w1"] == 0.8


def test_layer14_orchestrator():
    orchestrator = FourteenLayerEntrepreneurshipOrchestrator()
    res = orchestrator.run_full_14_layer_pipeline({
        "capital_in": 200000,
        "capital_out": 20000,
        "burn_rate_days": 30,
        "acv": 25000,
    })
    assert res["status"] == "success"
    assert res["l1_reality"]["is_sustainable"] is True
    assert res["l9_sales_model"] == "INSIDE_SALES_HYBRID"
