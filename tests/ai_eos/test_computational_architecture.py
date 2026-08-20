from __future__ import annotations
import pytest
from uuid import uuid4

from apodex.ai_eos.intelligence.computational_architecture import (
    Opportunity,
    CustomerProfile,
    RealityEngine,
    OpportunityDiscoveryEngine,
    AdvancedCausalEngine,
    ActiveInferencePlanner,
    OpportunityEvaluationEngine,
    ProductCreationEngine,
    CustomerUnderstandingEngine,
    MarketingEngine,
    SalesEngine,
    GrowthEngine,
    CompetitionEngine,
    OrganizationDesignEngine,
    MetaLearningEngine,
    EntrepreneurialIntelligenceOrchestrator
)


def test_layer_1_reality_engine() -> None:
    engine = RealityEngine()
    res_auto = engine.evaluate_task_automation("opportunity_evaluation")
    res_human = engine.evaluate_task_automation("human_trust_building")

    assert res_auto["can_automate"] is True
    assert res_human["can_automate"] is False
    assert res_human["psychology_weight"] > res_auto["psychology_weight"]


def test_layer_2_opportunity_discovery_engine() -> None:
    engine = OpportunityDiscoveryEngine()
    signals = [
        {"title": "Weak AI Signal", "signal_strength": 0.25, "novelty": 0.6},
        {"title": "Noise Signal", "signal_strength": 0.05, "novelty": 0.1}
    ]
    opps = engine.search_state_space(signals)
    assert len(opps) == 1
    assert opps[0].title == "Weak AI Signal"


def test_layer_3_problem_decomposition_and_scm() -> None:
    engine = AdvancedCausalEngine()
    prob_def = engine.decompose_problem(
        stated_problem="Low Customer Retention",
        observed_symptoms=["high_churn", "poor_onboarding", "slow_support"]
    )
    assert prob_def.is_root_cause is True
    assert prob_def.ignore_score < 0.1  # Root causes must not be ignored


def test_active_inference_planner_ranking() -> None:
    planner = ActiveInferencePlanner(curiosity_weight=2.0)

    opp_1 = Opportunity(
        title="high_exploratory_opportunity",
        domain="tech_frontier",
        prior_entropy=2.0,
        post_entropy_simulated=0.4,
        success_probability=0.4,
        target_preference=0.9
    )

    opp_2 = Opportunity(
        title="conservative_replication",
        domain="traditional_retail",
        prior_entropy=0.6,
        post_entropy_simulated=0.5,
        success_probability=0.85,
        target_preference=0.9
    )

    ranked = planner.rank_opportunities([opp_1, opp_2])
    assert ranked[0][0].title == "high_exploratory_opportunity"
    assert ranked[0][1] < ranked[1][1]


def test_layer_5_opportunity_evaluation_and_kelly() -> None:
    eval_engine = OpportunityEvaluationEngine()
    opp = Opportunity(
        title="SaaS Venture",
        domain="B2B",
        success_probability=0.6,
        tam_cents=1000000000,
        capital_required_cents=100000000
    )
    ev = eval_engine.compute_expected_value_cents(opp)
    kelly = eval_engine.calculate_kelly_fraction(opp)

    assert ev == 600000000.0
    assert 0.0 < kelly <= 0.25

    should_abandon = eval_engine.evaluate_abandonment(opp, current_loss_cents=60000000)
    assert should_abandon is True


def test_layer_6_product_creation_and_pruning() -> None:
    product_engine = ProductCreationEngine()
    features = [
        {"name": "core_workflow", "complexity": 0.2, "jtbd_value": 0.8},
        {"name": "bloat_analytics", "complexity": 0.9, "jtbd_value": 0.2}
    ]
    pruned = product_engine.prune_anti_features(features)
    assert len(pruned) == 1
    assert pruned[0]["name"] == "core_workflow"


