"""Integration tests validating joint cross-layer interactions across Research OS, EIOS Kernel, EOS Engine, AEAN HiveMind, and APODEX WorldModel."""

from __future__ import annotations
import pytest
from apodex.ai_eos.research.research_os import ResearchOS
from apodex.arcs.kernel.kernel import EIOSKernel, ExecutionDAG, ExecutionNode
from apodex.ai_eos.intelligence.eos_engine import EOSEngine
from apodex.aean.coordination.hive_mind import HiveMind, TaskBid
from apodex.world_model.world_model import WorldModel
from apodex.ai_eos.research.integration import ResearchToSystemBridge


def test_research_os_to_kernel_and_eos_handoff():
    ros = ResearchOS()
    kernel = EIOSKernel()
    eos = EOSEngine()

    # Register and validate hypothesis
    hyp = ros.register_hypothesis(
        title="Market Demand Model",
        description="Demand scales exponentially with virality ratio",
        null_hypothesis="virality <= 1.0",
        target_metric="virality"
    )
    exp = ros.create_experiment(hyp.hypothesis_id, seed=123)
    ros.execute_experiment_simulation(exp.experiment_id, ground_truth_yield=2.5)

    assert hyp.status == "validated"

    # Handoff to Kernel and EOS
    k_res = ros.export_validated_hypothesis_to_kernel(hyp.hypothesis_id, kernel)
    e_res = ros.promote_hypothesis_to_eos(hyp.hypothesis_id, eos)

    assert k_res is True
    assert e_res is True
    assert len(kernel.registered_hypotheses) == 1
    assert len(eos.active_hypotheses) == 1


def test_hivemind_research_insight_bidding():
    hive_mind = HiveMind(token_budget=50)

    insight = {
        "title": "Virality Coefficient Alpha",
        "priority": 0.95,
        "expected_value": 0.90,
        "token_cost": 20
    }

    bid = hive_mind.register_research_insight(insight)
    grants = hive_mind.arbitrate([bid])

    assert len(grants) == 1
    assert grants[0].granted is True
    assert grants[0].tokens == 20


def test_research_to_system_bridge_cross_layer_handoff():
    ros = ResearchOS()
    kernel = EIOSKernel()
    eos = EOSEngine()
    hive_mind = HiveMind(token_budget=100)
    world_model = WorldModel()

    bridge = ResearchToSystemBridge(
        research_os=ros,
        eios_kernel=kernel,
        eos_engine=eos,
        hive_mind=hive_mind,
        world_model=world_model
    )

    hyp = ros.register_hypothesis(
        title="Quantum Pricing Elasticity",
        description="Dynamic surge pricing reduces customer acquisition cost by 18%",
        null_hypothesis="cost_reduction <= 0",
        target_metric="cac"
    )

    result = bridge.execute_cross_layer_handoff(hyp)

    assert result["status"] == "complete"
    assert result["kernel_handoff"] is True
    assert result["eos_handoff"] is True
    assert result["hivemind_task_bid"] is not None
    assert result["world_model_handoff"] is True
    assert len(world_model.beliefs) == 1
