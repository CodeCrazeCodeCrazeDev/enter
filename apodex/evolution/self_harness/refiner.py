"""
HarnessRefiner
Proposes harness changes (prompts, retry limits, thresholds) based on:
- Weakness mining (Self-Harness pattern).
- Context compression & prompt tuning (Lilian Weng's patterns like ACE, Meta-Harness, EVOLVE-BLOCKs, and Pareto frontiers).
- Archetypal clamp-12k (PR #1) diffs.
"""

from __future__ import annotations

import difflib
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field

from apodex.evolution.self_harness.trajectory_areal import AgentTrajectory, EvolutionControlPlane


class HarnessProposal(BaseModel):
    """A bounded proposal detailing specific harness code or prompt mutations."""
    proposal_id: str
    target_parameter: str
    old_value: Any
    new_value: Any
    citation_reference: str = "Self-Harness (Shanghai AI Lab, June 2026)"
    diff_preview: str = ""
    rationale: str = ""


class HarnessRefiner:
    """
    Analyzes historical trajectories to isolate failures, dithering, or missing memories,
    and constructs a targeted improvement proposal on the Pareto frontier.
    """

    def __init__(self, control_plane: EvolutionControlPlane) -> None:
        self.control_plane = control_plane

    def mine_weaknesses(self, trajectories: List[AgentTrajectory]) -> List[Dict[str, Any]]:
        """
        Scans trace steps to find exact bottlenecks:
        - stuck points (turns > 8, or long durations)
        - tool failures
        - prompt errors
        - missing memories
        - time wasted (inefficient looping)
        """
        weaknesses = []
        for traj in trajectories:
            failures = traj.get_failures()
            for f in failures:
                weaknesses.append({
                    "task_id": traj.task_id,
                    "type": "tool_failure" if f.get("is_error") else "stuck_or_slow",
                    "details": f
                })
            # Check for excessive turns / dither loop (Time wasted)
            if len(traj.steps) > 8:
                weaknesses.append({
                    "task_id": traj.task_id,
                    "type": "time_wasted",
                    "details": {"steps_count": len(traj.steps), "message": "Excessive step execution loop detected."}
                })
        return weaknesses

    def propose_refinement(self, trajectories: List[AgentTrajectory]) -> Optional[HarnessProposal]:
        """
        Generates a bounded improvement proposal (e.g., prompt tuning, retry limits, context compression).
        Refers to Lilian Weng's EVOLVE-BLOCKs and the PR #1 clamp-12k diff as standard.
        """
        weaknesses = self.mine_weaknesses(trajectories)
        if not weaknesses:
            return None

        # Determine best type of optimization based on weaknesses
        primary_issue_type = weaknesses[0]["type"]

        if primary_issue_type == "tool_failure":
            # Propose increasing max_llm_retries or adjusting retry rules
            old_val = self.control_plane.global_parameters.get("max_llm_retries", 5)
            new_val = old_val + 3
            rationale = "Tool failure detected. Elevating retry rules & limits to ensure robust recovery."
            return HarnessProposal(
                proposal_id="prop_retry_tuning",
                target_parameter="max_llm_retries",
                old_value=old_val,
                new_value=new_val,
                diff_preview=f"- max_llm_retries = {old_val}\n+ max_llm_retries = {new_val}",
                rationale=rationale
            )
        elif primary_issue_type == "time_wasted":
            # Propose clamping threshold optimization (PR #1 clamp-12k style)
            old_val = self.control_plane.global_parameters.get("clamping_threshold", 12000)
            new_val = 8000  # clamp more aggressively
            rationale = "Time wasted in long contexts. Optimizing context compression and clamping threshold to 8k to fit Pareto frontier."
            return HarnessProposal(
                proposal_id="prop_clamp_12k",
                target_parameter="clamping_threshold",
                old_value=old_val,
                new_value=new_val,
                diff_preview=f"- clamping_threshold = {old_val}\n+ clamping_threshold = {new_val}",
                rationale=rationale
            )
        else:
            # Propose prompt prefix refinement (ACE/Meta-Harness style)
            old_val = self.control_plane.global_parameters.get("system_prompt_prefix", "")
            new_val = old_val + " Break down tasks carefully and verify intermediate tool results."
            rationale = "Agent got stuck. Appending structured meta-cognition block instructions."
            return HarnessProposal(
                proposal_id="prop_prompt_tuning",
                target_parameter="system_prompt_prefix",
                old_value=old_val,
                new_value=new_val,
                diff_preview=f"- prefix = {old_val}\n+ prefix = {new_val}",
                rationale=rationale
            )
