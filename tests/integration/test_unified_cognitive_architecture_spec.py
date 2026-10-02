"""
Integration tests validating the unified 4-layer cognitive operating system specification:
- Layer 1: Research OS
- Layer 2: EIOS Kernel & EOS Engine
- Layer 3: AEAN HiveMind & Learnable Routing Gate
- Layer 4: APODEX WorldModel & Belief Engine
"""

from __future__ import annotations
import pytest
import asyncio
from apodex.ai_eos.research.research_os import ResearchOS
from apodex.arcs.kernel.kernel import EIOSKernel, ExecutionDAG, ExecutionNode
from apodex.ai_eos.intelligence.eos_engine import EOSEngine
from apodex.aean.coordination.hive_mind import HiveMind, TaskBid
from apodex.world_model.world_model import WorldModel, CausalNode
from apodex.ai_eos.research.integration import ResearchToSystemBridge, LearnableRoutingGateDispatcher, SpecializedAgentProfile


@pytest.mark.asyncio
async def test_unified_4layer_cross_layer_cycle():
    # Setup instances
    ros = ResearchOS()
    kernel = EIOSKernel()
    eos = EOSEngine()
    hive_mind = HiveMind(token_budget=200)
    world_model = WorldModel()

    # Step 1: Register hypothesis in Layer 1
    hyp = ros.register_hypothesis(
        title="Unified Active Inference EFE",
        description="Active Inference EFE reduces surprise across all 4 system layers.",
        null_hypothesis="EFE provides no benefit.",
        target_metric="variational_free_energy"
    )
    assert hyp.status == "registered"

    # Step 2: Initialize bridge and run cross-layer cycle
    bridge = ResearchToSystemBridge(
        research_os=ros,
        eios_kernel=kernel,
        eos_engine=eos,
        hive_mind=hive_mind,
        world_model=world_model
    )

    cycle_result = await bridge.execute_cross_layer_cycle(hyp)

    # Assertions on cross-layer state handoffs
    assert cycle_result["status"] == "completed"
    assert "layer_results" in cycle_result

    # Layer 1 Verification
    l1_res = cycle_result["layer_results"]["layer1_research_os"]
    assert l1_res["status"] in ["validated", "active"]
    assert l1_res["hypothesis_title"] == "Unified Active Inference EFE"

    # Layer 2 Verification
    l2_res = cycle_result["layer_results"]["layer2_eios_eos"]
    assert l2_res["dag_status"] == "completed"
    assert l2_res["executed_tasks"] >= 2

    # Layer 3 Verification
    l3_res = cycle_result["layer_results"]["layer3_aean"]
    assert l3_res["grants_count"] >= 1
    assert l3_res["token_budget"] == 200

    # Layer 4 Verification
    l4_res = cycle_result["layer_results"]["layer4_apodex_world_model"]
    assert l4_res["belief_status"] == "updated"
    assert l4_res["updated_posterior"] == 0.85

    # Check that node exists in World Model
    causal_node_id = l4_res["causal_node_id"]
    assert causal_node_id in world_model.nodes
    assert world_model.beliefs[causal_node_id]["posterior"] == 0.85


@pytest.mark.asyncio
async def test_learnable_routing_gate_dispatcher():
    dispatcher = LearnableRoutingGateDispatcher(budget_limit_usd=10.0)

    agent_a = SpecializedAgentProfile(
        agent_id="agent_research",
        domain_specialty="science",
        cost_per_token=0.001,
        historical_success_rate=0.85,
        epistemic_curiosity=0.7
    )
    agent_b = SpecializedAgentProfile(
        agent_id="agent_code",
        domain_specialty="engineering",
        cost_per_token=0.002,
        historical_success_rate=0.90,
        epistemic_curiosity=0.4
    )

    dispatcher.register_subagent(agent_a)
    dispatcher.register_subagent(agent_b)

    routed_agent_id = dispatcher.route_task(task_complexity=100.0, domain="science")
    assert routed_agent_id == "agent_research"

    dispatcher.update_routing_parameters("agent_research", success=True, cost_incurred=0.1)
    assert dispatcher.budget_spent == 0.1
