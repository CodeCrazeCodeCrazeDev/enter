# -*- coding: utf-8 -*-
"""
test_unified_cognitive_architecture_spec.py
Integration test suite validating cross-layer active inference state handoffs
and single authority model across the 4 cognitive layers:
  - Layer 1: Research OS
  - Layer 2: EIOS Kernel & EOS Engine
  - Layer 3: AEAN HiveMind Multi-Agent Coordination
  - Layer 4: APODEX WorldModel Graph & Beliefs
"""

from uuid import uuid4
import pytest

from apodex.ai_eos.research.research_os import ResearchOS
from apodex.ai_eos.research.integration import ResearchToSystemBridge
from apodex.arcs.kernel.kernel import EIOSKernel
from apodex.ai_eos.intelligence.eos_engine import EOSEngine
from apodex.aean.coordination.hive_mind import HiveMind
from apodex.world_model.world_model import WorldModel


def test_unified_cognitive_architecture_cross_layer_handoff():
    """
    Validates end-to-end active inference handoff:
    Layer 1 (Research OS Hypothesis) ->
    Layer 2 (EIOS Anomaly Sensing & EOS Ingestion) ->
    Layer 3 (AEAN HiveMind Insight Registration) ->
    Layer 4 (APODEX WorldModel Causal Node & Belief Update).
    """
    # Initialize Layer 1: Research OS
    ros = ResearchOS()
    hyp = ros.register_hypothesis(
        title="Active Inference EFE Strategy",
        description="Expected Free Energy bounds curiosity and pragmatic cost.",
        null_hypothesis="EFE offers no improvement over random selection.",
        target_metric="active_inference_efficiency"
    )

    # Validate hypothesis via simulation
    exp = ros.create_experiment(hyp.hypothesis_id, seed=123)
    ros.execute_experiment_simulation(exp.experiment_id, ground_truth_yield=2.5)

    # Initialize Layer 2: EIOS Kernel & EOS Engine
    eios = EIOSKernel()
    eos = EOSEngine()

    # Initialize Layer 3: AEAN HiveMind
    hive_mind = HiveMind()

    # Initialize Layer 4: APODEX WorldModel
    world_model = WorldModel()

    # Create Cross-Layer Bridge
    bridge = ResearchToSystemBridge(
        research_os=ros,
        eios_kernel=eios,
        eos_engine=eos,
        hive_mind=hive_mind,
        world_model=world_model
    )

    # Execute Cross-Layer State Handoff
    handoff_record = bridge.execute_active_inference_handoff(hyp.hypothesis_id)

    # Assertions
    assert handoff_record["hypothesis_id"] == str(hyp.hypothesis_id)
    assert handoff_record["layer1_research_os"]["validated"] is True
    assert handoff_record["layer2_eios_eos"]["eos_ingested"] is True
    assert handoff_record["layer3_aean"]["insight_registered"] is True
    assert handoff_record["layer4_apodex"]["belief_updated"] is True
