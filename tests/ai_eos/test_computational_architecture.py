"""
Unit and integration tests for the 14-Layer Computational Architecture of Entrepreneurship.
"""

import pytest
from uuid import uuid4
from apodex.ai_eos.intelligence.computational_architecture import (
    ComputationalArchitectureOfEntrepreneurship,
    Opportunity,
    Layer1_RealitySubstrate,
    Layer2_OpportunityDiscovery,
    Layer3_ProblemDiscovery,
    Layer4_DecisionEngine,
    Layer5_OpportunityEvaluation,
    Layer6_ProductCreation,
    Layer7_CustomerUnderstanding,
    Layer8_MarketingDynamics,
    Layer9_SalesSystems,
    Layer10_GrowthFlywheels,
    Layer11_CompetitiveStrategy,
    Layer12_OrganizationalDesign,
    Layer13_MetaLearning,
    Layer14_AIEntrepreneurshipOrchestration
)


def test_layer1_reality_invariants():
    l1 = Layer1_RealitySubstrate()
    res_psych = l1.classify_domain_task("build customer empathy and trust")
    assert res_psych["category"] == "human_psychology"
    assert res_psych["can_automate"] is False

    res_opt = l1.classify_domain_task("capital allocation optimization")
    assert res_opt["category"] == "optimization_problem"
    assert res_opt["can_automate"] is True

    valid, violations = l1.audit_invariants({"capture_value_before_creation": True})
    assert valid is False
    assert len(violations) > 0


def test_layer2_opportunity_discovery_sensing():
    l2 = Layer2_OpportunityDiscovery()
    raw = [
        {"id": "sig1", "amplitude": 0.5, "noise_floor": 1.0},
        {"id": "sig2", "amplitude": 5.0, "noise_floor": 1.0}
    ]
    filtered = l2.detect_weak_signals(raw, snr_threshold=1.0)
    assert len(filtered) == 1
    assert filtered[0]["id"] == "sig2"

    combos = l2.combine_unrelated_domains(["AI Agents"], ["Legal Compliance"])
    assert len(combos) == 1
    assert "Legal Compliance" in combos[0]["synthesized_opportunity"]


def test_layer3_problem_decomposition_scm():
    l3 = Layer3_ProblemDiscovery()
    l3.add_causal_relationship("price_increase", "churn", 0.8)
    l3.add_causal_relationship("churn", "revenue_drop", 1.2)

    inter_state = l3.execute_do_intervention("price_increase", 2.0)
    assert inter_state["price_increase"] == 2.0
    assert inter_state["churn"] == 1.6
    assert inter_state["revenue_drop"] == pytest.approx(1.92)


def test_layer4_decision_making_efe():
    l4 = Layer4_DecisionEngine(curiosity_weight=1.0)
    opp = Opportunity(
        title="Test Opp",
        domain="tech",
        prior_entropy=1.2,
        post_entropy_simulated=0.3,
        success_probability=0.7,
        target_preference=0.9
    )
    efe = l4.calculate_efe(opp)
    assert isinstance(efe, float)
    should_kill = l4.should_kill_idea(efe, max_efe_threshold=5.0)
    assert should_kill is False


def test_layer5_opportunity_evaluation_kelly():
    l5 = Layer5_OpportunityEvaluation()
    opp = Opportunity(
        title="High Yield Opp",
        domain="finance",
        win_probability=0.6,
        win_payoff=20000.0,
        loss_payoff=-10000.0
    )
    ev = l5.calculate_expected_value(opp)
    assert ev == (0.6 * 20000.0) + (0.4 * -10000.0)  # 8000.0

    kelly_f = l5.calculate_kelly_fraction(opp)
    assert kelly_f > 0.0
    assert kelly_f <= 1.0


def test_layer6_product_jtbd_pruning():
    l6 = Layer6_ProductCreation()
    features = [
        {"name": "core_search", "validation_score": 0.8},
        {"name": "bloated_ui", "validation_score": 0.1}
    ]
    pruned = l6.prune_unvalidated_features(features)
    assert len(pruned) == 1
    assert pruned[0]["name"] == "core_search"

    efficiency = l6.calculate_learning_efficiency(experiments_run=10, core_hypotheses_validated=7)
    assert efficiency == 0.7


