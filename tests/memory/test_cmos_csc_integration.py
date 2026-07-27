"""Comprehensive system integration tests simulating CMOS in real cognitive workloads.

Simulates stable connections with Cognitive System Controllers (CSC), active Query Planners,
dynamic Pluggable Operator executions, and background Scheduler tasks.
"""

from __future__ import annotations

import pytest
from uuid import uuid4
from datetime import datetime

from apodex.memory.cmos.models import MemoryNode, MemoryEdge, CMOSNodeType, CMOSEdgeType, ProvenanceBlock
from apodex.memory.cmos.repositories import InMemoryMemoryRepository
from apodex.memory.cmos.interfaces import OperatorContext
from apodex.memory.cmos.planner import CMOSQueryPlanner
from apodex.memory.cmos.registry import CMOSOperatorRegistry
from apodex.memory.cmos.scheduler import CMOSMemoryScheduler
from apodex.memory.cmos.operators import RecallOperator, CompareOperator


@pytest.fixture
def clean_provenance():
    return ProvenanceBlock(
        origin="csc_simulated_brain",
        timestamp=datetime.utcnow(),
        creator_id="csc_orchestrator",
        confidence=1.0
    )


@pytest.mark.anyio
async def test_csc_decision_pipeline_simulation(clean_provenance):
    repo = InMemoryMemoryRepository()
    registry = CMOSOperatorRegistry()
    registry.register(RecallOperator)
    registry.register(CompareOperator)

    planner = CMOSQueryPlanner()
    scheduler = CMOSMemoryScheduler()

    ctx = OperatorContext(
        task_id=uuid4(),
        tenant_id="institutional_tenant",
        user_id="executive_agent"
    )

    # 1. Seed existing strategy nodes
    strategy_a = MemoryNode(
        node_type=CMOSNodeType.STRATEGY,
        label="Strategy A",
        content="Aggressive prompt variant containing multi-turn search",
        provenance=clean_provenance
    )
    strategy_b = MemoryNode(
        node_type=CMOSNodeType.STRATEGY,
        label="Strategy B",
        content="Conservative prompt variant containing zero-shot lookup",
        provenance=clean_provenance
    )
    await repo.save_node(strategy_a)
    await repo.save_node(strategy_b)

    # 2. CSC issues cognitive objective target: Compare both strategies
    objective = "Compare Strategy A with Strategy B to identify optimization patterns"
    execution_plan = await planner.plan(objective, ctx)

    # Validate compiled plan structure
    assert len(execution_plan) == 3
    assert execution_plan[0]["operator"] == "Recall"
    assert execution_plan[1]["operator"] == "Recall"
    assert execution_plan[2]["operator"] == "Compare"

    # 3. Simulate step-by-step execution by CSC
    resolved_nodes = []
    for step in execution_plan:
        op = registry.get_operator(step["operator"])
        res = await op.execute(ctx, repo, **step["args"])
        assert res.success
        resolved_nodes.extend(res.output_nodes)

    # 4. Final step execution (Comparison assertion creation)
    comp_op = CompareOperator()
    comp_res = await comp_op.execute(ctx, repo, node_a_id=strategy_a.node_id, node_b_id=strategy_b.node_id)
    assert len(comp_res.output_nodes) == 1
    assert "Shared features" in comp_res.output_nodes[0].content

    # 5. Schedule background compression job via infrastructure scheduler
    await scheduler.schedule_task("medium-term", "recalculate_utility", target_node_id=strategy_a.node_id)
    assert len(scheduler.queues["medium-term"]) == 1
