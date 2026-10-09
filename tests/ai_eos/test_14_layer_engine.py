"""
Unit and integration tests for the 14-Layer Computational Architecture Engine.
"""

import pytest
from apodex.ai_eos.intelligence import (
    FourteenLayerEntrepreneurshipEngine,
    Layer1RealityEngine,
    Layer2OpportunitySearchEngine,
    Layer3ProblemDecompositionEngine,
    Layer4DecisionEngineUnderUncertainty,
    Layer5OpportunityEvaluator,
    Layer6ProductCreationEngine,
    Layer7CustomerPsychologyEngine,
    Layer8MarketFormationEngine,
    Layer9SalesDynamicsEngine,
    Layer10CompoundingGrowthEngine,
    Layer11CompetitiveMoatEngine,
    Layer12OrganizationalDesignEngine,
    Layer13MetaLearningEngine,
    Layer14AutonomousOrchestratorEngine,
)

def test_individual_layers():
    l1 = Layer1RealityEngine()
    res1 = l1.evaluate_invariant_grounding({"upside_potential": 10.0, "downside_loss": 2.0, "knowledge_gained": 2.0, "capital_expended": 1.0})
    assert res1["grounded"] is True

    l2 = Layer2OpportunitySearchEngine()
    res2 = l2.search_state_space([{"title": "Autonomous Agent", "kl_divergence": 0.9, "signal_strength": 0.1, "growth_acceleration": 0.5}])
    assert len(res2) == 1
    assert res2[0]["is_weak_signal"] is True

    l3 = Layer3ProblemDecompositionEngine()
    res3 = l3.decompose_root_cause({"symptoms": ["latency"], "causal_nodes": ["DB", "Query", "Index"]})
    assert res3["isolated_root_cause"] == "Index"

    l4 = Layer4DecisionEngineUnderUncertainty()
    res4 = l4.compute_efe_decision(prior_entropy=1.0, p_success=0.8, p_target=0.9)
    assert "efe" in res4

    l5 = Layer5OpportunityEvaluator()
    res5 = l5.evaluate_opportunity(tam_cents=100000000, p_success=0.5, loss_cents=1000000)
    assert res5["proceed"] is True

    l6 = Layer6ProductCreationEngine()
    res6 = l6.optimize_jtbd_features([{"name": "useful", "value": 2.0, "complexity": 1.0}, {"name": "useless", "value": 0.1, "complexity": 2.0}])
    assert "useful" in res6["approved_features"]
    assert "useless" not in res6["approved_features"]

    l7 = Layer7CustomerPsychologyEngine()
    res7 = l7.evaluate_customer_utility(pain=10.0, gain=10.0, switching_cost=1.0, price=2.0)
    assert res7["will_buy"] is True

    l8 = Layer8MarketFormationEngine()
    res8 = l8.calculate_virality_and_positioning(transmission_rate=1.2, recovery_rate=0.5)
    assert res8["is_viral"] is True

    l9 = Layer9SalesDynamicsEngine()
    res9 = l9.determine_sales_strategy(acv_usd=150000.0, multi_stakeholder=True)
    assert res9["recommended_strategy"] == "enterprise_field_sales"

    l10 = Layer10CompoundingGrowthEngine()
    res10 = l10.compute_network_value(user_base=100, network_type="direct")
    assert res10["network_value"] == 10000

    l11 = Layer11CompetitiveMoatEngine()
    res11 = l11.evaluate_moat_defensibility(switching_cost=0.9, scale_advantage=0.8)
    assert res11["is_defensible"] is True

    l12 = Layer12OrganizationalDesignEngine()
    res12 = l12.evaluate_hiring_and_structure(utilization_rate=0.95, team_size=20)
    assert res12["should_hire"] is True
    assert res12["recommended_structure"] == "modular_squads"

    l13 = Layer13MetaLearningEngine()
    res13 = l13.evaluate_decision_quality(predicted_p=0.9, actual_outcome=1.0)
    assert res13["brier_score"] == pytest.approx(0.01)

    l14 = Layer14AutonomousOrchestratorEngine()
    res14 = l14.allocate_capital_and_compute(capital_reserve=100000.0, opportunities=[{"title": "Opp A"}])
    assert res14["status"] == "autonomous_execution_active"

def test_full_14_layer_pipeline():
    engine = FourteenLayerEntrepreneurshipEngine()
    signal = {"title": "Autonomous AI Startup", "kl_divergence": 0.85, "upside_potential": 12.0, "downside_loss": 1.5}
    res = engine.run_full_14_layer_pipeline(signal)
    assert res["status"] == "completed"
    assert "layer_1_reality" in res
    assert "layer_14_autonomous_orchestrator" in res