def test_layer7_customer_psychology_trust():
    l7 = Layer7_CustomerUnderstanding()
    trust = l7.compute_trust_decay(initial_trust=1.0, negative_incidents=2)
    assert trust < 1.0

    prob_switch = l7.calculate_switching_probability(value_delta=10.0, switching_friction=2.0, trust=trust)
    assert prob_switch > 0.5


def test_layer8_marketing_viral_attention():
    l8 = Layer8_MarketingDynamics()
    curve = l8.simulate_viral_spread(initial_adopters=10, k_factor=0.5, cycles=3)
    assert len(curve) == 4
    assert curve[-1] > curve[0]

    pos_score = l8.compute_positioning_score({"speed": 9.0}, {"speed": 3.0})
    assert pos_score == 6.0


def test_layer9_sales_urgency_objections():
    l9 = Layer9_SalesSystems()
    urgency = l9.calculate_buying_urgency(pain_severity=8.0, time_to_consequence=1.0)
    assert urgency > 0.0

    motion_auto = l9.route_sales_motion(acv_dollars=1000.0)
    assert motion_auto == "automated_self_serve"

    motion_ent = l9.route_sales_motion(acv_dollars=50000.0)
    assert motion_ent == "field_enterprise_sales"


def test_layer10_growth_flywheel_network():
    l10 = Layer10_GrowthFlywheels()
    net_val = l10.calculate_network_effect_value(active_users=100, network_type="metcalfe")
    assert net_val == 10000.0

    should_throttle = l10.evaluate_deceleration_need(churn_rate=0.20, infrastructure_load=0.50)
    assert should_throttle is True


def test_layer11_competitive_moat_game_theory():
    l11 = Layer11_CompetitiveStrategy()
    moat = l11.calculate_moat_durability(switching_costs=0.9, network_effects=0.8, cost_advantage=0.7)
    assert moat == pytest.approx(0.8)

    response = l11.predict_competitor_response(market_share_gain=0.8, incumbent_aggression=0.9)
    assert response == "aggressive_price_war"


def test_layer12_org_design_delegation():
    l12 = Layer12_OrganizationalDesign()
    delegation = l12.recommend_delegation(decision_reversibility=0.9, decision_impact_dollars=500.0)
    assert delegation == "delegate_autonomously"

    delegation_exec = l12.recommend_delegation(decision_reversibility=0.1, decision_impact_dollars=500000.0)
    assert delegation_exec == "centralized_executive_approval"


def test_layer13_meta_learning_reflection():
    l13 = Layer13_MetaLearning()
    brier = l13.audit_decision_quality(predicted_prob=0.8, actual_outcome=True)
    assert brier == pytest.approx((0.8 - 1.0) ** 2)


def test_layer14_ai_entrepreneurship_allocation():
    l14 = Layer14_AIEntrepreneurshipOrchestration()
    opp = Opportunity(
        title="AI Automation Platform",
        domain="ai",
        win_probability=0.7,
        win_payoff=30000.0,
        loss_payoff=-10000.0
    )
    exp = l14.design_validation_experiment(opp)
    assert exp.opportunity_id == opp.opportunity_id

    alloc = l14.allocate_resources(opp, total_capital=100000.0, total_compute=1e12)
    assert alloc.capital_dollars > 0.0
    assert alloc.compute_flop_budget > 0.0


def test_computational_architecture_orchestrator_end_to_end():
    orchestrator = ComputationalArchitectureOfEntrepreneurship()
    opp = orchestrator.ingest_signal({
        "title": "Autonomous AI Agent Operating System",
        "domain": "ai_software",
        "variables": ["pricing", "user_growth", "churn"],
        "causal_edges": [("pricing", "user_growth"), ("user_growth", "churn")],
        "success_probability": 0.7,
        "win_probability": 0.7,
        "win_payoff": 100000.0,
        "loss_payoff": -20000.0
    })

    assert len(orchestrator.opportunities) == 1
    assert opp.title == "Autonomous AI Agent Operating System"

    result = orchestrator.run_full_14_layer_cycle(total_capital=200000.0, total_compute=1e14)
    assert result["status"] == "executed"
    assert result["primary_opportunity"] == "Autonomous AI Agent Operating System"
    assert result["invariants_valid"] is True
    assert "causal_intervention_state" in result
    assert result["expected_value"] > 0
    assert result["kelly_fraction"] > 0
    assert result["should_abandon"] is False
    assert len(result["pruned_features"]) == 1
    assert result["sales_motion"] == "inside_sales"
    assert "experiment_plan" in result
    assert "capital_allocation" in result
