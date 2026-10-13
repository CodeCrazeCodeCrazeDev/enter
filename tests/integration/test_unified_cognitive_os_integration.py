"""Integration test suite validating closed-loop multi-layer execution of UnifiedCognitiveOS

Tests cross-subsystem state handoffs across Research OS, EIOS Kernel, EOS Engine,
AEAN HiveMind, and APODEX WorldModel.
"""

from __future__ import annotations
import pytest
from apodex.orchestration.unified_cognitive_os import UnifiedCognitiveOS
from apodex.ai_eos.research.integration import ResearchToSystemBridge


@pytest.mark.asyncio
async def test_unified_cognitive_os_initialization():
    """Verify Master Orchestrator initializes all 5 subsystems and bridge."""
    os_inst = UnifiedCognitiveOS()
    assert os_inst.research_os is not None
    assert os_inst.eios_kernel is not None
    assert os_inst.eos_engine is not None
    assert os_inst.hive_mind is not None
    assert os_inst.world_model is not None
    assert isinstance(os_inst.bridge, ResearchToSystemBridge)


@pytest.mark.asyncio
async def test_unified_cognitive_cycle_execution():
    """Verify closed-loop cognitive cycle execution across all 5 layers."""
    os_inst = UnifiedCognitiveOS()
    input_data = {
        "title": "Autonomous AI Agent Fleet Expansion",
        "description": "Probe feasibility of scaling specialized AEAN agent clusters",
        "null_hypothesis": "Fleet expansion does not improve throughput",
        "target_metric": "system_throughput_tps",
        "keywords": ["agent_fleet", "scaling", "active_inference"],
        "value_cents": 25000_00,
        "expected_value": 0.92
    }

    result = await os_inst.run_cognitive_cycle(input_data)

    assert result["status"] == "SUCCESS"
    assert result["cycle_title"] == "Autonomous AI Agent Fleet Expansion"
    assert result["dag_executed_successfully"] is True
    assert result["statistically_significant"] is True

    # Validate Layer 1 Research OS Hypothesis State
    hyp_list = os_inst.research_os.hypotheses.list_all()
    assert len(hyp_list) == 1
    assert hyp_list[0].title == "Autonomous AI Agent Fleet Expansion"
    assert hyp_list[0].status == "validated"

    # Validate Layer 2 EIOS Kernel Hypothesis State
    assert len(os_inst.eios_kernel.registered_hypotheses) == 1

    # Validate Layer 2 EOS Engine Opportunity Graph
    assert len(os_inst.eos_engine.opportunity_graph.nodes) == 1

    # Validate Layer 3 AEAN HiveMind Bids & History
    assert len(os_inst.hive_mind.granted_history) >= 1

    # Validate Layer 4 APODEX WorldModel Graph Nodes, Edges, and Beliefs
    assert len(os_inst.world_model.nodes) >= 1
    assert len(os_inst.world_model.edges) >= 1
    assert "belief_system_throughput_tps" in os_inst.world_model.beliefs


@pytest.mark.asyncio
async def test_research_to_system_bridge_direct_handoffs():
    """Verify individual cross-layer state handoffs via ResearchToSystemBridge."""
    os_inst = UnifiedCognitiveOS()
    bridge = os_inst.bridge

    # 1. Hypothesis -> EIOS Kernel
    hyp = os_inst.research_os.register_hypothesis(
        title="Direct Bridge Test",
        description="Testing direct bridge handoffs",
        null_hypothesis="No effect",
        target_metric="latency_ms"
    )
    eios_res = bridge.bridge_hypothesis_to_eios(hyp)
    assert "eios_record" in eios_res
    assert len(eios_res["anomalies_sensed"]) >= 1

    # 2. Opportunity -> EOS Engine
    eos_res = bridge.bridge_opportunity_to_eos(
        opportunity_id="op_bridge_001",
        name="Direct EOS Opportunity",
        value_cents=5000_00,
        keywords=["bridge", "direct"]
    )
    assert eos_res["opportunity_id"] == "op_bridge_001"
    assert "world_sensing" in eos_res

    # 3. Insight -> AEAN HiveMind
    aean_res = bridge.bridge_insight_to_aean(
        insight_id="ins_bridge_001",
        domain="latency_ms",
        expected_value=0.88
    )
    assert aean_res["bid"].expected_value == 0.88
    assert len(aean_res["grants"]) == 1
    assert aean_res["grants"][0].granted is True

    # 4. Execution -> APODEX WorldModel
    wm_res = bridge.bridge_execution_to_world_model(
        node_id="node_exec_001",
        node_type="test_run",
        relation_type="validates",
        target_id="target_hyp_001",
        belief_key="latency_ms_belief",
        belief_val=12.5
    )
    assert wm_res["node"].node_id == "node_exec_001"
    assert wm_res["edge"].relation_type == "validates"
    assert os_inst.world_model.beliefs["latency_ms_belief"]["value"] == 12.5
