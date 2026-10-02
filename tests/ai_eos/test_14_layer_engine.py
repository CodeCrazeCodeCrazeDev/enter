"""
Unit and integration test suite for the 14-Layer Computational Architecture Engine.
"""

from __future__ import annotations
import pytest
from apodex.ai_eos.intelligence import (
    OpportunityState,
    Layer1Reality,
    Layer2OpportunityDiscovery,
    Layer3ProblemDiscovery,
    Layer4DecisionMaking,
    Layer5OpportunityEvaluation,
    Layer6ProductCreation,
    Layer7CustomerUnderstanding,
    Layer8Marketing,
    Layer9Sales,
    Layer10Growth,
    Layer11Competition,
    Layer12OrganizationalDesign,
    Layer13MetaLearning,
    Layer14AIEntrepreneurship,
    FourteenLayerOrchestrator
)


def test_layer1_reality() -> None:
    l1 = Layer1Reality()
    invariants = l1.evaluate_fundamental_invariants()
    assert "active_inference" in invariants
    assert l1.classify_task_domain("Build customer relationship trust") == "HUMAN_PSYCHOLOGY"
    assert l1.classify_task_domain("Unit economics CAC optimization") == "OPTIMIZATION_PROBLEM"
    assert not l1.is_automatable("ultimate_goal_setting")
    assert l1.is_automatable("market_signal_scanning")


def test_layer2_opportunity_discovery() -> None:
    l2 = Layer2OpportunityDiscovery(min_tam_cents=10_000_000)
    surprise = l2.detect_weak_signal([0.1, 0.5, 0.9, 0.2])
    assert surprise > 0.0

    opp = OpportunityState(title="Small Niche", domain="test", tam_cents=5_000_000)
    assert not l2.filter_signal(opp)

    fused = l2.combine_unrelated_observations(["robotics"], ["biotech"])
    assert "robotics_biotech_fusion" in fused

    emerging = l2.predict_emerging_market([10.0, 25.0, 50.0])
    assert emerging["is_emerging"] is True


def test_layer3_problem_discovery() -> None:
    l3 = Layer3ProblemDiscovery()
    delta = l3.define_problem_graph({"cost": 100.0}, {"cost": 20.0})
    assert delta["cost"] == -80.0

    nodes = l3.decompose_problem("root", [("root", "sub1"), ("sub1", "sub2")])
    assert nodes["root"].is_first_order is True
    assert nodes["sub1"].is_first_order is False

    is_root = l3.classify_root_cause_do_calculus("node_a", {("node_a", "node_b"): 1.5})
    assert is_root is True


def test_layer4_decision_making() -> None:
    l4 = Layer4DecisionMaking(curiosity_weight=2.0)
    opp = OpportunityState(
        title="High Curiosity Venture",
        domain="deeptech",
        prior_entropy=2.0,
        post_entropy_simulated=0.5,
        success_probability=0.6,
        target_preference=0.9
    )
    efe = l4.calculate_expected_free_energy(opp)
    assert efe < 0.0  # High epistemic gain produces negative EFE

    should_kill = l4.evaluate_sprt_fast_kill(success_observations=1, total_trials=10)
    assert should_kill is True

    debiased = l4.debias_adversarial_red_team(proposal_confidence=0.8, red_team_critique_score=0.6)
    assert debiased == pytest.approx(0.56)


def test_layer5_opportunity_evaluation() -> None:
    l5 = Layer5OpportunityEvaluation()
    opp = OpportunityState(title="EV Test", domain="tech", tam_cents=100_000_000, gross_margin=0.80, success_probability=0.5)
    ev = l5.calculate_expected_value_cents(opp, capital_at_risk_cents=1_000_000)
    # 0.5 * (100M * 0.8 * 0.05) - 0.5 * 1M = 0.5 * 4M - 0.5M = 1.5M
    assert ev == 1_500_000

    should_switch = l5.evaluate_abandonment_rule(current_opp_efe=-0.2, new_opp_efe=-1.0, switching_cost=0.3)
    assert should_switch is True


