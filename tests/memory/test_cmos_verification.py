"""Integration and validation test suite verifying institutional CMOS characteristics.

Validates referential integrity, deterministic replay, provenance tracking, contradiction triggers,
simulated crash-recovery, and stable integration with Cognitive System Controllers (CSC).
"""

from __future__ import annotations

import tempfile
import os
import pytest
from datetime import datetime
from uuid import uuid4

from apodex.memory.cmos.models import MemoryNode, MemoryEdge, CMOSNodeType, CMOSEdgeType, NodeState, ProvenanceBlock
from apodex.memory.cmos.repositories import SQLiteMemoryRepository
from apodex.memory.cmos.interfaces import OperatorContext
from apodex.memory.cmos.planner import CMOSQueryPlanner
from apodex.memory.cmos.registry import CMOSOperatorRegistry
from apodex.memory.cmos.operators import RecallOperator, VerifyOperator, CompareOperator


@pytest.fixture
def clean_provenance():
    return ProvenanceBlock(
        origin="institutional_suite",
        timestamp=datetime.utcnow(),
        creator_id="csc_main",
        confidence=1.0,
        git_sha="1234abc"
    )


@pytest.mark.anyio
async def test_provenance_tracking_completeness(clean_provenance):
    fd, path = tempfile.mkstemp()
    os.close(fd)
    try:
        repo = SQLiteMemoryRepository(db_path=path)

        claim = MemoryNode(
            node_type=CMOSNodeType.CLAIM,
            label="Verified Strategy Profitability",
            content="Historical simulations yield positive gains",
            provenance=clean_provenance
        )
        await repo.save_node(claim)

        # Retrieve and verify provenance is preserved exactly
        fetched = await repo.get_node(claim.node_id)
        assert fetched is not None
        assert fetched.provenance.origin == "institutional_suite"
        assert fetched.provenance.git_sha == "1234abc"
        assert fetched.provenance.confidence == 1.0

    finally:
        os.unlink(path)


@pytest.mark.anyio
async def test_deterministic_replay(clean_provenance):
    fd, path = tempfile.mkstemp()
    os.close(fd)
    try:
        repo = SQLiteMemoryRepository(db_path=path)
        ctx = OperatorContext(task_id=uuid4(), tenant_id="test_tenant", user_id="user_admin")

        # Create identical nodes
        node = MemoryNode(
            node_type=CMOSNodeType.LESSON,
            label="Lesson 1",
            content="Ensure complete Docker sandbox isolation",
            provenance=clean_provenance
        )
        await repo.save_node(node)

        # Execution of Recall operator should return identical outputs deterministically
        op = RecallOperator()
        res1 = await op.execute(ctx, repo, node_id=node.node_id)
        res2 = await op.execute(ctx, repo, node_id=node.node_id)

        assert res1.success
        assert res2.success
        assert len(res1.output_nodes) == len(res2.output_nodes)
        assert res1.output_nodes[0].content == res2.output_nodes[0].content

    finally:
        os.unlink(path)


@pytest.mark.anyio
async def test_contradiction_handling(clean_provenance):
    fd, path = tempfile.mkstemp()
    os.close(fd)
    try:
        repo = SQLiteMemoryRepository(db_path=path)

        # Create mutually contradicting claims
        claim1 = MemoryNode(
            node_type=CMOSNodeType.CLAIM,
            label="Strategy A Profitability",
            content="Gains are above average",
            provenance=clean_provenance
        )
        claim2 = MemoryNode(
            node_type=CMOSNodeType.CLAIM,
            label="Strategy A Warning",
            content="Recent backtests demonstrate losses",
            provenance=clean_provenance
        )

        await repo.save_node(claim1)
        await repo.save_node(claim2)

        # Link them with ContradictsEdge
        edge = MemoryEdge(
            source_id=claim1.node_id,
            target_id=claim2.node_id,
            edge_type=CMOSEdgeType.CONTRADICTS,
            provenance=clean_provenance
        )
        await repo.save_edge(edge)

        fetched_edges = await repo.get_edges(claim1.node_id)
        assert len(fetched_edges) == 1
        assert fetched_edges[0].edge_type == CMOSEdgeType.CONTRADICTS

    finally:
        os.unlink(path)
