"""
Comprehensive unit and integration test suite for the 14-Layer Computational Architecture Engine.
"""

import pytest
from apodex.ai_eos.intelligence.fourteen_layer_engine import (
    FourteenLayerEngine,
    RealitySubstrateLayer,
    OpportunityDiscoveryLayer,
    ProblemDiscoveryLayer,
    DecisionMakingLayer,
    OpportunityEvaluationLayer,
    ProductCreationLayer,
    CustomerUnderstandingLayer,
    MarketingSystemLayer,
    SalesSystemLayer,
    GrowthCompoundingLayer,
    CompetitionMoatLayer,
    OrganizationalDesignLayer,
    MetaLearningLayer,
    AIEntrepreneurshipOrchestratorLayer,
    FourteenLayerOpportunityState,
    MarketSignal,
    ProblemDefinition,
    DecisionOption,
    OpportunityMetrics,
    ProductFeature,
    CustomerProfile,
    MarketingCampaign,
    SalesLead,
    GrowthMetrics,
    MoatEvaluator,
    OrgBottleneck
)


def test_layer1_reality_substrate():
    layer = RealitySubstrateLayer()
    assert len(layer.invariant_principles) == 4
    res = layer.classify_task("Build user trust in negotiation")
    assert res["type"] == "human_psychology"
    assert res["automatable"] is False

    res_opt = layer.classify_task("Optimize capital allocation pipeline")
    assert res_opt["type"] == "optimization_problem"
    assert res_opt["automatable"] is True


def test_layer2_opportunity_discovery():
    layer = OpportunityDiscoveryLayer()
    signals = [
        MarketSignal(source="rss", magnitude=0.1, timestamp=1.0),
        MarketSignal(source="github", magnitude=0.9, timestamp=2.0)
    ]
    filtered = layer.filter_hawkes_signals(signals)
    assert len(filtered) == 1
    assert filtered[0].source == "github"

    combinations = layer.generate_combinatorial_novelty(["ai", "bio"], ["saas", "hardware"])
    assert len(combinations) == 4


def test_layer3_problem_discovery():
    layer = ProblemDiscoveryLayer()
    prob = ProblemDefinition(
        description="High API latency",
        current_state_utility=2.0,
        desired_state_utility=8.0,
        switching_cost=1.0,
        is_root_cause=True
    )
    assert prob.net_friction == 5.0
    friction = layer.perform_causal_intervention(prob, is_intervened=True)
    assert friction == 0.5


def test_layer4_decision_making():
    layer = DecisionMakingLayer()
    opt1 = DecisionOption(name="A", expected_value=100.0, confidence=0.8, execution_energy=10.0, falsification_threshold=5.0)
    opt2 = DecisionOption(name="B", expected_value=200.0, confidence=0.9, execution_energy=10.0, falsification_threshold=10.0)

    ranked = layer.prioritize_attention([opt1, opt2])
    assert ranked[0].name == "B"

    assert layer.evaluate_falsification(opt1, metric_value=2.0) is True
    assert layer.evaluate_falsification(opt1, metric_value=8.0) is False


def test_layer5_opportunity_evaluation():
    layer = OpportunityEvaluationLayer()
    metrics = OpportunityMetrics(
        tam_cents=100000000,
        margin_potential=0.8,
        adoption_velocity=1.5,
        retention_rate=0.9,
        success_probability=0.7,
        downside_cost_cents=10000,
        upside_value_cents=100000
    )
    ev = layer.calculate_ev(metrics)
    assert ev == (0.7 * 100000) - (0.3 * 10000)
    sharpe = layer.calculate_sharpe_ratio(metrics, variance=100.0)
    assert sharpe > 0


def test_layer6_product_creation():
    layer = ProductCreationLayer()
    f1 = ProductFeature(name="A", jtbd_contribution=10.0, complexity_cost=2.0)
    f2 = ProductFeature(name="B", jtbd_contribution=2.0, complexity_cost=10.0)

    pruned = layer.prune_features([f1, f2], max_complexity=5.0)
    assert len(pruned) == 1
    assert pruned[0].name == "A"


def test_layer7_customer_understanding():
    layer = CustomerUnderstandingLayer()
    profile = CustomerProfile(perceived_outcome=10.0, perceived_probability=0.8, time_delay=2.0, effort_and_sacrifice=2.0)
    val = layer.calculate_perceived_value(profile)
    assert val == 8.0 / 4.0


def test_layer8_marketing():
    layer = MarketingSystemLayer()
    campaign = MarketingCampaign(invites_per_user=2.5, conversion_rate=0.5, top_of_funnel_reach=10000)
    assert layer.calculate_viral_coefficient(campaign) == 1.25
    assert layer.is_viral(campaign) is True


def test_layer9_sales():
    layer = SalesSystemLayer()
    lead = SalesLead(acv_cents=100000, seller_certainty=0.9, buyer_perceived_risk=0.4, objections=[])
    assert layer.evaluate_sale_closure(lead) is True
    assert layer.should_automate_sales(acv_cents=200000) is True
    assert layer.should_automate_sales(acv_cents=1000000) is False


def test_layer10_growth():
    layer = GrowthCompoundingLayer()
    metrics = GrowthMetrics(active_users=1000, cac_cents=5000, ltv_cents=20000, net_revenue_retention=1.3, monthly_churn=0.01)
    health = layer.evaluate_growth_health(metrics)
    assert health["ltv_cac_ratio"] == 4.0
    assert health["is_healthy"] is True


def test_layer11_competition():
    layer = CompetitionMoatLayer()
    moat = MoatEvaluator(network_effects=1.0, switching_costs=1.0, brand_equity=1.0, cost_advantage=1.0)
    assert abs(layer.calculate_moat_score(moat) - 1.0) < 1e-6


def test_layer12_org_design():
    layer = OrganizationalDesignLayer()
    b = OrgBottleneck(department="Engineering", capacity_utilization=0.9, queue_backlog=100)
    assert layer.evaluate_hiring_need(b) is True


def test_layer13_meta_learning():
    layer = MetaLearningLayer()
    post = layer.update_prior_belief(prior=0.5, likelihood=0.8)
    assert post > 0.5


def test_layer14_ai_orchestrator_and_full_engine():
    engine = FourteenLayerEngine()
    opp1 = FourteenLayerOpportunityState(title="Opp 1", success_probability=0.8, prior_entropy=1.0, post_entropy_simulated=0.2)
    opp2 = FourteenLayerOpportunityState(title="Opp 2", success_probability=0.2, prior_entropy=1.0, post_entropy_simulated=0.8)

    ranked = engine.ai_orchestrator.rank_opportunities([opp1, opp2])
    assert ranked[0][0].title == "Opp 1"

    res = engine.run_full_pipeline(opp1)
    assert res["status"] == "analyzed_across_14_layers"
