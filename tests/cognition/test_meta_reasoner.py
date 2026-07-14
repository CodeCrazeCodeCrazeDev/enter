from __future__ import annotations

from apodex.cognition.meta_reasoner import (
    InterventionResponse,
    LoopConfig,
    MetaReasonerObserver,
    TurnContext,
)


def _ctx(**kwargs) -> TurnContext:
    base = {"turn": 1, "max_turns": 10, "task_id": "t", "role_id": "agent", "ai_text": ""}
    base.update(kwargs)
    return TurnContext(**base)


async def test_on_loop_start_resets_state():
    obs = MetaReasonerObserver()
    obs.tool_call_history = [{"name": "x", "args": {}}]
    obs.unrelated_turns = 5
    await obs.on_loop_start(LoopConfig(task_id="t"))
    assert obs.tool_call_history == []
    assert obs.unrelated_turns == 0


async def test_extract_goal_from_system_message():
    obs = MetaReasonerObserver()
    ctx = _ctx(
        ai_text="working",
        messages=[{"role": "system", "content": "The GOAL is to win"}],
    )
    await obs.on_llm_response(ctx)
    assert obs.goal == "The GOAL is to win"


async def test_echo_trap_detected_on_repeated_tool_calls():
    obs = MetaReasonerObserver(max_repeated_calls=2)
    call = [{"name": "search", "args": {"q": "x"}}]
    first = await obs.on_llm_response(_ctx(tool_calls=call))
    assert first is None
    second = await obs.on_llm_response(_ctx(tool_calls=call))
    assert isinstance(second, InterventionResponse)
    assert second.pop_last_message is True
    assert second.continue_to_next_turn is True
    assert "Echo Trap" in second.inject_messages[0]
    # history cleared to prevent repeated triggers
    assert obs.tool_call_history == []


async def test_distinct_tool_calls_do_not_trigger_echo_trap():
    obs = MetaReasonerObserver(max_repeated_calls=2)
    assert await obs.on_llm_response(_ctx(tool_calls=[{"name": "a", "args": {}}])) is None
    assert await obs.on_llm_response(_ctx(tool_calls=[{"name": "b", "args": {}}])) is None


async def test_goal_drift_triggers_after_three_unrelated_turns():
    obs = MetaReasonerObserver(drift_threshold=0.2)
    obs.goal = "build a rocket engine"
    resp = None
    for _ in range(3):
        resp = await obs.on_llm_response(_ctx(ai_text="completely different topic entirely"))
    assert isinstance(resp, InterventionResponse)
    assert "Goal Drift" in resp.inject_messages[0]
    assert obs.unrelated_turns == 0


async def test_related_turn_resets_drift_counter():
    obs = MetaReasonerObserver(drift_threshold=0.2)
    obs.goal = "build a rocket engine"
    await obs.on_llm_response(_ctx(ai_text="unrelated words here"))
    await obs.on_llm_response(_ctx(ai_text="unrelated words here"))
    assert obs.unrelated_turns == 2
    # highly similar text resets counter
    await obs.on_llm_response(_ctx(ai_text="build a rocket engine"))
    assert obs.unrelated_turns == 0


def test_calculate_similarity():
    obs = MetaReasonerObserver()
    assert obs._calculate_similarity("a b", "a b") == 1.0
    assert obs._calculate_similarity("", "a") == 0.0
    assert obs._calculate_similarity("a b", "b c") == 1 / 3
