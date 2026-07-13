from __future__ import annotations
import uuid
import pytest

from apodex.memory.models import PersonalEvolutionProfile, AtomicMemory, ScenarioPattern
from apodex.memory.services import TencentDBMemoryStore
from apodex.evolution.common.models import EvolutionChangelog, ConfigDelta, ChangelogEntry, CostMode
from apodex.evolution.production.orchestrator import SandboxSubstrateManager, ProductionOrchestrator
from apodex.evolution.production.compliance import CrossTenantLearningEngine
from apodex.evolution.production.rollout import ProductionRolloutManager, EvolutionObservabilityMonitor


@pytest.mark.asyncio
async def test_production_orchestration_and_pep():
    """
    Verifies production-scale cost-aware orchestrations and PEP adaptation:
    - Loading T4 PEP (Personal Evolution Profile) constraints.
    - Dynamically recruiting specialized sub-agents.
    - Capturing SLA stats.
    """
    sb_mgr = SandboxSubstrateManager()
    orch = ProductionOrchestrator(sandbox_manager=sb_mgr)

    tenant_id = "tenant_scale_9"
    task_id = uuid.uuid4()

    # Setup PEP Profile (FAST_CHEAP)
    pep_fc = PersonalEvolutionProfile(tenant_id=tenant_id, user_id="user_fc")
    pep_fc.cost_budget_preferences["default_mode"] = "fast_cheap"
    pep_fc.style_preferences["verbosity"] = "concise"

    res_fc = await orch.execute_task_at_scale(tenant_id, pep_fc, task_id, "Analyze parser.")
    assert "Concise summary" in res_fc["response"]
    assert res_fc["stats"]["subagents_recruited"] == 1
    assert res_fc["stats"]["cost_mode"] == "fast_cheap"

    # Setup PEP Profile (MAX_QUALITY)
    pep_mq = PersonalEvolutionProfile(tenant_id=tenant_id, user_id="user_mq")
    pep_mq.cost_budget_preferences["default_mode"] = "max_quality"
    pep_mq.style_preferences["verbosity"] = "verbose"

    res_mq = await orch.execute_task_at_scale(tenant_id, pep_mq, task_id, "Exhaustive analyze.")
    assert "Exhaustive architectural summary" in res_mq["response"]
    assert res_mq["stats"]["subagents_recruited"] >= 4
    assert res_mq["stats"]["cost_mode"] == "max_quality"


def test_sandbox_substrate_snapshotting():
    """
    Verifies SandboxSubstrateManager container allocation, resource limits,
    and checkpoint snapshot/restores.
    """
    sb_mgr = SandboxSubstrateManager()
    tenant_id = "tenant_snapshot_4"

    sb = sb_mgr.allocate_sandbox(tenant_id, quota_multiplier=2.0)
    assert sb.resource_quota["cpu_cores"] == 4
    assert sb.resource_quota["memory_mb"] == 8192

    # Snapshotting sandbox state
    state = {"cursor": "step_500", "node_id": "node_9a"}
    snap_id = sb_mgr.create_snapshot(sb.sandbox_id, state)

    assert "snap_" in snap_id
    assert sb.snapshot_count == 1

    # Restoring sandbox state
    restored = sb_mgr.restore_snapshot(sb.sandbox_id)
    assert restored is not None
    assert restored["state_data"]["cursor"] == "step_500"


def test_cross_tenant_learning_compliance():
    """
    Verifies that CrossTenantLearningEngine enforces opt-in consent and
    cleanly anonymizes and distills shared atoms and scenarios.
    """
    engine = CrossTenantLearningEngine()

    tenant_opt_in = "tenant_consented"
    tenant_opt_out = "tenant_restricted"

    engine.set_tenant_consent(tenant_opt_in, opted_in=True)
    engine.set_tenant_consent(tenant_opt_out, opted_in=False)

    # Distill T2 Atom (Opt-In tenant)
    atom_ok = AtomicMemory(
        tenant_id=tenant_opt_in,
        user_id="user_123",
        content="Confidential transaction processed successfully for org_consented.",
        embedding=[0.05] * 1536
    )
    distilled_ok = engine.anonymize_and_distill_atom(atom_ok)
    assert distilled_ok is not None
    assert distilled_ok.user_id == "anonymous"
    assert distilled_ok.tenant_id == "global_shared"
    # Content must have private terms anonymized
    assert "[ANONYMIZED]" in distilled_ok.content

    # Distill T2 Atom (Opt-Out tenant) -> Blocked/Nullified
    atom_no = AtomicMemory(
        tenant_id=tenant_opt_out,
        user_id="user_123",
        content="Private keys exposed in config file.",
        embedding=[0.05] * 1536
    )
    distilled_no = engine.anonymize_and_distill_atom(atom_no)
    assert distilled_no is None


@pytest.mark.asyncio
async def test_staged_rollout_and_auto_rollback():
    """
    Verifies production rollout manager A/B testing routing, staged scaling,
    and automatic incident rollback on SLA metric regressions.
    """
    changelog = EvolutionChangelog()
    rollout_mgr = ProductionRolloutManager(changelog=changelog)

    # 1. Apply a configuration change to the changelog
    delta = ConfigDelta(target_id="routing_threshold", delta_type="workflow", old_value=0.5, new_value=0.9)
    entry = ChangelogEntry(
        entry_id="e1", timestamp=123.0, cost_mode=CostMode.BALANCED,
        applied_deltas=[delta], verifier_score_before=0.5, verifier_score_after=0.8,
        description="Optimize threshold"
    )
    changelog.apply_change(entry)
    assert changelog.current_config["routing_threshold"] == 0.9

    # 2. Register new variant in rollout manager
    variant = rollout_mgr.register_variant("v2.1.0-variant", "harness_workflow", initial_traffic=50.0)

    # 3. Simulate healthy production metrics (SLA OK)
    ok_metrics = rollout_mgr.monitor.record_sla_metrics(variant, latency=2.1, score=0.8)
    assert ok_metrics is True

    # 4. Simulate a critical SLA breach (e.g. timeout spike)
    regression_detected = rollout_mgr.monitor.record_sla_metrics(variant, latency=9.5, score=0.4)
    assert regression_detected is False

    # 5. Trigger automated rollback
    rolled_back = rollout_mgr.trigger_incident_rollback(variant.variant_id)
    assert rolled_back is True
    # Verify changelog rolled back routing_threshold to v1 state
    assert changelog.current_config["routing_threshold"] == 0.5
