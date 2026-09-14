from __future__ import annotations
import pytest

from apodex.ai_eos.intelligence import (
    Signal,
    OpportunityState,
    CustomerProfile,
    Layer1RealitySubstrateEngine,
    Layer2OpportunityDiscoveryEngine,
    Layer3ProblemDiscoveryEngine,
    Layer4DecisionMakingEngine,
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
    FourteenLayerEntrepreneurialEngine,
)


def test_layer1_reality_substrate() -> None:
    l1 = Layer1RealitySubstrateEngine()
    res = l1.evaluate_invariants(ltv_cac_ratio=3.2, customer_value_surplus=100.0)
    assert res["invariant_pass"] is True
    assert res["unit_economics_healthy"] is True
    assert l1.classify_task_automation("normative_value_judgment") == "HUMAN_ONLY"
    assert l1.classify_task_automation("LTV_CAC_OPTIMIZATION") == "AUTOMATABLE_AI"


def test_layer2_opportunity_discovery() -> None:
    l2 = Layer2OpportunityDiscoveryEngine()
    signals = [
        Signal(title="High Entropy Weak Signal", spectral_entropy=0.8, raw_intensity=0.5),
        Signal(title="Low Entropy Noise", spectral_entropy=0.2, raw_intensity=0.1),
    ]
    weak = l2.detect_weak_signals(signals)
    assert len(weak) == 1
    assert weak[0].title == "High Entropy Weak Signal"

    filtered = l2.filter_signals(signals, min_intensity=0.3)
    assert len(filtered) == 1

    combos = l2.generate_novelty_combinations(["ai", "bio"], ["robotics"])
    assert "ai_X_robotics" in combos


def test_layer3_problem_discovery() -> None:
    l3 = Layer3ProblemDiscoveryEngine()
    prob = l3.define_problem(current_state={"speed": 10.0}, target_state={"speed": 50.0})
    assert prob["is_valid_problem"] is True
    assert pytest.approx(prob["gap_magnitude"]) == 40.0

    dag = l3.decompose_problem_dag("latency_bottleneck")
    assert len(dag) == 3
    assert dag[0]["is_root_cause"] is True


def test_layer4_decision_making() -> None:
    l4 = Layer4DecisionMakingEngine()
    efe = l4.compute_active_inference_efe(
        pragmatic_utility=1.0,
        epistemic_information_gain=0.5,
        curiosity_weight=1.5
    )
    # EFE = -1.0 - (1.5 * 0.5) = -1.75
    assert pytest.approx(efe) == -1.75

    best_exp = l4.select_information_first_experiments([
        {"title": "Exp A", "info_gain": 2.0, "cost": 10.0},
        {"title": "Exp B", "info_gain": 5.0, "cost": 10.0},
    ])
    assert best_exp["title"] == "Exp B"


def test_layer5_opportunity_evaluation() -> None:
    l5 = Layer5OpportunityEvaluationEngine()
    ev = l5.calculate_opportunity_ev(
        tam_cents=100_000_000,
        win_probability=0.5,
        margin_pct=0.8,
        capital_at_risk_cents=5_000_000
    )
    # EV = (0.5 * 100M * 0.8) - (0.5 * 5M) = 40M - 2.5M = 37.5M = 37,500,000 cents
    assert ev == 37_500_000

    timing_defer = l5.evaluate_real_options_timing(uncertainty=0.8, option_cost_cents=1000)
    assert timing_defer == "DEFER_AND_STAGE_EXPERIMENT"


def test_layer6_product_creation() -> None:
    l6 = Layer6ProductCreationEngine()
    features = [
        {"name": "high_val_low_comp", "value": 10.0, "complexity": 2.0},
        {"name": "low_val_high_comp", "value": 1.0, "complexity": 9.0},
    ]
    accepted = l6.filter_what_not_to_build(features, max_complexity_budget=5.0)
    assert len(accepted) == 1
    assert accepted[0]["name"] == "high_val_low_comp"

    jtbd = l6.discover_jtbd(["manual_data_entry"])
    assert "MANUAL_DATA_ENTRY" in jtbd


def test_layer7_customer_understanding() -> None:
    l7 = Layer7CustomerUnderstandingEngine()
    profile = CustomerProfile(perceived_new_utility=0.9, current_utility=0.3, switching_friction=0.2)
    res = l7.model_customer_switching(profile)
    assert res["should_switch"] is True

    trust = l7.calculate_trust_score([0.9, 0.95, 0.85])
    assert pytest.approx(trust) == 0.90


