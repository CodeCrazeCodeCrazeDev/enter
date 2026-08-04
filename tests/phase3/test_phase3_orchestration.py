from __future__ import annotations

import os
import time
import pytest
from apodex.skills.models import CostTier
from apodex.cognition.meta_reasoner import LoopConfig, TurnContext, MetaReasonerObserver
from apodex.memory.semantic_memory import (
    Belief,
    EvidenceCard,
    Fact,
    SemanticMemory,
    SQLiteMemoryRepository,
    UnresolvedQuestion,
)
from apodex.orchestration.hierarchical import (
    CoordinatorAgent,
    HierarchicalOrchestrator,
    WorkerAgent,
)
from apodex.cognition.dataset_generator import TrajectoryDatasetCompiler
from apodex.cognition.trajectory_verification import (
    TwoLevelCreditAssignment,
    MultiDimensionalTrajectoryVerifier,
)


@pytest.mark.asyncio
async def test_e1_echo_trap_detector():
    observer = MetaReasonerObserver(max_repeated_calls=2)
    cfg = LoopConfig(task_id="t_e1_01")
    await observer.on_loop_start(cfg)

    # Turn 1
    ctx_1 = TurnContext(
        turn=1, max_turns=10, task_id="t_e1_01", role_id="ag_01",
        ai_text="Executing search", thinking="",
        tool_calls=[{"name": "web_search", "args": {"q": "AI history"}}],
        messages=[], usage={}, metadata={}
    )
    res_1 = await observer.on_llm_response(ctx_1)
    assert res_1 is None

    # Turn 2: Duplicate tool call with identical arguments
    ctx_2 = TurnContext(
        turn=2, max_turns=10, task_id="t_e1_01", role_id="ag_01",
        ai_text="Executing search again", thinking="",
        tool_calls=[{"name": "web_search", "args": {"q": "AI history"}}],
        messages=[], usage={}, metadata={}
    )
    res_2 = await observer.on_llm_response(ctx_2)

    assert res_2 is not None
    assert res_2.pop_last_message is True
    assert res_2.continue_to_next_turn is True
    assert "Echo Trap" in res_2.inject_messages[0]


def test_e3_semantic_memory_deduplication_and_pruning():
    repo = SQLiteMemoryRepository(db_path=":memory:")
    # Small max token threshold to trigger pruning (e.g., 40 tokens)
    memory = SemanticMemory(repository=repo, max_semantic_tokens=40, max_cards=3)

    # 1. Add identical Evidence Cards (same URL and content hash)
    card1 = EvidenceCard(
        evidence_id="ev_1", source_url="https://test.com", content="Duplicate info", extracted_at=time.time()
    )
    card2 = EvidenceCard(
        evidence_id="ev_2", source_url="https://test.com", content="Duplicate info", extracted_at=time.time()
    )

    memory.add_evidence(card1)
    memory.add_evidence(card2)

    # Assert that deduplication kept only one card in the repository
    all_cards = repo.load_all_evidence()
    assert len(all_cards) == 1
    assert all_cards[0].evidence_id == "ev_1"

    # 2. Add multiple cards to trigger raw card count limit
    card3 = EvidenceCard(
        evidence_id="ev_3", source_url="https://test3.com", content="Distinct info 3", extracted_at=time.time()
    )
    card4 = EvidenceCard(
        evidence_id="ev_4", source_url="https://test4.com", content="Distinct info 4", extracted_at=time.time()
    )
    card5 = EvidenceCard(
        evidence_id="ev_5", source_url="https://test5.com", content="Distinct info 5", extracted_at=time.time()
    )

    memory.add_evidence(card3)
    memory.add_evidence(card4)
    memory.add_evidence(card5)

    all_cards = repo.load_all_evidence()
    # Should cap at max_cards = 3
    assert len(all_cards) <= 3

    # 3. Add facts/beliefs to blow the token limit
    fact1 = Fact(fact_id="f1", assertion="The catalyst is lithium.", confidence=0.9)
    fact2 = Fact(fact_id="f2", assertion="The pressure is extremely high.", confidence=0.3)  # lower confidence
    belief1 = Belief(belief_id="b1", hypothesis="Fusion is clean.", strength=0.8, last_updated=time.time())

    memory.add_fact(fact1)
    memory.add_fact(fact2)
    memory.add_belief(belief1)

    # Assert consolidation has run and lower confidence facts are dropped to stay within limit
    stored_facts = memory.get_facts()
    stored_fact_ids = {f.fact_id for f in stored_facts}
    assert "f2" not in stored_fact_ids


