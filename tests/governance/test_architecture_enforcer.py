from __future__ import annotations

import pytest
from apodex.governance.architecture_verifier import ArchitectureVerifier, ArchitecturalVetoError


def test_verifier_seeds_singular_capability_owners():
    verifier = ArchitectureVerifier()
    # Pre-seeded canonical ownership should hold true
    assert verifier.verify_boundary_registration(
        subsystem_name="apodex/cognition/planning/unified_planner.py",
        capability="Planning"
    )

    with pytest.raises(ArchitecturalVetoError, match="Boundary validation failed"):
        # Unregistered calling owner must be rejected
        verifier.verify_boundary_registration(
            subsystem_name="agent_harness/core/v2/unauthorized_agent.py",
            capability="Planning"
        )


def test_verifier_blocks_duplicate_or_overlapping_registration():
    verifier = ArchitectureVerifier()

    # Registering custom unique capability succeeds
    verifier.register_subsystem_capability(
        subsystem_name="apodex/custom_subsystem.py",
        capability="CustomSubsystemCore"
    )
    assert verifier.verify_boundary_registration("apodex/custom_subsystem.py", "CustomSubsystemCore")

    # Attempting to register existing/pre-seeded canonical capability by another owner fails
    with pytest.raises(ArchitecturalVetoError, match="Duplicate capability ownership violation"):
        verifier.register_subsystem_capability(
            subsystem_name="agent_harness/core/v2/malicious_planner.py",
            capability="Planning"
        )


def test_verifier_rejects_unregistered_capability_execution():
    verifier = ArchitectureVerifier()
    with pytest.raises(ArchitecturalVetoError, match="not registered under Cognitive OS"):
        verifier.verify_boundary_registration(
            subsystem_name="apodex/custom_subsystem.py",
            capability="UnknownSuperPower"
        )
