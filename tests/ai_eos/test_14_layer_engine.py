from __future__ import annotations
import math
import pytest

from apodex.ai_eos.intelligence.fourteen_layer_engine import (
    Layer1_Reality,
    Layer2_OpportunityDiscovery,
    Layer3_ProblemDiscovery,
    Layer4_DecisionMaking,
    Layer5_OpportunityEvaluation,
    Layer6_ProductCreation,
    Layer7_CustomerUnderstanding,
    Layer8_Marketing,
    Layer9_Sales,
    Layer10_Growth,
    Layer11_Competition,
    Layer12_OrganizationalDesign,
    Layer13_MetaLearning,
    Layer14_AIEntrepreneurship,
    FourteenLayerEngine
)


def test_layer1_reality_substrate() -> None:
    l1 = Layer1_Reality()
    bounds = l1.evaluate_thermodynamic_bounds(capital_budget_cents=1000000, time_horizon_days=10.0)
    assert bounds["viable"] is True
    assert bounds["max_burn_per_day_cents"] == 100000.0

    task_h = l1.classify_task_automation("terminal_value_alignment", involves_human_terminal_value=True, involves_causal_optimization=False)
    assert task_h["automation_status"] == "HUMAN_ARBITRATED"

    task_a = l1.classify_task_automation("causal_inference", involves_human_terminal_value=False, involves_causal_optimization=True)
    assert task_a["automation_status"] == "FULLY_AUTOMATABLE"

    invariants = l1.get_invariant_principles()
    assert len(invariants) == 4


def test_layer2_opportunity_discovery() -> None:
    l2 = Layer2_OpportunityDiscovery()
    signal_stream = [
        {"title": "Noise Signal", "variance": 0.1, "frequency_hz": 1.0},
        {"title": "Weak Anomaly", "variance": 5.0, "frequency_hz": 0.01}
    ]
    detected = l2.scan_weak_signals(signal_stream, anomaly_threshold=2.0)
    assert len(detected) == 1
    assert detected[0]["title"] == "Weak Anomaly"

    fused = l2.fuse_unrelated_observations(
        {"title": "AI Bio", "domain": "bio", "variables": ["dna"], "tam_cents": 50000},
        {"title": "Robotics", "domain": "robotics", "variables": ["servo"], "tam_cents": 70000}
    )
    assert fused["title"] == "AI Bio x Robotics"
    assert "dna" in fused["variables"] and "servo" in fused["variables"]

    invisible = l2.detect_invisible_opportunity({"supply_demand_kl_div": 1.5})
    assert invisible["opportunity_detected"] is True


def test_layer3_problem_discovery() -> None:
    l3 = Layer3_ProblemDiscovery()
    dag = l3.define_problem_dag(["root_cause", "symptom"], [("root_cause", "symptom")])
    assert len(dag.variables) == 2

    root_eval = l3.distinguish_root_cause_from_symptoms(dag, "root_cause")
    assert root_eval["classification"] == "ROOT_CAUSE"

    symptom_eval = l3.distinguish_root_cause_from_symptoms(dag, "symptom")
    assert symptom_eval["classification"] == "DOWNSTREAM_SYMPTOM"

    # Test Ignore Criteria: EVIG (1.0) + Delta_U (2.0) = 3.0 < Cost (5.0) -> True (Ignore)
    assert l3.should_ignore_problem(evig=1.0, delta_utility=2.0, investigation_cost=5.0) is True


def test_layer4_decision_making() -> None:
    l4 = Layer4_DecisionMaking()
    efe = l4.calculate_expected_free_energy(
        success_prob=0.8,
        target_pref=0.9,
        prior_entropy=2.0,
        post_entropy=0.5,
        curiosity_weight=1.0
    )
    assert isinstance(efe, float)

    post_mean, post_prec = l4.bayesian_conjugate_update(
        intuition_prior_mean=0.5,
        intuition_prior_precision=2.0,
        data_likelihood_mean=0.9,
        data_sample_size=10
    )
    assert post_mean > 0.5
    assert post_prec == 12.0

    assert l4.sprt_fast_kill_check(-4.0) == "KILL"
    assert l4.sprt_fast_kill_check(4.0) == "VALIDATED"
    assert l4.sprt_fast_kill_check(0.0) == "KEEP_TESTING"

    beliefs = {"market_size": 1.0}
    stressed = l4.negative_bias_belief_search(beliefs)
    assert stressed["market_size"] < 1.0


def test_layer5_opportunity_evaluation() -> None:
    l5 = Layer5_OpportunityEvaluation()
    unit_econ = l5.calculate_unit_economics(tam_cents=100000000, ltv_cents=1000, cac_cents=200, gross_margin=0.8)
    assert unit_econ["viable"] is True
    assert unit_econ["ltv_cac_ratio"] == 5.0

    opt_val = l5.price_real_option_jump_diffusion(base_value=100.0, volatility=0.2, jump_intensity=0.1, time_to_expiry=1.0)
    assert opt_val > 100.0

    assert l5.evaluate_abandonment_trigger(efe_continue=10.0, efe_pivot=2.0, switching_cost=3.0) is True


def test_layer6_product_creation() -> None:
    l6 = Layer6_ProductCreation()
    features = l6.minimize_product_complexity(["f1_long_name", "f2"], {"f1_long_name": 0.2, "f2": 0.9}, complexity_penalty_weight=0.05)
    assert "f2" in features

    jtbd = l6.extract_jtbd_factors([{"type": "functional"}, {"type": "functional"}, {"type": "emotional"}])
    assert pytest.approx(jtbd["functional_weight"]) == 2.0 / 3.0

    probe = l6.design_active_learning_probe("Split CTA Test")
    assert probe["probe_type"] == "A/B_SPLIT_PROBE"


