"""
Lightweight mock and conformance tests for the Apodex meta-system components.
"""

from __future__ import annotations

import pytest
from apodex.meta.experience_db import (
    ExperienceDatabase,
    ExecutionTrace,
    FailureSignature,
    DistilledLesson,
)
from apodex.meta.safety_manager import (
    SafetyGuardrailManager,
    DiffProposal,
)
from apodex.meta.harness_loop import HarnessLoopController
from apodex.meta.research_loop import (
    ResearchLoopController,
    TrialConfig,
)


@pytest.mark.asyncio
async def test_experience_database_flows():
    # Instantiate DB
    db = ExperienceDatabase()

    # Save and retrieve a task execution trace
    trace = ExecutionTrace(
        task_id="task_001",
        steps=[{"step": 1, "action": "web_search", "result": "success"}],
        metrics={"duration_sec": 4.5, "token_count": 1200},
        errors=[]
    )
    await db.save_trace(trace)

    retrieved = await db.get_trace("task_001")
    assert retrieved is not None
    assert retrieved.task_id == "task_001"
    assert retrieved.metrics["token_count"] == 1200

    # Save and query distilled lessons
    lesson = DistilledLesson(
        lesson_id="lesson_01",
        domain="coding",
        description="Avoid wrapped markdown inside python execution tools",
        trigger_conditions=["markdown codeblock in tool arguments"],
        actionable_guidelines=["Parse and clean arguments before calling compiler"]
    )
    await db.save_distilled_lesson(lesson)

    coding_lessons = await db.query_lessons_for_domain("coding")
    assert len(coding_lessons) == 1
    assert coding_lessons[0].lesson_id == "lesson_01"


@pytest.mark.asyncio
async def test_safety_guardrail_manager():
    manager = SafetyGuardrailManager()

    # Check a safe change
    safe_proposal = DiffProposal(
        component_key="standard_system_prompt",
        original_value="...",
        proposed_value="...",
        change_type="prompt"
    )
    assert manager.is_modification_safe(safe_proposal) is True

    # Check modification to an immutable zone (fails safety check)
    unsafe_proposal = DiffProposal(
        component_key="system_safety_constraints",
        original_value="...",
        proposed_value="...",
        change_type="prompt"
    )
    assert manager.is_modification_safe(unsafe_proposal) is False


@pytest.mark.asyncio
async def test_harness_loop_controller():
    db = ExperienceDatabase()
    safety_manager = SafetyGuardrailManager()
    harness = HarnessLoopController(db, safety_manager)

    # Register an active scaffolding component
    harness.active_scaffolding["coding_assistant_system_prompt"] = "You are a coding assistant..."

    # Register multiple occurrences of a failure to trigger weakness mining
    sig = FailureSignature(
        signature_id="sig_json_err",
        error_pattern="JSON parsing failed on tool execution",
        occurrence_count=5,
        affected_tasks=["t1", "t2", "t3"]
    )
    await db.save_failure_signature(sig)

    # Test weakness mining
    weaknesses = await harness.mine_weaknesses()
    assert len(weaknesses) == 1
    assert weaknesses[0].signature_id == "sig_json_err"

    # Test harness proposal generation
    proposal = await harness.propose_harness_edit(weaknesses[0])
    assert proposal is not None
    assert proposal.change_type == "prompt"
    assert "JSON" in proposal.proposed_value

    # Test validate and deploy
    deployed = await harness.validate_and_deploy(proposal)
    assert deployed is True
    assert "Format your tool call in pure JSON." in harness.active_scaffolding["coding_assistant_system_prompt"]


@pytest.mark.asyncio
async def test_research_loop_controller():
    db = ExperienceDatabase()
    researcher = ResearchLoopController(db)

    # Test SFT training dataset compilation
    dataset_path = await researcher.compile_training_dataset("mathematics")
    assert dataset_path == "sandbox/data/sft_mathematics.jsonl"

    # Launch simulation of sandboxed container run
    config = TrialConfig(
        trial_id="trial_101",
        base_model_path="models/base-v2",
        training_script_path="scripts/train.py",
        dataset_path=dataset_path,
        hyperparameters={"epochs": 3, "lr": 1e-5}
    )

    result = await researcher.launch_sandbox_experiment(config)
    assert result.success is True
    assert "models/finetuned_trial_101" == result.new_model_weights_path
    assert result.metrics["math_accuracy"] == 0.688

    # Generate PR
    pr = await researcher.generate_git_pull_request(result)
    assert pr["status"] == "pending_human_review"
    assert "trial-trial_101" in pr["branch_name"]
