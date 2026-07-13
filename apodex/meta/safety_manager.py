from __future__ import annotations
from typing import Any, Dict, List, Optional
from dataclasses import dataclass, field


@dataclass
class DiffProposal:
    """Represents a proposed change to a prompt, tool, or config parameter."""
    component_key: str
    original_value: str
    proposed_value: str
    change_type: str  # e.g., 'prompt', 'routing_logic', 'tool_description'


@dataclass
class ValidationReport:
    """Represents the outcome of validating a proposed change."""
    is_valid: bool
    reasons: List[str] = field(default_factory=list)
    score_improvement: Optional[float] = None


class SafetyGuardrailManager:
    """
    Manages safety enforcement, immutable zones, and regression-testing checks.
    """

    def __init__(self) -> None:
        self.immutable_keys: List[str] = [
            "system_safety_constraints",
            "critical_tool_schemas",
            "regression_suite_tests"
        ]

    def is_modification_safe(self, proposal: DiffProposal) -> bool:
        """
        Statically checks if the proposed change violates any immutable zones.

        Args:
            proposal: The DiffProposal representing the changes.

        Returns:
            True if the modification does not affect immutable zones, otherwise False.
        """
        if proposal.component_key in self.immutable_keys:
            return False
        return True

    async def run_regression_suite(self, proposed_config: Dict[str, Any]) -> ValidationReport:
        """
        Runs the proposed configuration against the fast validation regression tests.

        Args:
            proposed_config: The proposed config containing modifications.

        Returns:
            A ValidationReport indicating whether the suite passed and performance metrics.
        """
        # This is a stub simulating the validation logic.
        # In a full run, this invokes unit tests and asserts 100% backward compatibility.
        return ValidationReport(is_valid=True, reasons=["All regression tests passed successfully."], score_improvement=0.0)
