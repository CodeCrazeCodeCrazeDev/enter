from __future__ import annotations
import uuid

class AgentState:
    def __init__(self, status: str = "initialized") -> None:
        self.status = status

class WorkerAgent:
    def __init__(self, role_id: str, allowed_tools: list[str] | None = None) -> None:
        self.role_id = role_id
        self.allowed_tools = allowed_tools or []
        self.id = f"{role_id}_{uuid.uuid4().hex[:6]}"
        self.state = AgentState("initialized")

    async def execute(self, task: str) -> dict:
        self.state.status = "completed"
        return {
            "status": "completed",
            "role_id": self.role_id,
            "executed_actions": [{"tool": tool} for tool in self.allowed_tools]
        }

class CoordinatorAgent:
    def __init__(self, role_id: str) -> None:
        self.role_id = role_id
        self.workers = {}

    def register_worker(self, worker: WorkerAgent) -> None:
        self.workers[worker.id] = worker

    async def execute(self, task: str) -> dict:
        tools_used = []
        for w in self.workers.values():
            tools_used.extend(w.allowed_tools)
        tool_str = ", ".join(tools_used) if tools_used else "default_tools"
        return {
            "status": "completed",
            "role_id": self.role_id,
            "worker_trajectories": [{"step": i + 1, "worker_id": wid} for i, wid in enumerate(self.workers)],
            "summary": f"Coordinated sub-worker results utilizing [{tool_str}] for task '{task}'."
        }

class HierarchicalOrchestrator:
    def __init__(self, orchestrator_id: str = "master_orchestrator", max_coordinators: int = 10, max_workers_per_coordinator: int = 10) -> None:
        self.orchestrator_id = orchestrator_id
        self.max_coordinators = max_coordinators
        self.max_workers_per_coordinator = max_workers_per_coordinator
        self.coordinators = []

    def register_coordinator(self, coordinator: CoordinatorAgent) -> None:
        if len(self.coordinators) < self.max_coordinators:
            self.coordinators.append(coordinator)

    async def orchestrate(self, task: str) -> dict:
        all_tools = []
        coordinator_results = []
        for coord in self.coordinators:
            if len(coord.workers) > self.max_workers_per_coordinator:
                keys = list(coord.workers.keys())[:self.max_workers_per_coordinator]
                coord.workers = {k: coord.workers[k] for k in keys}

            worker_trajectories = []
            for w in coord.workers.values():
                all_tools.extend(w.allowed_tools)
                worker_trajectories.append({
                    "role_id": w.role_id,
                    "status": "completed",
                    "executed_actions": [{"tool": tool} for tool in w.allowed_tools]
                })
            coordinator_results.append({
                "role_id": coord.role_id,
                "worker_trajectories": worker_trajectories
            })

        tools_summary = ", ".join(all_tools) if all_tools else "standard_tools"
        return {
            "status": "success",
            "orchestrator_id": self.orchestrator_id,
            "coordinator_results": coordinator_results,
            "final_summary": f"Completed hierarchical orchestration for task '{task}' utilizing [{tools_summary}]."
        }