def test_layer8_marketing() -> None:
    l8 = Layer8MarketingEngine()
    adoption = l8.simulate_bass_diffusion(potential_market=10000, p=0.03, q=0.38, steps=4)
    assert len(adoption) == 4
    assert adoption[-1] > adoption[0]

    k_factor = l8.calculate_virality_k_factor(invites_per_user=4.0, conversion_rate=0.3)
    assert pytest.approx(k_factor) == 1.2


def test_layer9_sales() -> None:
    l9 = Layer9SalesEngine()
    resolution = l9.resolve_objection_tree("price")
    assert "ROI_GUARANTEE" in resolution

    route = l9.route_sales_pipeline(deal_size_cents=50000_00)
    assert route == "CONSULTATIVE_ENTERPRISE_HUMAN_SALES"


def test_layer10_growth() -> None:
    l10 = Layer10GrowthEngine()
    metcalfe = l10.calculate_network_effects_value(node_count=10, network_type="metcalfe")
    assert pytest.approx(metcalfe) == 100.0

    nrr = l10.predict_retention_nrr(initial_mrr=10000, expansion_mrr=2000, churn_mrr=500)
    assert pytest.approx(nrr) == 115.0


def test_layer11_competition() -> None:
    l11 = Layer11CompetitionEngine()
    moat = l11.compute_moat_durability(
        network_density=0.9,
        switching_costs_cents=10000_00,
        brand_trust=0.8,
        scale_cost_advantage_pct=0.5
    )
    assert moat > 0.6

    should_pivot = l11.check_pivot_trigger(revenue_decay_pct=0.20, customer_attrition_pct=0.25)
    assert should_pivot is True


def test_layer12_org_design() -> None:
    l12 = Layer12OrganizationalDesignEngine()
    actions = l12.check_hiring_and_spawning_trigger(capacity_utilization=0.90, forecast_error_ratio=0.35)
    assert "SPAWN_WORKER_AGENT_INSTANCE" in actions
    assert "SPLIT_GENERALIST_INTO_PEER_REVIEW_TRIAD" in actions

    delegation = l12.delegate_task_execution("LAUNCH_NEW_GTM_CAMPAIGN")
    assert delegation["centralized_intent"] == "LAUNCH_NEW_GTM_CAMPAIGN"


def test_layer13_meta_learning() -> None:
    l13 = Layer13MetaLearningEngine()
    brier = l13.evaluate_brier_score([0.8, 0.9], [1, 1])
    assert brier < 0.1

    updates = l13.update_mental_models_from_trajectories([
        {"success": True},
        {"success": True},
        {"success": False},
    ])
    assert updates["processed_trajectories"] == 3
    assert updates["updated_prior_alpha"] == 12.0


def test_layer14_ai_entrepreneurship() -> None:
    l14 = Layer14AIEntrepreneurshipEngine()
    opp = OpportunityState(title="Autonomous Scientific Lab")
    form = l14.formalize_entrepreneurial_pipeline(opp)
    assert form["opportunity_title"] == "Autonomous Scientific Lab"


def test_fourteen_layer_pipeline_execution() -> None:
    engine = FourteenLayerEntrepreneurialEngine()
    raw_signals = [
        Signal(title="Quantum Compute Material Sensing", domain="deeptech", spectral_entropy=0.75, raw_intensity=0.8)
    ]

    result = engine.execute_full_14_layer_pipeline(raw_signals=raw_signals, total_budget_cents=500_000_00)

    assert result["status"] == "SUCCESS"
    assert result["primary_signal_title"] == "Quantum Compute Material Sensing"
    assert result["layer_1_invariants"]["invariant_pass"] is True
    assert result["layer_3_problem"]["is_valid_problem"] is True
    assert "layer_4_expected_free_energy" in result
    assert result["layer_5_expected_value_cents"] > 0
    assert result["layer_7_customer_should_switch"] is True
    assert result["layer_8_virality_k_factor"] > 1.0
    assert result["layer_10_predicted_nrr_pct"] > 100.0
    assert result["layer_11_moat_score"] > 0.5
    assert len(result["layer_12_org_actions"]) >= 1
