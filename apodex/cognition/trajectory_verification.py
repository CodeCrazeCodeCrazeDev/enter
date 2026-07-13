from __future__ import annotations
from typing import Dict, Any, List


class TwoLevelCreditAssignment:
    """Computes credit assignment scores globally across trajectories and locally across execution steps."""

    def assign_credit(self, trajectory: Dict[str, Any], is_success: bool) -> Dict[str, Any]:
        steps = trajectory.get("steps", [])
        num_steps = len(steps)

        if is_success:
            trajectory_credit = 1.0
            base_multiplier = 1.0
        else:
            trajectory_credit = -0.5
            base_multiplier = -0.2

        # Credit distribution heuristic: allocate credit weights progressively to focus on decisive steps
        step_credits = []
        for i, step in enumerate(steps):
            progress_ratio = (i + 1) / num_steps if num_steps > 0 else 1.0
            step_credits.append({
                "step": step.get("step", i + 1),
                "action": step.get("action"),
                "credit": base_multiplier * progress_ratio
            })

        trajectory["trajectory_credit"] = trajectory_credit
        trajectory["step_credits"] = step_credits
        return trajectory


class MultiDimensionalTrajectoryVerifier:
    """Validates trajectories across syntactic quality, duplicate actions, and step efficiency (E10)."""

    def verify_trajectory(self, messages: List[Dict[str, Any]]) -> Dict[str, Any]:
        # Check mismatched brackets/parentheses across all assistant messages
        stack = []
        mapping = {")": "(", "}": "{", "]": "["}
        syntax_valid = True

        assistant_contents = []
        for msg in messages:
            if msg.get("role") == "assistant":
                content = msg.get("content", "")
                assistant_contents.append(content)
                for char in content:
                    if char in mapping.values():
                        stack.append(char)
                    elif char in mapping.keys():
                        if not stack or stack[-1] != mapping[char]:
                            syntax_valid = False
                            break
                        stack.pop()

        if stack:
            syntax_valid = False

        syntax_score = 1.0 if syntax_valid else 0.4

        # Check for duplicate assistant consecutive output turns
        duplicates = 0
        for i in range(len(assistant_contents) - 1):
            if assistant_contents[i] == assistant_contents[i + 1]:
                duplicates += 1

        efficiency_score = 1.0 - (duplicates * 0.3)
        efficiency_score = max(efficiency_score, 0.1)

        is_high_quality = syntax_valid and duplicates == 0

        return {
            "is_high_quality": is_high_quality,
            "syntax_score": syntax_score,
            "efficiency_score": efficiency_score,
            "details": {
                "mismatched_brackets": not syntax_valid,
                "consecutive_duplicates": duplicates
            }
        }
