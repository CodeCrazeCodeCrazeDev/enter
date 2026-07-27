"""Unit tests for Phase 7 Institutional Evolution System (IES) and agent management."""

import pytest
from apodex.ai_eos.governance.gateway import GovernanceGateway


def test_ies_agent_lifecycle_management():
    """Verify that agents can be spawned and retired under complexity constraints."""
    ies = GovernanceGateway()

    # Initial roster has 29 default agents
    assert len(ies.agent_registry) == 29

    # Spawn new econometrics agent
    res = ies.manage_agent_lifecycle(action="SPAWN", agent_id="agent_pricing_econometrics")
    assert res == "SPAWNED"
    assert "agent_pricing_econometrics" in ies.agent_registry

    # Try to spawn exceeding complexity limit
    ies.complexity_budget_limit = 5
    res_blocked = ies.manage_agent_lifecycle(action="SPAWN", agent_id="agent_redundant")
    assert res_blocked == "SPAWN_BLOCKED"

    # Retire agent
    res_retire = ies.manage_agent_lifecycle(action="RETIRE", agent_id="agent_pricing_econometrics")
    assert res_retire == "RETIRED"
    assert "agent_pricing_econometrics" not in ies.agent_registry


def test_ies_institutional_decision_calibration():
    """Verify recording of strategic decisions and calibration error bias tracing."""
    ies = GovernanceGateway()

    # Record decision with 80% confidence, realized accuracy was 85% (+5% positive bias)
    record = ies.record_institutional_decision(
        decision_id="dec_GTM_launch",
        reasoning="Top banner tested with high CTR",
        confidence=0.80,
        actual_accuracy=0.85
    )

    assert record["decision_id"] == "dec_GTM_launch"
    assert record["bias"] == pytest.approx(0.05)
    assert len(ies.decision_record_ledger) == 1
