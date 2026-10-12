from __future__ import annotations
import pytest
from apodex.ai_eos.intelligence import (
    MarketSignal,
    ProblemSpec,
    OpportunitySpec,
    RealitySubstrateEngine,
    ContinuousStateSpaceDiscoveryEngine,
    ProblemDiscoveryDecompositionEngine,
    DecisionUnderUncertaintyEngine,
    QuantitativeEvaluationEngine,
    ProductCreationEngine,
    CustomerPsychologyEngine,
    MarketFormationEngine,
    PsychologicalSalesEngine,
    CompoundingGrowthEngine,
    CompetitiveDynamicsEngine,
    OrganizationalScalingEngine,
    EntrepreneurialMetaLearningEngine,
    AutonomousAIEntrepreneurshipEngine,
    FourteenLayerOrchestrator,
)


def test_layer1_reality_substrate() -> None:
    engine = RealitySubstrateEngine()
    principles = engine.get_invariant_principles()
    assert len(principles) == 3
    assert "Asymmetric Risk/Reward Arbitrage" in principles

    auto_check = engine.classify_automation_feasibility("sovereign_risk_acceptance")
    assert auto_check["requires_human_sovereignty"] is True
    assert auto_check["automation_feasibility"] == 0.1


def test_layer2_continuous_discovery() -> None:
    engine = ContinuousStateSpaceDiscoveryEngine(variance_threshold=0.3)
    signal = MarketSignal(
        domain="AI",
        title="Generative Agent Hardware",
        variance=0.6,
        domain_a="AI",
        domain_b="Hardware",
        incumbent_cognitive_lock=True
    )
    assert engine.detect_weak_signal_anomaly(signal) is True
    assert engine.synthesize_combinatorial_crossover("AI", "Hardware") == "Crossover_AI_X_Hardware"
    assert engine.is_invisible_opportunity(signal) is True


def test_layer3_problem_decomposition() -> None:
    engine = ProblemDiscoveryDecompositionEngine()
    spec = ProblemSpec(
        stated_problem="Need faster report generation",
        real_problem="Data pipeline schema fragmentation",
        nodes=["pipeline_fragmentation", "slow_ingestion", "delayed_reporting"],
        edges=[("pipeline_fragmentation", "slow_ingestion"), ("slow_ingestion", "delayed_reporting")],
        direct_effect=0.85,
        indirect_effect=0.15,
        cost_to_solve=20000.0,
        expected_value_saved=150000.0
    )
    dag_res = engine.decompose_problem_dag(spec)
    assert "pipeline_fragmentation" in dag_res["root_causes"]
    assert "ROOT_CAUSE" in engine.distill_root_cause_vs_symptom(spec)
    assert engine.evaluate_ignore_decision(spec) is False


def test_layer4_decision_making() -> None:
    engine = DecisionUnderUncertaintyEngine()
    opp = OpportunitySpec(
        title="Active Inference Edge Device",
        domain="robotics",
        prior_entropy=1.8,
        post_entropy_simulated=0.3,
        success_probability=0.7,
        target_preference=0.95
    )
    efe = engine.calculate_expected_free_energy(opp)
    assert isinstance(efe, float)

    voi = engine.calculate_value_of_information(prior_entropy=1.5, cost_of_sample=10000.0)
    assert voi > 0.0

    assert engine.fast_idea_killer(posterior_prob=0.20, cutoff=0.35) is True


def test_layer5_quantitative_evaluation() -> None:
    engine = QuantitativeEvaluationEngine()
    opp = OpportunitySpec(
        title="SaaS B2B Platform",
        domain="enterprise",
        tam_cents=1000000000,
        ltv_cents=2000000,
        cac_cents=400000,
        downside_loss_cents=10000000,
        success_probability=0.6
    )
    ev = engine.compute_expected_value_cents(opp)
    assert ev > 0.0

    var = engine.compute_downside_var_cents(opp)
    assert var > opp.downside_loss_cents

    should_switch = engine.evaluate_bellman_switching_threshold(
        current_ev=1000.0,
        candidate_ev=5000.0,
        switching_cost=500.0
    )
    assert should_switch is True


def test_layer6_product_creation() -> None:
    engine = ProductCreationEngine()
    keep = engine.evaluate_anti_feature_matrix(utility_delta=3.0, complexity_delta=1.0)
    assert keep is True

    prune = engine.evaluate_anti_feature_matrix(utility_delta=1.0, complexity_delta=2.0)
    assert prune is False

    ratio = engine.compute_learning_build_ratio(epistemic_gain=2.0, build_hours=10.0)
    assert ratio == 0.2


