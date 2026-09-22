"""
Unified Cross-Layer End-to-End Integration Test Suite.
Validates state handoffs across Layer 1 (Research OS), Layer 2 (EIOS/EOS), Layer 3 (AEAN), and Layer 4 (APODEX WorldModel).
"""

import pytest
from apodex.ai_eos.research.integration import ResearchToSystemBridge
from apodex.aean.coordination.hive_mind import HiveMind
from apodex.arcs.kernel.kernel import EIOSKernel
from apodex.ai_eos.intelligence.eos_engine import EOSEngine
from apodex.world_model.world_model import WorldModel


class MockHypothesis:
    def __init__(self, hid: str = "hyp_e2e_001", title: str = "Active Inference Synergy"):
        self.id = hid
        self.hypothesis_id = hid
        self.title = title
        self.confidence_score = 0.92
        self.expected_sharpe = 2.1


def test_unified_cognitive_os_cross_layer_handoff():
    kernel = EIOSKernel()
    eos = EOSEngine()
    hive = HiveMind()
    wm = WorldModel()

    bridge = ResearchToSystemBridge(
        eios_kernel=kernel,
        eos_engine=eos,
        hive_mind=hive,
        world_model=wm
    )

    hyp = MockHypothesis()
    results = bridge.propagate_validated_hypothesis(hyp)

    assert results["hypothesis_id"] == "hyp_e2e_001"
    assert "eios_node_id" in results
    assert "hive_mind_token_id" in results
    assert results.get("world_model_belief_updated") is True
