"""
Self-Harness End-to-End Integration Test Suite.
Simulates:
1. Agent run getting stuck or hitting a tool failure.
2. HarnessObserver capturing step-level traces.
3. HarnessRefiner proposing a self-improvement config patch (clamp-12k / retry limit tuning).
4. HarnessCritic verifying security, utility, and objective alignment.
5. SandboxValidator performing static offline and online task simulation verification.
6. SelectiveRollout canary-deploying to production.
7. RollbackManager reverting the parameter change upon simulated latency SLA spikes.
"""

from __future__ import annotations

import pytest
from uuid import uuid4

# Import AgentHarness structures
from agent_harness.core.loop_types import LoopConfig, TurnContext, ToolResult, AgentLoopResult
from agent_harness.components.harness_observer import HarnessObserver
from agent_harness.components.selective_rollout import SelectiveRollout
from agent_harness.components.rollback_manager import RollbackManager

# Import generic self-improvement logic
from apodex.evolution.self_harness.trajectory_areal import AReaLDataProxy, EvolutionControlPlane
from apodex.evolution.self_harness.refiner import HarnessRefiner
from apodex.evolution.self_harness.critic import HarnessCritic
from apodex.evolution.self_harness.validator import SandboxValidator

# Import baseline evolution changelog models
from apodex.evolution.common.models import EvolutionChangelog, ConfigDelta, ChangelogEntry, CostMode


@pytest.mark.asyncio
async def test_self_harness_self_improvement_loop():
    # -------------------------------------------------------------
    # 1. Setup the Self-Improvement System
    # -------------------------------------------------------------
    data_proxy = AReaLDataProxy()
    control_plane = EvolutionControlPlane(data_proxy=data_proxy)
    refiner = HarnessRefiner(control_plane=control_plane)
    critic = HarnessCritic()
    validator = SandboxValidator()
    changelog = EvolutionChangelog()

    # -------------------------------------------------------------
    # 2. Simulate Agent Run with Failures tracked by HarnessObserver
    # -------------------------------------------------------------
    tenant_id = "tenant_test_harness"
    observer = HarnessObserver(data_proxy=data_proxy, tenant_id=tenant_id)

    # Simulated start of loop
    config = LoopConfig(task_id="task_101", role_id="agent_coder")
    await observer.on_loop_start(config)

    # Simulated tool execution steps with errors (representing a stuck/failed tool call)
    ctx_step_1 = TurnContext(
        turn=1, max_turns=10, task_id="task_101", role_id="agent_coder",
        ai_text="Executing code executor tool.", thinking="Need to compile.",
        tool_calls=[{"name": "code_executor", "args": {"code": "print(1)"}}],
        messages=[], usage=None, metadata={}
    )
    tool_res_1 = ToolResult(
        name="code_executor", args={"code": "print(1)"},
        result="Traceback (most recent call): error in library compilation.",
        duration_ms=12000, tool_call_id="tc_1", is_error=True
    )
    await observer.on_tool_result(ctx_step_1, tool_res_1)

    # Simulated prompt error step
    ctx_step_2 = TurnContext(
        turn=2, max_turns=10, task_id="task_101", role_id="agent_coder",
        ai_text="System error context overflow.", thinking="",
        tool_calls=[], messages=[], usage=None, metadata={}
    )
    await observer.on_turn_end(ctx_step_2)

    # Simulated loop end
    loop_res = AgentLoopResult(messages=[], final_content="Failed.", turns_used=2, stopped_by="error")
    await observer.on_loop_end(loop_res)

    # Verify trajectory successfully logged
    buffered = data_proxy.get_trajectories(tenant_id)
    assert len(buffered) == 1
    trajectory = buffered[0]
    assert len(trajectory.steps) == 2
    assert trajectory.get_failures()[0]["tool_name"] == "code_executor"

    # -------------------------------------------------------------
    # 3. Weakness Mining & Refinement Proposals (Self-Harness Template)
    # -------------------------------------------------------------
    weaknesses = refiner.mine_weaknesses(buffered)
    assert len(weaknesses) >= 1
    assert any(w["type"] == "tool_failure" for w in weaknesses)

    proposal = refiner.propose_refinement(buffered)
    assert proposal is not None
    assert proposal.target_parameter == "max_llm_retries"
    assert proposal.new_value == 8

    # -------------------------------------------------------------
    # 4. HarnessCritic & SandboxValidator Verification (Gemma / PR #1 Style)
    # -------------------------------------------------------------
    audit = critic.check_alignment(proposal)
    assert audit.is_safe is True
    assert audit.is_aligned is True

    val_report = validator.validate_proposal(proposal, past_tasks=[])
    assert val_report.passed_offline_tests is True
    assert val_report.is_positive_yield is True
    assert val_report.improved_score > val_report.baseline_score

    # -------------------------------------------------------------
    # 5. Selective Rollout Canary Deployment
    # -------------------------------------------------------------
    rollout_mgr = SelectiveRollout(changelog=changelog)
    variant = rollout_mgr.deploy_canary(
        variant_id="var-max-llm-retries-v1",
        target_parameter=proposal.target_parameter,
        value=proposal.new_value,
        traffic_percentage=20.0
    )
    assert variant.variant_id == "var-max-llm-retries-v1"
    assert changelog.current_config["max_llm_retries"] == 8

    # -------------------------------------------------------------
    # 6. Observability and Automatic Rollback Manager Verification
    # -------------------------------------------------------------
    rollback_mon = RollbackManager(changelog=changelog, rollout_manager=rollout_mgr)

    # Record healthy metric (SLA satisfies limits)
    did_rollback_ok = rollback_mon.record_metrics_and_check_rollback(variant, latency=2.5, score=0.85)
    assert did_rollback_ok is False
    assert changelog.current_config["max_llm_retries"] == 8

    # Record SLA regression metric (Latency is 9.0s which breaches SLA > 5.0s)
    did_rollback_fail = rollback_mon.record_metrics_and_check_rollback(variant, latency=9.0, score=0.4)
    assert did_rollback_fail is True  # Rollback triggered!

    # Verify changelog reverted parameter back to default
    assert "max_llm_retries" not in changelog.current_config or changelog.current_config["max_llm_retries"] == 5
