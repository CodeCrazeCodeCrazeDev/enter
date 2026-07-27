"""Abstract Service Interfaces for the AI-EOS operating system.

These interfaces define the stable contracts across all bounded contexts, preventing
circular dependencies and enforcing loose coupling.
"""

from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Any, Callable, Dict, List, Optional, Type, TypeVar
from uuid import UUID
from ..domain.models import VentureCell, Hypothesis, Experiment, Capability, DecisionProvenance
from ..domain.events import DomainEvent
from ..domain.commands import DomainCommand

E = TypeVar("E", bound=DomainEvent)
C = TypeVar("C", bound=DomainCommand)


class IEventBus(ABC):
    """Core Event-Driven Pub-Sub contract."""

    @abstractmethod
    def subscribe(self, event_type: Type[E], handler: Callable[[E], Any]) -> None:
        """Register a callback for a specific event type."""
        pass

    @abstractmethod
    def publish(self, event: DomainEvent) -> None:
        """Publish an event to all subscribed handlers."""
        pass


class ICommandDispatcher(ABC):
    """Core Command dispatch routing contract."""

    @abstractmethod
    def register_handler(self, command_type: Type[C], handler: Callable[[C], Any]) -> None:
        """Register a handler for a specific command."""
        pass

    @abstractmethod
    def dispatch(self, command: DomainCommand) -> Any:
        """Dispatch a command to its registered handler."""
        pass


class IResearchOS(ABC):
    """Contract for scientific hypothesis registration and validation."""

    @abstractmethod
    def register_hypothesis(self, title: str, description: str, null_hypothesis: str, target_metric: str, significance_alpha: float = 0.05) -> Hypothesis:
        pass

    @abstractmethod
    def create_experiment(self, hypothesis_id: UUID, seed: int = 42) -> Experiment:
        pass

    @abstractmethod
    def execute_experiment_simulation(self, experiment_id: UUID, ground_truth_yield: float) -> Experiment:
        """Run statistical walk-forward validation and White's reality checks in a sandbox simulator."""
        pass


class IKnowledgeInfrastructure(ABC):
    """Contract for the Institutional Knowledge Graph (IKG) and T0-T4 Memory."""

    @abstractmethod
    def record_node(self, node_id: str, node_type: str, properties: Dict[str, Any]) -> None:
        pass

    @abstractmethod
    def record_edge(self, source_id: str, target_id: str, relation_type: str, weight: float = 1.0) -> None:
        pass

    @abstractmethod
    def get_provenance_lineage(self, capability_id: str) -> List[Dict[str, Any]]:
        """Traverse the IKG to answer questions about capability origins/experiments."""
        pass


class IExecutiveOptimizer(ABC):
    """Contract for constrained active inference, portfolio allocation, and belief updating."""

    @abstractmethod
    def update_beliefs(self, cell: VentureCell, actual_revenue: int, expected_revenue: int) -> VentureCell:
        """Execute Bayesian update of belief states based on observation prediction errors."""
        pass

    @abstractmethod
    def compute_composite_objective(self, cell: VentureCell, policy_expected_utility: float, policy_risk: float) -> float:
        """Calculate G = EconomicUtility - RiskPenalty - ComputeCost + InformationGain - GovernancePenalty."""
        pass

    @abstractmethod
    def optimize_allocations(self, cells: List[VentureCell], total_budget_cents: int) -> Dict[UUID, int]:
        """Solve multi-objective portfolio budget allocation subject to risk and capacity ceilings."""
        pass


class IExecutionBackend(ABC):
    """Contract for coordinating legacy execution engines (AEAN Organism, ARCS) as replaceable services."""

    @abstractmethod
    def run_cycle(self, cell_id: UUID, capital_cents: int) -> Dict[str, Any]:
        """Drive a physical or simulated flywheel execution run of AEAN/ARCS."""
        pass


class ICapabilityRegistry(ABC):
    """Definitive ledger managing capability lineages, rollbacks, and active deployments."""

    @abstractmethod
    def register_capability(self, capability: Capability) -> None:
        pass

    @abstractmethod
    def get_capability(self, capability_id: str) -> Optional[Capability]:
        pass

    @abstractmethod
    def trigger_rollback(self, capability_id: str, reason: str) -> bool:
        pass


class IGovernanceGateway(ABC):
    """Gating mechanism for multi-criteria policy and architectural check evaluations."""

    @abstractmethod
    def evaluate_action(self, action_type: str, risk_score: float, context: Dict[str, Any]) -> Dict[str, Any]:
        """Check safety, legal, risk, ethic, budget, and human approval limits."""
        pass

    @abstractmethod
    def evaluate_architecture_conformance(self, capability: Capability) -> bool:
        """Validate that a new capability does not duplicate or violate bounded contexts."""
        pass
