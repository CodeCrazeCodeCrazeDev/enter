from __future__ import annotations
from typing import List
from uuid import UUID


class GraphIndexingService:
    """Manages high-performance vector and term indexes for quick entity retrieval."""

    async def index_entity(self, tenant_id: str, entity_id: UUID, text_content: str) -> None:
        """Adds or updates an entity in the vector and semantic index."""
        pass

    async def semantic_search(self, tenant_id: str, query: str, limit: int = 10) -> List[UUID]:
        """Performs semantic vector query over indexed entities."""
        return []
