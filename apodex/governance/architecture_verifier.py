"""Architectural Verification & Runtime Boundary Enforcement.

Enforces singular capability ownership across the unified Cognitive Operating System,
blocking unauthorized, overlapping, or bypass capability execution.
"""
from __future__ import annotations

import logging
from typing import Dict, Set

logger = logging.getLogger("apodex.governance.architecture_verifier")


class ArchitecturalVetoError(Exception):
    """Exception raised when an unauthorized or overlapping capability execution is detected."""
    pass


class ArchitectureVerifier:
    """Rigorous runtime enforcer of the five-layer boundary boundaries."""

    def __init__(self) -> None:
        # Pre-seed the singular, non-duplicative capability ownership map.
        self._capability_owners: Dict[str, str] = {
            "Planning": "apodex/cognition/planning/unified_planner.py",
            "WorldModel": "apodex/world_model/world_model.py",
            "Memory": "apodex/memory/semantic_memory.py",
            "CausalInference": "apodex/ai_eos/intelligence/decision_engine.py",
            "MultipleTestingCorrection": "apodex/research_os/pipeline.py",
            "ConstitutionalSafety": "apodex/aean/governance.py",
            "EMNodeMining": "apodex/memory/emg_engine.py",
        }
        self._active_registrations: Dict[str, str] = {}

    def register_subsystem_capability(self, subsystem_name: str, capability: str) -> None:
        """Registers a subsystem capability, enforcing strict singular ownership."""
        expected_owner = self._capability_owners.get(capability)
        if not expected_owner:
            # Open capability, register it
            self._capability_owners[capability] = subsystem_name
            expected_owner = subsystem_name

        if expected_owner != subsystem_name:
            # Overlapping/duplicate ownership detected!
            raise ArchitecturalVetoError(
                f"Duplicate capability ownership violation! Capability '{capability}' is authoritatively "
                f"owned by '{expected_owner}', but subsystem '{subsystem_name}' attempted to register it."
            )

        self._active_registrations[capability] = subsystem_name
        logger.info("Successfully verified and registered capability '%s' to owner '%s'.", capability, subsystem_name)

    def verify_boundary_registration(self, subsystem_name: str, capability: str) -> bool:
        """Verifies if the calling subsystem has authorized singular ownership of the capability."""
        owner = self._capability_owners.get(capability)
        if not owner:
            # Capability unregistered
            raise ArchitecturalVetoError(
                f"Boundary validation failed! Capability '{capability}' is not registered under Cognitive OS."
            )

        if owner != subsystem_name:
            raise ArchitecturalVetoError(
                f"Boundary validation failed! Subsystem '{subsystem_name}' attempted to execute capability "
                f"'{capability}' which is authoritatively owned by '{owner}'."
            )

        return True
