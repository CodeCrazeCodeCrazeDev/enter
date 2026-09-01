"""
Unit and Integration Test Suite for the 14-Layer Computational Architecture of Entrepreneurship.
"""

from __future__ import annotations
import pytest
from uuid import uuid4

from apodex.ai_eos.intelligence import (
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
    FourteenLayerEntrepreneurialEngine,
    OpportunityState,
    CustomerCohort,
    SystemState,
)


def test_layer1_reality_task_classification() -> None:
    layer1 = Layer1_Reality()
    reality_def = layer1.define_entrepreneurship()
    assert "Value_Captured" in reality_def["core_equation"]
    assert len(reality_def["invariants"]) == 4

    judgment_task = layer1.classify_task_automation("Build trust and empathy with founders")
    assert not judgment_task.can_be_automated
    assert judgment_task.category == "judgment"

    algo_task = layer1.classify_task_automation("Sort database records by timestamp")
    assert algo_task.can_be_automated
    assert algo_task.category == "algorithmic"


def test_layer2_opportunity_discovery() -> None:
    layer2 = Layer2_OpportunityDiscovery()
    raw_signals = [
        {"name": "noise", "magnitude": 0.5, "noise_ratio": 1.0},
        {"name": "weak_signal", "magnitude": 3.0, "noise_ratio": 0.5},
    ]
    detected = layer2.detect_weak_signals(raw_signals)
    assert len(detected) == 1
    assert detected[0]["name"] == "weak_signal"

    novel_opp = layer2.synthesize_novel_opportunity("biotech", "ai", {"entropy": 1.9})
    assert novel_opp.domain == "biotech_ai"
    assert "biotech_efficiency" in novel_opp.variables

    invisible_opp = layer2.extract_invisible_opportunity(market_friction_index=0.8, unserved_demand=0.7)
    assert invisible_opp is not None
    assert invisible_opp.title == "Invisible Structural Arbitrage"


def test_layer3_problem_discovery() -> None:
    layer3 = Layer3_ProblemDiscovery()
    causal_edges = [("root_cause_node", "intermediate_node"), ("intermediate_node", "symptom_node")]
    analysis = layer3.isolate_root_cause(["Surface Symptom"], causal_edges)
    assert analysis["root_causes"] == ["root_cause_node"]
    assert analysis["stated_vs_real"]["real_problem"] == "root_cause_node"

    decomposition = layer3.decompose_problem("High operational cost due to manual entry")
    assert len(decomposition["first_order_subproblems"]) > 0
    assert not decomposition["should_ignore"]


def test_layer4_decision_making() -> None:
    layer4 = Layer4_DecisionMaking()

    # Good evidence & high hypothesis confidence -> Proceed
    gate_proceed = layer4.evaluate_decision_gate(hypothesis_confidence=0.8, evidence_p_value=0.01)
    assert gate_proceed["action"] == "PROCEED_TO_EXPERIMENT"
    assert gate_proceed["confirmation_bias_mitigated"]

    # Weak evidence -> Fail fast / kill idea
    gate_kill = layer4.evaluate_decision_gate(hypothesis_confidence=0.3, evidence_p_value=0.30)
    assert gate_kill["action"] == "KILL_IMMEDIATELY"


def test_layer5_opportunity_evaluation() -> None:
    layer5 = Layer5_OpportunityEvaluation(curiosity_weight=1.5)

    opp1 = OpportunityState(
        title="High Epistemic Gain",
        prior_entropy=2.0,
        post_entropy_simulated=0.5,
        success_probability=0.6,
        target_preference=0.9,
        downside_risk=0.1,
    )

    opp2 = OpportunityState(
        title="Low Information Gain",
        prior_entropy=0.7,
        post_entropy_simulated=0.6,
        success_probability=0.4,
        target_preference=0.9,
        downside_risk=0.5,
    )

    ranked = layer5.rank_opportunities([opp1, opp2])
    assert ranked[0][0].title == "High Epistemic Gain"
    assert ranked[0][1] < ranked[1][1]  # Lower EFE score is preferred

    # Test opportunity switching evaluation
    should_switch = layer5.evaluate_opportunity_switch(current_opp=opp2, candidate_opp=opp1)
    assert should_switch


def test_layer6_product_creation() -> None:
    layer6 = Layer6_ProductCreation()
    features = [
        {"name": "high_value_simple", "value_impact": 0.9, "complexity": 0.2},
        {"name": "low_value_complex", "value_impact": 0.1, "complexity": 0.9},
    ]
    res = layer6.evaluate_features_to_exclude(features)
    assert "high_value_simple" in res["features_to_build"]
    assert "low_value_complex" in res["features_to_exclude"]

    jtbd = layer6.discover_jtbd(["Manual invoice reconciliation takes 10 hours"])
    assert "invoice reconciliation" in jtbd


