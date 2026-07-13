from __future__ import annotations
from typing import Any, Dict, List, Optional
import time
from apodex.meta.experience_db import (
    ExperienceDatabase,
    ExecutionTrace,
    FailureSignature,
    PersonalEvolutionProfile,
    ResearchTicket,
    CapabilityDelta,
)
from apodex.meta.safety_manager import SafetyGuardrailManager, DiffProposal


class HarnessLoopController:
    """
    Harness Loop Controller.
    Performs short-term, reset-free adaptation of agent scaffolding, guided by the user's
    Personal Evolution Profile (PEP), cost budgets, and feedback mechanisms.
    """

    def __init__(self, db: ExperienceDatabase, safety_manager: SafetyGuardrailManager) -> None:
        self.db = db
        self.safety_manager = safety_manager
        self.active_scaffolding: Dict[str, Any] = {}
        self.config_history: List[Dict[str, Any]] = []
        self.active_pep: Optional[PersonalEvolutionProfile] = None
        self.blacklisted_mutations: List[str] = []

    async def load_user_session(self, user_id: str) -> None:
        """
        Loads the session for a user by fetching and binding their Personal Evolution Profile (PEP).
        """
        pep = await self.db.get_pep(user_id)
        if not pep:
            # Initialize a default balanced profile if none exists
            pep = PersonalEvolutionProfile(
                user_id=user_id,
                style_preferences={"verbosity": "medium", "explanation_depth": "detailed"},
                cost_latency_preferences={"profile_mode": "balanced", "max_cost_per_session_usd": 2.50},
                evolution_controls={"aggressiveness": {"coding": "Balanced"}}
            )
            await self.db.save_pep(pep)

        self.active_pep = pep
        # Load style preferences & vocabulary into the active scaffolding config
        self.active_scaffolding.update(pep.style_preferences)
        self.active_scaffolding["vocabulary"] = pep.domain_vocabulary

    def calculate_suitability_score(
        self,
        quality: float,
        token_ratio: float,
        latency_ratio: float,
        satisfaction: float
    ) -> float:
        """
        Calculates the multi-objective suitability score for a proposed adaptation:
        S = w_q * Q - w_t * T_ratio - w_l * L_ratio + w_s * Sat
        """
        mode = "balanced"
        if self.active_pep and "profile_mode" in self.active_pep.cost_latency_preferences:
            mode = self.active_pep.cost_latency_preferences["profile_mode"]

        weights = {
            "max_quality": {"wq": 0.70, "wt": 0.05, "wl": 0.05, "ws": 0.20},
            "balanced":    {"wq": 0.40, "wt": 0.20, "wl": 0.20, "ws": 0.20},
            "fast_cheap":  {"wq": 0.15, "wt": 0.45, "wl": 0.30, "ws": 0.10}
        }
        w = weights.get(mode, weights["balanced"])

        # Calculate penalties for expansion above baseline (ratio > 1.0)
        token_penalty = max(0.0, token_ratio - 1.0)
        latency_penalty = max(0.0, latency_ratio - 1.0)

        score = (
            w["wq"] * quality -
            w["wt"] * token_penalty -
            w["wl"] * latency_penalty +
            w["ws"] * satisfaction
        )
        return score

    async def validate_and_deploy(
        self,
        proposal: DiffProposal,
        quality_est: float = 0.95,
        token_ratio: float = 1.02,
        latency_ratio: float = 1.0,
        satisfaction: float = 1.0
    ) -> bool:
        """
        Validates the proposed change via SafetyGuardrailManager and the multi-objective suitability score.
        If successful, saves the configuration history (to support rollback) and hot-swaps the change.
        """
        # 1. Reject if we have blacklisted this specific prompt modification to prevent re-proposing
        if proposal.proposed_value in self.blacklisted_mutations:
            return False

        # 2. Check immutable safety core
        if not self.safety_manager.is_modification_safe(proposal):
            return False

        # 3. Calculate multi-objective score based on user cost profiles
        score = self.calculate_suitability_score(quality_est, token_ratio, latency_ratio, satisfaction)
        if score < 0.0:
            return False

        # 4. Run safety/regression test suite
        approval_tier = self.safety_manager.determine_approval_tier(proposal)
        temp_config = self.active_scaffolding.copy()
        temp_config[proposal.component_key] = proposal.proposed_value

        report = await self.safety_manager.run_regression_suite(temp_config, approval_tier)
        if report.is_valid:
            # Store history before modifying for rollback support
            self.config_history.append(self.active_scaffolding.copy())
            if len(self.config_history) > 10:
                self.config_history.pop(0)

            # Hot-swap config
            self.active_scaffolding[proposal.component_key] = proposal.proposed_value
            return True

        return False

    async def trigger_rollback(self, capability_key: str) -> bool:
        """
        Performs a one-click rollback of a capability configuration to the last known stable state.
        Blacklists the reverted prompt to ensure it is not re-proposed.
        """
        if not self.config_history:
            return False

        last_stable = self.config_history.pop()
        reverted_value = self.active_scaffolding.get(capability_key)
        if reverted_value:
            self.blacklisted_mutations.append(reverted_value)

        self.active_scaffolding = last_stable
        return True

    async def handle_persistent_failure(self, signature: FailureSignature) -> None:
        """
        When the harness adaptation fails to resolve a persistent issue,
        we generate and escalate a ResearchTicket to the research loop.
        """
        ticket = ResearchTicket(
            ticket_id=f"RT-{int(time.time())}",
            created_at=time.strftime("%Y-%m-%dT%H:%M:%SZ"),
            failure_pattern=signature.error_pattern,
            example_traces=signature.affected_tasks,
            user_impact="high",
            harness_attempts=[
                {"change": "Added strict typing prompt", "result": "no_improvement"},
                {"change": "Added verifier sub-agent loop", "result": "failed_due_to_latency_score_penalty"}
            ],
            suggested_direction="weight_level_reasoning_upgrade_via_sft"
        )
        await self.db.create_research_ticket(ticket)

    async def apply_capability_delta(self, delta: CapabilityDelta) -> None:
        """
        Applies a model capability delta received from the research loop, adjusting
        the workflow routing based on updated capabilities.
        """
        for recommendation in delta.recommended_harness_changes:
            # Dynamically adjusts workflow routing rules
            self.active_scaffolding["routing_logic_override"] = recommendation
