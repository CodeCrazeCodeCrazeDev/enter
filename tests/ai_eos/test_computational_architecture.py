from __future__ import annotations
import pytest
from uuid import uuid4

from apodex.ai_eos.intelligence.computational_architecture import (
    Opportunity,
    AdvancedCausalEngine,
    ActiveInferencePlanner,
    EntrepreneurialIntelligenceOrchestrator,
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
    ComputationalArchitectureOfEntrepreneurship
)


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


def test_orchestrated_pipeline_execution() -> None:
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
    pipeline_result = orchestrator.execute_orchestrated_pipeline()

    assert pipeline_result["status"] == "executed"
    assert pipeline_result["selected_opportunity"] == "Autonomous Scientific Hardware Venture"
    assert "best_expected_free_energy" in pipeline_result
    assert pipeline_result["propagated_state"]["marketing_spend"] == 1.5


def test_layer1_reality_bounds() -> None:
    layer1 = Layer1_Reality()
    res = layer1.evaluate_reality_bounds(inputs_entropy=1.2, capital_available_cents=5000000)
    assert res["is_physically_feasible"] is True
    assert "human_psychology" in res["human_psychology_vs_optimization"]
    assert "unautomatable" in res["task_boundaries"]


def test_layer2_opportunity_discovery() -> None:
    layer2 = Layer2_OpportunityDiscovery()

    demand = {"ai_agents": 0.7, "manual_tools": 0.3}
    supply = {"ai_agents": 0.1, "manual_tools": 0.9}
    res = layer2.scan_state_space(demand, supply, snr_raw=3.0)
    assert res["is_weak_signal_detected"] is True
    assert res["kl_divergence"] > 0.3

    combined = layer2.combine_unrelated_observations(["BioTech"], ["QuantumComputing"])
    assert "BioTech x QuantumComputing" in combined

    invisible = layer2.detect_invisible_opportunity({"incumbent_myopia_score": 0.8, "info_asymmetry_index": 0.9})
    assert invisible["is_invisible_opportunity"] is True


def test_layer3_problem_discovery() -> None:
    layer3 = Layer3_ProblemDiscovery()

    causal_graph = {
        "incentive_misalignment": ["high_churn"],
        "high_churn": ["revenue_drop"]
    }
    decomp = layer3.decompose_problem(causal_graph, stated_problem="high_churn")
    assert decomp["is_root_cause"] is False
    assert "incentive_misalignment" in decomp["identified_parents_root_causes"]

    ignore_res = layer3.should_ignore_problem(evig=0.1, utility_gain=0.1, investigation_cost=1.0)
    assert ignore_res["should_ignore"] is True


def test_layer4_decision_making() -> None:
    layer4 = Layer4_DecisionMaking()

    bayes = layer4.bayesian_decision_update(
        prior_mean=0.8, prior_precision=10.0, data_mean=0.2, data_sample_count=2, data_precision=1.0
    )
    assert bayes["dominant_decision_factor"] == "intuition_dominated"

    sprt_kill = layer4.sequential_probability_ratio_test(log_likelihood_ratio=-3.0)
    assert sprt_kill["sprt_decision"] == "KILL_IDEA_QUICKLY"

    sprt_accept = layer4.sequential_probability_ratio_test(log_likelihood_ratio=3.5)
    assert sprt_accept["sprt_decision"] == "ACCEPT_IDEA"

    bias = layer4.mitigate_confirmation_bias([0.5, 0.5])
    assert bias["confirmation_bias_mitigated"] is True


def test_layer5_opportunity_evaluation() -> None:
    layer5 = Layer5_OpportunityEvaluation()

    ev = layer5.calculate_expected_value(
        tam_cents=100000000, gross_margin=0.8, success_prob=0.5, epistemic_risk=0.2, systemic_risk=0.1
    )
    assert ev > 0

    timing = layer5.evaluate_timing_real_option(volatility=2.0, first_mover_advantage=1.0)
    assert timing["timing_decision"] == "DEFER_AND_GATHER_INFO"

    abandon = layer5.check_abandonment_trigger(efe_continue=5.0, efe_pivot=1.0, switching_cost=0.5)
    assert abandon["should_abandon_or_pivot"] is True


def test_layer6_product_creation() -> None:
    layer6 = Layer6_ProductCreation()

    features = [
        {"name": "must_have", "value_score": 10.0, "complexity": 1.0},
        {"name": "bloat_v1", "value_score": 1.0, "complexity": 5.0}
    ]
    pruning = layer6.minimize_product_complexity(features, complexity_budget=2.0)
    assert "must_have" in pruning["retained_features"]
    assert "bloat_v1" in pruning["what_not_to_build"]

    jtbd = layer6.isolate_core_jtbd({"fast_speed": 0.92, "fancy_ui": 0.15})
    assert jtbd["core_jtbd"] == "fast_speed"


