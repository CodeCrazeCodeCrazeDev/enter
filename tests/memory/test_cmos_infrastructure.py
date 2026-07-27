"""Unit tests for CMOS infrastructure, planning, and economics subsystems.

Validates Query Planner compilation, temporal scheduling, and multi-objective economics utility scoring.
"""

from __future__ import annotations

import pytest
from datetime import datetime, timedelta
from uuid import uuid4

from apodex.memory.cmos.models import MemoryNode, CMOSNodeType, ProvenanceBlock
from apodex.memory.cmos.interfaces import OperatorContext
from apodex.memory.cmos.planner import CMOSQueryPlanner
from apodex.memory.cmos.scheduler import CMOSMemoryScheduler
from apodex.memory.cmos.intelligence import MemoryEconomicsEngine


@pytest.mark.anyio
async def test_query_planner_comparison_intent():
    planner = CMOSQueryPlanner()
    ctx = OperatorContext(task_id=uuid4(), tenant_id="t1", user_id="u1")

    # Compile objective for strategy comparisons
    plan = await planner.plan("Compare Strategy A with Strategy B under Bear regime", ctx)

    assert len(plan) == 3
    assert plan[0]["operator"] == "Recall"
    assert plan[2]["operator"] == "Compare"


@pytest.mark.anyio
async def test_memory_scheduler_temporal_queues():
    scheduler = CMOSMemoryScheduler()

    # Schedule tasks across different temporal tiers
    await scheduler.schedule_task("immediate", "confidence_decay_update", node_id="node_123")
    await scheduler.schedule_task("long-term", "compression_run", ratio=0.5)

    assert len(scheduler.queues["immediate"]) == 1
    assert len(scheduler.queues["long-term"]) == 1

    completed_immediate = await scheduler.run_pending("immediate")
    assert completed_immediate == 1
    assert len(scheduler.queues["immediate"]) == 0


def test_memory_economics_utility_decay():
    engine = MemoryEconomicsEngine()

    prov = ProvenanceBlock(origin="test", creator_id="test", confidence=1.0)
    node_fresh = MemoryNode(
        node_type=CMOSNodeType.CLAIM,
        label="Fresh Claim",
        content="Short test content assertion",
        provenance=prov,
        retrieval_count=10,
        last_retrieved_at=datetime.utcnow()
    )

    node_old = MemoryNode(
        node_type=CMOSNodeType.CLAIM,
        label="Old Claim",
        content="Short test content assertion",
        provenance=prov,
        retrieval_count=10,
        last_retrieved_at=datetime.utcnow() - timedelta(days=5)
    )

    utility_fresh = engine.compute_utility(node_fresh)
    utility_old = engine.compute_utility(node_old)

    # Fresh node should yield a higher utility score than decaying old node
    assert utility_fresh > utility_old
