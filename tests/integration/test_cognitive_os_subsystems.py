# -*- coding: utf-8 -*-
"""
test_cognitive_os_subsystems.py: End-to-end multi-layer integration test suite
validating seamless cross-layer active inference interactions across:
  - Layer 1: Research OS
  - Layer 2: EIOS Kernel & EOS Engine
  - Layer 3: AEAN HiveMind
  - Layer 4: APODEX WorldModel
"""

import pytest
import asyncio
from uuid import uuid4

from apodex.ai_eos.research.research_os import ResearchOS
from apodex.ai_eos.intelligence.eos_engine import EOSEngine
from apodex.arcs.kernel.kernel import EIOSKernel, ExecutionDAG, ExecutionNode
from apodex.aean.coordination.hive_mind import HiveMind, TaskBid
from apodex.world_model.world_model import WorldModel
from apodex.ai_eos.research.integration import ResearchToSystemBridge


def test_cross_layer_hypothesis_propagation():
    """Verify hypothesis propagation from ResearchOS through bridge into Kernel, EOS, HiveMind, and WorldModel."""
    # 1. Initialize Subsystems
    ros = ResearchOS()
    kernel = EIOSKernel()
    eos = EOSEngine()
    hive = HiveMind(token_budget=100)
    world = WorldModel()

    # 2. Instantiate Cross-Layer Bridge
    bridge = ResearchToSystemBridge(
        research_os=ros,
        kernel=kernel,
        eos_engine=eos,
        hive_mind=hive,
        world_model=world
    )

    # 3. Register and Statistically Validate Hypothesis in Layer 1
    hyp = ros.register_hypothesis(
        title="GRPO Active Inference Acceleration",
        description="GRPO policy optimization reduces expected free energy by 35% in micro-VM environments.",
        null_hypothesis="GRPO does not reduce free energy.",
        target_metric="free_energy_reduction",
        significance_alpha=0.05
    )
    exp = ros.create_experiment(hyp.hypothesis_id, seed=101)
    validated_exp = ros.execute_experiment_simulation(exp.experiment_id, ground_truth_yield=2.5)

    assert hyp.status == "validated"
    assert validated_exp.is_statistically_significant

    # 4. Execute Cross-Layer Handoff
    handoff_summary = bridge.execute_cross_layer_handoff(hyp)

    # Assertions across all layers
    assert handoff_summary["hypothesis_id"] == str(hyp.hypothesis_id)
    assert handoff_summary["sensing_node_id"] is not None
    assert handoff_summary["eos_promoted"] is True
    assert handoff_summary["aean_bid_created"] is True
    assert handoff_summary["world_model_updated"] is True

    # Check Layer 2 EOS Engine state
    assert hyp.hypothesis_id in eos.hypothesis_engine.hypotheses

    # Check Layer 4 WorldModel state
    node_id = f"hypothesis_{hyp.hypothesis_id}"
    assert node_id in world.nodes
    assert node_id in world.beliefs
    assert world.beliefs[node_id]["posterior_confidence"] == hyp.posterior_confidence


def test_active_inference_state_handoff():
    """Verify free energy and task bidding state handoffs across EIOS Kernel, AEAN HiveMind, and WorldModel."""
    kernel = EIOSKernel()
    hive = HiveMind(token_budget=50)
    world = WorldModel()

    # Create and execute an EIOS Execution DAG
    dag = ExecutionDAG()
    node = ExecutionNode(name="Research Sensing Cycle", action_type="research_sensing", payload={"domain": "ai_eos"})
    dag.add_node(node)

    # Run DAG execution
    asyncio.run(kernel.execute_dag(dag))
    assert node.status == "COMPLETED"

    # AEAN HiveMind arbitration
    bids = [
        TaskBid(task="High Priority Free Energy Optimization", priority=0.9, expected_value=0.85, token_cost=20),
        TaskBid(task="Low Priority Background Maintenance", priority=0.2, expected_value=0.10, token_cost=40)
    ]
    grants = hive.arbitrate(bids)
    granted_map = hive.granted_tasks(grants)

    assert granted_map["High Priority Free Energy Optimization"] is True
    assert granted_map["Low Priority Background Maintenance"] is False
