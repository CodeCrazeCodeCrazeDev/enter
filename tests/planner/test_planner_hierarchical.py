from __future__ import annotations

import pytest

from apodex.planning.planner_executor import StrategicPlanner, StrategicRoadmap


async def test_hierarchical_htn_decomposition_depth_limit():
    # 1. Test with standard depth limit
    planner = StrategicPlanner(max_depth=3)
    roadmap = await planner.create_roadmap("design causal model")

    assert isinstance(roadmap, StrategicRoadmap)
    assert len(roadmap.steps) == 2

    # 2. Verify sub-steps are recursively populated
    step_1 = roadmap.steps[0]
    assert len(step_1.sub_steps) > 0
    assert step_1.sub_steps[0].preconditions == ["context_valid"]
    assert step_1.sub_steps[0].action_type == "decomposition"


async def test_hierarchical_htn_max_depth_zero_yields_no_sub_steps():
    # 3. Setting max depth to zero should prevent recursive decomposition
    planner = StrategicPlanner(max_depth=0)
    roadmap = await planner.create_roadmap("rapid prototype")

    step_1 = roadmap.steps[0]
    assert len(step_1.sub_steps) == 0
