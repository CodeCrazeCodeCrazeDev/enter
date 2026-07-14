from __future__ import annotations

from apodex.cognition.trajectory_verification import (
    MultiDimensionalTrajectoryVerifier,
    TwoLevelCreditAssignment,
)


def test_assign_credit_success_distributes_positive_credit():
    trajectory = {"steps": [{"step": 1, "action": "a"}, {"step": 2, "action": "b"}]}
    result = TwoLevelCreditAssignment().assign_credit(trajectory, is_success=True)
    assert result["trajectory_credit"] == 1.0
    credits = [c["credit"] for c in result["step_credits"]]
    # progressive: 1.0 * 0.5, 1.0 * 1.0
    assert credits == [0.5, 1.0]


def test_assign_credit_failure_uses_negative_multiplier():
    trajectory = {"steps": [{"step": 1, "action": "a"}]}
    result = TwoLevelCreditAssignment().assign_credit(trajectory, is_success=False)
    assert result["trajectory_credit"] == -0.5
    assert result["step_credits"][0]["credit"] == -0.2


def test_assign_credit_empty_steps():
    trajectory = {"steps": []}
    result = TwoLevelCreditAssignment().assign_credit(trajectory, is_success=True)
    assert result["step_credits"] == []
    assert result["trajectory_credit"] == 1.0


def test_assign_credit_defaults_step_number_to_index():
    trajectory = {"steps": [{"action": "a"}, {"action": "b"}]}
    result = TwoLevelCreditAssignment().assign_credit(trajectory, is_success=True)
    assert [c["step"] for c in result["step_credits"]] == [1, 2]


def _msg(role, content):
    return {"role": role, "content": content}


def test_verify_trajectory_high_quality():
    messages = [
        _msg("assistant", "first (balanced) output"),
        _msg("assistant", "second distinct output"),
    ]
    result = MultiDimensionalTrajectoryVerifier().verify_trajectory(messages)
    assert result["is_high_quality"] is True
    assert result["syntax_score"] == 1.0
    assert result["efficiency_score"] == 1.0
    assert result["details"]["mismatched_brackets"] is False
    assert result["details"]["consecutive_duplicates"] == 0


def test_verify_trajectory_detects_bad_syntax():
    messages = [_msg("assistant", "unbalanced (bracket")]
    result = MultiDimensionalTrajectoryVerifier().verify_trajectory(messages)
    assert result["is_high_quality"] is False
    assert result["syntax_score"] == 0.4
    assert result["details"]["mismatched_brackets"] is True


def test_verify_trajectory_penalizes_consecutive_duplicates():
    messages = [
        _msg("assistant", "same"),
        _msg("assistant", "same"),
    ]
    result = MultiDimensionalTrajectoryVerifier().verify_trajectory(messages)
    assert result["details"]["consecutive_duplicates"] == 1
    assert abs(result["efficiency_score"] - 0.7) < 1e-9
    assert result["is_high_quality"] is False


def test_verify_trajectory_efficiency_floor():
    messages = [_msg("assistant", "x")] * 10
    result = MultiDimensionalTrajectoryVerifier().verify_trajectory(messages)
    assert result["efficiency_score"] == 0.1


def test_verify_trajectory_ignores_non_assistant_messages():
    messages = [_msg("user", "unbalanced ("), _msg("assistant", "clean")]
    result = MultiDimensionalTrajectoryVerifier().verify_trajectory(messages)
    assert result["is_high_quality"] is True
