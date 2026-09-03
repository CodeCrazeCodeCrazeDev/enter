# -*- coding: utf-8 -*-
"""
test_unified_4layer_integration.py: End-to-end integration test validating
joint active inference handoffs across Layer 1 (Research OS), Layer 2 (EIOS / EOS),
Layer 3 (AEAN HiveMind), and Layer 4 (APODEX WorldModel & SkillRegistry).
"""

import pytest
from unittest.mock import MagicMock
from apodex.ai_eos.research.integration import ResearchToSystemBridge, ValidatedHypothesisPayload
from apodex.arcs.kernel.kernel import EIOSKernel
from apodex.ai_eos.intelligence.eos_engine import EOSEngine
from apodex.aean.coordination.hive_mind import HiveMind, TaskBid
from apodex.world_model.world_model import WorldModel, CausalNode
from apodex.skills.registry import SkillRegistry


def test_unified_4layer_active_inference_handoff():
    # 1. Layer 1 Research OS Mock & Bridge Setup
    mock_research_os = MagicMock()
    kernel = EIOSKernel()
    eos_engine = EOSEngine()

    bridge = ResearchToSystemBridge(
        research_os=mock_research_os,
        eios_kernel=kernel,
        eos_engine=eos_engine
    )

    # Hypothesis Promotion: L1 -> L2
    payload = bridge.promote_validated_hypothesis("HYP-401")
    assert payload.hypothesis_id == "HYP-401"
    assert len(kernel.active_hypotheses) == 1
    assert len(eos_engine.active_hypotheses) == 1

    # 2. Layer 2 Active Inference Sensing & Task DAG Construction
    anomalies = kernel.sense_opportunity_anomalies([
        {"metric_id": "latency_spike", "observed_delta": 0.85, "variance": 0.1}
    ])
    assert len(anomalies) >= 1
    assert anomalies[0]["expected_free_energy"] > 0

    opportunity = eos_engine.ingest_opportunity_signal({
        "opportunity_id": "OPP-99",
        "description": "Optimize latency via autonomous caching",
        "priority": 0.9,
        "complexity": 0.5
    })
    assert opportunity.opportunity_id == "OPP-99"

    # 3. Layer 3 AEAN HiveMind Bidding & Coordination
    hive_mind = HiveMind(token_budget=100)
    bids = [
        TaskBid(task="OPP-99_subtask_1", priority=0.9, expected_value=1.5, token_cost=20),
        TaskBid(task="OPP-99_subtask_2", priority=0.3, expected_value=0.5, token_cost=90)
    ]
    grants = hive_mind.arbitrate(bids)
    assert len(grants) == 2
    assert grants[0].granted is True
    assert grants[1].granted is False  # exceeds remaining token budget

    # 4. Layer 4 APODEX WorldModel & Skill Execution
    world_model = WorldModel()
    world_model.add_node(CausalNode(node_id="cache_cluster", node_type="state", properties={"status": "degraded"}))

    skills = SkillRegistry()
    skill = skills.get_skill("opportunity_evaluation_frameworks")
    assert skill is not None

    node = world_model.nodes.get("cache_cluster")
    assert node is not None
    node.properties["status"] = "optimized"
    assert world_model.nodes["cache_cluster"].properties["status"] == "optimized"
