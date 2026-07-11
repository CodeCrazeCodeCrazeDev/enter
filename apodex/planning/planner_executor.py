from __future__ import annotations
from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field


class RoadmapStep(BaseModel):
    step_id: str
    goal: str
    action_type: str
    parameters: Dict[str, Any] = Field(default_factory=dict)


class StrategicRoadmap(BaseModel):
    goal: str
    steps: List[RoadmapStep] = Field(default_factory=list)


class StrategicPlanner:
    """Strategic Planner generating execution roadmap steps."""

    def __init__(self) -> None:
        self.history: List[Dict[str, Any]] = []

    async def create_roadmap(self, goal: str) -> StrategicRoadmap:
        # Strategic plan must be stored in history
        self.history.append({"goal": goal, "status": "planning"})

        # Return a simple multi-step plan
        steps = [
            RoadmapStep(step_id="step_1", goal=f"Formulate approach for {goal}", action_type="research"),
            RoadmapStep(step_id="step_2", goal=f"Verify findings for {goal}", action_type="validation")
        ]
        return StrategicRoadmap(goal=goal, steps=steps)


class TaskExecutor:
    """Task Executor running steps in isolation without polluting the Planner context."""

    async def execute_step(self, step: RoadmapStep) -> Dict[str, Any]:
        # Return isolated execution payload
        return {
            "status": "success",
            "step_id": step.step_id,
            "extracted_payload": f"Execution result of action {step.action_type} for goal: {step.goal}"
        }


class PlanVerifier:
    """Verifies executed output against the roadmap step constraints."""

    async def verify(self, step: RoadmapStep, result: Dict[str, Any]) -> bool:
        return result.get("status") == "success" and "extracted_payload" in result
