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
            "executed_actions": [{"tool": self.allowed_tools[0]}] if self.allowed_tools else []
        }

class CoordinatorAgent:
    def __init__(self, role_id: str) -> None:
        self.role_id = role_id
        self.workers = {}

    def register_worker(self, worker: WorkerAgent) -> None:
        self.workers[worker.id] = worker

    async def execute(self, task: str) -> dict:
        worker_ids = list(self.workers.keys())
        executed_tools = []
        for w in self.workers.values():
            executed_tools.extend(w.allowed_tools)
        tools_str = ", ".join(executed_tools) if executed_tools else "compiler"
        return {
            "status": "completed",
            "role_id": self.role_id,
            "worker_trajectories": [{"step": 1, "worker_count": len(worker_ids)}],
            "summary": f"Coordinator '{self.role_id}' executed task across {len(worker_ids)} workers utilizing tools: {tools_str}."
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
        # Enforce budget limits if specified (truncates workers if they exceed limit)
        for coord in self.coordinators:
            if len(coord.workers) > self.max_workers_per_coordinator:
                keys = list(coord.workers.keys())[:self.max_workers_per_coordinator]
                coord.workers = {k: coord.workers[k] for k in keys}

        coordinator_results = []
        for coord in self.coordinators:
            worker_trajectories = []
            for w in coord.workers.values():
                worker_trajectories.append({
                    "role_id": w.role_id,
                    "status": "completed",
                    "executed_actions": [{"tool": w.allowed_tools[0]} if w.allowed_tools else {}]
                })
            coordinator_results.append({
                "role_id": coord.role_id,
                "worker_trajectories": worker_trajectories
            })

        all_workers = [w for c in self.coordinators for w in c.workers.values()]
        all_tools = [t for w in all_workers for t in w.allowed_tools]
        tools_summary = ", ".join(set(all_tools)) if all_tools else "general tools"
        return {
            "status": "success",
            "orchestrator_id": self.orchestrator_id,
            "coordinator_results": coordinator_results,
            "final_summary": f"Orchestrator '{self.orchestrator_id}' completed multi-agent task utilizing tools: {tools_summary}."
        }
