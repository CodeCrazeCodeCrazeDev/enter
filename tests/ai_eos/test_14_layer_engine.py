"""
Test suite for the 14-Layer Computational Architecture of Entrepreneurship.
"""

from __future__ import annotations
import pytest
from apodex.ai_eos.intelligence.fourteen_layer_engine import (
    OpportunitySignal,
    ProblemDefinition,
    DecisionEvaluation,
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
    AIEntrepreneurshipLayer,
    FourteenLayerEntrepreneurialEngine
)


def test_layer1_reality_substrate() -> None:
    layer = RealitySubstrateLayer()
    decomp_trust = layer.decompose_problem_domain("trust_building")
    decomp_pricing = layer.decompose_problem_domain("pricing")
    bounds = layer.evaluate_automation_bounds()

    assert decomp_trust["category"] == "HUMAN_PSYCHOLOGY"
    assert decomp_trust["requires_human_judgment"] is True
    assert decomp_pricing["category"] == "OPTIMIZATION_PROBLEM"
    assert decomp_pricing["automatable"] is True
    assert len(bounds["cannot_be_automated"]) > 0
    assert len(bounds["can_be_automated"]) > 0


def test_layer2_opportunity_discovery() -> None:
    layer = OpportunityDiscoveryLayer()
    signal = OpportunitySignal(title="Weak Signal", domain="tech", noise_ratio=0.1)
    filtered = layer.filter_weak_signal(signal, SNR_threshold=2.0)

    assert filtered.surpass_threshold is True

    fused = layer.fuse_cross_domain_observations(["AI Agents"], ["Biotech"])
    assert len(fused) == 1
    assert "Cross-Domain Synthesis" in fused[0]

    velocity = layer.evaluate_trend_velocity(0.5, 0.2)
    assert pytest.approx(velocity) == 0.32


def test_layer3_problem_discovery() -> None:
    layer = ProblemDiscoveryLayer()
    causal_chain = [("root_friction", "checkout_abandonment"), ("checkout_abandonment", "revenue_loss")]
    problem_def = layer.decompose_and_isolate_root_cause(
        stated_problem="Revenue Drop",
        causal_chain=causal_chain,
        estimated_tam_cents=500_000_000
    )

    assert problem_def.latent_root_cause == "root_friction"
    assert problem_def.should_ignore is False


def test_layer4_decision_making() -> None:
    layer = DecisionMakingLayer()
    signal = OpportunitySignal(title="High EV Signal", domain="SaaS", success_probability=0.8, prior_entropy=1.5, post_entropy_simulated=0.3)
    eval_res = layer.evaluate_decision_under_uncertainty(signal)

    assert eval_res.decision_type == "EXECUTE"
    assert eval_res.expected_free_energy < 0.0


def test_layer5_opportunity_evaluation() -> None:
    layer = OpportunityEvaluationLayer()
    res = layer.calculate_expected_value_and_cvar(
        tam_cents=100_000_000,
        success_prob=0.6,
        downside_loss_cents=10_000_000
    )

    assert res["expected_value_cents"] == 56_000_000
    assert res["cvar_downside_risk_cents"] == pytest.approx(500_000)

    timing = layer.evaluate_real_option_timing(0.8, 0.3)
    assert timing == "WAIT_AND_OBSERVE_OPTION"


def test_layer6_product_creation() -> None:
    layer = ProductCreationLayer()
    mvp = layer.determine_mvp_boundary([
        {"name": "Core Value Prop", "jtbd_impact": 0.9, "complexity": 0.2},
        {"name": "Nice To Have Widget", "jtbd_impact": 0.1, "complexity": 0.9}
    ])

    assert "Core Value Prop" in mvp["build_features"]
    assert "Nice To Have Widget" in mvp["discard_features"]

    velocity = layer.calculate_learning_velocity(10.0, 100_00, 5)
    assert pytest.approx(velocity) == 0.02


def test_layer7_customer_understanding() -> None:
    layer = CustomerUnderstandingLayer()
    prob = layer.model_customer_switching_barrier(
        perceived_value_delta=2.0,
        switching_cost_cents=500_00,
        brand_trust=0.9
    )
    assert prob > 0.5

    hazard = layer.calculate_churn_hazard(1.0, 5)
    assert hazard > 0.4


def test_layer8_marketing() -> None:
    layer = MarketingLayer()
    viral = layer.calculate_epidemic_viral_coefficient(2.0, 0.6)
    assert viral["is_exponential_growth"] is True
    assert pytest.approx(viral["viral_coefficient_k"]) == 1.2

    attribution = layer.evaluate_channel_attribution({"seo": 100.0, "paid": 300.0})
    assert pytest.approx(attribution["paid"]) == 0.75


def test_layer9_sales() -> None:
    layer = SalesLayer()
    touch = layer.evaluate_sales_touch_threshold(2_000_000)
    assert touch == "FIELD_ENTERPRISE_SALES"

    script = layer.resolve_objection("price_too_high")
    assert "payback" in script


def test_layer10_growth() -> None:
    layer = GrowthLayer()
    val_metcalfe = layer.compute_network_effect_value(10, topology="metcalfe")
    assert val_metcalfe == 100.0

    nrr = layer.calculate_nrr(100_000, 30_000, 10_000)
    assert nrr == 120.0


def test_layer11_competition() -> None:
    layer = CompetitionLayer()
    moat = layer.score_moat_durability(0.8, 0.7, 0.9)
    assert moat > 0.7

    pivot = layer.detect_pivot_trigger(-0.30, 0.20)
    assert pivot is True


def test_layer12_organizational_design() -> None:
    layer = OrganizationalDesignLayer()
    hire = layer.evaluate_hiring_trigger(0.90, 20_000_000)
    assert hire is True

    route = layer.route_task_delegation(0.9, 0.1)
    assert route == "CENTRALIZED_FOUNDER_CORE"


def test_layer13_meta_learning() -> None:
    layer = MetaLearningLayer()
    brier = layer.calculate_brier_score([0.9, 0.1], [1, 0])
    assert brier == pytest.approx(0.01)

    knowledge = layer.convert_failure_to_knowledge("hyp_123", {"churn": 0.5})
    assert "hyp_123" in knowledge["failed_hypothesis_id"]


def test_layer14_ai_entrepreneurship() -> None:
    layer = AIEntrepreneurshipLayer()
    tax = layer.classify_task_taxonomy("unit_economics")
    assert tax == "DETERMINISTIC_ALGORITHM"

    opp = OpportunitySignal(title="AI Startup", domain="AI", tam_cents=100_000_000)
    res = layer.allocate_resources_autonomously(10_000_000, 50.0, [opp])
    assert res["status"] == "ALLOCATED"
    assert "AI Startup" in res["allocations"]


def test_fourteen_layer_engine_orchestration() -> None:
    engine = FourteenLayerEntrepreneurialEngine()
    raw_signal = OpportunitySignal(
        title="Autonomous Scientific OS",
        domain="AI OS",
        noise_ratio=0.1,
        success_probability=0.7,
        tam_cents=1_000_000_000,
        expected_ltv_cents=5_000_00,
        estimated_cac_cents=1_000_00
    )

    result = engine.execute_end_to_end_pipeline(raw_signal, budget_cents=50_000_000)

    assert result["status"] == "SUCCESS"
    assert result["opportunity_title"] == "Autonomous Scientific OS"
    assert result["decision"] == "EXECUTE"
    assert result["moat_score"] > 0.5
    assert len(result["mvp_features"]) > 0
