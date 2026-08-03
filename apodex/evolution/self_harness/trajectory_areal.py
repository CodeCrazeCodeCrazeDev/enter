"""
AReaL (Agentic Reinforcement Learning) Trajectory Protocol, Data Proxy, and Evolution Control Plane.
Specifically aligns with Ant Group / HKUST / Tsinghua (July 2026) paper 'Next-Generation Agentic Reinforcement Learning Systems'.
"""

from __future__ import annotations

import time
import json
import sqlite3
import threading
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
    Persistently stores trajectories and steps in a relational SQLite schema.
    """

    def __init__(self, db_path: str = ":memory:") -> None:
        self.db_path = db_path
        self._lock = threading.RLock()
        self._conn = sqlite3.connect(db_path, check_same_thread=False)
        self._conn.execute("PRAGMA journal_mode=WAL;")
        self._init_db()

    def _init_db(self) -> None:
        with self._lock:
            self._conn.execute("""
                CREATE TABLE IF NOT EXISTS trajectories (
                    task_id TEXT PRIMARY KEY,
                    tenant_id TEXT,
                    metadata TEXT
                )
            """)
            self._conn.execute("""
                CREATE TABLE IF NOT EXISTS trajectory_steps (
                    task_id TEXT,
                    step_id TEXT,
                    node_type TEXT,
                    tool_name TEXT,
                    status TEXT,
                    is_error INTEGER,
                    tool_result_preview TEXT,
                    duration_ms INTEGER,
                    timestamp REAL,
                    step_data TEXT,
                    PRIMARY KEY (task_id, step_id, timestamp)
                )
            """)
            self._conn.commit()

    def buffer_trajectory(self, tenant_id: str, trajectory: AgentTrajectory) -> None:
        """Buffers the raw trajectory for self-improvement processing."""
        with self._lock:
            # Insert or replace trajectory
            self._conn.execute(
                "INSERT OR REPLACE INTO trajectories (task_id, tenant_id, metadata) VALUES (?, ?, ?)",
                (trajectory.task_id, tenant_id, json.dumps(trajectory.metadata))
            )
            # Insert steps
            for step in trajectory.steps:
                # Normalize values
                step_id = step.get("step_id") or step.get("id") or f"step_{time.time()}"
                node_type = step.get("node_type", "tool_execution")
                tool_name = step.get("tool_name") or step.get("tool") or ""
                status = step.get("status", "success")
                is_error = 1 if step.get("is_error") else 0
                tool_result_preview = step.get("tool_result_preview") or step.get("result") or ""
                duration_ms = step.get("duration_ms") or step.get("duration") or 0
                timestamp = step.get("timestamp") or time.time()

                self._conn.execute(
                    """INSERT OR REPLACE INTO trajectory_steps
                       (task_id, step_id, node_type, tool_name, status, is_error, tool_result_preview, duration_ms, timestamp, step_data)
                       VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                    (trajectory.task_id, step_id, node_type, tool_name, status, is_error, tool_result_preview, duration_ms, timestamp, json.dumps(step))
                )
            self._conn.commit()

    def get_trajectories(self, tenant_id: str) -> List[AgentTrajectory]:
        """Returns buffered trajectories for a tenant."""
        with self._lock:
            cur = self._conn.execute("SELECT task_id, metadata FROM trajectories WHERE tenant_id = ?", (tenant_id,))
            trajectories = []
            for row in cur.fetchall():
                task_id, meta_str = row
                metadata = json.loads(meta_str) if meta_str else {}

                # Fetch steps
                steps_cur = self._conn.execute(
                    "SELECT step_data FROM trajectory_steps WHERE task_id = ? ORDER BY timestamp ASC",
                    (task_id,)
                )
                steps = []
                for s_row in steps_cur.fetchall():
                    steps.append(json.loads(s_row[0]))

                trajectories.append(AgentTrajectory(task_id=task_id, steps=steps, metadata=metadata))
            return trajectories

    def clear_buffer(self, tenant_id: str) -> None:
        """Clears buffered trajectories for a tenant."""
        with self._lock:
            # Get all task IDs for this tenant
            cur = self._conn.execute("SELECT task_id FROM trajectories WHERE tenant_id = ?", (tenant_id,))
            task_ids = [row[0] for row in cur.fetchall()]
            for task_id in task_ids:
                self._conn.execute("DELETE FROM trajectory_steps WHERE task_id = ?", (task_id,))
            self._conn.execute("DELETE FROM trajectories WHERE tenant_id = ?", (tenant_id,))
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
