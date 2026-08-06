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
from apodex.memory.semantic_memory import SemanticMemory
from apodex.memory.emg_engine import EMGEngine


class HarnessProposal(BaseModel):
    """A bounded proposal detailing specific harness code or prompt mutations."""
    proposal_id: str
    target_parameter: str
    old_value: Any
    new_value: Any
    citation_reference: str = "Self-Harness (Shanghai AI Lab, June 2026)"
    diff_preview: str = ""
    rationale: str = ""
    graph_edit_steps: List[str] = Field(default_factory=list)


class HarnessRefiner:
    """
    Analyzes historical trajectories to isolate failures, dithering, or missing memories,
    and constructs a targeted improvement proposal on the Pareto frontier.
    """

    def __init__(self, control_plane: EvolutionControlPlane, semantic_memory: Optional[SemanticMemory] = None) -> None:
        self.control_plane = control_plane
        self.semantic_memory = semantic_memory

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

        primary_issue_type = weaknesses[0]["type"]

        # Build EMG ActionDecisionGraphs to extract graph-edit paths if multiple trajectories exist
        graph_edit_steps: List[str] = []
        if len(trajectories) >= 2:
            failed_traj = next((t for t in trajectories if any(f.get("is_error") or "error" in f.get("tool_result_preview", "").lower() for f in t.steps)), None)
            ref_traj = next((t for t in trajectories if t != failed_traj), None)

            if failed_traj and ref_traj:
                failed_graph = EMGEngine.build_graph_from_trajectory(failed_traj.task_id, failed_traj.steps)
                ref_graph = EMGEngine.build_graph_from_trajectory(ref_traj.task_id, ref_traj.steps)

                edit_ops = EMGEngine.compute_graph_edit_path(failed_graph, ref_graph)
                for op in edit_ops:
                    graph_edit_steps.append(f"{op.op_type} (node_type={op.node_type}, action={op.action}): {op.rationale}")

        # Retrieve matching historical context if MemoHarness is integrated
        memo_context = ""
        if self.semantic_memory and len(weaknesses) > 0:
            query_topic = weaknesses[0]["details"].get("tool_name", "general failure")
            past_evidence = self.semantic_memory.retrieve_similar_evidence(query_topic, limit=2)
            if past_evidence:
                memo_context = " | Historical Success Match: " + " & ".join([e.content for e in past_evidence])

        if primary_issue_type == "tool_failure":
            old_val = self.control_plane.global_parameters.get("max_llm_retries", 5)
            new_val = old_val + 3
            rationale = f"Tool failure detected. Elevating retry rules & limits to ensure robust recovery.{memo_context}"
            return HarnessProposal(
                proposal_id="prop_retry_tuning",
                target_parameter="max_llm_retries",
                old_value=old_val,
                new_value=new_val,
                diff_preview=f"- max_llm_retries = {old_val}\n+ max_llm_retries = {new_val}",
                rationale=rationale,
                graph_edit_steps=graph_edit_steps
            )
        elif primary_issue_type == "time_wasted":
            old_val = self.control_plane.global_parameters.get("clamping_threshold", 12000)
            new_val = 8000  # clamp more aggressively
            rationale = f"Time wasted in long contexts. Optimizing context compression and clamping threshold to 8k to fit Pareto frontier.{memo_context}"
            return HarnessProposal(
                proposal_id="prop_clamp_12k",
                target_parameter="clamping_threshold",
                old_value=old_val,
                new_value=new_val,
                diff_preview=f"- clamping_threshold = {old_val}\n+ clamping_threshold = {new_val}",
                rationale=rationale,
                graph_edit_steps=graph_edit_steps
            )
        else:
            old_val = self.control_plane.global_parameters.get("system_prompt_prefix", "")
            new_val = old_val + " Break down tasks carefully and verify intermediate tool results."
            rationale = f"Agent got stuck. Appending structured meta-cognition block instructions.{memo_context}"
            return HarnessProposal(
                proposal_id="prop_prompt_tuning",
                target_parameter="system_prompt_prefix",
                old_value=old_val,
                new_value=new_val,
                diff_preview=f"- prefix = {old_val}\n+ prefix = {new_val}",
                rationale=rationale,
                graph_edit_steps=graph_edit_steps
            )
