# -*- coding: utf-8 -*-
"""
test_unified_4layer_integration.py
Comprehensive end-to-end integration test suite validating joint multi-layer active inference state handoffs
across Layer 1 Research OS, Layer 2 EIOS Kernel & EOS Engine, Layer 3 AEAN HiveMind, and Layer 4 APODEX WorldModel.
"""

import pytest
from apodex.ai_eos.research.integration import ResearchToSystemBridge
from apodex.arcs.kernel.kernel import EIOSKernel
from apodex.ai_eos.intelligence.eos_engine import EOSEngine
from apodex.aean.coordination.hive_mind import HiveMind
from apodex.world_model.world_model import WorldModel, CausalNode


def test_unified_4layer_active_inference_handoff():
    # Instantiate Layer Components
    kernel = EIOSKernel()
    eos = EOSEngine()
    hive = HiveMind()
    world = WorldModel()

    # Create Unified 4-Layer Bridge
    bridge = ResearchToSystemBridge(
        eios_kernel=kernel,
        eos_engine=eos,
        hive_mind=hive,
        world_model=world
    )

    # Pre-register target entity in Layer 4 WorldModel
    hypo_id = "HYPO_2026_EFE_001"
    world.add_node(CausalNode(node_id=hypo_id, label="EFE Minimization Hypothesis", node_type="hypothesis", properties={"status": "INITIAL"}))

    # Execute 4-Layer Active Inference Handoff
    result = bridge.handoff_hypothesis_to_execution(
        hypothesis_id=hypo_id,
        hypothesis_statement="Active inference minimizes expected free energy across business loops.",
        efe_delta=0.85,
        domain="cognitive_orchestration"
    )

    # 1. Verify Bridge Execution Output
    assert result["status"] == "completed"
    assert result["hypothesis_id"] == hypo_id
    assert result["efe_delta"] == 0.85

    # 2. Verify Layer 1 -> Layer 2 Ingestion
    assert result["layer_states"]["layer_2_eios_eos"]["status"] == "ingested"

    # 3. Verify Layer 2 -> Layer 3 Registration
    assert result["layer_states"]["layer_3_aean"]["status"] == "bidding_auction_registered"

    # 4. Verify Layer 3 -> Layer 4 WorldModel Entity Belief Update
    updated_node = world.nodes.get(hypo_id)
    assert updated_node is not None
    assert updated_node.properties["status"] == "ACTIVE_INFERENCE"
    assert updated_node.properties["efe"] == 0.85