def test_layer_7_customer_trust_and_switching() -> None:
    customer_engine = CustomerUnderstandingEngine()
    cust = CustomerProfile(segment="enterprise", trust_level=0.5, switching_friction=0.6)
    new_trust = customer_engine.simulate_trust_dynamics(cust, positive_touchpoints=2, negative_touchpoints=0)
    assert new_trust == 0.7

    switch_prob = customer_engine.calculate_switching_probability(cust, competitor_value_delta=1.2)
    assert switch_prob > 0.4


def test_layer_8_9_10_11_12_13_operations() -> None:
    marketing = MarketingEngine()
    assert marketing.compute_viral_k_factor(2.0, 0.6) == 1.2

    sales = SalesEngine()
    assert sales.should_automate_sales(100000) is True
    assert sales.should_automate_sales(1000000) is False

    growth = GrowthEngine()
    assert growth.calculate_network_effect_value(100) == 100.0
    assert growth.evaluate_platform_transition(12, 0.25) is True

    competition = CompetitionEngine()
    moat = competition.compute_moat_durability(0.8, 0.8, 0.8)
    assert pytest.approx(moat) == 0.8

    org = OrganizationDesignEngine()
    assert org.evaluate_delegation_threshold(0.5, 0.8) == "delegate"

    meta = MetaLearningEngine()
    rule = meta.process_failure_post_mortem("premature_scaling", 100000.0)
    assert "AVOID: premature_scaling" in rule

    bayesian_post = meta.update_prior_belief(0.5, 0.8)
    assert bayesian_post == 0.8


def test_advanced_causal_engine_do_and_counterfactual() -> None:
    engine = AdvancedCausalEngine()
    engine.add_causal_relationship("marketing_spend", "click_through_rate", 0.6)
    engine.add_causal_relationship("click_through_rate", "sales_revenue", 1.8)

    state = engine.execute_do_intervention("marketing_spend", 2.0)
    assert state["marketing_spend"] == 2.0
    assert pytest.approx(state["click_through_rate"]) == 1.2
    assert pytest.approx(state["sales_revenue"]) == 2.16

    factual_observations = {
        "marketing_spend": 1.0,
        "click_through_rate": 0.8,
        "sales_revenue": 1.44
    }
    counterfactual_revenue = engine.estimate_counterfactual(
        factual_observations=factual_observations,
        counterfactual_intervention=("marketing_spend", 2.0),
        target_outcome_var="sales_revenue"
    )
    assert pytest.approx(counterfactual_revenue) == 2.52


def test_orchestrated_pipeline_execution_all_14_layers() -> None:
    engine = AdvancedCausalEngine()
    planner = ActiveInferencePlanner(curiosity_weight=1.5)
    orchestrator = EntrepreneurialIntelligenceOrchestrator(engine, planner)

    signal = {
        "title": "Autonomous Scientific Hardware Venture",
        "domain": "robotics",
        "variables": ["marketing_spend", "click_through_rate", "sales_revenue"],
        "causal_edges": [("marketing_spend", "click_through_rate"), ("click_through_rate", "sales_revenue")],
        "coefficients": {
            "marketing_spend->click_through_rate": 0.5,
            "click_through_rate->sales_revenue": 2.0
        },
        "prior_entropy": 1.8,
        "post_entropy_simulated": 0.5,
        "success_probability": 0.6,
        "tam_cents": 500000000
    }

    orchestrator.ingest_signal(signal)
    res = orchestrator.execute_orchestrated_pipeline()

    assert res["status"] == "executed"
    assert res["selected_opportunity"] == "Autonomous Scientific Hardware Venture"
    assert "layer_1_reality" in res
    assert "layer_3_problem_decomposition" in res
    assert res["viral_k_factor"] == 1.2
    assert res["sales_automated"] is True
    assert res["moat_durability_score"] > 0.0
    assert res["delegation_recommendation"] == "delegate"
    assert "meta_learning_rule" in res
