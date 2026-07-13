from __future__ import annotations
from typing import Any, Dict, List, Optional
from apodex.meta.experience_db import ExperienceDatabase, ExecutionTrace, FailureSignature
from apodex.meta.safety_manager import SafetyGuardrailManager, DiffProposal


class HarnessLoopController:
    """
    Harness Loop Controller (Continual Harness & Self-Harness style).
    Executes short-term, reset-free adaptation of agent scaffolding.
    """

    def __init__(self, db: ExperienceDatabase, safety_manager: SafetyGuardrailManager) -> None:
        self.db = db
        self.safety_manager = safety_manager
        self.active_scaffolding: Dict[str, Any] = {}

    async def mine_weaknesses(self) -> List[FailureSignature]:
        """
        Scans trace records and error signatures to identify frequent failures.

        Returns:
            A list of FailureSignatures representing current weaknesses.
        """
        # Scans the experience database for frequent errors
        signatures = await self.db.get_all_failure_signatures()
        # Filter or rank signatures that require immediate prompt/workflow adjustments
        return [sig for sig in signatures if sig.occurrence_count >= 3]

    async def propose_harness_edit(self, weakness: FailureSignature) -> Optional[DiffProposal]:
        """
        Generates a diff-style prompt/tool description adjustment to solve a weakness.

        Args:
            weakness: The target FailureSignature to address.

        Returns:
            A DiffProposal object containing the recommended change, or None.
        """
        # Simulates prompt engineering / mutation using TextGrad-style meta-prompting
        if "JSON" in weakness.error_pattern:
            return DiffProposal(
                component_key="coding_assistant_system_prompt",
                original_value="You are a coding assistant...",
                proposed_value="You are a coding assistant... Format your tool call in pure JSON.",
                change_type="prompt"
            )
        return None

    async def validate_and_deploy(self, proposal: DiffProposal) -> bool:
        """
        Validates the proposed change via SafetyGuardrailManager.
        If successful, hot-swaps the change into active_scaffolding.

        Args:
            proposal: The DiffProposal to test and deploy.

        Returns:
            True if deployed, otherwise False.
        """
        # 1. Check static safety constraints
        if not self.safety_manager.is_modification_safe(proposal):
            return False

        # 2. Run fast validation suite
        temp_config = self.active_scaffolding.copy()
        temp_config[proposal.component_key] = proposal.proposed_value

        report = await self.safety_manager.run_regression_suite(temp_config)
        if report.is_valid:
            # 3. Hot-swap configuration
            self.active_scaffolding[proposal.component_key] = proposal.proposed_value
            return True

        return False
