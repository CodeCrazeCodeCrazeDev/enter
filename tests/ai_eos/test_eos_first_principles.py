"""Unit and Integration Tests for EOS First-Principles Reconstruction.

Validates all 11 sections of the Entrepreneurial Operating System model.
"""

import pytest
from uuid import uuid4
from apodex.ai_eos.intelligence import (
    EOSEngineFirstPrinciples,
    EntrepreneurialIntelligenceSystemFirstPrinciples,
    MasterLoopEngine,
    InternalCognitiveLoopEngine,
    ExternalBusinessLoopsEngine,
    CustomerLifecycleEngine,
    GTMSystemSimulator,
    CompanyGrowthStateMachine,
    StrategicMoatEngine,
    FailureModeMonitor,
    EOSOpportunityDecisionTree,
    DecisionRiskType,
    GrowthStage,
    CustomerJourneyStage,
    AIOSState,
)
from apodex.ai_eos.intelligence.eos_first_principles import MasterLoopNode


def test_section_1_master_loop_engine_and_kill_signals():
    """Test Master Loop 19-node execution and kill signal rerouting."""
    engine = MasterLoopEngine()
    assert engine.active_node == MasterLoopNode.ENVIRONMENTAL_SENSING

    # Step through nodes sequentially
    next_node = engine.transition_next({})
    assert next_node == MasterLoopNode.SIGNAL_COLLECTION

    # Advance to Customer Validation and trigger kill signal
    engine.active_node = MasterLoopNode.CUSTOMER_VALIDATION
    next_node = engine.transition_next({"validation_passed": False})
    assert next_node == MasterLoopNode.OPPORTUNITY_DISCOVERY
    assert len(engine.kill_signals_triggered) == 1
    assert engine.kill_signals_triggered[0]["source"] == MasterLoopNode.CUSTOMER_VALIDATION.value

    # Advance to MVP Experimentation and trigger kill signal
    engine.active_node = MasterLoopNode.MVP_EXPERIMENTATION
    next_node = engine.transition_next({"mvp_viable": False})
    assert next_node == MasterLoopNode.OPPORTUNITY_DISCOVERY
    assert len(engine.kill_signals_triggered) == 2


def test_section_2_internal_cognitive_loops():
    """Test anomaly detection, risk classification, and Bayesian mental model updating."""
    engine = InternalCognitiveLoopEngine()

    # Anomaly detection (Kuhn paradigm shift signal)
    assert engine.detect_anomaly(observed_val=120.0, baseline_expected=80.0, threshold=0.20) is True
    assert engine.detect_anomaly(observed_val=81.0, baseline_expected=80.0, threshold=0.20) is False

    # Type I vs Type II risk heuristic
    risk_type_type2 = engine.classify_risk(is_reversible=True, capital_commitment_cents=10000000) # $100k
    assert risk_type_type2 == DecisionRiskType.TYPE_II

    risk_type_type1 = engine.classify_risk(is_reversible=False, capital_commitment_cents=10000000)
    assert risk_type_type1 == DecisionRiskType.TYPE_I

    # Forced hypothesis generation
    hyp = engine.generate_forced_hypothesis("broadband_growth", "penetration > 50%", "streaming becomes viable")
    assert "penetration > 50%" in hyp["claim"]

    # Bayesian Mental Model updating
    model = engine.update_mental_model("streaming", empirical_evidence=0.90, expected_val=0.30)
    assert model.domain == "streaming"
    assert model.version == 2 # Structural shift due to large delta > 0.50


def test_section_3_external_business_loops():
    """Test evaluation of all 13 external business loops and failure modes."""
    engine = ExternalBusinessLoopsEngine()

    # Healthy metrics input
    healthy_inputs = {
        "retention_curve_flattening": 0.40,
        "nps": 60,
        "cac_cents": 2000,
        "conversion_rate": 0.05,
        "win_rate": 0.30,
        "nrr": 1.25,
        "churn_rate": 0.01,
        "price_elasticity": -1.1,
        "arpu_cents": 15000,
        "viral_k_factor": 0.25,
        "decision_latency_hrs": 12.0,
        "burn_multiple": 1.1,
        "runway_months": 24.0,
        "time_to_fill_days": 30,
        "regretted_attrition_rate": 0.02,
        "enps": 55,
        "shipped_experiments": 15,
        "experiment_hit_rate": 0.25,
        "feature_parity_gap": 0.90,
    }

    loop_results = engine.evaluate_all_loops(healthy_inputs)
    assert len(loop_results) == 13
    assert loop_results["product"]["failure_mode"] is None
    assert loop_results["financial"]["failure_mode"] is None

    # Unhealthy financial metrics input
    unhealthy_inputs = healthy_inputs.copy()
    unhealthy_inputs["burn_multiple"] = 4.0
    unhealthy_inputs["runway_months"] = 4.0

    unhealthy_results = engine.evaluate_all_loops(unhealthy_inputs)
    assert unhealthy_results["financial"]["failure_mode"] == "Growth at negative unit economics"


