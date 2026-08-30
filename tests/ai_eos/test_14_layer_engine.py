"""
Unit and integration tests for the 14-Layer Computational Architecture of Entrepreneurship.
"""

import pytest
from apodex.ai_eos.intelligence.fourteen_layer_engine import (
    Layer1_Reality,
    Layer2_OpportunityDiscovery,
    WorldStateSignal,
    Layer3_ProblemDiscovery,
    Layer4_DecisionMaking,
    Layer5_OpportunityEvaluation,
    Layer6_ProductCreation,
    Layer7_CustomerUnderstanding,
    CustomerProfileState,
    Layer8_Marketing,
    Layer9_Sales,
    Layer10_Growth,
    Layer11_Competition,
    Layer12_OrgDesign,
    Layer13_MetaLearning,
    FourteenLayerEntrepreneurshipEngine,
)


def test_layer1_reality_boundary():
    layer1 = Layer1_Reality()
    res_auto = layer1.evaluate_task_automation_boundary("Weak signal trend scanning", 0.5)
    assert res_auto["is_automatable"] is True
    assert res_auto["requires_human_judgment"] is False

    res_human = layer1.evaluate_task_automation_boundary("Existential pivot vision under total informational blackout", 0.95)
    assert res_human["is_automatable"] is False
    assert res_human["requires_human_judgment"] is True


def test_layer2_opportunity_discovery():
    layer2 = Layer2_OpportunityDiscovery(noise_filter_threshold=0.2)
    sig1 = WorldStateSignal(source_domain="AI_Compute", raw_magnitude=3.5, noise_variance=0.1, features={"growth": 0.8})
    sig2 = WorldStateSignal(source_domain="Noise_Domain", raw_magnitude=0.01, noise_variance=1.0)

    opps = layer2.search_state_space([sig1, sig2])
    assert len(opps) == 1
    assert opps[0].domain == "AI_Compute"
    assert opps[0].detected_weak_signal_strength > 0.0

    fused = layer2.combine_unrelated_observations({"gpu": 10.0}, {"bio": 5.0})
    assert fused["cross_domain_novelty"] == 50.0


def test_layer3_problem_discovery_scm():
    layer3 = Layer3_ProblemDiscovery()
    causal_graph = {
        "Suboptimal_Product_Architecture": ["High_Latency", "Customer_Churn"],
        "High_Latency": ["Negative_Reviews"]
    }

    decomp = layer3.decompose_problem(
        stated_problem="High Customer Churn",
        observed_symptoms=["High_Latency", "Customer_Churn", "Negative_Reviews"],
        causal_graph=causal_graph,
        impact_score=0.8
    )

    assert decomp.true_root_cause == "Suboptimal_Product_Architecture"
    assert decomp.is_second_order is True
    assert decomp.triage_action == "SOLVE"


def test_layer4_decision_making_efe():
    layer4 = Layer4_DecisionMaking()
    # High probability of success, low EFE
    res = layer4.make_decision(
        action_name="Launch MVP",
        p_success=0.8,
        p_target=0.9,
        prior_entropy=1.5,
        post_entropy=0.3,
        latency_budget_ms=50.0,
        active_counter_evidence_count=3
    )
    assert res.decision_mode == "DATA_DRIVEN_BAYESIAN"
    assert res.kill_flag is False

    # Fast kill trigger test
    res_kill = layer4.make_decision(
        action_name="Unviable Market",
        p_success=0.05,
        p_target=0.9,
        prior_entropy=1.0,
        post_entropy=0.9
    )
    assert res_kill.kill_flag is True


def test_layer5_opportunity_evaluation():
    layer5 = Layer5_OpportunityEvaluation()
    eval_res = layer5.evaluate_opportunity(
        tam_cents=100000000,
        conversion_rate=0.05,
        arpu_cents=20000,
        cogs_cents=4000,
        readiness_timing=0.9,
        risk_variance=0.04
    )
    assert eval_res.unit_economics_margin == 0.8
    assert eval_res.expected_value_cents > 0
    assert eval_res.abandonment_pivot_flag is False


def test_layer6_product_creation_jtbd():
    layer6 = Layer6_ProductCreation()
    proposed = {
        "Core Search Engine": 0.95,
        "Active Inference Solver": 0.90,
        "Custom Theme Customizer": 0.10
    }
    spec = layer6.build_product_spec(
        core_jtbd="Discover latent market opportunities",
        proposed_features=proposed,
        max_complexity_budget=50.0
    )
    assert "Core Search Engine" in spec.essential_features
    assert "Active Inference Solver" in spec.essential_features
    assert "Custom Theme Customizer" in spec.pruned_features


