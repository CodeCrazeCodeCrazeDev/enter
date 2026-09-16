"""Integration test suite validating joint cross-layer interactions across
Research OS, EIOS Kernel, EOS Engine, AEAN HiveMind, and APODEX WorldModel.
"""

from __future__ import annotations
import pytest
from uuid import uuid4

from apodex.ai_eos.research.research_os import ResearchOS
from apodex.arcs.kernel.kernel import EIOSKernel, EntrepreneurialCompiler
from apodex.ai_eos.intelligence.eos_engine import EOSEngine
from apodex.aean.coordination.hive_mind import HiveMind, TaskBid
from apodex.world_model.world_model import WorldModel, CausalNode
from apodex.ai_eos.research.integration import ResearchToSystemBridge


def test_cognitive_os_subsystems_joint_behavior():
    # 1. Instantiate Layer 1: Research OS
    ros = ResearchOS()
    hyp = ros.register_hypothesis(
        title="Predictive Monetization Optimization",
        description="Predictive AI pricing model increases SaaS ARPU by 25%",
        null_hypothesis="Pricing model has no effect on ARPU",
        target_metric="arpu_growth"
    )
    exp = ros.create_experiment(hyp.hypothesis_id, seed=42)
    completed_exp = ros.execute_experiment_simulation(exp.experiment_id, ground_truth_yield=2.0)
    assert completed_exp.is_statistically_significant is True
    assert hyp.status == "validated"

    # 2. Instantiate Layer 2: EIOS Kernel & EOS Engine
    eios = EIOSKernel()
    eos = EOSEngine()

    # 3. Instantiate Layer 3: AEAN HiveMind
    hive = HiveMind(token_budget=100)

    # 4. Instantiate Layer 4: APODEX WorldModel
    wm = WorldModel()

    # 5. Execute Cross-Layer State Handoff via ResearchToSystemBridge
    bridge = ResearchToSystemBridge()
    handoff_res = bridge.handoff_validated_hypothesis(
        hypothesis=hyp,
        research_os=ros,
        eios_kernel=eios,
        eos_engine=eos,
        hive_mind=hive,
        world_model=wm
    )

    # Verify Handoff Record
    assert handoff_res["layer1_research_os"] == "VALIDATED"
    assert handoff_res["layer2_eios"] is not None
    assert handoff_res["layer2_eos"] == "PROMOTED_TO_EOS_ENGINE"
    assert "HIVEMIND_BID_ARBITRATED_GRANTED_True" in handoff_res["layer3_aean"]
    assert handoff_res["layer4_world_model"] == "CAUSAL_NODE_AND_BELIEF_UPDATED"

    # Verify EOS Engine State Updates
    assert len(eos.hypothesis_engine.hypotheses) == 1

    # Verify AEAN HiveMind Grants
    assert len(hive.granted_history) == 1
    assert hive.granted_history[0].granted is True

    # Verify APODEX WorldModel Updates
    assert f"research_hyp_{hyp.hypothesis_id}" in wm.nodes
    assert f"belief_{hyp.hypothesis_id}" in wm.beliefs
    assert wm.beliefs[f"belief_{hyp.hypothesis_id}"]["validated"] is True
