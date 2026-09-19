# -*- coding: utf-8 -*-
"""
test_unified_cognitive_os_e2e.py: End-to-end integration test suite
validating joint cross-layer active inference interactions across:
- Layer 1: Research OS (Hypothesis generation, power analysis & statistical validation)
- Layer 2: EIOS Kernel (Active inference sensing) & EOS Engine (Opportunity evaluation & state transitions)
- Layer 3: AEAN HiveMind (Token-bounded bidding & multi-agent resource allocation)
- Layer 4: APODEX WorldModel (Causal graph node creation & Bayesian belief updates)
"""

from __future__ import annotations
import pytest
from uuid import uuid4

from apodex.ai_eos.research.research_os import ResearchOS
from apodex.arcs.kernel.kernel import EIOSKernel
from apodex.ai_eos.intelligence.eos_engine import EOSEngine
from apodex.aean.coordination.hive_mind import HiveMind, TaskBid
from apodex.world_model.world_model import WorldModel, CausalNode
from apodex.ai_eos.research.integration import (
    ResearchToSystemBridge,
    CodeRewriteEngine,
    GeneticWorkflowOptimizer,
    SFTPreferenceCollector,
    LearnableRoutingGateDispatcher,
    SpecializedAgentProfile,
    TrajectoryStep,
)


def test_e2e_research_to_system_bridge_active_inference_handoff() -> None:
    """Tests full cross-layer propagation of a validated scientific hypothesis across L1-L4."""
    # 1. Initialize Subsystem Stack
    research_os = ResearchOS()
    eios_kernel = EIOSKernel()
    eos_engine = EOSEngine()
    hive_mind = HiveMind(token_budget=100)
    world_model = WorldModel()

    bridge = ResearchToSystemBridge(
        research_os=research_os,
        eios_kernel=eios_kernel,
        eos_engine=eos_engine,
        hive_mind=hive_mind,
        world_model=world_model,
    )

    # 2. Layer 1: Register and validate hypothesis in Research OS
    hyp = research_os.register_hypothesis(
        title="Hawkes Process Active Inference Routing",
        description="Non-Gaussian Hawkes self-excitation reduces agent routing latency.",
        null_hypothesis="Hawkes routing has no effect on latency.",
        target_metric="latency_ms",
        significance_alpha=0.05,
    )

    exp = research_os.create_experiment(hyp.hypothesis_id, seed=123)
    completed_exp = research_os.execute_experiment_simulation(
        exp.experiment_id, ground_truth_yield=2.5
    )

    assert hyp.status == "validated"
    assert completed_exp.is_statistically_significant is True

    # 3. Propagate validated research across system bridge to L2, L3, and L4
    handoff = bridge.propagate_validated_hypothesis(
        hypothesis_id=hyp.hypothesis_id,
        title=hyp.title,
        target_metric=hyp.target_metric,
        p_value=completed_exp.p_value,
        effect_size=completed_exp.effect_size,
        commercial_value=1500.0,
    )

    assert "L2_EIOS_Kernel" in handoff["layers_updated"]
    assert "L2_EOS_Engine" in handoff["layers_updated"]
    assert "L3_AEAN_HiveMind" in handoff["layers_updated"]
    assert "L4_APODEX_WorldModel" in handoff["layers_updated"]

    # 4. Verify Layer 2: EOS Engine received hypothesis
    assert len(eos_engine.active_hypotheses) == 1
    assert eos_engine.active_hypotheses[0]["title"] == hyp.title

    # 5. Verify Layer 3: AEAN HiveMind bidding
    bids = [
        TaskBid(task="execute_hawkes_routing", priority=0.9, expected_value=1.5, token_cost=20),
        TaskBid(task="routine_maintenance", priority=0.2, expected_value=0.1, token_cost=10),
    ]
    grants = hive_mind.arbitrate(bids)
    granted = hive_mind.granted_tasks(grants)
    assert granted["execute_hawkes_routing"] is True

    # 6. Verify Layer 4: APODEX WorldModel belief & causal node state
    node_id = f"hyp_{hyp.hypothesis_id}"
    wm_node = world_model.nodes.get(node_id)
    assert wm_node is not None
    assert wm_node.properties["status"] == "validated"
    assert node_id in world_model.beliefs
    assert world_model.beliefs[node_id]["posterior_probability"] > 0.95


def test_e2e_transferable_engineering_modules_integration() -> None:
    """Verifies joint execution of transferable research modules across cognitive components."""
    # 1. Genetic Workflow Optimizer (ShinkaEvolve MAP-Elites)
    optimizer = GeneticWorkflowOptimizer(population_size=4, mutation_rate=0.3)
    optimizer.initialize_population(
        base_template="Optimize active inference expected free energy.",
        base_params={"lr": 0.01, "curiosity": 0.5},
    )
    optimizer.evaluate_generation(lambda g: g.parameters.get("curiosity", 0.0) * 2.0)
    optimizer.perform_crossover_and_mutation()
    assert len(optimizer.population) == 4

    # 2. Preference Collector (DPO Temporal-Difference Advantage Margin)
    collector = SFTPreferenceCollector(discount_factor=0.9)
    traj_a = [TrajectoryStep(action="a1", predicted_expectation=0.2, actual_outcome=0.8, reward=0.8)]
    traj_b = [TrajectoryStep(action="b1", predicted_expectation=0.2, actual_outcome=0.3, reward=0.3)]
    dpo_pair = collector.compile_dpo_preference_pair("Prompt task", traj_a, traj_b)
    assert dpo_pair["margin"] > 0.0

    # 3. Learnable Routing Gate Dispatcher (Uno-Orchestra EFE)
    dispatcher = LearnableRoutingGateDispatcher(budget_limit_usd=10.0)
    dispatcher.register_subagent(
        SpecializedAgentProfile(
            agent_id="solver_1",
            domain_specialty="Research",
            cost_per_token=0.002,
            historical_success_rate=0.8,
            epistemic_curiosity=0.6,
        )
    )
    selected = dispatcher.route_task(task_complexity=100, domain="Research")
    assert selected == "solver_1"
