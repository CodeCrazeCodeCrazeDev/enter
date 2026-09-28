"""
Integration Test Suite: test_unified_cognitive_architecture_spec.py
Purpose: Validates cross-layer state handoffs and active inference execution across:
- Layer 1: Research OS
- Layer 2: EIOS Kernel & EOS Engine
- Layer 3: AEAN HiveMind
- Layer 4: APODEX WorldModel & Cognitive Brain
"""

import pytest
import asyncio
from apodex.ai_eos.research.research_os import ResearchOS
from apodex.arcs.kernel.kernel import EIOSKernel
from apodex.ai_eos.intelligence.eos_engine import EOSEngine
from apodex.aean.coordination.hive_mind import HiveMind
from apodex.world_model.world_model import WorldModel
from apodex.ai_eos.research.integration import ResearchToSystemBridge

@pytest.fixture
def system_components():
    research_os = ResearchOS()
    kernel = EIOSKernel()
    eos_engine = EOSEngine()
    hive_mind = HiveMind()
    world_model = WorldModel()
    bridge = ResearchToSystemBridge(
        research_os=research_os,
        kernel=kernel,
        eos_engine=eos_engine,
        hive_mind=hive_mind,
        world_model=world_model,
    )
    return {
        "research_os": research_os,
        "kernel": kernel,
        "eos_engine": eos_engine,
        "hive_mind": hive_mind,
        "world_model": world_model,
        "bridge": bridge,
    }

def test_layer1_to_layer2_handoff(system_components):
    research_os = system_components["research_os"]
    eos_engine = system_components["eos_engine"]

    # Generate hypothesis in Research OS (Layer 1)
    hypotheses = research_os.generate_hypotheses(domain="active_inference", count=1)
    assert len(hypotheses) == 1
    hypo = hypotheses[0]

    # Validate hypothesis statistically
    val_res = research_os.validate_hypothesis(hypo.id)
    assert val_res["validated"] is True

    # Ingest into EOS Engine (Layer 2)
    eos_engine.ingest_validated_research(hypo)
    assert len(eos_engine.active_hypotheses) == 1
    assert eos_engine.active_hypotheses[0].id == hypo.id

def test_layer2_to_layer3_handoff(system_components):
    kernel = system_components["kernel"]
    hive_mind = system_components["hive_mind"]

    # EIOS Kernel senses opportunity and compiles execution DAG (Layer 2)
    anomalies = kernel.sense_opportunity_anomalies(market_data={"arbitrage_spread": 0.08})
    assert len(anomalies) > 0
    dag = kernel.compile_execution_dag(opportunity_id=anomalies[0]["id"])
    assert dag is not None

    # Dispatch DAG task nodes to AEAN HiveMind (Layer 3)
    for task in dag["tasks"]:
        hive_mind.register_task(task_id=task["id"], task_type=task["type"], payload=task["payload"])

    assert len(hive_mind.pending_tasks) == len(dag["tasks"])

def test_layer3_to_layer4_handoff(system_components):
    hive_mind = system_components["hive_mind"]
    world_model = system_components["world_model"]

    # Register agent in AEAN HiveMind (Layer 3)
    hive_mind.register_agent(agent_id="agent_coder_01", specialization="coder", token_balance=100.0)

    # Agent updates WorldModel causal belief (Layer 4)
    c_node = world_model.create_node(node_id="refactored_module_01", label="Code Refactor Node")
    world_model.update_belief(node_id=c_node.id, prior_confidence=0.85, observation=0.92)

    fetched_node = world_model.get_node(c_node.id)
    assert fetched_node is not None
    assert fetched_node.properties.get("label") == "Code Refactor Node"

def test_full_cross_layer_bridge_handoff(system_components):
    bridge = system_components["bridge"]

    # Execute full research-to-system active inference handoff via Bridge
    result = bridge.execute_full_active_inference_handoff(domain="continuous_optimization")
    assert result["status"] == "success"
    assert "hypothesis_id" in result
    assert "dag_id" in result
    assert "world_model_node_id" in result
