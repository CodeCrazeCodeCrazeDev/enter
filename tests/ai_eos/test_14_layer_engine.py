"""
Unit and integration tests for the 14-Layer Computational Architecture of Entrepreneurship.
"""

import pytest
from apodex.ai_eos.intelligence.fourteen_layer_engine import (
    EntrepreneurialSignal,
    DiscoveredOpportunity,
    ProblemNode,
    JTBDDefinition,
    CustomerPsychModel,
    SalesFunnelState,
    Layer1RealityEngine,
    Layer2OpportunityDiscoveryEngine,
    Layer3ProblemDiscoveryEngine,
    Layer4DecisionEngine,
    Layer5OpportunityEvaluationEngine,
    Layer6ProductCreationEngine,
    Layer7CustomerUnderstandingEngine,
    Layer8MarketingEngine,
    Layer9SalesEngine,
    Layer10GrowthEngine,
    Layer11CompetitionEngine,
    Layer12OrganizationalDesignEngine,
    Layer13MetaLearningEngine,
    Layer14AIEntrepreneurshipEngine,
    FourteenLayerComputationalEngine
)


def test_layer_1_reality():
    engine = Layer1RealityEngine()
    arbitrage = engine.evaluate_thermodynamic_arbitrage(current_yield=100.0, potential_yield=250.0, friction=30.0)
    assert arbitrage == 120.0
    assert not engine.is_automatable_task("human_empathy_relational")
    assert engine.is_automatable_task("data_scraping")


def test_layer_2_opportunity_discovery():
    engine = Layer2OpportunityDiscoveryEngine()
    sig = EntrepreneurialSignal(domain="fintech", source="twitter", entropy_score=1.2, signal_to_noise=2.0)
    assert engine.detect_weak_signal(sig, threshold=1.5)

    opp = engine.bisociate_domains("healthcare", "ai_llm")
    assert opp.domain == "healthcare_ai_llm"
    assert "healthcare" in opp.bisociated_domains


def test_layer_3_problem_discovery():
    engine = Layer3ProblemDiscoveryEngine()
    chain = ["slow_checkout", "payment_gateway_timeout", "legacy_soap_api"]
    prob = engine.decompose_problem("Customer abandoned cart", chain)
    assert prob.root_cause == "legacy_soap_api"
    assert not prob.is_first_order  # Multiple hops
    assert engine.should_ignore_problem(prob, solve_cost=200000.0)


def test_layer_4_decision_making():
    engine = Layer4DecisionEngine()
    # Bad hypothesis giving negative log-likelihood ratios
    ratios = [-0.8, -0.7, -0.6]
    kill = engine.evaluate_sprt_kill_switch(ratios, lower_bound=-2.0)
    assert kill


def test_layer_5_opportunity_evaluation():
    engine = Layer5OpportunityEvaluationEngine()
    opp = DiscoveredOpportunity(
        title="Test Arbitrage",
        domain="saas",
        tam_cents=100000000,  # $1M
        prior_entropy=1.5,
        post_entropy_simulated=0.2,
        p_success=0.7,
        p_target_preference=0.9
    )
    efe = engine.calculate_expected_free_energy(opp)
    ev = engine.calculate_expected_value(opp, margin=0.8, execution_cost=50000.0)
    assert efe < 0  # Low Expected Free Energy indicates high value
    assert ev == (0.7 * 1000000.0 * 0.8) - 50000.0  # $560k - $50k = $510k


def test_layer_6_product_creation():
    engine = Layer6ProductCreationEngine()
    features = {"core_analytics": 0.9, "ai_autocompletion": 0.8, "custom_themes": 0.2}
    jtbd = engine.formulate_jtbd("manual_reporting", "automated_insights", features)
    assert "core_analytics" in jtbd.core_features
    assert "custom_themes" in jtbd.pruned_features


def test_layer_7_customer_understanding():
    engine = Layer7CustomerUnderstandingEngine()
    psych = CustomerPsychModel(customer_segment="b2b_saas", trust_score=0.5, switching_barrier=1.5)
    new_trust = engine.update_trust(psych, delivery_delta=0.4, learning_rate=0.2)
    assert new_trust == pytest.approx(0.58)
    assert not engine.will_customer_switch(psych, new_utility=2.0, old_utility=1.0)
    assert engine.will_customer_switch(psych, new_utility=3.0, old_utility=1.0)


def test_layer_8_marketing():
    engine = Layer8MarketingEngine()
    k = engine.calculate_viral_coefficient(infection_rate_beta=0.1, susceptible_pop=50.0, recovery_rate_gamma=2.0)
    assert k == 2.5  # K > 1 indicates viral exponential growth


def test_layer_9_sales():
    engine = Layer9SalesEngine()
    funnel = SalesFunnelState(stage="awareness")
    engine.advance_funnel(funnel, "inquire")
    assert funnel.stage == "interest"
    engine.advance_funnel(funnel, "demo")
    assert funnel.stage == "evaluation"
    assert engine.should_automate_sales(acv_cents=100000)  # $1,000 ACV -> automated
    assert not engine.should_automate_sales(acv_cents=5000000)  # $50,000 ACV -> enterprise high-touch


def test_layer_10_growth():
    engine = Layer10GrowthEngine()
    metcalfe = engine.calculate_metcalfe_value(num_nodes=100)
    assert metcalfe == 10000.0
    compounded = engine.calculate_compounding_users(100, k_factor=0.1, reinvestment_ltv_cac=1.0, periods=3)
    assert compounded > 100


def test_layer_11_competition():
    engine = Layer11CompetitionEngine()
    moat_score = engine.evaluate_moat_score({"network_effects": 1.0, "switching_costs": 0.8, "cost_advantages": 0.5})
    assert moat_score > 0.5


def test_layer_12_organizational_design():
    engine = Layer12OrganizationalDesignEngine()
    assert engine.should_trigger_hiring(work_demand=130.0, throughput_capacity=100.0)
    assert not engine.should_trigger_hiring(work_demand=100.0, throughput_capacity=100.0)


def test_layer_13_meta_learning():
    engine = Layer13MetaLearningEngine()
    brier = engine.compute_brier_score(predictions=[0.8, 0.9, 0.2], outcomes=[1, 1, 0])
    assert brier == pytest.approx((0.04 + 0.01 + 0.04) / 3.0)


def test_layer_14_ai_entrepreneurship():
    engine = Layer14AIEntrepreneurshipEngine()
    projects = [
        {"name": "Project Alpha", "ev": 500000.0, "var": 50000.0},
        {"name": "Project Beta", "ev": 200000.0, "var": 100000.0}
    ]
    allocation = engine.allocate_resources(projects, total_budget=100000.0)
    assert "Project Alpha" in allocation
    assert allocation["Project Alpha"] > allocation["Project Beta"]


def test_end_to_end_14_layer_engine():
    master_engine = FourteenLayerComputationalEngine()
    sig = EntrepreneurialSignal(domain="edtech", source="github_trends", entropy_score=1.5, signal_to_noise=2.0)
    result = master_engine.process_end_to_end_opportunity(
        signal=sig,
        domain_b="generative_ai",
        causal_chain=["high_dropout_rates", "lack_of_personalization"],
        feature_candidates={"ai_tutor": 0.9, "gamified_badges": 0.3},
        budget=250000.0
    )

    assert result["status"] == "orchestrated_successfully"
    assert result["is_valid_signal"]
    assert "edtech" in result["opportunity_title"]
    assert result["root_cause_problem"] == "lack_of_personalization"
    assert "ai_tutor" in result["jtbd_core_features"]
    assert result["resource_allocation"] is not None
