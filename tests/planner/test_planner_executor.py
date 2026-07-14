from __future__ import annotations

import pytest

from apodex.planning.planner_executor import (
    PlanVerifier,
    RoadmapStep,
    StrategicPlanner,
    StrategicRoadmap,
    TaskExecutor,
)


async def test_create_roadmap_builds_two_step_plan():
    planner = StrategicPlanner()
    roadmap = await planner.create_roadmap("launch product")
    assert isinstance(roadmap, StrategicRoadmap)
    assert roadmap.goal == "launch product"
    assert [s.step_id for s in roadmap.steps] == ["step_1", "step_2"]
    assert roadmap.steps[0].action_type == "research"
    assert roadmap.steps[1].action_type == "validation"


async def test_create_roadmap_records_history():
    planner = StrategicPlanner()
    await planner.create_roadmap("goal a")
    await planner.create_roadmap("goal b")
    assert planner.history == [
        {"goal": "goal a", "status": "planning"},
        {"goal": "goal b", "status": "planning"},
    ]


async def test_execute_step_returns_isolated_payload():
    executor = TaskExecutor()
    step = RoadmapStep(step_id="step_1", goal="do thing", action_type="research")
    result = await executor.execute_step(step)
    assert result["status"] == "success"
    assert result["step_id"] == "step_1"
    assert "research" in result["extracted_payload"]
    assert "do thing" in result["extracted_payload"]


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
async def test_plan_verifier_rejects_invalid_results(result):
    step = RoadmapStep(step_id="step_1", goal="g", action_type="research")
    assert await PlanVerifier().verify(step, result) is False


def test_roadmap_step_default_parameters():
    step = RoadmapStep(step_id="s", goal="g", action_type="research")
    assert step.parameters == {}
