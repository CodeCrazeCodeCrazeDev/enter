from __future__ import annotations
import time
from typing import Any, Dict, List, Optional
from uuid import UUID, uuid4
from pydantic import BaseModel, Field

from apodex.memory.models import ResearchTicket, ScenarioPattern, AtomicMemory, CapabilityDelta
from apodex.safety.core import ImmutableSafetyCore, RiskTier


class ArchitectureCandidate(BaseModel):
    """Represents a proposed model configuration, agent topology, or hybrid architecture."""
    candidate_id: UUID = Field(default_factory=uuid4)
    ticket_id: UUID
    name: str
    target_capability: str
    risk_tier: RiskTier
    model_configuration: Dict[str, Any] = Field(
        default_factory=dict,
        description="e.g. {'model_family': 'claude-3-5-sonnet', 'max_tokens': 4000}"
    )
    agent_topology: List[str] = Field(
        default_factory=list,
        description="e.g. ['planner', 'executor', 'verifier']"
    )
    hypothesis: str


class ResearchTicketManager:
    """
    Scans memory stores (T3 Scenarios) for persistent weaknesses,
    prioritizes issues, and manages active research tasks.
    """

    def __init__(self, tencent_db: Any) -> None:
        self.db = tencent_db

    def scan_for_weaknesses(self, tenant_id: str) -> List[ResearchTicket]:
        """
        Scans T3 Scenarios for success rates below threshold (e.g. < 80%)
        or average token cost that is too high, creating prioritized ResearchTickets.
        """
        tickets_created: List[ResearchTicket] = []

        for scenario in self.db.scenarios.values():
            if scenario.tenant_id != tenant_id:
                continue

            # Identify weakness: low success rate
            if scenario.success_rate < 0.95:
                ticket = ResearchTicket(
                    ticket_id=uuid4(),
                    tenant_id=tenant_id,
                    title=f"Resolve low success rate in {scenario.name}",
                    failure_description=(
                        f"Scenario {scenario.name} has a persistent low success rate "
                        f"of {scenario.success_rate:.2f}."
                    ),
                    related_episode_ids=[],
                    related_atom_ids=scenario.linked_atoms,
                    priority=2 if scenario.success_rate < 0.8 else 3,
                    status="queued"
                )
                self.db.scenarios[scenario.scenario_id].failure_patterns.append("low_success_rate")
                tickets_created.append(ticket)

        return tickets_created


class ResearchAgent:
    """
    Takes a ResearchTicket and formulates structured ArchitectureCandidate proposals,
    collaborating with the ImmutableSafetyCore to assign risk tiers.
    """

    def __init__(self, safety_core: Optional[ImmutableSafetyCore] = None) -> None:
        self.safety_core = safety_core or ImmutableSafetyCore()

    def propose_candidate(self, ticket: ResearchTicket, name: str, hypothesis: str) -> ArchitectureCandidate:
        """
        Proposes a new architecture candidate based on the ticket description,
        then evaluates and attaches the safety RiskTier.
        """
        # Determine target capability based on ticket title
        target_capability = "harness_workflow"
        if "coherence" in ticket.failure_description.lower():
            target_capability = "long_horizon_reasoning"
        elif "cost" in ticket.failure_description.lower():
            target_capability = "token_cost_optimization"

        # Determine risk tier based on proposed changes
        # E.g. modifying model or safety core has a higher risk tier
        risk_tier = RiskTier.TIER_1_LOW
        if "model" in name.lower() or "claude" in name.lower() or "gpt" in name.lower():
            risk_tier = RiskTier.TIER_3_HIGH
        elif "topology" in name.lower() or "parallel" in name.lower():
            risk_tier = RiskTier.TIER_2_MEDIUM

        return ArchitectureCandidate(
            ticket_id=ticket.ticket_id,
            name=name,
            target_capability=target_capability,
            risk_tier=risk_tier,
            model_configuration={"model_family": "claude-3-5-sonnet"} if risk_tier == RiskTier.TIER_3_HIGH else {},
            agent_topology=["planner", "executor", "verifier"] if risk_tier == RiskTier.TIER_2_MEDIUM else ["main_agent"],
            hypothesis=hypothesis
        )
