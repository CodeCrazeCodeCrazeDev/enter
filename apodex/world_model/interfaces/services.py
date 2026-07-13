from __future__ import annotations
from abc import ABC, abstractmethod
from typing import List
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
