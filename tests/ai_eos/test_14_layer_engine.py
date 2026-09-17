"""
Unit and integration test suite for the 14-Layer Computational Architecture
of Entrepreneurship in apodex.ai_eos.intelligence.fourteen_layer_engine.
"""

import pytest
from uuid import uuid4
from apodex.ai_eos.intelligence import (
    Signal,
    OpportunityCandidate,
    CausalNode,
    ProblemDAG,
    JobToBeDone,
    Feature,
    Layer1_RealitySubstrate,
    Layer2_OpportunitySearchEngine,
    Layer3_ProblemDecompositionEngine,
    Layer4_ActiveInferenceDecisionEngine,
    Layer5_OpportunityValuationEngine,
    Layer6_ProductSynthesisEngine,
    Layer7_CustomerPsychologyEngine,
    Layer8_MarketingDiffusionEngine,
    Layer9_RepeatableSalesEngine,
    Layer10_CompoundingGrowthEngine,
    Layer11_CompetitiveMoatEngine,
    Layer12_OrganizationalScalingEngine,
    Layer13_MetaLearningEngine,
    Layer14_AutonomousAIEntrepreneur,
    FourteenLayerEntrepreneurialEngine
)


def test_layer1_reality_substrate():
    l1 = Layer1_RealitySubstrate()
    res = l1.check_invariant_principles(ltv_cents=300000, cac_cents=50000, adaptation_rate=2.0, decay_rate=0.5)
    assert res["unit_economics_valid"] is True
    assert res["ltv_to_cac_ratio"] == 6.0
    assert res["feedback_velocity_valid"] is True
    assert res["can_automate_execution"] is True


def test_layer2_opportunity_search_engine():
    l2 = Layer2_OpportunitySearchEngine()
    s1 = Signal(domain="AI", historical_variance=0.1, recent_variance=0.8, delta_mean=2.0, entropy_kl_div=0.9)
    s2 = Signal(domain="Biotech", historical_variance=0.2, recent_variance=0.9, delta_mean=1.5, entropy_kl_div=0.7)

    detected = l2.detect_weak_signals([s1, s2])
    assert len(detected) == 2

    opp = l2.bisociative_combination(s1, s2)
    assert "Bisociative Arbitrage" in opp.title
    assert opp.novelty_score == 0.8


def test_layer3_problem_decomposition_engine():
    l3 = Layer3_ProblemDecompositionEngine()
    dag = ProblemDAG(
        nodes={
            "root_bug": CausalNode(name="root_bug", friction_weight=5.0),
            "symptom_latency": CausalNode(name="symptom_latency", friction_weight=2.0)
        },
        edges=[("root_bug", "symptom_latency", 2.0)]
    )

    root, reduction = l3.analyze_root_cause(dag)
    assert root == "root_bug"
    assert reduction > 5.0

    assert l3.evaluate_active_ignore(solve_cost_cents=100, recovery_value_cents=50) is True
    assert l3.evaluate_active_ignore(solve_cost_cents=50, recovery_value_cents=100) is False


def test_layer4_active_inference_decision_engine():
    l4 = Layer4_ActiveInferenceDecisionEngine()
    opp = OpportunityCandidate(title="EFE Test", domain_a="A", domain_b="B", success_probability=0.7, prior_entropy=1.5, post_entropy_simulated=0.3)

    efe = l4.calculate_efe(opp)
    assert isinstance(efe, float)
    assert l4.check_fast_kill_gate(posterior_confidence=0.1, kill_threshold=0.25) is True
    assert l4.check_fast_kill_gate(posterior_confidence=0.8, kill_threshold=0.25) is False


def test_layer5_opportunity_valuation_engine():
    l5 = Layer5_OpportunityValuationEngine()
    opp = OpportunityCandidate(title="Valuation Test", domain_a="A", domain_b="B", success_probability=0.6, tam_cents=1000000, estimated_cac_cents=100000)

    ev = l5.calculate_probabilistic_ev(opp)
    assert ev == 500000.0

    cvar = l5.estimate_cvar([10.0, 50.0, 100.0, 20.0], alpha=0.9)
    assert cvar >= 50.0

    bs_val = l5.black_scholes_real_option(S=100.0, K=80.0, T=1.0, r=0.05, sigma=0.2)
    assert bs_val > 0.0


def test_layer6_product_synthesis_engine():
    l6 = Layer6_ProductSynthesisEngine()
    f1 = Feature(feature_id="1", name="High Utility", utility_gain=0.9, complexity_cost=1.0)
    f2 = Feature(feature_id="2", name="Low Utility", utility_gain=0.2, complexity_cost=5.0)

    selected = l6.select_features_under_budget([f1, f2], complexity_budget=2.0)
    assert len(selected) == 1
    assert selected[0].name == "High Utility"


