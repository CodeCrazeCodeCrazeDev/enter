"""Unit tests for pluggable cognitive operators in CMOS.

Validates execution paths, telemetry emission, and operator correctness contracts.
"""

from __future__ import annotations

import pytest
from datetime import datetime
from uuid import uuid4

from apodex.memory.cmos.models import MemoryNode, MemoryEdge, CMOSNodeType, CMOSEdgeType, NodeState, ProvenanceBlock
from apodex.memory.cmos.repositories import InMemoryMemoryRepository
from apodex.memory.cmos.interfaces import OperatorContext
from apodex.memory.cmos.registry import CMOSOperatorRegistry
from apodex.memory.cmos.operators import (
    RecallOperator,
    VerifyOperator,
    CompareOperator,
    ContrastOperator,
    ExplainOperator,
    ChallengeOperator,
    GeneralizeOperator,
    SpecializeOperator,
    SimulateOperator,
    ReflectOperator,
    CompressOperator,
    ForgetOperator,
)


@pytest.fixture
def test_context():
    return OperatorContext(
        task_id=uuid4(),
        tenant_id="test_tenant",
        user_id="user_admin"
    )


@pytest.fixture
def test_provenance():
    return ProvenanceBlock(
        origin="ops_suite",
        timestamp=datetime.utcnow(),
        creator_id="ops_agent",
        confidence=1.0
    )


@pytest.fixture
def populated_repo(test_provenance):
    repo = InMemoryMemoryRepository()
    return repo


@pytest.mark.anyio
async def test_registry_and_recall_operator(test_context, test_provenance, populated_repo):
    registry = CMOSOperatorRegistry()
    registry.register(RecallOperator)

    # Add a mock node
    node = MemoryNode(
        node_type=CMOSNodeType.CLAIM,
        label="Test Recall Node",
        content="Stable performance results",
        provenance=test_provenance
    )
    await populated_repo.save_node(node)

    # Get Operator and Execute
    op = registry.get_operator("Recall")
    res = await op.execute(test_context, populated_repo, node_id=node.node_id)

    assert res.success
    assert len(res.output_nodes) == 1
    assert res.output_nodes[0].label == "Test Recall Node"
    assert res.telemetry.operator_name == "Recall"


@pytest.mark.anyio
async def test_verify_operator(test_context, test_provenance, populated_repo):
    # Setup claim with supporting evidence node
    claim = MemoryNode(
        node_type=CMOSNodeType.CLAIM,
        label="Claim to Verify",
        content="Execution succeeded under load",
        provenance=test_provenance
    )
    evidence = MemoryNode(
        node_type=CMOSNodeType.EVIDENCE,
        label="Factual Evidence",
        content="CPU utilization matched expectations",
        provenance=test_provenance
    )

    await populated_repo.save_node(claim)
    await populated_repo.save_node(evidence)

    edge = MemoryEdge(
        source_id=claim.node_id,
        target_id=evidence.node_id,
        edge_type=CMOSEdgeType.SUPPORT,
        provenance=test_provenance
    )
    await populated_repo.save_edge(edge)

    verify_op = VerifyOperator()
    res = await verify_op.execute(test_context, populated_repo, node_id=claim.node_id)

    assert res.success
    assert res.output_nodes[0].state == NodeState.VALIDATED


@pytest.mark.anyio
async def test_compare_and_contrast_operators(test_context, test_provenance, populated_repo):
    node_a = MemoryNode(node_type=CMOSNodeType.STRATEGY, label="Strategy A", content="First strategy", provenance=test_provenance)
    node_b = MemoryNode(node_type=CMOSNodeType.STRATEGY, label="Strategy B", content="Second strategy", provenance=test_provenance)

    await populated_repo.save_node(node_a)
    await populated_repo.save_node(node_b)

    comp_op = CompareOperator()
    contrast_op = ContrastOperator()

    res_comp = await comp_op.execute(test_context, populated_repo, node_a_id=node_a.node_id, node_b_id=node_b.node_id)
    res_contrast = await contrast_op.execute(test_context, populated_repo, node_a_id=node_a.node_id, node_b_id=node_b.node_id)

    assert len(res_comp.output_nodes) == 1
    assert "Shared features" in res_comp.output_nodes[0].content

    assert len(res_contrast.output_nodes) == 1
    assert "Diff:" in res_contrast.output_nodes[0].content


@pytest.mark.anyio
async def test_simulate_and_overlay_operators(test_context, test_provenance, populated_repo):
    sim_op = SimulateOperator()
    res = await sim_op.execute(test_context, populated_repo, virtual_content="Testing mock virtual branches")

    assert len(res.output_nodes) == 1
    # Verify overlay container is populated without writing to repo
    assert len(test_context.graph_overlay.nodes) == 1
