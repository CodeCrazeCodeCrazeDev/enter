from __future__ import annotations
import pytest

from apodex.ai_eos.intelligence.fourteen_layer_engine import (
    RealitySubstrateLayer,
    OpportunityDiscoveryLayer,
    ProblemDiscoveryLayer,
    DecisionMakingLayer,
    OpportunityEvaluationLayer,
    ProductCreationLayer,
    CustomerUnderstandingLayer,
    MarketingLayer,
    SalesLayer,
    GrowthLayer,
    CompetitionLayer,
    OrganizationalDesignLayer,
    MetaLearningLayer,
    FourteenLayerEngine
)
from apodex.ai_eos.intelligence import (
    FourteenLayerEngine as ExportedEngine,
    RealitySubstrateLayer as ExportedReality
)


def test_layer_1_reality_substrate() -> None:
    layer = RealitySubstrateLayer()
    opportunity_data = {
        "marginal_value": 150.0,
        "marginal_cost": 50.0,
        "agent_belief_value": 0.9,
        "market_belief_value": 0.2,
        "capital_reserve_cents": 100000,
        "burn_rate_cents": 10000
    }
    result = layer.evaluate_invariants(opportunity_data)
    assert result["unit_economic_solvency"] is True
    assert pytest.approx(result["information_asymmetry"]) == 0.7
    assert result["survival_guaranteed"] is True
    assert result["is_viable"] is True

    cat = layer.categorize_task_automation("terminal_moral_accountability")
    assert cat == "NON_AUTOMATABLE_HUMAN_REQUIRED"


def test_layer_2_opportunity_discovery() -> None:
    layer = OpportunityDiscoveryLayer()
    intensity = layer.detect_hawkes_intensity([1.0, 1.5, 2.0])
    assert intensity > 0.1

    obs_a = {"title": "AI Hardware", "domain": "hardware", "variables": ["cost"], "entropy": 1.5}
    obs_b = {"title": "Lab Automation", "domain": "bio", "variables": ["speed"], "entropy": 0.4}
    combined = layer.combine_unrelated_observations(obs_a, obs_b)
    assert combined["combined_title"] == "AI Hardware x Lab Automation"
    assert combined["is_novel"] is True


def test_layer_3_problem_discovery() -> None:
    layer = ProblemDiscoveryLayer()
    res = layer.separate_symptom_from_root_cause(
        observations={"latency": 2.5, "database_load": 10.0},
        structural_coefs={("database_load", "latency"): 0.2},
        target_symptom="latency",
        candidate_root="database_load"
    )
    assert res["is_root_cause"] is True

    gravity = layer.calculate_problem_gravity(0.9, 10.0, 5000)
    assert pytest.approx(gravity) == 450.0


def test_layer_4_decision_making() -> None:
    layer = DecisionMakingLayer()
    efe = layer.compute_expected_free_energy(
        p_success=0.7,
        p_target_preference=0.9,
        prior_entropy=1.5,
        post_entropy_simulated=0.5,
        curiosity_weight=1.0
    )
    assert efe < 0.0  # Lower EFE is superior
    assert layer.evaluate_fast_kill_criteria(efe) is False


def test_layer_5_opportunity_evaluation() -> None:
    layer = OpportunityEvaluationLayer()
    ev = layer.calculate_expected_value(100000000, 0.5, 0.8)
    assert pytest.approx(ev) == 400000.0

    cvar = layer.estimate_cvar_downside(1000000)
    assert cvar > 10000.0

    mfer = layer.calculate_marginal_free_energy_reduction(2.5, 10.0)
    assert pytest.approx(mfer) == 0.25


def test_layer_6_product_creation() -> None:
    layer = ProductCreationLayer()
    features = [
        {"name": "f1", "value_impact": 0.8, "complexity_cost": 0.2},
        {"name": "f2", "value_impact": 0.05, "complexity_cost": 2.0}
    ]
    pruned = layer.prune_features(features, value_threshold=0.5)
    assert len(pruned) == 1
    assert pruned[0]["name"] == "f1"