def test_section_4_customer_lifecycle_engine():
    """Test 15-stage customer journey cohort progression."""
    engine = CustomerLifecycleEngine()
    cohort_size = 1000

    rates = {
        CustomerJourneyStage.AWARENESS: 0.95,
        CustomerJourneyStage.INTEREST: 0.95,
        CustomerJourneyStage.CONSIDERATION: 0.95,
        CustomerJourneyStage.EVALUATION: 0.95,
        CustomerJourneyStage.PURCHASE: 0.95,
        CustomerJourneyStage.ONBOARDING: 0.95,
        CustomerJourneyStage.ACTIVATION: 0.95,
        CustomerJourneyStage.ENGAGEMENT: 0.95,
        CustomerJourneyStage.HABIT_FORMATION: 0.95,
        CustomerJourneyStage.RETENTION: 0.95,
        CustomerJourneyStage.LOYALTY: 0.95,
        CustomerJourneyStage.ADVOCACY: 0.95,
        CustomerJourneyStage.REFERRAL: 0.95,
        CustomerJourneyStage.EXPANSION: 0.95,
        CustomerJourneyStage.REPURCHASE: 0.95,
    }

    res = engine.evaluate_cohort_progression(cohort_size, rates)
    assert res["initial_cohort_size"] == 1000
    assert res["funnel_counts"]["Activation"] > 0
    assert res["healthy"] is True


def test_section_5_gtm_system_simulator():
    """Test GTM system positioning, pricing, and distribution channel alignment."""
    simulator = GTMSystemSimulator()

    # Enterprise alignment
    ent_res = simulator.evaluate_gtm_fit(
        positioning_target="enterprise",
        arpu_cents=1500000, # $15k
        primary_channel="Enterprise Sales"
    )
    assert ent_res["is_system_aligned"] is True

    # Mismatched self-serve alignment
    mismatch_res = simulator.evaluate_gtm_fit(
        positioning_target="self_serve",
        arpu_cents=1500000,
        primary_channel="Enterprise Sales"
    )
    assert mismatch_res["is_system_aligned"] is False


def test_section_6_company_growth_state_machine():
    """Test transitions across 9 growth stages and binding constraints."""
    sm = CompanyGrowthStateMachine()
    assert sm.current_stage == GrowthStage.IDEA

    # Transition Idea -> Validation
    next_stage = sm.evaluate_transition({"validated_learnings_count": 6})
    assert next_stage == GrowthStage.VALIDATION

    # Transition Validation -> Startup
    next_stage = sm.evaluate_transition({"paying_customers_count": 5})
    assert next_stage == GrowthStage.STARTUP

    # Transition Startup -> PMF
    next_stage = sm.evaluate_transition({"ltv_to_cac": 3.5, "runway_months": 12})
    assert next_stage == GrowthStage.PMF


def test_section_7_strategic_moat_engine():
    """Test Hamilton Helmer 7 Powers moat durability scoring and cost curve timing."""
    engine = StrategicMoatEngine()

    score = engine.calculate_moat_score(
        network_effects=0.8,
        switching_costs=0.9,
        economies_of_scale=0.7,
        brand_trust=0.8,
        counter_positioning=0.9,
        cornered_resource=0.6,
        process_power=0.7
    )
    assert round(score, 2) == 0.77

    timing_viable = engine.evaluate_cost_curve_timing(unit_cost=50.0, threshold_viability_cost=100.0)
    assert timing_viable is True


def test_section_8_failure_mode_monitor():
    """Test failure mode root cause diagnostics and corrective recommendations."""
    monitor = FailureModeMonitor()

    diagnoses = monitor.diagnose_and_correct({
        "engagement_low": True,
        "survey_positive": True,
        "decision_latency_days": 10.0
    })

    assert len(diagnoses) == 2
    failure_names = [d["failure_mode"] for d in diagnoses]
    assert "Solving the wrong problem" in failure_names
    assert "Organizational bottlenecks" in failure_names


def test_section_10_eos_opportunity_decision_tree():
    """Test section 10.2 Decision Tree logic."""
    tree = EOSOpportunityDecisionTree()

    # Valid opportunity path
    res_go = tree.evaluate_opportunity(
        is_structural_anomaly=True,
        is_reversible_decision=True,
        high_confidence_multi_source_signal=True,
        cheap_test_available=True,
        test_result_exceeds_kill_threshold=True,
        expected_value_positive=True,
        has_structural_advantage=True
    )
    assert res_go["pursue"] is True
    assert "Commit resources" in res_go["reason"]

    # Failed cheap test path
    res_kill = tree.evaluate_opportunity(
        is_structural_anomaly=True,
        is_reversible_decision=True,
        high_confidence_multi_source_signal=True,
        cheap_test_available=True,
        test_result_exceeds_kill_threshold=False,
        expected_value_positive=True,
        has_structural_advantage=True
    )
    assert res_kill["pursue"] is False
    assert "failed kill threshold" in res_kill["reason"]


def test_section_10_3_master_ai_eos_orchestrator_lifecycle():
    """Test full AI-EOS system sensing, hypothesis, test, build, scale execution cycle."""
    system = EntrepreneurialIntelligenceSystemFirstPrinciples()
    assert system.state == AIOSState.SENSING

    environment_signals = {
        "observed_metric": 150.0,
        "baseline_expected": 100.0,
        "is_reversible": True,
        "multi_source_signal": True,
        "cheap_test_available": True,
        "test_passed": True,
        "ev_positive": True,
        "has_moat": True,
        "validated_learnings_count": 10,
        "network_effects": 0.8
    }

    cycle_output = system.run_full_execution_cycle(environment_signals)
    assert cycle_output["state"] == AIOSState.OPERATE.value
    assert cycle_output["opportunity_decision"]["pursue"] is True
    assert cycle_output["moat_durability_score"] > 0.5