def test_layer7_customer_understanding() -> None:
    layer7 = Layer7_CustomerUnderstanding()

    switch = layer7.calculate_switching_probability(push_factor=3.0, pull_factor=2.0, inertia=1.0, anxiety=0.5)
    assert switch["will_customer_switch"] is True

    trust = layer7.update_trust_and_loyalty(current_trust=0.7, positive_interactions=5, failures=0)
    assert trust["is_evangelist"] is True


def test_layer8_marketing() -> None:
    layer8 = Layer8_Marketing()

    viral = layer8.model_attention_cascade(seed_audience=1000, emotional_resonance=0.9, network_degree=2.0)
    assert viral["is_viral"] is True
    assert viral["projected_reach"] > 1000

    authority = layer8.calculate_brand_authority([0.8, 0.9], [0.5, 0.5])
    assert authority == pytest.approx(0.85)


def test_layer9_sales() -> None:
    layer9 = Layer9_Sales()

    auto = layer9.evaluate_sales_automation_boundary(acv_cents=300000, stakeholder_count=1)
    assert auto["can_fully_automate"] is True

    ent = layer9.evaluate_sales_automation_boundary(acv_cents=5000000, stakeholder_count=5)
    assert ent["can_fully_automate"] is False

    urgency = layer9.create_urgency_and_resolve_objections(counterfactual_loss_cents=5000000, customer_objection_causal_gap=0.1)
    assert urgency["objection_resolved"] is True


def test_layer10_growth() -> None:
    layer10 = Layer10_Growth()

    net = layer10.evaluate_network_effects(active_users=5000, cluster_cohesion=0.9)
    assert net["is_platform_ready"] is True

    slowdown = layer10.check_intentional_slowdown(growth_rate=0.8, operational_sla_capacity=0.3)
    assert slowdown["should_slow_down_growth"] is True


def test_layer11_competition() -> None:
    layer11 = Layer11_Competition()

    moat = layer11.score_moat_durability(switching_costs=0.9, network_density=0.8, proprietary_data_scale=0.9, cost_advantage=0.7)
    assert moat["is_defensible"] is True


def test_layer12_organizational_design() -> None:
    layer12 = Layer12_OrganizationalDesign()

    hire = layer12.evaluate_hiring_trigger(shadow_price_hourly_cents=20000, market_wage_hourly_cents=12000)
    assert hire["should_hire"] is True

    coase = layer12.evaluate_coasian_boundary(internal_coordination_cost=50.0, external_transaction_cost=120.0)
    assert coase["organizational_structure"] == "CENTRALIZED_IN_HOUSE"


test_layer13_meta_learning_data = {"failure_reason": "database_deadlock", "context": "checkout"}

def test_layer13_meta_learning() -> None:
    layer13 = Layer13_MetaLearning()

    rule = layer13.convert_failure_to_reusable_rule(test_layer13_meta_learning_data)
    assert "DATABASE_DEADLOCK" in rule["compiled_reusable_rule"]

    calib = layer13.measure_decision_calibration(predicted_probs=[0.9, 0.8], actual_outcomes=[1, 1])
    assert calib["is_well_calibrated"] is True


def test_layer14_ai_entrepreneurship() -> None:
    layer14 = Layer14_AIEntrepreneurship()

    matrix = layer14.formalize_task_matrix()
    assert "causal" in matrix
    assert "human_judgment" in matrix

    efe = layer14.calculate_global_efe(enterprise_value_cents=10000000, discovery_value=2.0)
    assert isinstance(efe, float)


def test_computational_architecture_master_orchestrator() -> None:
    master = ComputationalArchitectureOfEntrepreneurship()

    raw_signal = {
        "entropy": 1.2,
        "capital_cents": 500000000,
        "demand_dist": {"quantum": 0.8, "classical": 0.2},
        "supply_dist": {"quantum": 0.1, "classical": 0.9},
        "snr": 3.5,
        "causal_graph": {"churn": ["slow_ui"]},
        "sprt_llr": 3.1,
        "tam_cents": 1000000000,
        "acv_cents": 250000
    }

    result = master.process_end_to_end_venture_cycle(raw_signal)

    assert result["status"] == "COMPLETED_14_LAYER_EXECUTION"
    assert "layer1_reality" in result
    assert "layer2_discovery" in result
    assert "layer3_problem" in result
    assert "layer4_decision" in result
    assert "layer5_ev_cents" in result
    assert "layer6_product" in result
    assert "layer7_customer" in result
    assert "layer8_marketing" in result
    assert "layer9_sales" in result
    assert "layer10_growth" in result
    assert "layer11_competition" in result
    assert "layer12_org" in result
    assert "layer13_meta" in result
    assert "layer14_global_efe" in result
