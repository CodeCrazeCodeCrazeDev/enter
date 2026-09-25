# -*- coding: utf-8 -*-
"""
test_unified_cognitive_os_integration.py
End-to-end multi-layer integration test suite validating closed-loop interaction
across Layer 1 Research OS, Layer 2 EIOS Kernel & EOS Engine, Layer 3 AEAN HiveMind,
and Layer 4 APODEX WorldModel via ResearchToSystemBridge.
"""

import pytest
from apodex.ai_eos.research.research_os import ResearchOS, Hypothesis
from apodex.arcs.kernel.kernel import EIOSKernel
from apodex.ai_eos.intelligence.eos_engine import EOSEngine
from apodex.aean.coordination.hive_mind import HiveMind
from apodex.world_model.world_model import WorldModel
from apodex.ai_eos.research.integration import ResearchToSystemBridge


def test_unified_cognitive_os_end_to_end_closed_loop():
    # 1. Initialize all 5 core subsystem layers
    research_os = ResearchOS()
    eios_kernel = EIOSKernel()
    eos_engine = EOSEngine()
    hive_mind = HiveMind()
    world_model = WorldModel()

    # Instantiate cross-layer bridge
    bridge = ResearchToSystemBridge(
        research_os=research_os,
        eios_kernel=eios_kernel,
        eos_engine=eos_engine,
        hive_mind=hive_mind,
        world_model=world_model
    )

    # 2. Register research hypothesis in Research OS
    hypo = research_os.register_hypothesis(
        title="Active Inference Task Routing",
        description="Hierarchical active inference with EFE task routing increases execution efficiency.",
        null_hypothesis="Routing performance is identical to random dispatcher.",
        target_metric="execution_efficiency",
        significance_alpha=0.05
    )
    hypo_id_str = str(hypo.hypothesis_id)
    assert research_os.hypotheses.get(hypo.hypothesis_id) is not None

    # 3. Trigger cross-layer state handoff via Bridge
    handoff_record = bridge.handoff_validated_hypothesis(hypo_id_str)
    assert handoff_record["status"] == "completed"
    assert "EIOS_Kernel" in handoff_record["layers_notified"]
    assert "EOS_Engine" in handoff_record["layers_notified"]
    assert "AEAN_HiveMind" in handoff_record["layers_notified"]
    assert "APODEX_WorldModel" in handoff_record["layers_notified"]

    # 4. Verify downstream state propagation across subsystems
    # EIOS Kernel active processes tracking
    assert isinstance(eios_kernel.active_processes, dict)

    # EOS Engine hypothesis ingestion verification
    assert len(eos_engine.hypothesis_engine.hypotheses) >= 1

    # AEAN HiveMind token budget availability
    assert hive_mind.token_budget >= 0

    # APODEX WorldModel node and belief updates
    assert f"node_{hypo_id_str}" in world_model.nodes
    assert f"belief_{hypo_id_str}" in world_model.beliefs


def test_research_os_literature_review_querying():
    research_os = ResearchOS()
    results = research_os.conduct_literature_review(domain="active_inference")
    assert isinstance(results, dict)
