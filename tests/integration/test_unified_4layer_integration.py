"""Unified 4-Layer Cognitive Operating System Integration Tests.

Validates active inference state handoffs and joint execution across:
- Layer 1: Research OS
- Layer 2: EIOS Kernel & EOS Engine
- Layer 3: AEAN HiveMind
- Layer 4: APODEX WorldModel
"""

import pytest
from uuid import uuid4
from apodex.ai_eos.research.research_os import ResearchOS
from apodex.arcs.kernel.kernel import EIOSKernel
from apodex.ai_eos.intelligence.eos_engine import EOSEngine
from apodex.aean.coordination.hive_mind import HiveMind, TaskBid
from apodex.world_model.world_model import WorldModel
from apodex.ai_eos.research.integration import ResearchToSystemBridge


def test_research_to_kernel_handoff():
    ros = ResearchOS()
    kernel = EIOSKernel()
    bridge = ResearchToSystemBridge()

    hyp = ros.register_hypothesis("Quantum Market Predictor", "Predict volatility using quantum state vectors", "No effect", "sharpe_ratio")
    dag = bridge.handoff_research_to_kernel(hyp, kernel)

    assert dag.id in kernel.active_processes
    assert len(dag.nodes) == 1
    node = list(dag.nodes.values())[0]
    assert "EFE_Sensing" in node.name


def test_kernel_to_eos_handoff():
    eos = EOSEngine()
    bridge = ResearchToSystemBridge()

    kernel_output = {
        "hypothesis_id": str(uuid4()),
        "title": "Arbitrage Opportunity in SaaS B2B",
        "posterior_confidence": 0.88
    }

    eos_hyp = bridge.handoff_kernel_to_eos(kernel_output, eos)

    assert eos_hyp.hypothesis_id in eos.hypothesis_engine.hypotheses
    assert eos.hypothesis_engine.hypotheses[eos_hyp.hypothesis_id].posterior_confidence == 0.88


def test_eos_to_hive_mind_handoff():
    eos = EOSEngine()
    hive = HiveMind()
    bridge = ResearchToSystemBridge()

    node_id = "op_node_1"
    eos.opportunity_graph.add_opportunity(node_id, "Enterprise AI Copilot", 100000_00, ["ai", "enterprise", "copilot"])
    op_node = eos.opportunity_graph.nodes[node_id]

    task_id = bridge.handoff_eos_to_hive_mind(op_node, hive)

    assert task_id.startswith("task_hive_")


def test_hive_mind_to_world_model_handoff():
    wm = WorldModel()
    bridge = ResearchToSystemBridge()

    agent_results = {
        "node_id": "cnode_gtm_launch",
        "label": "GTM Campaign Execution",
        "domain": "marketing",
        "value": 1.5,
        "confidence": 0.92
    }

    causal_node = bridge.handoff_hive_mind_to_world_model(agent_results, wm)

    assert causal_node.node_id in wm.nodes
    assert wm.nodes[causal_node.node_id].properties["label"] == "GTM Campaign Execution"


def test_full_4layer_unified_active_inference_cycle():
    ros = ResearchOS()
    kernel = EIOSKernel()
    eos = EOSEngine()
    hive = HiveMind()
    wm = WorldModel()

    # 1. Layer 1 Research OS validates hypothesis
    hyp = ros.register_hypothesis("EFE Active Inference Engine", "Minimizes epistemic uncertainty", "Null", "accuracy")
    exp = ros.create_experiment(hyp.hypothesis_id, seed=123)
    completed_exp = ros.execute_experiment_simulation(exp.experiment_id, ground_truth_yield=2.5)

    assert completed_exp.is_statistically_significant

    # 2. Layer 1 -> Layer 2 Kernel handoff
    dag = ros.export_validated_hypothesis_to_kernel(hyp.hypothesis_id, kernel)
    assert dag.id in kernel.active_processes

    # 3. Layer 1 -> Layer 2 EOS Engine handoff
    eos_hyp = ros.promote_hypothesis_to_eos(hyp.hypothesis_id, eos)
    assert eos_hyp.hypothesis_id in eos.hypothesis_engine.hypotheses

    # 4. Layer 2 EOS -> Layer 3 AEAN HiveMind handoff
    bid = hive.register_research_insight(str(eos_hyp.hypothesis_id), eos_hyp.title)
    grants = hive.arbitrate([bid])
    assert len(grants) == 1
    assert grants[0].granted

    # 5. Layer 3 AEAN -> Layer 4 WorldModel handoff
    cnode = wm.create_node(label="EFE Active Inference Executed", domain="intelligence", value=2.0)
    wm.update_belief(node_id=cnode.node_id, new_confidence=0.95)

    assert cnode.node_id in wm.nodes
    assert wm.beliefs[cnode.node_id]["confidence"] == 0.95