@pytest.mark.asyncio
async def test_e5_goal_drift_monitor():
    observer = MetaReasonerObserver(drift_threshold=0.2)
    cfg = LoopConfig(task_id="t_e5_01")
    await observer.on_loop_start(cfg)

    # Feed system prompt goal during loop start
    initial_messages = [
        {"role": "system", "content": "The goal is to research volatile chemistry catalysts for energy generation."}
    ]

    # Turn 1: totally unrelated text
    ctx_1 = TurnContext(
        turn=1, max_turns=10, task_id="t_e5_01", role_id="ag_01",
        ai_text="The blue sky is wonderful and the weather is very warm today.", thinking="",
        tool_calls=[], messages=initial_messages, usage={}, metadata={}
    )
    res_1 = await observer.on_llm_response(ctx_1)
    assert res_1 is None

    # Turn 2: totally unrelated text
    ctx_2 = TurnContext(
        turn=2, max_turns=10, task_id="t_e5_01", role_id="ag_01",
        ai_text="Cats are small mammals with fluffy tails and soft fur.", thinking="",
        tool_calls=[], messages=initial_messages, usage={}, metadata={}
    )
    res_2 = await observer.on_llm_response(ctx_2)
    assert res_2 is None

    # Turn 3: totally unrelated text (exceeds turn threshold and rolling window of 3 turns)
    ctx_3 = TurnContext(
        turn=3, max_turns=10, task_id="t_e5_01", role_id="ag_01",
        ai_text="Pineapples do not grow on pine trees but on small shrubs.", thinking="",
        tool_calls=[], messages=initial_messages, usage={}, metadata={}
    )
    res_3 = await observer.on_llm_response(ctx_3)

    assert res_3 is not None
    assert res_3.pop_last_message is True
    assert "Goal Drift" in res_3.inject_messages[0]


@pytest.mark.asyncio
async def test_e8_coordination_budget_guard():
    # Hard limits: 1 coordinator, 2 workers
    orchestrator = HierarchicalOrchestrator(
        orchestrator_id="budget_orch", max_coordinators=1, max_workers_per_coordinator=2
    )

    coord_1 = CoordinatorAgent(role_id="coord_primary")
    coord_2 = CoordinatorAgent(role_id="coord_secondary")

    # Attempt to register 2 coordinators (limit is 1)
    orchestrator.register_coordinator(coord_1)
    orchestrator.register_coordinator(coord_2)

    assert len(orchestrator.coordinators) == 1
    assert orchestrator.coordinators[0].role_id == "coord_primary"

    # Register 3 workers to primary coordinator (limit is 2)
    w1 = WorkerAgent(role_id="w1", allowed_tools=["t1"])
    w2 = WorkerAgent(role_id="w2", allowed_tools=["t2"])
    w3 = WorkerAgent(role_id="w3", allowed_tools=["t3"])

    coord_1.register_worker(w1)
    coord_1.register_worker(w2)
    coord_1.register_worker(w3)

    # Executing orchestration should truncate the coordinator's workers to 2
    res = await orchestrator.orchestrate("Do work")
    assert res["status"] == "success"
    assert len(coord_1.workers) == 2


