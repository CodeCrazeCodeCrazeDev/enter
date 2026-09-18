from __future__ import annotations
import pytest

from apodex.ai_eos.intelligence import (
    RealitySubstrateEngine,
    OpportunityDiscoveryEngine,
    ProblemDiscoveryEngine,
    ActiveInferenceDecisionEngine,
    OpportunityEvaluationEngine,
    ProductCreationEngine,
    CustomerPsychologyEngine,
    MarketingSystemDynamicsEngine,
    SalesEngineStateMachine,
    GrowthCompoundingEngine,
    CompetitiveMoatEngine,
    OrganizationalDesignEngine,
    MetaLearningEngine,
    FourteenLayerEntrepreneurialEngine
)


def test_layer1_reality_substrate() -> None:
    engine = RealitySubstrateEngine()
    res = engine.evaluate_arbitrage(current_utility=10.0, expected_future_value=50.0)
    assert res["free_energy_delta"] == 40.0
    assert res["arbitrage_ratio"] == 5.0


def test_layer2_opportunity_discovery() -> None:
    engine = OpportunityDiscoveryEngine()
    z_score = engine.detect_weak_signal_anomaly([1.0, 1.2, 5.0], baseline_mean=1.0, baseline_std=0.5)
    assert z_score == 8.0

    fused = engine.synthesize_cross_domain_knowledge(["ai", "bio"], ["saas", "hardware"])
    assert len(fused) == 4
    assert ("ai", "saas") in fused


def test_layer3_problem_discovery() -> None:
    engine = ProblemDiscoveryEngine()
    decomp = engine.decompose_problem(
        symptoms=["slow_page_load", "high_dropoff"],
        causal_graph={"db_bottleneck": ["slow_page_load", "high_dropoff"]}
    )
    assert decomp["root_bottleneck"] == "db_bottleneck"
    assert decomp["symptoms_count"] == 2


def test_layer4_decision_engine() -> None:
    engine = ActiveInferenceDecisionEngine()
    efe = engine.compute_efe(
        p_success=0.8,
        p_target_preference=0.9,
        prior_entropy=1.2,
        simulated_entropy=0.3,
        curiosity_weight=1.5
    )
    assert efe < 0.0


def test_layer5_opportunity_evaluation() -> None:
    engine = OpportunityEvaluationEngine()
    res = engine.evaluate_opportunity_quality(
        tam_cents=10_000_000_00,
        p_success=0.5,
        hazard_risk=0.1,
        capex_cents=100_000_00
    )
    assert res["is_viable"] is True
    assert res["expected_gross_cents"] == 5_000_000_00


def test_layer6_product_creation() -> None:
    engine = ProductCreationEngine()
    feats = [
        {"name": "f1", "satisfaction_impact": 0.5, "complexity_cost": 1.0},
        {"name": "f2", "satisfaction_impact": 0.4, "complexity_cost": 2.0},
        {"name": "f3", "satisfaction_impact": 0.1, "complexity_cost": 10.0}
    ]
    selected = engine.optimize_minimum_viable_complexity(feats, target_satisfaction_threshold=0.8)
    assert len(selected) == 2
    assert selected[0]["name"] == "f1"


def test_layer7_customer_psychology() -> None:
    engine = CustomerPsychologyEngine()
    switch_res = engine.calculate_switching_utility(
        v_new=10.0, v_old=3.0, cognitive_friction=1.0, financial_cost=1.0, perceived_risk=1.0
    )
    assert switch_res["will_switch"] is True
    assert switch_res["net_switching_utility"] == 4.0

    trust = engine.update_trust_score(current_trust=0.5, promised_value=1.0, actual_value=1.0)
    assert trust == 0.5


def test_layer8_marketing_system_dynamics() -> None:
    engine = MarketingSystemDynamicsEngine()
    res = engine.simulate_viral_growth(initial_users=100, invite_rate=2.0, conversion_rate=0.6, cycles=3)
    assert res["viral_coefficient_k"] == 1.2
    assert res["is_supercritical"] is True
    assert res["final_user_count"] > 100


def test_layer9_sales_engine() -> None:
    engine = SalesEngineStateMachine()
    urgency = engine.compute_buying_urgency(cost_of_inaction_cents=10000_00, time_to_value_days=10)
    # 1,000,000 cents / 10 days = 100,000.0
    assert urgency == 100000.0

    res = engine.handle_objection("pricing", 0.8)
    assert res["resolved"] is True
    assert res["recommended_action"] == "proceed_to_closing"


def test_layer10_growth_compounding() -> None:
    engine = GrowthCompoundingEngine()
    m_val = engine.calculate_metcalfe_network_value(10, value_per_connection_cents=200)
    assert m_val == 9000

    health = engine.evaluate_growth_health(nrr_percent=125.0, ltv_to_cac=4.0, payback_months=8.0)
    assert health["is_compounding_healthy"] is True


def test_layer11_competitive_moat() -> None:
    engine = CompetitiveMoatEngine()
    score = engine.compute_moat_durability_index(0.8, 0.8, 0.8, 0.8)
    assert pytest.approx(score) == 0.8


def test_layer12_org_design() -> None:
    engine = OrganizationalDesignEngine()
    res = engine.evaluate_hiring_need(0.90)
    assert res["needs_hiring"] is True
    assert res["recommended_action"] == "scale_agent_nodes"


def test_layer13_meta_learning() -> None:
    engine = MetaLearningEngine()
    dq = engine.calculate_decision_quality(
        expected_utility=10.0,
        predicted_dist=[0.5, 0.5],
        observed_dist=[0.5, 0.5]
    )
    assert pytest.approx(dq) == 10.0


def test_layer14_full_orchestrator_pipeline() -> None:
    orchestrator = FourteenLayerEntrepreneurialEngine()
    res = orchestrator.run_full_14_layer_pipeline(
        domain_a=["ai", "crypto"],
        domain_b=["fintech", "logistics"],
        current_utility=5.0,
        expected_future_value=25.0,
        tam_cents=50_000_000_00,
        capex_cents=100_000_00
    )
    assert res["status"] == "executed"
    assert "layer1_arbitrage" in res
    assert "layer2_selected_pair" in res
    assert "layer4_efe_score" in res
    assert res["layer10_growth_health"]["is_compounding_healthy"] is True
    assert res["layer11_moat_score"] > 0.0