def test_layer7_customer_understanding() -> None:
    l7 = Layer7_CustomerUnderstanding()
    fe = l7.model_customer_free_energy(perceived_friction=0.5, financial_cost=0.5, social_risk=0.5)
    assert pytest.approx(fe) == 0.5

    p_switch = l7.calculate_switching_probability(push=2.0, pull=2.0, inertia=1.0, anxiety=1.0)
    assert p_switch > 0.5

    trust_lowered = l7.update_customer_trust(current_trust=0.8, product_failure_event=True, failure_severity=0.3)
    assert pytest.approx(trust_lowered) == 0.5


def test_layer8_marketing() -> None:
    l8 = Layer8_Marketing()
    cascade = l8.simulate_scale_free_attention(network_nodes=1000, viral_coefficient=2.0, decay_rate=0.1, steps=3)
    assert len(cascade) == 3
    assert cascade[-1] > cascade[0]

    pos = l8.calculate_cognitive_positioning([1.0, 0.0], [1.0, 0.0])
    assert pytest.approx(pos) == 1.0

    adj = [[0, 1], [1, 0]]
    pr = l8.compute_domain_pagerank_authority(adj)
    assert len(pr) == 2


def test_layer9_sales() -> None:
    l9 = Layer9_Sales()
    urgency = l9.calculate_counterfactual_loss_urgency(delay_cost_per_day=100.0, action_cost=1000.0, urgency_days=30)
    assert urgency == 3.0

    resolved = l9.resolve_structural_causal_objection("pricing", {})
    assert "pricing" in resolved["objection"]

    assert l9.determine_sales_channel_boundary(acv_cents=200000, decision_complexity=0.2) == "AUTOMATED_SELF_SERVE"
    assert l9.determine_sales_channel_boundary(acv_cents=1000000, decision_complexity=0.8) == "ENTERPRISE_HIGH_TOUCH"


def test_layer10_growth() -> None:
    l10 = Layer10_Growth()
    val = l10.calculate_zipf_network_value(user_count=100)
    assert val > 100.0

    assert l10.should_transition_to_platform(marginal_integration_cost=10.0, marginal_ecosystem_utility=50.0) is True

    throttle = l10.check_growth_safety_throttle(growth_rate=0.5, support_capacity_throughput=0.2)
    assert throttle["is_safe"] is False
    assert throttle["action"] == "THROTTLE_GROWTH"


def test_layer11_competition() -> None:
    l11 = Layer11_Competition()
    moat = l11.evaluate_moat_durability(switching_costs=0.9, network_effect_strength=0.9, proprietary_data_advantage=0.9)
    assert moat > 0.8

    reaction = l11.anticipate_competitor_reaction("price_drop", {"price_match": 10.0, "ignore": 2.0})
    assert "price_match" in reaction

    assert l11.check_pivot_trigger_under_density(competitor_density=15, margin_compression_rate=0.3) is True


def test_layer12_organizational_design() -> None:
    l12 = Layer12_OrganizationalDesign()
    assert l12.evaluate_hiring_lagrange_trigger(shadow_price_hourly=150.0, market_wage_hourly=100.0) is True

    boundary = l12.determine_coasian_boundary(internal_coordination_cost=50.0, external_transaction_cost=100.0)
    assert boundary == "CENTRALIZED_INTERNAL"

    tree = l12.build_scalable_decision_tree(nodes_count=50)
    assert tree["hierarchy_depth"] >= 2


def test_layer13_meta_learning() -> None:
    l13 = Layer13_MetaLearning()
    telemetry = l13.triple_loop_learning_update({"error_rate": 0.35})
    assert telemetry["loop_3_code_evolution_triggered"] is True

    weights = {"w1": 1.0}
    updated = l13.backpropagate_operational_error(prediction_error=2.0, world_model_weights=weights)
    assert updated["w1"] < 1.0

    emg_rule = l13.convert_failure_to_emg_rule({"failure_cause": "out_of_memory"})
    assert "out_of_memory" in emg_rule["condition"]


def test_layer14_master_engine_orchestration() -> None:
    engine = FourteenLayerEngine()

    catalog = ["ethics_review", "causal_symptom_check", "copywriting"]
    matrix = engine.formalize_task_matrix(catalog)
    assert matrix["ethics_review"] == "HUMAN_JUDGMENT"
    assert matrix["causal_symptom_check"] == "CAUSAL_INFERENCE"

    opps = [
        {"title": "OppA", "success_probability": 0.8, "prior_entropy": 2.0, "post_entropy": 0.5},
        {"title": "OppB", "success_probability": 0.4, "prior_entropy": 0.8, "post_entropy": 0.7}
    ]
    capital = engine.allocate_capital_gittins_bandit(opps, total_capital_cents=1000000)
    assert capital["OppA"] > capital["OppB"]

    result = engine.execute_complete_14_layer_pipeline(
        input_signal={"title": "Autonomous Venture", "variables": ["price", "demand"], "tam_cents": 500000000},
        capital_cents=100000000
    )
    assert result["status"] == "SUCCESS"
    assert "layer1_bounds" in result
    assert "layer14_capital_allocation" in result
