"""Hermetic Mock-Based Unit and Integration Tests for AgentHarness v2 Upgrades.

Tests all ten upgrades using a direct synchronous runner wrapper to ensure
cross-plugin compatibility without relying on external pytest async loops.
"""

from __future__ import annotations

import asyncio
from typing import Any

from agent_harness.core.v2.memory import PersistentMemoryManager
from agent_harness.core.v2.graphs import ThoughtGraph, WorldModelRepresentation
from agent_harness.core.v2.orchestrator import (
    WorkerAgent,
    CoordinatorAgent,
    MasterOrchestrator,
    PlanAndActEngine,
    ParallelVerificationService,
)
from agent_harness.core.v2.reasoner import MetaReasoner, ActiveLearningService


class MockLLMClient:
    """Mock LLM client for provider-agnostic, network-free, hermetic testing."""

    class MockResponse:
        def __init__(self, content: str) -> None:
            self.content = content
            self.usage = {"prompt_tokens": 10, "completion_tokens": 10}

    def __init__(self, default_response: str = "Mocked response content") -> None:
        self.default_response = default_response

    async def chat(self, messages: list[dict[str, Any]], timeout: float | None = None) -> MockResponse:
        last_message = messages[-1]["content"] if messages else ""
        if "concise summary" in last_message:
            return self.MockResponse("Summary of mock execution: success.")
        if "final report" in last_message:
            return self.MockResponse("Final synthesized mock report.")
        if "strategic plan" in last_message:
            return self.MockResponse("Mock plan: Step 1. Think, Step 2. Execute.")
        if "Verify the execution" in last_message or "Validate the execution" in last_message:
            return self.MockResponse("VERIFIED_SUCCESS")
        if "most critical missing fact" in last_message:
            return self.MockResponse("Mock informational query fact.")
        return self.MockResponse(self.default_response)


def run_async(coro: Any) -> Any:
    return asyncio.run(coro)


def test_persistent_memory_and_learning() -> None:
    """Tests Persistent Semantic Memory (Upgrade 4) and Long-Term Learning Memory (Upgrade 9)."""
    mem = PersistentMemoryManager(db_path=":memory:")

    # Store & retrieve semantic items
    mem.store_semantic("test-task-1", "belief", "The earth is round.", confidence=1.0)
    mem.store_semantic("test-task-1", "fact", "Gravity exists.", confidence=0.95)

    beliefs = mem.retrieve_semantic("test-task-1", "belief")
    assert len(beliefs) == 1
    assert beliefs[0]["content"] == "The earth is round."

    facts = mem.retrieve_semantic("test-task-1", "fact")
    assert len(facts) == 1
    assert facts[0]["content"] == "Gravity exists."

    # Store & retrieve learning strategies (Upgrade 9)
    mem.store_learning_strategy("math_problems", "Iterative breakdown", 0.95, {"tool": "calculator"})
    strategies = mem.retrieve_learning_strategies("math_problems")
    assert len(strategies) == 1
    assert strategies[0]["strategy"] == "Iterative breakdown"
    assert strategies[0]["tool_performance"] == {"tool": "calculator"}


def test_graph_of_thought_and_world_model() -> None:
    """Tests Graph-of-Thought (Upgrade 2) and World Model (Upgrade 5)."""
    # GoT
    got = ThoughtGraph()
    n1 = got.add_thought("n1", "Idea A")
    n2 = got.add_thought("n2", "Idea B")
    got.add_dependency("n1", "n2")

    valid = got.get_valid_thoughts()
    assert len(valid) == 2

    got.prune_branch("n1")
    valid_after_pruning = got.get_valid_thoughts()
    assert len(valid_after_pruning) == 0  # n2 is dependent on n1 and pruned too

    # World Model
    mem = PersistentMemoryManager(db_path=":memory:")
    wm = WorldModelRepresentation(mem, "task-1")
    wm.add_knowledge("A", "related_to", "B")
    wm.add_causal_link("Smoking", "Cancer", weight=0.9)
    wm.add_temporal_sequence("Morning", "before", "Noon")

    snapshot = wm.get_world_snapshot()
    assert len(snapshot) == 3


def test_hierarchical_orchestration_and_plan_act() -> None:
    """Tests Hierarchical Multi-Agent (Upgrade 1) and Plan-and-Act (Upgrade 3)."""
    llm = MockLLMClient()
    workers = [WorkerAgent("W1"), WorkerAgent("W2")]
    coord = CoordinatorAgent("C1", workers)
    master = MasterOrchestrator([coord])

    async def run() -> None:
        # Run Hierarchical orchestration directly
        res = await master.orchestrate("Solve climate change", {}, llm)
        assert res["status"] == "completed"
        assert "final_answer" in res

        # Run Plan-and-Act Engine (Upgrade 3)
        engine = PlanAndActEngine(master)
        engine_res = await engine.run_plan_act("Optimize engine output", llm)
        assert "plan" in engine_res
        assert "execution" in engine_res
        assert engine_res["verification_verdict"] == "VERIFIED_SUCCESS"

    run_async(run())


def test_parallel_verification() -> None:
    """Tests Concurrent Domain and Meta Verification (Upgrade 7)."""
    service = ParallelVerificationService()
    async def run() -> None:
        res = await service.run_parallel_verification({"code": "print(1)", "source": "verified_web_source_ref_1"})
        assert res["meta_status"] == "pass"
        assert len(res["domain_verdicts"]) == 3

    run_async(run())


def test_meta_reasoner() -> None:
    """Tests Meta Reasoner monitoring turn execution (Upgrade 8)."""
    reasoner = MetaReasoner()
    response_text = "Repeated SGLang think think think loop containing long thought process patterns..."
    assert len(response_text) > 50
    monitored = reasoner.monitor_turn("User query", response_text, tokens_used=1000)
    assert monitored["status"] == "monitored"
    assert reasoner.diagnostics["token_waste"] > 0


def test_active_learning() -> None:
    """Tests Active Learning uncertainty estimation and query loops (Upgrade 10)."""
    mem = PersistentMemoryManager(db_path=":memory:")
    wm = WorldModelRepresentation(mem, "task-99")
    llm = MockLLMClient()

    active_learner = ActiveLearningService(confidence_threshold=0.8)

    async def run() -> None:
        # Estimate uncertainty of empty model
        uncertainty = await active_learner.estimate_uncertainty(wm.get_world_snapshot())
        assert uncertainty == 1.0  # complete uncertainty initially

        # Run Active Learning Loop
        result = await active_learner.run_active_learning_cycle(wm, "quantum gravity", llm)
        assert result["final_confidence"] > 0.0

    run_async(run())
