from __future__ import annotations
import pytest

from apodex.ai_eos.intelligence.fourteen_layer_engine import (
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
    FourteenLayerEngine,
)


def test_layer1_reality() -> None:
    l1 = Layer1_Reality()
    res = l1.analyze_fundamental_reality()
    assert "invariant_principles" in res
    assert len(res["invariant_principles"]) >= 5
    assert l1.is_automation_feasible("signal_sensing") is True
    assert l1.is_automation_feasible("empathy") is False


def test_layer2_opportunity_discovery() -> None:
    l2 = Layer2_OpportunityDiscovery()
    signals = [
        {"title": "Weak signal", "signal_strength": 0.8, "noise_level": 0.1, "tam_cents": 50_000_000_00},
        {"title": "Noise signal", "signal_strength": 0.1, "noise_level": 0.5, "tam_cents": 1_000_000_00}
    ]
    opps = l2.search_world_state_space(signals)
    assert len(opps) == 1
    assert opps[0]["title"] == "Weak signal"

    bisoc = l2.bisociative_synthesis(
        {"concept": "AI", "mechanism": "Active Inference", "name": "AI Domain"},
        {"concept": "Biotech", "target": "Drug Discovery", "name": "Biotech Domain"}
    )
    assert bisoc["title"] == "AI x Biotech"


def test_layer3_problem_discovery() -> None:
    l3 = Layer3_ProblemDiscovery()
    prob = l3.define_problem({"revenue": 1000}, {"revenue": 5000})
    assert prob["quantified_gaps"]["revenue"] == 4000

    root_analysis = l3.five_whys_root_cause_analysis(
        stated_problem="Low Conversion Rate",
        causal_chain=["Low Conversion", "High Page Latency", "Unoptimized Database Query"]
    )
    assert root_analysis["root_cause"] == "Unoptimized Database Query"
    assert root_analysis["is_symptom"] is True


def test_layer4_decision_making() -> None:
    l4 = Layer4_DecisionMaking()
    # Under low data density (0.2), curiosity/epistemic value boosts exploration
    decision = l4.make_decision_under_uncertainty(
        options=[
            {"name": "Safe Path", "utility": 0.8, "uncertainty": 0.1},
            {"name": "High Curiosity Path", "utility": 0.7, "uncertainty": 0.9}
        ],
        data_density=0.2
    )
    assert decision["selected_option"]["name"] == "High Curiosity Path"
    assert decision["decision_mode"] == "epistemic_exploration"

    falsification = l4.evaluate_falsification(hypothesis_posterior=0.8, red_team_contradictions=5)
    assert falsification["should_kill_idea"] is True


def test_layer5_opportunity_evaluation() -> None:
    l5 = Layer5_OpportunityEvaluation()
    ev = l5.calculate_expected_value(tam_cents=100_000_000_00, win_probability=0.2)
    assert isinstance(ev, float)

    downside = l5.estimate_downside_risk(capital_committed_cents=500_000_00, insolvency_hazard=0.5)
    assert downside["risk_tier"] == "CRITICAL"


def test_layer6_product_creation() -> None:
    l6 = Layer6_ProductCreation()
    features = [
        {"name": "Feature High ROI", "value": 10.0, "complexity": 2.0},
        {"name": "Feature Low ROI", "value": 1.0, "complexity": 9.0}
    ]
    selected = l6.determine_what_not_to_build(features, max_complexity_budget=5.0)
    assert len(selected) == 1
    assert selected[0]["name"] == "Feature High ROI"


def test_layer7_customer_understanding() -> None:
    l7 = Layer7_CustomerUnderstanding()
    psych = l7.model_customer_psychology(utility_delta=10.0, switching_cost=3.0, friction=2.0)
    assert psych["will_customer_switch"] is True

    psych_stay = l7.model_customer_psychology(utility_delta=2.0, switching_cost=5.0, friction=2.0)
    assert psych_stay["will_customer_switch"] is False


def test_layer8_marketing() -> None:
    l8 = Layer8_Marketing()
    diffusion = l8.model_attention_diffusion(
        total_population=1000, infected_initial=10, transmission_rate=0.4, recovery_rate=0.1, steps=5
    )
    assert diffusion["total_reached"] > 10


def test_layer9_sales() -> None:
    l9 = Layer9_Sales()
    sales_sys = l9.design_repeatable_sales_system(
        annual_contract_value_cents=100_000_00,  # $100k ACV
        funnel_conversion_rates={"mql_to_sql": 0.3, "sql_to_close": 0.2}
    )
    assert sales_sys["recommended_sales_model"] == "ENTERPRISE_DIRECT_SALES"


def test_layer10_growth() -> None:
    l10 = Layer10_Growth()
    growth = l10.model_compounding_growth(network_nodes=20, retention_rate=0.95, ltv_cac_ratio=4.0)
    assert growth["metcalfe_network_value"] == 400
    assert growth["is_compounding_healthily"] is True


def test_layer11_competition() -> None:
    l11 = Layer11_Competition()
    # 2x2 minimax matrix
    payoffs = [
        [3.0, 1.0],  # Strategy 0: worst case = 1.0
        [2.0, 0.5]   # Strategy 1: worst case = 0.5
    ]
    minimax = l11.anticipate_competitor_moves_minimax(payoffs)
    assert minimax["optimal_strategy_index"] == 0
    assert minimax["maximin_guaranteed_payoff"] == 1.0


def test_layer12_organizational_design() -> None:
    l12 = Layer12_OrganizationalDesign()
    hiring = l12.evaluate_hiring_triggers(workload_utilization=0.9, sla_breaches=0)
    assert hiring["should_hire"] is True

    delegation = l12.design_delegation_structure(task_criticality=0.2)
    assert delegation["delegation_mode"] == "AUTONOMOUS_AGENT_EXECUTION"


def test_layer13_meta_learning() -> None:
    l13 = Layer13_MetaLearning()
    brier = l13.measure_decision_quality_brier(
        predictions=[0.9, 0.8, 0.1],
        outcomes=[1, 1, 0]
    )
    assert brier["calibration"] == "EXCELLENT"


def test_layer14_ai_entrepreneurship() -> None:
    l14 = Layer14_AIEntrepreneurship()
    task_eval = l14.formalize_entrepreneurial_task("Unit Economics Cohort Analysis")
    assert task_eval["formalization_category"] == "DETERMINISTIC_ALGORITHM"

    kelly = l14.allocate_resources_kelly(
        total_capital_cents=1000_000_00,
        win_probability=0.6,
        payoff_ratio=2.0
    )
    # p=0.6, q=0.4, b=2.0 -> f* = (0.6*2 - 0.4)/2 = 0.4. Half-kelly = 0.2
    assert pytest.approx(kelly["safe_half_kelly_fraction"]) == 0.2
    assert kelly["allocated_capital_cents"] == 200_000_00


def test_fourteen_layer_engine_e2e_pipeline() -> None:
    engine = FourteenLayerEngine()
    signals = [
        {"title": "Autonomous AI Agent Platform", "signal_strength": 0.9, "noise_level": 0.1, "tam_cents": 2000_000_00}
    ]
    res = engine.run_full_14_layer_pipeline(signals)
    assert res["status"] == "COMPLETED_14_LAYER_PIPELINE"
    assert "layer1_reality" in res
    assert "layer14_kelly_capital_allocation" in res
