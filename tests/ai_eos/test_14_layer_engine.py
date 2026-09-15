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
    FourteenLayerEntrepreneurialEngine,
    EnterpriseState
)


def test_layer_1_reality_substrate() -> None:
    engine = RealitySubstrateEngine()
    eff = engine.calculate_thermodynamic_efficiency(1_000_000.0, 0.5)
    assert eff == 0.5

    boundary = engine.delineate_automation_boundary("ultimate_human_value", True)
    assert boundary["automatable"] is False
    assert boundary["action"] == "defer_to_human_arbitration"

    opt_boundary = engine.delineate_automation_boundary("causal_optimization", False)
    assert opt_boundary["automatable"] is True


def test_layer_2_opportunity_discovery() -> None:
    engine = OpportunityDiscoveryEngine()
    signals = [{"title": "s1", "value": 1.0}, {"title": "s2", "value": 1.1}, {"title": "anomaly", "value": 10.0}]
    anomalies = engine.detect_weak_signals(signals, z_score_threshold=1.2)
    assert len(anomalies) >= 1
    assert anomalies[0]["title"] == "anomaly"

    kl_gap = engine.calculate_kl_divergence_gap([0.1, 0.9], [0.8, 0.2])
    assert kl_gap > 0.0

    syntheses = engine.generate_novel_conceptual_synthesis(["AI"], ["Robotics"])
    assert len(syntheses) == 1
    assert "AI x Robotics" in syntheses[0]["title"]


def test_layer_3_problem_discovery() -> None:
    engine = ProblemDiscoveryEngine()
    scm = engine.decompose_problem_scm(
        variables=["root_cause", "mid_var", "symptom"],
        edges=[("root_cause", "mid_var"), ("mid_var", "symptom")]
    )
    assert "root_cause" in scm["root_causes"]
    assert "symptom" in scm["symptoms"]

    should_ignore = engine.evaluate_ignore_criteria(evig=0.1, expected_utility_gain=0.2, investigation_cost=1.0)
    assert should_ignore is True


def test_layer_4_decision_making() -> None:
    engine = DecisionMakingEngine()
    efe = engine.compute_expected_free_energy(p_success=0.8, p_target=0.9, prior_entropy=1.5, post_entropy=0.5)
    assert isinstance(efe, float)

    sprt_res = engine.sequential_probability_ratio_test([False, False, False, False, False])
    assert sprt_res == "KILL_IDEA_QUICKLY"


def test_layer_5_opportunity_evaluation() -> None:
    engine = OpportunityEvaluationEngine()
    ev_cents = engine.calculate_expected_value(tam_cents=10_000_000_00, gross_margin=0.8, success_probability=0.5, risk_discount=0.1)
    assert ev_cents == 3_600_000_00

    timing = engine.evaluate_real_option_timing(volatility=0.8, time_horizon_years=2.0, first_mover_advantage=0.2)
    assert timing == "DEFER_AND_GATHER_INFORMATION"

    should_abandon = engine.check_abandonment_threshold(efe_continue=5.0, efe_pivot=1.0, switching_cost=1.0)
    assert should_abandon is True


def test_layer_6_product_creation() -> None:
    engine = ProductCreationEngine()
    selected = engine.apply_kolmogorov_complexity_penalty(
        proposed_features=["f1", "extremely_long_complex_unnecessary_feature_name"],
        feature_utilities={"f1": 0.9, "extremely_long_complex_unnecessary_feature_name": 0.2},
        lambda_reg=0.05
    )
    assert "f1" in selected


def test_layer_7_customer_understanding() -> None:
    engine = CustomerUnderstandingEngine()
    p_switch = engine.calculate_switching_probability(push_force=1.5, pull_force=1.0, inertia=0.2, anxiety=0.3)
    assert p_switch > 0.8


def test_layer_8_marketing() -> None:
    engine = MarketingEngine()
    reach = engine.simulate_information_cascade(initial_seeds=50, virality_coefficient=1.2, network_decay=0.1)
    assert reach > 50


def test_layer_9_sales() -> None:
    engine = SalesEngine()
    strat_self = engine.determine_sales_strategy(annual_contract_value_cents=2000_00, stakeholder_complexity_score=0.1)
    assert strat_self == "AUTOMATED_SELF_SERVE_FUNNEL"

    strat_ent = engine.determine_sales_strategy(annual_contract_value_cents=50000_00, stakeholder_complexity_score=0.8)
    assert strat_ent == "HIGH_TOUCH_ENTERPRISE_SALES"


def test_layer_10_growth() -> None:
    engine = GrowthEngine()
    val = engine.compute_subquadratic_network_value(1000)
    assert val > 1000.0

    slowdown = engine.check_intentional_slowdown(growth_rate=2.0, operational_throughput_capacity=1.0)
    assert slowdown is True


def test_layer_11_competition() -> None:
    engine = CompetitionEngine()
    moat = engine.score_moat_durability(switching_costs=0.8, network_density=0.9, cost_advantage=0.7)
    assert 0.0 <= moat <= 1.0


def test_layer_12_organizational_design() -> None:
    engine = OrganizationalDesignEngine()
    hire = engine.evaluate_hiring_trigger(shadow_price_constraint=200.0, market_wage=150.0)
    assert hire is True

    coase = engine.evaluate_coasian_boundary(internal_coordination_cost=50.0, external_transaction_cost=100.0)
    assert coase == "CENTRALIZED_IN_HOUSE"


def test_layer_13_meta_learning() -> None:
    engine = MetaLearningEngine()
    res = engine.execute_triple_loop_learning(execution_errors=[{"severity": 0.9, "err": "failed_gtm"}])
    assert res["status"] == "learning_applied"
    assert res["loop_3_code_rewrites"] == 1


def test_layer_14_fourteen_layer_master_engine() -> None:
    master_engine = FourteenLayerEntrepreneurialEngine()
    signals = [{"title": "sig1", "value": 1.0}, {"title": "sig2", "value": 2.0}, {"title": "sig3", "value": 15.0}]

    result = master_engine.run_full_14_layer_cycle(signals)

    assert result["status"] == "success"
    assert result["layers_executed"] == 14
    assert "expected_free_energy" in result
    assert "moat_durability_score" in result
    assert len(master_engine.state.execution_history) == 1
