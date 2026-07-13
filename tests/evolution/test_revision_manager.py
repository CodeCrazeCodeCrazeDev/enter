from __future__ import annotations
import uuid
import pytest
from apodex.evolution.common.models import CostMode
from apodex.evolution.revision.manager import RevisionSessionManager
from apodex.safety.core import ImmutableSafetyCore


@pytest.mark.asyncio
async def test_revision_session_plateau():
    """
    Verifies that the RevisionSessionManager runs a session and stops when a plateau is hit
    (i.e. score improvement < 0.01).
    """
    safety = ImmutableSafetyCore()
    manager = RevisionSessionManager(safety_core=safety)

    task_id = uuid.uuid4()
    # Mocking rounds where the scores don't improve (plateau)
    mock_rounds = [
        "{\n  \"processed\": true,\n  \"summary\": \"Refactored version\"\n}",
        "{\n  \"processed\": true,\n  \"summary\": \"Refactored version\"\n}"  # Same content -> plateau
    ]

    session = await manager.run_improvement_session(
        task_id=task_id,
        tenant_id="tenant_x",
        user_id="user_y",
        prompt="Optimize code structure.",
        initial_output="Standard raw code.",
        cost_mode=CostMode.MAX_QUALITY,
        target_id="prompt_template_01",
        mock_rounds_content=mock_rounds
    )

    assert session.stop_reason == "PLATEAU"
    assert len(session.rounds) == 2


@pytest.mark.asyncio
async def test_revision_session_degradation():
    """
    Verifies that the RevisionSessionManager terminates the revision cycle and returns DEGRADATION
    when the score of a new revision falls below the previous round.
    """
    safety = ImmutableSafetyCore()
    manager = RevisionSessionManager(safety_core=safety)

    task_id = uuid.uuid4()
    # Mocking a degradation step (round 2 is empty/bad syntax -> score degrades)
    mock_rounds = [
        "{ \"processed\": true }",  # good round 1 (quality=0.7)
        "bad code syntax {"          # bad round 2 (quality=0.5 -> degradation)
    ]

    session = await manager.run_improvement_session(
        task_id=task_id,
        tenant_id="tenant_x",
        user_id="user_y",
        prompt="Optimize structure.",
        initial_output="Normal text",
        cost_mode=CostMode.MAX_QUALITY,
        target_id="prompt_template_02",
        mock_rounds_content=mock_rounds
    )

    assert session.stop_reason == "DEGRADATION"
    assert len(session.rounds) == 2


@pytest.mark.asyncio
async def test_revision_session_budget():
    """
    Verifies that the revision session respects Cost Mode budget constraints
    (e.g., FAST_CHEAP capped at 1 round).
    """
    safety = ImmutableSafetyCore()
    manager = RevisionSessionManager(safety_core=safety)

    task_id = uuid.uuid4()
    # Mocking multiple good rounds
    mock_rounds = [
        "{ \"step\": 1 }",
        "{ \"step\": 2 }",
        "{ \"step\": 3 }"
    ]

    session = await manager.run_improvement_session(
        task_id=task_id,
        tenant_id="tenant_x",
        user_id="user_y",
        prompt="Fast query.",
        initial_output="Normal output.",
        cost_mode=CostMode.FAST_CHEAP,
        target_id="prompt_template_03",
        mock_rounds_content=mock_rounds
    )

    assert session.stop_reason == "BUDGET_LIMIT_REACHED"
    assert len(session.rounds) == 1
