"""Unit tests for the Apodex 2.0 5-Tier Memory models and interfaces."""

from __future__ import annotations

import uuid
from datetime import datetime
from pydantic import ValidationError
import pytest

from apodex.memory.models import (
    AtomicMemory,
    CostMode,
    EpisodeLogRecord,
    NodeType,
    PersonalEvolutionProfile,
    WorkingContextGraph,
    WorkingContextNode,
)
from apodex.memory.interfaces import RetrievalAPI


def test_working_context_node_validation():
    # Valid Node
    node = WorkingContextNode(
        task_id=uuid.uuid4(),
        type=NodeType.SUBTASK,
        label="Refactor parsing logic"
    )
    assert node.node_id.startswith("node_")
    assert node.status == "active"

    # Invalid Node due to label too short
    with pytest.raises(ValidationError):
        WorkingContextNode(
            task_id=uuid.uuid4(),
            type=NodeType.SUBTASK,
            label="a"  # min_length=2
        )


def test_atomic_memory_validation():
    # Valid Atom
    atom = AtomicMemory(
        tenant_id="tenant_abc",
        user_id="user_123",
        content="Identified parsing bottleneck in fast_parser.py",
        embedding=[0.1] * 1536,
        confidence=0.95,
        tags=["parser", "bottleneck"]
    )
    assert atom.confidence == 0.95
    assert len(atom.embedding) == 1536

    # Invalid Atom due to wrong embedding dimension
    with pytest.raises(ValidationError):
        AtomicMemory(
            tenant_id="tenant_abc",
            user_id="user_123",
            content="Identified parsing bottleneck in fast_parser.py",
            embedding=[0.1] * 512,  # Must be exactly 1536
            confidence=0.95
        )


def test_personal_evolution_profile_validation():
    pep = PersonalEvolutionProfile(
        tenant_id="tenant_abc",
        user_id="user_123"
    )
    assert pep.style_preferences["verbosity"] == "concise"
    assert pep.cost_budget_preferences["default_mode"] == "balanced"


class DummyRetrievalAPI(RetrievalAPI):
    """Concrete implementation of RetrievalAPI to test its helper methods."""

    async def query_hybrid_memory(self, tenant_id, query_text, query_embedding, pep, limit=10):
        return []

    async def retrieve_active_working_context(self, task_id):
        return WorkingContextGraph(task_id=task_id, tenant_id="dummy")

    async def retrieve_matched_scenarios(self, tenant_id, pattern_type):
        return []


def test_retrieval_api_scoring():
    api = DummyRetrievalAPI()

    # Test max_quality mode scoring
    score_hq = api.score_memory_item(
        semantic_sim=0.9,
        bm25_score=0.8,
        entity_overlap=1.0,
        temporal_proximity=0.5,
        graph_proximity=0.7,
        confidence=0.95,
        mode=CostMode.MAX_QUALITY
    )

    # Test fast_cheap mode scoring
    score_fc = api.score_memory_item(
        semantic_sim=0.9,
        bm25_score=0.8,
        entity_overlap=1.0,
        temporal_proximity=0.5,
        graph_proximity=0.7,
        confidence=0.95,
        mode=CostMode.FAST_CHEAP
    )

    assert score_hq != score_fc
    assert isinstance(score_hq, float)
    assert isinstance(score_fc, float)
