from __future__ import annotations
from typing import Dict, Any, List

# Forward to canonical APODEX capability
from apodex.planning.planner_executor import (
    StrategicPlanner as CanonicalStrategicPlanner,
    TaskExecutor as CanonicalTaskExecutor,
    PlanVerifier as CanonicalPlanVerifier,
    RoadmapStep as CanonicalRoadmapStep,
    StrategicRoadmap as CanonicalStrategicRoadmap,
)

class RoadmapStep(CanonicalRoadmapStep):
    """Legacy compatibility adapter forwarding to canonical APODEX capability."""
    def __init__(self, description: str = "", **data: Any) -> None:
        # Backward-compatible construction mapping description to goal/step_id if needed
        goal_val = description or data.get("goal") or "Default step"
        step_id_val = data.get("step_id") or "legacy_step"
        action_type_val = data.get("action_type") or "legacy_action"
        super().__init__(step_id=step_id_val, goal=goal_val, action_type=action_type_val, **data)

    @property
    def description(self) -> str:
        return self.goal

    @description.setter
    def description(self, value: str) -> None:
        self.goal = value

class StrategicPlanner(CanonicalStrategicPlanner):
    """Legacy compatibility adapter forwarding to canonical APODEX capability."""
    pass

class TaskExecutor(CanonicalTaskExecutor):
    """Legacy compatibility adapter forwarding to canonical APODEX capability."""
    pass

class PlanVerifier(CanonicalPlanVerifier):
    """Legacy compatibility adapter forwarding to canonical APODEX capability."""
    pass