def test_layer7_customer_understanding():
    layer7 = Layer7_CustomerUnderstanding()
    initial_profile = CustomerProfileState(trust_index=0.6)
    updated = layer7.simulate_customer_lifecycle(
        profile=initial_profile,
        product_quality=0.9,
        onboarding_friction=0.1
    )
    assert updated.trust_index > initial_profile.trust_index
    assert updated.churn_probability < 0.5


def test_layer8_marketing_virality():
    layer8 = Layer8_Marketing()
    mkt = layer8.simulate_attention_dynamics(
        initial_susceptible=50000.0,
        virality_rate_beta=1.5,
        decay_rate_gamma=0.5,
        channel_diversity_count=3
    )
    assert mkt.virality_r0 == 3.0
    assert mkt.attention_reach > 0.0
    assert mkt.brand_authority_score > 0.0


def test_layer9_sales_systems():
    layer9 = Layer9_Sales()
    sales = layer9.process_sales_funnel(
        urgency=0.9,
        objections=["integration_time"],
        contract_value_cents=100000  # Self-serve threshold
    )
    assert sales.conversion_probability > 0.5
    assert sales.is_enterprise_deal is False
    assert sales.automation_recommended is True


def test_layer10_growth_and_ecosystem():
    layer10 = Layer10_Growth()
    growth = layer10.evaluate_growth_engine(
        user_count=10000,
        k_factor=1.3,
        system_load_capacity=5000.0
    )
    assert growth.network_effect_score > 0.0
    assert growth.intentional_growth_throttle is True  # Load capacity exceeded


def test_layer11_competition():
    layer11 = Layer11_Competition()
    comp = layer11.analyze_competition(
        proprietary_ip_weight=0.9,
        switching_cost_weight=0.8,
        competitor_velocity=0.3
    )
    assert comp.moat_score > 0.8
    assert comp.replication_barrier_months > 15.0
    assert comp.pivot_required_flag is False


def test_layer12_org_design():
    layer12 = Layer12_OrgDesign()
    org = layer12.optimize_org_structure(workload_units=50.0, current_headcount=2)
    assert org.hiring_trigger_flag is True
    assert "Capital allocation" in org.centralized_tasks
    assert "Feature implementation" in org.delegated_tasks


def test_layer13_meta_learning():
    layer13 = Layer13_MetaLearning()
    priors = {"prior_alpha": 0.5}
    meta = layer13.evaluate_and_update(
        predicted_probabilities=[0.8, 0.9, 0.7],
        actual_outcomes=[1, 1, 1],
        priors=priors
    )
    assert meta.brier_decision_score >= 0.0
    assert "prior_alpha" in meta.updated_prior_beliefs


def test_fourteen_layer_master_engine_integration():
    engine = FourteenLayerEntrepreneurshipEngine()
    signals = [
        WorldStateSignal(
            source_domain="Quantum_Computing",
            raw_magnitude=4.2,
            noise_variance=0.05,
            features={"market_pull": 0.85}
        )
    ]
    causal_graph = {"Underlying_Algorithmic_Friction": ["Execution_Bottleneck"]}
    priors = {"market_adoption_rate": 0.5}

    result = engine.execute_complete_pipeline(signals, causal_graph, priors)

    assert result["status"] == "pipeline_executed"
    assert len(result["layer1_reality_invariants"]) > 0
    assert result["layer2_discovered_opportunities_count"] == 1
    assert result["layer3_root_cause"] == "Underlying_Algorithmic_Friction"
    assert "layer4_decision_efe" in result
    assert result["layer5_expected_value_cents"] > 0
    assert len(result["layer6_product_essential_features"]) > 0
    assert result["layer7_customer_trust"] > 0.0
    assert result["layer8_virality_r0"] > 0.0
    assert result["layer9_sales_conversion_prob"] > 0.0
    assert result["layer10_network_score"] > 0.0
    assert result["layer11_moat_score"] > 0.0
    assert "layer12_hiring_needed" in result
    assert result["layer13_brier_score"] >= 0.0
    assert "capital_allocation_cents" in result["layer14_resource_allocation"]
