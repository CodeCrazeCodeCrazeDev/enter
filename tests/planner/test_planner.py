"""Unit and integration tests for the Planner / Executor Separation subsystem."""

from __future__ import annotations

import pytest
from agent_harness.core.runtime.orchestration.planner_executor import (
    PlanVerifier,
    RoadmapStep,
    StrategicPlanner,
    TaskExecutor,
)


@pytest.mark.asyncio
async def test_planner_and_executor_isolation():
    planner = StrategicPlanner()
    executor = TaskExecutor()
    verifier = PlanVerifier()

    # Create strategic roadmap
    roadmap = await planner.create_roadmap("Synthesize new chemical compounds")
    assert len(roadmap.steps) >= 2
    assert planner.history[0]["goal"] == "Synthesize new chemical compounds"

    # Execute step 1 in isolation
    step_1 = roadmap.steps[0]
    exec_result_1 = await executor.execute_step(step_1)

    assert exec_result_1["status"] == "success"
    assert "extracted_payload" in exec_result_1

    # Verify output against original requirements
    is_valid = await verifier.verify(step_1, exec_result_1)
    assert is_valid is True

    # Critical requirement: Ensure that executing steps does NOT pollute the planner's history/context window
    assert len(planner.history) == 1
    assert "extracted_payload" not in planner.history[0]
