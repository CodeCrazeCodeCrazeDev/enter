from __future__ import annotations
import pytest
from apodex.evolution.common.models import CostMode, ConfigDelta, EvolutionChangelog
from apodex.evolution.harness_loop.approval import ChangeProposal, SelfImprovementOrchestrator
from apodex.safety.core import ImmutableSafetyCore, RiskTier


@pytest.mark.asyncio
async def test_tiered_approval_workflow():
    """
    Verifies end-to-end ChangeProposal routing through Risk Tiers.
    """
    safety = ImmutableSafetyCore()
    changelog = EvolutionChangelog()
    orchestrator = SelfImprovementOrchestrator(safety_core=safety, changelog=changelog)

    tenant_id = "tenant_test"
    user_id = "user_test"

    # 1. Tier 1 Change (Low Risk auto-apply)
    delta_t1 = ConfigDelta(
        target_id="system_prompt_title",
        delta_type="prompt",
        old_value="v1",
        new_value="v1_optimized"
    )
    prop_t1 = ChangeProposal(tenant_id=tenant_id, user_id=user_id, delta=delta_t1)

    res_t1 = await orchestrator.process_change_proposal(prop_t1, CostMode.BALANCED)
    assert res_t1["status"] == "applied"
    assert res_t1["risk_tier"] == RiskTier.TIER_1_LOW
    assert len(changelog.history) == 1
    assert changelog.current_config["system_prompt_title"] == "v1_optimized"

    # 2. Tier 2 Change (Medium Risk sandbox testing)
    delta_t2 = ConfigDelta(
        target_id="agent_workflow_steps",
        delta_type="workflow",
        old_value="[react]",
        new_value="[react, verifier]"
    )
    prop_t2 = ChangeProposal(tenant_id=tenant_id, user_id=user_id, delta=delta_t2)

    # In CostMode.FAST_CHEAP -> simulated shadow test fails (rolled back)
    res_t2_fail = await orchestrator.process_change_proposal(prop_t2, CostMode.FAST_CHEAP)
    assert res_t2_fail["status"] == "rolled_back"
    assert "agent_workflow_steps" not in changelog.current_config

    # In CostMode.MAX_QUALITY -> simulated shadow test succeeds (promoted)
    res_t2_success = await orchestrator.process_change_proposal(prop_t2, CostMode.MAX_QUALITY)
    assert res_t2_success["status"] == "applied"
    assert changelog.current_config["agent_workflow_steps"] == "[react, verifier]"

    # 3. Tier 3 Change (High Risk staged manual approval)
    delta_t3 = ConfigDelta(
        target_id="llm_model_selection",
        delta_type="model_swap",
        old_value="gpt-4o-mini",
        new_value="claude-3-5-sonnet"
    )
    prop_t3 = ChangeProposal(tenant_id=tenant_id, user_id=user_id, delta=delta_t3)

    res_t3 = await orchestrator.process_change_proposal(prop_t3, CostMode.MAX_QUALITY)
    assert res_t3["status"] == "staged_for_approval"
    assert res_t3["risk_tier"] == RiskTier.TIER_3_HIGH
    assert prop_t3.proposal_id in orchestrator.staged_approvals

    # Manual human approval execution (Approved)
    res_app = orchestrator.execute_manual_approval(prop_t3.proposal_id, CostMode.MAX_QUALITY, approved=True)
    assert res_app["status"] == "applied"
    assert changelog.current_config["llm_model_selection"] == "claude-3-5-sonnet"
