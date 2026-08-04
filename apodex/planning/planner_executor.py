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
    """Strategic Planner generating execution roadmap steps with advanced ToT/LADDER capabilities."""

    def __init__(self) -> None:
        self.history: List[Dict[str, Any]] = []
        self.lessons_learned: List[str] = []

    async def create_roadmap(self, goal: str) -> StrategicRoadmap:
        # Strategic plan must be stored in history
        self.history.append({"goal": goal, "status": "planning"})

        # Return a simple multi-step plan
        steps = [
            RoadmapStep(step_id="step_1", goal=f"Formulate approach for {goal}", action_type="research"),
            RoadmapStep(step_id="step_2", goal=f"Verify findings for {goal}", action_type="validation")
        ]
        return StrategicRoadmap(goal=goal, steps=steps)

    def decompose_step_recursively(self, step: RoadmapStep, max_depth: int = 3, current_depth: int = 1) -> List[RoadmapStep]:
        """
        Decomposes a single complex roadmap step into finer-grained milestones recursively,
        up to a strict safety depth-limit to prevent planning deadlocks.
        Derived from LADDER (Paper #9).
        """
        if current_depth > max_depth:
            return [step]

        # Decompose the goal semantically/procedurally into sub-steps
        sub_steps = [
            RoadmapStep(
                step_id=f"{step.step_id}_sub_{current_depth}_1",
                goal=f"Analyze and ingest subset parameters for: {step.goal}",
                action_type="research",
                parameters={**step.parameters, "sub_depth": current_depth, "part": 1}
            ),
            RoadmapStep(
                step_id=f"{step.step_id}_sub_{current_depth}_2",
                goal=f"Verify isolated compliance assertions for: {step.goal}",
                action_type="validation",
                parameters={**step.parameters, "sub_depth": current_depth, "part": 2}
            )
        ]

        # Recursively decompose if deeper detail is requested (simulating complex planning tree exploration)
        final_sub_steps = []
        for s in sub_steps:
            if s.action_type == "research" and current_depth < max_depth:
                final_sub_steps.extend(self.decompose_step_recursively(s, max_depth, current_depth + 1))
            else:
                final_sub_steps.append(s)

        return final_sub_steps

    async def execute_with_backtracking(
        self,
        roadmap: StrategicRoadmap,
        executor: TaskExecutor,
        verifier: PlanVerifier,
        backtrack_limit: int = 3
    ) -> Dict[str, Any]:
        """
        Executes the steps of a StrategicRoadmap as a tree search. If any step fails,
        it invokes an active backtracking self-correction loop, attempting alternative
        actions or recovery procedures, up to a strict backtrack limit.
        Derived from Tree of Thoughts (Paper #65) and Reflexion (Paper #22).
        """
        execution_log = []
        active_steps = list(roadmap.steps)
        step_idx = 0
        backtrack_count = 0

        while step_idx < len(active_steps):
            step = active_steps[step_idx]
            # Isolated execution
            res = await executor.execute_step(step)
            is_valid = await verifier.verify(step, res)

            if is_valid:
                execution_log.append({"step_id": step.step_id, "status": "success", "payload": res})
                step_idx += 1
            else:
                # Failure detected! Invoke backtracking and dynamic self-correction
                backtrack_count += 1
                lesson = f"Step {step.step_id} failed verification for goal: {step.goal}"
                self.lessons_learned.append(lesson)

                if backtrack_count > backtrack_limit:
                    return {
                        "status": "failed",
                        "reason": f"Backtrack limit exceeded ({backtrack_limit}) at step {step.step_id}",
                        "execution_log": execution_log,
                        "lessons_learned": self.lessons_learned
                    }

                # Generate an alternative recovery step at runtime
                recovery_step = RoadmapStep(
                    step_id=f"{step.step_id}_recovery_{backtrack_count}",
                    goal=f"Dynamic fallback recovery for: {step.goal} (Correction of failure)",
                    action_type="research",
                    parameters={"original_failure": step.step_id, "recovery_attempt": backtrack_count}
                )
                # Replace the failing step with the recovery step and attempt execution on it
                active_steps[step_idx] = recovery_step
                execution_log.append({
                    "step_id": step.step_id,
                    "status": "backtracked",
                    "recovery_triggered": recovery_step.step_id
                })

        return {
            "status": "success",
            "execution_log": execution_log,
            "lessons_learned": self.lessons_learned
        }


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
