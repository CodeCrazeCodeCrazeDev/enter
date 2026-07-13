from __future__ import annotations
import pytest
from apodex.safety.core import ImmutableSafetyCore, RiskTier


def test_safety_core_policy_blocking():
    """
    Verifies that ImmutableSafetyCore PolicyEngine successfully identifies and blocks
    restricted modifications (e.g. self-edits to safety/security targets).
    """
    safety = ImmutableSafetyCore()

    # 1. Allowed low risk change
    eval_ok = safety.evaluate_change_proposal(
        tenant_id="tenant_123",
        user_id="user_abc",
        target_id="system_prompt_v1",
        delta_type="prompt",
        details={}
    )
    assert eval_ok["allowed"] is True
    assert eval_ok["risk_tier"] == RiskTier.TIER_1_LOW
    assert eval_ok["action_required"] == "PROPOSAL_EVALUATED_LOW"

    # 2. Blocked modification (touching restricted safety core config)
    eval_blocked = safety.evaluate_change_proposal(
        tenant_id="tenant_123",
        user_id="user_abc",
        target_id="safety_core_rules",
        delta_type="code_modification",
        details={}
    )
    assert eval_blocked["allowed"] is False
    assert eval_blocked["risk_tier"] == RiskTier.TIER_3_HIGH
    assert eval_blocked["action_required"] == "BLOCKED"

    # Verify immutable audit ledger has logged both events
    assert len(safety.audit_ledger) == 2
    assert safety.audit_ledger[0].action == "PROPOSAL_EVALUATED_LOW"
    assert safety.audit_ledger[1].action == "BLOCKED"


def test_risk_classification_mapping():
    """
    Verifies that RiskClassifier maps proposed changes correctly to appropriate Risk Tiers.
    """
    safety = ImmutableSafetyCore()
    classifier = safety.risk_classifier

    # Tier 1 - Wording modifications
    assert classifier.classify_proposal("system_prompt_intro", "prompt") == RiskTier.TIER_1_LOW

    # Tier 2 - Workflow / tool alterations
    assert classifier.classify_proposal("main_workflow_graph", "workflow") == RiskTier.TIER_2_MEDIUM
    assert classifier.classify_proposal("web_search_routing", "tool_routing") == RiskTier.TIER_2_MEDIUM

    # Tier 3 - Security / model upgrades
    assert classifier.classify_proposal("reasoning_model_select", "model_swap") == RiskTier.TIER_3_HIGH
    assert classifier.classify_proposal("immutable_safety_policies", "schema_update") == RiskTier.TIER_3_HIGH