def test_layer7_customer_psychology_engine():
    l7 = Layer7_CustomerPsychologyEngine()
    prob = l7.calculate_purchase_probability(value_score=10.0, price=2.0, friction=0.5, switching_cost=0.5)
    assert prob > 0.95

    trust = l7.accumulate_trust(current_trust=0.5, delight_signal=0.8)
    assert trust > 0.5


def test_layer8_marketing_diffusion_engine():
    l8 = Layer8_MarketingDiffusionEngine()
    next_n = l8.bass_diffusion_step(N_t=100.0, M=10000.0)
    assert next_n > 100.0

    k = l8.calculate_k_factor(invites_sent_per_user=5.0, conversion_rate=0.3)
    assert k == 1.5


def test_layer9_repeatable_sales_engine():
    l9 = Layer9_RepeatableSalesEngine()
    coi = l9.calculate_cost_of_inaction(monthly_bleed_cents=5000, duration_months=6.0)
    assert coi == 30000

    resolution = l9.resolve_objection("price_too_high")
    assert "payback" in resolution.lower()


def test_layer10_compounding_growth_engine():
    l10 = Layer10_CompoundingGrowthEngine()
    v = l10.metcalfe_value(100)
    assert v == 100.0

    asymptote = l10.predict_day30_retention_asymptote(day1_retention=0.6, day7_retention=0.4)
    assert 0.05 <= asymptote <= 0.95


def test_layer11_competitive_moat_engine():
    l11 = Layer11_CompetitiveMoatEngine()
    mds = l11.calculate_mds(switching_cost=0.9, network_density=0.8, cost_advantage=0.7, brand_equity=0.6)
    assert 0.0 <= mds <= 1.0


def test_layer12_organizational_scaling_engine():
    l12 = Layer12_OrganizationalScalingEngine()
    wait_time = l12.calculate_queue_wait_time(utilization=0.8, service_time_mean=10.0)
    assert wait_time > 0.0

    action = l12.evaluate_delegation_threshold(utilization=0.90)
    assert action == "DELEGATE_TO_AI_WORKERS"


def test_layer13_meta_learning_engine():
    l13 = Layer13_MetaLearningEngine()
    skill = l13.compute_counterfactual_skill_score(actual_return=0.40, benchmark_return=0.15)
    assert skill == 0.25

    failure_mem = l13.update_failure_memory([{"trigger_cause": "high_cac", "condition": "tight_funding"}])
    assert failure_mem["failure_count"] == 1


def test_layer14_autonomous_ai_entrepreneur():
    l14 = Layer14_AutonomousAIEntrepreneur()
    opp1 = OpportunityCandidate(title="Opp 1", domain_a="A", domain_b="B", success_probability=0.8, novelty_score=0.9)
    opp2 = OpportunityCandidate(title="Opp 2", domain_a="C", domain_b="D", success_probability=0.2, novelty_score=0.1)

    alloc = l14.allocate_resources([opp1, opp2], total_budget_cents=100000)
    assert len(alloc) == 2
    assert alloc[opp1.opportunity_id] > alloc[opp2.opportunity_id]


def test_fourteen_layer_master_engine_e2e():
    engine = FourteenLayerEntrepreneurialEngine()
    raw_signals = [
        Signal(domain="AI", historical_variance=0.1, recent_variance=0.8, delta_mean=2.0, entropy_kl_div=0.9),
        Signal(domain="Fintech", historical_variance=0.2, recent_variance=0.9, delta_mean=1.8, entropy_kl_div=0.8)
    ]

    res = engine.execute_full_14_layer_pipeline(raw_signals=raw_signals, available_capital_cents=500000)

    assert res["status"] == "success"
    assert res["layer1_invariants"]["unit_economics_valid"] is True
    assert res["layer2_weak_signals_count"] == 2
    assert res["layer3_root_cause"] == "high_latency"
    assert isinstance(res["layer4_efe"], float)
    assert res["layer5_probabilistic_ev"] > 0
    assert len(res["layer6_features_selected"]) == 1
    assert res["layer7_purchase_probability"] > 0.5
    assert res["layer8_bass_diffusion_next"] > 100.0
    assert res["layer9_cost_of_inaction"] == 3000000
    assert res["layer10_metcalfe_value"] > 0
    assert 0.0 <= res["layer11_moat_durability_score"] <= 1.0
    assert res["layer12_delegation_action"] == "DELEGATE_TO_AI_WORKERS"
    assert abs(res["layer13_skill_score"] - 0.25) < 1e-5
    assert len(res["layer14_allocations"]) >= 1