def test_e9_model_collapse_guard(tmp_path):
    # Strict mode: raise error on ratio > 50% self-generated
    compiler_strict = TrajectoryDatasetCompiler(max_self_generated_ratio=0.5, strict_mode=True)

    trace_real = [{"role": "system", "content": "Real trace"}]
    trace_self_1 = [{"role": "system", "content": "Self gen 1"}]
    trace_self_2 = [{"role": "system", "content": "Self gen 2"}]

    input_data = [
        {"messages": trace_real, "is_self_generated": False, "score": 1.0},
        {"messages": trace_self_1, "is_self_generated": True, "score": 0.3},
        {"messages": trace_self_2, "is_self_generated": True, "score": 0.8}
    ]

    # Ratio is 2/3 (66.7%), which exceeds 50% -> should raise ValueError in strict mode
    jsonl_file = os.path.join(tmp_path, "collapse_strict.jsonl")
    with pytest.raises(ValueError, match="Model-Collapse Guard"):
        compiler_strict.export_to_jsonl(input_data, jsonl_file)

    # Non-strict mode: should log warning and downsample self-generated data
    # (keeps 1 real and 1 self-generated record with the highest score: self_1 should be dropped as score 0.3 < 0.8)
    compiler_warn = TrajectoryDatasetCompiler(max_self_generated_ratio=0.5, strict_mode=False)
    jsonl_file_warn = os.path.join(tmp_path, "collapse_warn.jsonl")
    compiler_warn.export_to_jsonl(input_data, jsonl_file_warn)

    assert os.path.exists(jsonl_file_warn)
    with open(jsonl_file_warn, "r", encoding="utf-8") as f:
        lines = f.readlines()
        assert len(lines) == 2
        # Check that we kept the high-scoring self-generated trace (0.8 score)
        contents = [line for line in lines if "Self gen 2" in line]
        assert len(contents) == 1
        # Check that the low-scoring self-generated trace was dropped (0.3 score)
        contents_dropped = [line for line in lines if "Self gen 1" in line]
        assert len(contents_dropped) == 0


def test_e4_two_level_credit_assignment():
    assigner = TwoLevelCreditAssignment()
    trajectory = {
        "task_id": "task_e4_01",
        "steps": [
            {"step": 1, "action": "web_search"},
            {"step": 2, "action": "sandbox_run"}
        ]
    }

    # Successful trajectory
    res_success = assigner.assign_credit(trajectory.copy(), is_success=True)
    assert res_success["trajectory_credit"] == 1.0
    assert len(res_success["step_credits"]) == 2
    assert res_success["step_credits"][0]["credit"] == 0.5  # 1.0 * (1/2)
    assert res_success["step_credits"][1]["credit"] == 1.0  # 1.0 * (2/2)

    # Unsuccessful trajectory
    res_fail = assigner.assign_credit(trajectory.copy(), is_success=False)
    assert res_fail["trajectory_credit"] == -0.5
    assert len(res_fail["step_credits"]) == 2
    assert res_fail["step_credits"][0]["credit"] == -0.1  # -0.2 * (1/2)
    assert res_fail["step_credits"][1]["credit"] == -0.2  # -0.2 * (2/2)


def test_e10_multi_dimensional_trajectory_verification():
    verifier = MultiDimensionalTrajectoryVerifier()

    # High-quality messages
    good_messages = [
        {"role": "system", "content": "Goal: solve problem"},
        {"role": "user", "content": "Execute task"},
        {"role": "assistant", "content": "Completed with { [ ] } bracket format."}
    ]
    report_good = verifier.verify_trajectory(good_messages)
    assert report_good["is_high_quality"] is True
    assert report_good["syntax_score"] == 1.0

    # Low-quality messages (mismatched brackets + duplicates)
    bad_messages = [
        {"role": "system", "content": "Goal: solve problem"},
        {"role": "user", "content": "Execute task"},
        {"role": "assistant", "content": "Completed with { [ bracket format."},
        {"role": "assistant", "content": "Completed with { [ bracket format."}  # Duplicate turn
    ]
    report_bad = verifier.verify_trajectory(bad_messages)
    assert report_bad["syntax_score"] < 1.0
    assert report_bad["efficiency_score"] < 1.0
    assert report_bad["is_high_quality"] is False
