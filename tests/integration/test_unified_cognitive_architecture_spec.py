# -*- coding: utf-8 -*-
"""
test_unified_cognitive_architecture_spec.py: Integration test suite verifying
the unified 4-layer Cognitive Operating System architecture:
- Layer 1: Research OS
- Layer 2: EIOS / EOS Engine
- Layer 3: AEAN HiveMind
- Layer 4: APODEX WorldModel
"""

import pytest
from apodex.ai_eos.research.integration import ResearchToSystemBridge

class MockResearchOS:
    def export_validated_hypotheses(self):
        class Hyp:
            hypothesis_id = "hyp-101"
            title = "Active Inference Expected Free Energy Reduction"
            target_subsystem = "EIOS"
            confidence_score = 0.98
        return [Hyp()]

class MockEOSEngine:
    def __init__(self):
        self.ingested = []
    def ingest_validated_research(self, hyps):
        self.ingested.extend(hyps)

class MockHiveMind:
    def __init__(self):
        self.insights = []
    def register_research_insight(self, insight_id, topic, priority):
        self.insights.append((insight_id, topic, priority))

class MockWorldModel:
    def __init__(self):
        self.nodes = []
    def create_node(self, node_id, node_type, metadata):
        self.nodes.append((node_id, node_type, metadata))

def test_unified_cognitive_architecture_spec_handoff():
    ros = MockResearchOS()
    eos = MockEOSEngine()
    hive = MockHiveMind()
    wm = MockWorldModel()

    bridge = ResearchToSystemBridge(
        research_os=ros,
        eos_engine=eos,
        hive_mind=hive,
        world_model=wm
    )

    count = bridge.propagate_validated_hypotheses()
    assert count == 1
    assert len(eos.ingested) == 1
    assert len(hive.insights) == 1
    assert len(wm.nodes) == 1
    assert wm.nodes[0][0] == "hyp-101"