def test_layer7_customer_psychology() -> None:
    engine = CustomerPsychologyEngine()
    p_switch = engine.calculate_switching_probability(utility_new=1.0, utility_old=0.2, friction=0.3)
    assert p_switch > 0.5

    hazard = engine.predict_churn_hazard_rate(usage_decay_slope=0.1)
    assert hazard > 0.02


def test_layer8_market_formation() -> None:
    engine = MarketFormationEngine()
    k = engine.compute_viral_coefficient_k(invitations_per_user=3.0, conversion_rate=0.4)
    assert k == pytest.approx(1.2)

    sir = engine.simulate_sir_attention_spread(population=1000, initial_infected=10, beta=0.3, gamma=0.1)
    assert len(sir["infected_attention"]) == 11


def test_layer9_psychological_sales() -> None:
    engine = PsychologicalSalesEngine()
    urgency = engine.compute_buying_urgency(status_quo_loss=100000.0, time_to_deadline=10.0)
    assert urgency > 100000.0

    channel = engine.route_sales_channel(acv_cents=2000000)
    assert channel == "ENTERPRISE_HIGH_TOUCH"


def test_layer10_compounding_growth() -> None:
    engine = CompoundingGrowthEngine()
    val = engine.compute_metcalfe_value(user_count=500)
    assert val == 250000.0

    throttle = engine.evaluate_growth_throttling(churn_rate=0.12, critical_churn_threshold=0.08)
    assert throttle is True


def test_layer11_competitive_dynamics() -> None:
    engine = CompetitiveDynamicsEngine()
    score = engine.score_moat_strength(network_effects=0.9, switching_costs=0.8, cost_advantages=0.7)
    assert 0.0 <= score <= 1.0

    pivot = engine.evaluate_pivot_necessity(ltv_cac_ratio=0.8, incumbent_aggression=0.9)
    assert pivot is True


def test_layer12_organizational_scaling() -> None:
    engine = OrganizationalScalingEngine()
    hire = engine.evaluate_hiring_trigger(capacity_utilization=0.92)
    assert hire is True

    route = engine.route_decision_centralization("capital_allocation")
    assert route == "CENTRALIZED_HQ"


def test_layer13_meta_learning() -> None:
    engine = EntrepreneurialMetaLearningEngine()
    dqs = engine.compute_decision_quality_score(info_completeness=0.8, bias_suppression=0.9, efe_alignment=0.95)
    assert dqs > 0.8

    fail_info = engine.extract_failure_knowledge("Misjudged regulatory timeline")
    assert fail_info["registered_in_global_memory"] is True


def test_layer14_ai_entrepreneurship() -> None:
    engine = AutonomousAIEntrepreneurshipEngine()
    paradigm = engine.classify_execution_paradigm("Evaluate causal counterfactual intervention")
    assert paradigm == "CAUSAL_INFERENCE"

    alloc = engine.optimize_resource_allocation(capital_cents=50000000, compute_units=50.0, max_risk_budget=0.15)
    assert alloc["allocated_capital_cents"] == 35000000


def test_fourteen_layer_orchestrator_e2e() -> None:
    orchestrator = FourteenLayerOrchestrator()

    signal = MarketSignal(
        domain="Autonomous AI",
        title="Autonomous Research Engine",
        variance=0.8,
        domain_a="AI",
        domain_b="ResearchOS",
        incumbent_cognitive_lock=True
    )

    problem = ProblemSpec(
        stated_problem="High latency research hypothesis cycle",
        real_problem="Lack of automated closed-loop validation",
        nodes=["manual_validation", "latency", "slow_execution"],
        edges=[("manual_validation", "latency"), ("latency", "slow_execution")],
        direct_effect=0.9,
        indirect_effect=0.1,
        cost_to_solve=10000.0,
        expected_value_saved=100000.0
    )

    opp = OpportunitySpec(
        title="Autonomous Scientific Research Enterprise",
        domain="AI_EOS",
        prior_entropy=1.9,
        post_entropy_simulated=0.2,
        success_probability=0.75,
        target_preference=0.95,
        tam_cents=2000000000,
        ltv_cents=5000000,
        cac_cents=500000,
        downside_loss_cents=20000000,
        capacity_utilization=0.95
    )

    result = orchestrator.execute_complete_14_layer_pipeline(signal, problem, opp)

    assert result["status"] == "COMPLETED"
    assert result["opportunity_title"] == "Autonomous Scientific Research Enterprise"
    assert "layer1_invariant_principles" in result
    assert "layer14_ai_entrepreneurship" in result
    assert result["layer14_ai_entrepreneurship"]["task_paradigm"] == "CAUSAL_INFERENCE"
