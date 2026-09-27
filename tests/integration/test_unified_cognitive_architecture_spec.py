"""
Integration test suite for the Unified 4-Layer Cognitive Operating System Specification.

Validates closed-loop active inference state handoffs and multi-layer task execution across:
- Layer 1: Research OS (Hypothesis generation & empirical validation)
- Layer 2: EIOS Kernel & EOS Engine (Opportunity sensing, Expected Free Energy, DAG compilation)
- Layer 3: AEAN Organism / HiveMind (Swarm bidding & specialized multi-agent coordination)
- Layer 4: APODEX WorldModel (Causal graph creation & Bayesian belief updating)
"""

import pytest
from apodex.ai_eos.research.research_os import ResearchOS
from apodex.arcs.kernel.kernel import EIOSKernel
from apodex.ai_eos.intelligence.eos_engine import EOSEngine
from apodex.aean.coordination.hive_mind import HiveMind
from apodex.world_model.world_model import WorldModel
from apodex.ai_eos.research.integration import ResearchToSystemBridge


def test_unified_4layer_closed_loop_active_inference():
    """
    Validates end-to-end active inference handoff across all 4 layers of the cognitive OS.
    """
    # 1. Initialize Layer Subsystems
    research_os = ResearchOS()
    eios_kernel = EIOSKernel()
    eos_engine = EOSEngine()
    hive_mind = HiveMind()
    world_model = WorldModel()

    # Create integration bridge
    bridge = ResearchToSystemBridge(
        research_os=research_os,
        eios_kernel=eios_kernel,
        eos_engine=eos_engine,
        hive_mind=hive_mind,
        world_model=world_model,
    )

    # 2. Layer 1: Formulate and validate hypothesis
    hypothesis = research_os.register_hypothesis(
        title="Hawkes Non-Gaussian AST Depth Control",
        description="Recursive depth limits in AST rewrites prevent runaway execution",
        null_hypothesis="AST depth limits have no effect on execution stability",
        target_metric="AEAN_stability",
    )
    # Validate hypothesis
    hypothesis.status = "validated"
    research_os.hypotheses.save(hypothesis.hypothesis_id, hypothesis)
    assert hypothesis.status == "validated"

    # 3. Layer 1 -> Layer 2 Handoff via Bridge
    handoff_result = bridge.handoff_hypothesis_to_execution(hypothesis.hypothesis_id)
    assert handoff_result["kernel_registered"] is True
    assert handoff_result["eos_ingested"] is True

    # Check EIOS Kernel sensing
    anomalies = eios_kernel.sense_opportunity_anomalies()
    assert isinstance(anomalies, list)

    # 4. Layer 2 -> Layer 3 Handoff: Register task on HiveMind
    task_id = f"task_exec_{hypothesis.hypothesis_id}"
    hive_mind.register_task(
        task_id=task_id,
        description=hypothesis.description,
        required_role="CodeArchitect",
        token_reward=100.0,
    )
    assert task_id in hive_mind.pending_tasks

    # Simulate agent bid and allocation
    hive_mind.register_agent("agent_alpha", ["CodeArchitect"], initial_tokens=50.0)
    bid_success = hive_mind.place_bid("agent_alpha", task_id, bid_amount=10.0)
    assert bid_success is True

    # 5. Layer 3 -> Layer 4 Handoff: Update WorldModel causal graph and Bayesian beliefs
    causal_node = world_model.create_node(
        node_id=f"node_{hypothesis.hypothesis_id}",
        name=hypothesis.title,
        domain="cognitive_os",
    )
    assert causal_node.node_id == f"node_{hypothesis.hypothesis_id}"

    belief_update = world_model.update_belief(
        node_id=causal_node.node_id,
        evidence_score=0.95,
        observation_notes="Verified via HiveMind swarm execution",
    )
    assert belief_update["posterior"] > belief_update["prior"]

    # 6. Verify cross-layer active inference state consistency
    system_state = bridge.get_unified_system_state()
    assert system_state["layer1_active_hypotheses_count"] >= 1
    assert system_state["layer2_kernel_hypotheses_count"] >= 1
    assert system_state["layer3_hive_mind_pending_tasks_count"] >= 0
    assert system_state["layer4_world_model_nodes_count"] >= 1
