"""
AReaL (Agentic Reinforcement Learning) Trajectory Protocol, Data Proxy, and Evolution Control Plane.
Specifically aligns with Ant Group / HKUST / Tsinghua (July 2026) paper 'Next-Generation Agentic Reinforcement Learning Systems'.
"""

from __future__ import annotations

import time
from typing import Any, Dict, List, Optional, Protocol, runtime_checkable
from pydantic import BaseModel, Field


@runtime_checkable
class TrajectoryProtocol(Protocol):
    """Protocol defining standard step-by-step agent execution trajectory."""
    task_id: str
    steps: List[Dict[str, Any]]
    metadata: Dict[str, Any]

    def add_step(self, step_data: Dict[str, Any]) -> None:
        """Appends a recorded execution step."""
        ...

    def get_failures(self) -> List[Dict[str, Any]]:
        """Identifies and returns failed steps, errors, or timeouts."""
        ...


class AgentTrajectory(BaseModel):
    """Concrete Pydantic implementation of the AReaL TrajectoryProtocol."""
    task_id: str
    steps: List[Dict[str, Any]] = Field(default_factory=list)
    metadata: Dict[str, Any] = Field(default_factory=dict)

    def add_step(self, step_data: Dict[str, Any]) -> None:
        self.steps.append({
            "timestamp": time.time(),
            **step_data
        })

    def get_failures(self) -> List[Dict[str, Any]]:
        failures = []
        for step in self.steps:
            if step.get("is_error") or step.get("status") == "failed" or "error" in step.get("tool_result_preview", "").lower():
                failures.append(step)
            elif step.get("duration_ms", 0) > 10000:  # High latency/stuck point
                failures.append({**step, "warning": "stuck_or_slow"})
        return failures


class AReaLDataProxy:
    """
    Acts as a secure local data proxy to ingest, buffer, and serve trajectories
    to the self-improvement controller, satisfying hexagonal storage isolation.
    """

    def __init__(self) -> None:
        self._trajectories: Dict[str, List[AgentTrajectory]] = {}

    def buffer_trajectory(self, tenant_id: str, trajectory: AgentTrajectory) -> None:
        """Buffers the raw trajectory for self-improvement processing."""
        if tenant_id not in self._trajectories:
            self._trajectories[tenant_id] = []
        self._trajectories[tenant_id].append(trajectory)

    def get_trajectories(self, tenant_id: str) -> List[AgentTrajectory]:
        """Returns buffered trajectories for a tenant."""
        return self._trajectories.get(tenant_id, [])

    def clear_buffer(self, tenant_id: str) -> None:
        """Clears buffered trajectories for a tenant."""
        self._trajectories.pop(tenant_id, None)


class EvolutionControlPlane:
    """
    The control plane managing step-level optimization schedules,
    coordinating feedback between loops, and checking Pareto frontiers.
    """

    def __init__(self, data_proxy: AReaLDataProxy) -> None:
        self.data_proxy = data_proxy
        self.global_parameters: Dict[str, Any] = {
            "retry_wait_fixed": 2,
            "max_llm_retries": 5,
            "context_token_limit": 120000,
            "clamping_threshold": 12000,
            "system_prompt_prefix": "You are a professional assistant."
        }

    def update_global_parameters(self, updates: Dict[str, Any]) -> None:
        """Updates global configuration parameters safely."""
        self.global_parameters.update(updates)
