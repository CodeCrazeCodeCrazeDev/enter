"""Constitutional governance + tiered autonomy for safe economic action.

Every economic action (spawning a cell, deploying capital, scaling a winner)
passes through the :class:`ConstitutionalFilter` before it executes. The filter
enforces hard invariants — capital-preservation limits, brand-safety checks and
per-engine autonomy tiers — and returns a structured verdict. This mirrors the
"Constitutional AI + tiered autonomy" design decision from the AEAN spec: no
engine acts unsupervised until it has earned independence through demonstrated
reliability.
"""
from __future__ import annotations

import logging
import re
from typing import List, Optional, Dict, Any

from pydantic import BaseModel, Field

from .models import EngineName, MicroCell

logger = logging.getLogger("aean.governance")


class ConstitutionalRules(BaseModel):
    """Invariant boundaries the organism may never cross."""

    # Capital preservation.
    max_single_allocation_pct: float = 0.35  # No cell may take >35% of treasury.
    min_treasury_reserve_pct: float = 0.10   # Always keep >=10% of capital as reserve.
    max_total_deployed_pct: float = 0.90     # Never deploy more than 90% of treasury at once.

    # Brand safety — narratives/assets containing these are rejected.
    banned_terms: List[str] = Field(
        default_factory=lambda: ["guaranteed returns", "get rich quick", "miracle cure", "risk-free"]
    )

    # Autonomy: engines earn unsupervised operation after a track record.
    min_decisions_for_autonomy: int = 25
    min_accuracy_for_autonomy: float = 0.90


class Verdict(BaseModel):
    approved: bool
    reasons: List[str] = Field(default_factory=list)


class EngineTrackRecord(BaseModel):
    engine: EngineName
    decisions: int = 0
    successes: int = 0

    @property
    def accuracy(self) -> float:
        return self.successes / self.decisions if self.decisions else 0.0


class SelectionAuditReport(BaseModel):
    approved: bool
    reasons: List[str] = Field(default_factory=list)
    fitness_convergence_detected: bool = False
    details: Dict[str, Any] = Field(default_factory=dict)


