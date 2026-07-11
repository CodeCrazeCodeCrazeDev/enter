"""Unit and integration tests for the Hierarchical Multi-Agent Orchestration subsystem."""

from __future__ import annotations

import pytest
from agent_harness.core.runtime.orchestration.hierarchical import (
    AgentState,
    CoordinatorAgent,
    HierarchicalOrchestrator,
    WorkerAgent,
)


@pytest.mark.asyncio
async def test_worker_agent_execution():
    worker = WorkerAgent(role_id="tester", allowed_tools=["run_test"])
    assert worker.id.startswith("tester_")
    assert worker.state.status == "initialized"

    result = await worker.execute("Run code unit tests.")
    assert result["status"] == "completed"
    assert "tester" in result["role_id"]
    assert len(result["executed_actions"]) == 1
    assert result["executed_actions"][0]["tool"] == "run_test"
    assert worker.state.status == "completed"


@pytest.mark.asyncio
async def test_coordinator_delegation():
    coordinator = CoordinatorAgent(role_id="manager")
    worker = WorkerAgent(role_id="coder", allowed_tools=["python_compiler"])
    coordinator.register_worker(worker)

    assert worker.id in coordinator.workers

    result = await coordinator.execute("Build and run verification script")
    assert result["status"] == "completed"
    assert "manager" in result["role_id"]
    # Verify sub-worker results are compiled
    assert len(result["worker_trajectories"]) == 1
    assert "compiler" in result["summary"]


@pytest.mark.asyncio
async def test_hierarchical_orchestrator():
    orchestrator = HierarchicalOrchestrator()
    coordinator = CoordinatorAgent(role_id="coord_01")
    worker = WorkerAgent(role_id="work_01", allowed_tools=["web_search"])
    coordinator.register_worker(worker)
    orchestrator.register_coordinator(coordinator)

    result = await orchestrator.orchestrate("Search and compile report on supercomputing")
    assert result["status"] == "success"
    assert "orchestrator" in result["orchestrator_id"]
    assert "web_search" in result["final_summary"]
