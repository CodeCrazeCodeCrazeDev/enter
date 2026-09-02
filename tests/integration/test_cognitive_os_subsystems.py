# -*- coding: utf-8 -*-
"""
test_cognitive_os_subsystems.py: Comprehensive integration test suite
validating joint state handoffs and lifecycle loops across all 5 unified cognitive subsystems:
- Layer 1: Research OS
- Layer 2: EIOS Kernel & EOS Engine
- Layer 3: AEAN Multi-Agent HiveMind
- Layer 4: APODEX WorldModel & Execution Platform
"""

import pytest
import asyncio
from uuid import uuid4

from apodex.ai_eos.research.research_os import ResearchOS
from apodex.arcs.kernel.kernel import EIOSKernel
from apodex.ai_eos.intelligence.eos_engine import EOSEngine
from apodex.aean.coordination.hive_mind import HiveMind
from apodex.world_model.world_model import WorldModel, CausalNode
from apodex.ai_eos.domain.models import Hypothesis


@pytest.mark.asyncio
async def test_cross_subsystem_research_hypothesis_flow():
    """
    Tests end-to-end handoff of a research hypothesis:
    1. Formulated and registered in Layer 1 Research OS.
    2. Registered into Layer 2 EIOS Kernel for Active Inference EFE anomaly sensing.
    3. Ingested into Layer 2 EOS Engine for opportunity evaluation.
    4. Registered in Layer 3 AEAN HiveMind for agent token bidding.
    5. Reflected in Layer 4 APODEX WorldModel entity and belief updates.
    """
    # 1. Layer 1: Research OS
    research_os = ResearchOS()
    hypothesis_obj = research_os.register_hypothesis(
        title="Hawkes Process Yield Curve Anomalies",
        description="Self-exciting Hawkes process detects market market-making yield anomalies.",
        null_hypothesis="Hawkes process yields no significant predictive anomaly signal.",
        target_metric="yield_spread_error",
        significance_alpha=0.05
    )
    assert hypothesis_obj.title == "Hawkes Process Yield Curve Anomalies"
    assert hypothesis_obj.status == "registered"

    hyp_dict = {
        "hypothesis_id": str(hypothesis_obj.hypothesis_id),
        "title": hypothesis_obj.title,
        "description": hypothesis_obj.description,
        "confidence_score": 0.85,
        "status": hypothesis_obj.status
    }

    # 2. Layer 2: EIOS Kernel Sensing
    kernel = EIOSKernel()
    kernel.register_research_hypothesis(hyp_dict)
    anomalies = kernel.sense_opportunity_anomalies()
    assert len(anomalies) >= 1
    assert anomalies[0]["title"] == hypothesis_obj.title

    # 2. Layer 2: EOS Engine Ingestion
    eos_engine = EOSEngine()
    eos_engine.ingest_validated_research(hypothesis_obj)
    active_hyps = eos_engine.active_hypotheses
    assert len(active_hyps) == 1
    assert active_hyps[0].title == hypothesis_obj.title

    # 3. Layer 3: AEAN HiveMind Insight Registration
    hive_mind = HiveMind()
    hive_mind.register_research_insight(
        insight_id=str(hypothesis_obj.hypothesis_id),
        title=hypothesis_obj.title,
        confidence=0.85
    )
    bids = hive_mind.get_token_bids_for_insight(str(hypothesis_obj.hypothesis_id))
    assert isinstance(bids, list)

    # 4. Layer 4: APODEX WorldModel State Update
    world_model = WorldModel()
    node_id = f"node_{hypothesis_obj.hypothesis_id}"
    causal_node = CausalNode(
        node_id=node_id,
        node_type="RESEARCH_HYPOTHESIS",
        properties={"title": hypothesis_obj.title, "confidence": 0.85}
    )
    world_model.add_node(causal_node)
    retrieved_node = world_model.nodes.get(node_id)
    assert retrieved_node is not None
    assert retrieved_node.properties["title"] == "Hawkes Process Yield Curve Anomalies"

    belief_id = str(uuid4())
    world_model.beliefs[belief_id] = {
        "target_id": node_id,
        "probability": 0.85,
        "evidence": [hypothesis_obj.title]
    }
    retrieved_belief = world_model.beliefs.get(belief_id)
    assert retrieved_belief is not None
    assert retrieved_belief["probability"] == 0.85


@pytest.mark.asyncio
async def test_research_os_literature_review_synthesis():
    """
    Validates Layer 1 Research OS literature review synthesis across corpus principles.
    """
    research_os = ResearchOS()
    review = research_os.conduct_literature_review("Active Inference and Hawkes Process")
    assert "domain" in review
    assert review["domain"] == "Active Inference and Hawkes Process"
    assert "reviewed_citations_count" in review
    assert review["reviewed_citations_count"] >= 1
