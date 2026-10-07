"""Unit and integration tests for the 14-Layer Computational Architecture Engine."""

import pytest
from apodex.ai_eos.intelligence.fourteen_layer_engine import (
    RealitySubstrateEngine,
    StateSpaceOpportunityDiscoveryEngine,
    StructuralProblemDecomposer,
    ActiveInferenceDecisionEngine,
    OpportunityEvaluationEngine,
    MinimumComplexityProductEngine,
    CustomerPsychologyModeler,
    MarketFormationEngine,
    SalesPsychologyEngine,
    CompoundingGrowthEngine,
    CompetitiveMoatEngine,
    OrganizationalScalingEngine,
    MetaLearningEngine,
    FourteenLayerOrchestrator,
)


def test_layer_1_reality_substrate():
    engine = RealitySubstrateEngine()
    runway = engine.evaluate_thermodynamic_runway(revenue_cents=2000, burn_cents=10000, cash_reserve_cents=80000)
    assert runway["net_burn_cents"] == 8000
    assert runway["runway_months"] == 10.0
    assert runway["is_surviving"] is True

    auto_res = engine.classify_task_automation("data_processing")
    assert auto_res["is_automatable"] is True
    assert auto_res["execution_mode"] == "autonomous_agent"

    human_res = engine.classify_task_automation("ethical_alignment")
    assert human_res["is_automatable"] is False
    assert human_res["execution_mode"] == "human_in_the_loop"


def test_layer_2_opportunity_discovery():
    engine = StateSpaceOpportunityDiscoveryEngine()
    demand = {"ai_tools": 0.8, "manual_ops": 0.2}
    supply = {"ai_tools": 0.3, "manual_ops": 0.7}
    kl_div = engine.calculate_kl_divergence(demand, supply)
    assert kl_div > 0.0

    signals = [
        {"title": "s1", "value": 10.0},
        {"title": "s2", "value": 10.0},
        {"title": "s3", "value": 10.0},
        {"title": "s4", "value": 10.0},
        {"title": "s5", "value": 10.0},
        {"title": "anomaly", "value": 100.0},
    ]
    weak_signals = engine.detect_weak_signals(signals, z_threshold=1.5)
    assert len(weak_signals) == 1
    assert weak_signals[0]["title"] == "anomaly"

    tensor = engine.synthesize_cross_domain_tensor([1.0, 2.0], [3.0, 4.0])
    assert tensor == [3.0, 4.0, 6.0, 8.0]


def test_layer_3_problem_decomposition():
    engine = StructuralProblemDecomposer()
    vars_list = ["cause_a", "symptom_b", "symptom_c"]
    edges = [("cause_a", "symptom_b"), ("symptom_b", "symptom_c")]
    decomp = engine.decompose_causal_graph(vars_list, edges)
    assert decomp["root_causes"] == ["cause_a"]
    assert "symptom_b" in decomp["symptoms"]

    should_ignore = engine.evaluate_evig_ignore_threshold(evig=0.1, utility_delta=0.2, investigation_cost=1.0)
    assert should_ignore is True


def test_layer_4_decision_making():
    engine = ActiveInferenceDecisionEngine()
    mean, std = engine.bayesian_prior_likelihood_update(prior_mean=0.5, prior_std=0.2, obs_mean=0.9, obs_std=0.1, n_samples=10)
    assert mean > 0.5  # Updated towards observed mean
    assert std < 0.2   # Uncertainty reduced

    action = engine.evaluate_sprt_termination([1.0, 1.5, 0.5])
    assert action == "ACCEPT_HYPOTHESIS"

    term_action = engine.evaluate_sprt_termination([-1.0, -1.5, -0.5])
    assert term_action == "TERMINATE_HYPOTHESIS"


def test_layer_5_opportunity_evaluation():
    engine = OpportunityEvaluationEngine()
    efe = engine.calculate_expected_free_energy(
        success_probability=0.7, target_preference=0.9, prior_entropy=1.5, post_entropy=0.5
    )
    assert isinstance(efe, float)

    timing = engine.evaluate_real_options_timing(opportunity_val=100.0, volatility=0.8, waiting_cost=10.0)
    assert timing in ["DEFER_INVESTMENT", "DEPLOY_IMMEDIATELY"]


