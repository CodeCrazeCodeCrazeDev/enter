from __future__ import annotations
import pytest

from apodex.ai_eos.intelligence.fourteen_layer_engine import (
    RealitySubstrateEngine,
    OpportunityDiscoveryEngine,
    ProblemDiscoveryEngine,
    DecisionMakingEngine,
    OpportunityEvaluationEngine,
    ProductCreationEngine,
    CustomerUnderstandingEngine,
    MarketingEngine,
    SalesEngine,
    GrowthEngine,
    CompetitionEngine,
    OrganizationalDesignEngine,
    MetaLearningEngine,
    FourteenLayerEntrepreneurshipOrchestrator
)


def test_layer_1_reality_substrate() -> None:
    l1 = RealitySubstrateEngine()
    res = l1.evaluate_invariants(utility_cents=20000, price_cents=10000, cost_cents=3000)
    assert res["valid"] is True
    assert res["net_customer_surplus"] == 10000
    assert res["unit_margin"] == 7000

    auto_res = l1.classify_task_automation("terminal_ethics")
    assert auto_res["automatable"] is False


def test_layer_2_opportunity_discovery() -> None:
    l2 = OpportunityDiscoveryEngine()
    kl = l2.calculate_kl_divergence([0.1, 0.9], [0.5, 0.5])
    assert kl > 0.0

    weak_signals = l2.detect_weak_signals([10.0, 10.0, 10.0, 10.0, 50.0], threshold_sigma=1.5)
    assert len(weak_signals) >= 1
    assert weak_signals[0]["value"] == 50.0

    tensor = l2.cross_synthesize_domains([1.0, 2.0], [3.0, 4.0])
    assert tensor == [[3.0, 4.0], [6.0, 8.0]]


def test_layer_3_problem_discovery() -> None:
    l3 = ProblemDiscoveryEngine()
    causal = l3.isolate_root_cause_vs_symptom(
        nodes=["marketing", "traffic", "revenue"],
        edges=[("marketing", "traffic"), ("traffic", "revenue")]
    )
    assert causal["root_causes"] == ["marketing"]
    assert "revenue" in causal["symptoms"]

    ignore = l3.evaluate_ignore_criteria(evig=10.0, delta_utility=5.0, cost_investigate=50.0)
    assert ignore is True


def test_layer_4_decision_making() -> None:
    l4 = DecisionMakingEngine()
    post_mean = l4.update_bayesian_belief(prior_mean=0.5, likelihood_sample=1.0)
    assert post_mean > 0.5

    sprt = l4.evaluate_sprt_termination(3.5)
    assert sprt == "ACCEPT_HYPOTHESIS"

    entropy = l4.calculate_shannon_entropy([0.5, 0.5])
    assert pytest.approx(entropy, 0.01) == 0.693


def test_layer_5_opportunity_evaluation() -> None:
    l5 = OpportunityEvaluationEngine()
    ev = l5.calculate_expected_value(tam_cents=100000000, margin_pct=0.8, ltv_cac=4.0)
    assert ev > 0.0

    defer = l5.evaluate_real_option_deferral(option_value=100.0, first_mover_advantage=50.0)
    assert defer == "DEFER_INVESTMENT"

    pivot = l5.check_pivot_trigger(efe_continue=10.0, efe_pivot=2.0, switching_cost=3.0)
    assert pivot is True


def test_layer_6_product_creation() -> None:
    l6 = ProductCreationEngine()
    penalty = l6.apply_complexity_penalty(feature_count=10)
    assert penalty > 0.0

    eff = l6.calculate_epistemic_probe_efficiency(entropy_reduction=1.5, development_cost_dollars=1000.0)
    assert eff == 0.0015


def test_layer_7_customer_understanding() -> None:
    l7 = CustomerUnderstandingEngine()
    prob = l7.calculate_switching_probability(push=1.0, pull=1.0, inertia=0.2, anxiety=0.2)
    assert prob > 0.8

    trust = l7.update_trust_vector(current_trust=0.5, fulfillment_quality=1.0)
    assert trust == pytest.approx(0.6)


def test_layer_8_marketing() -> None:
    l8 = MarketingEngine()
    cascade = l8.model_attention_cascade(initial_infected=0.01, virality_coeff=0.5, time_steps=3)
    assert len(cascade) == 4
    assert cascade[-1] > cascade[0]

    proj = l8.project_positioning_vector(feature_vector=[1.0, 2.0], cognitive_projection_matrix=[[0.5, 0.5]])
    assert proj == [1.5]


def test_layer_9_sales() -> None:
    l9 = SalesEngine()
    urgency = l9.calculate_counterfactual_urgency(expected_loss_status_quo=10000.0, solution_cost=2000.0)
    assert urgency == 8000.0

    route = l9.determine_automation_boundary(acv_dollars=2000.0, stakeholder_count=1)
    assert route == "AUTOMATED_SELF_SERVE_FUNNEL"


def test_layer_10_growth() -> None:
    l10 = GrowthEngine()
    util = l10.calculate_metcalfe_utility(user_count=100)
    assert util == 1000.0

    throttle = l10.check_growth_throttle_trigger(acquisition_rate=150.0, capacity_limit=100.0)
    assert throttle is True


def test_layer_11_competition() -> None:
    l11 = CompetitionEngine()
    payoff = l11.compute_minimax_payoff([[10.0, 2.0], [4.0, 6.0]])
    assert payoff == 4.0

    pivot = l11.evaluate_margin_pivot(ltv_cac_ratio=1.2)
    assert pivot is True


def test_layer_12_organizational_design() -> None:
    l12 = OrganizationalDesignEngine()
    hire = l12.calculate_shadow_price_hiring_trigger(marginal_utility_per_hour=150.0, market_hourly_wage=100.0)
    assert hire["trigger_hire"] is True

    boundary = l12.evaluate_coasian_boundary(internal_coord_cost=50.0, market_trans_cost=100.0)
    assert boundary == "CENTRALIZED_IN_HOUSE"


def test_layer_13_meta_learning() -> None:
    l13 = MetaLearningEngine()
    post_mortem = l13.mine_failure_post_mortem({"root_cause": "churn_spike", "id": "exp_42"})
    assert "CHURN_SPIKE" in post_mortem["extracted_safety_constraint"]


def test_layer_14_orchestrator_pipeline() -> None:
    orchestrator = FourteenLayerEntrepreneurshipOrchestrator()
    signal = {
        "title": "Autonomous Hardware Enterprise",
        "domain": "robotics",
        "tam_cents": 500000000,
        "price_cents": 20000,
        "cost_cents": 5000,
        "customer_utility_cents": 50000
    }
    result = orchestrator.run_full_14_layer_pipeline(signal)
    assert result["status"] == "SUCCESS"
    assert result["opportunity_title"] == "Autonomous Hardware Enterprise"
    assert result["layer_1_invariants_valid"] is True
    assert "layer_13_safety_constraint" in result