def test_layer6_product_creation() -> None:
    l6 = Layer6ProductCreation()
    features = {"core_engine": 0.9, "bloat_ui": 0.2}
    matrix = l6.generate_mvp_feature_exclusion_matrix(features, threshold=0.5)
    assert matrix["core_engine"] is True
    assert matrix["bloat_ui"] is False

    utility = l6.calculate_regularized_product_utility(raw_utility=10.0, code_lines=5000, lambda_complexity=0.0001)
    assert utility == pytest.approx(9.5)


def test_layer7_customer_understanding() -> None:
    l7 = Layer7CustomerUnderstanding()
    u = l7.calculate_customer_utility(perceived_value=100.0, price=20.0, friction=10.0)
    assert u == 70.0

    should_switch = l7.evaluate_switching_condition(new_utility=80.0, current_utility=40.0, switching_cost=30.0)
    assert should_switch is True


def test_layer8_marketing() -> None:
    l8 = Layer8Marketing()
    r0 = l8.calculate_viral_reproduction_number(sharing_prob=0.3, avg_contacts=10, payload_retention=0.5)
    assert r0 == 1.5
    assert l8.is_viral(r0) is True


def test_layer9_sales() -> None:
    l9 = Layer9Sales()
    coi = l9.calculate_cost_of_inaction_cents(daily_loss_cents=1_000_00, days_delayed=30)
    assert coi == 30_000_00

    route = l9.select_sales_channel_route(acv_cents=10_000_00, requires_compliance=True)
    assert route == "ENTERPRISE_HIGH_TOUCH"


def test_layer10_growth() -> None:
    l10 = Layer10Growth()
    utility = l10.calculate_metcalfe_network_utility(active_nodes=100)
    assert utility == pytest.approx(100.0)

    should_transition = l10.evaluate_platform_transition_trigger(third_party_ecosystem_value=500.0, internal_product_value=200.0)
    assert should_transition is True


def test_layer11_competition() -> None:
    l11 = Layer11Competition()
    moat = l11.calculate_moat_depth_index(network_effects=0.8, switching_costs=0.9, scale_economies=0.7, brand_authority=0.6)
    assert 0.0 <= moat <= 1.0

    should_pivot = l11.evaluate_pivot_trigger(iterations_failed=6, zero_conversion_duration_days=30)
    assert should_pivot is True


def test_layer12_organizational_design() -> None:
    l12 = Layer12OrganizationalDesign()
    should_hire = l12.evaluate_hiring_trigger(resource_shadow_price=200.0, marginal_wage_cost=150.0)
    assert should_hire is True

    alloc = l12.allocate_organizational_task("CAPITAL_ALLOCATION")
    assert alloc == "CENTRAL_EXECUTIVE_POD"


def test_layer13_meta_learning() -> None:
    l13 = Layer13MetaLearning()
    updated = l13.update_mental_model_priors(prior_model_confidence=0.5, ex_post_venture_roi=2.0)
    assert updated > 0.5

    archived = l13.archive_falsified_hypothesis("hyp_123", [("a", "b")], "Zero conversion")
    assert archived["status"] == "ARCHIVED_INVARIANT_FAILURE"


def test_layer14_ai_entrepreneurship() -> None:
    l14 = Layer14AIEntrepreneurship()
    ctype = l14.classify_task_capability_type("Execute root cause do calculus intervention")
    assert ctype == "CAUSAL"

    res = l14.optimize_resource_allocation(
        capital_cents=100_000_00,
        compute_flops=1e12,
        time_hours=100.0,
        talent_agents=10,
        shadow_prices={"capital": 0.8, "compute": 0.9}
    )
    assert res["allocated_capital_cents"] == 80_000_00


def test_fourteen_layer_orchestrator_integration() -> None:
    orchestrator = FourteenLayerOrchestrator()
    opp = orchestrator.ingest_signal_and_discover(
        title="Autonomous AI Operating System Venture",
        domain="ai_infrastructure",
        stream_embedding=[0.9, 0.4, 0.7, 0.8],
        tam_cents=200_000_000
    )
    assert opp is not None

    results = orchestrator.run_full_14_layer_pipeline(opp)
    assert results["status"] == "COMPLETED_14_LAYER_ORCHESTRATION"
    assert results["opportunity_title"] == "Autonomous AI Operating System Venture"
    assert results["layer8_viral_r0"] > 1.0
