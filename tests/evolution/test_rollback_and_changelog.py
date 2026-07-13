from __future__ import annotations
import time
from apodex.evolution.common.models import (
    CostMode,
    ConfigDelta,
    ChangelogEntry,
    EvolutionChangelog,
)


def test_changelog_and_rollback_flow():
    """
    Verifies that configurations applied as deltas are tracked correctly in the history
    and can be rolled back to their original state in LIFO order.
    """
    changelog = EvolutionChangelog(current_config={"system_prompt": "initial prompt v1", "threshold": 0.5})

    # Delta 1: update system_prompt
    delta_1 = ConfigDelta(
        target_id="system_prompt",
        delta_type="prompt",
        old_value="initial prompt v1",
        new_value="optimized prompt v2"
    )
    entry_1 = ChangelogEntry(
        entry_id="e1",
        timestamp=time.time(),
        cost_mode=CostMode.BALANCED,
        applied_deltas=[delta_1],
        verifier_score_before=0.5,
        verifier_score_after=0.7,
        description="First optimization step."
    )

    changelog.apply_change(entry_1)
    assert changelog.current_config["system_prompt"] == "optimized prompt v2"
    assert changelog.current_config["threshold"] == 0.5
    assert len(changelog.history) == 1

    # Delta 2: update threshold and system_prompt together
    delta_2a = ConfigDelta(
        target_id="system_prompt",
        delta_type="prompt",
        old_value="optimized prompt v2",
        new_value="perfect prompt v3"
    )
    delta_2b = ConfigDelta(
        target_id="threshold",
        delta_type="workflow",
        old_value=0.5,
        new_value=0.8
    )
    entry_2 = ChangelogEntry(
        entry_id="e2",
        timestamp=time.time(),
        cost_mode=CostMode.MAX_QUALITY,
        applied_deltas=[delta_2a, delta_2b],
        verifier_score_before=0.7,
        verifier_score_after=0.9,
        description="Second optimization step."
    )

    changelog.apply_change(entry_2)
    assert changelog.current_config["system_prompt"] == "perfect prompt v3"
    assert changelog.current_config["threshold"] == 0.8
    assert len(changelog.history) == 2

    # Rollback 1: should revert Delta 2
    popped_1 = changelog.rollback_last_change()
    assert popped_1 is not None
    assert popped_1.entry_id == "e2"
    assert changelog.current_config["system_prompt"] == "optimized prompt v2"
    assert changelog.current_config["threshold"] == 0.5
    assert len(changelog.history) == 1

    # Rollback 2: should revert Delta 1
    popped_2 = changelog.rollback_last_change()
    assert popped_2 is not None
    assert popped_2.entry_id == "e1"
    assert changelog.current_config["system_prompt"] == "initial prompt v1"
    assert changelog.current_config["threshold"] == 0.5
    assert len(changelog.history) == 0

    # Rollback 3: empty, should return None
    assert changelog.rollback_last_change() is None
