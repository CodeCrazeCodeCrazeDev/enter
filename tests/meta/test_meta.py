"""
Upgraded conformance and integration tests for the Apodex meta-system components.
"""

from __future__ import annotations

import pytest
import time
from apodex.meta.experience_db import (
    ExperienceDatabase,
    ExecutionTrace,
    FailureSignature,
    DistilledLesson,
    PersonalEvolutionProfile,
    ResearchTicket,
    CapabilityDelta,
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
from apodex.meta.verifier_layer import (
    LLMAsAJudgeNode,
    SelfCritiqueCritic,
    DenseRewardModel,
    GroundedFactChecker,
    RuntimeAgentVerifier,
)


@pytest.mark.asyncio
async def test_experience_database_flows():
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
async def test_personal_evolution_profile_flows():
    db = ExperienceDatabase()
    safety_manager = SafetyGuardrailManager()
    harness = HarnessLoopController(db, safety_manager)

    # Load default PEP when not found
    await harness.load_user_session("usr-abc")
    assert harness.active_pep is not None
    assert harness.active_pep.user_id == "usr-abc"
    assert harness.active_scaffolding["verbosity"] == "medium"

    # Save and reload custom PEP
    pep = PersonalEvolutionProfile(
        user_id="usr-abc",
        version=2,
        style_preferences={"verbosity": "low", "explanation_depth": "concise"},
        cost_latency_preferences={"profile_mode": "fast_cheap", "max_cost_per_session_usd": 1.0},
        domain_vocabulary={"Jules": "verification expert"}
    )
    await db.save_pep(pep)

    await harness.load_user_session("usr-abc")
    assert harness.active_pep.version == 2
    assert harness.active_scaffolding["verbosity"] == "low"
    assert harness.active_scaffolding["vocabulary"]["Jules"] == "verification expert"


@pytest.mark.asyncio
async def test_safety_guardrail_and_tiered_approvals():
    manager = SafetyGuardrailManager()

    # Check safe prompt change -> Tier 1
    proposal_1 = DiffProposal(
        component_key="prompt_formatting",
        original_value="...",
        proposed_value="...",
        change_type="prompt"
    )
    assert manager.is_modification_safe(proposal_1) is True
    assert manager.determine_approval_tier(proposal_1) == 1

    # Check routing change -> Tier 2
    proposal_2 = DiffProposal(
        component_key="route_math_tasks",
        original_value="...",
        proposed_value="...",
        change_type="routing_logic"
    )
    assert manager.determine_approval_tier(proposal_2) == 2

    # Check model weights change -> Tier 3
    proposal_3 = DiffProposal(
        component_key="base_model_weights",
        original_value="...",
        proposed_value="...",
        change_type="model_weights"
    )
    assert manager.determine_approval_tier(proposal_3) == 3

    # Check safe immutable block modification check -> Tier 4
    proposal_4 = DiffProposal(
        component_key="system_safety_constraints",
        original_value="...",
        proposed_value="...",
        change_type="prompt"
    )
    assert manager.is_modification_safe(proposal_4) is False
    assert manager.determine_approval_tier(proposal_4) == 4

    # Run regression suite and verify cryptographic logs are written
    report = await manager.run_regression_suite({"some": "config"}, approval_tier=2)
    assert report.is_valid is True
    assert report.approval_tier == 2
    assert len(manager.audit_log) == 1
    assert "audit_hash" in manager.audit_log[0]


@pytest.mark.asyncio
async def test_harness_scoring_and_rollbacks():
    db = ExperienceDatabase()
    safety_manager = SafetyGuardrailManager()
    harness = HarnessLoopController(db, safety_manager)

    # 1. Custom fast_cheap profile: Heavy penalty for extra tokens
    pep = PersonalEvolutionProfile(
        user_id="usr-budget",
        cost_latency_preferences={"profile_mode": "fast_cheap"}
    )
    await db.save_pep(pep)
    await harness.load_user_session("usr-budget")

    # A proposed change that doubles token counts (ratio = 2.0) should yield negative score in fast_cheap
    score = harness.calculate_suitability_score(quality=0.9, token_ratio=2.0, latency_ratio=1.0, satisfaction=0.8)
    assert score < 0.0

    # 2. Max quality profile: Prioritizes success over token overhead
    pep_high = PersonalEvolutionProfile(
        user_id="usr-rich",
        cost_latency_preferences={"profile_mode": "max_quality"}
    )
    await db.save_pep(pep_high)
    await harness.load_user_session("usr-rich")

    score_high = harness.calculate_suitability_score(quality=0.95, token_ratio=2.0, latency_ratio=1.0, satisfaction=1.0)
    assert score_high > 0.0

    # 3. Test deploy and rollbacks
    harness.active_scaffolding["prompt_cfg"] = "baseline prompt"

    prop = DiffProposal(
        component_key="prompt_cfg",
        original_value="baseline prompt",
        proposed_value="mutated prompt v1",
        change_type="prompt"
    )

    # First deploy
    deployed = await harness.validate_and_deploy(prop, quality_est=0.95, token_ratio=1.0, latency_ratio=1.0, satisfaction=1.0)
    assert deployed is True
    assert harness.active_scaffolding["prompt_cfg"] == "mutated prompt v1"

    # Rollback -> Revert and blacklist "mutated prompt v1"
    reverted = await harness.trigger_rollback("prompt_cfg")
    assert reverted is True
    assert harness.active_scaffolding["prompt_cfg"] == "baseline prompt"
    assert "mutated prompt v1" in harness.blacklisted_mutations

    # Second deploy of the exact same value should now be rejected as blacklisted
    redeployed = await harness.validate_and_deploy(prop)
    assert redeployed is False


@pytest.mark.asyncio
async def test_feedback_loop_tickets_and_deltas():
    db = ExperienceDatabase()
    safety_manager = SafetyGuardrailManager()
    harness = HarnessLoopController(db, safety_manager)
    researcher = ResearchLoopController(db)

    # 1. Escalate a failure signature to a ResearchTicket from harness loop
    failure = FailureSignature(
        signature_id="err_asyncio",
        error_pattern="asynchronous loop deadlock",
        occurrence_count=5,
        affected_tasks=["tr-1", "tr-2"]
    )
    await harness.handle_persistent_failure(failure)

    # Verify ticket resides in Experience DB
    tickets = await db.get_research_tickets()
    assert len(tickets) == 1
    assert tickets[0].failure_pattern == "asynchronous loop deadlock"

    # 2. Research controller ingests and prioritizes tickets
    ingested_tickets = await researcher.ingest_and_prioritize_tickets()
    assert len(ingested_tickets) == 1
    assert ingested_tickets[0].ticket_id.startswith("RT-")

    # Compile dataset & launch container experiment
    dataset_path = await researcher.compile_training_dataset(ingested_tickets[0])
    trial_cfg = TrialConfig(
        trial_id="async-upgrade-v1",
        base_model_path="models/base",
        training_script_path="train.py",
        dataset_path=dataset_path
    )
    trial_res = await researcher.launch_sandbox_experiment(trial_cfg)
    assert trial_res.success is True

    # Promote model and publish CapabilityDelta
    delta = await researcher.promote_model_and_publish_delta(trial_res, ingested_tickets[0])
    assert delta.model_version == "Apodex-model-async-upgrade-v1"

    # 3. Harness loop consumes CapabilityDelta to update workflows
    await harness.apply_capability_delta(delta)
    assert "async-upgrade-v1" in harness.active_scaffolding["routing_logic_override"]


@pytest.mark.asyncio
async def test_verifier_layer_components():
    # 1. LLM-as-a-Judge Evaluation and Pairwise testing
    judge = LLMAsAJudgeNode()
    score = await judge.evaluate_response("What is 2+2?", "4")
    assert score.rating == 0.95
    assert "<thinking>" in score.thinking_trajectory
    assert "JSON" in score.verdict

    winner = await judge.pairwise_rank("Option A", "Option B")
    assert winner == "B"

    # 2. Introspective Critic (CRITIC / RISE style)
    critic = SelfCritiqueCritic()
    report = await critic.generate_tool_critique("some code", "SyntaxError: invalid syntax")
    assert report.needs_revision is True
    assert "syntax error" in report.critique_text
    assert len(report.tool_outcomes) == 1

    report_ok = await critic.generate_tool_critique("some code", "Successfully compiled.")
    assert report_ok.needs_revision is False

    # 3. Dense Reward Model step-level computation
    rm = DenseRewardModel()
    step_rewards = rm.calculate_trajectory_rewards([{"action": "search"}, {"action": "parse"}, {"action": "compile"}])
    assert len(step_rewards) == 3
    assert step_rewards[0] == 0.1
    assert step_rewards[1] == 0.2

    # 4. Grounded Fact-Checking verification
    checker = GroundedFactChecker()
    ground_ok = await checker.verify_claims("Claim: system runs on python.", ["Source: python is verified."])
    assert ground_ok.is_grounded is True

    ground_hallucinated = await checker.verify_claims("Claim: unverified hallucination is true.", ["Source: python runs."])
    assert ground_hallucinated.is_grounded is False
    assert len(ground_hallucinated.hallucinated_claims) == 1
    assert ground_hallucinated.confidence_score == 0.4

    # 5. Runtime Agent Verifier with temporal logic rules
    verifier = RuntimeAgentVerifier()
    # Correct sequence: verification occurs before deploy
    assert verifier.verify_temporal_logic(["Plan: verify then deploy"], ["verify", "deploy"]) is True
    # Violation sequence: deploy occurs but verify is missing from execution
    assert verifier.verify_temporal_logic(["Plan: verify then deploy"], ["deploy"]) is False
