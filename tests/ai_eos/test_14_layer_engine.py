"""
Unit and integration test suite for the 14-Layer Computational Architecture
of Entrepreneurship Engine.
"""

import pytest
from apodex.ai_eos.intelligence.fourteen_layer_engine import (
    RealityEngine,
    OpportunityDiscoveryEngine,
    ProblemDiscoveryEngine,
    DecisionEngine,
    OpportunityEvaluationEngine,
    ProductCreationEngine,
    CustomerUnderstandingEngine,
    MarketingEngine,
    SalesEngine,
    GrowthEngine,
    CompetitionEngine,
    OrganizationalDesignEngine,
    MetaLearningEngine,
    AIEntrepreneurshipEngine,
    FourteenLayerEngine
)


def test_reality_engine():
    engine = RealityEngine()
    res1 = engine.evaluate_task_automation("evaluate_opportunity", False)
    assert res1["automatable"] is True

    res2 = engine.evaluate_task_automation("ultimate_legal_accountability", True)
    assert res2["automatable"] is False


def test_opportunity_discovery_engine():
    engine = OpportunityDiscoveryEngine()
    signal = engine.detect_weak_signal("AI Market Shift", surprise_score=2.0, domain="fintech")
    assert signal["is_valid_opportunity_signal"] is True

    synth = engine.synthesize_cross_domain_novelty("crypto", "healthcare")
    assert synth["novelty_score"] > 0.8


def test_problem_discovery_engine():
    engine = ProblemDiscoveryEngine()
    decomp = engine.decompose_problem(["symptom1", "symptom2"], "root_cause_1", 0.9)
    assert decomp["is_root_cause_validated"] is True
    assert decomp["problem_classification"] == "first_order"


def test_decision_engine():
    engine = DecisionEngine()
    efe = engine.compute_expected_free_energy(p_success=0.8, p_target=0.9, prior_entropy=1.0, simulated_entropy=0.2)
    assert isinstance(efe, float)


def test_opportunity_evaluation_engine():
    engine = OpportunityEvaluationEngine()
    eval_res = engine.evaluate_opportunity(100_000_000_00, 0.6, 0.1, 4.0)
    assert eval_res["risk_adjusted_ev_cents"] > 0
    assert eval_res["quality_tier"] == "tier_1"

    switch = engine.evaluate_switching_decision(100.0, 500.0, 50.0)
    assert switch is True


def test_product_creation_engine():
    engine = ProductCreationEngine()
    features = [
        {"name": "f1", "value": 0.9, "complexity": 0.2},
        {"name": "f2", "value": 0.1, "complexity": 0.9}
    ]
    res = engine.optimize_feature_set(features)
    assert "f1" in res["selected_features"]
    assert "f2" not in res["selected_features"]


def test_customer_understanding_engine():
    engine = CustomerUnderstandingEngine()
    res = engine.evaluate_customer_switching(0.9, 0.1, 0.1)
    assert res["will_switch"] is True


def test_marketing_engine():
    engine = MarketingEngine()
    res = engine.simulate_virality(2.0, 0.6)
    assert res["is_viral"] is True


def test_sales_engine():
    engine = SalesEngine()
    res = engine.resolve_objection("price", 0.9)
    assert res["resolved"] is True
    assert res["action"] == "close_sale"


def test_growth_engine():
    engine = GrowthEngine()
    val = engine.compute_network_value(10)
    assert val == 100.0


def test_competition_engine():
    engine = CompetitionEngine()
    moat = engine.score_moat_durability(0.8, 0.8, 0.8, 0.8)
    assert moat > 0.7

    pivot = engine.evaluate_pivot_trigger(0.20, 0.25)
    assert pivot is True


def test_organizational_design_engine():
    engine = OrganizationalDesignEngine()
    res = engine.evaluate_delegation(500.0, 5.0, 50.0, 50.0)
    assert res["should_delegate"] is True


def test_meta_learning_engine():
    engine = MetaLearningEngine()
    res = engine.record_and_calibrate_decision(0.8, 0.9)
    assert res["prediction_error"] == pytest.approx(0.1)


def test_ai_entrepreneurship_engine():
    engine = AIEntrepreneurshipEngine()
    opps = [{"title": "opp1", "efe": 0.2}, {"title": "opp2", "efe": 0.8}]
    alloc = engine.allocate_resources(opps, 100_000_000, 1e18)
    assert alloc["status"] == "allocated"
    assert "opp1" in alloc["allocations"]


def test_fourteen_layer_engine_e2e():
    engine = FourteenLayerEngine()
    result = engine.run_full_14_layer_cycle(
        signal_title="Autonomous Agent Breakout",
        surprise_score=2.5,
        domain="ai_infrastructure"
    )
    assert result["cycle_status"] == "completed"
    assert result["layer_2_signal"]["is_valid_opportunity_signal"] is True
    assert result["layer_14_resource_allocation"]["status"] == "allocated"
