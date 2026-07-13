from __future__ import annotations
import time
from typing import Any, Dict, List, Optional
from uuid import UUID, uuid4
from pydantic import BaseModel, Field

from apodex.evolution.common.models import CostMode, MultiObjectiveMetric, calculate_multiobjective_score
from apodex.evolution.verifier.judge import EvolutionVerifier, EvaluationReport
from apodex.safety.core import ImmutableSafetyCore, RiskTier


class RevisionRound(BaseModel):
    """Holds results of a single revision round inside the session."""
    round_id: UUID = Field(default_factory=uuid4)
    output: str
    critique: str
    verifier_score: float
    safety_allowed: bool
    token_cost: float
    latency_ms: float


class RevisionSession(BaseModel):
    """Encapsulates a multi-round recursive self-improvement session."""
    session_id: UUID = Field(default_factory=uuid4)
    task_id: UUID
    initial_output: str
    final_output: Optional[str] = None
    rounds: List[RevisionRound] = Field(default_factory=list)
    stop_reason: Optional[str] = None


class RevisionSessionManager:
    """
    Manages multi-round critique-revise-verify loops under cost budgets and safety constraints.
    """

    def __init__(
        self,
        verifier: Optional[EvolutionVerifier] = None,
        safety_core: Optional[ImmutableSafetyCore] = None
    ) -> None:
        self.verifier = verifier or EvolutionVerifier()
        self.safety_core = safety_core or ImmutableSafetyCore()

    async def run_improvement_session(
        self,
        task_id: UUID,
        tenant_id: str,
        user_id: str,
        prompt: str,
        initial_output: str,
        cost_mode: CostMode,
        target_id: str,
        mock_rounds_content: Optional[List[str]] = None
    ) -> RevisionSession:
        """
        Runs the recursive self-improvement session loop:
        - Evaluates initial output.
        - Sequentially runs critique-revise-verify rounds.
        - Applies stopping criteria: plateau, degradation, budget limits, or safety core block.
        """
        session = RevisionSession(task_id=task_id, initial_output=initial_output)

        # 1. Establish initial score
        initial_rep = await self.verifier.evaluate_output(prompt, initial_output)
        initial_score = calculate_multiobjective_score(initial_rep.metrics, cost_mode)

        # Set cost-mode-aware round limits
        if cost_mode == CostMode.FAST_CHEAP:
            max_rounds = 1
        elif cost_mode == CostMode.BALANCED:
            max_rounds = 2
        else:  # MAX_QUALITY
            max_rounds = 4

        current_output = initial_output
        prev_score = initial_score

        # Loop for revision rounds
        for r in range(max_rounds):
            # Check safety core first before continuing with revision
            safety_eval = self.safety_core.evaluate_change_proposal(
                tenant_id=tenant_id,
                user_id=user_id,
                target_id=target_id,
                delta_type="prompt_revision",
                details={"round": r, "current_output_len": len(current_output)}
            )

            if not safety_eval["allowed"]:
                session.stop_reason = f"BLOCKED_BY_SAFETY_CORE: {safety_eval['risk_tier']}"
                break

            # Critique generation
            critique = f"Format improvement suggestions for round {r+1}."

            # Revision generation
            if mock_rounds_content and r < len(mock_rounds_content):
                revised_text = mock_rounds_content[r]
            else:
                # Fallback simple revision simulating incremental improvements
                revised_text = f"{{\n  \"content\": \"{current_output}\",\n  \"round\": {r+1}\n}}"

            # Verifier evaluation
            rep = await self.verifier.evaluate_output(prompt, revised_text)
            mo_score = calculate_multiobjective_score(rep.metrics, cost_mode)

            # Record round
            round_record = RevisionRound(
                output=revised_text,
                critique=critique,
                verifier_score=mo_score,
                safety_allowed=True,
                token_cost=rep.metrics.cost,
                latency_ms=rep.metrics.latency * 1000.0
            )
            session.rounds.append(round_record)

            # Check stopping conditions:
            # 1. Degradation check
            if mo_score < prev_score:
                session.stop_reason = "DEGRADATION"
                break

            # 2. Plateau check (improvement < 0.01)
            if (mo_score - prev_score) < 0.01:
                session.stop_reason = "PLATEAU"
                current_output = revised_text
                break

            # Accept revision and proceed
            current_output = revised_text
            prev_score = mo_score

        if not session.stop_reason:
            session.stop_reason = "BUDGET_LIMIT_REACHED"

        session.final_output = current_output
        return session
