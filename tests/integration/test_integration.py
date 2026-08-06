"""Integration tests validating joint behavior of multiple cognitive upgrades."""

from __future__ import annotations

import pytest
from apodex.cognition.meta_reasoner import (
    MetaReasonerObserver,
    LoopConfig,
    TurnContext,
)
from apodex.orchestration.hierarchical import (
    CoordinatorAgent,
    HierarchicalOrchestrator,
    WorkerAgent,
)


@pytest.mark.asyncio
async def test_meta_reasoner_loop_intervention():
    # Setup observer
    observer = MetaReasonerObserver(max_repeated_calls=2)

    cfg = LoopConfig(max_turns=10, task_id="t_int_01", role_id="agent_int")
    await observer.on_loop_start(cfg)

    # Turn 1: Normal call
    ctx_1 = TurnContext(
        turn=1, max_turns=10, task_id="t_int_01", role_id="agent_int",
        ai_text="Searching first step", thinking="",
        tool_calls=[{"name": "search", "args": {"q": "test"}}],
        messages=[], usage={"input_tokens": 1000, "output_tokens": 200},
        metadata={}
    )
    res_1 = await observer.on_llm_response(ctx_1)
    assert res_1 is None  # No loop yet

    # Turn 2: Repetitive tool call (reaches max_repeated_calls=2)
    ctx_2 = TurnContext(
        turn=2, max_turns=10, task_id="t_int_01", role_id="agent_int",
        ai_text="Searching again", thinking="",
        tool_calls=[{"name": "search", "args": {"q": "test"}}],
        messages=[], usage={"input_tokens": 1000, "output_tokens": 200},
        metadata={}
    )
    res_2 = await observer.on_llm_response(ctx_2)

    # Active intervention must be triggered
    assert res_2 is not None
    assert res_2.pop_last_message is True
    assert res_2.continue_to_next_turn is True
    assert "WARNING" in res_2.inject_messages[0]


@pytest.mark.asyncio
async def test_hierarchical_cognitive_orchestration():
    # Construct complete cognitive multi-agent tree
    orchestrator = HierarchicalOrchestrator(orchestrator_id="master_orch")

    coordinator = CoordinatorAgent(role_id="math_coordinator")
    worker_1 = WorkerAgent(role_id="calculator", allowed_tools=["run_calc"])
    worker_2 = WorkerAgent(role_id="validator", allowed_tools=["validate_math"])

    coordinator.register_worker(worker_1)
    coordinator.register_worker(worker_2)
    orchestrator.register_coordinator(coordinator)

    # Run top-level orchestrator
    result = await orchestrator.orchestrate("Solve formula: 2 + 2 * 3")

    assert result["status"] == "success"
    assert result["orchestrator_id"] == "master_orch"
    assert len(result["coordinator_results"]) == 1

    coord_res = result["coordinator_results"][0]
    assert coord_res["role_id"] == "math_coordinator"
    assert len(coord_res["worker_trajectories"]) == 2
    assert coord_res["worker_trajectories"][0]["role_id"] == "calculator"
    assert coord_res["worker_trajectories"][1]["role_id"] == "validator"
