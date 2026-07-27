"""Unit tests for the Cognitive Memory Operating System (CMOS).

Validates polymorphic schemas, repos, telemetry, and referential integrity constraints.
"""

from __future__ import annotations

import os
import tempfile
import pytest
from datetime import datetime
from uuid import uuid4

from apodex.memory.cmos.models import MemoryNode, MemoryEdge, CMOSNodeType, CMOSEdgeType, NodeState, ProvenanceBlock
from apodex.memory.cmos.repositories import InMemoryMemoryRepository, SQLiteMemoryRepository


@pytest.fixture
def clean_provenance():
    return ProvenanceBlock(
        origin="test_suite",
        timestamp=datetime.utcnow(),
        creator_id="test_agent",
        confidence=1.0,
        git_sha="abcdef123"
    )


@pytest.mark.anyio
async def test_in_memory_repository(clean_provenance):
    repo = InMemoryMemoryRepository()

    # Create nodes
    node_a = MemoryNode(
        node_type=CMOSNodeType.CLAIM,
        label="Test Claim",
        content="Our prompt works well",
        provenance=clean_provenance
    )
    node_b = MemoryNode(
        node_type=CMOSNodeType.EVIDENCE,
        label="Test Evidence",
        content="Pass rate: 96%",
        provenance=clean_provenance
    )

    await repo.save_node(node_a)
    await repo.save_node(node_b)

    # Save Edge (with proper referential integrity)
    edge = MemoryEdge(
        source_id=node_a.node_id,
        target_id=node_b.node_id,
        edge_type=CMOSEdgeType.SUPPORT,
        provenance=clean_provenance
    )
    await repo.save_edge(edge)

    # Check existence
    fetched_a = await repo.get_node(node_a.node_id)
    assert fetched_a is not None
    assert fetched_a.label == "Test Claim"

    fetched_edges = await repo.get_edges(node_a.node_id)
    assert len(fetched_edges) == 1
    assert fetched_edges[0].target_id == node_b.node_id


@pytest.mark.anyio
async def test_in_memory_referential_integrity(clean_provenance):
    repo = InMemoryMemoryRepository()
    edge = MemoryEdge(
        source_id="nonexistent_source",
        target_id="nonexistent_target",
        edge_type=CMOSEdgeType.CAUSAL,
        provenance=clean_provenance
    )

    with pytest.raises(ValueError, match="Referential Integrity broken"):
        await repo.save_edge(edge)


@pytest.mark.anyio
async def test_sqlite_repository(clean_provenance):
    fd, path = tempfile.mkstemp()
    os.close(fd)
    try:
        repo = SQLiteMemoryRepository(db_path=path)

        node_a = MemoryNode(
            node_type=CMOSNodeType.STRATEGY,
            label="Pluggable Strategy",
            content="Use prompt style B",
            provenance=clean_provenance
        )
        node_b = MemoryNode(
            node_type=CMOSNodeType.FAILURE,
            label="Execution Failure",
            content="Timeout on long step",
            provenance=clean_provenance
        )

        await repo.save_node(node_a)
        await repo.save_node(node_b)

        # Save edge
        edge = MemoryEdge(
            source_id=node_a.node_id,
            target_id=node_b.node_id,
            edge_type=CMOSEdgeType.CAUSAL,
            provenance=clean_provenance
        )
        await repo.save_edge(edge)

        # Fetch Node
        fetched_b = await repo.get_node(node_b.node_id)
        assert fetched_b is not None
        assert fetched_b.node_type == CMOSNodeType.FAILURE

        # Fetch Edges
        edges = await repo.get_edges(node_a.node_id)
        assert len(edges) == 1
        assert edges[0].target_id == node_b.node_id

        # Clean delete cascade
        await repo.delete_node(node_a.node_id)
        assert await repo.get_node(node_a.node_id) is None
        assert len(await repo.get_edges(node_a.node_id)) == 0

    finally:
        os.unlink(path)
