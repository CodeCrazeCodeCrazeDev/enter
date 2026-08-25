"""
Integration tests for Cognitive OS subsystems: Research OS, EIOS Kernel, EOS Engine, AEAN HiveMind, and APODEX.
"""

import pytest
from uuid import uuid4
from apodex.ai_eos.research.research_os import ResearchOS
from apodex.arcs.kernel.kernel import EIOSKernel
from apodex.ai_eos.intelligence.eos_engine import EOSEngine
from apodex.aean.coordination.hive_mind import HiveMind
from apodex.cognition.brain import CognitiveBrain
from apodex.ai_eos.research.integration import ResearchToSystemBridge


def test_research_os_hypothesis_and_experiment_lifecycle():
    ros = ResearchOS()
    hyp = ros.register_hypothesis(
        title="EFE Active Inference Routing Optimization",
        description="Active inference routing reduces expected free energy.",
        null_hypothesis="Active inference routing has no effect.",
        target_metric="efe_kl_div"
    )
    assert hyp.status == "registered"

    exp = ros.create_experiment(hyp.hypothesis_id, seed=123)
    assert (exp.status.value if hasattr(exp.status, "value") else exp.status) == "queued"

    completed_exp = ros.execute_experiment_simulation(exp.experiment_id, ground_truth_yield=2.5)
    assert (completed_exp.status.value if hasattr(completed_exp.status, "value") else completed_exp.status) == "completed"
    assert completed_exp.is_statistically_significant is True
    assert hyp.status == "validated"

    exported = ros.export_validated_hypothesis_to_kernel(hyp.hypothesis_id)
    assert exported["exported"] is True

    promoted = ros.promote_hypothesis_to_eos(hyp.hypothesis_id)
    assert promoted["promoted"] is True


def test_cross_layer_active_inference_handoff():
    ros = ResearchOS()
    kernel = EIOSKernel()
    eos = EOSEngine()
    hive = HiveMind()
    brain = CognitiveBrain()

    bridge = ResearchToSystemBridge(
        research_os=ros,
        eios_kernel=kernel,
        eos_engine=eos,
        hive_mind=hive,
        brain=brain
    )

    hyp = ros.register_hypothesis(
        title="Market Drift Sensing",
        description="EIOS sensing detects market regime changes.",
        null_hypothesis="No drift detected.",
        target_metric="market_drift"
    )

    handoff = bridge.handoff_validated_hypothesis_to_kernel(hyp.hypothesis_id)
    assert handoff["kernel_sensed"] is True
    assert handoff["hypothesis_id"] == str(hyp.hypothesis_id)

    eos_decision = {"action": "allocate_capital", "target_cell": "venture_alpha", "weight": 0.25}
    handshake = bridge.handshake_eos_with_aean_and_brain(eos_decision)
    assert handshake["hive_mind_aligned"] is True
    assert handshake["brain_consolidated"] is True