def test_layer_7_customer_understanding() -> None:
    layer = CustomerUnderstandingLayer()
    trust = layer.update_trust(0.5, 1.0, 0.5)
    assert trust > 0.5

    status = layer.predict_churn_or_evangelism(trust=0.9, delivered_vs_expected_ratio=2.0)
    assert status == "EVANGELIST"


def test_layer_8_marketing() -> None:
    layer = MarketingLayer()
    r_0 = layer.calculate_viral_reproduction_number(0.2, 10.0, 1.0)
    assert pytest.approx(r_0) == 2.0

    shaps = layer.attribution_shapley_values(["google", "twitter", "email"], 300)
    assert shaps["google"] == 100.0


def test_layer_9_sales() -> None:
    layer = SalesLayer()
    urgency = layer.calculate_urgency_vector(50000, 10000)
    assert pytest.approx(urgency) == 5.0

    channel = layer.route_sales_channel(10000000)  # $100k
    assert channel == "ENTERPRISE_FIELD_SALES"


def test_layer_10_growth() -> None:
    layer = GrowthLayer()
    utility = layer.calculate_metcalfe_utility(10)
    assert utility == 45.0

    throttle = layer.should_throttle_growth(95, 100, 0.8)
    assert throttle is True


def test_layer_11_competition() -> None:
    layer = CompetitionLayer()
    moat = layer.evaluate_moat_strength(0.8, 0.9, 0.7, 0.8, 0.8)
    assert pytest.approx(moat) == 0.8

    pivot = layer.evaluate_pivot_trigger(0.2)
    assert pivot is True


def test_layer_12_org_design() -> None:
    layer = OrganizationalDesignLayer()
    hire = layer.evaluate_hiring_trigger(0.9, 0.7)
    assert hire is True

    route = layer.route_decision_type(is_reversible=False, impact_score=0.9)
    assert route == "TYPE_1_CENTRALIZED_BOARD_APPROVAL"


def test_layer_13_meta_learning() -> None:
    layer = MetaLearningLayer()
    updated = layer.bayesian_model_update(prior_belief=0.5, likelihood=0.8, evidence=0.6)
    assert pytest.approx(updated, abs=0.01) == 0.6667

    constraint = layer.convert_failure_to_negative_constraint({"action": "deploy_untested", "context": "high_traffic"})
    assert constraint["severity"] == "CRITICAL"
    assert "DO_NOT_DEPLOY_UNTESTED_WHEN_HIGH_TRAFFIC" in constraint["constraint"]


def test_fourteen_layer_engine_e2e() -> None:
    engine = FourteenLayerEngine()
    signal = {
        "title": "Autonomous Scientific Hardware Venture",
        "signal_history": [1.0, 1.2, 1.8],
        "pain_magnitude": 0.9,
        "frequency": 10.0,
        "willingness_to_pay_cents": 10000,
        "p_success": 0.7,
        "prior_entropy": 1.8,
        "post_entropy_simulated": 0.4,
        "tam_cents": 500000000,
        "features": [{"name": "f1", "value_impact": 0.9, "complexity_cost": 0.1}],
        "acv_cents": 2500000,
        "marginal_value": 200.0,
        "marginal_cost": 50.0,
        "capital_reserve_cents": 5000000,
        "burn_rate_cents": 100000
    }

    res = engine.process_opportunity_pipeline(signal)
    assert res["pipeline_status"] == "COMPLETED"
    assert res["opportunity_title"] == "Autonomous Scientific Hardware Venture"
    assert res["layer_1_reality"]["is_viable"] is True
    assert res["layer_3_problem_gravity"] == 900.0
    assert res["layer_4_fast_kill"] is False
    assert res["layer_6_pruned_feature_count"] == 1
    assert res["layer_9_sales_route"] == "INSIDE_SALES_HYBRID"


def test_package_exports() -> None:
    engine = ExportedEngine()
    assert isinstance(engine.reality, ExportedReality)
