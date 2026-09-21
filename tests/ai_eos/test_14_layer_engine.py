"""
Tests for the 14-Layer Computational Engine of Entrepreneurship.
"""

import pytest
from apodex.ai_eos.intelligence import (
    FourteenLayerEntrepreneurialEngine,
    RealitySubstrateEngine,
    SignalFilter,
    ProblemDecompositionEngine,
    ActiveInferenceDecisionEngine,
    CapitalAllocationEngine,
    ProductValueOptimizer,
    CustomerPsychologyEngine,
    AttentionDiffusionEngine,
    RepeatableSalesEngine,
    CompoundingGrowthEngine,
    CompetitiveMoatAnalyzer,
    OrganizationalScalingEngine,
    MetaLearningEngine,
)


def test_layer1_reality_substrate():
    engine = RealitySubstrateEngine()
    val = engine.calculate_value_creation(initial_entropy=10.0, final_entropy=2.0, friction_cost=1.5)
    assert val == 6.5

    classification = engine.classify_task_automatability("Capital Allocation", involves_existential_trust=False)
    assert classification["automatable"] is True
    assert classification["category"] == "algorithmic_optimization"


def test_layer2_opportunity_discovery():
    filter_engine = SignalFilter()
    filtered = filter_engine.filter_signal(raw_signal=5.0, noise_variance=1.0)
    assert filtered == 2.5

    synth = filter_engine.cross_domain_synthesis(["AI"], ["Biotech"])
    assert "AI x Biotech" in synth


def test_layer3_problem_discovery():
    problem_engine = ProblemDecompositionEngine()
    severity = problem_engine.define_problem(current_state_friction=3.0, goal_state_value=10.0)
    assert severity == 7.0

    real_pain = problem_engine.disambiguate_stated_vs_real(stated_pain=10.0, price_elasticity_revealed=0.8)
    assert real_pain == 8.0


def test_layer4_decision_making():
    decision_engine = ActiveInferenceDecisionEngine(curiosity_weight=1.0)
    efe = decision_engine.calculate_expected_free_energy(
        p_success=0.8, p_target=0.9, prior_entropy=1.5, post_entropy=0.3
    )
    # Epistemic value = 1.2
    # Pragmatic value = ln(0.8) - ln(0.9) < 0
    # EFE should be negative (favorable option)
    assert efe < 0.0


def test_layer5_capital_allocation():
    capital_engine = CapitalAllocationEngine()
    ev = capital_engine.calculate_expected_value(p_success=0.7, upside_npv=1_000_000, capital_at_risk=100_000)
    assert ev == 670_000.0

    tranches = capital_engine.evaluate_staged_option_tranches(100_000)
    assert tranches == [1_000.0, 5_000.0, 20_000.0, 74_000.0]


def test_layer6_product_creation():
    product_engine = ProductValueOptimizer()
    score = product_engine.calculate_feature_value_score(retention_lift=0.25, engineering_hours=10.0)
    assert score == 0.025

    ttv = product_engine.calculate_time_to_value(user_steps=3, latency_per_step_seconds=5.0)
    assert ttv == 15.0


def test_layer7_customer_understanding():
    customer_engine = CustomerPsychologyEngine()
    switch = customer_engine.evaluate_switching_utility(
        new_utility=100.0, old_utility=50.0, switching_cost=20.0, risk_penalty=10.0
    )
    assert switch is True


def test_layer8_marketing():
    mkt = AttentionDiffusionEngine()
    k = mkt.calculate_viral_coefficient(invites_per_user=5.0, conversion_per_invite=0.3)
    assert k == 1.5


def test_layer9_sales():
    sales = RepeatableSalesEngine()
    coi = sales.calculate_cost_of_inaction(daily_loss=500.0, decision_delay_days=10)
    assert coi == 5000.0

    motion = sales.categorize_sales_motion(100_000.0)
    assert motion == "enterprise_committee"


def test_layer10_growth():
    growth = CompoundingGrowthEngine()
    val = growth.calculate_metcalfe_value(user_count=1000, network_constant=1e-4)
    assert val == 100.0


def test_layer11_competition():
    moat = CompetitiveMoatAnalyzer()
    score = moat.evaluate_moat_strength(switching_cost=10.0, network_effect=8.0, scale_economy=5.0)
    assert score == 8.2


def test_layer12_org():
    org = OrganizationalScalingEngine()
    hire = org.evaluate_hiring_trigger(
        bottleneck_sla_seconds=120.0, target_sla_seconds=30.0, labor_cost=5000.0, automation_cost=20000.0
    )
    assert hire is True


def test_layer13_meta_learning():
    meta = MetaLearningEngine()
    surprise = meta.calculate_bayesian_surprise(prior_prob=0.8, posterior_prob=0.2)
    assert surprise > 0.0


def test_master_14_layer_engine_end_to_end():
    engine = FourteenLayerEntrepreneurialEngine()
    res = engine.execute_end_to_end_cycle(
        raw_signal=10.0, noise=1.0, prior_prob=0.7, posterior_prob=0.3
    )
    assert res["status"] == "cycle_completed"
    assert res["filtered_signal"] == 5.0
    assert "expected_free_energy" in res
    assert "expected_value" in res
    assert "bayesian_surprise" in res
