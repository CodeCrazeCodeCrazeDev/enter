from __future__ import annotations
import pytest
from apodex.ai_eos.intelligence import (
    RealityMatrixEngine,
    OpportunityDiscoveryEngine,
    ProblemDecompositionEngine,
    DecisionEngine,
    OpportunityEvaluationEngine,
    ProductCreationEngine,
    CustomerUnderstandingEngine,
    MarketingEngine,
    SalesEngine,
    GrowthEngine,
    CompetitiveMoatEngine,
    OrganizationalDesignEngine,
    MetaLearningEngine,
    FourteenLayerEntrepreneurshipOrchestrator
)


def test_layer1_reality_matrix() -> None:
    engine = RealityMatrixEngine()
    assessment = engine.assess_invariant_principles({
        "max_downside_cents": 10000_00,
        "expected_upside_cents": 1000000_00,
        "experiment_cycle_days": 5.0,
        "has_code_or_media_leverage": True,
        "bottleneck": "sales_funnel"
    })
    assert assessment["is_aligned_with_invariant_principles"] is True
    assert assessment["asymmetry_ratio"] == 100.0

    boundary = engine.classify_automation_boundary("allocate_capital", {"sovereign_capital_authority": True})
    assert boundary == "human_judgment_required"


def test_layer2_opportunity_discovery() -> None:
    engine = OpportunityDiscoveryEngine()
    signals = [
        {"name": "s1", "acceleration": 0.20, "noise_ratio": 0.1},
        {"name": "s2", "acceleration": 0.05, "noise_ratio": 0.8}
    ]
    weak = engine.sense_weak_signals(signals)
    assert len(weak) == 1
    assert weak[0]["name"] == "s1"

    synthesis = engine.combinatorial_synthesis(
        {"name": "Quantum", "taxonomy_id": 1, "feasibility": 0.9, "market_cents": 1000},
        {"name": "Logistics", "taxonomy_id": 5, "feasibility": 0.8, "market_cents": 2000}
    )
    assert synthesis["synthetic_opportunity"] == "Quantum x Logistics"
    assert synthesis["novelty_score"] > 0


def test_layer3_problem_decomposition() -> None:
    engine = ProblemDecompositionEngine()
    decomp = engine.decompose_causal_dag(
        symptoms=["High latency", "Dropped checkout"],
        causal_edges=[("DB Lock", "High latency"), ("High latency", "Dropped checkout")]
    )
    assert decomp["root_causes"] == ["DB Lock"]

    jtbd = engine.evaluate_jtbd_vector(functional=0.9, emotional=0.5, social=0.2, current_friction=0.8)
    assert jtbd["is_actionable"] is True

    ignore = engine.should_ignore_problem(wtp_cents=100, cost_cents=500, frequency_per_year=1)
    assert ignore is True


def test_layer4_decision_engine() -> None:
    engine = DecisionEngine()
    evoi = engine.compute_evoi(prior_uncertainty=0.6, experiment_cost_cents=5000, potential_gain_cents=50000)
    assert evoi == 25000.0

    gate = engine.gate_data_vs_intuition(sample_size=10, market_novelty_score=0.9)
    assert gate == "rely_on_intuition_priors"

    kill = engine.check_kill_switch(posterior_confidence=0.1, threshold=0.2)
    assert kill is True


def test_layer5_opportunity_evaluation() -> None:
    engine = OpportunityEvaluationEngine()
    val = engine.calculate_opportunity_value(
        tam_cents=100000000, urgency=0.9, margin_percent=0.8, defensibility=0.7, risk=0.3, capital_intensity=0.2
    )
    assert val > 0.0

    timing = engine.evaluate_timing_window(platform_shift=True, cost_threshold_met=True, regulatory_deadline=False)
    assert timing == "open"


