# -*- coding: utf-8 -*-
"""
test_unified_5layer_integration.py: End-to-End Integration Test Suite.
Validates joint active inference cycles across:
1. Layer 1: Research OS
2. Layer 2: EIOS Kernel & EOS Engine
3. Layer 3: AEAN HiveMind
4. Layer 4: APODEX WorldModel & Cognitive Brain
"""

import pytest
from apodex.orchestration.unified_cognitive_os import UnifiedCognitiveOS
from apodex.ai_eos.research.research_os import ResearchOS
from apodex.arcs.kernel.kernel import EIOSKernel, ExecutionDAG, ExecutionNode
from apodex.ai_eos.intelligence.eos_engine import EOSEngine
from apodex.aean.coordination.hive_mind import HiveMind, TaskBid
from apodex.world_model.world_model import WorldModel
from apodex.ai_eos.research.integration import ResearchToSystemBridge


def test_unified_cognitive_os_closed_loop():
    """Validates full end-to-end active inference loop in UnifiedCognitiveOS."""
    ucos = UnifiedCognitiveOS()

    result = ucos.run_active_inference_loop(
        hypothesis_title="Automated Autonomous Arbitrage",
        hypothesis_description="Deploying AI active inference agents increases transaction efficiency by 25%",
        target_metric="arbitrage_yield"
    )

    assert result["status"] == "ACTIVE_INFERENCE_CYCLE_SUCCESS"
    assert result["statistically_significant"] is True
    assert result["handoff_result"]["status"] == "HANDOFF_COMPLETED"
    assert result["handoff_result"]["eios_registered"] is True
    assert result["anomalies_sensed"] >= 1


def test_research_to_system_bridge_direct_handoff():
    """Validates direct cross-layer state handoffs via ResearchToSystemBridge."""
    ros = ResearchOS()
    eios = EIOSKernel()
    eos = EOSEngine()
    hive = HiveMind(token_budget=100)
    wm = WorldModel()

    bridge = ResearchToSystemBridge(
        research_os=ros,
        eios_kernel=eios,
        eos_engine=eos,
        hive_mind=hive,
        world_model=wm
    )

    hyp = ros.register_hypothesis(
        title="Predictive Micro-SaaS Deployment",
        description="Predictive routing reduces SLA latencies",
        null_hypothesis="H0: no latency decrease",
        target_metric="latency_ms"
    )

    handoff = bridge.execute_cross_layer_handoff(hyp)

    assert handoff["status"] == "HANDOFF_COMPLETED"
    assert str(hyp.hypothesis_id) in eios.registered_hypotheses
    assert str(hyp.hypothesis_id) in eos.opportunity_graph.nodes
    assert len(hive.registered_insights) == 1
    assert len(wm.nodes) >= 1
    assert len(wm.beliefs) == 1


@pytest.mark.asyncio
async def test_eios_kernel_dag_execution_with_world_model():
    """Validates EIOS Kernel DAG execution coupled with APODEX WorldModel belief updates."""
    kernel = EIOSKernel()
    wm = WorldModel()

    dag = ExecutionDAG()
    node1 = ExecutionNode(name="Data Ingestion", action_type="research_only")
    node2 = ExecutionNode(name="Causal Modeling", action_type="research_only", depends_on=[node1.node_id])
    dag.add_node(node1)
    dag.add_node(node2)

    success = await kernel.execute_dag(dag)
    assert success is True

    # Register DAG execution in WorldModel
    node_wm = wm.create_node(node_id=dag.id, node_type="dag_execution", properties={"success": True})
    updated_prob = wm.update_belief(f"belief_dag_{dag.id}", prior_probability=0.5, evidence_weight=0.90)

    assert node_wm.node_id == dag.id
    assert updated_prob > 0.5
