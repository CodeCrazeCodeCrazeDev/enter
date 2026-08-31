# -*- coding: utf-8 -*-
"""
test_unified_4layer_integration.py: Integration test suite for the Unified 4-Layer Cognitive Operating System Architecture.
Verifies active inference handoffs across:
- Layer 1: Research OS (Hypothesis validation and literature review)
- Layer 2: EIOS Kernel & EOS Engine (Opportunity anomaly sensing and decision trees)
- Layer 3: AEAN HiveMind & Router (Multi-agent token bidding & EFE task routing)
- Layer 4: APODEX WorldModel (Continuous state, Entity & Bayesian belief updates)
"""

import pytest
from uuid import uuid4
from unittest.mock import MagicMock

from apodex.ai_eos.research.integration import (
    ResearchToSystemBridge,
    LearnableRoutingGateDispatcher,
    SpecializedAgentProfile
)
from apodex.world_model.world_model import WorldModel
from apodex.world_model.domain.entities import Entity
from apodex.world_model.domain.beliefs import Belief


class DummyHypothesis:
    def __init__(self, title: str, statement: str, domain: str = "ai_architecture"):
        self.id = uuid4()
        self.title = title
        self.statement = statement
        self.domain = domain


def test_end_to_end_4layer_active_inference_cycle():
    """Validates full state propagation from Layer 1 hypothesis to Layer 4 WorldModel belief updates."""
    mock_eios_kernel = MagicMock()
    mock_eos_engine = MagicMock()
    mock_hive_mind = MagicMock()
    world_model = WorldModel()

    bridge = ResearchToSystemBridge(
        eios_kernel=mock_eios_kernel,
        eos_engine=mock_eos_engine,
        hive_mind=mock_hive_mind,
        world_model=world_model
    )

    hypo = DummyHypothesis(
        title="Active Inference Multi-Agent Synergy",
        statement="EFE minimization across layers improves task dispatch efficiency by 30%."
    )

    records = bridge.execute_full_cross_layer_cycle(hypothesis=hypo)

    assert len(records) == 4
    assert records[0]["stage"] == "RESEARCH_TO_EIOS"
    assert records[1]["stage"] == "EIOS_TO_EOS"
    assert records[2]["stage"] == "EOS_TO_AEAN_HIVEMIND"
    assert records[3]["stage"] == "AEAN_TO_APODEX_WORLDMODEL"

    # Verify Mock interactions in Layer 2 and Layer 3
    mock_eios_kernel.register_research_hypothesis.assert_called_once_with(hypo)
    mock_eos_engine.ingest_validated_research.assert_called_once_with(hypo)
    mock_hive_mind.register_research_insight.assert_called_once_with(hypo)

    # Verify Layer 4 WorldModel state updates
    entity_id = records[3]["entity_id"]
    assert entity_id in world_model.beliefs
    assert world_model.beliefs[entity_id]["probability"] == 0.85
    assert len(world_model.nodes) == 1


def test_efe_routing_and_hivemind_insight_bidding():
    """Validates Expected Free Energy task routing and agent profile adaptation in Layer 3."""
    dispatcher = LearnableRoutingGateDispatcher(budget_limit_usd=10.0)

    agent_a = SpecializedAgentProfile(
        agent_id="research_agent_alpha",
        domain_specialty="ai_architecture",
        cost_per_token=0.001,
        historical_success_rate=0.8,
        epistemic_curiosity=0.7
    )
    agent_b = SpecializedAgentProfile(
        agent_id="finance_agent_beta",
        domain_specialty="finance",
        cost_per_token=0.0005,
        historical_success_rate=0.6,
        epistemic_curiosity=0.4
    )

    dispatcher.register_subagent(agent_a)
    dispatcher.register_subagent(agent_b)

    # Route task matching agent_a's domain specialty
    chosen_agent = dispatcher.route_task(task_complexity=100.0, domain="ai_architecture")
    assert chosen_agent == "research_agent_alpha"

    # Update metrics after successful execution
    dispatcher.update_routing_parameters(agent_id="research_agent_alpha", success=True, cost_incurred=0.1)
    assert dispatcher.agents["research_agent_alpha"].historical_success_rate > 0.8


def test_worldmodel_belief_update_propagation():
    """Validates explicit Entity creation and Bayesian belief updates in Layer 4."""
    entity = Entity(
        name="Cognitive Operating System Architecture",
        entity_type="SYSTEM_SPEC",
        properties={"layer_count": 4, "active_inference": True}
    )

    belief = Belief(
        target_id=entity.entity_id,
        probability=0.7,
        evidence=["Initial_Prior"]
    )

    # Perform recursive Bayesian belief update
    belief.update_confidence(likelihood=0.9, prior_probability=0.7)
    assert belief.probability > 0.7

    # Update entity property
    entity.update_property("status", "VERIFIED")
    assert entity.properties["status"] == "VERIFIED"
