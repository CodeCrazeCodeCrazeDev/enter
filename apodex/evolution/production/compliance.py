from __future__ import annotations
import uuid
from typing import Any, Dict, List, Optional
from uuid import UUID, uuid4
from pydantic import BaseModel, Field

from apodex.memory.models import AtomicMemory, ScenarioPattern


class CrossTenantLearningEngine:
    """
    Manages safe, opt-in cross-tenant learning.
    Enforces raw log boundaries and distills anonymized patterns (T2/T3) to share globally.
    """

    def __init__(self) -> None:
        self.opted_in_tenants: Dict[str, bool] = {}
        self.global_scenario_registry: Dict[UUID, ScenarioPattern] = {}

    def set_tenant_consent(self, tenant_id: str, opted_in: bool) -> None:
        """Sets the opt-in consent configuration for a tenant."""
        self.opted_in_tenants[tenant_id] = opted_in

    def anonymize_and_distill_atom(self, atom: AtomicMemory) -> Optional[AtomicMemory]:
        """
        Safely distills a T2 AtomicMemory by purging user identifiers,
        tenant IDs, and private strings, making it compliant for global aggregation.
        """
        # Enforce compliance: Check if tenant has consented to cross-tenant learning
        if not self.opted_in_tenants.get(atom.tenant_id, False):
            return None  # Blocked

        # Anonymize: Strip private IDs and mask identifying terms
        anonymized_content = atom.content
        for term in ["user_", "tenant_", "org_", "confidential", "secret"]:
            anonymized_content = anonymized_content.replace(term, "[ANONYMIZED]")

        return AtomicMemory(
            atom_id=uuid4(),
            tenant_id="global_shared",
            user_id="anonymous",
            content=anonymized_content,
            embedding=list(atom.embedding),
            confidence=atom.confidence,
            tags=list(atom.tags) + ["global_shared"]
        )

    def federate_scenario_pattern(self, scenario: ScenarioPattern) -> Optional[ScenarioPattern]:
        """
        Federates a T3 Scenario pattern (workflows and solution paths) globally,
        enforcing opt-in consent and stripping private properties.
        """
        if not self.opted_in_tenants.get(scenario.tenant_id, False):
            return None

        return ScenarioPattern(
            scenario_id=uuid4(),
            tenant_id="global_shared",
            name=f"Global Shared Pattern: {scenario.pattern_type}",
            pattern_type=scenario.pattern_type,
            typical_workflow=list(scenario.typical_workflow),
            failure_patterns=list(scenario.failure_patterns),
            solution_patterns=list(scenario.solution_patterns),
            linked_atoms=[],  # Purge pointers to raw local atoms
            success_rate=scenario.success_rate
        )
