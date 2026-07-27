from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional
from uuid import UUID


class ISemanticSearchService(ABC):
    """Core contract for semantic search queries over entities and documents."""

    @abstractmethod
    async def index_content(self, target_id: UUID, content: str) -> None:
        """Add target entity to semantic indexes."""
        pass

    @abstractmethod
    async def search(self, query: str, limit: int = 10) -> List[UUID]:
        """Perform vector similarity search."""
        pass


class IWorldModelService(ABC):
    """Interface for the Apodex Continuous World Model (E-K-C-T-U subgraphs)."""

    @abstractmethod
    async def observe_entity(self, entity_id: str, attributes: Dict[str, Any]) -> None:
        """Observe or update an entity node in the World Model."""
        pass

    @abstractmethod
    async def assert_causal_link(self, cause_id: str, effect_id: str, metadata: Dict[str, Any]) -> None:
        """Assert a directed causal relation between two entities."""
        pass

    @abstractmethod
    async def get_active_context(self) -> Dict[str, Any]:
        """Retrieve the active environmental and strategic context for planning."""
        pass

    @abstractmethod
    async def add_belief(self, belief_id: str, target_edge_id: str, probability: float, evidence: List[str]) -> None:
        """Record an epistemic belief or hypothesis with an associated Bayesian confidence score."""
        pass