def test_layer7_customer_understanding() -> None:
    layer7 = Layer7_CustomerUnderstanding()
    high_motive_cohort = CustomerCohort(
        name="Frustrated Users",
        push_frustration=0.9,
        pull_attraction=0.9,
        inertia_habit=0.1,
        anxiety_risk=0.1,
        perceived_trust=0.9,
    )
    switch_prob = layer7.calculate_switching_probability(high_motive_cohort)
    assert switch_prob > 0.8

    flywheel = layer7.evaluate_evangelist_flywheel(high_motive_cohort, satisfaction_score=0.95)
    assert flywheel["is_evangelist"]
    assert flywheel["viral_referral_rate"] == 2.5


def test_layer8_marketing_spread() -> None:
    layer8 = Layer8_Marketing()
    spread = layer8.simulate_attention_spread(
        population=5000,
        initial_aware=50,
        virality_beta=0.4,
        decay_gamma=0.1,
        steps=5
    )
    assert spread["is_viral"]
    assert spread["k_factor"] > 1.0
    assert spread["final_aware_count"] > 50


def test_layer9_sales_systems() -> None:
    layer9 = Layer9_Sales()
    strategy_enterprise = layer9.determine_sales_strategy(acv_cents=5000000, buyer_complexity=0.8)
    assert strategy_enterprise == "ENTERPRISE_HIGH_TOUCH"

    strategy_automated = layer9.determine_sales_strategy(acv_cents=50000, buyer_complexity=0.2)
    assert strategy_automated == "PRODUCT_LED_AUTOMATED"

    objection_res = layer9.resolve_objection("price")
    assert "payback period" in objection_res["counter_strategy"]


def test_layer10_growth_compounding() -> None:
    layer10 = Layer10_Growth()
    network_val = layer10.calculate_network_valuation(active_nodes=100, coupling_strength=0.05)
    assert pytest.approx(network_val) == 500.0  # 0.05 * 100^2

    throttle = layer10.evaluate_growth_throttle(
        monthly_growth_rate=0.30,
        churn_rate=0.12,  # Elevated churn triggers throttle
        capacity_utilisation=0.70
    )
    assert throttle["should_throttle_growth"]


def test_layer11_competition_moats() -> None:
    layer11 = Layer11_Competition()
    moat = layer11.score_moat_durability(
        switching_costs_norm=0.9,
        network_density_norm=0.8,
        cost_advantage_norm=0.7,
        brand_trust_norm=0.8
    )
    assert moat["defensibility_class"] == "HIGH_MOAT"
    assert not moat["pivot_recommended"]


def test_layer12_organizational_design() -> None:
    layer12 = Layer12_OrganizationalDesign()
    org = layer12.evaluate_hiring_trigger(team_utilization=0.95, backlog_growth_rate=0.25)
    assert org["trigger_hire"]
    assert "Delegate operational execution" in org["delegation_recommendation"]


def test_layer13_meta_learning() -> None:
    layer13 = Layer13_MetaLearning()
    calibration = layer13.measure_calibration_score(predictions=[0.9, 0.8, 0.1], outcomes=[1, 1, 0])
    # Perfect calibration (0.9 vs 1 = 0.01, 0.8 vs 1 = 0.04, 0.1 vs 0 = 0.01) -> avg = 0.02
    assert pytest.approx(calibration, abs=0.05) == 0.02

    lesson = layer13.convert_failure_to_knowledge({
        "root_cause": "Premature scaling",
        "failed_condition": "CAC > LTV",
        "metric": "LTV/CAC ratio"
    })
    assert "Premature scaling" in lesson["root_cause"]
    assert len(layer13.knowledge_base) == 1


def test_layer14_ai_entrepreneurship_allocation() -> None:
    layer14 = Layer14_AIEntrepreneurship()
    system_state = SystemState(capital_cents=10000000)
    opp1 = OpportunityState(prior_entropy=2.0, post_entropy_simulated=0.5)  # Delta entropy = 1.5
    opp2 = OpportunityState(prior_entropy=1.0, post_entropy_simulated=0.5)  # Delta entropy = 0.5

    allocations = layer14.allocate_resources(system_state, [opp1, opp2])
    assert len(allocations) == 2
    # opp1 gets 1.5 / 2.0 = 75% of capital ($75k)
    assert allocations[opp1.opportunity_id]["capital_cents"] == 7500000
    assert allocations[opp2.opportunity_id]["capital_cents"] == 2500000


def test_master_fourteen_layer_engine_e2e() -> None:
    engine = FourteenLayerEntrepreneurialEngine()
    signals = [
        {"name": "Signal_A", "magnitude": 4.0, "noise_ratio": 0.5, "entropy": 1.9},
        {"name": "Noise_B", "magnitude": 0.2, "noise_ratio": 1.0},
    ]

    result = engine.execute_full_entrepreneurial_cycle(signals)

    assert result["status"] == "SUCCESS"
    assert "definition" in result["layer1_reality"]
    assert result["layer2_selected_opportunity"] == "Ai-Robotics Cross-Domain Convergence"
    assert result["layer4_decision"] == "PROCEED_TO_EXPERIMENT"
    assert result["layer8_viral"] is True
    assert result["layer9_sales_strategy"] == "ENTERPRISE_HIGH_TOUCH"
    assert len(result["layer14_resource_allocations"]) == 1
