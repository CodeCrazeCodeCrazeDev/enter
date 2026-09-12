"""
Comprehensive unit and integration test suite for the 14-Layer Computational Architecture
of Entrepreneurship (apodex.ai_eos.intelligence.fourteen_layer_engine).
"""

import pytest
from apodex.ai_eos.intelligence import (
    OpportunityState,
    RealitySubstrateEngine,
    OpportunityDiscoveryEngine,
    ProblemDiscoveryEngine,
    DecisionMakingEngine,
    OpportunityEvaluationEngine,
    ProductCreationEngine,
    CustomerUnderstandingEngine,
    MarketingEngine,
    SalesSystemEngine,
    GrowthDynamicsEngine,
    CompetitiveMoatEngine,
    OrganizationalDesignEngine,
    MetaLearningEngine,
    FourteenLayerEntrepreneurialEngine,
)


def test_layer1_reality_invariants():
    engine = RealitySubstrateEngine()
    opp = OpportunityState(title="Quantum Supply", domain="quantum", ltv_cents=100000, cac_cents=10000)
    res = engine.analyze_invariants(opp)
    assert res["is_viable_invariant"] is True
    assert res["asymmetry_ratio"] > 2.0


def test_layer2_opportunity_discovery():
    engine = OpportunityDiscoveryEngine()
    opp = engine.discover_opportunity({"title": "Autonomous Agent Ops", "domain": "ai"})
    assert opp.title == "Autonomous Agent Ops"
    assert len(opp.variables) > 0
    assert opp.success_probability > 0.0


def test_layer3_problem_discovery_scm():
    engine = ProblemDiscoveryEngine()
    vars_list = ["marketing", "leads", "conversions", "churn"]
    edges = [("marketing", "leads"), ("leads", "conversions"), ("conversions", "churn")]
    res = engine.isolate_root_cause(vars_list, edges)
    assert res["root_causes"] == ["marketing"]
    assert res["symptoms"] == ["churn"]


def test_layer4_decision_making_efe():
    engine = DecisionMakingEngine(curiosity_weight=1.5)
    opp1 = OpportunityState(title="Opp A", success_probability=0.8, prior_entropy=1.5, post_entropy_simulated=0.3)
    opp2 = OpportunityState(title="Opp B", success_probability=0.3, prior_entropy=1.5, post_entropy_simulated=1.2)
    best_opp, efe = engine.select_best_decision([opp1, opp2])
    assert best_opp.title == "Opp A"
    assert isinstance(efe, float)


def test_layer5_opportunity_evaluation_real_options_and_kelly():
    engine = OpportunityEvaluationEngine()
    opp = OpportunityState(title="SaaS Platform", tam_cents=1000000000, success_probability=0.6)
    val = engine.evaluate_real_option(opp, strike_cost=100000.0)
    assert val > 0.0
    kelly_f = engine.calculate_kelly_capital_fraction(p_win=0.6, payout_ratio=3.0)
    assert 0.0 <= kelly_f <= 0.25


def test_layer6_product_creation_complexity():
    engine = ProductCreationEngine()
    features = [
        {"name": "f1_core", "cost": 2.0, "value": 10.0},
        {"name": "f2_extra", "cost": 5.0, "value": 4.0},
        {"name": "f3_fluff", "cost": 8.0, "value": 1.0}
    ]
    res = engine.optimize_feature_set(features, max_complexity=8.0)
    assert "f1_core" in res["selected_features"]
    assert "f3_fluff" not in res["selected_features"]


def test_layer7_customer_understanding():
    engine = CustomerUnderstandingEngine()
    prob = engine.evaluate_switching_probability(new_utility=10.0, old_utility=2.0, switching_cost=1.0, perceived_risk=1.0)
    assert prob > 0.95


def test_layer8_marketing_virality():
    engine = MarketingEngine()
    r0 = engine.calculate_viral_reproduction_number(contact_rate_beta=2.0, recovery_rate_gamma=1.0)
    assert r0 == 2.0


def test_layer9_sales_urgency():
    engine = SalesSystemEngine()
    prob = engine.compute_close_probability(urgency=3.0, perceived_value=4.0, friction=1.0, price=2.0)
    assert prob > 0.90


def test_layer10_growth_dynamics():
    engine = GrowthDynamicsEngine()
    val = engine.calculate_metcalfe_value(100)
    assert val == 10000.0
    curve = engine.project_compounding_growth(initial_users=10, growth_rate=0.5, capacity_k=1000, steps=3)
    assert len(curve) == 4
    assert curve[-1] > curve[0]


def test_layer11_competitive_moat_pivot():
    engine = CompetitiveMoatEngine()
    should_pivot = engine.should_trigger_pivot(cac_history=[10, 20, 30], retention_rate=0.20)
    assert should_pivot is True


def test_layer12_org_design_provisioning():
    engine = OrganizationalDesignEngine()
    res = engine.evaluate_provisioning(arrival_rate_lambda=10.0, service_rate_mu=10.0)
    assert res["should_provision_agent"] is True


def test_layer13_meta_learning_failure_synthesis():
    engine = MetaLearningEngine()
    res = engine.synthesize_failure_knowledge([{"step": "deployment", "state": "flawed"}], outcome_reward=-1.0)
    assert res["status"] == "failure_synthesized"
    assert "NEGATIVE_PRIOR" in res["knowledge_primitive"]


def test_fourteen_layer_orchestrator_pipeline():
    master_engine = FourteenLayerEntrepreneurialEngine()
    pipeline_res = master_engine.run_full_14_layer_pipeline({
        "title": "Autonomous Enterprise AI",
        "domain": "enterprise_ai",
        "signal_timestamps": [0.5, 1.0, 1.8, 2.2, 2.9]
    })
    assert pipeline_res["opportunity_title"] == "Autonomous Enterprise AI"
    assert pipeline_res["reality_audit"]["is_viable_invariant"] is True
    assert "core_workflow" in pipeline_res["product_features"]
    assert pipeline_res["switching_probability"] > 0.5
    assert pipeline_res["viral_reproduction_number"] > 1.0
