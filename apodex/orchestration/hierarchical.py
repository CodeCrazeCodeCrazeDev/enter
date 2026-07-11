from __future__ import annotations
import logging
import uuid
from typing import List, Dict, Any, Optional

logger = logging.getLogger("apodex.orchestration")


class AgentState:
    def __init__(self) -> None:
        self.status = "initialized"  # initialized, active, completed, failed


class WorkerAgent:
    """Isolated task-specific executor with static/gated tool permissions (E8)."""

    def __init__(self, role_id: str, allowed_tools: List[str]) -> None:
        self.id = f"{role_id}_{uuid.uuid4().hex[:6]}"
        self.role_id = role_id
        self.allowed_tools = allowed_tools
        self.state = AgentState()

    async def execute(self, task_description: str) -> Dict[str, Any]:
        self.state.status = "active"
        logger.info(f"Worker {self.id} executing task: {task_description}")

        # Simulate executing the configured tool
        executed_actions = []
        if self.allowed_tools:
            executed_actions.append({
                "tool": self.allowed_tools[0],
                "args": {"task": task_description},
                "status": "success"
            })

        self.state.status = "completed"
        return {
            "status": "completed",
            "role_id": self.role_id,
            "executed_actions": executed_actions,
            "summary": f"Completed using tool: {self.allowed_tools[0] if self.allowed_tools else 'none'}"
        }


class CoordinatorAgent:
    """Coordinator Agent responsible for delegating execution tasks to child workers."""

    def __init__(self, role_id: str) -> None:
        self.id = f"{role_id}_{uuid.uuid4().hex[:6]}"
        self.role_id = role_id
        self.workers: Dict[str, WorkerAgent] = {}

    def register_worker(self, worker: WorkerAgent) -> None:
        self.workers[worker.id] = worker
        logger.info(f"Coordinator {self.id} registered worker: {worker.id}")

    async def execute(self, task_description: str) -> Dict[str, Any]:
        logger.info(f"Coordinator {self.id} coordinating task: {task_description}")

        worker_trajectories = []
        summary_parts = []

        # Run all registered workers concurrently
        import asyncio
        tasks = []
        worker_list = list(self.workers.values())

        for w in worker_list:
            tasks.append(w.execute(task_description))

        if tasks:
            results = await asyncio.gather(*tasks)
            for w, res in zip(worker_list, results):
                worker_trajectories.append({
                    "role_id": w.role_id,
                    "trajectory": res
                })
                summary_parts.append(res["summary"])

        return {
            "status": "completed",
            "role_id": self.role_id,
            "worker_trajectories": worker_trajectories,
            "summary": f"Delegated tasks to workers: {', '.join(summary_parts)}"
        }


class HierarchicalOrchestrator:
    """Master Orchestrator class managing coordinators and enforcing budget-coordination limits (E8)."""

    def __init__(self, orchestrator_id: str = "orchestrator", max_coordinators: int = 5, max_workers_per_coordinator: int = 5) -> None:
        self.orchestrator_id = orchestrator_id
        self.coordinators: List[CoordinatorAgent] = []
        self.max_coordinators = max_coordinators
        self.max_workers_per_coordinator = max_workers_per_coordinator

    def register_coordinator(self, coordinator: CoordinatorAgent) -> None:
        # Enforce E8 Hard Limit: Coordinator Budget Guard
        if len(self.coordinators) >= self.max_coordinators:
            logger.warning(f"Orchestrator limit hit. Ignoring coordinator registration: {coordinator.id}")
            return
        self.coordinators.append(coordinator)

    async def orchestrate(self, goal: str) -> Dict[str, Any]:
        logger.info(f"Orchestration started: {goal}")

        coordinator_results = []
        final_summaries = []

        for coord in self.coordinators:
            # Enforce E8 Hard Limit: Workers per Coordinator budget guard
            if len(coord.workers) > self.max_workers_per_coordinator:
                logger.warning(f"Coordinator {coord.id} exceeds max worker budget. Truncating workers.")
                # Truncate to limit
                worker_keys = list(coord.workers.keys())[:self.max_workers_per_coordinator]
                coord.workers = {k: coord.workers[k] for k in worker_keys}

            res = await coord.execute(goal)
            coordinator_results.append(res)
            final_summaries.append(res["summary"])

        return {
            "status": "success",
            "orchestrator_id": self.orchestrator_id,
            "coordinator_results": coordinator_results,
            "final_summary": f"Orchestrated successfully: {'; '.join(final_summaries)}"
        }
