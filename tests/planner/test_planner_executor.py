from __future__ import annotations

from typing import Dict, Any
import pytest

from apodex.planning.planner_executor import (
    PlanVerifier,
    RoadmapStep,
    StrategicPlanner,
    StrategicRoadmap,
    TaskExecutor,
)


@pytest.mark.asyncio
async def test_create_roadmap_builds_two_step_plan():
    planner = StrategicPlanner()
    roadmap = await planner.create_roadmap("launch product")
    assert isinstance(roadmap, StrategicRoadmap)
    assert roadmap.goal == "launch product"
    assert [s.step_id for s in roadmap.steps] == ["step_1", "step_2"]
    assert roadmap.steps[0].action_type == "research"
    assert roadmap.steps[1].action_type == "validation"


@pytest.mark.asyncio
async def test_create_roadmap_records_history():
    planner = StrategicPlanner()
    await planner.create_roadmap("goal a")
    await planner.create_roadmap("goal b")
    assert planner.history == [
        {"goal": "goal a", "status": "planning"},
        {"goal": "goal b", "status": "planning"},
    ]


@pytest.mark.asyncio
async def test_execute_step_returns_isolated_payload():
    executor = TaskExecutor()
    step = RoadmapStep(step_id="step_1", goal="do thing", action_type="research")
    result = await executor.execute_step(step)
    assert result["status"] == "success"
    assert result["step_id"] == "step_1"
    assert "research" in result["extracted_payload"]
    assert "do thing" in result["extracted_payload"]


@pytest.mark.asyncio
async def test_plan_verifier_accepts_successful_result():
    step = RoadmapStep(step_id="step_1", goal="g", action_type="research")
    result = await TaskExecutor().execute_step(step)
    assert await PlanVerifier().verify(step, result) is True


@pytest.mark.parametrize(
    "result",
    [
        {"status": "failed", "extracted_payload": "x"},
        {"status": "success"},
        {},
    ],
)
@pytest.mark.asyncio
async def test_plan_verifier_rejects_invalid_results(result):
    step = RoadmapStep(step_id="step_1", goal="g", action_type="research")
    assert await PlanVerifier().verify(step, result) is False


def test_roadmap_step_default_parameters():
    step = RoadmapStep(step_id="s", goal="g", action_type="research")
    assert step.parameters == {}


# =====================================================================
# Advanced Integration & Regression Tests for Research-to-Code Improvements
# =====================================================================

@pytest.mark.asyncio
async def test_hierarchical_task_decomposition_ladder():
    """Verifies Hierarchical Task Decomposition (LADDER / Paper #9) of strategic targets."""
    planner = StrategicPlanner()
    step = RoadmapStep(step_id="step_complex", goal="Assemble marketing funnel", action_type="research")

    # Decompose step recursively up to depth 2
    sub_steps = planner.decompose_step_recursively(step, max_depth=2)

    assert len(sub_steps) > 1
    # Check that ids are generated correctly with hierarchical sub-depth markers
    assert any("complex_sub_1_1" in s.step_id for s in sub_steps)
    assert any("complex_sub_1_2" in s.step_id for s in sub_steps)
    # The sub_steps parameters should retain original parameters and sub-depth metadata
    assert all("sub_depth" in s.parameters for s in sub_steps)


@pytest.mark.asyncio
async def test_execute_with_backtracking_tree_of_thoughts_success():
    """Verifies that normal, successful planning executions proceed directly without backtracking."""
    planner = StrategicPlanner()
    executor = TaskExecutor()
    verifier = PlanVerifier()

    # Define a roadmap with steps
    roadmap = await planner.create_roadmap("Launch SaaS product")

    res = await planner.execute_with_backtracking(roadmap, executor, verifier)
    assert res["status"] == "success"
    assert len(res["execution_log"]) == 2
    assert all(log["status"] == "success" for log in res["execution_log"])
    assert len(res["lessons_learned"]) == 0


@pytest.mark.asyncio
async def test_execute_with_backtracking_tree_of_thoughts_recovery():
    """Verifies dynamic backtracking (Tree of Thoughts / Paper #65) and Reflexion failure logging (Paper #22)."""
    planner = StrategicPlanner()
    verifier = PlanVerifier()

    # Create a custom executor that fails for "step_1" but succeeds for any fallback/recovery steps
    class CustomBacktrackingExecutor(TaskExecutor):
        async def execute_step(self, step: RoadmapStep) -> Dict[str, Any]:
            if "step_1" in step.step_id and "recovery" not in step.step_id:
                # Simulate failure on the primary step
                return {"status": "failed", "extracted_payload": "simulated primary failure"}
            return {"status": "success", "extracted_payload": f"successful recovery step: {step.goal}"}

    executor = CustomBacktrackingExecutor()
    roadmap = await planner.create_roadmap("Build landing page")

    res = await planner.execute_with_backtracking(roadmap, executor, verifier, backtrack_limit=2)

    assert res["status"] == "success"
    # Should contain a backtracked entry for step_1 and a successful entry for the recovery and step_2
    log_statuses = [item["status"] for item in res["execution_log"]]
    assert "backtracked" in log_statuses
    assert "success" in log_statuses

    # Verify that Reflexion-style lessons learned were recorded
    assert len(res["lessons_learned"]) >= 1
    assert any("failed verification" in lesson for lesson in res["lessons_learned"])


@pytest.mark.asyncio
async def test_execute_with_backtracking_tree_of_thoughts_exceeded_limit():
    """Verifies that backtracking limit terminates execution safely when failures persist."""
    planner = StrategicPlanner()
    verifier = PlanVerifier()

    # Create an executor that always fails
    class FailingExecutor(TaskExecutor):
        async def execute_step(self, step: RoadmapStep) -> Dict[str, Any]:
            return {"status": "failed", "extracted_payload": "always failing"}

    executor = FailingExecutor()
    roadmap = await planner.create_roadmap("Solve P vs NP")

    # Run with limit = 1
    res = await planner.execute_with_backtracking(roadmap, executor, verifier, backtrack_limit=1)

    assert res["status"] == "failed"
    assert "Backtrack limit exceeded" in res["reason"]
    assert len(res["lessons_learned"]) >= 2  # primary step fail + recovery step fail
