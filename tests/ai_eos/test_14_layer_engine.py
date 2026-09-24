"""
Unit and Integration Test Suite for the 14-Layer Computational Architecture Engine.
"""

import pytest
from apodex.ai_eos.intelligence import (
    RealitySubstrate,
    WeakSignal,
    OpportunityDiscoveryEngine,
    ProblemNode,
    ProblemDiscoveryEngine,
    DecisionState,
    OpportunityEvaluator,
    FeatureSpec,
    ProductCreationEngine,
    CustomerPsychologyEngine,
    MarketingEngine,
    SalesEngine,
    GrowthEngine,
    CompetitionEngine,
    OrgDesignEngine,
    MetaLearningEngine,
    ResourceAllocationPlan,
    AutonomousAIEntrepreneurEngine,
)


def test_layer_1_reality_substrate():
    reality = RealitySubstrate()
    assert reality.asymmetric_value_ratio == 10.0
    delta = reality.evaluate_entropy_reduction(10.0, 3.0)
    assert delta == 7.0


def test_layer_2_opportunity_discovery():
    disc = OpportunityDiscoveryEngine()
    signals = [
        WeakSignal(domain="tech", intensity=0.9, reconstruction_error=2.5, economic_relevance=0.8),
        WeakSignal(domain="noise", intensity=0.1, reconstruction_error=0.5, economic_relevance=0.2),
    ]
    filtered = disc.filter_weak_signals(signals, anomaly_threshold=2.0)
    assert len(filtered) == 1
    assert filtered[0].domain == "tech"


def test_layer_3_problem_discovery():
    prob_engine = ProblemDiscoveryEngine()
    nodes = [
        ProblemNode(node_id="symptom_slow_build", is_root_cause=False),
        ProblemNode(node_id="root_arch_debt", is_root_cause=True),
    ]
    weights = {"symptom_slow_build": 0.2, "root_arch_debt": 0.9}
    root = prob_engine.identify_root_cause(nodes, weights)
    assert root is not None
    assert root.node_id == "root_arch_debt"

    assert prob_engine.should_ignore_problem(expected_value_delta=10.0, intervention_cost=20.0, opportunity_cost=5.0) is True


def test_layer_4_decision_making():
    ds = DecisionState(prior_entropy=1.5, posterior_entropy=0.3, pragmatic_value=2.0)
    efe = ds.compute_expected_free_energy()
    # EFE = -2.0 - (1.2 * 1.0) = -3.2
    assert pytest.approx(efe, 1e-4) == -3.2


def test_layer_5_opportunity_evaluation():
    evaluator = OpportunityEvaluator()
    npv = evaluator.calculate_net_present_value(tam=10_000_000, success_prob=0.5)
    assert npv > 0.0

    # Abandonment check
    should_kill = evaluator.check_abandonment_threshold(current_posterior=0.1, alternative_ev=100.0, current_ev=200.0)
    assert should_kill is True


def test_layer_6_product_creation():
    product_engine = ProductCreationEngine()
    features = [
        FeatureSpec(feature_id="core_login", causal_path_length=1, complexity_penalty=0.1),
        FeatureSpec(feature_id="bloat_animation", causal_path_length=5, complexity_penalty=1.5),
    ]
    filtered = product_engine.filter_essential_features(features)
    assert len(filtered) == 1
    assert filtered[0].feature_id == "core_login"


def test_layer_7_customer_understanding():
    cust_engine = CustomerPsychologyEngine()
    gain_u = cust_engine.compute_prospect_utility(10.0)
    loss_u = cust_engine.compute_prospect_utility(-10.0)
    assert abs(loss_u) > abs(gain_u)  # Loss aversion

    assert cust_engine.will_customer_switch(new_utility=10.0, current_utility=3.0, switching_cost=5.0) is True


def test_layer_8_marketing():
    mkt = MarketingEngine()
    k_factor = mkt.compute_viral_reproduction_number(invites_per_user=5.0, conversion_rate=0.3)
    assert k_factor == 1.5


def test_layer_9_sales():
    sales = SalesEngine()
    coi = sales.calculate_cost_of_inaction(monthly_inefficiency=1000.0, duration_months=6)
    assert coi > 6000.0


def test_layer_10_growth():
    growth = GrowthEngine()
    assert growth.should_throttle_growth(acquisition_rate=1000.0, ops_capacity_rate=500.0) is True


def test_layer_11_competition():
    comp = CompetitionEngine()
    assert comp.evaluate_pivot_necessity([1.5, 2.0, 1.8], min_threshold=3.0) is True


def test_layer_12_org_design():
    org = OrgDesignEngine()
    assert org.should_hire_agent(task_workload_hours=50.0, delegation_overhead=5.0) is True


def test_layer_13_meta_learning():
    meta = MetaLearningEngine()
    new_prior = meta.update_system_priors(prior_weight=0.5, episode_outcome=1.0, learning_rate=0.2)
    assert pytest.approx(new_prior, 1e-4) == 0.6


def test_layer_14_ai_entrepreneurship_orchestrator():
    master = AutonomousAIEntrepreneurEngine()
    allocations = master.allocate_resources(
        total_capital=100_000.0,
        total_flops=1e15,
        total_time=1000.0,
        opportunities=[
            {"id": "opp_a", "ev": 300.0},
            {"id": "opp_b", "ev": 100.0},
        ]
    )
    assert "opp_a" in allocations
    assert allocations["opp_a"].capital_usd == 75_000.0
    assert allocations["opp_b"].capital_usd == 25_000.0

    eroicc = master.calculate_eroicc(
        valuation_change=1_000_000.0,
        free_cash_flow_change=200_000.0,
        capital_consumed=100_000.0,
        flops_consumed=1e15,
        flops_cost_weight=1e-12
    )
    assert eroicc > 0.0
