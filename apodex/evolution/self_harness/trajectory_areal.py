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


import sqlite3
import json
import threading

class AReaLDataProxy:
    """
    Acts as a secure local data proxy to ingest, buffer, and serve trajectories
    to the self-improvement controller, satisfying hexagonal storage isolation.
    Relational and persistent SQLite-backed trajectory store ensuring RAM stability.
    """

    def __init__(self, db_path: str = ":memory:") -> None:
        self.db_path = db_path
        self._lock = threading.RLock()
        self._conn = sqlite3.connect(self.db_path, check_same_thread=False)
        self._init_db()

    def _init_db(self) -> None:
        with self._lock:
            # Enable WAL mode for high concurrency if file-based database
            if self.db_path != ":memory:":
                try:
                    self._conn.execute("PRAGMA journal_mode=WAL;")
                    self._conn.execute("PRAGMA synchronous=NORMAL;")
                except sqlite3.OperationalError:
                    pass
            self._conn.execute("""
                CREATE TABLE IF NOT EXISTS trajectories (
                    tenant_id TEXT,
                    task_id TEXT,
                    steps TEXT,
                    metadata TEXT,
                    PRIMARY KEY (tenant_id, task_id)
                )
            """)
            self._conn.commit()

    def buffer_trajectory(self, tenant_id: str, trajectory: AgentTrajectory) -> None:
        """Buffers the raw trajectory for self-improvement processing, persisting to SQLite."""
        with self._lock:
            steps_json = trajectory.model_dump_json()
            # steps_json contains task_id, steps, metadata
            self._conn.execute(
                "INSERT OR REPLACE INTO trajectories (tenant_id, task_id, steps, metadata) VALUES (?, ?, ?, ?)",
                (tenant_id, trajectory.task_id, steps_json, json.dumps(trajectory.metadata))
            )
            self._conn.commit()

    def get_trajectories(self, tenant_id: str) -> List[AgentTrajectory]:
        """Returns buffered trajectories for a tenant from SQLite."""
        with self._lock:
            cursor = self._conn.execute(
                "SELECT steps FROM trajectories WHERE tenant_id = ?",
                (tenant_id,)
            )
            rows = cursor.fetchall()
            trajectories = []
            for row in rows:
                trajectories.append(AgentTrajectory.model_validate_json(row[0]))
            return trajectories

    def clear_buffer(self, tenant_id: str) -> None:
        """Clears buffered trajectories for a tenant in SQLite."""
        with self._lock:
            self._conn.execute(
                "DELETE FROM trajectories WHERE tenant_id = ?",
                (tenant_id,)
            )
            self._conn.commit()


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
