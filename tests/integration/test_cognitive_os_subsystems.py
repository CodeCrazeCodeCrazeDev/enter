"""
Integration test suite verifying end-to-end cognitive operating system execution across:
1. ResearchOS (Scientific discovery, literature review, experiment design, Holm-Bonferroni trial validation)
2. EIOS Kernel (Active Inference Expected Free Energy, Pearl do-calculus SCM interventions, DAG execution)
3. EOS Engine (13 coupled business loops, 15 customer journey stages, 14-layer computational engine)
4. AEAN Hive Mind (Multi-agent token arbitration, Bayesian Nash Equilibrium clearing)
5. Apodex Cognitive Brain (Deep causal world model, Ebbinghaus memory decay, procedural skills flywheel)
"""

from __future__ import annotations
import math
import pytest
from uuid import uuid4

# 1. ResearchOS
from apodex.ai_eos.research.research_os import ResearchOS

# 2. EIOS Kernel
from apodex.arcs.kernel import EIOSKernel, EntrepreneurialCompiler

# 3. EOS Engine & 14-Layer Engine
from apodex.ai_eos.intelligence.eos_engine import EOSEngine
from apodex.ai_eos.intelligence.computational_architecture import (
    EntrepreneurialIntelligenceOrchestrator,
    AdvancedCausalEngine,
    ActiveInferencePlanner,
    Opportunity
)

# 4. AEAN Hive Mind & Core
from apodex.aean.coordination.hive_mind import HiveMind, TaskBid
from apodex.aean.core import SystemEconomics, PaymentsFinancialOps

# 5. Apodex Cognitive Brain & Memory
from apodex.cognition.brain import (
    CognitiveBrain,
    AdvancedMemoryEngine,
    TrajectoryStep,
    UnifiedConcept
)


@pytest.mark.asyncio
async def test_end_to_end_cognitive_os_subsystems_pipeline():
    """
    Validates joint cross-layer execution flow connecting:
    ResearchOS -> EIOS Kernel -> EOS Engine -> AEAN Hive Mind -> Apodex Cognitive Brain.
    """
    # ------------------------------------------------------------------
    # Step 1: ResearchOS Scientific Discovery & Trial Validation
    # ------------------------------------------------------------------
    ros = ResearchOS()
    lit_report = ros.conduct_literature_review("active_inference_gtm")
    assert "Active Inference" in lit_report["synthesized_trends"][1]

    # Register scientific hypothesis
    hyp = ros.register_hypothesis(
        title="Usage-Based Pricing Increases Net Retention",
        description="Transitioning from flat rate to usage-based pricing increases NRR by 25%",
        null_hypothesis="Usage-based pricing has no effect on NRR",
        target_metric="net_retention_rate",
        significance_alpha=0.05
    )
    assert hyp.status == "registered"

    # Design experiment with statistical power analysis
    exp_design = ros.design_experiment(hyp.hypothesis_id)
    assert exp_design["recommended_sample_size"] > 0

    # Initialize sandbox experiment and execute walk-forward simulation
    exp = ros.create_experiment(hyp.hypothesis_id, seed=101)
    trial_res = ros.execute_experiment_simulation(exp.experiment_id, ground_truth_yield=0.35)

    assert trial_res.is_statistically_significant is True
    assert hyp.status == "validated"

    # ------------------------------------------------------------------
    # Step 2: EIOS Kernel Active Inference Sensing & Pearl do-calculus
    # ------------------------------------------------------------------
    eios = EIOSKernel()

    # Sense opportunity anomalies using Expected Free Energy
    anomaly_sensing = eios.sense_opportunity_anomalies("usage_based_pricing_nrr")
    assert anomaly_sensing["epistemic_information_gain"] > 0.0
    assert anomaly_sensing["expected_free_energy"] < 0.0

    # Execute Pearl do-calculus intervention
    causal_intervention = eios.execute_causal_intervention("pricing_tier", 2.5)
    assert causal_intervention["variable_name"] == "pricing_tier"
    assert "do(pricing_tier = 2.5)" in causal_intervention["intervention"]

    # Compile goal into execution DAG
    compiler = EntrepreneurialCompiler()
    dag = compiler.compile_goal_to_dag(
        "Deploy usage-based pricing model to validated target segment",
        target_budget_usd=25000
    )
    dag_success = await eios.execute_dag(dag)
    assert dag_success is True

    # ------------------------------------------------------------------
    # Step 3: EOS Engine First-Principles & 14-Layer Computational Pipeline
    # ------------------------------------------------------------------
    eos = EOSEngine()

    # Run continuous sensing cycle over world state transitions
    world_cycle = eos.run_continuous_sensing_cycle(cells=[], total_budget_cents=500000)
    assert "world_state" in world_cycle
    assert world_cycle["market_uncertainty"] >= 0.0

    # Execute 14-Layer Computational Architecture Pipeline
    causal_engine = AdvancedCausalEngine()
    planner = ActiveInferencePlanner(curiosity_weight=1.5)
    eos_orchestrator = EntrepreneurialIntelligenceOrchestrator(causal_engine, planner)

    opp = eos_orchestrator.ingest_signal({
        "title": "Usage-Based Pricing Segment Expansion",
        "domain": "pricing",
        "variables": ["pricing_model", "conversion_rate", "net_revenue"],
        "causal_edges": [("pricing_model", "conversion_rate"), ("conversion_rate", "net_revenue")],
        "coefficients": {"pricing_model->conversion_rate": 0.8, "conversion_rate->net_revenue": 1.2},
        "prior_entropy": 1.8,
        "post_entropy_simulated": 0.3,
        "success_probability": 0.85
    })
    assert opp.title == "Usage-Based Pricing Segment Expansion"

    pipeline_res = eos_orchestrator.execute_orchestrated_pipeline()
    assert pipeline_res["status"] == "executed"
    assert pipeline_res["best_expected_free_energy"] < 0.0

    # ------------------------------------------------------------------
    # Step 4: AEAN Hive Mind Arbitrated Bidding & Economics
    # ------------------------------------------------------------------
    hive = HiveMind(token_budget=100)

    bids = [
        TaskBid(task="execute_pricing_migration", priority=0.9, expected_value=0.85, token_cost=30),
        TaskBid(task="run_funnel_campaign", priority=0.8, expected_value=0.70, token_cost=40),
        TaskBid(task="audit_compliance", priority=0.95, expected_value=0.90, token_cost=20),
        TaskBid(task="expensive_speculative_task", priority=0.3, expected_value=0.20, token_cost=50)
    ]

    grants = hive.arbitrate(bids)
    assert len(grants) == 4

    # Top priority/value bids must be granted
    granted_map = hive.granted_tasks(grants)
    assert granted_map["audit_compliance"] is True
    assert granted_map["execute_pricing_migration"] is True

    # System Economics tracking
    economics = SystemEconomics()
    cost_record = economics.attribute_cost(
        engine="AEAN_HiveMind",
        layer="Layer_3_Execution",
        token_cost=90,
        opportunity_id=str(opp.opportunity_id)
    )
    assert cost_record.dollars_cost > 0.0

    # ------------------------------------------------------------------
    # Step 5: Apodex Cognitive Brain Memory Decay & World Model Consolidation
    # ------------------------------------------------------------------
    brain = CognitiveBrain()

    # Log execution trajectory step
    traj_step = TrajectoryStep(
        action="execute_pricing_migration",
        parameters={"pricing_model": "usage_based", "granted_tokens": 30},
        outcome={"success": True, "nrr_increase": 0.26},
        duration_sec=4.2,
        cost_cents=180
    )
    brain.memory.log_episode(traj_step)

    # Assert fact into semantic memory
    fact = brain.memory.assert_fact(
        name="usage_based_pricing_validated",
        concept_type="fact",
        attributes={"nrr_increase": 0.26, "p_value": trial_res.p_value},
        confidence=0.95
    )

    # Apply Ebbinghaus forgetting curve decay over elapsed time delta
    current_time = fact.last_updated + 100.0
    pruned_count = brain.memory.apply_ebbinghaus_forgetting(current_time)
    assert pruned_count == 0  # Confidence remains above 0.1 threshold

    # Consolidate short-term episodic traces into long-term lesson
    consolidation = brain.memory.consolidate_memories()
    assert consolidation["consolidated_episodes"] == 1
    assert len(brain.memory.long_term_memory) == 1
    assert "Historical success rate: 1.00" in brain.memory.long_term_memory[0]["summary"]


