# -*- coding: utf-8 -*-
"""
test_unified_5layer_integration.py: Comprehensive end-to-end integration test suite
validating closed-loop interactions across Research OS (Layer 1), EIOS Kernel & EOS Engine (Layer 2),
AEAN HiveMind (Layer 3), and APODEX WorldModel & Cognitive Brain (Layer 4) via ResearchToSystemBridge.
"""

import pytest
import asyncio
from uuid import uuid4

from apodex.ai_eos.research.research_os import ResearchOS
from apodex.ai_eos.intelligence.eos_engine import EOSEngine, VentureCell
from apodex.arcs.kernel.kernel import EIOSKernel
from apodex.aean.coordination.hive_mind import HiveMind
from apodex.world_model.world_model import WorldModel
from apodex.cognition.brain import CognitiveBrain
from apodex.ai_eos.research.integration import (
    ResearchToSystemBridge,
    LearnableRoutingGateDispatcher,
    SpecializedAgentProfile,
)


@pytest.mark.asyncio
async def test_unified_5layer_closed_loop_active_inference():
    """
    Validates end-to-end active inference workflow across all 5 layers:
    - Layer 1: Research OS hypothesis creation and statistical validation.
    - Layer 2: EOS Engine continuous sensing & EIOS Kernel DAG execution.
    - Layer 3: AEAN HiveMind token arbitration and routing gate task dispatch.
    - Layer 4: APODEX WorldModel causal graph and CognitiveBrain Bayesian belief updates.
    - Bridge: ResearchToSystemBridge 4-layer state handoff execution.
    """
    # 1. Initialize Layer 1: Research OS
    ros = ResearchOS()
    hyp = ros.register_hypothesis(
        title="Active Inference Free Energy Optimization",
        description="Active inference EFE minimization reduces organizational decision surprise by >= 30%.",
        null_hypothesis="Active inference EFE does not reduce decision surprise.",
        target_metric="decision_surprise_index",
        significance_alpha=0.05
    )
    exp = ros.create_experiment(hypothesis_id=hyp.hypothesis_id, seed=123)
    exp_res = ros.execute_experiment_simulation(experiment_id=exp.experiment_id, ground_truth_yield=2.5)
    assert hyp.status in {"validated", "refuted"}

    # 2. Initialize Layer 2: EOS Engine & EIOS Kernel
    eos = EOSEngine()
    eios = EIOSKernel()

    vcell = VentureCell(cell_id=uuid4(), name="ActiveInferenceVenture", namespace="active_inf_ns", allocated_capital_cents=1000_00)
    sensing_res = eos.run_continuous_sensing_cycle(cells=[vcell], total_budget_cents=5000_00)
    assert "world_state" in sensing_res
    assert "allocated_budgets" in sensing_res

    # 3. Initialize Layer 3: AEAN HiveMind & Router
    hive = HiveMind(token_budget=100)
    dispatcher = LearnableRoutingGateDispatcher(budget_limit_usd=10.0)
    agent = SpecializedAgentProfile(
        agent_id="agent_research_ai",
        domain_specialty="AI Research",
        cost_per_token=0.002,
        historical_success_rate=0.88,
        epistemic_curiosity=0.70
    )
    dispatcher.register_subagent(agent)

    # 4. Initialize Layer 4: APODEX WorldModel & Cognitive Brain
    wm = WorldModel()
    brain = CognitiveBrain()

    # 5. Initialize ResearchToSystemBridge
    bridge = ResearchToSystemBridge(
        research_os=ros,
        eos_engine=eos,
        eios_kernel=eios,
        hive_mind=hive,
        world_model=wm,
        brain=brain,
        dispatcher=dispatcher
    )

    # Execute 4-layer active inference state handoff
    handoff_res = await bridge.handoff_validated_hypothesis(
        hypothesis_id=hyp.hypothesis_id,
        goal_description="Deploy Active Inference EFE Optimization Pipeline",
        token_bid_amount=15,
        estimated_cost_usd=0.03
    )

    # Verify Handoff Outcomes across all 4 layers
    assert handoff_res["hypothesis_id"] == str(hyp.hypothesis_id)
    assert handoff_res["layer_2_eios_dag_executed"] is True
    assert handoff_res["layer_2_free_energy"] >= 0.0
    assert handoff_res["layer_3_grant_approved"] is True
    assert handoff_res["layer_3_dispatched_agent"] == "agent_research_ai"
    assert handoff_res["layer_4_world_model_updated"] is True
    assert handoff_res["layer_4_belief_updated"] is True

    # Check WorldModel graph state
    assert f"hyp_{hyp.hypothesis_id}" in wm.nodes
    assert f"exec_{hyp.hypothesis_id}" in wm.nodes
    assert len(wm.edges) >= 1

    # Check CognitiveBrain fact assertion
    semantic_concepts = [c.name for c in brain.memory.semantic_memory.values()]
    assert hyp.title in semantic_concepts


def test_research_to_system_bridge_partial_subsystems():
    """Verifies that ResearchToSystemBridge handles partial subsystem configurations gracefully."""
    bridge = ResearchToSystemBridge()
    dummy_hyp_id = uuid4()

    # Run loop synchronously wrapper for async call
    handoff_res = asyncio.run(bridge.handoff_validated_hypothesis(
        hypothesis_id=dummy_hyp_id,
        goal_description="Test Standalone Bridge Handoff"
    ))

    assert handoff_res["hypothesis_id"] == str(dummy_hyp_id)
    assert handoff_res["layer_2_eios_dag_executed"] is False
    assert handoff_res["layer_3_grant_approved"] is False
    assert handoff_res["layer_4_world_model_updated"] is False
    assert len(bridge.handoff_history) == 1