def test_layer_6_product_creation():
    engine = MinimumComplexityProductEngine()
    features = [
        {"name": "f1", "utility": 0.9, "complexity": 0.2},
        {"name": "f2", "utility": 0.1, "complexity": 2.0},
    ]
    retained = engine.minimize_product_complexity(features, complexity_penalty=0.5)
    assert len(retained) == 1
    assert retained[0]["name"] == "f1"

    jtbd = engine.extract_core_jtbd_factors([{"action": "speed", "frequency": 10, "satisfaction_gap": 0.8}])
    assert "speed" in jtbd


def test_layer_7_customer_psychology():
    engine = CustomerPsychologyModeler()
    p_switch = engine.calculate_switching_probability(push=2.0, pull=2.0, inertia=0.5, anxiety=0.5)
    assert p_switch > 0.9

    trust = engine.update_trust_state_vector(current_trust=0.5, execution_success=True)
    assert trust > 0.5


def test_layer_8_market_formation():
    engine = MarketFormationEngine()
    cascade = engine.simulate_attention_cascade(initial_nodes=10, transmission_rate=0.5, network_decay=0.1, steps=3)
    assert len(cascade) == 4
    assert cascade[-1] > cascade[0]

    ranks = engine.calculate_brand_authority_pagerank(["brand_a", "brand_b"], {"brand_a": ["brand_b"]})
    assert "brand_a" in ranks and "brand_b" in ranks


def test_layer_9_sales_psychology():
    engine = SalesPsychologyEngine()
    loss = engine.calculate_counterfactual_loss_of_inaction(daily_cost_of_delay_cents=10000, delay_days=30)
    assert loss == 300000

    mode = engine.determine_sales_automation_mode(acv_cents=1000_00, decision_complexity="low")
    assert mode == "AUTOMATED_SELF_SERVE_FUNNEL"

    ent_mode = engine.determine_sales_automation_mode(acv_cents=60000_00, decision_complexity="high")
    assert ent_mode == "ENTERPRISE_HIGH_TOUCH_SALES"


def test_layer_10_growth():
    engine = CompoundingGrowthEngine()
    val = engine.calculate_subquadratic_network_value(user_count=1000)
    assert val > 1000.0

    risk = engine.check_capacity_blowout_risk(growth_rate=0.8, operational_capacity=0.3)
    assert risk is True


def test_layer_11_competition():
    engine = CompetitiveMoatEngine()
    moat = engine.calculate_moat_durability_score(0.8, 0.7, 0.9, 0.6)
    assert 0.0 <= moat <= 1.0

    pivot = engine.check_pivot_trigger(gross_margin=0.15)
    assert pivot is True


def test_layer_12_org_scaling():
    engine = OrganizationalScalingEngine()
    hire = engine.evaluate_lagrange_hiring_trigger(resource_shadow_price=150.0, market_wage=100.0)
    assert hire is True

    mode = engine.evaluate_coasian_boundary(internal_coordination_cost=30.0, external_transaction_cost=80.0)
    assert mode == "CENTRALIZED_IN_HOUSE"


def test_layer_13_meta_learning():
    engine = MetaLearningEngine()
    backprop = engine.execute_triple_loop_backpropagation([0.35, 0.40])
    assert backprop["triple_loop_rewrite_code"] is True

    rules = engine.compile_post_mortem_heuristics([{"failure_reason": "cash_exhaustion"}])
    assert "SAFETY_RULE_PREVENT_CASH_EXHAUSTION" in rules


def test_layer_14_orchestrator_integration():
    orchestrator = FourteenLayerOrchestrator()
    signal = {
        "title": "Quantum AI Cloud Service",
        "variables": ["pricing", "latency", "conversion"],
        "causal_edges": [("pricing", "conversion"), ("latency", "conversion")],
        "success_probability": 0.65,
        "tam_cents": 1000000_00
    }
    result = orchestrator.ingest_and_orchestrate(signal, budget_cents=500000_00)
    assert result["status"] == "orchestrated"
    assert result["layer_1_runway"]["is_surviving"] is True
    assert result["layer_2_anomalies_detected"] == 1
    assert "pricing" in result["layer_3_root_causes"] or "latency" in result["layer_3_root_causes"]
    assert "layer_4_5_calculated_efe" in result
    assert result["layer_11_moat_score"] > 0.0
    assert result["layer_12_delegation_mode"] == "CENTRALIZED_IN_HOUSE"