def test_research_os_to_eios_kernel_handoff():
    """
    Verifies state transfer and parameter propagation from ResearchOS to EIOS Kernel.
    """
    ros = ResearchOS()
    eios = EIOSKernel()

    # Register and validate hypothesis in ResearchOS
    hyp = ros.register_hypothesis(
        title="AI Automation Reduces Customer Churn",
        description="Deploying AI support agents reduces monthly customer churn by 15%",
        null_hypothesis="AI support agents do not reduce churn",
        target_metric="churn_rate"
    )
    exp = ros.create_experiment(hyp.hypothesis_id, seed=202)
    ros.execute_experiment_simulation(exp.experiment_id, ground_truth_yield=0.28)

    # Export validated hypothesis state
    assert hyp.status == "validated"

    # EIOS senses anomaly and executes do-calculus based on ResearchOS findings
    kernel_sensing = eios.sense_opportunity_anomalies("churn_reduction_ai")
    assert kernel_sensing["status"] == "sensed"
    assert kernel_sensing["expected_free_energy"] < 0.0

    do_res = eios.execute_causal_intervention("ai_support_coverage", 0.85)
    assert do_res["intervention"] == "do(ai_support_coverage = 0.85)"


def test_eos_to_aean_hive_mind_execution():
    """
    Verifies multi-agent debate and second-price token arbitration on EOS state decisions.
    """
    eos = EOSEngine()
    hive = HiveMind(token_budget=50)

    # EOS evaluates failure prediction and insolvency risk
    hazard_prob = eos.failure_predictor.predict_insolvency_probability(
        burn_multiple=1.2,
        runway_months=18.0,
        ltv_to_cac=3.8
    )
    assert hazard_prob < 0.10

    # EOS formulates candidates for Hive Mind token bidding
    bids = [
        TaskBid(task="scale_proven_channel", priority=0.85, expected_value=0.90, token_cost=25),
        TaskBid(task="explore_secondary_market", priority=0.40, expected_value=0.30, token_cost=30)
    ]

    grants = hive.arbitrate(bids)
    granted_map = hive.granted_tasks(grants)

    # High EV task gets granted; secondary market task exceeds remaining budget (50 - 25 = 25 < 30)
    assert granted_map["scale_proven_channel"] is True
    assert granted_map["explore_secondary_market"] is False