def test_layer6_product_creation() -> None:
    engine = ProductCreationEngine()
    features = [
        {"name": "Core Flow", "delta_retention": 0.3, "delta_wtp": 0.2, "complexity_cost": 0.2},
        {"name": "Feature Creep", "delta_retention": 0.01, "delta_wtp": 0.01, "complexity_cost": 2.0}
    ]
    approved = engine.anti_bloat_feature_prune(features, complexity_threshold=1.0)
    assert len(approved) == 1
    assert approved[0]["name"] == "Core Flow"


def test_layer7_customer_understanding() -> None:
    engine = CustomerUnderstandingEngine()
    prob = engine.calculate_switching_probability(push=0.8, pull=0.9, anxiety=0.2, habit=0.3)
    assert prob > 0.5


def test_layer8_marketing_engine() -> None:
    engine = MarketingEngine()
    trajectory = engine.simulate_attention_diffusion(initial_aware=10, total_population=1000, transmissibility=0.3, decay_rate=0.1, steps=5)
    assert len(trajectory) == 6

    pos_dist = engine.evaluate_positioning_distance(
        our_vector=[2.0, 3.0], competitor_vectors=[[0.0, 0.0]], customer_centroid=[2.1, 3.1]
    )
    assert pos_dist > 0.0


def test_layer9_sales_engine() -> None:
    engine = SalesEngine()
    urgency = engine.calculate_urgency_ratio(cost_of_inaction_annual_cents=100000_00, cost_of_change_one_time_cents=10000_00)
    assert urgency == 10.0

    route = engine.route_sales_model(acv_cents=100000_00)
    assert route == "enterprise_solution_architecture"


def test_layer10_growth_engine() -> None:
    engine = GrowthEngine()
    val = engine.calculate_network_effect_value(user_base=50, network_type="metcalfe")
    assert val == 2500.0

    decel = engine.check_intentional_deceleration_trigger(churn_spike_rate=0.20, latency_p99_sec=0.5)
    assert decel is True


def test_layer11_competitive_moats() -> None:
    engine = CompetitiveMoatEngine()
    moat = engine.compute_moat_durability(network_density=0.8, switching_cost_cents=15000_00, scale_economies=0.7, proprietary_ip=0.9)
    assert moat > 0.5

    pivot = engine.check_pivot_mandate(ltv_cac_ratio=0.8, monthly_attrition=0.05)
    assert pivot is True


def test_layer12_org_design() -> None:
    engine = OrganizationalDesignEngine()
    split = engine.centralization_vs_delegation_split(decision_type="capital_allocation", strategic_impact_score=0.9)
    assert split == "centralized_governance"

    hiring = engine.compute_hiring_trigger(capacity_utilization=0.90, revenue_per_employee_cents=250000_00)
    assert hiring is True


def test_layer13_meta_learning() -> None:
    engine = MetaLearningEngine()
    posterior = engine.bayesian_mental_model_update(prior_belief=0.5, experiment_evidence_positive=True, likelihood_ratio=3.0)
    assert posterior > 0.5

    antipattern = engine.convert_failure_to_antipattern("deploy_untested_billing", {"reason": "Database lock timeout"})
    assert antipattern["failed_action"] == "deploy_untested_billing"


def test_fourteen_layer_orchestrator_end_to_end() -> None:
    orchestrator = FourteenLayerEntrepreneurshipOrchestrator()
    venture_input = {
        "title": "Autonomous AI EOS Engine Venture",
        "tam_cents": 500000000_00,
        "acv_cents": 25000_00,
        "max_downside_cents": 50000_00,
        "expected_upside_cents": 5000000_00,
        "experiment_cycle_days": 3.0,
        "has_code_or_media_leverage": True,
        "bottleneck": "customer_acquisition"
    }

    result = orchestrator.orchestrate_complete_cycle(venture_input)
    assert result["status"] == "success"
    assert result["venture_title"] == "Autonomous AI EOS Engine Venture"
    assert "layer1_reality" in result
    assert "layer2_combinatorial" in result
    assert "layer5_opportunity_value" in result
    assert "layer11_moat_score" in result
    assert "layer13_posterior_belief" in result
