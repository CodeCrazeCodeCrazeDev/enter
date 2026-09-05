from __future__ import annotations
import math
import pytest
from apodex.ai_eos.intelligence import (
    RealitySubstrateEngine,
    OpportunityDiscoveryEngine,
    ProblemDiscoveryEngine,
    DecisionMakingEngine,
    OpportunityEvaluationEngine,
    ProductCreationEngine,
    CustomerUnderstandingEngine,
    MarketingEngine,
    SalesEngine,
    GrowthEngine,
    CompetitionEngine,
    OrganizationalDesignEngine,
    MetaLearningEngine,
    FourteenLayerEntrepreneurialEngine
)


def test_layer1_reality_substrate() -> None:
    engine = RealitySubstrateEngine()

    boundary_human = engine.classify_automation_boundary("Executive Vision", {"requires_empathy": True})
    assert boundary_human["can_automate"] is False

    boundary_opt = engine.classify_automation_boundary("Pricing Optimization", {"is_convex_optimization": True})
    assert boundary_opt["can_automate"] is True

    invariants = engine.evaluate_invariant_principles({
        "max_downside_cents": 1000,
        "max_upside_cents": 10000,
        "prediction_error": 0.1,
        "active_experiments_count": 2
    })
    assert invariants["asymmetric_risk_reward"] is True
    assert invariants["variational_free_energy_minimization"] is True


def test_layer2_opportunity_discovery() -> None:
    engine = OpportunityDiscoveryEngine()

    spectral_amps = [1.0, 1.1, 1.0, 5.5, 0.9]
    weak_signals = engine.detect_weak_signals(spectral_amps, anomaly_threshold=1.5)
    assert 3 in weak_signals

    recombinations = engine.recombine_unrelated_observations(["AI"], ["Robotics"])
    assert "Hybrid(AI + Robotics)" in recombinations


def test_layer3_problem_discovery() -> None:
    engine = ProblemDiscoveryEngine()

    links = [("Root_A", "Middle_B"), ("Middle_B", "Symptom_C")]
    decomp = engine.decompose_problem_dag("Symptom_C", links)

    assert "Root_A" in decomp["root_causes"]
    assert "Symptom_C" in decomp["symptoms"]


def test_layer4_decision_making() -> None:
    engine = DecisionMakingEngine()

    efe = engine.calculate_expected_free_energy(prior_entropy=2.0, post_entropy=0.5, success_prob=0.8)
    assert efe < 0  # Negative expected free energy indicates desirable policy

    blended = engine.blend_intuition_and_data(intuition_prior=0.9, data_likelihood=0.5, sample_size=10)
    # n=10 -> data_weight = 0.5 -> 0.5*0.9 + 0.5*0.5 = 0.7
    assert pytest.approx(blended) == 0.7

    assert engine.fast_kill_check(0.02, 0.05) is True


def test_layer5_opportunity_evaluation() -> None:
    engine = OpportunityEvaluationEngine()

    ev = engine.calculate_expected_value(tam_cents=100000000, win_rate=0.1, margin=0.5, exp_cost_cents=100000)
    assert ev == 5000000 - 100000

    cvar = engine.calculate_cvar_downside([-500.0, -200.0, 100.0, 500.0], alpha=0.25)
    assert cvar <= -200.0


def test_layer6_product_creation() -> None:
    engine = ProductCreationEngine()

    jtbd = engine.extract_core_jtbd("Users need fast data processing.")
    assert "Automate" in jtbd["functional_job"]

    features = [
        {"name": "A", "complexity": 1.0, "utility_per_complexity": 3.0},
        {"name": "B", "complexity": 2.0, "utility_per_complexity": 1.0},
        {"name": "C", "complexity": 5.0, "utility_per_complexity": 0.1}
    ]
    pruned = engine.prune_feature_complexity(features, complexity_budget=3.0)
    assert len(pruned) == 2
    assert [f["name"] for f in pruned] == ["A", "B"]


def test_layer7_customer_understanding() -> None:
    engine = CustomerUnderstandingEngine()

    prob = engine.calculate_switching_probability(u_new=1.0, u_old=0.2, switching_friction=0.1)
    assert prob > 0.6

    updated_trust = engine.update_trust_score(current_trust=0.5, promised_utility=0.8, delivered_utility=0.82)
    assert updated_trust == 0.55


def test_layer8_marketing() -> None:
    engine = MarketingEngine()

    r0 = engine.calculate_viral_r0(transmission_rate=0.2, active_retention_days=10.0)
    assert pytest.approx(r0) == 2.0

    pos_dist = engine.compute_positioning_distance([1.0, 1.0], [[0.0, 0.0]])
    assert pytest.approx(pos_dist) == math.sqrt(2)


def test_layer9_sales() -> None:
    engine = SalesEngine()

    resolution = engine.resolve_objection("TOO_EXPENSIVE")
    assert "payback" in resolution

    urgency = engine.calculate_buying_urgency_index(cost_of_inaction_cents=10000000, implementation_friction=1.0)
    assert urgency > 0.5


def test_layer10_growth() -> None:
    engine = GrowthEngine()

    cohorts = engine.simulate_compounding_growth(initial_users=100, viral_k=0.2, retention_rate=0.8, cycles=3)
    assert len(cohorts) == 4
    assert cohorts[-1] == int(100 * (0.8 + 0.16) ** 3)

    assert engine.evaluate_platform_transition(user_base=20000, active_developers=100) is True


def test_layer11_competition() -> None:
    engine = CompetitionEngine()

    moat = engine.calculate_moat_score(switching_costs=0.9, network_effects=0.8, scale_moat=0.7)
    assert pytest.approx(moat) == (0.9 * 0.4 + 0.8 * 0.4 + 0.7 * 0.2)

    payoff = engine.predict_competitor_payoff("PRICE_CUT")
    assert payoff == -0.2


def test_layer12_org_design() -> None:
    engine = OrganizationalDesignEngine()

    assert engine.evaluate_hiring_demand(shadow_price_talent=2.0) is True
    assert engine.determine_delegation_level(0.9) == "CENTRALIZED_FOUNDER_DIRECTED"


def test_layer13_meta_learning() -> None:
    engine = MetaLearningEngine()

    brier = engine.calculate_brier_score(forecast_probs=[0.9, 0.1], actual_outcomes=[1, 0])
    assert pytest.approx(brier) == 0.01

    axiom = engine.convert_failure_to_axiom("EXP_001", "High churn")
    assert "AXIOM_NEVER" in axiom["domain_axiom"]


def test_layer14_fourteen_layer_master_orchestrator() -> None:
    orchestrator = FourteenLayerEntrepreneurialEngine()

    signal = {
        "title": "Autonomous AI Agent Enterprise Opportunity",
        "stated_problem": "High manual operational bottleneck",
        "causal_links": [("Manual_Process", "Bottleneck")],
        "spectral_amplitudes": [0.2, 0.4, 4.2, 0.5],
        "tam_cents": 1000000000
    }

    result = orchestrator.execute_full_entrepreneurial_cycle(
        market_signal=signal,
        available_capital_cents=50000000,
        compute_budget=100.0
    )

    assert result["cycle_number"] == 1
    assert result["layer1_automation_boundary"]["can_automate"] is True
    assert result["layer1_invariants_satisfied"]["asymmetric_risk_reward"] is True
    assert 2 in result["layer2_weak_signal_indices"]
    assert result["layer4_expected_free_energy"] < 0
    assert result["layer10_is_platform_ready"] is True
    assert "AXIOM_NEVER" in result["layer13_registered_axiom"]