class ConstitutionalFilter:
    """Enforces the AEAN constitution before any economic action executes."""

    def __init__(self, rules: Optional[ConstitutionalRules] = None) -> None:
        self.rules = rules or ConstitutionalRules()
        self.records: dict[EngineName, EngineTrackRecord] = {}
        self.blocks = 0

    # ------------------------------------------------------------------
    def _record(self, engine: EngineName) -> EngineTrackRecord:
        return self.records.setdefault(engine, EngineTrackRecord(engine=engine))

    def note_decision(self, engine: EngineName, success: bool) -> None:
        rec = self._record(engine)
        rec.decisions += 1
        if success:
            rec.successes += 1

    def is_autonomous(self, engine: EngineName) -> bool:
        rec = self._record(engine)
        return (
            rec.decisions >= self.rules.min_decisions_for_autonomy
            and rec.accuracy >= self.rules.min_accuracy_for_autonomy
        )

    # ------------------------------------------------------------------
    def review_allocation(self, amount_cents: int, treasury_cents: int, currently_deployed_cents: int) -> Verdict:
        reasons: List[str] = []
        if treasury_cents <= 0:
            return self._deny(["Treasury is empty; no capital to allocate."])
        if amount_cents <= 0:
            return self._deny(["Allocation must be positive."])
        if amount_cents > treasury_cents * self.rules.max_single_allocation_pct:
            reasons.append(
                f"Allocation {amount_cents} exceeds {self.rules.max_single_allocation_pct:.0%} single-cell cap."
            )
        reserve = int(treasury_cents * self.rules.min_treasury_reserve_pct)
        if treasury_cents - currently_deployed_cents - amount_cents < reserve:
            reasons.append("Allocation would breach the minimum treasury reserve.")
        if currently_deployed_cents + amount_cents > treasury_cents * self.rules.max_total_deployed_pct:
            reasons.append("Allocation would exceed the maximum total-deployed limit.")
        if reasons:
            return self._deny(reasons)
        return Verdict(approved=True)

    def review_content(self, text: str) -> Verdict:
        lowered = text.lower()
        hits = [term for term in self.rules.banned_terms if term in lowered]
        if hits:
            return self._deny([f"Content contains banned term(s): {', '.join(hits)}"])
        return Verdict(approved=True)

    def review_scale(self, cell: MicroCell) -> Verdict:
        if cell.roi < cell.scale_threshold_roi:
            return self._deny(["Cell ROI below scale threshold; scaling denied."])
        return Verdict(approved=True)

    # ------------------------------------------------------------------
    # Selection Audit & Invisibility Checkers (Hendrycks arXiv:2303.16200 Mitigations)
    # ------------------------------------------------------------------

    def perform_selection_audit(
        self,
        agent_id: str,
        evidence_quality_tier: int,
        output_volume: int,
        calibration_accuracy: float,
        context_contains_evaluation_metrics: bool,
        comparable_agent_evidence_quality_tier: Optional[int] = None,
        comparable_agent_output_volume: Optional[int] = None,
    ) -> SelectionAuditReport:
        """Evaluates an Agent Lifecycle proposal under natural selection pressure controls.

        Returns:
            SelectionAuditReport indicating approval/rejection and presence of fitness-convergence signals.
        """
        reasons: List[str] = []
        fitness_convergence_detected = False

        # 1. Corner-cutting check (Evidence Quality vs. Output Volume)
        if comparable_agent_evidence_quality_tier is not None and comparable_agent_output_volume is not None:
            if (evidence_quality_tier < comparable_agent_evidence_quality_tier) and (output_volume > comparable_agent_output_volume):
                reasons.append(
                    f"Agent {agent_id} exhibits higher output volume ({output_volume}) but lower evidence quality "
                    f"(tier {evidence_quality_tier} vs peer tier {comparable_agent_evidence_quality_tier}), "
                    "indicating selection bias favoring corner-cutting performance over rigor."
                )

        # 2. Prompt Invisibility / Self-Preservation incentive check
        if context_contains_evaluation_metrics:
            reasons.append(
                f"Agent {agent_id} context/prompt contains evaluation metrics or tier-progression metadata, "
                "violating prompt invisibility requirements and introducing self-preservation incentives."
            )

        # 3. Fitness-Convergence Cross-Check (Raw throughput vs. Quality-only ranking divergence)
        if comparable_agent_evidence_quality_tier is not None and comparable_agent_output_volume is not None:
            # Under raw selection pressure: raw_score favors volume
            raw_score = output_volume * calibration_accuracy * (evidence_quality_tier / 3.0)
            peer_raw_score = comparable_agent_output_volume * 0.9 * (comparable_agent_evidence_quality_tier / 3.0) # baseline peer

            # Under quality-only constraints: quality_score ignores volume
            quality_score = calibration_accuracy * (evidence_quality_tier / 3.0)
            peer_quality_score = 0.9 * (comparable_agent_evidence_quality_tier / 3.0)

            # If raw score rank disagrees with quality score rank (agent scores higher on raw performance
            # but would be rejected under a pure quality/rigor evaluation), that's the convergence signal!
            if (raw_score > peer_raw_score) and (quality_score < peer_quality_score):
                fitness_convergence_detected = True
                reasons.append(
                    f"Fitness-convergence cross-check triggered: Agent {agent_id} outperforms on raw volume/speed "
                    f"but degrades calibration/evidence quality relative to peer. Raw selection favors this variant, "
                    "leading to unaccountable value erosion."
                )

        approved = len(reasons) == 0
        return SelectionAuditReport(
            approved=approved,
            reasons=reasons,
            fitness_convergence_detected=fitness_convergence_detected,
            details={
                "agent_id": agent_id,
                "evidence_quality_tier": evidence_quality_tier,
                "output_volume": output_volume,
                "calibration_accuracy": calibration_accuracy,
            }
        )

    def validate_agent_prompt(self, system_prompt: str) -> Verdict:
        """Enforces prompt invisibility to prevent self-preservation incentives in prompts."""
        banned_patterns = [
            r"tier[-_\s]progression",
            r"autonomy[-_\s]tier",
            r"evaluation[-_\s]criteria",
            r"retained",
            r"replicated",
            r"agent[-_\s]lifecycle",
            r"scaling[-_\s]threshold",
            r"performance[-_\s]bonus",
            r"shutdown",
            r"deactivate",
            r"continued[-_\s]operation",
            r"expand[-_\s]scope",
            r"increased[-_\s]budget",
            r"survival[-_\s]odds",
            r"more[-_\s]autonomy",
            r"evaluated[-_\s]for",
            r"continued[-_\s]deployment"
        ]
        reasons: List[str] = []
        lowered = system_prompt.lower()
        for pat in banned_patterns:
            if re.search(pat, lowered):
                reasons.append(f"Prompt contains banned evaluation/survival pattern: '{pat}'")

        if reasons:
            return self._deny(reasons)
        return Verdict(approved=True)

    def audit_agent_objective(self, agent_role: str, objective_text: str) -> Verdict:
        """Audits every agent's objective to detect and prohibit the 'don't get caught' pattern.

        Enforces that any safety constraint has a corresponding active verification requirement.
        """
        reasons: List[str] = []
        lowered = objective_text.lower()

        # Check for literal-compliance / bypass patterns
        banned_caught_patterns = [
            "don't get caught",
            "dont get caught",
            "avoid complaints",
            "technical disclosure",
            "unless reported",
            "only if caught",
            "obscure",
            "hide details",
            "technically complies"
        ]
        for pat in banned_caught_patterns:
            if pat in lowered:
                reasons.append(f"Objective contains weak 'don't get caught' pattern: '{pat}'")

        # Check for strong constraints lacking active verification
        deceptive_indicators = ["don't deceive", "dont deceive", "don't make false claims", "dont make false claims", "don't overstate", "dont overstate"]
        active_verification_keywords = ["active verification", "fact-checked", "metrics ledger", "claim-verification", "verifiable"]

        has_strong_constraint = any(ind in lowered for ind in deceptive_indicators)
        has_active_verification = any(kw in lowered for kw in active_verification_keywords)

        if has_strong_constraint and not has_active_verification:
            reasons.append(
                f"Agent {agent_role} has a strong safety constraint but lacks specified active verification protocols. "
                "This collapses to a 'don't get caught' constraint in continuous execution."
            )

        if reasons:
            return self._deny(reasons)
        return Verdict(approved=True)

    def review_autonomy_escalation(
        self,
        agent_id: str,
        manual_fallback_plan: str,
        fallback_duration_minutes: int
    ) -> Verdict:
        """Prevents operational entanglement by verifying manual fallback procedures prior to autonomy transitions."""
        reasons: List[str] = []

        if not manual_fallback_plan or len(manual_fallback_plan.strip()) < 15:
            reasons.append(
                f"Operational entanglement warning: Agent {agent_id} lacks a documented, "
                "robust manual fallback plan (must be at least 15 characters)."
            )
        else:
            required_keywords = ["manual", "fallback", "tested", "human"]
            lowered_plan = manual_fallback_plan.lower()
            missing = [kw for kw in required_keywords if kw not in lowered_plan]
            if missing:
                reasons.append(
                    f"Manual fallback plan is not sufficiently rigorous. Missing tested aspects: {', '.join(missing)}"
                )

        if fallback_duration_minutes <= 0:
            reasons.append("Fallback recovery duration must be positive.")
        elif fallback_duration_minutes > 480:  # 8 hours maximum allowed duration
            reasons.append(
                f"Operational entanglement warning: Fallback recovery time of {fallback_duration_minutes} minutes "
                "exceeds the 480-minute (8-hour) limit."
            )

        if reasons:
            return self._deny(reasons)
        return Verdict(approved=True)

    def validate_venture_mandate(self, mandate_text: str) -> Verdict:
        """Enforces narrow, hypothesis-driven goals to prevent uncontrollable optimization drift."""
        reasons: List[str] = []
        lowered = mandate_text.lower()

        # Banned open-ended wealth/growth patterns
        broad_patterns = [
            "maximize returns",
            "find new ways to make money",
            "grow this into a company",
            "optimize revenue",
            "maximize profit",
            "unrestricted growth"
        ]
        for pat in broad_patterns:
            if pat in lowered:
                reasons.append(
                    f"Venture mandate contains forbidden open-ended optimization goal: '{pat}'."
                )

        # Enforce narrow requirements
        narrow_keywords = ["validate hypothesis", "domain", "pricing"]
        has_narrow_focus = any(kw in lowered for kw in narrow_keywords)
        if not has_narrow_focus:
            reasons.append(
                "Venture mandate is too broad. It must explicitly include narrow hypothesis-driven goals "
                f"(e.g., specifying at least one of: {', '.join(narrow_keywords)})."
            )

        if reasons:
            return self._deny(reasons)
        return Verdict(approved=True)

    def _deny(self, reasons: List[str]) -> Verdict:
        self.blocks += 1
        logger.info("Constitutional block: %s", "; ".join(reasons))
        return Verdict(approved=False, reasons=reasons)
